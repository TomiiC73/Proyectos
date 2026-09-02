"""
Script de siembra de datos para el laboratorio HackerBank.

Borra el esquema entero y lo recrea desde cero en CADA corrida (ver
db.reset_db()), y siembra al usuario ficticio Uriel Bagley con sus
tarjetas y movimientos - asi cada arranque del contenedor empieza con
datos limpios, sin arrastrar passkeys o cuentas creadas por signup en
una corrida anterior. No registra ninguna passkey: el usuario entra
con contrasena y puede activar una desde el dashboard ("Reforzar
seguridad") cuando quiera.

Uso:
    python seed.py
"""
from werkzeug.security import generate_password_hash

import config
import db

MOVEMENTS = [
    ("Supermercado La Anonima", "Consumo", -18450.00, "2026-07-10"),
    ("Transferencia recibida - Maria Lopez", "Transferencia", 45000.00, "2026-07-09"),
    ("Netflix", "Suscripcion", -4999.00, "2026-07-08"),
    ("Pago de sueldo", "Ingreso", 620000.00, "2026-07-01"),
    ("YPF Combustible", "Consumo", -22300.50, "2026-06-29"),
    ("Farmacity", "Consumo", -7650.00, "2026-06-27"),
]


def _create_demo_user():
    password_hash = generate_password_hash(config.DEMO_USER_PASSWORD)
    user_id = db.insert_user(
        email=config.DEMO_USER_EMAIL.strip().lower(),
        password_hash=password_hash,
        first_name=config.DEMO_USER_FIRST_NAME,
        last_name=config.DEMO_USER_LAST_NAME,
        dni=config.DEMO_USER_DNI,
        cbu=config.DEMO_USER_CBU,
        alias=config.DEMO_USER_ALIAS,
        balance_ars=config.DEMO_BALANCE_ARS,
        balance_usd=config.DEMO_BALANCE_USD,
        daily_yield_ars=config.DEMO_DAILY_YIELD_ARS,
    )
    db.insert_card(user_id, "credito", "Visa", "4821", "09/28")
    db.insert_card(user_id, "debito", "Mastercard", "3307", None)
    for description, category, amount, movement_date in MOVEMENTS:
        db.insert_movement(user_id, description, category, amount, movement_date)
    print(f"Usuario {config.DEMO_USER_FIRST_NAME} {config.DEMO_USER_LAST_NAME} creado con id={user_id}.")
    print(f"Email: {config.DEMO_USER_EMAIL}  Password: {config.DEMO_USER_PASSWORD}")
    return user_id


def seed():
    db.reset_db()
    db.init_db()
    _create_demo_user()


if __name__ == "__main__":
    seed()
