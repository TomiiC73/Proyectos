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
    gmail: {
      imapUser: process.env.GMAIL_IMAP_USER || "",
      imapPass: process.env.GMAIL_IMAP_PASS || "",
    },
  };
}

module.exports = { validateEnvironment, getConfig };
