class RequestFailure(Exception):
    "Raised for request failures"
    pass

class HTTPError(Exception):
    "Raised for non 200 response codes"
    def __init__(self, meg, status_code):
        super(HTTPError, self).__init__(msg)
        self.status_code = status_code