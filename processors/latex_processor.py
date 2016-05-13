from processors.processor import Processor as BaseProcessor
from settings.align_types import ImageAlignType
import re


class Processor(BaseProcessor):
    """LaTeX Processor. Base class for user-defined LaTeX processors"""

    def source(self, code):
        """Processing source code"""
        return '\\begin{lstlisting}\n' + code + '\n\\end{lstlisting}'

    def text(self, text):
        """Processing text results of code execution"""
        text = self.tex_escape(text)
        return text.replace('\n', '\\\\\n')

    def image(self, data, mime_type):
        """Processing image"""
        url = super(Processor, self).image(data, mime_type)
        url = url.replace('\\', '/')
        # TODO: pdf? label? caption? -> settings?
        width = "width=\\linewidth"
        if self.image_width is not None:
            width = "width=" + str(self.image_width) + "px"

        height = ""
        if self.image_height is not None:
            height = ",height=" + str(self.image_height) + "px"

        align_begin = ""
        align_end = ""

        if self.image_align != ImageAlignType.Default:
            if self.image_align == ImageAlignType.Left:
                align_begin = "\\begin{flushleft}\n"
                align_end = "\\end{flushleft}\n"

            if self.image_align == ImageAlignType.Right:
                align_begin = "\\begin{flushright}\n"
                align_end = "\\end{flushright}\n"

            if self.image_align == ImageAlignType.Center:
                align_begin = "\\begin{center}\n"
                align_end = "\\end{center}\n"

        return '\\begin{figure}\n%s\\includegraphics[%s%s]{%s}\n%s\\end{figure}\n' % \
               (align_begin, width, height, url, align_end)

    def result(self, result):
        """Processing whole result"""
        return result

    @staticmethod
    def tex_escape(text):
        """
            :param text: a plain text message
            :return: the message escaped to appear correctly in LaTeX
        """
        conv = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
            '<': r'\textless ',
            '>': r'\textgreater ',
        }
        regex = re.compile(
            '|'.join(re.escape(key) for key in sorted(conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)
