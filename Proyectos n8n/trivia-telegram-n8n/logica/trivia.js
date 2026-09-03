'use strict';

// Traducción 1:1 del JavaScript que corre dentro de los nodos Code del workflow
// (trivia_telegram.json), para poder testearlo sin n8n ni Telegram real.
// El workflow importado NO usa este módulo — cada nodo Code sigue llevando su
// propia copia del código, porque así es como corre dentro de n8n.
//
// Fases del juego (data.fase en $getWorkflowStaticData('global')):
//   'inactivo' (o undefined) -> nadie puede unirse ni responder.
//   'lobby'                  -> /iniciar; los jugadores se anotan con /unirme
//                                pero NO reciben la pregunta todavía.
//   'jugando'                -> /comenzar; todos los anotados reciben la
//                                pregunta 1 al mismo tiempo y ya pueden responder.

const PREGUNTAS = [
{ texto: "Cuando dos aplicaciones no intercambian información, ¿qué rol termina cumpliendo la persona?", opciones: { A: "Supervisora del área", B: "Intermediaria entre sistemas", C: "Auditora de calidad", D: "Responsable de backups" }, correcta: "B" },
{ texto: "Como criterio general, ¿qué conviene automatizar?", opciones: { A: "Todo, sin excepciones", B: "Solo tareas creativas", C: "Los casos normales, derivando los especiales", D: "Únicamente lo urgente" }, correcta: "C" },
{ texto: "En n8n, ¿qué representa cada nodo del workflow?", opciones: { A: "Un servidor físico", B: "Una operación", C: "Un usuario del sistema", D: "Un tipo de error" }, correcta: "B" },
{ texto: "¿Cuándo es más eficiente una organización?", opciones: { A: "Cuando gasta más para producir más", B: "Cuando logra el mismo resultado con menos recursos", C: "Cuando reduce la calidad", D: "Cuando contrata más gente" }, correcta: "B" },
{ texto: "¿Qué le permite hacer a n8n la información que guarda de cada ejecución?", opciones: { A: "Facturar a los clientes", B: "Rastrear qué pasó y dónde falló", C: "Generar backups", D: "Cambiar los permisos de usuario" }, correcta: "B" },
{ texto: "¿Qué significa la sigla RPA?", opciones: { A: "Remote Process Automation", B: "Rapid Process Application", C: "Robotic Process Automation", D: "Real-time Program Access" }, correcta: "C" },
{ texto: "¿La automatización elimina todos los errores posibles?", opciones: { A: "Sí, nunca falla", B: "No, un workflow también puede fallar", C: "Sí, usando IA", D: "No aplica a errores" }, correcta: "B" },
{ texto: "¿Qué hay que hacer antes de automatizar un proceso mal diseñado?", opciones: { A: "Automatizarlo igual", B: "Contratar más gente", C: "Entenderlo primero", D: "Nada, se corrige solo" }, correcta: "C" },
{ texto: "¿Qué tipo de decisiones puede tomar un robot RPA por sí solo?", opciones: { A: "Cualquier decisión compleja", B: "Decisiones simples basadas en condiciones definidas", C: "Ninguna decisión", D: "Solo decisiones financieras" }, correcta: "B" },
];

// Espejo de "Interpretar Mensaje" (bot de jugadores)
function interpretarMensaje(message) {
  const msg = message || {};
  const texto = (msg.text || '').trim();
  const nombre = msg.from ? (msg.from.first_name || msg.from.username || ('Jugador' + msg.from.id)) : 'Anonimo';
  const chatId = msg.chat ? msg.chat.id : null;

  let accion = '';
  let respuesta = '';
  const textoLower = texto.toLowerCase();

  if (textoLower.indexOf('/start') === 0 || textoLower.indexOf('/unirme') === 0) {
    accion = 'unirse';
  } else if (textoLower.indexOf('/') === 0) {
    accion = '';
    respuesta = '';
  } else {
    respuesta = texto;
  }

  return { nombre, accion, respuesta, chat_id: chatId };
}

