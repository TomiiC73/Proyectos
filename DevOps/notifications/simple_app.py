"""
 Microservicio de Notificaciones con Email Real
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notifications Service")

def read_secret(secret_name: str) -> str:
    """Leer secretos desde archivos Docker o variables de entorno"""
    # Primero intentar leer desde archivo de secreto Docker
    secret_file = f"/run/secrets/{secret_name}"
    if os.path.exists(secret_file):
        with open(secret_file, 'r') as f:
            value = f.read().strip()
            logger.info(f"  Secreto '{secret_name}' leído desde Docker Secret")
            return value
    
    # Fallback a variable de entorno con _FILE suffix
    env_file = os.getenv(f"{secret_name.upper()}_FILE")
    if env_file and os.path.exists(env_file):
        with open(env_file, 'r') as f:
            value = f.read().strip()
            logger.info(f"  Secreto '{secret_name}' leído desde archivo: {env_file}")
            return value
    
    # Fallback a variable de entorno directa (para desarrollo)
    env_var = os.getenv(secret_name.upper())
    if env_var and env_var not in ["tu-email@gmail.com", "tu-app-password-aqui"]:
        logger.info(f"  Secreto '{secret_name}' leído desde variable de entorno")
        return env_var
    
    # Si no encuentra nada, retornar valor por defecto
    logger.error(f"     No se pudo encontrar el secreto: {secret_name}")
    return ""

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotificationRequest(BaseModel):
    type: str
    title: str
    message: str
    recipient: str
    isHtml: bool = False

def send_email_smtp(to_email: str, subject: str, body: str, is_html: bool = False):
    """Enviar email usando SMTP con Gmail - Usando secretos seguros"""
    
    # CONFIGURACIÓN DE EMAIL DESDE SECRETOS:
    MI_EMAIL = read_secret("smtp_username")  # Email desde secreto
    MI_PASSWORD = read_secret("smtp_password")  # App Password desde secreto
    
    if not MI_EMAIL or not MI_PASSWORD:
        logger.error("Credenciales SMTP no configuradas. Revisa los secretos.")
        raise Exception("Credenciales SMTP no disponibles")
    
    try:
        # Verificar si los secretos están configurados correctamente
        if not MI_EMAIL or MI_EMAIL == "tu-email@gmail.com" or not MI_PASSWORD or MI_PASSWORD == "tu-app-password-aqui":
            logger.warning("    Credenciales SMTP no configuradas, simulando envío")
            logger.info(f"  SIMULANDO ENVÍO DE EMAIL:")
            logger.info(f"   Destinatario: {to_email}")
            logger.info(f"   Asunto: {subject}")
            logger.info("   💡 Para envío real, configura los archivos de secretos")
            import time
            time.sleep(0.5)
            return True
        
        # Usar las credenciales de los secretos
        logger.info(f"  Enviando email real a: {to_email}")
        
        sender_email = MI_EMAIL
        sender_password = MI_PASSWORD
        smtp_server = "smtp.gmail.com"
        port = 587
        
        logger.info(f"  ENVIANDO EMAIL REAL:")
        logger.info(f"   Destinatario: {to_email}")
        logger.info(f"   Asunto: {subject}")
        logger.info(f"   Servidor: {smtp_server}:{port}")
        
        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email
        
        # Crear contenido HTML - usar HTML directo si is_html es True, sino usar template
        if is_html:
            html = body  # Usar el HTML que viene del frontend directamente
        else:
            # Template HTML profesional para texto plano (fallback)
            html = f"""
            <html>
              <head>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
              </head>
              <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);">
                <div style="background: linear-gradient(135deg, #00bcd4 0%, #26c6da 50%, #4dd0e1 100%); color: white; padding: 30px; text-align: center; border-radius: 15px 15px 0 0;">
                  <h1 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: -0.025em;">{subject}</h1>
                  <p style="margin: 10px 0 0 0; opacity: 0.9; font-weight: 400;">TODO App - Sistema de Notificaciones</p>
                </div>
                
                <div style="padding: 30px; background: white; border-radius: 0 0 15px 15px; box-shadow: 0 8px 25px rgba(0, 188, 212, 0.15);">
                  <div style="background: #e1f5fe; padding: 20px; border-radius: 12px; border-left: 5px solid #00bcd4;">
                    <pre style="white-space: pre-wrap; font-family: 'Inter', 'Courier New', monospace; line-height: 1.6; margin: 0; color: #263238; font-size: 14px;">{body}</pre>
                  </div>
                  
                  <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e1f5fe; text-align: center;">
                    <p style="color: #0277bd; margin: 0; font-weight: 500;">Enviado desde TODO App</p>
                    <p style="color: #0097a7; font-size: 12px; margin: 5px 0 0 0; font-weight: 400;">{datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}</p>
                  </div>
                </div>
                
                <div style="text-align: center; padding: 20px; color: #0097a7; font-size: 12px;">
                  <p style="margin: 0;">Este email fue generado automáticamente por el sistema de notificaciones.</p>
                </div>
              </body>
            </html>
            """
        
        # Crear parte HTML
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Enviar email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
            
        logger.info(f"  Email REAL enviado exitosamente a {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error enviando email real: {str(e)}")
        logger.error(f"   Verifica las credenciales y configuración SMTP")
        return False

@app.get("/health")
async def health_check():
    return {"status": "🟢 Healthy", "service": "Notifications Service", "timestamp": datetime.now().isoformat()}

@app.post("/send")
async def send_notification(notification: NotificationRequest):
    """Enviar notificación por email"""
    try:
        if notification.type == "email":
            # Enviar email real
            success = send_email_smtp(
                to_email=notification.recipient,
                subject=notification.title,
                body=notification.message,
                is_html=notification.isHtml
            )
            
            if success:
                return {
                    "success": True,
                    "message": "    Email enviado exitosamente",
                    "type": notification.type,
                    "recipient": notification.recipient,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                raise HTTPException(status_code=500, detail="   Error enviando email")
        else:
            # Para otros tipos, simular envío
            return {
                "success": True,
                "message": f"   Notificación {notification.type} simulada exitosamente",
                "type": notification.type,
                "recipient": notification.recipient,
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"   Error en send_notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)