import logging

# Define el nivel SUCCESS en 25, entre INFO (20) y WARNING (30)
SUCCESS_LEVEL = 25


class Logger(logging.Logger):
    def separator(self, string='- ', length=30):
        return string * length

    def success(self, message, *args, **kwargs):
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, **kwargs)


def get_levels() -> list:
    return [level for level in logging._levelToName.values()]


logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
logging.setLoggerClass(Logger)
