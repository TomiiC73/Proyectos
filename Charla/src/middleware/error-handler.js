const { AppError } = require("../errors/app-errors");

function errorHandler(err, req, res, next) {
  // Errores de Multer (tamanio de archivo, cantidad, tipo)
  if (err.code === "LIMIT_FILE_SIZE") {
    return res.status(400).json({
      error: {
        code: "FILE_TOO_LARGE",
        message: "El archivo excede el tamanio maximo permitido (5 MB).",
      },
    });
  }

  if (err.code === "LIMIT_FILE_COUNT") {
    return res.status(400).json({
      error: {
        code: "TOO_MANY_FILES",
        message: "Se excedio la cantidad maxima de archivos permitidos (10).",
      },
    });
  }

  // Errores tipados de la aplicacion
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
      },
    });
  }

  // Errores no controlados: no exponer detalles internos
  console.error("Error no controlado:", err);
  return res.status(500).json({
    error: {
      code: "INTERNAL_ERROR",
      message: "Error interno del servidor. Intentar nuevamente.",
    },
  });
}

module.exports = { errorHandler };
