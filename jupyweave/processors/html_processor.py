from html import escape

from jupyweave.processors.processor import Processor as BaseProcessor
from jupyweave.settings.align_types import ImageAlignType


class Processor(BaseProcessor):
    """HTML Processor. Base class for user-defined HTML processors"""

    def source(self, code):
        """Processing source code"""
        return '<pre>' + escape(code) + '</pre>'

    def text(self, text):
        """Processing text results of code execution"""
        text = escape(text)
        text = text.replace('\n', '<br>\n')

        return text

    def result(self, result):
        """Processing whole result"""
        return '<p>' + result + '</p>'

    def image(self, data, mime_type):
        """Processing image"""
        url = super(Processor, self).image(data, mime_type)

        size = ""

        if self.image_width is not None or self.image_height is not None:
            size = ' style="'

            if self.image_width is not None:
                size += "width: " + str(self.image_width) + "px;"

            if self.image_height is not None:
                size += "height: " + str(self.image_height) + "px;"

            size += '" '

        align = ""

        if self.image_align != ImageAlignType.Default:
            align = ' style="text-align: '

            if self.image_align == ImageAlignType.Left:
                align += 'left'

            if self.image_align == ImageAlignType.Right:
                align += 'right'

            if self.image_align == ImageAlignType.Center:
                align += 'center'

            align += ';"'

        return str.format('<p{2}><img src="{0}"{1}></p>\n', url, size, align)
