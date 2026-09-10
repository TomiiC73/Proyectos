const express = require("express");
const { getConfig } = require("../config/environment");

const router = express.Router();
const config = getConfig();

/**
 * POST /api/gmail-analyze
 * Proxy seguro hacia Groq que usa la API key del .env
 * El frontend nunca ve la clave.
 *
 * Body: { systemPrompt: string, userContent: string }
 * Returns: { response: string }
 */
router.post("/gmail-analyze", async (req, res) => {
  try {
    const { systemPrompt, userContent } = req.body;

    if (!systemPrompt || !userContent) {
      return res.status(400).json({ error: "Faltan campos: systemPrompt y userContent son obligatorios." });
    }

    const apiKey = config.groq.apiKey;
    if (!apiKey) {
      return res.status(500).json({ error: "API key de Groq no configurada en el servidor (.env)." });
    }

    const groqRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type":  "application/json",
        "Authorization": `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model:       config.groq.model || "llama-3.3-70b-versatile",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user",   content: userContent  },
        ],
        temperature: 0.1,
        max_tokens:  1024,
      }),
    });

    if (!groqRes.ok) {
      const errBody = await groqRes.json().catch(() => ({}));
      return res.status(groqRes.status).json({
        error: errBody.error?.message || `Groq HTTP ${groqRes.status}`,
      });
    }

    const data = await groqRes.json();
    const text = data.choices?.[0]?.message?.content || "";
    return res.json({ response: text });

  } catch (err) {
    console.error("[gmail-analyze]", err);
    return res.status(500).json({ error: err.message });
  }
});

module.exports = router;
