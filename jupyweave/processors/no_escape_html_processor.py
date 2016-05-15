from jupyweave.processors.html_processor import Processor as BaseProcesor


class Processor(BaseProcesor):
    """No escape processor"""

    def text(self, text):
        """Returns raw html"""
        return text
