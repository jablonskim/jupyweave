import re

from exceptions.snippet_errors import \
    BeginSnippetSyntaxError, \
    EndSnippetSyntaxError, \
    OutputSnippetSyntaxError, \
    SettingSnippetSyntaxError

from settings.pattern import Pattern
from settings.group_names import GroupName


class Snippet:
    """Code snippet settings"""

    PATTERN_CODE_SNIPPET = str.format(R'(?P<{0}>(?:.|\s)*?)', GroupName.CODE)
    PATTERN_CODE_SETTINGS = str.format(R'(?P<{0}>(?:.|\s)*?)', GroupName.CODE_SETTINGS)
    PATTERN_OUTPUT_SETTINGS = str.format(R'(?P<{0}>(?:.|\s)*?)', GroupName.OUTPUT_SETTINGS)

    PATTERN_SETTING = R'(?P<{0}>(?:.|\s)*?)'

    def __init__(self, data):
        """Creates snippet pattern"""
        begin_pattern = Snippet.__create_begin_pattern(data)        # Pattern for snippet beginning tag
        end_pattern = Snippet.__create_end_pattern(data)            # Pattern for snippet ending tag
        output_pattern = Snippet.__create_output_pattern(data)      # Pattern for output snippet

        # Pattern for full code snippet
        code_snippet = str.format(R'{0}{1}{2}', begin_pattern, Snippet.PATTERN_CODE_SNIPPET, end_pattern)

        # Pattern for full code snippet with regex group
        code_snippet = str.format(R'(?P<{0}>{1})', GroupName.CODE_SNIPPET, code_snippet)

        # Pattern for full output snippet with regex group
        output_snippet = str.format(R'(?P<{0}>{1})', GroupName.OUTPUT_SNIPPET, output_pattern)

        # Pattern for full entry (code or output snippet)
        entry_regex = str.format(R'(?:{0})|(?:{1})', code_snippet, output_snippet)

        # Patterns for snippets settings
        language_regex = self.create_setting_regex(data, 'language', GroupName.LANGUAGE)
        echo_regex = self.create_setting_regex(data, 'echo', GroupName.ECHO)
        output_regex = self.create_setting_regex(data, 'output', GroupName.OUTPUT)
        context_regex = self.create_setting_regex(data, 'context', GroupName.CONTEXT)
        id_regex = self.create_setting_regex(data, 'snippet_id', GroupName.ID)

        self.__regex_patterns = Pattern(entry_regex, language_regex, echo_regex, output_regex, context_regex, id_regex)

    def pattern(self):
        """Returns patterns"""
        return self.__regex_patterns

    @staticmethod
    def create_setting_regex(data, name, group_name):
        """Creates regex pattern for snippet setting name"""
        setting_pattern = data['patterns'][name]
        setting_regex = data['settings'][name]

        if setting_pattern not in setting_regex:
            raise SettingSnippetSyntaxError(name, setting_pattern)

        setting_pattern = re.escape(re.escape(setting_pattern))
        setting_regex = re.escape(setting_regex)

        setting_group = str.format(Snippet.PATTERN_SETTING, group_name)
        setting_regex = re.sub(setting_pattern, setting_group, setting_regex, 1)

        return setting_regex

    @staticmethod
    def __create_begin_pattern(data):
        """Creates pattern for snippet beginning tag"""
        patterns = data['patterns']
        settings_pattern = patterns['settings']

        if settings_pattern not in data['begin']:
            raise BeginSnippetSyntaxError(settings_pattern)

        settings_pattern = re.escape(re.escape(settings_pattern))

        snippet_pattern = re.escape(data['begin'])
        snippet_pattern = re.sub(settings_pattern, Snippet.PATTERN_CODE_SETTINGS, snippet_pattern, 1)

        return snippet_pattern

    @staticmethod
    def __create_end_pattern(data):
        """Creates pattern for snippet ending tag"""
        patterns = data['patterns']

        if patterns['settings'] in data['end']:
            raise EndSnippetSyntaxError(patterns['settings'])

        return re.escape(data['end'])

    @staticmethod
    def __create_output_pattern(data):
        """Creates pattern for output snippet"""
        patterns = data['patterns']
        settings_pattern = patterns['settings']

        if settings_pattern not in data['output']:
            raise OutputSnippetSyntaxError(settings_pattern)

        settings_pattern = re.escape(re.escape(settings_pattern))

        snippet_pattern = re.escape(data['output'])
        snippet_pattern = re.sub(settings_pattern, Snippet.PATTERN_OUTPUT_SETTINGS, snippet_pattern, 1)

        return snippet_pattern