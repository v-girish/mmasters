class MovieNotFoundException(Exception):
    def __init__(self, title):
        self.message = f"Movie with title {title} not found"
        super().__init__(self.message)


class MovieClientException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
