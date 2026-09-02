"""
HackerBank - banco ficticio con autenticacion MFA real (HackerTech UTN-FRC).

Punto de entrada Flask. Define las rutas de las pantallas y la API de
autenticacion: usuario/contrasena (primer factor) + passkey FIDO2/WebAuthn
(segundo factor, cuando el usuario ya tiene una registrada). La logica de
WebAuthn vive en webauthn_auth.py.
"""
import base64
import random
import socket
import unicodedata
from functools import wraps

import webauthn
from webauthn.helpers.structs import AuthenticatorAttachment
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import config
import db
import rate_limit
import webauthn_auth

SERVER_PORT = 5000

app = Flask(__name__)
app.config.update(
    SECRET_KEY=config.FLASK_SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=config.SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE=config.SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE=config.SESSION_COOKIE_SECURE,
)

db.init_db()


def _format_currency(amount):
    """Formatea un numero con separador de miles '.' y decimales ',' (es-AR)."""
    is_negative = amount < 0
    formatted = f"{abs(amount):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"-{formatted}" if is_negative else formatted


app.jinja_env.filters["currency"] = _format_currency


# --------------------------------------------------------------------
# Guards de sesion
# --------------------------------------------------------------------
def require_pre_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get(config.SESSION_KEY_PRE_AUTH)
        if not user_id or db.get_user_by_id(user_id) is None:
            # Sesion vieja apuntando a un user_id que ya no existe (p.ej. se
            # reseteo la base) - se limpia en vez de romper con un 500.
            session.clear()
            return redirect(url_for("login_page"))
        return view(*args, **kwargs)
    return wrapped


