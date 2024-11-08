import typing
from logging import Formatter, LogRecord

DEFAULT_LOG_FMT = '%(levelname)s : %(message)s'


class LevelBasedFormatter(Formatter):
    """
    Formateador que cambia el formato del mensaje según el nivel de log.
    Preconstruye los formateadores para cada nivel para evitar crear instancias repetidamente.
    """
    default_format = DEFAULT_LOG_FMT

    def __init__(self, fmt: typing.Mapping[str, str], **kwargs: typing.Any):
        super().__init__()
        self.formatters = {
            level: Formatter(fmt=f, **kwargs) for level, f in fmt.items()
        }
        self.default_formatter = Formatter(self.default_format)

    def format(self, record: LogRecord) -> str:
        formatter = self.formatters.get(record.levelname, self.default_formatter)
        return formatter.format(record)
