
class Processor:

    def __init__(self, output_manager):
        self.__output_manager = output_manager

    def save_to_file(self, data, extension):
        return self.__output_manager.save_data(data, extension)

    def begin(self):
        return ''

    def end(self):
        return ''

    def source(self, code):
        return code

    def text(self, text):
        return text

    def image(self, data, mime_type):
        if '/' in mime_type:
            extension = str.format('.{0}', mime_type.split('/')[-1])
            return self.save_to_file(data, extension)

        return ''

    def result(self, result):
        return result
