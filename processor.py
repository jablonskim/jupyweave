import io
import re
from os.path import splitext

from exceptions.processor_errors import InvalidSnippetError, RequiredSettingNotFoundError
from kernel_engine import KernelEngine
from result_manager import ResultManager
from settings.pattern import GROUP_NAME__SNIPPET_CODE, GROUP_NAME__SNIPPET_OUTPUT, \
    GROUP_NAME__CODE, GROUP_NAME__CODE_SETTINGS, GROUP_NAME__OUTPUT_SETTINGS


class Processor:

    def __init__(self, filename, settings):
        self.settings = settings
        self.document_file_name = filename

        self.language = self.get_language_by_extension(self.document_file_name)
        self.pattern = self.settings.pattern(self.language)
        self.engine = KernelEngine()
        self.results = ResultManager()

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
        language = self.pattern.language(settings)
        if language is None:
            raise RequiredSettingNotFoundError()

        is_echo = self.pattern.echo(settings)
        if is_echo is None:
            is_echo = True

        is_output = self.pattern.output(settings)
        context = self.pattern.context(settings)
        snippet_id = self.pattern.id(settings)

        if is_output is None:
            is_output = False if snippet_id is not None else True

        result = self.engine.execute(language, code, context)

        output = ''

        if snippet_id is not None:
            self.results.store(snippet_id, result)

        if is_echo is not None:
            output = code

        if is_output is not None:
            if len(output) > 0:
                output += '\n'
            output += result

        return output

    def process_output(self, settings):
        snippet_id = self.pattern.id(settings)

        if snippet_id is None:
            raise RequiredSettingNotFoundError()

        return self.results.get(snippet_id)

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

        # TODO: error?
        with open(self.document_file_name + '_new.html', 'w', encoding='utf8') as f:
            f.write(data)

    def get_filename(self):
        return self.document_file_name
