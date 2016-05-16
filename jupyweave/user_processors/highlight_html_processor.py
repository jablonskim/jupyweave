from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from html_processor import Processor as BaseProcessor


class Processor(BaseProcessor):
    """Example of user-defined processof for source highlighting"""

    def source(self, code):
        """Source code highlighting for any language"""
        lexer = get_lexer_by_name(self.language.replace(' ', ''))
        formatter = HtmlFormatter(noclasses=True, linenos='table')
        return highlight(code, lexer, formatter)
