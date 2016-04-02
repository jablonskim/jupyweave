from processors.html_processor import Processor as BaseProcessor
from pygments.lexers import get_lexer_by_name
from pygments import highlight
from pygments.formatters import HtmlFormatter


class Processor(BaseProcessor):

    def source(self, code):
        lexer = get_lexer_by_name(self.language.replace(' ', ''))
        formatter = HtmlFormatter(noclasses=True, linenos='table')
        return highlight(code, lexer, formatter)
