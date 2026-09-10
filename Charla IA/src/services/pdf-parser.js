const pdfParse = require("pdf-parse");
const { FileParseError } = require("../errors/app-errors");

async function extractTextFromPdf(buffer) {
  try {
    const data = await pdfParse(buffer);

    if (!data.text || data.text.trim().length === 0) {
      throw new FileParseError(
        "El PDF no contiene texto extraible. Puede estar escaneado o protegido."
      );
    }

    return data.text;
  } catch (error) {
    if (error instanceof FileParseError) {
      throw error;
    }

    throw new FileParseError(
      `Error al procesar el archivo PDF: ${error.message}`
    );
  }
}

module.exports = { extractTextFromPdf };
