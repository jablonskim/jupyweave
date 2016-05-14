from processors.html_processor import Processor as BaseProcessor
from html import escape


class Processor(BaseProcessor):

    def result(self, result):
        return '<pre>' + escape(result) + '</pre>'

    def text(self, text):
        return text
