# Protocolo de Cierre de Rampa — Aeropuertos Argentinas (demo n8n)

Flujo de n8n que orquesta la respuesta operativa ante condiciones meteorológicas severas
en rampa: evalúa un reporte tipo METAR, identifica los vuelos en ventana de riesgo y
dispara en paralelo las notificaciones a las áreas involucradas (pista, mantenimiento,
terminal, auditoría). Preparado como demo técnica para la defensa del TPI.

## 1. Payload mock (`mock_data.json`)

Simula el input que en un sistema real vendría de una fuente meteorológica (AIS/METAR)
combinado con el sistema de programación de vuelos. Incluye:

- **`reporte_meteorologico`**: un METAR crítico para SAEZ (Ezeiza) — viento sostenido
  38kt con ráfagas de 52kt, tormenta eléctrica activa (`+TSRA`), windshear reportado en
  todas las pistas (`WS ALL RWY`) y nubosidad convectiva (CB). Son las condiciones que en
  la operación real obligan a evaluar el cierre de plataforma.
- **`vuelos_programados`**: 4 vuelos (Aerolíneas Argentinas, JetSmart, Flybondi) con
  operaciones de despegue/aterrizaje escalonadas entre los 15 y los 44 minutos siguientes
  al reporte — todos caen dentro de la ventana de riesgo de 45 minutos.

Se inyecta directamente como **pinData** del nodo Manual Trigger dentro de
`cierre_rampa_workflow.json`, así que al importar el workflow ya queda listo para
ejecutar sin tocar nada.

## 2. Lógica de evaluación (`evaluar_riesgo.js`)

Código del nodo **Evaluar Riesgo Meteorologico** (`n8n-nodes-base.code`). Aplica una
escala de 4 niveles en base a umbrales operativos configurables al principio del script:

| Nivel | Condición | Acción |
|---|---|---|
| 3 | Tormenta eléctrica **y** (ráfaga ≥ 45kt **o** windshear reportado) | `CIERRE_RAMPA` |
| 2 | Tormenta eléctrica, o ráfaga ≥ 45kt, o visibilidad ≤ 1500m | `ALERTA_PREPARAR_CIERRE` |
| 1 | Viento sostenido ≥ 30kt sin tormenta | `MONITOREO_ACTIVO` |
| 0 | Ninguna de las anteriores | `OPERACION_NORMAL` |

Además filtra `vuelos_programados` a los que caen dentro de la ventana de
`VENTANA_MINUTOS` (45 por defecto) desde la hora del reporte, y le agrega a cada uno
`minutos_hasta_operacion` para trazabilidad. Devuelve un único item con:
`riesgo_nivel`, `riesgo_nivel_3` (booleano), `accion_requerida`, `resumen`,
`cantidad_vuelos_afectados`, `vuelos_afectados` y el reporte meteorológico original.

Con el mock incluido, el resultado es `riesgo_nivel: 3` con los 4 vuelos afectados —
verificado corriendo el script fuera de n8n antes de armar el workflow.

## 3. Estructura de nodos

```
Ingesta de Reporte (Manual Trigger)
        |
        v
Evaluar Riesgo Meteorologico (Code)
        |
        v
Switch Nivel de Riesgo
        |
        +-- [Nivel 3 - Cierre Total] --+--> Notificar Cierre a Operaciones de Pista   (Telegram)
        |                              +--> Crear Ticket de Mantenimiento             (Trello)
        |                              +--> Enviar Alerta a Terminal                  (Gmail)
        |                              +--> Registrar Auditoria                       (Google Sheets)
        |
        +-- [Nivel 2 - Alerta] -------------> Registrar Auditoria                     (Google Sheets)
        |
        +-- [Nivel 0/1 - Normal] -----------> Sin Accion Requerida                    (NoOp)
```

**Por qué Switch y no If:** el nodo `If` solo da dos salidas (verdadero/falso). Acá hay
una escala de severidad de 4 niveles con respuestas operativas distintas — `Switch` con
`mode: rules` modela esa semántica de forma explícita, con una salida por nivel y un
`fallbackOutput` para el caso normal, en vez de anidar varios `If` uno adentro del otro.

**Por qué las 4 ramas del Nivel 3 salen del mismo output:** en n8n una sola salida puede
tener múltiples conexiones — el mismo item se copia y se manda en paralelo a los 4 nodos
sin que dependan entre sí. Si notificar a Telegram falla, igual se crea el ticket de
Trello, se manda el mail y se registra la auditoría (no es una cadena secuencial, es un
fan-out real). Es el mismo patrón que usa `Notificar al Admin` en el bot de trivia para
avisar a la vez al organizador y al jugador.

