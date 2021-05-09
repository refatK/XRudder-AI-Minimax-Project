# The base class used when capturing any errors. Has an error message that can be printed
class Error(Exception):
    def __init__(self, msg='ERROR: There was an error'):
        self._msg = msg

    def get_msg(self):
        return self._msg