// Espejo de "Interpretar Comando Admin" (bot del organizador)
function interpretarComandoAdmin(message) {
  const msg = message || {};
  const texto = (msg.text || '').trim();
  const nombre = msg.from ? (msg.from.first_name || msg.from.username || ('Organizador' + msg.from.id)) : 'Organizador';
  const chatId = msg.chat ? msg.chat.id : null;
  const textoLower = texto.toLowerCase();

  let accion = 'desconocido';
  if (textoLower.indexOf('/iniciar') === 0) accion = 'iniciar';
  else if (textoLower.indexOf('/comenzar') === 0) accion = 'comenzar';
  else if (textoLower.indexOf('/detener') === 0) accion = 'detener';
  else if (textoLower.indexOf('/reiniciar') === 0) accion = 'reiniciar';
  else if (textoLower.indexOf('/resetear') === 0) accion = 'resetear';

  return { nombre, accion, chat_id: chatId };
}

// data.fase empieza undefined (=> 'inactivo'): el juego arranca pausado.
function crearEstadoGlobal() {
  return { participantes: {} };
}

// Espejo de "Cargar Preguntas y Estado"
function cargarEstado(data, nombre, chatId) {
  data.participantes = data.participantes || {};

  if (!data.participantes[nombre]) {
    data.participantes[nombre] = { etapa: 0, puntaje: 0, historial: [], chatId };
  }
  data.participantes[nombre].chatId = chatId;

  const estado = data.participantes[nombre];
  const preguntaActual = estado.etapa < PREGUNTAS.length ? PREGUNTAS[estado.etapa] : null;

  return {
    nombre,
    fase: data.fase || 'inactivo',
    etapa_actual: estado.etapa,
    puntaje_actual: estado.puntaje,
    total_preguntas: PREGUNTAS.length,
    pregunta_actual: preguntaActual,
  };
}

// Espejo de "Juego No Activo" (fase 'inactivo')
function mensajeJuegoNoActivo(accion) {
  return accion === 'unirse'
    ? '⏳ Todavia no arranco el juego. Espera el aviso del organizador y volve a mandar /unirme.'
    : '⏳ El juego esta pausado en este momento. Espera a que el organizador lo reactive.';
}

// Espejo de "En Lobby" (fase 'lobby')
function mensajeEnLobby(accion) {
  return accion === 'unirse'
    ? '👋 ¡Te uniste! Espera a que el organizador mande /comenzar para arrancar.'
    : '⏳ Ya estas anotado. Espera a que el organizador mande /comenzar.';
}

// Espejo de "Iniciar Juego (Abrir Lobby)" — abre lobby, empieza de cero y
// recuerda de qué chat vino el admin, para poder notificarle ahí más adelante.
function iniciarJuego(data, chatId) {
  data.fase = 'lobby';
  data.participantes = {};
  data.adminChatId = chatId;
  return {
    chat_id: chatId,
    mensaje_participante: '✅ Lobby abierto. Los jugadores ya pueden mandar /unirme. Cuando estén todos los que van a jugar, mandá /comenzar.',
  };
}

function formatearPreguntaUno() {
  const primera = PREGUNTAS[0];
  return (
    'Pregunta 1/' + PREGUNTAS.length + ': ' + primera.texto +
    '\n\nA) ' + primera.opciones.A +
    '\nB) ' + primera.opciones.B +
    '\nC) ' + primera.opciones.C +
    '\nD) ' + primera.opciones.D +
    '\n\nRespondé con la letra (A, B, C o D).'
  );
}

// Espejo de "Enviar Pregunta 1 a Todos" + "Confirmar Inicio de Partida"
function comenzarJuego(data, chatIdAdmin) {
  data.fase = 'jugando';

  const textoPregunta = formatearPreguntaUno();
  const participantes = data.participantes || {};
  const nombres = Object.keys(participantes);

  const mensajesJugadores = nombres.map((nombre) => ({
    chat_id: participantes[nombre].chatId,
    mensaje: textoPregunta,
  }));

  const confirmacion = {
    chat_id: chatIdAdmin,
    mensaje_participante: `🚀 Juego iniciado con ${nombres.length} jugador(es). ¡Buena suerte para todos!`,
  };

  return { mensajesJugadores, confirmacion };
}

// Espejo de "Detener Juego" — corta todo, hace falta /iniciar de nuevo
function detenerJuego(data, chatId) {
  data.fase = 'inactivo';
  return {
    chat_id: chatId,
    mensaje_participante: '⏸️ Juego detenido. Mandá /iniciar para abrir un lobby nuevo cuando quieras retomar.',
  };
}

