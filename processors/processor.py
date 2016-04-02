
class Processor:

    def begin(self):
        return ''

    def end(self):
        return ''

    def source(self, code):
        return code

    def text(self, text):
        return text

    def image(self, data):
        return ''

    def result(self, result):
        return result
