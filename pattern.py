import re
from exceptions.processor_errors import ToManySettingOccurencesError, InvalidBoolValueError

GROUP_NAME__CODE = R'code'
GROUP_NAME__CODE_SETTINGS = R'code_settings'
GROUP_NAME__OUTPUT_SETTINGS = R'output_settings'
GROUP_NAME__LANGUAGE = R'lang'
GROUP_NAME__ECHO = R'echo'
GROUP_NAME__OUTPUT = R'out'
GROUP_NAME__CONTEXT = R'ctx'
GROUP_NAME__ID = R'id'

GROUP_NAME__SNIPPET_OUTPUT = R'snippet_output'
GROUP_NAME__SNIPPET_CODE = R'snippet_code'


class Pattern:

    def __init__(self, entry, language, echo, output, context, snippet_id):
        self._entry = re.compile(entry)
        self._language = re.compile(language)
        self._echo = re.compile(echo)
        self._output = re.compile(output)
        self._context = re.compile(context)
        self._id = re.compile(snippet_id)

    def entry(self):
        return self._entry

    @staticmethod
    def extract_setting(string, regex, group_name):
        items = re.finditer(regex, string)
        items = [item for item in items]

        if len(items) == 0:
            return None

        if len(items) != 1:
            raise ToManySettingOccurencesError()

        return items[0].group(group_name)

    @staticmethod
    def convert_to_bool(value):
        if value is None:
            return None

        if value.lower() in ['t', 'true', '1', 'y', 'yes']:
            return True

        if value.lower() in ['f', 'false', '0', 'n', 'no']:
            return False

        raise InvalidBoolValueError

    def language(self, string):
        return Pattern.extract_setting(string, self._language, GROUP_NAME__LANGUAGE)

    def echo(self, string):
        return Pattern.convert_to_bool(Pattern.extract_setting(string, self._echo, GROUP_NAME__ECHO))

    def output(self, string):
        return Pattern.convert_to_bool(Pattern.extract_setting(string, self._output, GROUP_NAME__OUTPUT))

    def context(self, string):
        return Pattern.extract_setting(string, self._context, GROUP_NAME__CONTEXT)

    def id(self, string):
        return Pattern.extract_setting(string, self._id, GROUP_NAME__ID)
