# Legacy: laboratorio de reconocimiento facial + tema "bomba"

Este código fue el segundo factor original de HackerBank y ya **no está en uso**.
Se conserva acá completo (no se borró) por si el profesor pide volver atrás
antes del evento. Nada de esto se importa desde `banco_app/` actualmente.

## Qué era

- **`face_auth.py`** — segundo factor "biométrico" deliberadamente inseguro:
  Haar cascade (OpenCV) para detectar el rostro en un frame de cámara +
  comparación de features ORB contra muestras guardadas del usuario, sin
  ninguna detección de vida (liveness). El desafío pedagógico consistía en
  mostrarle a la cámara una foto del usuario para superar ese segundo factor.
- **`bomb_notify.py`** — POST fire-and-forget a una URL externa (ngrok) que
  disparaba la puesta en escena de "bomba desactivada" del evento en vivo,
  apenas el segundo factor facial daba éxito.
- **`static/img/sr_vargas_reference.jpg`** — foto de referencia (placeholder)
  que `seed.py` enrolaba como el rostro del usuario demo.
- **`static/img/bomb_desactivated.svg`** — ilustración mostrada en la pantalla
  de verificación al superar el segundo factor.
- **`static/js/face.js`** — captura continua de frames de la webcam
  (`getUserMedia`) y polling contra `POST /api/face/verify`.
- **`templates/face_auth.html`** — pantalla de verificación facial con el
  círculo de cámara y el resultado "¡Bomba desactivada!".

## Por qué se sacó

Reemplazado por un segundo factor FIDO2/WebAuthn real (huella/PIN/rostro vía
el autenticador de plataforma del sistema operativo, migrado desde
`../../utn_frc_redesign/`), y se eliminó por completo la mecánica de evento
"desactivar bomba" (el POST externo, la imagen y el mensaje animado). El
login exitoso ahora lleva directo al dashboard/perfil del usuario. Ver
`../CLAUDE.md`, `../README.md` e `../INSTRUCTOR_GUIDE.md` para el flujo
actual.

## Dependencias que este código necesitaba

`opencv-python`, `numpy`, `Pillow` — ya no están en `../requirements.txt`.
Si se restaura este módulo, hay que volver a agregarlas ahí y reinstalar las
libs de sistema de OpenCV en el `Dockerfile` (`libgl1`, `libglib2.0-0`,
`libsm6`, `libxext6`, `libxrender1`).

## Cómo restaurarlo (si hiciera falta)

1. Mover `face_auth.py`, `bomb_notify.py`, `static/img/sr_vargas_reference.jpg`,
   `static/img/bomb_desactivated.svg`, `static/js/face.js` y
   `templates/face_auth.html` de vuelta a sus carpetas originales en
   `banco_app/`.
2. Re-agregar `opencv-python`, `numpy`, `Pillow` a `requirements.txt` y las
   libs de sistema al `Dockerfile`.
3. Restaurar en `db.py` la tabla `faces` y las funciones `insert_face`,
   `count_faces_for_user`, `get_faces_for_user`.
4. Restaurar en `config.py` las constantes `FACE_REFERENCE_PATH`,
   `FACE_ORB_MIN_MATCHES`, `FACE_COMPARE_SIZE`, `BOMB_DESACTIVATE_URL`,
   `BOMB_DESACTIVATE_TOKEN`.
5. Restaurar en `app.py` las rutas `/face` y `/api/face/verify`, y el import
   de `face_auth`/`bomb_notify`.
6. Restaurar en `seed.py` la llamada a `_ensure_demo_face`.
