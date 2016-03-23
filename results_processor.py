
class ResultsProcessor:

    def __init__(self):
        self.__result = ''

    def process_stream(self, text, stream_type):
        # TODO: stderr/stdout
        self.__result += text

    def process_data(self, mime_type, data):
        print(mime_type)
        pass

    def get_result(self):
        return self.__result
