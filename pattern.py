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

    def __init__(self, entry, language, echo, output, context, snippet_id):
        self._entry = re.compile(entry)
        self._language = re.compile(language)
        self._echo = re.compile(echo)
        self._output = re.compile(output)
        self._context = re.compile(context)
        self._id = re.compile(snippet_id)

    def entry(self):
        return self._entry

    def language(self):
        return self._language

    def echo(self):
        return self._echo

    def output(self):
        return self._output

    def context(self):
        return self._context

    def id(self):
        return self._id
