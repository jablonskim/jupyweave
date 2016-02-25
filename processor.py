
from os.path import splitext
import re
import io


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

    def process_code_sippet(self):
        pass

    def process_output(self):
        pass

    def process_entry(self, entry):
        print('a')
        return ''

    def process(self):
        # TODO: file not found?
        with io.open(self.document_file_name, 'r', encoding='utf8') as f:
            data = f.read()

        #print(data)

        data = re.sub(self.pattern.entry(), self.process_entry, data)

        with open(self.document_file_name + '_new.html', 'w', encoding='utf8') as f:
            f.write(data)


