from logging import Handler


class EventStreamHandler(Handler):
    """
    Handler de logging que envía mensajes a través de Server-Sent Events (SSE).
    Utiliza una cola para comunicar mensajes entre el logger y el stream.
    """

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages_queue = queue

    def emit(self, record):
        """Formatea el mensaje y lo envía a la cola."""
        log_entry = self.format(record)
        self.messages_queue.put(log_entry)
