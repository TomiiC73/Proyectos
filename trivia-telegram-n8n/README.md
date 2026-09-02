# Trivia por Telegram — demo con n8n Cloud

Bot de trivia (5 preguntas, opción múltiple, temática tech/n8n) para una demo en vivo de
automatización. Corre sobre **n8n Cloud** (no hace falta Docker ni túnel) con **dos bots de
Telegram separados**:

- **Bot jugadores** — con el que los participantes hablan (`/unirme`, responder A/B/C/D).
- **Bot admin** — el tuyo, para controlar la partida (`/iniciar`, `/comenzar`, `/detener`,
  `/reiniciar`, `/resetear`) sin que un jugador pueda arrancar o resetear el juego por accidente.
  Una vez que arranca la partida, este mismo bot te va avisando en vivo quién respondió qué y si
  acertó (ej. "✅ Martín respondió la pregunta 1 con: A -> avanza a la pregunta 2") — no hace
  falta ninguna pantalla ni canal externo, todo llega a tu chat con el bot admin. Cuando **todos**
  los jugadores anotados terminan las 5 preguntas, se manda automáticamente una **tabla de
  clasificación final** (ordenada por puntaje) tanto a vos como a cada jugador.

### Fases del juego

El juego tiene 3 fases, controladas solo por el bot admin:

1. **Inactivo** (por defecto) — nadie puede `/unirme` ni responder.
2. **Lobby** (`/iniciar`) — se abre la inscripción: los jugadores pueden `/unirme` al bot de
   jugadores y quedan anotados, pero **todavía no reciben ninguna pregunta**. Esperan.
3. **Jugando** (`/comenzar`) — se cierra el lobby y **todos los anotados reciben la pregunta 1
   al mismo tiempo**. A partir de ahí cada uno juega a su ritmo, respondiendo A/B/C/D.

`/detener` corta todo y vuelve a "Inactivo" (hace falta `/iniciar` de nuevo para reabrir el
lobby). `/reiniciar` borra el progreso de todos sin cambiar la fase actual (útil para repetir la
partida sin salir del modo "jugando"). `/resetear` es un borrado total: borra a todos los
participantes, corta el juego (vuelve a "Inactivo") y olvida el chat admin guardado — para dejar
todo como recién importado, sin que quede ningún jugador guardado de una prueba anterior.

## Requisitos previos

