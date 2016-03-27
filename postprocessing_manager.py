from importlib import import_module


class PostprocessingManager:

    def __init__(self, document_language):
        package_name = str.format('post_processors.{0}_postprocessor', document_language.lower())

        try:
            module = import_module(package_name)
            self.__postprocessor = getattr(module, 'PostProcessor')()
        except (ImportError, AttributeError):
            self.__postprocessor = None

    def image(self, image):
        if self.__postprocessor is None:
            return image

        try:
            return self.__postprocessor.image(image)
        except AttributeError:
            return image

    def source(self, code):
        if self.__postprocessor is None:
            return code

        try:
            return self.__postprocessor.source(code)
        except AttributeError:
            return code

    def result(self, text):
        if self.__postprocessor is None:
            return text

        try:
            return self.__postprocessor.result(text)
        except AttributeError:
            return text
