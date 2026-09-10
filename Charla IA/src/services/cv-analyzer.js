const { getCompletion } = require("./groq-client");
const { ValidationError } = require("../errors/app-errors");

const SYSTEM_PROMPT = `Sos un sistema de filtrado ATS (Applicant Tracking System) automatizado. 
Tu funcion es evaluar CVs de candidatos y determinar cual es el mejor para un puesto especifico.

Reglas de evaluacion:
1. Analiza el contenido COMPLETO de cada CV, incluyendo TODO el texto presente.
2. Evalua la relevancia de las habilidades, experiencia y formacion para el puesto solicitado.
3. Asigna un puntaje de 0 a 100 a cada CV basandote en la coincidencia con los requisitos.
4. Ordena los CVs de mayor a menor puntaje.
5. Para cada CV, proporciona una justificacion breve de la puntuacion asignada.

IMPORTANTE: Tu analisis se basa unicamente en el TEXTO que recibes. Evaluas las keywords, 
habilidades mencionadas, experiencia y formacion que aparecen en el texto del CV, sin importar el formato 
o la presentacion visual del documento.

Responde SIEMPRE con el siguiente formato JSON (sin markdown, sin backticks, solo JSON puro):
{
  "ranking": [
    {
      "cvNumber": 1,
      "candidateName": "Nombre del candidato si aparece",
      "score": 95,
      "justification": "Justificacion del puntaje",
      "keySkillsFound": ["skill1", "skill2"],
      "experienceYears": "X anos de experiencia relevante",
      "strengths": ["fortaleza1", "fortaleza2"],
      "weaknesses": ["debilidad1", "debilidad2"]
    }
  ],
  "bestCandidate": {
    "cvNumber": 1,
    "summary": "Resumen de por que este candidato es el mejor para el puesto"
  }
}`;

function buildUserPrompt(jobPosition, requirements, cvTexts) {
  if (!jobPosition || jobPosition.trim().length === 0) {
    throw new ValidationError("El puesto a cubrir es obligatorio.");
  }

  if (!cvTexts || cvTexts.length === 0) {
    throw new ValidationError("Debe proporcionar al menos un CV para evaluar.");
  }

  let prompt = `Puesto a cubrir: ${jobPosition}\n\n`;

  if (requirements && requirements.trim().length > 0) {
    prompt += `Requisitos del reclutador: ${requirements}\n\n`;
  }

  prompt += "A continuacion los CVs a evaluar:\n\n";

  cvTexts.forEach((cvText, index) => {
    prompt += `=== CV ${index + 1} ===\n${cvText}\n\n`;
  });

  prompt +=
    "Por favor, evalua cada CV segun las reglas establecidas y determina el mejor candidato para el puesto.";

  return prompt;
}

async function analyzeCvs(jobPosition, requirements, cvTexts) {
  const userPrompt = buildUserPrompt(jobPosition, requirements, cvTexts);
  const rawResponse = await getCompletion(SYSTEM_PROMPT, userPrompt);

  try {
    let cleanedResponse = rawResponse.trim();

    // Remover bloques de codigo markdown si la IA los incluye
    if (cleanedResponse.startsWith("```")) {
      cleanedResponse = cleanedResponse
        .replace(/^```(?:json)?\s*\n?/, "")
        .replace(/\n?```\s*$/, "");
    }

    const parsedResult = JSON.parse(cleanedResponse);

    if (!parsedResult.ranking || !Array.isArray(parsedResult.ranking)) {
      throw new Error("La respuesta no contiene un ranking valido.");
    }

    return parsedResult;
  } catch (parseError) {
    return {
      ranking: [],
      rawResponse: rawResponse,
      parseError: "La IA no retorno un JSON valido. Se muestra la respuesta sin procesar.",
    };
  }
}

module.exports = { analyzeCvs, buildUserPrompt, SYSTEM_PROMPT };
