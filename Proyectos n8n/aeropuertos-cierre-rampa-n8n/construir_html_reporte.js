// Nodo Code: "Construir HTML del Reporte"
// Genera el HTML (+ footer de paginacion) del reporte de incidente con
// identidad visual propia (Aeropuertos Argentina 2000) para convertirlo a PDF
// en el nodo siguiente via Gotenberg. Reemplaza al viejo "Registrar Auditoria"
// en Google Sheets: ahora el registro del incidente es este PDF.

const data = $json;
const clima = data.reporte_meteorologico || {};
const vuelos = data.vuelos_afectados || [];
const nivel = data.riesgo_nivel;

// Paleta propia (petroleo + dorado + terracota), NO colores semanticos de
// framework: los dos niveles de severidad son variaciones tonales de la MISMA
// paleta calida, no un semaforo azul/amarillo/rojo generico.
const BRAND = '#0B3B39';
const ACCENT_NIVEL2 = '#C08A2E';
const ACCENT_NIVEL2_SUAVE = '#F5EBD8';
const ACCENT_NIVEL3 = '#8C3A2E';
const ACCENT_NIVEL3_SUAVE = '#F2E2DE';

const colorNivel = nivel === 3 ? ACCENT_NIVEL3 : nivel === 2 ? ACCENT_NIVEL2 : BRAND;
const colorNivelSuave = nivel === 3 ? ACCENT_NIVEL3_SUAVE : nivel === 2 ? ACCENT_NIVEL2_SUAVE : '#EAEFEE';
const etiquetasNivel = { 2: 'Alerta - Preparar Cierre', 3: 'Cierre de Rampa' };
const etiquetaNivel = etiquetasNivel[nivel] || 'Reporte Operacional';
const generadoEl = new Date().toISOString();
const referencia = 'RPT-' + Date.now();

// Hash corto y determinista del contenido, solo para que el pie tecnico se
// sienta como el checksum de un sistema real (no es criptografico).
function hashCorto(texto) {
  let h = 5381;
  for (let i = 0; i < texto.length; i++) h = (h * 33) ^ texto.charCodeAt(i);
  return (h >>> 0).toString(16).toUpperCase().padStart(8, '0');
}
const hashReporte = hashCorto(referencia + (data.resumen || '') + generadoEl);

// Isotipo: no es un icono generico de libreria (flecha/pin) sino un motivo de
// radar de control de trafico aereo (anillos de barrido + blip), a juego con
// la paleta propia.
const svgRadar =
  '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">' +
  '<circle cx="12" cy="12" r="9.5" stroke="white" stroke-opacity="0.22" stroke-width="1"/>' +
  '<circle cx="12" cy="12" r="6.2" stroke="white" stroke-opacity="0.4" stroke-width="1"/>' +
  '<circle cx="12" cy="12" r="3" stroke="white" stroke-opacity="0.65" stroke-width="1"/>' +
  `<line x1="12" y1="12" x2="19" y2="6" stroke="${ACCENT_NIVEL2}" stroke-width="1.4" stroke-linecap="round"/>` +
  `<circle cx="12" cy="12" r="1.3" fill="${ACCENT_NIVEL2}"/>` +
  '</svg>';

const filasVuelos = vuelos.length
  ? vuelos
      .map(
        (v) => `
    <tr>
      <td class="flight">${v.vuelo || ''}</td>
      <td>${v.aerolinea || ''}</td>
      <td>${v.tipo_operacion || ''}</td>
      <td>${v.posicion_rampa || ''}</td>
      <td class="num">${v.minutos_hasta_operacion != null ? v.minutos_hasta_operacion + ' min' : '-'}</td>
    </tr>`,
      )
      .join('')
  : '<tr><td colspan="5" style="text-align:center;color:#74827D;padding:24px;">Sin vuelos afectados en la ventana evaluada</td></tr>';

