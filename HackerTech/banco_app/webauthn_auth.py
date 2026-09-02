"""
Segundo factor: confirmacion FIDO2/WebAuthn real (huella/PIN/rostro via el
autenticador de plataforma del sistema operativo, o una llave de seguridad
externa tipo YubiKey).

Adaptado desde ../utn_frc_redesign/webauthn_auth.py a la estructura de
HackerBank (no se comparte modulo entre proyectos, se copia y adapta).

------------------------------------------------------------------
COMO FUNCIONA EL SEGUNDO FACTOR:
------------------------------------------------------------------
El usuario ya fue identificado en el paso 1 (email + contraseña, ver
app.py `/api/login`). Por eso `build_authentication_options` recibe el
usuario y arma un `allow_credentials` acotado a SUS propias credenciales:
el navegador solo ofrece esas, no cualquiera guardada en el dispositivo.

La biometria (huella, rostro, PIN del autenticador) nunca sale del
dispositivo del usuario: solo se usa localmente para desbloquear la clave
privada que firma un challenge aleatorio de un solo uso. El servidor jamas
recibe datos biometricos.

El challenge se guarda en la sesion de Flask (cookie firmada) entre el
`begin` y el `complete`, no en la base de datos: es efimero y de un solo uso.
------------------------------------------------------------------
"""
import webauthn
from webauthn.helpers.structs import (
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)

import config
import db

# authenticator_attachment se recibe como parametro (ver
# build_registration_options): PLATFORM fuerza que el navegador solo
# ofrezca el autenticador integrado (Windows Hello, Touch ID); CROSS_PLATFORM
# fuerza que solo ofrezca uno externo (YubiKey u otra llave FIDO2 por
# USB/NFC/BLE). No hay un tercer valor "cualquiera" en el estandar: si se
# quiere dejar la eleccion abierta hay que pasar None. app.py decide cual
# de los dos pedir segun el boton que toco el usuario en el dashboard.
#
# Esta restriccion NO existe para generate_authentication_options() (login):
# el estandar WebAuthn no tiene authenticatorAttachment en las opciones de
# autenticacion, solo en las de registro. En el login, lo que efectivamente
# acota que autenticador sirve es allow_credentials (ver
# build_authentication_options): el navegador solo va a poder completar la
# operacion con un autenticador que tenga una de esas credenciales guardadas.


def build_registration_options(user, rp_id, authenticator_attachment=None):
    """Genera las opciones para registrar una passkey de ESTE usuario ya logueado.

    authenticator_attachment: AuthenticatorAttachment.PLATFORM,
    AuthenticatorAttachment.CROSS_PLATFORM, o None (sin restriccion).
    """
    existing_credentials = db.get_webauthn_credentials_for_user(user["id"])
    exclude_credentials = [
        PublicKeyCredentialDescriptor(id=cred["credential_id"])
        for cred in existing_credentials
    ]

    authenticator_selection = AuthenticatorSelectionCriteria(
        authenticator_attachment=authenticator_attachment,
        # PREFERRED (no DISCOURAGED): pedimos credencial discoverable/resident
        # cuando el autenticador lo soporte, para que quede listada en apps
        # como Yubico Authenticator. No es indispensable para el login de
        # HackerBank (allow_credentials ya acota la credencial sin necesitar
        # esto - ver comentario mas arriba), pero no tiene costo funcional y
        # mejora la visibilidad/gestion del lado del usuario. PREFERRED en vez
        # de REQUIRED para no romper el registro en autenticadores viejos que
        # no soporten resident keys.
        resident_key=ResidentKeyRequirement.PREFERRED,
        user_verification=UserVerificationRequirement.REQUIRED,
    )

    options = webauthn.generate_registration_options(
        rp_id=rp_id,
        rp_name=config.WEBAUTHN_RP_NAME,
        user_id=str(user["id"]).encode("utf-8"),
        user_name=user["email"],
        user_display_name=f"{user['first_name']} {user['last_name']}",
        authenticator_selection=authenticator_selection,
        exclude_credentials=exclude_credentials,
    )
    return options


def complete_registration(user, credential_json, expected_challenge, rp_id, origin):
    parsed_credential = webauthn.helpers.parse_registration_credential_json(credential_json)

    verification = webauthn.verify_registration_response(
        credential=parsed_credential,
        expected_challenge=expected_challenge,
        expected_rp_id=rp_id,
        expected_origin=origin,
        require_user_verification=True,
    )

    db.save_webauthn_credential(
        user_id=user["id"],
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
    )
    return True


def build_authentication_options(user, rp_id):
    """Opciones de autenticacion acotadas a las credenciales de un usuario
    YA identificado por email/contraseña (segundo factor).
    """
    existing_credentials = db.get_webauthn_credentials_for_user(user["id"])
    allow_credentials = [
        PublicKeyCredentialDescriptor(id=cred["credential_id"])
        for cred in existing_credentials
    ]

    options = webauthn.generate_authentication_options(
        rp_id=rp_id,
        allow_credentials=allow_credentials,
        user_verification=UserVerificationRequirement.REQUIRED,
    )
    return options


def complete_authentication(user, credential_json, expected_challenge, rp_id, origin):
    """Verifica que la firma corresponda a una credencial de ESTE usuario.

    Levanta ValueError si la credencial es desconocida, pertenece a otro
    usuario, o la firma no valida.
    """
    parsed_credential = webauthn.helpers.parse_authentication_credential_json(credential_json)

    stored_credential = db.get_webauthn_credential_by_id(parsed_credential.raw_id)
    if stored_credential is None or stored_credential["user_id"] != user["id"]:
        raise ValueError("Credencial desconocida para este usuario.")

    verification = webauthn.verify_authentication_response(
        credential=parsed_credential,
        expected_challenge=expected_challenge,
        expected_rp_id=rp_id,
        expected_origin=origin,
        credential_public_key=stored_credential["public_key"],
        credential_current_sign_count=stored_credential["sign_count"],
        require_user_verification=True,
    )

    db.update_webauthn_sign_count(parsed_credential.raw_id, verification.new_sign_count)
    return True
