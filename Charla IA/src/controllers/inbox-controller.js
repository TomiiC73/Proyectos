/* =============================================================================
   INBOX CONTROLLER — API endpoint para emails recibidos via IMAP
   GET /api/inbox/poll   → devuelve emails cacheados del polling IMAP
   GET /api/inbox/status → devuelve estado de la conexión IMAP
   ============================================================================= */

"use strict";

const express = require("express");
const { getConfig } = require("../config/environment");
const { getCachedMessages } = require("../services/imap-service");

const router = express.Router();

/**
 * GET /api/inbox/poll
 * Devuelve todos los emails capturados por el poller IMAP.
 * El frontend compara UIDs y solo procesa los nuevos.
 */
router.get("/inbox/poll", (req, res) => {
  try {
    const config = getConfig();

    if (!config.gmail.imapUser || !config.gmail.imapPass) {
      return res.status(503).json({
        error: "IMAP no configurado. Agregá GMAIL_IMAP_USER y GMAIL_IMAP_PASS al .env",
        messages: [],
      });
    }

    const messages = getCachedMessages();
    return res.json({ messages });
  } catch (err) {
    console.error("[inbox/poll]", err);
    return res.status(500).json({ error: err.message, messages: [] });
  }
});

/**
 * GET /api/inbox/status
 * Devuelve si IMAP está configurado y qué email se monitorea.
 */
router.get("/inbox/status", (req, res) => {
  const config = getConfig();
  const configured = !!(config.gmail.imapUser && config.gmail.imapPass);
  return res.json({
    configured,
    monitoredEmail: configured ? config.gmail.imapUser : null,
  });
});

module.exports = router;
