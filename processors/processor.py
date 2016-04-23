
class Processor:
    """Base class for language-speciffic and user-defined processors"""

    def __init__(self, output_manager, executor, snippet_language, snippet_settings):
        """Initialization"""
        self.__output_manager = output_manager
        self.__executor = executor
        self.settings = snippet_settings
        self.language = snippet_language

    def execute(self, code):
        """Executes code. May be called by another method of Processor"""
        return self.__executor(code, self)

    def save_to_file(self, data, extension):
        """Saves data to file with speciffic extension."""
        return self.__output_manager.save_data(data, extension)

    def begin(self):
        """Called before snippet execution. Returns text, which will be pasted in the beginning of the result."""
        return ''

    def end(self):
        """Called after snippet execution. Returns text, which will be pasted in the end of the result."""
        return ''

    def source(self, code):
        """Processing source code (for displaying)"""
        return code

    def text(self, text):
        """Processing rext result of snippet execution. May be called multiple times per snippet"""
        return text

    def image(self, data, mime_type):
        """Processing image data. Returns url"""
        if '/' in mime_type:
            extension = str.format('.{0}', mime_type.split('/')[-1])
            return self.save_to_file(data, extension)

        return ''

    def result(self, result):
        """Processing result of execution of whole snippet"""
        return result