1. **Cuenta de n8n Cloud** (https://n8n.io) con una instancia ya creada (`https://tu-subdominio.app.n8n.cloud`).
2. **Dos bots de Telegram**, creados con [@BotFather](https://t.me/BotFather):
   - Hablale a @BotFather, mandale `/newbot`, elegí nombre y username → repetí esto **dos
     veces** para tener un bot de jugadores y un bot admin, cada uno con su propio token
     (forma `123456789:AA...`).
   - Abrí un chat con cada uno de los dos bots y mandale `/start` para habilitar que te escriban.
3. **API key de n8n Cloud** (solo si vas a usar los scripts de automatización, no para el setup
   manual): `Settings → n8n API → Create an API key` en tu instancia.
4. **Node.js 18 o superior**, solo para `npm test` y los scripts opcionales — no hace falta para
   el setup manual en el editor.

## Setup manual en el editor de n8n (recomendado)

1. **Abrí tu workflow** en n8n Cloud (uno vacío o uno existente).
2. **Importá el JSON**: menú **⋮ (tres puntitos)** arriba a la derecha → **Import from File...**
   → seleccioná `trivia_telegram.json` (en esta carpeta). Deberían aparecer 34 nodos conectados.
   Si ya habías importado una versión anterior, primero seleccioná todo el canvas (`Ctrl+A`) y
   borralo (`Delete`) antes de reimportar, para no dejar nodos viejos mezclados.
3. **Credencial del bot jugadores**: doble click en **Telegram Trigger - Recibir Mensaje** →
   "Credential to connect with" → **Create New Credential** → pegá el token del bot jugadores en
   **Access Token** → Save. Abrí **Responder al Jugador** y elegí esa misma credencial del
   dropdown (no crees una nueva).
4. **Credencial del bot admin**: doble click en **Telegram Trigger - Admin** → **Create New
   Credential** → pegá el token del bot admin → Save. Abrí **Notificar al Admin** y
   **Responder al Admin** y elegí esa misma credencial en ambos.
5. **Guardá y activá**: `Ctrl+S`, después el toggle **Active** arriba a la derecha → ON.

No hace falta configurar ningún chat_id a mano: el workflow guarda automáticamente el chat desde
donde mandaste `/iniciar` y le manda ahí mismo las notificaciones de cada respuesta.

### Probarlo

1. Hablale al **bot admin**: mandale `/iniciar`. Te confirma que se abrió el lobby (y este chat
   queda guardado como el que va a recibir las notificaciones de la partida).
2. Desde uno o más chats (pedile a gente que te ayude a probar), hablale al **bot jugadores**:
   `/unirme` → responde "te uniste, esperá /comenzar" — **todavía no manda la pregunta**.
3. De vuelta al **bot admin**: mandale `/comenzar`. Ahí sí, todos los que mandaron `/unirme`
   reciben la pregunta 1 al mismo tiempo, y a vos te llega la confirmación de cuántos van a jugar.
4. A medida que cada jugador responde, te va llegando a vos (al bot admin) un mensaje por cada
   respuesta — ej. "✅ Martín respondió la pregunta 1 con: A -> avanza a la pregunta 2" o, si
   termina las 5, "🏁 Martín completó el juego con 4/5 puntos."
5. Cuando **todos** los jugadores que se unieron terminan las 5 preguntas, se manda solo una
   **tabla de clasificación** (ej. "🥇 Ana - 5/5 puntos", "🥈 Beto - 3/5 puntos") tanto a vos como
   a cada jugador — no hace falta pedirla, se dispara automáticamente con la última respuesta.
6. `/detener` (al bot admin) corta todo y vuelve a "Inactivo" — hace falta `/iniciar` de nuevo
   para abrir un lobby nuevo. `/reiniciar` (al bot admin) borra el progreso de todos sin cambiar
   la fase actual. `/resetear` (al bot admin) es el borrado total — para dejar todo limpio antes
   de una nueva demo, sin ningún jugador de pruebas anteriores guardado.

## Setup por API (alternativa, si preferís no tocar el editor)

Requiere completar `.env` (copiá `.env.example`) con `N8N_CLOUD_URL`, `N8N_API_KEY`,
`TELEGRAM_BOT_TOKEN_JUGADORES` y `TELEGRAM_BOT_TOKEN_ADMIN`.
`.env` está en `.gitignore`, nunca se commitea.

```bash
npm run setup:import      # importa/actualiza trivia_telegram.json en tu cuenta de n8n Cloud
npm run setup:credencial  # crea las 2 credenciales de Telegram y las asocia a los nodos correctos
npm run setup:activar     # activa el workflow y verifica los 2 webhooks
```

Si `N8N_WORKFLOW_ID` está seteado en `.env`, `setup:import` actualiza ese workflow existente en
vez de crear uno nuevo (`PATCH` en lugar de `POST`).

Si algún paso falla porque tu versión de n8n Cloud cambió nombres de parámetros o el formato de
alguna API, el mensaje de error te va a decir cuál fue y, en el caso de las credenciales, te da
el paso manual puntual para hacer en el editor sin frenar el resto del setup.

## Tests de la lógica del juego

La lógica de los nodos Code (interpretar mensaje de jugador, interpretar comando de admin,
cargar estado, iniciar/detener el juego, reiniciar, evaluar y avanzar, preparar mensaje) está
traducida 1:1 a funciones puras en `logica/trivia.js`, para poder testearla sin depender de n8n
ni de Telegram real. El workflow importado sigue usando su propio código embebido en cada
nodo — este módulo es solo para validar la lógica.

```bash
npm test
```

Cubre: el juego arranca en fase "inactivo", `/iniciar` abre el lobby sin repartir la pregunta,
unirse durante el lobby queda anotado sin avanzar, `/comenzar` manda la pregunta 1 a todos los
anotados a la vez y pasa a "jugando" (incluso con el lobby vacío), responder correcto (por letra
y por texto completo), responder incorrecto (avanza igual, sin reintento), completar las 5
preguntas, `/detener` vuelve a "inactivo", `/reiniciar` sin tocar la fase actual, `/resetear`
como borrado total (participantes, fase y admin guardado), dos participantes jugando en paralelo
sin pisarse el progreso, que la tabla de posiciones no se dispara hasta que **todos** terminaron,
y que la tabla queda ordenada de mayor a menor puntaje.

## Desactivar después de la expo

Toggle **Active** a OFF en el editor, o por API:

```bash
npm run desactivar
```

Con eso alcanza: n8n deja de tener los webhooks activos y Telegram deja de mandarle updates.

## Troubleshooting

- **Mandé `/unirme` y no pasa nada, o me dice que espere:** revisá en qué fase está el juego —
  necesitás `/iniciar` (abre el lobby) antes de poder unirte, y `/comenzar` (del bot admin) antes
  de que llegue la primera pregunta. `/unirme` durante el lobby responde "esperá /comenzar" a
  propósito, no es un error.
- **El bot de jugadores no responde nada (ni siquiera "esperá"):**
  1. Confirmá que el workflow esté activo (toggle **Active** en el editor).
  2. Revisá `https://api.telegram.org/bot<TOKEN_JUGADORES>/getWebhookInfo` — el campo `url`
     debería contener el dominio de tu instancia de n8n Cloud.
  3. Abrí **Telegram Trigger - Recibir Mensaje** y **Responder al Jugador** en el editor y
     confirmá que el dropdown de credencial no esté vacío y sea el bot correcto.
- **El bot admin no responde a `/iniciar`/`/comenzar`/`/detener`/`/reiniciar`/`/resetear`:** mismos chequeos
  que arriba pero sobre `Telegram Trigger - Admin`, `Notificar al Admin` y
  `Responder al Admin`, con `getWebhookInfo` del `TOKEN_ADMIN`.
- **Mandé `/comenzar` y nadie recibió la pregunta:** probablemente nadie mandó `/unirme` durante
  el lobby (o mandaste `/comenzar` antes de que se unieran). Revisá el mensaje de confirmación
  que te llega a vos — dice cuántos jugadores recibieron la pregunta.
- **Token inválido:** revisá que el token en `.env` o en la credencial del editor sea
  exactamente el que te dio @BotFather para ese bot específico (es fácil confundir los dos).
- **Los jugadores responden pero a mí (admin) no me llega ningún aviso:** el chat que recibe
  esos avisos es el que mandó el último `/iniciar` — si reabriste el lobby desde otro chat o
  usuario, las notificaciones van a ese chat nuevo, no al anterior. Además confirmá que
  **Notificar al Admin** tenga la credencial del bot admin bien seleccionada.
- **Nunca llega la tabla de clasificación final:** solo se dispara cuando **todos** los que
  mandaron `/unirme` durante el lobby completaron las 5 preguntas — si alguien se unió pero nunca
  respondió nada, el juego se queda esperando a esa persona para siempre. Usá `/reiniciar` o
  `/resetear` si necesitás forzar el cierre de esa partida.
- **Un nodo de Telegram tira "Bad request" con algún campo vacío (`chat_id`, etc.):** en esta
  versión de n8n Cloud el "Include Other Input Fields" de los nodos Set no siempre
  preserva los campos que no seteás a mano — si agregás un campo nuevo en algún nodo Code y lo
  necesitás más adelante en la cadena, agregalo como asignación explícita en cada nodo Set
  intermedio (`Avanzó de Pregunta`, `Mensaje Final (Ganador)`, `Mostrar Pregunta Actual`)
  en vez de asumir que va a pasar solo.
- **`n8n API POST /credentials -> HTTP 4xx`** (solo si usás los scripts): tu instancia puede no
  exponer el tipo `telegramApi` vía API en esa versión — creá las credenciales a mano en el
  editor y asocialas vos mismo, después corré igual `npm run setup:activar` para el resto.
