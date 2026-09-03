#!/usr/bin/env node
'use strict';

const { loadEnv } = require('./lib/env');
const { n8nFetch } = require('./lib/n8nClient');
const { leerWorkflowId } = require('./lib/workflowId');

loadEnv();

async function main() {
  const workflowId = leerWorkflowId();
  console.log(`Desactivando el workflow ${workflowId} (POST /workflows/{id}/deactivate)...`);
  await n8nFetch(`/workflows/${workflowId}/deactivate`, { method: 'POST' });
  console.log('✅ Workflow desactivado. Telegram va a dejar de mandarle updates a n8n.');
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});
