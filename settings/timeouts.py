from exceptions.settings_errors import InvalidConfigurationError


class Timeouts:

    def __init__(self, timeouts):
        try:
            self.__default_timeout = timeouts['default']
            if type(self.__default_timeout) != int:
                raise InvalidConfigurationError('Timeouts must be numbers')
        except KeyError:
            raise InvalidConfigurationError('No default timeout defined')

        try:
            self.__timeouts = timeouts['languages']
            for _, t in self.__timeouts.items():
                if type(t) != int:
                    raise InvalidConfigurationError('Timeouts must be numbers')
        except KeyError:
            self.__timeouts = {}

    def timeout(self, language):
        try:
            return self.__timeouts[language]
        except KeyError:
            return self.__default_timeout
