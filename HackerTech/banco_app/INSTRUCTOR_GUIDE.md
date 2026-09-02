# Guía del instructor — HackerBank (HackerTech UTN-FRC)

Este documento es para el equipo docente/organizador: explica cómo demostrar
y explicar el segundo factor real (FIDO2/WebAuthn) que implementa HackerBank.

## 1. Objetivo pedagógico

Versiones anteriores de este lab hacían que el estudiante **vulnerara** un
segundo factor biométrico débil (reconocimiento facial sin liveness
detection, mostrando una foto a la cámara). Ese código sigue disponible en
[`_legacy_face_auth/`](_legacy_face_auth/) pero ya no está en uso.

Ahora HackerBank implementa el segundo factor **de la forma correcta**, con
FIDO2/WebAuthn real. El objetivo pedagógico pasa de "romper una MFA débil" a:

1. Entender cómo funciona un segundo factor moderno y por qué es resistente
   a los ataques que sí funcionaban contra el reconocimiento facial (foto,
   replay, phishing del secreto).
2. Ver en código real (`webauthn_auth.py`, `static/js/webauthn-common.js`)
   el flujo completo: generación de opciones, ceremonia en el navegador
   (`navigator.credentials.create/get`), verificación de la firma en el
   servidor.
3. Poder comparar, con este mismo proyecto, el "antes" (`_legacy_face_auth/`)
   contra el "después" (`webauthn_auth.py`) del mismo problema.

## 2. Demo paso a paso

1. Levantar la aplicación (`python app.py`) y cargar los datos de laboratorio
   (`python seed.py`).
2. Abrir `http://localhost:5000/login` e ingresar con `hackertech@gmail.com` /
   `1234` (primer factor). El usuario demo arranca **sin** ninguna
   passkey registrada, así que la contraseña sola alcanza para entrar: cae
   directo en el dashboard/perfil con todos los datos de la cuenta.
3. En el dashboard, mostrar la tarjeta **"Reforzar seguridad"** y registrar
   una passkey (cualquiera de los tres botones dispara el mismo
   `navigator.credentials.create()` — es el sistema operativo el que decide
   qué pedir según lo que el dispositivo tenga configurado).
4. Cerrar sesión (`/logout`) y volver a iniciar sesión con el mismo usuario:
   esta vez, tras la contraseña, `/api/login` detecta que ya tiene una
   passkey (`db.has_webauthn_credential`) y redirige a `/webauthn`, donde
   hay que confirmarla antes de entrar.
5. Punto clave para remarcar: en ningún momento de este flujo el servidor
   recibió una imagen, una huella ni ningún dato biométrico — solo una
   firma criptográfica de un challenge de un solo uso.

## 3. Cómo funciona técnicamente

`webauthn_auth.py` es el módulo central:

- `build_registration_options` / `complete_registration` — el registro de
  una passkey nueva, gateado por `require_authenticated` (hace falta estar
  ya logueado para asociarle una passkey a tu cuenta).
- `build_authentication_options` / `complete_authentication` — la
  confirmación del segundo factor, gateada por `require_pre_auth` (la
  contraseña ya se validó, falta el FIDO2). `allow_credentials` se acota a
  las credenciales de ESE usuario: el navegador solo ofrece esas, no
  cualquiera guardada en el dispositivo — sigue siendo un segundo factor
  real, no un login "usernameless".
- El challenge vive únicamente en la cookie de sesión firmada de Flask
  (`config.SESSION_KEY_WEBAUTHN_CHALLENGE`) entre el `begin` y el
  `complete` de cada ceremonia: es efímero y de un solo uso, nunca se
  persiste en la base de datos.
- `_webauthn_ids()` en `app.py` deriva `(rp_id, origin)` del request real en
  cada llamada, así el esquema sigue funcionando sin tocar config si el
  proyecto se expone detrás de un túnel (ngrok) con un dominio distinto.

### 3.1 Por qué esto es resistente a lo que rompía al reconocimiento facial

