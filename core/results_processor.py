import re
from base64 import b64decode
from exceptions.processor_errors import SnippetRuntimeError


class ResultsProcessor:

    ANSI_ESCAPE_SEQ_RE = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'
    ESCAPE_RE = re.compile(ANSI_ESCAPE_SEQ_RE)

    def __init__(self, allow_errors, output_types, result_patterns, output_manager, postprocessing_manager):
        self.__allow_errors = allow_errors
        self.__output_types = output_types
        self.__result_patterns = result_patterns
        self.__output_manager = output_manager
        self.__postprocessing_manager = postprocessing_manager

        self.__result = ''

    def process_stream(self, text, stream_type):
        if self.__output_types.is_enabled(stream_type):
            self.__result += self.__postprocessing_manager.result(text)

    def process_data(self, mime_type, data):
        if not self.__output_types.is_enabled(mime_type):
            return

        if 'image' in mime_type:
            filename = self.__process_image(data, mime_type)
            filename = self.__postprocessing_manager.image(filename)
            self.__result += self.__result_patterns.image(filename)

        if 'text' in mime_type:
            self.__result += self.__postprocessing_manager.result(data + '\n')

    def process_error(self, name, value, traceback):
        result = ''

        for t in traceback:
            result += str.format('\n{0}', ResultsProcessor.ESCAPE_RE.sub('', t))

        if not self.__allow_errors:
            raise SnippetRuntimeError(result)

        self.__result += self.__postprocessing_manager.result(result)

    def get_result(self):
        return self.__result

    def __process_image(self, image_data, mime_type):
        extension = str.format('.{0}', mime_type.split('/')[1])
        image_data = b64decode(image_data)

        return self.__output_manager.save_image(image_data, extension)
