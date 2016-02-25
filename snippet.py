
import re
from exceptions.snippet_errors import BeginSnippetSyntaxError, EndSnippetSyntaxError, OutputSnippetSyntaxError, \
    SettingSnippetSyntaxError
from pattern import Pattern

from pattern import GROUP_NAME__CODE, GROUP_NAME__CODE_SETTINGS, GROUP_NAME__OUTPUT_SETTINGS, \
    GROUP_NAME__SNIPPET_CODE, GROUP_NAME__SNIPPET_OUTPUT

PATTERN_CODE_SNIPPET = str.format(R'(?P<{0}>(?:.|\s)*?)', GROUP_NAME__CODE)
PATTERN_CODE_SETTINGS = str.format(R'(?P<{0}>(?:.|\s)*?)', GROUP_NAME__CODE_SETTINGS)
PATTERN_OUTPUT_SETTINGS = str.format(R'(?P<{0}>(?:.|\s)*?)', GROUP_NAME__OUTPUT_SETTINGS)


class Snippet:

    def __init__(self, data):
        begin_pattern = Snippet.create_begin_pattern(data)
        end_pattern = Snippet.create_end_pattern(data)
        output_pattern = Snippet.create_output_pattern(data)

        code_snippet = str.format(R'{0}{1}{2}', begin_pattern, PATTERN_CODE_SNIPPET, end_pattern)
        code_snippet = str.format(R'(?P<{0}>{1})', GROUP_NAME__SNIPPET_CODE, code_snippet)
        output_snippet = str.format(R'(?P<{0}>{1})', GROUP_NAME__SNIPPET_OUTPUT, output_pattern)

        entry_regex = str.format(R'(?:{0})|(?:{1})', code_snippet, output_snippet)

        self.regex_patterns = Pattern(entry_regex)

    @staticmethod
    def create_setting_regex(data, name, group_name):
        setting_pattern = data['patterns'][name]
        setting_regex = data['settings'][name]

        if setting_pattern not in setting_regex:
            raise SettingSnippetSyntaxError(name, setting_pattern)

        print(setting_pattern)
        # TODO

        return setting_regex

    @staticmethod
    def create_begin_pattern(data):
        patterns = data['patterns']
        settings_pattern = patterns['settings']

        if settings_pattern not in data['begin']:
            raise BeginSnippetSyntaxError(settings_pattern)

        settings_pattern = re.escape(re.escape(settings_pattern))

        snippet_pattern = re.escape(data['begin'])
        snippet_pattern = re.sub(settings_pattern, PATTERN_CODE_SETTINGS, snippet_pattern, 1)

        return snippet_pattern

    @staticmethod
    def create_end_pattern(data):
        patterns = data['patterns']

        if patterns['settings'] in data['end']:
            raise EndSnippetSyntaxError(patterns['settings'])

        return re.escape(data['end'])

    @staticmethod
    def create_output_pattern(data):
        patterns = data['patterns']
        settings_pattern = patterns['settings']

        if settings_pattern not in data['output']:
            raise OutputSnippetSyntaxError(settings_pattern)

        settings_pattern = re.escape(re.escape(settings_pattern))

        snippet_pattern = re.escape(data['output'])
        snippet_pattern = re.sub(settings_pattern, PATTERN_OUTPUT_SETTINGS, snippet_pattern, 1)

        return snippet_pattern

    def pattern(self):
        return self.regex_patterns
