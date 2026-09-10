# 📖 Documentación Técnica de la API — Laboratorio ATS

> Guía paso a paso de cómo funciona la integración con la IA (Groq) en este proyecto.

---

## Índice

1. [Stack tecnológico](#1-stack-tecnológico)
2. [Configuración del entorno](#2-configuración-del-entorno)
3. [Arquitectura general](#3-arquitectura-general)
4. [Flujo completo de una request](#4-flujo-completo-de-una-request)
5. [Paso 1 — Recepción de archivos (Middleware)](#5-paso-1--recepción-de-archivos-middleware)
6. [Paso 2 — Extracción de texto del PDF](#6-paso-2--extracción-de-texto-del-pdf)
7. [Paso 3 — Construcción del prompt para la IA](#7-paso-3--construcción-del-prompt-para-la-ia)
8. [Paso 4 — Llamada a la API de Groq](#8-paso-4--llamada-a-la-api-de-groq)
9. [Paso 5 — Parseo y respuesta al cliente](#9-paso-5--parseo-y-respuesta-al-cliente)
10. [Manejo de errores](#10-manejo-de-errores)
11. [Endpoints disponibles](#11-endpoints-disponibles)
12. [Ejemplo de respuesta completa](#12-ejemplo-de-respuesta-completa)

---

## 1. Stack tecnológico

| Capa | Tecnología | Uso |
|---|---|---|
| Servidor | **Express.js** | HTTP server y routing |
| IA | **Groq SDK** (`groq-sdk`) | LLM via API |
| Modelo | **llama-3.3-70b-versatile** | Análisis de CVs |
| Archivos | **Multer** | Recepción de uploads |
| PDF | **pdf-parse** | Extracción de texto |
| Config | **dotenv** | Variables de entorno |

---

## 2. Configuración del entorno

Antes de arrancar el servidor, la app valida que la API key de Groq esté presente. La configuración se centraliza en `src/config/environment.js`:

```js
// src/config/environment.js
const dotenv = require("dotenv");
const path = require("path");

dotenv.config({ path: path.resolve(__dirname, "../../.env") });

const REQUIRED_VARS = ["GROQ_API_KEY"];

function validateEnvironment() {
  const missingVars = REQUIRED_VARS.filter(
    (varName) => !process.env[varName] || process.env[varName].trim() === ""
  );

  if (missingVars.length > 0) {
    throw new Error(
      `Variables de entorno faltantes: ${missingVars.join(", ")}. ` +
        "Revisar el archivo .env o la configuracion del entorno."
    );
  }
}

function getConfig() {
  return {
    groq: {
      apiKey: process.env.GROQ_API_KEY,
      model: process.env.GROQ_MODEL || "llama-3.3-70b-versatile",
      temperature: parseFloat(process.env.GROQ_TEMPERATURE || "0.3"),
      maxTokens: parseInt(process.env.GROQ_MAX_TOKENS || "4000", 10),
    },
    server: {
      port: parseInt(process.env.PORT || "3000", 10),
    },
  };
}
```

El archivo `.env` tiene esta forma:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=4000
PORT=3000
```

> [!IMPORTANT]
> El servidor arranca igual aunque falte la `GROQ_API_KEY` (muestra un warning), pero **fallará** en el momento en que se intente hacer un análisis.

---

## 3. Arquitectura general

```
Cliente (navegador)
        │
        │  POST /api/analyze  (multipart/form-data)
        ▼
┌─────────────────────┐
│     server.js       │  ← Entry point, configura Express + rutas
└────────┬────────────┘
         │
┌────────▼────────────┐
│  ats-controller.js  │  ← Router: valida input, orquesta el flujo
└────────┬────────────┘
         │
    ┌────┴─────────────────┐
    │                      │
┌───▼────────┐    ┌────────▼──────────┐
│ pdf-parser │    │   cv-analyzer.js  │  ← Construye prompt y parsea JSON
└────────────┘    └────────┬──────────┘
                           │
                  ┌────────▼──────────┐
                  │  groq-client.js   │  ← Llama a la API de Groq
                  └───────────────────┘
```

---

## 4. Flujo completo de una request

Cuando el usuario sube CVs y hace click en "Analizar", el flujo es:

```
1. Cliente envía POST /api/analyze con archivos PDF + datos del formulario
2. Multer intercepta los archivos → los guarda en memoria (buffer)
3. El controlador extrae el texto de cada PDF con pdf-parse
4. cv-analyzer construye el System Prompt + User Prompt
5. groq-client llama a la API de Groq con streaming
6. La respuesta (JSON) se parsea y se devuelve al cliente
```

---

## 5. Paso 1 — Recepción de archivos (Middleware)

El middleware `upload.js` usa **Multer** para interceptar los archivos antes de que lleguen al controlador. Los archivos se guardan **en memoria** (no en disco), lo que hace la app stateless.

```js
// src/middleware/upload.js
const multer = require("multer");
const { ValidationError } = require("../errors/app-errors");

const ALLOWED_MIMETYPES = ["application/pdf", "text/plain"];
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB por archivo
const MAX_FILES = 10;

// Almacenamiento en memoria: los PDFs llegan como Buffer
const storage = multer.memoryStorage();

const fileFilter = (req, file, cb) => {
  if (ALLOWED_MIMETYPES.includes(file.mimetype)) {
    cb(null, true);   // ✅ Aceptar
  } else {
    cb(
      new ValidationError(
        `Tipo de archivo no permitido: ${file.mimetype}. Solo se aceptan PDF y TXT.`
      ),
      false             // ❌ Rechazar
    );
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: MAX_FILES,
  },
});
```

Límites en resumen:

| Restricción | Valor |
|---|---|
| Tipos aceptados | `.pdf`, `.txt` |
| Tamaño máximo por archivo | 5 MB |
| Cantidad máxima de archivos | 10 |

---

## 6. Paso 2 — Extracción de texto del PDF

Una vez que Multer pone el archivo en `req.files`, el controlador llama a `extractTextFromPdf()` para convertir el buffer binario en texto plano.

```js
// src/services/pdf-parser.js
const pdfParse = require("pdf-parse");
const { FileParseError } = require("../errors/app-errors");

async function extractTextFromPdf(buffer) {
  try {
    const data = await pdfParse(buffer);

    if (!data.text || data.text.trim().length === 0) {
      throw new FileParseError(
        "El PDF no contiene texto extraible. Puede estar escaneado o protegido."
      );
    }

    return data.text;  // String con el texto completo del PDF
  } catch (error) {
    if (error instanceof FileParseError) throw error;
    throw new FileParseError(`Error al procesar el archivo PDF: ${error.message}`);
  }
}
```

En el controlador, esto se hace para **cada archivo** subido:

```js
// src/controllers/ats-controller.js (fragmento)
const cvTexts = [];

for (const file of req.files) {
  let text;

  if (file.mimetype === "application/pdf") {
    text = await extractTextFromPdf(file.buffer);  // ← PDF → texto
  } else {
    text = file.buffer.toString("utf-8");           // ← TXT → texto directo
  }

  cvTexts.push({
    fileName: file.originalname,
    text: text,
  });
}
```

> [!NOTE]
> La librería `pdf-parse` trabaja directamente con el `Buffer` en memoria. No hace falta escribir nada al disco.

---

## 7. Paso 3 — Construcción del prompt para la IA

Esta es la parte más importante. La IA recibe **dos prompts**:

### System Prompt (rol e instrucciones fijas)

Define el comportamiento del modelo. Lo lee en cada llamada pero nunca cambia:

```js
// src/services/cv-analyzer.js
const SYSTEM_PROMPT = `Sos un sistema de filtrado ATS (Applicant Tracking System) automatizado.
Tu funcion es evaluar CVs de candidatos y determinar cual es el mejor para un puesto especifico.

Reglas de evaluacion:
1. Analiza el contenido COMPLETO de cada CV, incluyendo TODO el texto presente.
2. Evalua la relevancia de las habilidades, experiencia y formacion para el puesto solicitado.
3. Asigna un puntaje de 0 a 100 a cada CV basandote en la coincidencia con los requisitos.
4. Ordena los CVs de mayor a menor puntaje.
5. Para cada CV, proporciona una justificacion breve de la puntuacion asignada.

IMPORTANTE: Tu analisis se basa unicamente en el TEXTO que recibes. Evaluas las keywords,
habilidades mencionadas, experiencia y formacion que aparecen en el texto del CV.

Responde SIEMPRE con el siguiente formato JSON (sin markdown, sin backticks, solo JSON puro):
{
  "ranking": [
    {
      "cvNumber": 1,
      "candidateName": "Nombre del candidato si aparece",
      "score": 95,
      "justification": "Justificacion del puntaje",
      "keySkillsFound": ["skill1", "skill2"],
      "experienceYears": "X anos de experiencia relevante",
      "strengths": ["fortaleza1", "fortaleza2"],
      "weaknesses": ["debilidad1", "debilidad2"]
    }
  ],
  "bestCandidate": {
    "cvNumber": 1,
    "summary": "Resumen de por que este candidato es el mejor para el puesto"
  }
}`;
```

### User Prompt (datos dinámicos de cada análisis)

Se construye con los datos del formulario + el texto extraído de los PDFs:

```js
// src/services/cv-analyzer.js
function buildUserPrompt(jobPosition, requirements, cvTexts) {
  let prompt = `Puesto a cubrir: ${jobPosition}\n\n`;

  if (requirements && requirements.trim().length > 0) {
    prompt += `Requisitos del reclutador: ${requirements}\n\n`;
  }

  prompt += "A continuacion los CVs a evaluar:\n\n";

  cvTexts.forEach((cvText, index) => {
    prompt += `=== CV ${index + 1} ===\n${cvText}\n\n`;
  });

  prompt += "Por favor, evalua cada CV segun las reglas establecidas y determina el mejor candidato para el puesto.";

  return prompt;
}
```

Un prompt de ejemplo para 2 CVs se vería así:

```
Puesto a cubrir: Desarrollador Backend Senior

Requisitos del reclutador: Mínimo 5 años de experiencia, Node.js, bases de datos SQL

A continuacion los CVs a evaluar:

=== CV 1 ===
Juan Pérez
Desarrollador con 7 años de experiencia en Node.js y PostgreSQL...

=== CV 2 ===
María García
Desarrolladora Full Stack con 3 años en React y MongoDB...

Por favor, evalua cada CV segun las reglas establecidas y determina el mejor candidato para el puesto.
```

---

## 8. Paso 4 — Llamada a la API de Groq

`groq-client.js` es el único módulo que habla directamente con Groq. Usa **streaming** para recibir la respuesta por chunks y luego la ensambla en un string completo:

```js
// src/services/groq-client.js
const Groq = require("groq-sdk");
const { getConfig } = require("../config/environment");
const { GroqApiError, ConfigurationError } = require("../errors/app-errors");

function createGroqClient() {
  const config = getConfig();

  if (!config.groq.apiKey || config.groq.apiKey.trim() === "") {
    throw new ConfigurationError(
      "La variable de entorno GROQ_API_KEY no esta configurada."
    );
  }

  return new Groq({ apiKey: config.groq.apiKey });
}

async function getCompletion(systemPrompt, userPrompt) {
  const config = getConfig();
  const client = createGroqClient();

  // Llama a la API con streaming habilitado
  const stream = await client.chat.completions.create({
    model: config.groq.model,          // "llama-3.3-70b-versatile"
    messages: [
      { role: "system", content: systemPrompt },  // ← instrucciones del ATS
      { role: "user", content: userPrompt },       // ← CVs + puesto
    ],
    temperature: config.groq.temperature,   // 0.3 (respuestas más deterministas)
    max_completion_tokens: config.groq.maxTokens,  // 4000
    top_p: 1,
    stream: true,    // ← recibe la respuesta por chunks
    stop: null,
  });

  // Ensambla todos los chunks en un string completo
  let fullResponse = "";

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || "";
    fullResponse += content;
  }

  if (!fullResponse || fullResponse.trim().length === 0) {
    throw new GroqApiError("La API de Groq no retorno ninguna respuesta.");
  }

  return fullResponse;  // String con el JSON generado por la IA
}
```

### Parámetros clave del modelo

| Parámetro | Valor por defecto | Descripción |
|---|---|---|
| `model` | `llama-3.3-70b-versatile` | Modelo LLM usado |
| `temperature` | `0.3` | Temperatura baja = respuestas más consistentes |
| `max_completion_tokens` | `4000` | Máximo de tokens en la respuesta |
| `top_p` | `1` | Sin filtrado nucleus (usa todos los tokens) |
| `stream` | `true` | Respuesta por chunks para no bloquear |

---

## 9. Paso 5 — Parseo y respuesta al cliente

La IA a veces envuelve el JSON en bloques de markdown (` ```json ... ``` `). `cv-analyzer.js` los limpia antes de parsear:

```js
// src/services/cv-analyzer.js
async function analyzeCvs(jobPosition, requirements, cvTexts) {
  const userPrompt = buildUserPrompt(jobPosition, requirements, cvTexts);
  const rawResponse = await getCompletion(SYSTEM_PROMPT, userPrompt);

  try {
    let cleanedResponse = rawResponse.trim();

    // Remueve bloques de markdown si la IA los incluyó
    if (cleanedResponse.startsWith("```")) {
      cleanedResponse = cleanedResponse
        .replace(/^```(?:json)?\s*\n?/, "")
        .replace(/\n?```\s*$/, "");
    }

    const parsedResult = JSON.parse(cleanedResponse);

    if (!parsedResult.ranking || !Array.isArray(parsedResult.ranking)) {
      throw new Error("La respuesta no contiene un ranking valido.");
    }

    return parsedResult;

  } catch (parseError) {
    // Fallback: devuelve la respuesta cruda si no se puede parsear
    return {
      ranking: [],
      rawResponse: rawResponse,
      parseError: "La IA no retorno un JSON valido. Se muestra la respuesta sin procesar.",
    };
  }
}
```

Por último, el controlador enriquece el resultado vinculando cada entrada del ranking con el nombre del archivo original:

```js
// src/controllers/ats-controller.js (fragmento)
const enrichedResult = {
  ...result,                          // ranking + bestCandidate de la IA
  cvSources: cvTexts.map((cv, index) => ({
    cvNumber: index + 1,
    fileName: cv.fileName,            // nombre original del archivo
    textLength: cv.text.length,       // cuántos caracteres tuvo el texto
  })),
};

res.json(enrichedResult);
```

---

## 10. Manejo de errores

Todas las clases de error extienden `AppError` y tienen un código HTTP asociado:

```js
// src/errors/app-errors.js
class AppError extends Error {
  constructor(message, code, statusCode = 500) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
  }
}

class ValidationError extends AppError {
  constructor(message) {
    super(message, "VALIDATION_ERROR", 400);  // Bad Request
  }
}

class GroqApiError extends AppError {
  constructor(message) {
    super(message, "GROQ_API_ERROR", 502);    // Bad Gateway
  }
}

class FileParseError extends AppError {
  constructor(message) {
    super(message, "FILE_PARSE_ERROR", 422);  // Unprocessable Entity
  }
}

class ConfigurationError extends AppError {
  constructor(message) {
    super(message, "CONFIGURATION_ERROR", 500);
  }
}
```

El middleware `error-handler.js` captura todos estos errores y los formatea de manera uniforme:

```js
// src/middleware/error-handler.js
function errorHandler(err, req, res, next) {
  if (err.code === "LIMIT_FILE_SIZE") {
    return res.status(400).json({
      error: { code: "FILE_TOO_LARGE", message: "El archivo excede 5 MB." }
    });
  }

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message }
    });
  }

  // Errores no controlados: nunca exponer el stack trace
  console.error("Error no controlado:", err);
  return res.status(500).json({
    error: { code: "INTERNAL_ERROR", message: "Error interno del servidor." }
  });
}
```

Tabla de errores posibles:

| Código HTTP | Code | Causa |
|---|---|---|
| `400` | `VALIDATION_ERROR` | Falta el puesto, no se subieron archivos |
| `400` | `FILE_TOO_LARGE` | Archivo supera 5 MB |
| `400` | `TOO_MANY_FILES` | Más de 10 archivos |
| `400` | `VALIDATION_ERROR` | Tipo de archivo no permitido |
| `422` | `FILE_PARSE_ERROR` | PDF escaneado, protegido o corrupto |
| `500` | `CONFIGURATION_ERROR` | Falta `GROQ_API_KEY` en `.env` |
| `500` | `INTERNAL_ERROR` | Error inesperado del servidor |
| `502` | `GROQ_API_ERROR` | Error en la API de Groq (401, 429, etc.) |

---

## 11. Endpoints disponibles

### `GET /api/health`
Verifica que el servidor esté corriendo.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-03-27T01:00:00.000Z"
}
```

---

### `POST /api/analyze`
Analiza uno o varios CVs contra un puesto con IA.

**Content-Type:** `multipart/form-data`

**Body:**

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| `cvFiles` | `File[]` | ✅ Sí | Uno o más archivos PDF o TXT (máx. 10, 5 MB cada uno) |
| `jobPosition` | `string` | ✅ Sí | Nombre del puesto a cubrir |
| `requirements` | `string` | ❌ No | Requisitos adicionales del reclutador |

**Ejemplo con `curl`:**
```bash
curl -X POST http://localhost:3000/api/analyze \
  -F "jobPosition=Desarrollador Backend Senior" \
  -F "requirements=Node.js, PostgreSQL, 5 años de experiencia" \
  -F "cvFiles=@cv-juan.pdf" \
  -F "cvFiles=@cv-maria.pdf"
```

**Ejemplo con `fetch` en JavaScript:**
```js
const formData = new FormData();
formData.append("jobPosition", "Desarrollador Backend Senior");
formData.append("requirements", "Node.js, PostgreSQL, 5 años de experiencia");
// Agregar archivos desde un <input type="file">
for (const file of fileInput.files) {
  formData.append("cvFiles", file);
}

const response = await fetch("/api/analyze", {
  method: "POST",
  body: formData,
});

const result = await response.json();
```

---

## 12. Ejemplo de respuesta completa

```json
{
  "ranking": [
    {
      "cvNumber": 1,
      "candidateName": "Juan Pérez",
      "score": 88,
      "justification": "Cuenta con 7 años de experiencia en Node.js y PostgreSQL, cumpliendo ampliamente los requisitos del puesto.",
      "keySkillsFound": ["Node.js", "PostgreSQL", "REST APIs", "Docker"],
      "experienceYears": "7 años de experiencia relevante",
      "strengths": ["Experiencia sólida en backend", "Conocimiento de bases de datos relacionales"],
      "weaknesses": ["Sin experiencia en microservicios", "No menciona testing automatizado"]
    },
    {
      "cvNumber": 2,
      "candidateName": "María García",
      "score": 52,
      "justification": "Solo 3 años de experiencia y perfil principalmente frontend. Conocimientos de backend limitados.",
      "keySkillsFound": ["React", "Node.js", "MongoDB"],
      "experienceYears": "3 años de experiencia general",
      "strengths": ["Conocimiento de Node.js", "Perfil full stack"],
      "weaknesses": ["Por debajo del requerimiento de 5 años", "Sin experiencia en SQL"]
    }
  ],
  "bestCandidate": {
    "cvNumber": 1,
    "summary": "Juan Pérez es el candidato más adecuado. Supera los 5 años requeridos de experiencia y domina las tecnologías clave del puesto."
  },
  "cvSources": [
    { "cvNumber": 1, "fileName": "cv-juan.pdf", "textLength": 3420 },
    { "cvNumber": 2, "fileName": "cv-maria.pdf", "textLength": 2810 }
  ]
}
```

---

> [!TIP]
> Para cambiar el modelo de IA, modificar `GROQ_MODEL` en el `.env`. Modelos disponibles en Groq: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, entre otros.

> [!NOTE]
> El campo `cvSources` es agregado por el servidor (no por la IA) para poder vincular el número de CV del ranking con el nombre real del archivo subido.
