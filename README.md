# Django Stream Logging

A Django logging handler that allows streaming log messages to the console, browser, or other output destinations in real-time, making it easier to monitor what is happening within your Django application.


## Installation

```bash
pip install django-stream-logging
```

## Usage for commands

To stream log messages from custom management commands to the console, use the `BaseLoggingCommand` class as a base for your command. This will enable easy and configurable logging for various log levels.

For example, create a file: `myapp/management/commands/test-command.py`:

```python
from django_stream_logging import BaseLoggingCommand

class Command(BaseLoggingCommand):
    def handle(self, *args, **options):
        # Logging examples using different log levels
        self.logger.info('This is an info message')
        self.write_info('This is an info message (alias)')
        self.logger.error('This is an error message')
        self.write_error('This is an error message (alias)')
        self.logger.warning('This is a warning message')
        self.write_warning('This is a warning message (alias)')
        self.logger.debug('This is a debug message')
        self.write_debug('This is a debug message (alias)')
        self.logger.critical('This is a critical message')
        self.write_critical('This is a critical message (alias)')
```

Now you can run the command, and the logs will be displayed in the console in real-time.

```bash
python manage.py test-command
```

Additionally, you can use the `--log-level` argument to set the desired log level for the command, allowing you to control which messages are shown:

```bash
python manage.py test-command --log-level=WARNING
```

## Usage for views

To stream log messages directly to the browser from a view, inherit from the `EventStreamView` class. This is useful for scenarios where real-time feedback is needed in the browser, such as monitoring tasks or processes.

Example:

```python
from time import sleep

class ExampleEventStreamView(EventStreamView):
    """
    Example view that inherits from EventStreamView and generates log messages
    of different levels to demonstrate its functionality.
    """
    def event_stream(self):
        # Generating log messages with different severity levels
        self.logger.debug("Este es un mensaje de DEBUG.")
        sleep(1)
        self.logger.info("Este es un mensaje de INFO.")
        sleep(1)
        self.logger.warning("Este es un mensaje de WARNING.")
        sleep(1)
        self.logger.error("Este es un mensaje de ERROR.")
        sleep(1)
        self.logger.critical("Este es un mensaje de CRITICAL.")
```