**Justificación de negocio por rama:**
- **Telegram → Operaciones de Pista:** el canal más rápido para coordinar en tiempo real
  con el personal físicamente en plataforma (equipos de rampa, supervisores).
- **Trello → Mantenimiento:** deja un ticket trazable para asegurar equipos móviles
  (escaleras, cintas, GPU) antes de que llegue el viento fuerte — trabajo que no es
  "avisar" sino "hacer", por eso va a un board de tareas y no a un chat.
- **Gmail → Terminal:** los stakeholders de terminal (gerencia de turno, informes al
  pasajero) necesitan un registro formal por mail, no un mensaje de chat que se pierde
  en el scroll.
- **Google Sheets → Auditoría:** cumplimiento y trazabilidad — quedó un registro de qué
  pasó, cuándo, y qué vuelos estuvieron expuestos, para el análisis posterior del
  evento (auditoría regulatoria, informe a ANAC, etc.). Alternativa productiva:
  reemplazar por un nodo **Postgres** (`insert` en una tabla `eventos_meteorologicos`)
  si se quiere integrar con un data warehouse en vez de una planilla.

## 4. Importar el workflow

1. En n8n: menú **⋮ → Import from File...** → `cierre_rampa_workflow.json`. Deberían
   aparecer 8 nodos conectados, con el mock ya cargado como pinData en el Manual Trigger.
2. Configurá las credenciales de los 4 nodos de salida (Telegram, Trello, Gmail, Google
   Sheets) — cada uno con su cuenta/API key correspondiente. Sin credenciales el workflow
   igual se puede abrir y ejecutar el tramo Code/Switch para la demo de lógica; para que
   las notificaciones salgan de verdad necesitás completarlas.
3. Reemplazá los placeholders (`TU_CHAT_ID_OPERACIONES_PISTA`, `TU_LIST_ID_TRELLO_MANTENIMIENTO`,
   `TU_SPREADSHEET_ID`, el email de Gmail) por los valores reales de tu demo.
4. Click en **Execute Workflow** — al estar pineado el Manual Trigger, corre directo con
   el escenario crítico sin que tengas que tipear nada en vivo.

### Nota de versión

Los parámetros de `Switch`, `Trello`, `Gmail` y `Google Sheets` están escritos contra las
versiones de esos nodos más comunes en n8n Cloud/self-hosted recientes
(`typeVersion` 3, 1, 2.1 y 4.5 respectivamente). Si tu instancia tiene una versión distinta
y el editor marca algún campo como inválido al abrir el nodo, es normal — n8n te lo señala
en rojo y alcanza con volver a seleccionar el valor desde el dropdown correspondiente
(pasa lo mismo que documentamos con el bot de trivia: cambios de esquema entre versiones
de nodo son la causa más común de estos desajustes, no un error de lógica).

## 5. Motor de Triage — arquitectura de ingesta y enrutamiento de vuelos

Segunda etapa del sistema, centrada exclusivamente en cómo se desarma el array de vuelos
activos y se enruta cada uno según su estado operativo. Es un subsistema aparte dentro
del mismo workflow — comparte el Manual Trigger con el protocolo de cierre de rampa, pero
corre en paralelo, con su propia cadena de nodos.

### 5.1 Payload de ingesta (`mock_data_triage.json`)

Dos campos nuevos, agregados también al `pinData` del Manual Trigger para que una sola
ejecución dispare las dos partes del sistema:

- **`meteorologia`**: versión resumida del contexto climático (tipo de alerta, ráfagas,
  actividad eléctrica) — pensada como la entrada mínima que necesitaría un motor de triage
  desacoplado del detalle completo del METAR.
- **`vuelos_activos`**: 4 vuelos que cubren los 3 estados operativos posibles:
  - `AR1130` — `en_aproximacion`, 32 min de combustible → dispara alerta crítica.
  - `JA3045` — `en_aproximacion`, 58 min de combustible → dentro de rango normal.
  - `AR1303` — `embarcando`.
  - `FO2210` — `listo_para_pushback`.

  `combustible_remanente_minutos` solo existe en los vuelos `en_aproximacion` — es un dato
  que no aplica a un avión todavía en la puerta de embarque, así que omitirlo en esos casos
  es más correcto que forzar un `null`.

### 5.2 Configuración de nodos, paso a paso

