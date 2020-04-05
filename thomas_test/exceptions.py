##################################
# EXCEPTIONS

class DotEnvError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NytApiError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)