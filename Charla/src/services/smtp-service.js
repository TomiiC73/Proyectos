/* =============================================================================
   SMTP SERVICE — Servidor SMTP local que recibe emails entrantes
   Usa smtp-server + mailparser para capturar emails y exponerlos al lab
   Puerto: 2525 (configurable via SMTP_PORT en .env)
   ============================================================================= */

"use strict";

const { SMTPServer } = require("smtp-server");
const { simpleParser } = require("mailparser");

/* ── In-memory store ──────────────────────────────────────────────────────── */
let cachedMessages = [];
let uidCounter     = 1;

/**
 * Returns all emails received so far.
 */
function getCachedMessages() {
  return cachedMessages;
}

/**
 * Create and start the SMTP server.
 * Accepts any sender/recipient without authentication (solo para lab).
 */
function startSmtpServer(port = 2525) {
  const server = new SMTPServer({
    /* Accept any connection without auth (it's a lab, not production) */
    authOptional: true,
    allowInsecureAuth: true,

    /* Don't verify sender/recipient against a real domain */
    disabledCommands: ["STARTTLS"],

    onData(stream, session, callback) {
      let rawChunks = [];

      stream.on("data", (chunk) => rawChunks.push(chunk));

      stream.on("end", async () => {
        try {
          const rawEmail = Buffer.concat(rawChunks);
          const parsed   = await simpleParser(rawEmail);

          const fromAddr    = parsed.from?.value?.[0] || {};
          const senderName  = fromAddr.name    || fromAddr.address || "Desconocido";
          const senderEmail = fromAddr.address || "";

          /* Plain text, fallback to stripped HTML */
          let textBody = parsed.text || "";
          if (!textBody && parsed.html) {
            textBody = parsed.html
              .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
              .replace(/<[^>]+>/g, " ")
              .replace(/\s{2,}/g, " ")
              .trim();
          }

          const msg = {
            uid:          uidCounter++,
            subject:      parsed.subject || "(Sin asunto)",
            senderName,
            senderEmail,
            textBody:     textBody.slice(0, 4000),
            date:         parsed.date
              ? parsed.date.toISOString()
              : new Date().toISOString(),
          };

          cachedMessages.push(msg);
          /* Keep only the last 50 */
          if (cachedMessages.length > 50) cachedMessages = cachedMessages.slice(-50);

          console.log(`[smtp] ✉  Email recibido de ${senderEmail} — "${msg.subject}"`);
          callback(null); /* Accept the email */
        } catch (err) {
          console.error("[smtp] Error parseando email:", err.message);
          callback(null); /* Accept anyway to avoid bouncing */
        }
      });

      stream.on("error", (err) => {
        console.error("[smtp] Stream error:", err.message);
        callback(err);
      });
    },

    onError(err) {
      console.error("[smtp] Server error:", err.message);
    },
  });

  server.listen(port, "0.0.0.0", () => {
    console.log(`[smtp] Servidor SMTP escuchando en puerto ${port}`);
    console.log(`[smtp] Usá ngrok para exponerlo: ngrok tcp ${port}`);
  });

  server.on("error", (err) => {
    console.error("[smtp] Error al iniciar servidor:", err.message);
  });

  return server;
}

module.exports = { startSmtpServer, getCachedMessages };