**Nodo `Desarmar Vuelos Activos` (Item Lists):**
1. Agregar un nodo **Item Lists**, conectado directo desde el Manual Trigger.
2. Operation: **Split Out Items**.
3. Field To Split Out: `vuelos_activos`.

Con eso, un item que tenía un array de 4 vuelos adentro se convierte en 4 items
independientes, cada uno con un solo vuelo como `json` — es lo que permite que el `Switch`
de abajo evalúe a cada vuelo por separado. (Alternativa: **Split In Batches** con tamaño de
lote 1 logra un desarmado similar, pero está pensado para *loopear* con control manual de
iteración — para este caso, donde no hace falta ese control, `Item Lists` es más directo.)

**Nodo `Switch Triage por Estado`:**
1. Mode: **Rules**.
2. Una sola regla: `{{ $json.estado_operativo }}` **equals** `en_aproximacion` → output
   renombrado **"Rama A - En Aproximacion"**.
3. En Options, activar **Fallback Output** (captura todo lo que no matcheó la regla) y
   renombrarlo **"Rama B - En Tierra"**.

Con una sola regla alcanza porque `embarcando` y `listo_para_pushback` reciben el mismo
tratamiento (sumar demora) — no hace falta una rama por cada valor posible de
`estado_operativo`, sino agrupar por el tipo de respuesta que requieren.

**Rama A — nodo Code `Evaluar Riesgo de Desvio`** (`riesgo_desvio.js`):
Compara `combustible_remanente_minutos` contra el umbral de 45 minutos. Si está por
debajo, arma el mensaje de alerta crítica pidiendo desvío a MVD o COR; si no, confirma que
la aproximación puede continuar con normalidad. Probado contra el mock: `AR1130` (32 min)
da `riesgo_critico_combustible: true`, `JA3045` (58 min) da `false` — el umbral separa
correctamente los dos casos.

**Rama B — nodo Code `Calcular Nuevo ETD`** (`calcular_etd.js`):
Se evaluaron dos formas de sumarle 90 minutos a `hora_programada_original`:

- **Nodo `Date & Time` nativo** (operación "Add to Date"): funciona, pero su configuración
  vive enteramente en la UI (unidad de tiempo, cantidad, campo de entrada/salida) y esos
  parámetros son de los que más cambiaron de nombre entre versiones de n8n — el mismo
  problema de "desajuste de esquema" que ya documentamos para `Switch`/`Trello`/`Gmail`,
  pero más probable acá porque es un nodo que se usa con menos frecuencia.
- **Código JS directo con el objeto `Date`** (lo que se usa en este workflow): mismo
  resultado, cero dependencia de la versión del nodo, y consistente con el resto del
  proyecto — `Evaluar Riesgo Meteorologico` ya hace aritmética de fechas a mano
  (`minutos_hasta_operacion`) por la misma razón.

Si igual querés mostrar el nodo `Date & Time` nativo en la demo (para variar los tipos de
nodo que se ven en el canvas), configuralo así: Action **"Add to a Date"**, Date `{{
$json.hora_programada_original }}`, Duration `90`, Time Unit `Minutes`, y guardá el
resultado con el campo de salida renombrado a `nuevo_ETD_estimado` en el "Output Field
Name". Probado contra el mock con el código JS: `AR1303` (embarcando, 21:15Z) da
`22:45:00Z`; `FO2210` (pushback, 21:05Z) da `22:35:00Z` — ambos exactamente +90 minutos.

### 5.3 Por qué quedó como subsistema aparte, no integrado a las 4 ramas de notificación

A propósito, esta etapa no conecta `Evaluar Riesgo de Desvio` ni `Calcular Nuevo ETD` a
Telegram/Trello/Gmail/Sheets. El pedido fue enfocarse solo en la arquitectura de ingesta y
el motor de triage — dejar los resultados como salida de cada rama (en vez de forzarlos a
una notificación) es más honesto sobre el alcance real de esta etapa, y más fácil de
extender después: conectar `Evaluar Riesgo de Desvio` a `Notificar Cierre a Operaciones de
Pista` cuando `riesgo_critico_combustible` sea `true`, por ejemplo, es un cambio de una
sola conexión el día que se quiera integrar todo en un único protocolo end-to-end.
(Nota: en la evolución de la sección 6 esa conexión final ya se agregó.)

## 6. Evolución a datos en tiempo real (APIs reales, sin mock)

