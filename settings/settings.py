import json

from exceptions.settings_errors import InvalidConfigurationError
from settings.snippets import Snippets
from settings.timeouts import Timeouts


class Settings:

    def __init__(self, config_file):
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
        except KeyError as e:
            raise InvalidConfigurationError('Required configuration key %s was not found' % e)

    def languages(self):
        return self.__markup_languages

    def languages_by_extension(self, extension):
        languages = []

        for lang, exts in self.__extensions.items():
            if extension in exts:
                languages.append(lang)

        if len(languages) == 0:
            languages = self.languages()

        return languages

    def pattern(self, language):
        return self.__snippets.pattern(language)

    def timeout(self, language):
        return self.__timeouts.timeout(language)

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
