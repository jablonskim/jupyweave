from jupyweave.processors.latex_processor import Processor as BaseProcessor


class Processor(BaseProcessor):

    def begin(self):
        """Use pdf for images"""
        self.execute("options(jupyter.plot_mimetypes = 'application/pdf')")

        return ''
