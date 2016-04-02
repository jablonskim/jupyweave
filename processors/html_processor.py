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

    def image(self, data, mime_type):
        url = super(Processor, self).image(data, mime_type)
        return '<br /><img src="%s"><br />\n' % url
