from importlib import import_module


class ProcessingManager:

    def __init__(self, document_language, user_processor_name):
        package_name = str.format('processors.{0}_processor', document_language.lower())

        if user_processor_name is not None:
            package_name = str.format('processors.{0}_{1}_processor', user_processor_name, document_language.lower())
            module = import_module(package_name)
            self.__processor = getattr(module, 'Processor')()
        else:
            try:
                module = import_module(package_name)
                self.__processor = getattr(module, 'Processor')()
            except (ImportError, AttributeError):
                module = import_module('processors.processor')
                self.__processor = getattr(module, 'Processor')()

    def code(self, code):
        return self.__processor.source(code)

    def text(self, text):
        return self.__processor.text(text)

    def image(self, data, type):
        # TODO
        return ''

    def result(self, text):
        return self.__processor.result(text)

    def execute_before(self):
        return self.__processor.begin()

    def execute_after(self):
        return self.__processor.end()
