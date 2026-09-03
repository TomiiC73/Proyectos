#!/usr/bin/env node
'use strict';

const { loadEnv } = require('./lib/env');
const { n8nFetch } = require('./lib/n8nClient');
const { leerWorkflowId } = require('./lib/workflowId');

loadEnv();

async function verificarWebhook(nombre, token, host) {
  console.log(`Consultando getWebhookInfo del bot ${nombre}...`);
  const res = await fetch(`https://api.telegram.org/bot${token}/getWebhookInfo`);
  const info = await res.json();
  if (!info.ok) {
    throw new Error(`Telegram getWebhookInfo (${nombre}) falló: ${JSON.stringify(info)}`);
  }

  const url = info.result.url || '';
  console.log(`  Webhook del bot ${nombre}: ${url || '(vacío)'}`);
  if (host && url.includes(host)) {
    console.log(`  ✅ Apunta a tu instancia de n8n Cloud (${host}).`);
    return true;
  }
  console.warn(`  ⚠️  El webhook del bot ${nombre} NO parece apuntar a tu instancia de n8n Cloud.`);
  return false;
}

async function main() {
  const tokenJugadores = process.env.TELEGRAM_BOT_TOKEN_JUGADORES;
  const tokenAdmin = process.env.TELEGRAM_BOT_TOKEN_ADMIN;
  if (!tokenJugadores) throw new Error('Falta TELEGRAM_BOT_TOKEN_JUGADORES en .env');
  if (!tokenAdmin) throw new Error('Falta TELEGRAM_BOT_TOKEN_ADMIN en .env');

  const workflowId = leerWorkflowId();

  console.log('Activando el workflow (POST /workflows/{id}/activate)...');
  await n8nFetch(`/workflows/${workflowId}/activate`, { method: 'POST' });
  console.log('Workflow activado. n8n Cloud debería haber registrado los 2 webhooks en Telegram automáticamente.');

  let host = null;
  try {
    host = new URL(process.env.N8N_CLOUD_URL).host;
  } catch {
    // N8N_CLOUD_URL mal formada; ya habría fallado antes en n8nClient.
  }

  const okJugadores = await verificarWebhook('jugadores', tokenJugadores, host);
  const okAdmin = await verificarWebhook('admin', tokenAdmin, host);

  if (okJugadores && okAdmin) {
    console.log('\n✅ Todo listo. Mandale /iniciar al bot admin y después /unirme al bot de jugadores.');
  } else {
    console.warn(
      '\n⚠️  Al menos un webhook no quedó bien registrado. Revisá que el workflow esté activo en el editor ' +
        'y volvé a correr este script.'
    );
  }
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});
