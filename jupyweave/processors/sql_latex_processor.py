from jupyweave.processors.latex_processor import Processor as BaseProcessor


class Processor(BaseProcessor):

    def result(self, result):
        result = result.replace(' ', '~')
        return "{\\fontfamily{qcr}\\selectfont\n" + result + "\n}"
