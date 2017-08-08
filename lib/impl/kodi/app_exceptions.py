__author__ = 'bromix'


class AppException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self._message = message

    def get_message(self):
        return self._message
