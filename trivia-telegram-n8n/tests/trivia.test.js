'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const {
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
} = require('../logica/trivia');

test('interpretarMensaje: /unirme dispara accion "unirse"', () => {
  const r = interpretarMensaje({ text: '/unirme', from: { first_name: 'Ana' }, chat: { id: 111 } });
  assert.equal(r.accion, 'unirse');
  assert.equal(r.nombre, 'Ana');
  assert.equal(r.chat_id, 111);
});

test('interpretarMensaje: /start también dispara "unirse"', () => {
  const r = interpretarMensaje({ text: '/start', from: { username: 'ana_dev' }, chat: { id: 222 } });
  assert.equal(r.accion, 'unirse');
  assert.equal(r.nombre, 'ana_dev');
});

test('interpretarMensaje: /reiniciar en el bot de jugadores se ignora (no cuenta como respuesta)', () => {
  const r = interpretarMensaje({ text: '/reiniciar', from: { id: 5 }, chat: { id: 333 } });
  assert.equal(r.accion, '');
  assert.equal(r.respuesta, '');
});

test('interpretarMensaje: sin from cae en "Anonimo"', () => {
  const r = interpretarMensaje({ text: 'B', chat: { id: 444 } });
  assert.equal(r.nombre, 'Anonimo');
  assert.equal(r.accion, '');
  assert.equal(r.respuesta, 'B');
});

test('interpretarComandoAdmin: reconoce /iniciar, /comenzar, /detener, /reiniciar y /resetear', () => {
  assert.equal(interpretarComandoAdmin({ text: '/iniciar', chat: { id: 1 } }).accion, 'iniciar');
  assert.equal(interpretarComandoAdmin({ text: '/comenzar', chat: { id: 1 } }).accion, 'comenzar');
  assert.equal(interpretarComandoAdmin({ text: '/detener', chat: { id: 1 } }).accion, 'detener');
  assert.equal(interpretarComandoAdmin({ text: '/reiniciar', chat: { id: 1 } }).accion, 'reiniciar');
  assert.equal(interpretarComandoAdmin({ text: '/resetear', chat: { id: 1 } }).accion, 'resetear');
});

test('interpretarComandoAdmin: comando no reconocido cae en "desconocido"', () => {
  assert.equal(interpretarComandoAdmin({ text: '/ayuda', chat: { id: 1 } }).accion, 'desconocido');
});

test('el juego arranca en fase "inactivo" por defecto', () => {
  const data = crearEstadoGlobal();
  assert.equal(cargarEstado(data, 'Ana', 111).fase, 'inactivo');
});

test('unirse mientras está inactivo: pide esperar al organizador', () => {
  assert.match(mensajeJuegoNoActivo('unirse'), /organizador/);
});

test('/iniciar abre el lobby (fase "lobby") sin repartir la primera pregunta', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);

  const estado = cargarEstado(data, 'Ana', 111);
  assert.equal(estado.fase, 'lobby');
  assert.match(mensajeEnLobby('unirse'), /organizador mande \/comenzar/);
});

test('unirse durante el lobby: queda anotado, pero no avanza de etapa 0', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  cargarEstado(data, 'Beto', 222);

  assert.deepEqual(Object.keys(data.participantes).sort(), ['Ana', 'Beto']);
  assert.equal(data.participantes.Ana.etapa, 0);
  assert.equal(data.fase, 'lobby'); // /unirme no cambia la fase
});

test('/comenzar manda la pregunta 1 a todos los anotados en el lobby y pasa a fase "jugando"', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  cargarEstado(data, 'Beto', 222);

  const { mensajesJugadores, confirmacion } = comenzarJuego(data, 999);

  assert.equal(data.fase, 'jugando');
  assert.equal(mensajesJugadores.length, 2);
  const chatIds = mensajesJugadores.map((m) => m.chat_id).sort();
  assert.deepEqual(chatIds, [111, 222]);
  assert.match(mensajesJugadores[0].mensaje, /Pregunta 1\/5/);
  assert.match(mensajesJugadores[0].mensaje, new RegExp(PREGUNTAS[0].texto.replace(/[?]/g, '\\?')));
  assert.match(confirmacion.mensaje_participante, /2 jugador/);
});

test('/comenzar sin nadie anotado no rompe: devuelve 0 mensajes de jugadores', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);

  const { mensajesJugadores, confirmacion } = comenzarJuego(data, 999);

  assert.equal(mensajesJugadores.length, 0);
  assert.match(confirmacion.mensaje_participante, /0 jugador/);
});

test('responder correcto una vez que el juego está "jugando": suma punto y avanza', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);

  const r = evaluarYAvanzar(data, 'Ana', 'A', 111); // PREGUNTAS[0].correcta === 'A'

  assert.equal(r.correcta, true);
  assert.equal(r.puntaje_actual, 1);
  assert.equal(r.etapa_actual, 1);
  assert.equal(r.completado, false);
  assert.deepEqual(r.pregunta_siguiente, PREGUNTAS[1]);
});