23 nodos en total. El motor de triage ya no depende del `pinData` del Manual Trigger —
ahora tiene su propia cadena de ingesta en vivo, en paralelo al protocolo de cierre por
METAR (que sigue funcionando con el mock, sin tocarlo, como demo offline de respaldo).

### 6.1 Disparador parametrizable

`Disparador Programado (Cada 10s)` es un `Schedule Trigger` con `rule.interval` en modo
`seconds`, `secondsInterval: 10`.

**Sobre "fácilmente modificable por un usuario no técnico" — con una precisión importante:**
n8n resuelve el intervalo del Schedule Trigger **al activar el workflow**, antes de que
exista ningún contexto de ejecución — por eso ese campo específico **no acepta
expresiones** (`{{ }}`) ni puede leer de un nodo Set o de una variable de entorno; el
ícono de función (`fx`) ni siquiera aparece en ese campo en el editor. La única forma real
de cambiar el "cada 10 segundos" es editando el número directo en el nodo — que de por sí
ya es "no técnico" (un campo numérico, cero código).

Lo que **sí** se movió a una capa de configuración editable es todo lo demás: el nodo Set
`Configuracion (Editar Aca)`, colgado justo después del trigger, centraliza
`aeropuerto_iata`, `aeropuerto_lat/lon`, `umbral_combustible_critico_min`,
`demora_cierre_min` y `refresco_apis_min` — un operador no técnico cambia estos valores
sin tocar ningún código JS, y todos los nodos downstream los leen por expresión
(`$('Configuracion (Editar Aca)').first().json...`) en vez de tener los números
hardcodeados desperdigados. Las API keys, en cambio, si tu instancia de n8n lo permite,
son mejor candidato para variables de entorno de n8n (`$env.OPENWEATHER_API_KEY`) en vez
del Set, precisamente porque un secreto no debería poder verse abriendo un nodo Set en el
editor.

### 6.2 Ingesta desde APIs reales + Rate Limiting

Tres nodos `HTTP Request` (no dos — ver nota abajo):

- `Consultar Clima Real (OpenWeatherMap)`: `GET /data/2.5/weather` con `lat`/`lon` del
  aeropuerto (tomados de `Configuracion`), `units=metric`.
- `Consultar Vuelos Arribos Real (AviationStack)`: `GET /v1/flights` con `arr_iata=EZE` —
  alimenta la Rama A (`en_aproximacion`).
- `Consultar Vuelos Salidas Real (AviationStack)`: `GET /v1/flights` con `dep_iata=EZE` —
  alimenta la Rama B (`embarcando`/`listo_para_pushback`).

**Por qué tres nodos y no dos:** AviationStack no tiene un filtro "vuelos en este
aeropuerto en cualquier sentido" — `dep_iata` y `arr_iata` combinados en la misma llamada
se interpretan como *ruta* (de X a Y), no como *OR*. Como la Rama A necesita arribos y la
Rama B necesita salidas, hacen falta dos llamadas de vuelos distintas. Si preferís ceñirte
literalmente a "dos nodos HTTP", la alternativa es unificar en una sola llamada
`arr_iata` y aceptar que la Rama B quede sin dato real (solo simulado) — es un cambio de
una línea si lo preferís así para la demo.

**Rate Limiting — la consideración de ingeniería central de esta etapa:** a 10s de
intervalo, en una hora eso son 360 llamadas por API. OpenWeatherMap free tier (60
llamadas/min) lo tolera de sobra. **AviationStack free tier NO** — son apenas 100
llamadas/mes en total; a 360/hora se agota la cuota en menos de 20 minutos. Por eso el
Schedule Trigger de 10s **no dispara las llamadas HTTP directamente**: pasa primero por
`Verificar Necesidad de Refresco`, que compara `Date.now()` contra un timestamp guardado en
`$getWorkflowStaticData('global')` y solo deja pasar a las APIs reales cada
`refresco_apis_min` minutos (5 por defecto, configurable). El resto de las ejecuciones
(la gran mayoría) toma `Usar Datos en Cache` y reutiliza la última respuesta guardada.
Resultado: el motor de triage sigue reaccionando cada 10s sobre datos ya conocidos (rápido
para la demo), pero las APIs externas se consultan a un ritmo sostenible. Es el mismo
patrón que usaría cualquier integración real contra una API de terceros con cuota
limitada — desacoplar "frecuencia de reacción" de "frecuencia de consulta externa".

### 6.3 Capa de normalización (Anti-Corruption Layer)

