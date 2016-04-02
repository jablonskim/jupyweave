from processors.processor import Processor as BaseProcessor
from html import escape


class Processor(BaseProcessor):

    def source(self, code):
        return '<pre>' + escape(code) + '</pre>'

    def text(self, text):
        text = escape(text)
        text = text.replace('\n', '<br />\n')

        return text

    def result(self, result):
        return '<p>' + result + '</p>'
