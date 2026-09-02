#!/usr/bin/env node
'use strict';

const { loadEnv } = require('./lib/env');
const { n8nFetch } = require('./lib/n8nClient');
const { leerWorkflowId } = require('./lib/workflowId');

loadEnv();

// Dos bots distintos: el de jugadores y el del organizador (admin).
// Tienen que coincidir EXACTO con los "name" en trivia_telegram.json.
const NODOS_BOT_JUGADORES = ['Telegram Trigger - Recibir Mensaje', 'Responder al Jugador'];
const NODOS_BOT_ADMIN = ['Telegram Trigger - Admin', 'Notificar al Admin', 'Responder al Admin'];

async function crearCredencial(nombre, token) {
  console.log(`Creando credencial "${nombre}" en n8n Cloud...`);
  const credencial = await n8nFetch('/credentials', {
    method: 'POST',
    body: JSON.stringify({
      name: nombre,
      type: 'telegramApi',
      data: { accessToken: token },
    }),
  });
  console.log(`  -> id ${credencial.id}`);
  return credencial;
}

async function main() {
  const tokenJugadores = process.env.TELEGRAM_BOT_TOKEN_JUGADORES;
  const tokenAdmin = process.env.TELEGRAM_BOT_TOKEN_ADMIN;
  if (!tokenJugadores) throw new Error('Falta TELEGRAM_BOT_TOKEN_JUGADORES en .env');
  if (!tokenAdmin) throw new Error('Falta TELEGRAM_BOT_TOKEN_ADMIN en .env');

  const credencialJugadores = await crearCredencial('Telegram Trivia - Jugadores', tokenJugadores);
  const credencialAdmin = await crearCredencial('Telegram Trivia - Admin', tokenAdmin);

  const mapaCredenciales = new Map();
  for (const nombreNodo of NODOS_BOT_JUGADORES) mapaCredenciales.set(nombreNodo, credencialJugadores);
  for (const nombreNodo of NODOS_BOT_ADMIN) mapaCredenciales.set(nombreNodo, credencialAdmin);

  const workflowId = leerWorkflowId();
  const workflow = await n8nFetch(`/workflows/${workflowId}`);

  let asociados = 0;
  const nodes = workflow.nodes.map((node) => {
    const credencial = mapaCredenciales.get(node.name);
    if (!credencial) return node;
    asociados += 1;
    return {
      ...node,
      credentials: {
        ...(node.credentials || {}),
        telegramApi: { id: credencial.id, name: credencial.name },
      },
    };
  });

  const totalEsperado = NODOS_BOT_JUGADORES.length + NODOS_BOT_ADMIN.length;
  if (asociados !== totalEsperado) {
    throw new Error(
      `Se esperaban ${totalEsperado} nodos de Telegram y se encontraron ${asociados}. ` +
        'Revisá que los nombres de nodo en trivia_telegram.json no hayan cambiado.'
    );
  }

  console.log(`Asociando credenciales a ${asociados} nodos vía PATCH /workflows/${workflowId}...`);
  await n8nFetch(`/workflows/${workflowId}`, {
    method: 'PATCH',
    body: JSON.stringify({
      name: workflow.name,
      nodes,
      connections: workflow.connections,
      settings: workflow.settings,
    }),
  });

  console.log(`✅ Bot jugadores -> ${NODOS_BOT_JUGADORES.join(', ')}`);
  console.log(`✅ Bot admin -> ${NODOS_BOT_ADMIN.join(', ')}`);
  console.log('Siguiente paso: npm run setup:activar');
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  console.error(
    '\nSi la API de n8n Cloud rechazó crear o asociar alguna credencial "telegramApi" en tu versión,' +
      '\ncreála a mano: Settings → Credentials → New → Telegram, pegá el token correspondiente,' +
      '\ny asociala vos mismo a los nodos de ese bot abriendo cada uno en el editor.' +
      '\nDespués corré igual: npm run setup:activar'
  );
  process.exit(1);
});
