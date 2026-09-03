from flask import Flask
from flask_cors import CORS  # Habilita CORS para permitir solicitudes desde diferentes dominios
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)  # Inicializamos la aplicación Flask
CORS(app)  # Habilitamos CORS para permitir peticiones desde clientes externos

# Configurar Flask con variables de entorno y secrets
# Prioridad: 1) Docker secret file, 2) Variable de entorno directa, 3) Default dev
secret_key_file = os.getenv('SECRET_KEY_FILE')
if secret_key_file and os.path.exists(secret_key_file):
    try:
        with open(secret_key_file, 'r') as f:
            app.config['SECRET_KEY'] = f.read().strip()
    except (PermissionError, IOError) as e:
        print(f"Warning: No se pudo leer {secret_key_file}: {e}")
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
else:
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# cometario para probar si anda rulesssss