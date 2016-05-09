from processors.latex_processor import Processor as BaseProcessor


class Processor(BaseProcessor):
    """No escape LaTeX processor"""

    def text(self, text):
        """Raw LaTeX"""
        return text
