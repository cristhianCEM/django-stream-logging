import logging
import colorlog
from django.core.management.base import BaseCommand
from abc import ABC
from .mixins import LoggingMixin

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
LEVELS_CHOICES = BASE_LOG_COLORS.keys()


class BaseLoggingCommand(BaseCommand, LoggingMixin, ABC):

    log_format = BASE_LOG_FORMAT
    log_colors = BASE_LOG_COLORS

    def get_colorful_formatter(self):
        """Devuelve un formateador colorido para el logger."""
        return colorlog.ColoredFormatter(
            fmt=self.log_format,
            log_colors=self.log_colors
        )

    def add_colorful_handler(self):
        """Añade un handler de salida colorida al logger."""
        handler = logging.StreamHandler()
        formatter = self.get_colorful_formatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_logger()
        self.add_colorful_handler()

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

    def set_logger_level(self, options):
        """Ajusta el nivel del logger según el valor de --log-level si es diferente al actual."""
        option_level = options.get('log_level')
        if not option_level:
            return
        self.log_level = getattr(logging, option_level, self.log_level)
        if self.logger.level != self.log_level:
            self.logger.setLevel(self.log_level)

    def execute(self, *args, **options):
        """Ejecuta el comando asegurando que el nivel del logger esté configurado."""
        self.set_logger_level(options)
        return super().execute(*args, **options)
