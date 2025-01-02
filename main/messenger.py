import logging
from main.constants import *

# pylint: disable=invalid-name
_messenger = None
def get_messenger(args=None):
    global _messenger
    if not _messenger:
        _messenger = Messenger(args)
    return _messenger

class Messenger:
    def __init__(self, args):
        self.logger = self.setup_logger(args)
        self.latest_messages = []
        self.message_history = []
        self.number = 0
        self.max_messages = 100

    def set_verbose(self):
        self.logger.setLevel(logging.DEBUG)
        for h in self.logger.handlers:
            h.setLevel(logging.DEBUG)

    def setup_logger(self, args):
        # https://docs.python.org/3/howto/logging.html#configuring-logging
        if not args or not args.verbose:
            level = logging.WARNING
        else:
            level = logging.DEBUG
        logger = logging.getLogger(LOG_NAME)
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def clear(self):
        self.message_history.clear()
        self.number = 0
        self.clear_latest()

    def clear_latest(self):
        self.latest_messages.clear()

    def add(self, message):
        self.latest_messages.append(message)
        self.message_history.append(message)
        self.logger.info(message)
        self.number += 1
        if self.number > self.max_messages:
            self.message_history = self.message_history[(self.number - self.max_messages):]
            self.number = self.max_messages

    def get_latest(self, count=-1):
        if count > -1:
            start = max(self.number - count, 0)
            return self.message_history[start:]
        return self.latest_messages

    def warning(self, message):
        self.logger.warning(message)