def require_authenticated(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get(config.SESSION_KEY_AUTHENTICATED):
            return redirect(url_for("login_page"))
        user_id = session.get(config.SESSION_KEY_PRE_AUTH)
        if not user_id or db.get_user_by_id(user_id) is None:
            session.clear()
            return redirect(url_for("login_page"))
        return view(*args, **kwargs)
    return wrapped


def _current_user():
    user_id = session.get(config.SESSION_KEY_PRE_AUTH)
    return db.get_user_by_id(user_id) if user_id else None


def _account_view(user):
    """Datos derivados de la cuenta para el dashboard (solo presentacion)."""
    cbu = user["cbu"]
    account_number = f"{cbu[3:7]} / {cbu[8:]}" if len(cbu) >= 12 else cbu
    return {
        "account_number": account_number,
        "account_type": config.ACCOUNT_TYPE_LABEL,
        "branch": config.BANK_BRANCH_LABEL,
        "bic": config.BANK_BIC,
        "status": "Activa",
    }


def _generate_account_identifiers(first_name, last_name):
    """CBU/alias de presentacion para una cuenta nueva (el registro no le
    pide DNI/CBU real al usuario, asi que se generan como en un banco que
    los asigna solo al abrir la cuenta)."""
    cbu = "".join(str(random.randint(0, 9)) for _ in range(22))
    normalized = unicodedata.normalize("NFKD", f"{first_name}.{last_name}".lower())
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    alias_base = "".join(ch for ch in ascii_only if ch.isalnum() or ch == ".")
    alias = f"{alias_base or 'cuenta'}.hb"
    return cbu, alias


def _login_user(user_id):
    """Marca la sesion como autenticada para un usuario."""
    session.clear()
    session[config.SESSION_KEY_PRE_AUTH] = user_id
    session[config.SESSION_KEY_AUTHENTICATED] = True


def _webauthn_ids():
    """Deriva (rp_id, origin) del request real: funciona automaticamente
    detras de cualquier dominio (incluido un tunel ngrok o un proxy como
    Vercel) sin config fija. X-Forwarded-Host tiene prioridad sobre Host
    porque un proxy externo (ej. Vercel reescribiendo hacia la VM de Azure)
    reemplaza el Host real por el del destino; sin este header, rp_id/origin
    quedarian mal derivados y WebAuthn rechazaria toda credencial."""
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.headers.get("X-Forwarded-Host", request.host)
    hostname = host.split(":")[0]
    origin = f"{proto}://{host}"
    return hostname, origin


def _options_json(options):
    return webauthn.options_to_json(options), 200, {"Content-Type": "application/json"}


# --------------------------------------------------------------------
# Paginas
# --------------------------------------------------------------------
@app.route("/")
def landing():
    return render_template(
        "landing.html",
        usd_buy=config.PUBLIC_USD_BUY,
        usd_sell=config.PUBLIC_USD_SELL,
        eur_buy=config.PUBLIC_EUR_BUY,
        eur_sell=config.PUBLIC_EUR_SELL,
        loan_max_ars=config.PUBLIC_LOAN_MAX_ARS,
        loan_tna=config.PUBLIC_LOAN_TNA_PERCENT,
        fixed_deposit_tna=config.PUBLIC_FIXED_DEPOSIT_TNA_PERCENT,
        fixed_deposit_min_days=config.PUBLIC_FIXED_DEPOSIT_MIN_DAYS,
        credit_card_tna=config.PUBLIC_CREDIT_CARD_TNA_PERCENT,
        support_phone=config.PUBLIC_SUPPORT_PHONE,
        support_hours=config.PUBLIC_SUPPORT_HOURS,
        branches=config.PUBLIC_BRANCHES,
    )


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/webauthn")
@require_pre_auth
def webauthn_confirm_page():
    return render_template("webauthn_confirm.html")


@app.route("/dashboard")
@require_authenticated
def dashboard():
    user = _current_user()
    cards = db.get_cards_for_user(user["id"])
    movements = db.get_movements_for_user(user["id"])
    return render_template(
        "dashboard.html",
        user=user,
        cards=cards,
        movements=movements,
        account=_account_view(user),
        has_passkey=db.has_webauthn_credential(user["id"]),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


# --------------------------------------------------------------------
# API: login - contrasena (1er factor) + passkey FIDO2/WebAuthn (2do
# factor, solo si el usuario ya tiene una registrada).
# --------------------------------------------------------------------
@app.route("/api/login", methods=["POST"])
def api_login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password", "")

    # Proteccion de fuerza bruta: se limita por cuenta atacada (email).
    rate_key = f"login:{email}"
    if rate_limit.is_blocked(rate_key, config.LOGIN_MAX_ATTEMPTS, config.LOGIN_WINDOW_SECONDS):
        return jsonify(ok=False, error="Demasiados intentos. Esperá unos minutos."), 429

    user = db.get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        rate_limit.record_failure(rate_key, config.LOGIN_WINDOW_SECONDS)
        return jsonify(ok=False, error="Email o contraseña incorrectos."), 401

    rate_limit.reset(rate_key)

    if db.has_webauthn_credential(user["id"]):
        # Primer factor (contrasena) superado; falta confirmar la passkey.
        # session.clear() regenera el contenido de sesion (mitiga fijacion de sesion).
        session.clear()
        session[config.SESSION_KEY_PRE_AUTH] = user["id"]
        return jsonify(ok=True, next=url_for("webauthn_confirm_page"))

    # Primer ingreso / todavia sin passkey registrada: la contrasena sola
    # alcanza para entrar. Sin este camino nadie podria llegar nunca al
    # dashboard para registrar su primera passkey.
    _login_user(user["id"])
    return jsonify(ok=True, next=url_for("dashboard"))


# --------------------------------------------------------------------
# API: creacion de cuenta (nombre, apellido, email, contrasena). El
# usuario nuevo entra directo al dashboard (todavia sin passkey), igual
# que el camino de "primer ingreso" de /api/login.
# --------------------------------------------------------------------
@app.route("/api/signup", methods=["POST"])
def api_signup():
    payload = request.get_json(silent=True) or {}
    first_name = (payload.get("first_name") or "").strip()
    last_name = (payload.get("last_name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password", "")

    if not first_name or not last_name or not email or not password:
        return jsonify(ok=False, error="Completá todos los campos."), 400
    if len(password) < 6:
        return jsonify(ok=False, error="La contraseña debe tener al menos 6 caracteres."), 400
    if db.email_exists(email):
        return jsonify(ok=False, error="Ya existe una cuenta con ese email."), 409

    cbu, alias = _generate_account_identifiers(first_name, last_name)
    user_id = db.insert_user(
        email=email,
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        dni="No verificado",
        cbu=cbu,
        alias=alias,
        balance_ars=0.0,
        balance_usd=0.0,
        daily_yield_ars=0.0,
    )
    _login_user(user_id)
    return jsonify(ok=True, next=url_for("dashboard"))


# --------------------------------------------------------------------
# API: registro de una passkey (requiere estar ya autenticado). Se hace
# desde el dashboard, en la tarjeta "Reforzar seguridad".
# --------------------------------------------------------------------
_METHOD_TO_ATTACHMENT = {
    "llave": AuthenticatorAttachment.CROSS_PLATFORM,
    "huella": AuthenticatorAttachment.PLATFORM,
    "pin": AuthenticatorAttachment.PLATFORM,
    "rostro": AuthenticatorAttachment.PLATFORM,
}


@app.route("/api/webauthn/register/begin", methods=["POST"])
@require_authenticated
def api_webauthn_register_begin():
    user = _current_user()
    rp_id, _origin = _webauthn_ids()
    payload = request.get_json(silent=True) or {}
    attachment = _METHOD_TO_ATTACHMENT.get(payload.get("method"))
    options = webauthn_auth.build_registration_options(user, rp_id, authenticator_attachment=attachment)
    session[config.SESSION_KEY_WEBAUTHN_CHALLENGE] = base64.b64encode(options.challenge).decode("ascii")
    return _options_json(options)


@app.route("/api/webauthn/register/complete", methods=["POST"])
@require_authenticated
def api_webauthn_register_complete():
    user = _current_user()
    rp_id, origin = _webauthn_ids()
    challenge_b64 = session.pop(config.SESSION_KEY_WEBAUTHN_CHALLENGE, None)
    credential_json = request.get_data(as_text=True)

    if not challenge_b64:
        return jsonify(ok=False, error="No hay un registro de passkey pendiente."), 400

    try:
        expected_challenge = base64.b64decode(challenge_b64)
        webauthn_auth.complete_registration(user, credential_json, expected_challenge, rp_id, origin)
    except Exception as error:
        # No se filtra el detalle interno al cliente: se loguea server-side
        # para debugging y se responde un mensaje generico.
        app.logger.warning("Registro de passkey fallido (user_id=%s): %s", user["id"], error)
        return jsonify(ok=False, error="No se pudo registrar la passkey."), 400

    return jsonify(ok=True)


# --------------------------------------------------------------------
# API: segundo factor - confirmacion FIDO2 del usuario ya identificado
# por contrasena.
# --------------------------------------------------------------------
@app.route("/api/webauthn/authenticate/begin", methods=["POST"])
@require_pre_auth
def api_webauthn_authenticate_begin():
    user = _current_user()
    rp_id, _origin = _webauthn_ids()
    options = webauthn_auth.build_authentication_options(user, rp_id)
    session[config.SESSION_KEY_WEBAUTHN_CHALLENGE] = base64.b64encode(options.challenge).decode("ascii")
    return _options_json(options)


@app.route("/api/webauthn/authenticate/complete", methods=["POST"])
@require_pre_auth
def api_webauthn_authenticate_complete():
    user = _current_user()
    rp_id, origin = _webauthn_ids()
    challenge_b64 = session.pop(config.SESSION_KEY_WEBAUTHN_CHALLENGE, None)
    credential_json = request.get_data(as_text=True)

    if not challenge_b64:
        return jsonify(ok=False, error="No hay una confirmación pendiente."), 400

    try:
        expected_challenge = base64.b64decode(challenge_b64)
        webauthn_auth.complete_authentication(user, credential_json, expected_challenge, rp_id, origin)
    except Exception as error:
        app.logger.warning("Confirmación FIDO2 fallida (user_id=%s): %s", user["id"], error)
        return jsonify(ok=False, error="No se pudo verificar tu passkey."), 400

    # Segundo factor superado: recien aca queda autenticado.
    _login_user(user["id"])
    return jsonify(ok=True, next=url_for("dashboard"))


def _get_lan_ip():
    """Detecta la IP de LAN de esta maquina (sin enviar trafico real)."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        return probe.getsockname()[0]
    except OSError:
        return None
    finally:
        probe.close()


if __name__ == "__main__":
    lan_ip = _get_lan_ip()
    print(f"HackerBank disponible en: http://localhost:{SERVER_PORT}")
    if lan_ip:
        print(f"(o en tu misma wifi: http://{lan_ip}:{SERVER_PORT})")
    app.run(debug=True, host="0.0.0.0", port=SERVER_PORT)
