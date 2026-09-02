const Groq = require("groq-sdk");
const { getConfig } = require("../config/environment");
const { GroqApiError, ConfigurationError } = require("../errors/app-errors");

function createGroqClient() {
  const config = getConfig();

  if (!config.groq.apiKey || config.groq.apiKey.trim() === "") {
    throw new ConfigurationError(
      "La variable de entorno GROQ_API_KEY no esta configurada. " +
        "Revisar el archivo .env."
    );
  }

  return new Groq({ apiKey: config.groq.apiKey });
}

async function getCompletion(systemPrompt, userPrompt) {
  const config = getConfig();
  const client = createGroqClient();

  try {
    // Recolectar respuesta completa desde stream para poder parsear el JSON
    const stream = await client.chat.completions.create({
      model: config.groq.model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      temperature: config.groq.temperature,
      max_completion_tokens: config.groq.maxTokens,
      top_p: 1,
      stream: true,
      stop: null,
    });

    let fullResponse = "";

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || "";
      fullResponse += content;
    }

    if (!fullResponse || fullResponse.trim().length === 0) {
      throw new GroqApiError("La API de Groq no retorno ninguna respuesta.");
    }

    return fullResponse;
  } catch (error) {
    if (error instanceof GroqApiError || error instanceof ConfigurationError) {
      throw error;
    }

    if (error.status === 401) {
      throw new GroqApiError(
        "API key de Groq invalida. Verificar la configuracion en .env."
      );
    }

    if (error.status === 429) {
      throw new GroqApiError(
        "Se excedio el limite de requests a Groq. Intentar nuevamente en unos segundos."
      );
    }

    throw new GroqApiError(`Error al llamar a la API de Groq: ${error.message}`);
  }
}

module.exports = { createGroqClient, getCompletion };
