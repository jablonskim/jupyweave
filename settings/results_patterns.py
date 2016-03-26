from settings.results_pattern import ResultsPattern


class ResultsPatterns:

    def __init__(self, settings_data):
        self.__patterns = ResultsPatterns.__parse_patterns(settings_data)
        self.__empty_pattern = ResultsPattern(None)

    def patterns(self, language):
        try:
            return self.__patterns[language]
        except KeyError:
            return self.__empty_pattern

    @staticmethod
    def __parse_patterns(data):
        patterns = {}

        for key, value in data.items():
            patterns[key] = ResultsPattern(value)

        return patterns
