// Nodo Code: "Calcular Nuevo ETD" (Rama B - vuelos en tierra: embarcando o listo_para_pushback)
// Entrada: un item por vuelo, ya filtrado por el Switch a los estados en tierra (salida fallback).
// Salida: mismo vuelo + hora_programada_original + 90 minutos de demora estimada por el cierre.

const DEMORA_ESTIMADA_MINUTOS = 90;

const vuelo = $json;
const etdOriginal = new Date(vuelo.hora_programada_original);
const nuevoEtd = new Date(etdOriginal.getTime() + DEMORA_ESTIMADA_MINUTOS * 60000);

return [
  {
    json: {
      id_vuelo: vuelo.id_vuelo,
      aerolinea: vuelo.aerolinea,
      estado_operativo: vuelo.estado_operativo,
      hora_programada_original: vuelo.hora_programada_original,
      demora_aplicada_minutos: DEMORA_ESTIMADA_MINUTOS,
      nuevo_ETD_estimado: nuevoEtd.toISOString(),
    },
  },
];
