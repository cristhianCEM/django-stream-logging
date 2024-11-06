import logging
import colorlog
from abc import ABC
from django.core.management.base import BaseCommand
from django.conf import settings
from . import get_levels

BASE_LOG_FORMAT = "%(log_color)s%(message)s"
BASE_LOG_COLORS = {
    'DEBUG': 'blue',
    'INFO': 'cyan',
    'SUCCESS': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
    'FATAL': 'bold_red'
}
LEVELS_CHOICES = get_levels()
DEFAULT_LOG_LEVEL = 'DEBUG' if settings.DEBUG else 'INFO'


class BaseLoggingCommand(BaseCommand, ABC):
    logger = None
    logger_propagate = False
    log_level = DEFAULT_LOG_LEVEL
    log_format = BASE_LOG_FORMAT
    log_colors = BASE_LOG_COLORS

    def get_logger(self):
        """Obtiene el logger para la clase."""
        return logging.getLogger(__name__)

    def get_colorful_formatter(self):
        """Devuelve un formateador colorido para el logger."""
        return colorlog.ColoredFormatter(
            fmt=self.log_format,
            log_colors=self.log_colors
        )

    def add_colorful_handler(self, logger):
        """Añade un handler de salida colorida al logger."""
        handler = logging.StreamHandler()
        formatter = self.get_colorful_formatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def setup_logger(self):
        """Configura el logger solo si no se ha configurado previamente."""
        if self.logger:
            return
        self.logger = self.get_logger()
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(self.log_level)
        self.logger.propagate = self.logger_propagate
        self.add_colorful_handler(self.logger)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_logger()

    def create_parser(self, prog_name, subcommand, **kwargs):
        """Crea el parser del comando e incluye el argumento log-level."""
        parser = super().create_parser(prog_name, subcommand, **kwargs)
        parser.add_argument(
            '--log-level',
            type=str,
            choices=LEVELS_CHOICES,
            default=self.log_level,
            help='Nivel de logging para este comando.'
        )
        return parser

    def setup_logger_level(self, options):
        """Establece el nivel del logger si es diferente al actual."""
        option_level = options.get('log_level', self.log_level).upper()
        # Compara con el nivel actual para evitar reconfiguraciones innecesarias
        if option_level != self.log_level:
            self.log_level = getattr(logging, option_level, logging.INFO)
            self.logger.setLevel(self.log_level)

    def execute(self, *args, **options):
        """Ejecuta el comando asegurando que el nivel del logger esté configurado."""
        self.setup_logger_level(options)
        return super().execute(*args, **options)
