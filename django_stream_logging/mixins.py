from django.conf import settings
import logging

DEFAULT_LOG_FORMAT = "%(levelname)s : %(message)s"
try:
    if settings.DEBUG:
        DEFAULT_LOG_LEVEL = logging.DEBUG
    else:
        DEFAULT_LOG_LEVEL = logging.INFO
except AttributeError:
    DEFAULT_LOG_LEVEL = logging.INFO


class LoggingMixin:
    logger = None
    logger_propagate = False
    log_level = DEFAULT_LOG_LEVEL
    log_format = DEFAULT_LOG_FORMAT

    def get_logger(self):
        """Obtiene el logger para la clase."""
        return logging.getLogger(__name__)

    def set_write_methods(self, logger):
        """Registra los métodos de escritura en el logger, con manejo para niveles personalizados."""
        self.write_debug = logger.debug
        self.write_info = logger.info
        self.write_success = getattr(logger, 'success', logger.info)
        self.write_warning = logger.warning
        self.write_error = logger.error
        self.write_critical = logger.critical
        self.write_fatal = logger.critical

    def setup_logger(self):
        """Configura el logger solo si no se ha configurado previamente."""
        if self.logger:
            return
        self.logger = self.get_logger()
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(self.log_level)
        self.logger.propagate = self.logger_propagate
        self.set_write_methods(self.logger)
