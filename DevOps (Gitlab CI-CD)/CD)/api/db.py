# Re-exportar la función de db_config para mantener compatibilidad
from db_config import get_db_connection

__all__ = ['get_db_connection']