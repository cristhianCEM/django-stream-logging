from django.http import StreamingHttpResponse
from django.views import View
from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue, Empty

from .handlers import EventStreamHandler
from .mixins import LoggingMixin
from .formatters import LevelBasedFormatter


END_OF_STREAM = object()
DEFAULT_LOG_FMT = {
    'DEBUG': '%(levelname)s : %(message)s',
    'INFO': '%(message)s',
    'SUCCESS': '%(message)s',
    'WARNING': '%(levelname)s : %(message)s',
    'ERROR': '%(levelname)s : %(message)s',
    'CRITICAL': '%(levelname)s : %(message)s (%(module)s:%(lineno)d)',
    'FATAL': '%(levelname)s : %(message)s (%(module)s:%(lineno)d)',
}


class EventStreamView(View, LoggingMixin, ABC):
    """
    Vista base para enviar logs en tiempo real utilizando Server-Sent Events (SSE).
    Debe ser extendida e implementar el método `event_stream`.
    """
    log_handler = None
    log_fmt = DEFAULT_LOG_FMT

    def get_formatter(self):
        """Obtiene un formateador que cambia el formato según el nivel de log."""
        return LevelBasedFormatter(fmt=self.log_fmt)

    def add_stream_handler(self):
        self.queue = Queue()
        self.log_handler = EventStreamHandler(self.queue)
        formatter = self.get_formatter()
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_logger()
        self.add_stream_handler()

    @abstractmethod
    def event_stream(self):
        """Método abstracto que debe implementar la lógica de generación de eventos."""
        raise NotImplementedError("Debe implementar el método event_stream.")

    def finish_stream(self):
        """Finaliza el envío de mensajes."""
        self.queue.put("Stream finalizado")
        self.queue.put(END_OF_STREAM)

    def handle_stream(self):
        """Maneja el stream de eventos."""
        try:
            self.event_stream()
        except Exception:
            self.logger.critical("Ha ocurrido una excepción no controlada.")
        finally:
            self.finish_stream()

    def flush_stream(self):
        """Envía los mensajes de la cola al cliente en formato SSE."""
        event_thread = Thread(target=self.handle_stream)
        event_thread.start()
        while True:
            try:
                message = self.queue.get(timeout=0.1)
                if message is END_OF_STREAM:
                    break
                yield message
            except Empty:
                if not event_thread.is_alive():
                    break

    def get_event_stream_response(self):
        """Retorna el StreamingHttpResponse configurado para SSE."""
        response = StreamingHttpResponse(
            self.flush_stream(),
            content_type='text/event-stream',
            charset='utf-8'
        )
        response['Cache-Control'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs):
        """Maneja la solicitud GET y devuelve la respuesta del stream de eventos."""
        option_level = request.GET.get('log_level', None)
        if option_level:
            self.set_logger_level(option_level)
        return self.get_event_stream_response()
