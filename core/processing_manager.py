from importlib import import_module


class ProcessingManager:

    def __init__(self, document_language, snippet_language, user_processor_name, output_manager):
        package_name = str.format('processors.{0}_processor', document_language.lower())

        if user_processor_name is not None:
            package_name = str.format('processors.{0}_{1}_processor', user_processor_name, document_language.lower())
            module = import_module(package_name)
            self.__processor = getattr(module, 'Processor')(output_manager, snippet_language)
        else:
            try:
                module = import_module(package_name)
                self.__processor = getattr(module, 'Processor')(output_manager, snippet_language)
            except (ImportError, AttributeError):
                module = import_module('processors.processor')
                self.__processor = getattr(module, 'Processor')(output_manager, snippet_language)

    def code(self, code):
        return self.__processor.source(code)

    def text(self, text):
        return self.__processor.text(text)

    def image(self, data, mime_type):
        return self.__processor.image(data, mime_type)

    def result(self, text):
        return self.__processor.result(text)

    def execute_before(self):
        return self.__processor.begin()

    def execute_after(self):
        return self.__processor.end()
