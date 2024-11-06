import logging


def get_levels() -> list:
    """Retorna una lista de todos los niveles de logging disponibles."""
    return [level for level in logging._levelToName.values()]


def separator(string='- ', length=30):
    """Genera una línea separadora repetida para efectos visuales."""
    return string * length