`Normalizar Datos de APIs` traduce las respuestas crudas de ambas APIs al contrato interno
`{ meteorologia, vuelos_activos }` que ya esperaba el motor de triage — ningún nodo aguas
abajo necesita saber que esos datos vinieron de OpenWeatherMap o AviationStack. Puntos
técnicos del script:

- **Detección de tormenta**: los códigos 200-232 de OpenWeatherMap son el grupo
  "Thunderstorm" — se chequea `clima.weather[].id` contra esa lista.
- **Conversión de unidades**: OpenWeatherMap devuelve viento en m/s (`units=metric`); se
  convierte a nudos (`× 1.94384`) porque todo el resto del sistema (METAR, umbrales) ya
  trabaja en nudos.
- **Filtro de vuelos irrelevantes**: solo se procesan `flight_status === 'active'`
  (arribos) y `'scheduled'` (salidas) — vuelos `landed`, `cancelled`, `diverted` se
  descartan antes de llegar al triage.
- **Límite honesto de los datos públicos**: ninguna API pública de tracking expone
  combustible remanente real — es dato propietario ACARS/OOOI de cada aerolínea, nunca
  público. `combustible_remanente_minutos` se estima con una heurística simple a partir de
  la altitud en vivo, marcada como tal en el comentario del código. En una integración real
  con Aeropuertos Argentinas, ese dato saldría de un feed interno de la aerolínea/torre, no
  de una API de terceros — vale la pena decir esto explícitamente en la defensa: **muestra
  que entendés la diferencia entre lo que es públicamente integrable y lo que requeriría
  acceso privilegiado**, en vez de simular que la demo tiene datos que ninguna API real da.

Probado con respuestas simuladas con la forma real de ambas APIs (incluyendo vuelos
`landed`/`cancelled` para confirmar que se filtran) antes de subir el workflow — filtró
correctamente y clasificó cada vuelo en la rama esperada.

### 6.4 Integración con el Triage

`Normalizar Datos de APIs` y `Usar Datos en Cache` convergen ambos en `Desarmar Vuelos
Activos` (el mismo nodo `Item Lists` de la sección 5) — el Manual Trigger dejó de
alimentarlo; ahora es 100% la rama en tiempo real. `Switch Triage por Estado`, `Evaluar
Riesgo de Desvio` y `Calcular Nuevo ETD` no cambiaron de lógica, solo de origen de datos.

### 6.5 Alerta por Telegram sin firma de n8n

`Alertar Riesgo Critico a Operadores` cuelga de un nodo `If` nuevo
(`Es Riesgo Critico de Combustible?`) conectado después de `Evaluar Riesgo de Desvio` —
solo dispara cuando `riesgo_critico_combustible` es `true`.

**Dónde está `appendAttribution` en la interfaz:** al abrir el nodo Telegram, el campo está
adentro de **"Additional Fields"** (justo debajo de "Text") → hay que agregar el campo
**"Append n8n Attribution"** desde el selector de "Add Field" y dejarlo en **OFF**. Por
defecto ese campo no aparece en el panel (hay que agregarlo explícitamente), y por defecto
vale `true` — por eso el mensaje "This message was sent automatically with n8n" aparece a
menos que lo agregues y lo apagues vos. En el JSON exportado ya quedó como
`"additionalFields": { "appendAttribution": false }` en los dos nodos de Telegram del
workflow (el original y el nuevo), así que no hace falta tocar nada a mano — pero vale
saber dónde está el campo para poder mostrarlo en la defensa si preguntan.

## 7. Fusión del motor original y el motor en tiempo real

Al construir la sección 6 quedó un problema: el pipeline en tiempo real (Schedule
Trigger → APIs → `Normalizar Datos de APIs`) y el protocolo original de Cierre de Rampa
(`Evaluar Riesgo Meteorologico` → `Switch Nivel de Riesgo` → Telegram/Trello/Gmail/Sheets)
corrían en paralelo pero **sin tocarse**: el dato meteorológico real nunca llegaba al
motor que decide el cierre de rampa, así que las notificaciones seguían dependiendo
100% del mock del Manual Trigger. Se resolvió así:

- `Normalizar Datos de APIs` y `Usar Datos en Cache` ahora devuelven, además de
  `meteorologia`/`vuelos_activos` (formato Triage), los mismos datos en el formato que
  espera `Evaluar Riesgo Meteorologico`: `reporte_meteorologico` y `vuelos_programados`.
  Es el mismo dato en vivo, traducido a los dos contratos.