| Ataque que funcionaba contra `_legacy_face_auth/` | Por qué no funciona contra WebAuthn |
|---|---|
| Mostrar una foto/video a la cámara | No hay cámara ni imagen involucrada: la biometría solo desbloquea la clave privada localmente, nunca viaja |
| Robar las muestras guardadas en la base | La base solo tiene la clave **pública**; sin la privada (que nunca sale del dispositivo) no se puede firmar nada |
| Replay de un frame capturado | Cada ceremonia firma un challenge aleatorio de un solo uso; una firma vieja no sirve para un challenge nuevo |
| Phishing (sitio falso que captura contraseña + biometría) | La firma está atada al `origin` (dominio) real en el momento de firmar; un dominio distinto invalida la respuesta |

### 3.2 Qué es liveness detection y por qué WebAuthn no la necesita

La detección de vida (*liveness detection*) es el conjunto de técnicas que
verifican que una biometría capturada proviene de una persona viva presente
físicamente (parpadeo, movimiento, profundidad 3D, reflectancia IR). Es
necesaria cuando el servidor recibe y compara datos biométricos crudos —
que es exactamente lo que WebAuthn evita por diseño: el servidor nunca ve
biometría, solo verifica una firma criptográfica. Por eso FIDO2/WebAuthn no
"compite" con liveness detection, cambia el problema de raíz.

## 4. Preguntas sugeridas para el debate

1. ¿Por qué alcanza con que la clave privada nunca salga del dispositivo
   para volver irrelevante el robo de la base de datos del servidor?
2. ¿Qué rol cumple el `origin` en la verificación, y qué ataque específico
   previene atar la firma a él?
3. `webauthn_auth.py` pide `resident_key=PREFERRED` (credencial discoverable
   cuando el autenticador lo soporte, para que aparezca en apps como Yubico
   Authenticator), pero el login de HackerBank funciona igual sin que sea
   discoverable — `allow_credentials` ya le dice al navegador cuál usar.
   ¿En qué escenario ("usernameless", tocar la llave sin escribir el email
   primero) *sí* sería indispensable que la credencial sea discoverable?
4. Comparando con `_legacy_face_auth/face_auth.py`: ¿qué información
   biométrica llegaba a viajar por la red ahí que en WebAuthn nunca sale
   del dispositivo?
5. Si alguien roba el teléfono/laptop del usuario ya desbloqueado, ¿qué
   protege igual (o no) a la cuenta de HackerBank?

## 5. Notas de setup para el día del evento

### Requisitos

- Un dispositivo por estación con autenticador de plataforma configurado
  (Windows Hello, Touch ID, huella de Android/Chrome OS) para poder
  demostrar el registro y la confirmación en vivo.
- WebAuthn requiere un contexto seguro: `localhost` funciona sin HTTPS; si
  se expone la app públicamente (ngrok u otro túnel), tiene que ser HTTPS.

### Cómo preparar el entorno antes del HackerTech

1. Clonar el proyecto en cada estación (o distribuir un zip).
2. Verificar Python 3.10+ instalado.
3. Ejecutar `pip install -r requirements.txt` con anticipación.
4. Ejecutar `python seed.py` una vez por estación para cargar los datos.
5. Probar el flujo completo (login sin passkey → registrar → logout →
   login con confirmación FIDO2) en al menos una estación antes de que
   lleguen los estudiantes.

### Problemas comunes y cómo resolverlos en el momento

| Problema | Causa probable | Solución rápida |
|---|---|---|
| El botón de registrar/confirmar passkey no hace nada | El navegador no soporta `PublicKeyCredential`, o no es un contexto seguro | Usar un navegador moderno sobre `localhost` o HTTPS |
| "Este dispositivo no soporta ningún método de seguridad biométrica" | No hay autenticador de plataforma configurado en el sistema operativo | Configurar Windows Hello/Touch ID/huella en el dispositivo, o probar en otro |
| Confirmar la passkey falla con "No se pudo verificar" | Se está probando desde un dominio/origin distinto al que se usó para registrar | Registrar y confirmar siempre bajo el mismo `http://localhost:5000` (o el mismo túnel) |

### Tiempo estimado por estudiante

- Instalación y arranque (si no está preparado de antemano): 10-15 min.
- Explorar el flujo (login sin passkey, registrar, logout, login con
  confirmación FIDO2): 10-15 min.
- Lectura guiada de `webauthn_auth.py` y debate: 15-20 min.

**Total sugerido por estudiante: 35-50 minutos.**
