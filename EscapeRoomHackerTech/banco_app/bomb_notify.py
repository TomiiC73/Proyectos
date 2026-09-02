"""
Notificacion externa "bomba desactivada" (puesta en escena del evento).

Al completarse el login (contrasena + facial, el segundo factor inseguro a
proposito), se dispara un POST fire-and-forget a una URL fija del evento
(ver config.BOMB_DESACTIVATE_URL, con el token ya incluido en la URL).

Nunca debe bloquear ni romper el login del estudiante: corre en un hilo de
fondo con un timeout corto, y cualquier error (sin conexion a internet, URL
todavia sin configurar, timeout) se traga tras loguearlo por consola - el
dashboard tiene que mostrarse igual.
"""
import threading
import urllib.error
import urllib.request

import config

_REQUEST_TIMEOUT_SECONDS = 5


def _post_desactivate():
    try:
        request = urllib.request.Request(
            config.BOMB_DESACTIVATE_URL,
            method="POST",
            headers={
                "User-Agent": "curl/8.0.0",
                "Accept": "/",
            },
        )

        print(f"URL: {request.full_url}")
        print(f"Method: {request.method}")
        print(f"Headers: {dict(request.headers)}")

        with urllib.request.urlopen(request, timeout=_REQUEST_TIMEOUT_SECONDS) as response:
            print(response.status)
            print(response.read().decode())

    except (urllib.error.URLError, OSError, ValueError) as error:
        print(f"[bomb] No se pudo notificar la desactivacion (no bloquea el login): {error}")


def notify_desactivated():
    """Dispara el POST en un hilo aparte; no bloquea el request actual."""
    threading.Thread(target=_post_desactivate, daemon=True).start()
