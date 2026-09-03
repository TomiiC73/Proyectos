// Nodo Code: "Evaluar Riesgo Meteorologico"
// Entrada esperada: el payload inyectado en el Manual Trigger (reporte_meteorologico + vuelos_programados)
// Salida: un unico item con el nivel de riesgo, la accion requerida y los vuelos afectados.

const UMBRAL_RAFAGA_CIERRE_KT = 45;
const UMBRAL_VIENTO_SOSTENIDO_ALERTA_KT = 30;
const UMBRAL_VISIBILIDAD_CIERRE_M = 1500;
const VENTANA_MINUTOS = 45;

const data = $json;
const clima = data.reporte_meteorologico;
const vuelos = data.vuelos_programados || [];

const hayTormentaElectrica = !!clima.actividad_electrica;
const hayWindshear = !!clima.windshear_reportado;
const rafagaKt = (clima.viento && clima.viento.rafaga_kt) || 0;
const vientoSostenidoKt = (clima.viento && clima.viento.velocidad_kt) || 0;
const visibilidadM = clima.visibilidad_m || 9999;

// Nivel 3: cierre total de rampa - condiciones que obligan a detener operaciones en plataforma
// (tormenta electrica activa + rafaga o windshear por encima de umbral operativo).
const condicionNivel3 =
  hayTormentaElectrica && (rafagaKt >= UMBRAL_RAFAGA_CIERRE_KT || hayWindshear);

// Nivel 2: alerta alta - preparar cierre, todavia no obligatorio.
const condicionNivel2 =
  !condicionNivel3 &&
  (hayTormentaElectrica || rafagaKt >= UMBRAL_RAFAGA_CIERRE_KT || visibilidadM <= UMBRAL_VISIBILIDAD_CIERRE_M);

// Nivel 1: monitoreo activo - viento sostenido elevado, sin tormenta.
const condicionNivel1 =
  !condicionNivel3 && !condicionNivel2 && vientoSostenidoKt >= UMBRAL_VIENTO_SOSTENIDO_ALERTA_KT;

let riesgoNivel = 0;
if (condicionNivel3) riesgoNivel = 3;
else if (condicionNivel2) riesgoNivel = 2;
else if (condicionNivel1) riesgoNivel = 1;

const ahora = new Date(clima.hora_reporte_utc);

const vuelosAfectados = vuelos
  .map((vuelo) => {
    const horaVuelo = new Date(vuelo.hora_programada_utc);
    const minutosHastaVuelo = Math.round((horaVuelo.getTime() - ahora.getTime()) / 60000);
    return Object.assign({}, vuelo, { minutos_hasta_operacion: minutosHastaVuelo });
  })
  .filter((vuelo) => vuelo.minutos_hasta_operacion >= 0 && vuelo.minutos_hasta_operacion <= VENTANA_MINUTOS);

const accionesPorNivel = {
  0: 'OPERACION_NORMAL',
  1: 'MONITOREO_ACTIVO',
  2: 'ALERTA_PREPARAR_CIERRE',
  3: 'CIERRE_RAMPA',
};

// Version sin guion bajo, solo para texto libre (Telegram): Telegram interpreta
// un "_" suelto como inicio de cursiva en Markdown y rechaza el mensaje entero
// si no encuentra el cierre ("can't find end of the entity").
const accionesPorNivelLegible = {
  0: 'Operacion Normal',
  1: 'Monitoreo Activo',
  2: 'Alerta - Preparar Cierre',
  3: 'Cierre de Rampa',
};

const accionRequerida = accionesPorNivel[riesgoNivel];
const accionRequeridaLegible = accionesPorNivelLegible[riesgoNivel];

const resumen =
  `Nivel de riesgo ${riesgoNivel} (${accionRequeridaLegible}) en ${clima.estacion}. ` +
  `Viento ${vientoSostenidoKt}kt, rafagas ${rafagaKt}kt. ` +
  `Tormenta electrica: ${hayTormentaElectrica ? 'SI' : 'NO'}. ` +
  `Windshear: ${hayWindshear ? 'SI' : 'NO'}. ` +
  `${vuelosAfectados.length} vuelo(s) afectado(s) en los proximos ${VENTANA_MINUTOS} minutos.`;

return [
  {
    json: {
      riesgo_nivel: riesgoNivel,
      riesgo_nivel_3: riesgoNivel === 3,
      accion_requerida: accionRequerida,
      resumen,
      cantidad_vuelos_afectados: vuelosAfectados.length,
      vuelos_afectados: vuelosAfectados,
      reporte_meteorologico: clima,
    },
  },
];
