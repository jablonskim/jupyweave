import re

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

    def __init__(self, entry):
        self._entry = re.compile(entry)

    def entry(self):
        return self._entry

    def language(self):
        pass
