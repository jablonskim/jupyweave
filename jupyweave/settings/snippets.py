from jupyweave.exceptions.settings_errors import InvalidConfigurationError
from jupyweave.exceptions.snippet_errors import SnippetSyntaxError
from .snippet import Snippet


class Snippets:
    """Code snippets settings"""

    def __init__(self, snippets):
        """Parses snippets settings"""
        try:
            self.__default_snippet = Snippets.__create_snippet_for_language('default', snippets['default'])
        except KeyError:
            self.__default_snippet = None

        self.__languages = {}

        for lang, snippet in snippets.items():
            if lang != 'default':
                self.__languages[lang] = Snippets.__create_snippet_for_language(lang, snippet)

    def pattern(self, language):
        """Returns pattern for specific language (or default)"""
        try:
            return self.__languages[language].pattern()
        except KeyError:
            if self.__default_snippet is not None:
                return self.__default_snippet.pattern()
            else:
                raise InvalidConfigurationError("Snippets for '%s' not found and no defaults defined." % language)

    @staticmethod
    def __create_snippet_for_language(lang, snippet_data):
        """Creates Snippet for language. Sets language and rethrows exception in case od errors"""
        try:
            return Snippet(snippet_data)
        except SnippetSyntaxError as e:
            e.set_language(lang)
            raise e
