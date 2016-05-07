from processors.processor import Processor as BaseProcessor
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
        return '\\begin{figure}\\includegraphics[width=\\linewidth]{%s}\\end{figure}' % url

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
