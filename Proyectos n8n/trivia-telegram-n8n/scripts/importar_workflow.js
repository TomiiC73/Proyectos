#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { loadEnv } = require('./lib/env');
const { n8nFetch } = require('./lib/n8nClient');
const { guardarWorkflowId } = require('./lib/workflowId');

loadEnv();

const WORKFLOW_JSON_PATH = path.join(__dirname, '..', 'trivia_telegram.json');

async function main() {
  const raw = JSON.parse(fs.readFileSync(WORKFLOW_JSON_PATH, 'utf8'));

  const workflowIdExistente = process.env.N8N_WORKFLOW_ID;
  let nodesParaEnviar = raw.nodes;

  if (workflowIdExistente) {
    // El archivo local nunca tiene `credentials` (no se commitean). Si mandamos
    // raw.nodes tal cual, el PATCH pisa las credenciales de Telegram ya asignadas
    // en n8n Cloud y rompe los 2 bots. Por eso primero traemos el workflow remoto
    // y fusionamos por nombre de nodo, igual que hace subir_workflow.js en el
    // proyecto de aeropuertos.
    console.log(`Leyendo workflow actual (${workflowIdExistente}) desde n8n Cloud...`);
    const remoto = await n8nFetch(`/workflows/${workflowIdExistente}`);
    const remotoPorNombre = new Map(remoto.nodes.map((n) => [n.name, n]));

    let preservados = 0;
    let nuevos = 0;
    nodesParaEnviar = raw.nodes.map((nodoLocal) => {
      const nodoRemoto = remotoPorNombre.get(nodoLocal.name);
      if (!nodoRemoto) {
        nuevos += 1;
        return nodoLocal;
      }
      preservados += 1;
      const fusionado = { ...nodoLocal, id: nodoRemoto.id };
      if (nodoRemoto.credentials) fusionado.credentials = nodoRemoto.credentials;
      return fusionado;
    });
    console.log(`Nodos existentes preservados (id + credenciales): ${preservados}`);
    console.log(`Nodos nuevos a crear: ${nuevos}`);
  }

  // n8n Cloud rechaza propiedades de solo lectura (id, active, tags, versionId, pinData)
  // en el body, así que mandamos solo lo que la API espera tanto para crear como para actualizar.
  const payload = {
    name: raw.name,
    nodes: nodesParaEnviar,
    connections: raw.connections,
    settings: raw.settings || {},
  };

  let workflowId;

  if (workflowIdExistente) {
    console.log(
      `Actualizando el workflow existente ${workflowIdExistente} en ${process.env.N8N_CLOUD_URL} ` +
        `(PATCH /workflows/${workflowIdExistente}) con el contenido de trivia_telegram.json...`
    );
    const actualizado = await n8nFetch(`/workflows/${workflowIdExistente}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    });
    workflowId = actualizado.id;
  } else {
    console.log(`Creando un workflow nuevo "${payload.name}" en ${process.env.N8N_CLOUD_URL} ...`);
    const creado = await n8nFetch('/workflows', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    workflowId = creado.id;
  }

  guardarWorkflowId(workflowId);
  console.log(`Workflow id ${workflowId} guardado en .n8n_workflow_id`);

  console.log('Verificando con GET /workflows...');
  const lista = await n8nFetch('/workflows');
  const items = Array.isArray(lista) ? lista : lista.data || [];
  const encontrado = items.find((wf) => wf.id === workflowId);

  if (!encontrado) {
    throw new Error('El workflow no aparece en GET /workflows justo después de crearlo/actualizarlo.');
  }
  if (encontrado.name !== payload.name) {
    throw new Error(`El nombre no coincide: esperado "${payload.name}", encontrado "${encontrado.name}"`);
  }

  console.log(`✅ Verificado: "${encontrado.name}" (id ${encontrado.id}) está en tu cuenta de n8n Cloud.`);
  console.log('Siguiente paso: npm run setup:credencial');
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});
