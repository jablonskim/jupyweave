from exceptions.processor_errors import ResultNotFoundError


class ResultManager:

    def __init__(self):
        self.results = {}

    def store(self, result_id, result):
        self.results[result_id] = result

    def get(self, result_id):
        try:
            return self.results[result_id]
        except KeyError:
            raise ResultNotFoundError()
