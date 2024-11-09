import logging
import colorlog
from django.core.management.base import BaseCommand
from abc import ABC
from .mixins import LoggingMixin

BASE_LOG_COLORS = {
    'DEBUG': 'blue',
    'INFO': 'cyan',
    'SUCCESS': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
    'FATAL': 'bold_red'
}
BASE_LOG_FMT = {
    'DEBUG': '%(log_color)s%(levelname)s : %(message)s',
    'INFO': '%(log_color)s%(message)s',
    'SUCCESS': '%(log_color)s%(message)s',
    'WARNING': '%(log_color)s%(levelname)s : %(message)s',
    'ERROR': '%(log_color)s%(levelname)s : %(message)s',
    'CRITICAL': '%(log_color)s%(levelname)s : %(message)s (%(module)s:%(lineno)d)',
    'FATAL': '%(log_color)s%(levelname)s : %(message)s (%(module)s:%(lineno)d)',
}
LEVELS_CHOICES = BASE_LOG_COLORS.keys()


class BaseLoggingCommand(BaseCommand, LoggingMixin, ABC):

    log_fmt = BASE_LOG_FMT
    log_colors = BASE_LOG_COLORS

    def get_colorful_formatter(self):
        """Devuelve un formateador colorido para el logger."""
        return colorlog.LevelFormatter(
            fmt=self.log_fmt,
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

    def execute(self, *args, **options):
        """Ejecuta el comando asegurando que el nivel del logger esté configurado."""
        option_level = options.get('log_level')
        if option_level:
            self.set_logger_level(option_level)
        return super().execute(*args, **options)
