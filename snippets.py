
from snippet import Snippet


class Snippets:

    def __init__(self, snippets):
        self.default_snippet = Snippet(snippets['default'])
        self.languages = {}

        for lang, snippet in snippets.items():
            if lang != 'default':
                self.languages[lang] = Snippet(snippet)
