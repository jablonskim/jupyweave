from processors.processor import Processor as BaseProcessor
from html import escape


class Processor(BaseProcessor):
    """HTML Processor. Base class for user-defined HTML processors"""

    def source(self, code):
        """Processing source code"""
        return '<pre>' + escape(code) + '</pre>'

    def text(self, text):
        """Processing text results of code execution"""
        text = escape(text)
        text = text.replace('\n', '<br />\n')

        return text

    def result(self, result):
        """Processing whole result"""
        return '<p>' + result + '</p>'

    def image(self, data, mime_type):
        """Processing image"""
        url = super(Processor, self).image(data, mime_type)
        return '<br /><img src="%s"><br />\n' % url
