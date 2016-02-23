
import re

GROUP_NAME__CODE = R'code'

PATTERN_CODE_SNIPPET = str.format(R'(?P<{0}>(?:.|\s)*)', GROUP_NAME__CODE)


class Snippet:

    def __init__(self, data):

        print(self.create_begin_pattern(data))
        self.regex_pattern = ''
        pass

    @staticmethod
    def create_begin_pattern(data):
        return

    @staticmethod
    def create_end_pattern(data):
        # TODO: throw if settings/patterns in 'end'
        return re.escape(data['end'])

    @staticmethod
    def create_output_pattern(data):
        # TODO
        pass

    def pattern(self):
        return self.regex_pattern
