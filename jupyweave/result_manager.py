from .exceptions.processor_errors import ResultNotFoundError


class ResultManager:
    """Manages results of snippet execution"""

    def __init__(self):
        """Creates empty manages"""
        self.__results = {}

    def store(self, result_id, result):
        """Stores new result"""
        self.__results[result_id] = result

    def get(self, result_id):
        """Returns stored result (or exception)"""
        try:
            return self.__results[result_id]
        except KeyError:
            raise ResultNotFoundError(result_id)
