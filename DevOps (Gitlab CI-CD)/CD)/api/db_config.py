import mysql.connector
import os
import time

def read_secret(secret_path):
    """Lee un secreto desde un archivo"""
    try:
        with open(secret_path, 'r') as f:
            return f.read().strip()
    except (FileNotFoundError, PermissionError, IOError):
        return None

def get_db_connection():
    """Obtiene conexión a la BD con retry automático"""
    
    # Leer contraseña (prioridad: archivo secret -> variable entorno)
    password_file = os.getenv('DB_PASSWORD_FILE')
    password = read_secret(password_file) if password_file else None
    if not password:
        password = os.getenv('DB_PASSWORD', '')
    
    # Configuración de conexión
    db_host = os.getenv('DB_HOST', 'db')
    db_user = os.getenv('DB_USER', 'todos_user')
    db_name = os.getenv('DB_NAME', 'todos_db')
    
    # Retry hasta 5 intentos
    for attempt in range(1, 6):
        try:
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=password,
                database=db_name,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                connect_timeout=10
            )
            
            if connection.is_connected():
                print(f"✓ Conectado a MySQL en {db_host}")
                return connection
                
        except mysql.connector.Error as error:
            print(f"❌ Intento {attempt}/5 falló: {error}")
            if attempt < 5:
                time.sleep(2)
    
    print("❌ No se pudo conectar a la BD después de 5 intentos")
    return None