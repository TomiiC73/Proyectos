/* =============================================================================
   IMAP SERVICE — Polling de bandeja Gmail via IMAP (imapflow + mailparser)
   Se conecta periódicamente al INBOX, busca mensajes nuevos, los parsea
   y los almacena en memoria para que el frontend los consuma.
   ============================================================================= */

"use strict";

const { ImapFlow }     = require("imapflow");
const { simpleParser } = require("mailparser");

/* ── In-memory store ──────────────────────────────────────────────────────── */
let cachedMessages = [];   // { uid, subject, senderName, senderEmail, textBody, date }
let highestUid     = 0;    // Track the highest UID we've fetched
let isPolling      = false;
let pollInterval   = null;

/* ── Public API ───────────────────────────────────────────────────────────── */

function getCachedMessages() {
  return cachedMessages;
}

/**
 * Perform a single IMAP fetch cycle:
 *  1. Connect to imap.gmail.com
 *  2. Open INBOX
 *  3. Search for recent messages (last 24h)
 *  4. Fetch any with UID > highestUid
 *  5. Parse and cache them
 *  6. Disconnect
 */
async function fetchNewEmails(config) {
  const { imapUser, imapPass } = config.gmail;
  if (!imapUser || !imapPass) return [];

  const client = new ImapFlow({
    host:   "imap.gmail.com",
    port:   993,
    secure: true,
    auth: {
      user: imapUser,
      pass: imapPass,
    },
    logger: false,
    tls: { rejectUnauthorized: false },
    /* Timeout to avoid hanging connections */
    socketTimeout:  30000,
    greetingTimeout: 15000,
  });

  const newMessages = [];

  try {
    await client.connect();
    console.log("[imap] Conectado a imap.gmail.com");

    const lock = await client.getMailboxLock("INBOX");

    try {
      /* Search messages from the last 24 hours */
      const since = new Date(Date.now() - 24 * 60 * 60 * 1000);

      let uids;
      try {
        /* client.search returns an array of sequence numbers or UIDs */
        uids = await client.search({ since }, { uid: true });
      } catch (searchErr) {
        console.warn("[imap] Error en búsqueda:", searchErr.message);
        uids = [];
      }

      if (!uids || uids.length === 0) {
        console.log("[imap] No hay mensajes recientes (últimas 24h).");
      } else {
        /* Filter to only UIDs higher than what we've seen */
        const freshUids = uids.filter(u => u > highestUid);
        console.log(`[imap] Encontrados ${uids.length} msgs, ${freshUids.length} nuevos (highestUid=${highestUid})`);

        if (freshUids.length > 0) {
          /* Build a UID range string for fetching, e.g. "150:200" */
          const minUid = Math.min(...freshUids);
          const maxUid = Math.max(...freshUids);
          const range = `${minUid}:${maxUid}`;

          /* Use the async iterator from client.fetch */
          for await (const msg of client.fetch(range, { source: true }, { uid: true })) {
            try {
              const parsed = await simpleParser(msg.source);

              const fromAddr    = (parsed.from?.value?.[0]) || {};
              const senderName  = fromAddr.name    || fromAddr.address || "Desconocido";
              const senderEmail = fromAddr.address  || "";

              /* Prefer plain text, fallback to stripping HTML */
              let textBody = parsed.text || "";
              if (!textBody && parsed.html) {
                textBody = parsed.html
                  .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
                  .replace(/<[^>]+>/g, " ")
                  .replace(/&nbsp;/gi, " ")
                  .replace(/\s{2,}/g, " ")
                  .trim();
              }

              const emailObj = {
                uid:         msg.uid,
                subject:     parsed.subject || "(Sin asunto)",
                senderName,
                senderEmail,
                textBody:    textBody.slice(0, 8000),
                date:        parsed.date
                  ? parsed.date.toISOString()
                  : new Date().toISOString(),
              };

              newMessages.push(emailObj);
              console.log(`[imap] ✉  UID ${msg.uid} — de ${senderEmail} — "${emailObj.subject}"`);

              if (msg.uid > highestUid) highestUid = msg.uid;
            } catch (parseErr) {
              console.warn(`[imap] Error parseando UID ${msg.uid}:`, parseErr.message);
              /* Track the UID so we don't retry it forever */
              if (msg.uid > highestUid) highestUid = msg.uid;
            }
          }
        }
      }
    } finally {
      lock.release();
    }

    await client.logout();
  } catch (connErr) {
    console.error("[imap] Error de conexión:", connErr.message);
    /* Try to force-close if still connected */
    try { client.close(); } catch { /* ignore */ }
  }

  /* Merge into cache */
  if (newMessages.length > 0) {
    cachedMessages.push(...newMessages);
    /* Cap at 100 messages */
    if (cachedMessages.length > 100) {
      cachedMessages = cachedMessages.slice(-100);
    }
    console.log(`[imap] Cache actualizado: ${cachedMessages.length} mensajes totales`);
  }

  return newMessages;
}

/**
 * Start periodic polling.
 * @param {object} config  - From getConfig()
 * @param {number} ms      - Poll interval in ms (default 8000 = 8s)
 */
function startPolling(config, ms = 8000) {
  if (isPolling) {
    console.log("[imap] Polling ya está activo");
    return;
  }
  isPolling = true;

  const { imapUser } = config.gmail;
  console.log(`[imap] Iniciando polling cada ${ms / 1000}s → ${imapUser}`);

  const doPoll = async () => {
    try {
      await fetchNewEmails(config);
    } catch (err) {
      console.error("[imap] Error en ciclo de polling:", err.message);
    }
  };

  /* First fetch immediately */
  doPoll();

  /* Then on interval */
  pollInterval = setInterval(doPoll, ms);
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval);
    pollInterval = null;
  }
  isPolling = false;
  console.log("[imap] Polling detenido");
}

module.exports = { startPolling, stopPolling, getCachedMessages, fetchNewEmails };
