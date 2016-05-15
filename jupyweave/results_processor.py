import re
from base64 import b64decode

from .exceptions.processor_errors import SnippetRuntimeError


class ResultsProcessor:
    """Processes results of code execution"""

    ANSI_ESCAPE_SEQ_RE = r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]'
    ESCAPE_RE = re.compile(ANSI_ESCAPE_SEQ_RE)

    def __init__(self, allow_errors, output_types, processing_manager):
        """Initialization"""
        self.__allow_errors = allow_errors
        self.__output_types = output_types
        self.__processing_manager = processing_manager

        self.__result = ''

    def process_stream(self, text, stream_type):
        """Processes output stream (stdin/stderr)"""
        if self.__output_types.is_enabled(stream_type):
            self.__result += self.__processing_manager.text(text)

    def process_data(self, mime_type, data):
        """Processes text/plain and images"""
        if not self.__output_types.is_enabled(mime_type):
            return

        if mime_type in ['application/pdf', 'image/png', 'image/gif', 'image/jpeg', 'image/tiff']:
            self.__result += self.__processing_manager.image(b64decode(data), mime_type)
            return

        if mime_type == 'text/plain':
            self.__result += self.__processing_manager.text(data + '\n')
            return

        # raise ProcessingError('Not implemented result\'s mime type: %s' % mime_type)

    def process_error(self, name, value, traceback):
        """Processes errors. Raises if errors not allowed in output"""
        result = ''

        for t in traceback:
            result += str.format('\n{0}', ResultsProcessor.ESCAPE_RE.sub('', t))

        if not self.__allow_errors:
            raise SnippetRuntimeError(result)

        self.__result += self.__processing_manager.text(result)

    def get_result(self):
        """Returns processed results"""
        return self.__result
