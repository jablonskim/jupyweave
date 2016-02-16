
import json
import re
from os.path import splitext


class Settings:

    def __init__(self, config_file):
        self.data = {}

        with open(config_file, 'r') as f:
            self.data = json.load(f)

        self.snippets = self.data['code_snippets']

        # TODO: validate

    def languages(self):
        return self.data['markup_languages']

    def languages_by_extension(self, extension):
        languages = []

        for lang, exts in self.data['extensions'].items():
            if extension in exts:
                languages.append(lang)

        if len(languages) == 0:
            languages = self.languages()

        return languages

    def get_output_filename(self, input_file):
        i_base, i_ext = splitext(input_file)

        # TODO: re.sub()

        return ''
