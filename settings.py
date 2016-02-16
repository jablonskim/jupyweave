
import json


class Settings:

    def __init__(self, config_file):
        self.data = {}

        with open(config_file, 'r') as f:
            self.data = json.load(f)

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
