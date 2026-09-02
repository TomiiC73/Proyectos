"""
Configuracion centralizada de HackerBank.

Todas las constantes de la aplicacion viven aca (cero "numeros magicos"
dispersos por el codigo, segun mejores_practicas_programacion.md).
"""
import os

# --- Flask ---
# En produccion esto DEBE venir de una variable de entorno real.
# El valor de fallback es exclusivamente para el laboratorio educativo
# y queda documentado como inseguro-solo-lab en README.md.
FLASK_SECRET_KEY = os.environ.get("HACKERBANK_SECRET") or "lab-only-insecure-secret-hackertech-utn-frc"

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hackerbank.db")

# --- Endurecimiento de la cookie de sesion (CODING_STANDARDS: sesiones) ---
# HttpOnly evita que JavaScript lea la cookie (mitiga robo por XSS).
# SameSite=Lax mitiga CSRF en peticiones cross-site.
# Secure obliga HTTPS: se deja configurable porque el lab corre en http
# local; en produccion (HTTPS) poner HACKERBANK_COOKIE_SECURE=1.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = os.environ.get("HACKERBANK_COOKIE_SECURE", "0") == "1"

# --- Proteccion de fuerza bruta en el login (CODING_STANDARDS: Insecure Design) ---
# Tras LOGIN_MAX_ATTEMPTS fallos dentro de LOGIN_WINDOW_SECONDS para una misma
# cuenta, se responde 429 hasta que la ventana expire.
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300

# --- WebAuthn / FIDO2 (segundo factor, tras identificarse por contraseña) ---
# rp_id/origin NO se leen de config: app.py los deriva del request real en
# cada llamada (ver _webauthn_ids()), asi que funcionan automaticamente
# detras de cualquier dominio (incluido un tunel ngrok) sin tocar nada aca.
WEBAUTHN_RP_NAME = "HackerBank"

# --- Datos de presentacion de la cuenta (dashboard) ---
BANK_BRANCH_LABEL = "Sucursal Centro — Córdoba (031)"
ACCOUNT_TYPE_LABEL = "Caja de ahorro en pesos"
BANK_BIC = "HKBKARBA"            # codigo BIC/SWIFT ficticio

# --- Datos del usuario de laboratorio (Uriel Bagley) ---
# La contrasena en texto plano SOLO existe aca para que el instructor
# pueda re-generar el hash via seed.py; en la base de datos se guarda
# unicamente el hash (werkzeug.security).
DEMO_USER_EMAIL = "hackertech@gmail.com"
DEMO_USER_PASSWORD = "1234"
DEMO_USER_FIRST_NAME = "Uriel"
DEMO_USER_LAST_NAME = "Bagley"
DEMO_USER_DNI = "67.676.767"
DEMO_USER_CBU = "0000003100012345678901"
DEMO_USER_ALIAS = "uriel.bagley.67"
DEMO_BALANCE_ARS = 847320.50
DEMO_BALANCE_USD = 1240.00
DEMO_DAILY_YIELD_ARS = 1247.30

# --- Contenido publico de la landing (simula la home de un banco real) ---
PUBLIC_USD_BUY = 1180.50
PUBLIC_USD_SELL = 1220.50
PUBLIC_EUR_BUY = 1275.00
PUBLIC_EUR_SELL = 1325.00

PUBLIC_LOAN_MAX_ARS = 5000000.00
PUBLIC_LOAN_TNA_PERCENT = 45
PUBLIC_FIXED_DEPOSIT_TNA_PERCENT = 38
PUBLIC_FIXED_DEPOSIT_MIN_DAYS = 30
PUBLIC_CREDIT_CARD_TNA_PERCENT = 62

PUBLIC_SUPPORT_PHONE = "0800-555-4225"
PUBLIC_SUPPORT_HOURS = "Lunes a viernes de 8 a 20 hs · Sábados de 9 a 13 hs"

PUBLIC_BRANCHES = [
    {"name": "Sucursal Centro", "address": "Av. Colón 145, Córdoba"},
    {"name": "Sucursal Nueva Córdoba", "address": "Bv. Illia 355, Córdoba"},
    {"name": "Sucursal Güemes", "address": "Belgrano 620, Córdoba"},
]

# --- Sesion ---
SESSION_KEY_PRE_AUTH = "pre_auth_user_id"       # contraseña validada, FIDO2 pendiente (si tiene passkey)
SESSION_KEY_AUTHENTICATED = "authenticated"
SESSION_KEY_WEBAUTHN_CHALLENGE = "webauthn_challenge"
