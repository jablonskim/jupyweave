import json

from exceptions.settings_errors import InvalidConfigurationError
from settings.snippets import Snippets
from settings.timeouts import Timeouts
from settings.results_patterns import ResultsPatterns


class Settings:
    """Application settings"""

    def __init__(self, config_file):
        """Parses settings from config_file"""
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidConfigurationError('Invalid configuration format: %s' % e)
        except FileNotFoundError:
            raise InvalidConfigurationError('Configuration file %s not found.' % config_file)

        try:
            self.__markup_languages = self.__parse_markup_languages(data['markup_languages'])
            self.__extensions = self.__parse_extensions(data['extensions'])
            self.__snippets = Snippets(data['code_snippets'])
            self.__timeouts = Timeouts(data['execution_timeouts'])
            self.__results_patterns = ResultsPatterns(data['execution_results'])
        except KeyError as e:
            raise InvalidConfigurationError('Required configuration key %s was not found' % e)

    def languages(self):
        """Returns all defined markup languages"""
        return self.__markup_languages

    def languages_by_extension(self, extension):
        """Returns languages list which match speciffied extension (or all if no match)"""
        languages = []

        for lang, exts in self.__extensions.items():
            if extension in exts:
                languages.append(lang)

        if len(languages) == 0:
            languages = self.languages()

        return languages

    def pattern(self, language):
        """Returns pattern for specified language (or default)"""
        return self.__snippets.pattern(language)

    def timeout(self, language):
        """Returns timeout for speciffic language (in seconds)"""
        return self.__timeouts.timeout(language) / 1000.0

    def result_pattern(self, language):
        """Returns results patterns"""
        return self.__results_patterns.patterns(language)

    def __parse_markup_languages(self, markup_languages):
        if type(markup_languages) != list:
            raise InvalidConfigurationError('Key \'markup_languages\' must be a list of strings')

        for l in markup_languages:
            if type(l) != str:
                raise InvalidConfigurationError('Key \'markup_languages\' must be a list of strings')

        return markup_languages

    def __parse_extensions(self, extensions):
        if type(extensions) != dict:
            raise InvalidConfigurationError("Key 'extensions' must be a dictionary")

        return extensions
