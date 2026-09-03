# HackerBank

Banco ficticio construido para **HackerTech UTN-FRC**. HackerBank demuestra
un login MFA real: contraseña (primer factor) + passkey FIDO2/WebAuthn
(segundo factor, cuando el usuario tiene una registrada) usando el
autenticador de plataforma del sistema operativo (Windows Hello, Touch ID,
etc.). No hay servidor que reciba datos biométricos: la biometría se usa
solo localmente en el dispositivo del usuario para desbloquear una clave
privada que firma un challenge del servidor.

> Este proyecto es exclusivamente educativo. No procesa dinero real, no está
> conectado a ningún sistema bancario real y las credenciales están
> hardcodeadas a propósito para el laboratorio.

## Instalación

### Requisitos
- Python 3.10 o superior
- Un navegador y sistema operativo con autenticador de plataforma
  configurado (Windows Hello, Touch ID) si querés probar el registro y la
  confirmación de una passkey — WebAuthn además requiere un contexto
  seguro (`localhost` o HTTPS)

### Pasos

```bash
# 1. Clonar o descomprimir el proyecto y ubicarse en la carpeta banco_app/
cd banco_app

# 2. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Cargar los datos de laboratorio (usuario Uriel Bagley)
python seed.py

# 5. Levantar el servidor
python app.py
```

La aplicación queda disponible en **http://localhost:5000**.

## Cómo correr el proyecto

1. `python app.py` levanta Flask en modo debug sobre el puerto 5000.
2. Abrí `http://localhost:5000` en el navegador.
3. Ingresá con las credenciales de laboratorio (primer factor: contraseña):
   - Email: `hackertech@gmail.com`
   - Contraseña: `1234`
4. Como el usuario demo todavía no tiene ninguna passkey registrada, la
   contraseña sola alcanza para entrar: caés directo en tu perfil/dashboard
   con todos los datos de la cuenta.
5. Desde ahí, en la tarjeta **"Reforzar seguridad"**, podés activar una
   passkey con el autenticador de tu dispositivo. La próxima vez que
   inicies sesión, el sistema te va a pedir confirmarla como segundo factor
   antes de dejarte entrar.

## Credenciales de laboratorio

| Campo | Valor |
|---|---|
| Email | hackertech@gmail.com |
| Contraseña | 1234 |

## Cómo funciona el segundo factor (FIDO2/WebAuthn)

- **Registro** (`/api/webauthn/register/*`, desde el dashboard, ya logueado):
  el navegador le pide al sistema operativo que genere un par de claves
  nuevo en el autenticador de plataforma; la clave pública queda guardada
  en `webauthn_credentials`, la privada nunca sale del dispositivo.
- **Login** (`/api/login`): si el usuario identificado ya tiene una passkey
  (`db.has_webauthn_credential`), el servidor solo marca el primer factor
  como superado y exige confirmarla en `/webauthn`. Si todavía no registró
  ninguna, entra directo (así puede llegar al dashboard a activar su
  primera passkey — sin este camino nadie podría hacerlo nunca).
- **Confirmación** (`/api/webauthn/authenticate/*`): el navegador pide al
  autenticador que firme un challenge aleatorio de un solo uso con la clave
  privada guardada; el servidor verifica esa firma contra la clave pública
  guardada. Ni la biometría ni la clave privada viajan nunca por la red.

Ver [`INSTRUCTOR_GUIDE.md`](INSTRUCTOR_GUIDE.md) para el detalle técnico
completo pensado para la charla/demo con los estudiantes.

## Historial: laboratorio de reconocimiento facial (retirado)

Versiones anteriores de este proyecto usaban una "verificación facial"
deliberadamente insegura (sin liveness detection, vulnerable a mostrarle
una foto a la cámara) como segundo factor, más una mecánica de evento
("desactivar una bomba") sobre el login exitoso. Ese código no se usa más
y fue reemplazado por FIDO2/WebAuthn real; se conserva sin borrar en
[`_legacy_face_auth/`](_legacy_face_auth/) por si hace falta volver atrás
antes de un evento — ver el README de esa carpeta.

## Estructura del proyecto

```
app.py                  Rutas Flask (paginas + APIs)
config.py               Constantes de configuracion
db.py                   Acceso a datos SQLite (consultas parametrizadas)
seed.py                 Carga el usuario de laboratorio
webauthn_auth.py        Logica del segundo factor FIDO2/WebAuthn
static/                 CSS, JS y assets
templates/               Vistas Jinja2
_legacy_face_auth/       Codigo retirado del lab de reconocimiento facial
INSTRUCTOR_GUIDE.md      Guia para el instructor del taller
```

## Stack técnico

- Backend: Python + Flask
- Base de datos: SQLite
- Segundo factor: FIDO2/WebAuthn (`webauthn` en PyPI, `navigator.credentials`
  del navegador)
- Frontend: HTML/CSS/JS vanilla, sin frameworks
