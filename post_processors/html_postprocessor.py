from html import escape


class PostProcessor:

    def image(self, image):
        return image

    def source(self, code):
        code = escape(code)
        return code

    def result(self, text):
        text = escape(text)
        text = text.replace('\n', '<br />\n')

        return text
