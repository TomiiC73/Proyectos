class AppError extends Error {
  constructor(message, code, statusCode = 500) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
  }
}

class ValidationError extends AppError {
  constructor(message) {
    super(message, "VALIDATION_ERROR", 400);
  }
}

class GroqApiError extends AppError {
  constructor(message) {
    super(message, "GROQ_API_ERROR", 502);
  }
}

class FileParseError extends AppError {
  constructor(message) {
    super(message, "FILE_PARSE_ERROR", 422);
  }
}

class ConfigurationError extends AppError {
  constructor(message) {
    super(message, "CONFIGURATION_ERROR", 500);
  }
}

module.exports = {
  AppError,
  ValidationError,
  GroqApiError,
  FileParseError,
  ConfigurationError,
};
