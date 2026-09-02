"""
Capa de acceso a datos (patron DAO) de HackerBank.

Toda consulta usa parametros posicionales (placeholders "?") de sqlite3.
Esta prohibido concatenar strings para armar SQL en este proyecto,
segun mejores_practicas_programacion.md (prevencion de inyeccion SQL).

Tablas: users, cards, movements, webauthn_credentials (segundo factor
FIDO2/WebAuthn, ver webauthn_auth.py).
"""
import sqlite3
from contextlib import contextmanager

from config import DATABASE_PATH


@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def reset_db():
    """Borra el esquema entero (si existe) para que init_db() lo recree
    desde cero. Usado por seed.py para arrancar cada contenedor con datos
    limpios en vez de reusar lo que haya quedado de una corrida anterior."""
    with get_connection() as conn:
        conn.executescript(
            """
            DROP TABLE IF EXISTS webauthn_credentials;
            DROP TABLE IF EXISTS movements;
            DROP TABLE IF EXISTS cards;
            DROP TABLE IF EXISTS users;
            """
        )


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dni TEXT NOT NULL,
                cbu TEXT NOT NULL,
                alias TEXT NOT NULL,
                balance_ars REAL NOT NULL,
                balance_usd REAL NOT NULL,
                daily_yield_ars REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                card_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                last_four TEXT NOT NULL,
                expiry TEXT
            );

            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                movement_date TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS webauthn_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                credential_id BLOB UNIQUE NOT NULL,
                public_key BLOB NOT NULL,
                sign_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT
            );
            """
        )


def get_user_by_email(email):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None


def email_exists(email):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE email = ?", (email,)
        ).fetchone()
        return row is not None


def get_cards_for_user(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM cards WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def get_movements_for_user(user_id, limit=6):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM movements
            WHERE user_id = ?
            ORDER BY movement_date DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(row) for row in rows]


def insert_user(email, password_hash, first_name, last_name, dni, cbu, alias,
                 balance_ars, balance_usd, daily_yield_ars):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO users
                (email, password_hash, first_name, last_name, dni, cbu, alias,
                 balance_ars, balance_usd, daily_yield_ars)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (email, password_hash, first_name, last_name, dni, cbu, alias,
             balance_ars, balance_usd, daily_yield_ars),
        )
        return cursor.lastrowid


def insert_card(user_id, card_type, brand, last_four, expiry):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO cards (user_id, card_type, brand, last_four, expiry)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, card_type, brand, last_four, expiry),
        )


def insert_movement(user_id, description, category, amount, movement_date):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO movements (user_id, description, category, amount, movement_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, description, category, amount, movement_date),
        )


def save_webauthn_credential(user_id, credential_id, public_key, sign_count):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO webauthn_credentials
                (user_id, credential_id, public_key, sign_count, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
            """,
            (user_id, credential_id, public_key, sign_count),
        )


def get_webauthn_credentials_for_user(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM webauthn_credentials WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def has_webauthn_credential(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM webauthn_credentials WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row is not None


def get_webauthn_credential_by_id(credential_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM webauthn_credentials WHERE credential_id = ?", (credential_id,)
        ).fetchone()
        return dict(row) if row else None


def update_webauthn_sign_count(credential_id, sign_count):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE webauthn_credentials
            SET sign_count = ?
            WHERE credential_id = ?
            """,
            (sign_count, credential_id),
        )
