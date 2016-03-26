from exceptions.settings_errors import InvalidConfigurationError


class ResultsPattern:

    def __init__(self, settings_data):
        self.__image = None
        self.__image_pattern = ''
        self.__result = None
        self.__result_pattern = ''
        self.__source = None
        self.__source_pattern = ''

        if settings_data is not None:
            self.__parse_settings(settings_data)

    def image(self, src_url):
        if self.__image is None:
            return src_url

        return self.__image.replace(self.__image_pattern, src_url)

    def source(self, text):
        if self.__source is None:
            return text

        return self.__source.replace(self.__source_pattern, text)

    def result(self, text):
        if self.__result is None:
            return text

        return self.__result.replace(self.__result_pattern, text)

    def __parse_settings(self, settings_data):
        self.__image, self.__image_pattern = ResultsPattern.__extract_setting(settings_data, 'image')
        self.__source, self.__source_pattern = ResultsPattern.__extract_setting(settings_data, 'source')
        self.__result, self.__result_pattern = ResultsPattern.__extract_setting(settings_data, 'result')

    @staticmethod
    def __extract_setting(data, name):
        try:
            setting = data[name]

            try:
                pattern = data['patterns'][name]
                return setting, pattern
            except KeyError:
                raise InvalidConfigurationError('Cannot found pattern \'%s\' in \'execution_results\' setting' % name)

        except KeyError:
            return None, None
