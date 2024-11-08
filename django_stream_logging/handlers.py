from queue import Queue
from logging import Handler


class EventStreamHandler(Handler):
    """Manejador de logging que utiliza una cola para enviar mensajes a través de un evento de transmisión SSE."""

    messages_queue = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages_queue = Queue()

    def emit(self, record):
        """Formatea el mensaje y lo envía a la cola."""
        log_entry = self.format(record)
        self.messages_queue.put(log_entry)

    def finish(self):
        """Finaliza el envío de mensajes."""
        self.messages_queue.put("Stream finalizado")
        self.messages_queue.put(None)
