import logging
from .commands import BaseLoggingCommand

# Define el nivel SUCCESS en 25, entre INFO (20) y WARNING (30)
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


class Logger(logging.Logger):
    def success(self, message, *args, **kwargs):
        """Log con un mensaje con nivel SUCCESS."""
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, **kwargs)


logging.setLoggerClass(Logger)


def separator(string='- ', length=30):
    """Genera una línea separadora repetida para efectos visuales."""
    return string * length


__all__ = [
    "BaseLoggingCommand",
    "Logger",
    "SUCCESS_LEVEL",
    "separator"
]
