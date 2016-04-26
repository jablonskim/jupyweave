from processors.processor import Processor as BaseProcessor


class Processor(BaseProcessor):
    """Markdown Processor. Base class for user-defined Markdown processors"""

    def source(self, code):
        """Processing source code"""
        return '```\n' + code + '\n```\n'

    def text(self, text):
        """Processing text results of code execution"""
        return text.replace('\n', '  \n')

    def image(self, data, mime_type):
        """Processing image"""
        url = super(Processor, self).image(data, mime_type)
        return '\n![](%s)  \n' % url

    def result(self, result):
        """Processing whole result"""
        return '\n\n' + result + '\n\n'
