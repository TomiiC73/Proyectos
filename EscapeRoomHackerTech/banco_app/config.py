"""
Configuracion centralizada de HackerBank.

"""
import os

from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET_KEY = os.environ.get("HACKERBANK_SECRET") or "lab-only-insecure-secret-hackertech-utn-frc"

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hackerbank.db")

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = os.environ.get("HACKERBANK_COOKIE_SECURE", "0") == "1"

LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300

# --- Rutas de assets usados por la logica de reconocimiento facial ---
STATIC_IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img")
FACE_REFERENCE_PATH = os.path.join(STATIC_IMG_DIR, "sr_vargas_reference.jpg")


FACE_ORB_MIN_MATCHES = 150

FACE_COMPARE_SIZE = (200, 200)

# --- Datos de presentacion de la cuenta (dashboard) ---
BANK_BRANCH_LABEL = "Sucursal Centro — Córdoba (031)"
ACCOUNT_TYPE_LABEL = "Caja de ahorro en pesos"
BANK_BIC = "HKBKARBA"            # codigo BIC/SWIFT ficticio

DEMO_USER_EMAIL = os.environ.get("DEMO_USER_EMAIL") or "dev+ht"
DEMO_USER_PASSWORD = os.environ.get("DEMO_USER_PASSWORD") or "2NEfv7M3+hlE"
DEMO_USER_NAME = "Sr. Vargas"
DEMO_USER_DNI = "30.456.789"
DEMO_USER_CBU = "0000003100012345678901"
DEMO_USER_ALIAS = "sr.vargas.hb"
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
SESSION_KEY_PRE_AUTH = "pre_auth_user_id"
SESSION_KEY_AUTHENTICATED = "authenticated"


BOMB_DESACTIVATE_URL = os.environ.get("BOMB_DESACTIVATE_URL")