- Se agregó una segunda conexión desde esos dos nodos hacia `Evaluar Riesgo
  Meteorologico` (fan-out, sin nodo `Merge` — mismo patrón usado en el resto del
  workflow). El Manual Trigger sigue conectado a ese mismo nodo como demo offline.
  Resultado: **un único nodo de riesgo y una única cadena de notificaciones sirven
  tanto al botón manual (mock) como al pipeline en tiempo real (Schedule Trigger)**.
- Los campos que ninguna API pública expone (`windshear_reportado`, `metar_crudo`,
  `posicion_rampa`, `matricula`) quedan explícitamente en `false`/`'N/D'`/texto
  descriptivo en vez de inventarse — mismo criterio de honestidad técnica que en la
  sección 6.3.

**Sobre el error "Invalid API key" de OpenWeatherMap:** las claves de OpenWeatherMap y
AviationStack estaban hardcodeadas como texto placeholder (`TU_OPENWEATHER_API_KEY` /
`TU_AVIATIONSTACK_API_KEY`) directamente en los nodos HTTP Request. Ahora viven como dos
campos más en `Configuracion (Editar Aca)` (`openweather_api_key`,
`aviationstack_api_key`) y los 3 nodos HTTP las leen desde ahí por expresión — coherente
con el resto del diseño (un único lugar para editar parámetros). Para que ese nodo deje
de fallar hace falta reemplazar el valor placeholder por una clave real:

1. Entrá a [home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up) y creá una cuenta gratis (dato tuyo, tenés que hacerlo vos).
2. Una vez logueado, andá a la pestaña **"API keys"** de tu perfil — ahí tenés una clave por default (o generá una con "Generate").
3. Ojo: una clave nueva de OpenWeatherMap suele tardar **entre 10 minutos y 2 horas** en activarse — si probás el nodo enseguida y sigue dando 401, no está roto, esperá un rato.
4. Copiá esa clave y pegala en el campo `openweather_api_key` del nodo `Configuracion (Editar Aca)`, reemplazando `TU_OPENWEATHER_API_KEY`.
5. Mismo circuito para AviationStack: [aviationstack.com/signup/free](https://aviationstack.com/signup/free) → copiar el "Access Key" del dashboard → pegarlo en `aviationstack_api_key`.

Verificado (fuera de n8n, con datos simulados con la forma real de ambas APIs): la
salida de `Normalizar Datos de APIs` alimentada a `Evaluar Riesgo Meteorologico` produce
correctamente `riesgo_nivel: 3` / `CIERRE_RAMPA` cuando el clima simulado tiene tormenta
+ ráfaga sobre el umbral, con el vuelo afectado correctamente calculado. Subido a n8n vía
`scripts/subir_workflow.js`: los 23 nodos se preservaron por nombre (0 nodos nuevos) y
las 4 credenciales configuradas (2 Telegram, Trello, SMTP) siguen intactas.

## 8. Eliminación de la rama de riesgo por combustible

La Rama A del Triage (`Evaluar Riesgo de Desvio`, el `If` `Es Riesgo Critico de
Combustible?` y el Telegram `Alertar Riesgo Critico a Operadores`) se sacó del workflow
por completo. El motivo no es técnico sino de honestidad de datos: esa rama tomaba una
decisión automática — alertar para desviar un vuelo a un aeropuerto alterno — en base a
`combustible_remanente_minutos`, un valor que **nunca fue un dato real**: se estimaba con
una heurística a partir de la altitud en vivo del avión, porque ninguna API pública
expone el combustible remanente real (es dato propietario ACARS/OOOI de cada aerolínea).
Automatizar una alerta operacional crítica sobre un número inventado no tiene sentido en
un sistema real, así que se eliminó en vez de dejarlo como si fuera funcional.

`Switch Triage por Estado` sigue clasificando los vuelos en aproximación vs. en tierra
(es una distinción real y verificable), pero ahora los vuelos en aproximación terminan en
un `NoOp` (`Vuelos en Aproximacion (Sin Accion Automatica)`) — se identifican y quedan
documentados, sin una acción automática inventada sobre ellos. La Rama B
(`Calcular Nuevo ETD`, recálculo de demora para vuelos en tierra) no se tocó: esa sí usa
únicamente datos reales (hora programada + demora configurada). También se sacó
`combustible_remanente_minutos` del Code `Normalizar Datos de APIs`, ya que no queda
ningún nodo que lo consuma. El archivo `riesgo_desvio.js` (referencia local de esa lógica)
se borró del proyecto.
