
from os.path import splitext
import re
import io
from pattern import GROUP_NAME__SNIPPET_CODE, GROUP_NAME__SNIPPET_OUTPUT, \
    GROUP_NAME__CODE, GROUP_NAME__CODE_SETTINGS, GROUP_NAME__OUTPUT_SETTINGS
from exceptions.processor_errors import InvalidSnippetError


class Processor:

    def __init__(self, filename, settings):
        self.settings = settings
        self.document_file_name = filename

        self.language = self.get_language_by_extension(self.document_file_name)
        self.pattern = self.settings.pattern(self.language)
        # TODO

    @staticmethod
    def create_processors(filenames, settings):
        processors = []

        for doc in filenames:
            processors.append(Processor(doc, settings))

        return processors

    def get_language_by_extension(self, name):
        extension = splitext(name)[1].strip('.')
        languages = self.settings.languages_by_extension(extension)

        if len(languages) == 1:
            return languages[0]

        if len(languages) == 0:
            return self.ask_for_language(name, self.settings.languages())

        return self.ask_for_language(name, languages)

    @staticmethod
    def ask_for_language(filename, languages):
        print('Cannot determine document \'%s\' type by extension. Select correct type:' % filename)

        for i, lang in enumerate(languages):
            print(str.format('  {0}) -> {1}', i + 1, lang))

        language = None

        while not language:
            dtype = input('Enter type number > ')
            try:
                dtype = int(dtype)
                if 1 <= dtype <= len(languages):
                    language = languages[dtype - 1]
            except ValueError:
                pass

            if not language:
                print('Invalid value')

        return language

    def process_code_sippet(self, code, settings):
        return ''

    def process_output(self, settings):
        return ''

    def process_entry(self, entry):
        if entry.group(GROUP_NAME__SNIPPET_CODE) is not None:
            return self.process_code_sippet(entry.group(GROUP_NAME__CODE), entry.group(GROUP_NAME__CODE_SETTINGS))

        if entry.group(GROUP_NAME__SNIPPET_OUTPUT) is not None:
            return self.process_output(entry.group(GROUP_NAME__OUTPUT_SETTINGS))

        raise InvalidSnippetError()

    def process(self):
        # TODO: file not found?
        with io.open(self.document_file_name, 'r', encoding='utf8') as f:
            data = f.read()

        data = re.sub(self.pattern.entry(), self.process_entry, data)

        with open(self.document_file_name + '_new.html', 'w', encoding='utf8') as f:
            f.write(data)


