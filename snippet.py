
import re
from exceptions.snippet_errors import BeginSnippetSyntaxError, EndSnippetSyntaxError, OutputSnippetSyntaxError

GROUP_NAME__CODE = R'code'

PATTERN_CODE_SNIPPET = str.format(R'(?P<{0}>(?:.|\s)*)', GROUP_NAME__CODE)


class Snippet:

    def __init__(self, data):
        print(self.create_begin_pattern(data))
        self.regex_pattern = ''
        pass

    @staticmethod
    def create_begin_pattern(data):
        patterns = data['patterns']

        if not patterns['settings'] in data['begin']:
            raise BeginSnippetSyntaxError(patterns['settings'])

        # TODO

        return ''

    @staticmethod
    def create_end_pattern(data):
        patterns = data['patterns']

        if patterns['settings'] in data['end']:
            raise EndSnippetSyntaxError(patterns['settings'])

        return re.escape(data['end'])

    @staticmethod
    def create_output_pattern(data):
        patterns = data['patterns']

        if not patterns['settings'] in data['output']:
            raise OutputSnippetSyntaxError(patterns['settings'])

        # TODO
        
        return ''

    def pattern(self):
        return self.regex_pattern