// Espejo de "Reiniciar Juego" — no toca data.fase, solo borra progreso
function reiniciarJuego(data) {
  data.participantes = {};
}

// Espejo de "Resetear Todo" — reset completo: borra participantes,
// vuelve a "inactivo" y olvida el admin actual (hace falta /iniciar de nuevo).
function resetearTodo(data, chatId) {
  data.fase = 'inactivo';
  data.participantes = {};
  data.adminChatId = null;
  return {
    chat_id: chatId,
    mensaje_participante: '🗑️ Se borraron todos los participantes. El juego volvió a estar inactivo. Mandá /iniciar para abrir un lobby nuevo.',
  };
}

// Espejo de "Evaluar y Avanzar"
function evaluarYAvanzar(data, nombre, respuestaCruda, chatId) {
  const estado = data.participantes[nombre];
  const yaHabiaTerminado = estado.etapa >= PREGUNTAS.length;
  const preguntaActual = yaHabiaTerminado ? null : PREGUNTAS[estado.etapa];

  let correcta = false;
  if (preguntaActual) {
    const respuestaNorm = (respuestaCruda || '').trim().toUpperCase();
    const letraCorrecta = preguntaActual.correcta;
    const textoCorrecta = preguntaActual.opciones[letraCorrecta].toUpperCase();
    correcta = respuestaNorm === letraCorrecta || respuestaNorm === textoCorrecta;

    estado.etapa += 1;
    if (correcta) estado.puntaje += 1;
    estado.historial.push({
      pregunta: preguntaActual.texto,
      respuesta_dada: respuestaCruda,
      correcta,
      hora: new Date().toISOString(),
    });
  }

  const completado = estado.etapa >= PREGUNTAS.length;
  const preguntaSiguiente = completado ? null : PREGUNTAS[estado.etapa];
  const todosCompletaron = completado && Object.values(data.participantes).every((p) => p.etapa >= PREGUNTAS.length);

  return {
    nombre,
    chat_id: chatId,
    respuesta: respuestaCruda,
    correcta,
    etapa_actual: estado.etapa,
    puntaje_actual: estado.puntaje,
    total_preguntas: PREGUNTAS.length,
    completado,
    pregunta_siguiente: preguntaSiguiente,
    chat_id_admin: data.adminChatId || null,
    todos_completaron: todosCompletaron,
  };
}

// Espejo de "Armar Tabla de Clasificación" — ranking final ordenado por puntaje.
function armarTablaClasificacion(data) {
  const participantes = data.participantes || {};

  const ranking = Object.keys(participantes)
    .map((nombre) => ({ nombre, puntaje: participantes[nombre].puntaje }))
    .sort((a, b) => b.puntaje - a.puntaje);

  const medallas = ['🥇', '🥈', '🥉'];
  const lineas = ranking.map((r, i) => {
    const prefijo = medallas[i] || `${i + 1}.`;
    return `${prefijo} ${r.nombre} - ${r.puntaje}/${PREGUNTAS.length} puntos`;
  });

  const tabla = '🏆 ¡Trivia terminada! Tabla de clasificación final:\n\n' + lineas.join('\n');

  return { chat_id_admin: data.adminChatId || null, mensaje_telegram: tabla, tabla_texto: tabla, ranking };
}

// Espejo de "Preparar Mensaje para el Jugador"
function prepararMensajeJugador(json) {
  return {
    chat_id: json.chat_id,
    mensaje: json.mensaje_participante || 'Listo.',
    tipo_evento: json.tipo_evento || null,
    correcta: json.correcta === undefined ? null : json.correcta,
    completado: !!json.completado,
  };
}

module.exports = {
  PREGUNTAS,
  interpretarMensaje,
  interpretarComandoAdmin,
  crearEstadoGlobal,
  cargarEstado,
  mensajeJuegoNoActivo,
  mensajeEnLobby,
  iniciarJuego,
  comenzarJuego,
  detenerJuego,
  reiniciarJuego,
  resetearTodo,
  evaluarYAvanzar,
  armarTablaClasificacion,
  prepararMensajeJugador,
};
