const express = require("express");
const cors = require("cors");
const path = require("path");
const { validateEnvironment, getConfig } = require("./src/config/environment");
const atsController     = require("./src/controllers/ats-controller");
const gmailController   = require("./src/controllers/gmail-controller");
const inboxController   = require("./src/controllers/inbox-controller");
const imapService       = require("./src/services/imap-service");
const { errorHandler }  = require("./src/middleware/error-handler");

// Validar que las variables de entorno obligatorias esten presentes
try {
  validateEnvironment();
} catch (error) {
  console.warn(
    `[ADVERTENCIA] ${error.message}\n` +
      "La API key puede proporcionarse desde la interfaz web."
  );
}

const config = getConfig();
const app = express();

// Middleware global
app.use(cors());
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));

// Archivos estaticos del frontend
app.use(express.static(path.join(__dirname, "public")));

// Rutas de la API
app.use("/api", atsController);
app.use("/api", gmailController);
app.use("/api", inboxController);

// Middleware de errores (debe ir al final)
app.use(errorHandler);

// Iniciar servidor
app.listen(config.server.port, () => {
  console.log(
    `[Laboratorio ATS] Servidor iniciado en http://localhost:${config.server.port}`
  );
  console.log(
    `[Laboratorio ATS] Modelo configurado: ${config.groq.model}`
  );

  // Arrancar polling IMAP si está configurado
  if (config.gmail.imapUser && config.gmail.imapPass) {
    console.log(`[IMAP] Configurado para: ${config.gmail.imapUser}`);
    imapService.startPolling(config, 8000);
  } else {
    console.warn(
      "[IMAP] No configurado. Agregá GMAIL_IMAP_USER y GMAIL_IMAP_PASS al .env para recibir emails reales."
    );
  }
});
