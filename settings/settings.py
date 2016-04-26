import json

from exceptions.settings_errors import InvalidConfigurationError
from settings.snippets import Snippets
from settings.timeouts import Timeouts
from settings.output_settings import OutputSettings
from settings.validator import Validator


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

        Validator.check_keys(data, ['markup_languages', 'extensions', 'output', 'execution_timeouts', 'code_snippets'], 'Settings')

        try:
            self.__markup_languages = Settings.__parse_markup_languages(data['markup_languages'])
            self.__extensions = Settings.__parse_extensions(data['extensions'])
            self.__snippets = Snippets(data['code_snippets'])
            self.__timeouts = Timeouts(data['execution_timeouts'])
            self.__output_settings = OutputSettings(data['output'])
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

    def output_settings(self):
        """Returns output settings"""
        return self.__output_settings

    @staticmethod
    def __parse_markup_languages(markup_languages):
        """Parses markup languages types"""
        if type(markup_languages) != list:
            raise InvalidConfigurationError('Key \'markup_languages\' must be a list of strings')

        for l in markup_languages:
            if type(l) != str:
                raise InvalidConfigurationError('Key \'markup_languages\' must be a list of strings')

        return markup_languages

    @staticmethod
    def __parse_extensions(extensions):
        """Parses extensions"""
        if type(extensions) != dict:
            raise InvalidConfigurationError("Key 'extensions' must be a dictionary")

        return extensions
