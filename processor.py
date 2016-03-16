import io
import re
from os.path import splitext

from exceptions.processor_errors import InvalidSnippetError, RequiredSettingNotFoundError
from kernel_engine import KernelEngine
from result_manager import ResultManager
from settings.group_names import GroupName


class Processor:
    """Document processor"""

    def __init__(self, filename, settings):
        """Initializes processor for document file"""
        self.__settings = settings
        self.__document_file_name = filename

        self.__language = self.__get_language_by_extension(self.__document_file_name)
        self.__pattern = self.__settings.pattern(self.__language)
        self.__engine = KernelEngine(self.__settings)
        self.__results = ResultManager()

    @staticmethod
    def create_processors(filenames, settings):
        """Creates processors for documents"""
        processors = []

        for doc in filenames:
            processors.append(Processor(doc, settings))

        return processors

    def process(self):
        """Processes single document"""
        with io.open(self.__document_file_name, 'r', encoding='utf8') as f:
            data = f.read()

        data = re.sub(self.__pattern.entry(), self.__process_entry, data)

        with open(self.__document_file_name + '_new.html', 'w', encoding='utf8') as f:
            f.write(data)

    def get_filename(self):
        """Returns processed file name"""
        return self.__document_file_name

    def __get_language_by_extension(self, name):
        extension = splitext(name)[1].strip('.')
        languages = self.__settings.languages_by_extension(extension)

        if len(languages) == 1:
            return languages[0]

        if len(languages) == 0:
            return self.__ask_for_language(name, self.__settings.languages())

        return self.__ask_for_language(name, languages)

    @staticmethod
    def __ask_for_language(filename, languages):
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

    def __process_entry(self, entry):
        if entry.group(GroupName.CODE_SNIPPET) is not None:
            return self.__process_code_sippet(entry.group(GroupName.CODE), entry.group(GroupName.CODE_SETTINGS))

        if entry.group(GroupName.OUTPUT_SNIPPET) is not None:
            return self.__process_output(entry.group(GroupName.OUTPUT_SETTINGS))

        raise InvalidSnippetError()

    def __process_code_sippet(self, code, settings):
        language = self.__pattern.language(settings)
        if language is None:
            raise RequiredSettingNotFoundError()

        is_echo = self.__pattern.echo(settings)
        if is_echo is None:
            is_echo = True

        is_output = self.__pattern.output(settings)
        context = self.__pattern.context(settings)
        snippet_id = self.__pattern.id(settings)
        timeout = self.__pattern.timeout(settings)

        if is_output is None:
            is_output = False if snippet_id is not None else True

        result = self.__engine.execute(language, code, context, timeout)

        output = ''

        if snippet_id is not None:
            self.__results.store(snippet_id, result)

        if is_echo is not None:
            output = code

        if is_output is not None:
            if len(output) > 0:
                output += '\n'
            output += result

        return output

    def __process_output(self, settings):
        snippet_id = self.__pattern.id(settings)

        if snippet_id is None:
            raise RequiredSettingNotFoundError()

        return self.__results.get(snippet_id)
