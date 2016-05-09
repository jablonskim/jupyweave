from processors.markdown_processor import Processor as BaseProcessor


class Processor(BaseProcessor):
    """No escape processor"""

    def text(self, text):
        """Raw markdown"""
        return text