test('cada respuesta lleva el chat_id del admin que abrió el lobby, para notificarle directo a él', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999); // 999 = chat del admin
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);

  const r = evaluarYAvanzar(data, 'Ana', 'A', 111);

  assert.equal(r.chat_id_admin, 999);
});

test('responder correcto con el texto completo de la opción (no solo la letra)', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);

  const r = evaluarYAvanzar(data, 'Ana', 'application programming interface', 111);

  assert.equal(r.correcta, true);
  assert.equal(r.puntaje_actual, 1);
});

test('responder incorrecto: no suma punto pero igual avanza (sin reintento)', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);

  const r = evaluarYAvanzar(data, 'Ana', 'B', 111); // la correcta era 'A'

  assert.equal(r.correcta, false);
  assert.equal(r.puntaje_actual, 0);
  assert.equal(r.etapa_actual, 1);
  assert.equal(r.completado, false);
});

test('completar las 5 preguntas: queda completado con el puntaje final', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);

  let ultimo;
  for (const pregunta of PREGUNTAS) {
    ultimo = evaluarYAvanzar(data, 'Ana', pregunta.correcta, 111);
  }

  assert.equal(ultimo.completado, true);
  assert.equal(ultimo.etapa_actual, 5);
  assert.equal(ultimo.puntaje_actual, 5);
  assert.equal(ultimo.pregunta_siguiente, null);
});

test('/detener vuelve todo a "inactivo" (hace falta /iniciar de nuevo)', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);

  detenerJuego(data, 999);

  assert.equal(cargarEstado(data, 'Beto', 222).fase, 'inactivo');
});

test('reiniciar (admin): borra el progreso de todos sin tocar la fase actual', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);
  evaluarYAvanzar(data, 'Ana', 'A', 111);
  cargarEstado(data, 'Beto', 222);
  evaluarYAvanzar(data, 'Beto', 'A', 222);

  reiniciarJuego(data);

  assert.deepEqual(data.participantes, {});
  assert.equal(data.fase, 'jugando'); // reiniciar no pausa el juego

  const estado = cargarEstado(data, 'Ana', 111);
  assert.equal(estado.etapa_actual, 0);
  assert.equal(estado.puntaje_actual, 0);
});

test('dos participantes juegan en paralelo sin pisarse el progreso', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  cargarEstado(data, 'Beto', 222);
  comenzarJuego(data, 999);

  evaluarYAvanzar(data, 'Ana', 'A', 111); // correcto
  evaluarYAvanzar(data, 'Beto', 'Z', 222); // incorrecto

  assert.equal(data.participantes.Ana.puntaje, 1);
  assert.equal(data.participantes.Beto.puntaje, 0);
  assert.equal(data.participantes.Ana.etapa, 1);
  assert.equal(data.participantes.Beto.etapa, 1);
});

test('/resetear borra todos los participantes, pausa el juego y olvida al admin actual', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  comenzarJuego(data, 999);
  evaluarYAvanzar(data, 'Ana', 'A', 111);

  resetearTodo(data, 999);

  assert.deepEqual(data.participantes, {});
  assert.equal(data.fase, 'inactivo');
  assert.equal(data.adminChatId, null);
});

test('todos_completaron es false mientras falte algún jugador por terminar', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  cargarEstado(data, 'Beto', 222);
  comenzarJuego(data, 999);

  let ultimoDeAna;
  for (const pregunta of PREGUNTAS) {
    ultimoDeAna = evaluarYAvanzar(data, 'Ana', pregunta.correcta, 111);
  }

  assert.equal(ultimoDeAna.completado, true);
  assert.equal(ultimoDeAna.todos_completaron, false); // Beto todavía no terminó
});

test('todos_completaron es true recién cuando el último jugador termina, y arma la tabla de posiciones', () => {
  const data = crearEstadoGlobal();
  iniciarJuego(data, 999);
  cargarEstado(data, 'Ana', 111);
  cargarEstado(data, 'Beto', 222);
  comenzarJuego(data, 999);

  for (const pregunta of PREGUNTAS) evaluarYAvanzar(data, 'Ana', pregunta.correcta, 111); // Ana: 5/5

  let ultimoDeBeto;
  for (const pregunta of PREGUNTAS) {
    ultimoDeBeto = evaluarYAvanzar(data, 'Beto', 'Z', 222); // Beto: 0/5 (todo mal)
  }

  assert.equal(ultimoDeBeto.todos_completaron, true); // Beto fue el último en terminar

  const tabla = armarTablaClasificacion(data);
  assert.equal(tabla.ranking[0].nombre, 'Ana');
  assert.equal(tabla.ranking[0].puntaje, 5);
  assert.equal(tabla.ranking[1].nombre, 'Beto');
  assert.equal(tabla.ranking[1].puntaje, 0);
  assert.match(tabla.mensaje_telegram, /🏆/);
  assert.match(tabla.mensaje_telegram, /🥇 Ana - 5\/5/);
  assert.equal(tabla.chat_id_admin, 999);
});
