from processors.latex_processor import Processor as BaseProcessor


class Processor(BaseProcessor):

    def begin(self):
        """Use pdf for images"""
        self.execute("%matplotlib inline\n")
        self.execute("from IPython.display import set_matplotlib_formats\n")
        self.execute("set_matplotlib_formats('pdf')\n")

        return ''