const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
  :root {
    --brand: ${BRAND};
    --ink: #16221F;
    --ink-soft: #3F4D49;
    --muted: #74827D;
    --line: #E1E6E3;
    --surface: #F6F7F5;
    --accent: ${colorNivel};
    --accent-soft: ${colorNivelSuave};
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: 'IBM Plex Sans', Georgia, 'Segoe UI', sans-serif;
    color: var(--ink);
    font-size: 13.5px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    position: relative;
  }
  .watermark {
    position: fixed;
    top: 46%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-24deg);
    font-size: 64px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--brand);
    opacity: 0.035;
    white-space: nowrap;
    z-index: 0;
  }
  .page { position: relative; z-index: 1; padding: 40px 48px 28px; }

  .masthead { display: flex; align-items: center; justify-content: space-between; padding-bottom: 18px; border-bottom: 1px solid var(--line); }
  .brand { display: flex; align-items: center; gap: 11px; }
  .brand-mark { width: 38px; height: 38px; border-radius: 10px; background: var(--brand); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .brand-name { font-size: 11px; font-weight: 600; letter-spacing: 0.13em; text-transform: uppercase; color: var(--brand); }
  .brand-sub { font-size: 10px; color: var(--muted); letter-spacing: 0.03em; margin-top: 2px; }
  .meta { text-align: right; font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 9.5px; color: var(--muted); line-height: 1.7; }

  .hero { margin-top: 40px; margin-bottom: 36px; }
  .kicker { margin: 0 0 8px; font-size: 11px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
  .hero h1 { margin: 0 0 22px; font-size: 27px; font-weight: 600; letter-spacing: -0.01em; color: var(--brand); max-width: 480px; }
  .severity-strip { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; border-radius: 10px; background: var(--accent-soft); }
  .severity-strip .label { display: flex; align-items: center; gap: 9px; font-size: 13.5px; font-weight: 600; color: var(--accent); }
  .severity-strip .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); }
  .severity-strip .rule { flex: 1; height: 1px; background: var(--accent); opacity: 0.25; margin: 0 18px; }
  .severity-strip .n { font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 11px; color: var(--accent); opacity: 0.85; }

  .summary { margin-top: 18px; font-size: 13px; color: var(--ink-soft); line-height: 1.65; max-width: 620px; }

  .grid { margin-top: 26px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .card { border: 1px solid var(--line); border-radius: 8px; padding: 13px 15px; }
  .card h3 { margin: 0 0 9px; font-size: 9.5px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
  .stat-row { display: flex; align-items: baseline; justify-content: space-between; padding: 3px 0; }
  .stat-label { font-size: 11.5px; color: var(--muted); }
  .stat-value { font-size: 12.5px; font-weight: 500; color: var(--ink); font-variant-numeric: tabular-nums; }
  .stat-value.lg { font-size: 16px; font-weight: 600; color: var(--brand); }

  .terminal { margin-top: 10px; border-radius: 8px; overflow: hidden; border: 1px solid #0A2A28; }
  .terminal-bar { display: flex; align-items: center; justify-content: space-between; background: #0A2A28; padding: 7px 12px; }
  .terminal-bar .dots { display: flex; gap: 4px; }
  .terminal-bar .dots span { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.25); }
  .terminal-bar .label { font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 9px; letter-spacing: 0.1em; color: rgba(255,255,255,0.5); text-transform: uppercase; }
  .terminal-body { padding: 12px 14px; background: var(--brand); color: #CFE3E0; font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 10.5px; letter-spacing: 0.01em; word-break: break-all; }

  .section-label { margin: 30px 0 2px; font-size: 9.5px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; border-top: 2px solid var(--brand); }
  thead th { text-align: left; font-size: 9.5px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); padding: 8px 10px 6px; }
  thead th:last-child { text-align: right; }
  tbody td { padding: 8px 10px; font-size: 12.5px; color: var(--ink-soft); border-bottom: 1px solid var(--surface); }
  tbody tr:last-child td { border-bottom: none; }
  td.num { text-align: right; font-variant-numeric: tabular-nums; color: var(--ink); font-weight: 500; }
  td.flight { font-weight: 600; color: var(--brand); }

  .tech-footer { margin-top: 44px; padding-top: 12px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 9px; color: var(--muted); letter-spacing: 0.02em; }
</style>
</head>
<body>
  <div class="watermark">AA2000 &middot; OPERACIONAL</div>
  <div class="page">
    <div class="masthead">
      <div class="brand">
        <div class="brand-mark">${svgRadar}</div>
        <div>
          <div class="brand-name">Aeropuertos Argentina 2000</div>
          <div class="brand-sub">Operaciones de Rampa</div>
        </div>
      </div>
      <div class="meta">REF ${referencia}<br/>${generadoEl}</div>
    </div>

    <div class="hero">
      <p class="kicker">Protocolo de Cierre de Rampa</p>
      <h1>Reporte de Incidente Operacional</h1>
      <div class="severity-strip">
        <span class="label"><span class="dot"></span>Nivel ${nivel} &middot; ${etiquetaNivel}</span>
        <span class="rule"></span>
        <span class="n">${clima.estacion || '-'}</span>
      </div>
      <div class="summary">${data.resumen || ''}</div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Estacion</h3>
        <div class="stat-row"><span class="stat-label">Codigo</span><span class="stat-value lg">${clima.estacion || '-'}</span></div>
        <div class="stat-row"><span class="stat-label">Nombre</span><span class="stat-value">${clima.nombre_estacion || '-'}</span></div>
        <div class="stat-row"><span class="stat-label">Hora de reporte (UTC)</span><span class="stat-value">${clima.hora_reporte_utc || '-'}</span></div>
      </div>
      <div class="card">
        <h3>Condiciones de Viento</h3>
        <div class="stat-row"><span class="stat-label">Sostenido</span><span class="stat-value">${(clima.viento && clima.viento.velocidad_kt) || 0} kt</span></div>
        <div class="stat-row"><span class="stat-label">Rafaga</span><span class="stat-value">${(clima.viento && clima.viento.rafaga_kt) || 0} kt</span></div>
        <div class="stat-row"><span class="stat-label">Visibilidad</span><span class="stat-value">${clima.visibilidad_m || '-'} m</span></div>
        <div class="stat-row"><span class="stat-label">Tormenta / Windshear</span><span class="stat-value">${clima.actividad_electrica ? 'Si' : 'No'} / ${clima.windshear_reportado ? 'Si' : 'No'}</span></div>
      </div>
    </div>

    <div class="terminal">
      <div class="terminal-bar">
        <span class="label">Datos Raw &middot; METAR</span>
        <span class="dots"><span></span><span></span><span></span></span>
      </div>
      <div class="terminal-body">${clima.metar_crudo || 'METAR no disponible'}</div>
    </div>

    <p class="section-label">Vuelos Afectados (${vuelos.length})</p>
    <table>
      <thead><tr><th>Vuelo</th><th>Aerolinea</th><th>Operacion</th><th>Posicion</th><th>Ventana</th></tr></thead>
      <tbody>${filasVuelos}</tbody>
    </table>

    <div class="tech-footer">
      <span>Sistema de Triage Operacional &middot; v2.4.0</span>
      <span>SHA ${hashReporte}</span>
    </div>
  </div>
</body>
</html>`;

const footerHtml = `<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 100%; font-family: Consolas, 'Liberation Mono', Menlo, monospace; font-size: 8px; color: #74827D; }
  table { width: 100%; border-collapse: collapse; }
  td { padding: 0 48px; white-space: nowrap; }
  td.right { text-align: right; }
</style>
</head>
<body>
  <table><tr>
    <td>SISTEMA DE TRIAGE OPERACIONAL &middot; AA2000</td>
    <td class="right"><span class="pageNumber"></span> / <span class="totalPages"></span></td>
  </tr></table>
</body>
</html>`;

const binaryHtml = await this.helpers.prepareBinaryData(Buffer.from(html, 'utf-8'), 'index.html', 'text/html');
const binaryFooter = await this.helpers.prepareBinaryData(Buffer.from(footerHtml, 'utf-8'), 'footer.html', 'text/html');

return [{ json: data, binary: { data: binaryHtml, footer: binaryFooter } }];
