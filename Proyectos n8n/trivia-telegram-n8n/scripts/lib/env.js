'use strict';

const fs = require('fs');
const path = require('path');

// Loader mínimo de .env (sin dependencias externas): lee KEY=VALUE,
// ignora comentarios y líneas vacías, y no pisa variables ya seteadas
// en el entorno (para poder overridear con env reales en CI si hiciera falta).
function loadEnv() {
  const envPath = path.join(__dirname, '..', '..', '.env');
  if (!fs.existsSync(envPath)) return;

  const contenido = fs.readFileSync(envPath, 'utf8');
  for (const rawLine of contenido.split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;

    const eq = line.indexOf('=');
    if (eq === -1) continue;

    const key = line.slice(0, eq).trim();
    let value = line.slice(eq + 1).trim();
    const esComillasDobles = value.startsWith('"') && value.endsWith('"');
    const esComillasSimples = value.startsWith("'") && value.endsWith("'");
    if (esComillasDobles || esComillasSimples) {
      value = value.slice(1, -1);
    }

    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

module.exports = { loadEnv };
