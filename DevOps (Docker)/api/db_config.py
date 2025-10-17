import mysql.connector
import os

def read_secret(secret_path):
    """Lee un secreto desde un archivo"""
    try:
        with open(secret_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_db_connection():
    try:
        # Leer contraseña desde archivo de secreto si existe
        password_file = os.getenv('DB_PASSWORD_FILE')
        if password_file:
            password = read_secret(password_file)
        else:
            password = os.getenv('DB_PASSWORD', '')
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=password,
            database=os.getenv('DB_NAME', 'todos_db'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )

        if connection.is_connected():
            print("Conexión exitosa a la BD")
            return connection

    except mysql.connector.Error as error:
        print(f"Error de conexión a la base de datos: {error}")
        return None