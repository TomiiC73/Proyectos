#!/usr/bin/env node
'use strict';

// Actualiza el workflow en n8n vía API, fusionando por NOMBRE de nodo con lo que ya
// esta guardado en el servidor. Esto preserva las credenciales ya cargadas a mano
// (Telegram, Trello, SMTP, Sheets) y el id interno que n8n le asigno a cada nodo,
// en vez de pisarlas con el archivo local (que nunca tiene esos datos).

const path = require('path');
const { loadEnv } = require('./lib/env');
const { n8nFetch } = require('./lib/n8nClient');

loadEnv();

async function main() {
  const workflowId = process.env.N8N_WORKFLOW_ID;
  if (!workflowId) throw new Error('Falta N8N_WORKFLOW_ID en .env');

  const local = require(path.join(__dirname, '..', 'cierre_rampa_workflow.json'));

  console.log(`Leyendo workflow actual (${workflowId}) desde n8n...`);
  const remote = await n8nFetch(`/workflows/${workflowId}`);

  const remoteByName = new Map(remote.nodes.map((n) => [n.name, n]));

  let preservados = 0;
  let nuevos = 0;

  const nodesFusionados = local.nodes.map((nodoLocal) => {
    const nodoRemoto = remoteByName.get(nodoLocal.name);
    if (!nodoRemoto) {
      nuevos += 1;
      return nodoLocal;
    }
    preservados += 1;
    const fusionado = { ...nodoLocal, id: nodoRemoto.id };
    if (nodoRemoto.credentials) fusionado.credentials = nodoRemoto.credentials;

    // El nodo de Configuracion tiene campos que el usuario edita a mano en el
    // editor (API keys reales). Si no se preservan, cada push los pisa con los
    // placeholders del archivo local y rompe los nodos HTTP que las usan.
    if (
      nodoLocal.name === 'Configuracion (Editar Aca)' &&
      nodoRemoto.parameters &&
      nodoRemoto.parameters.assignments &&
      nodoLocal.parameters.assignments
    ) {
      const valoresRemotos = new Map(
        nodoRemoto.parameters.assignments.assignments.map((a) => [a.name, a.value]),
      );
      fusionado.parameters = {
        ...nodoLocal.parameters,
        assignments: {
          ...nodoLocal.parameters.assignments,
          assignments: nodoLocal.parameters.assignments.assignments.map((a) => ({
            ...a,
            value: valoresRemotos.has(a.name) ? valoresRemotos.get(a.name) : a.value,
          })),
        },
      };
    }

    return fusionado;
  });

  console.log(`Nodos existentes preservados (id + credenciales): ${preservados}`);
  console.log(`Nodos nuevos a crear: ${nuevos}`);

  const payloadBase = {
    name: remote.name,
    nodes: nodesFusionados,
    connections: local.connections,
    settings: local.settings,
  };

  try {
    await n8nFetch(`/workflows/${workflowId}`, {
      method: 'PUT',
      body: JSON.stringify({ ...payloadBase, pinData: local.pinData }),
    });
    console.log('Workflow actualizado (nodos, conexiones y mock pineado).');
  } catch (e) {
    // Algunas versiones de la API no aceptan pinData en el PATCH; reintenta sin eso.
    console.log(`pinData rechazado por la API (${e.message}), reintentando sin el mock...`);
    await n8nFetch(`/workflows/${workflowId}`, {
      method: 'PUT',
      body: JSON.stringify(payloadBase),
    });
    console.log('Workflow actualizado (sin mock pineado — pinealo a mano en el editor si hace falta).');
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
