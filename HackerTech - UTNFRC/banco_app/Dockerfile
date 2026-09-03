# HackerBank - imagen independiente (Flask + SQLite + WebAuthn). No comparte
# contexto de build con utn_frc_redesign/.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# seed.py borra y recrea la base entera en cada arranque (ver db.reset_db()):
# el contenedor siempre empieza con datos limpios, sin passkeys ni cuentas
# de una corrida anterior.
CMD ["sh", "-c", "python seed.py && python app.py"]
