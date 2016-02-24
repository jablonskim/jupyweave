
from snippet import Snippet
from exceptions.snippet_errors import SnippetSyntaxError


class Snippets:

    def __init__(self, snippets):
        self.default_snippet = Snippets.create_snippet_for_language('default', snippets['default'])

        self.languages = {}

        for lang, snippet in snippets.items():
            if lang != 'default':
                self.languages[lang] = Snippets.create_snippet_for_language(lang, snippet)

    @staticmethod
    def create_snippet_for_language(lang, snippet_data):
        try:
            return Snippet(snippet_data)
        except SnippetSyntaxError as e:
            e.set_language(lang)
            raise e

    def pattern(self, language):
        try:
            return self.languages[language].pattern()
        except KeyError:
            return self.default_snippet.pattern()
