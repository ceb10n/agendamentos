class BaseRequestError(Exception):
    def __init__(self, *args, **kwargs):
        self.errors = []
        self.code = 400

        if 'code' in kwargs:
            self.code = kwargs['code']

    def add_error(self, err):
        self.info.append(err)

    def set_errors(self, errors):
        self.errors = errors


class BadRequestError(BaseRequestError):
    """400 BadRequestError"""

    def __init__(self, *args, **kwargs):
        super(BadRequestError, self).__init__(*args, **kwargs)
