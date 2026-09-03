'use strict';

// Cliente mínimo para la REST API de n8n Cloud (/api/v1).
// Usa el fetch global de Node 18+, sin dependencias externas.

function baseUrl() {
  const raw = process.env.N8N_CLOUD_URL;
  if (!raw) throw new Error('Falta N8N_CLOUD_URL en .env (ej: https://tu-subdominio.app.n8n.cloud)');
  return raw.replace(/\/+$/, '');
}

function apiKey() {
  const key = process.env.N8N_API_KEY;
  if (!key) throw new Error('Falta N8N_API_KEY en .env (Settings → n8n API en tu instancia)');
  return key;
}

async function n8nFetch(path, options = {}) {
  const url = `${baseUrl()}/api/v1${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-N8N-API-KEY': apiKey(),
      ...(options.headers || {}),
    },
  });

  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = text;
  }

  if (!res.ok) {
    const detalle = typeof body === 'string' ? body : JSON.stringify(body);
    throw new Error(`n8n API ${options.method || 'GET'} ${path} -> HTTP ${res.status}: ${detalle}`);
  }

  return body;
}

module.exports = { n8nFetch };
