'use strict';

async function n8nFetch(pathname, options) {
  const baseUrl = process.env.N8N_CLOUD_URL;
  const apiKey = process.env.N8N_API_KEY;
  if (!baseUrl) throw new Error('Falta N8N_CLOUD_URL en .env');
  if (!apiKey) throw new Error('Falta N8N_API_KEY en .env');

  const res = await fetch(`${baseUrl}/api/v1${pathname}`, {
    ...options,
    headers: {
      'X-N8N-API-KEY': apiKey,
      'Content-Type': 'application/json',
      ...(options && options.headers),
    },
  });

  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch (e) {
    throw new Error(`Respuesta no-JSON de n8n (HTTP ${res.status}): ${text.slice(0, 300)}`);
  }

  if (!res.ok) {
    throw new Error(`n8n API ${pathname} -> HTTP ${res.status}: ${body.message || text.slice(0, 300)}`);
  }

  return body;
}

module.exports = { n8nFetch };
