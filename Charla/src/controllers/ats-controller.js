const express = require("express");
const { upload } = require("../middleware/upload");
const { extractTextFromPdf } = require("../services/pdf-parser");
const { analyzeCvs } = require("../services/cv-analyzer");
const { ValidationError } = require("../errors/app-errors");

const router = express.Router();

router.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

router.post("/analyze", upload.array("cvFiles", 10), async (req, res, next) => {
  try {
    const { jobPosition, requirements } = req.body;

    if (!jobPosition || jobPosition.trim().length === 0) {
      throw new ValidationError("El puesto a cubrir es obligatorio.");
    }

    if (!req.files || req.files.length === 0) {
      throw new ValidationError(
        "Debe subir al menos un archivo PDF para evaluar."
      );
    }

    // Extraer texto de cada PDF subido
    const cvTexts = [];

    for (const file of req.files) {
      let text;

      if (file.mimetype === "application/pdf") {
        text = await extractTextFromPdf(file.buffer);
      } else {
        text = file.buffer.toString("utf-8");
      }

      cvTexts.push({
        fileName: file.originalname,
        text: text,
      });
    }

    const textContents = cvTexts.map((cv) => cv.text);

    const result = await analyzeCvs(
      jobPosition.trim(),
      requirements ? requirements.trim() : "",
      textContents
    );

    const enrichedResult = {
      ...result,
      cvSources: cvTexts.map((cv, index) => ({
        cvNumber: index + 1,
        fileName: cv.fileName,
        textLength: cv.text.length,
      })),
    };

    res.json(enrichedResult);
  } catch (error) {
    next(error);
  }
});

module.exports = router;
