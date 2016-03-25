import re
from exceptions.processor_errors import SnippetRuntimeError


class ResultsProcessor:

    ANSI_ESCAPE_SEQ_RE = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'
    ESCAPE_RE = re.compile(ANSI_ESCAPE_SEQ_RE)

    def __init__(self, allow_errors, output_types):
        self.__allow_errors = allow_errors
        self.__output_types = output_types

        self.__result = ''

    def process_stream(self, text, stream_type):
        if self.__output_types.is_enabled(stream_type):
            self.__result += text

    def process_data(self, mime_type, data):
        if not self.__output_types.is_enabled(mime_type):
            return

        # TODO
        print(mime_type)
        pass

    def process_error(self, name, value, traceback):
        result = ''

        for t in traceback:
            result += str.format('\n{0}', ResultsProcessor.ESCAPE_RE.sub('', t))

        if not self.__allow_errors:
            raise SnippetRuntimeError(result)

        self.__result += result

    def get_result(self):
        return self.__result
