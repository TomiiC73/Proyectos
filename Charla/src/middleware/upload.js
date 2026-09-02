const multer = require("multer");
const path = require("path");
const { ValidationError } = require("../errors/app-errors");

const ALLOWED_MIMETYPES = [
  "application/pdf",
  "text/plain",
];

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB por archivo
const MAX_FILES = 10;

const storage = multer.memoryStorage();

const fileFilter = (req, file, cb) => {
  if (ALLOWED_MIMETYPES.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(
      new ValidationError(
        `Tipo de archivo no permitido: ${file.mimetype}. Solo se aceptan PDF y TXT.`
      ),
      false
    );
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: MAX_FILES,
  },
});

module.exports = { upload, MAX_FILES };
