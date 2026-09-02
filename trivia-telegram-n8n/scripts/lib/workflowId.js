'use strict';

const fs = require('fs');
const path = require('path');

// El id del workflow importado se guarda en un archivo local (gitignoreado)
// para que los scripts siguientes (credencial, activar, desactivar) no
// necesiten que lo pegues a mano en .env.
const ID_FILE = path.join(__dirname, '..', '..', '.n8n_workflow_id');

function guardarWorkflowId(id) {
  fs.writeFileSync(ID_FILE, String(id), 'utf8');
}

function leerWorkflowId() {
  if (process.env.N8N_WORKFLOW_ID) return process.env.N8N_WORKFLOW_ID;
  if (fs.existsSync(ID_FILE)) return fs.readFileSync(ID_FILE, 'utf8').trim();
  throw new Error(
    'No se encontró el workflow importado. Corré primero: npm run setup:import'
  );
}

module.exports = { guardarWorkflowId, leerWorkflowId };
