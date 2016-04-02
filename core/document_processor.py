import io
import re
from os.path import splitext

from exceptions.processor_errors import InvalidSnippetError, RequiredSettingNotFoundError
from core.kernel_engine import KernelEngine
from core.output_manager import OutputManager
from core.result_manager import ResultManager
from core.processing_manager import ProcessingManager
from settings.group_names import GroupName


class DocumentProcessor:
    """Document processor"""

    def __init__(self, filename, settings):
        """Initializes processor for document file"""
        self.__settings = settings
        self.__document_file_name = filename

        self.__document_language = self.__get_language_by_extension(self.__document_file_name)
        self.__pattern = self.__settings.pattern(self.__document_language)
        self.__output_manager = OutputManager(settings.output_settings(), self.__document_file_name)
        self.__engine = KernelEngine(self.__settings, self.__document_language)
        self.__results = ResultManager()

        self.__current_snippet_number = 0
        self.__number_of_snippets = 0

    @staticmethod
    def create_processors(filenames, settings):
        """Creates processors for documents"""
        processors = []

        for doc in filenames:
            processors.append(DocumentProcessor(doc, settings))

        return processors

    def process(self):
        """Processes single document"""
        with io.open(self.__document_file_name, 'r', encoding='utf8') as f:
            data = f.read()

        self.__current_snippet_number = 0
        self.__number_of_snippets = len(re.findall(self.__pattern.entry(), data))

        data = re.sub(self.__pattern.entry(), self.__process_entry, data)

        self.__output_manager.save_document(data)

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
        self.__current_snippet_number += 1
        print(str.format('\tProcessing snippet {0}/{1}...', self.__current_snippet_number, self.__number_of_snippets), end=' ', flush=True)

        result = None

        if entry.group(GroupName.CODE_SNIPPET) is not None:
            result = self.__process_code_sippet(entry.group(GroupName.CODE), entry.group(GroupName.CODE_SETTINGS))

        if entry.group(GroupName.OUTPUT_SNIPPET) is not None:
            result = self.__process_output(entry.group(GroupName.OUTPUT_SETTINGS))

        if result is None:
            raise InvalidSnippetError()

        print('[OK]')
        return result

    def __process_code_sippet(self, code, snippet_settings):
        language = self.__pattern.language(snippet_settings)
        if language is None:
            raise RequiredSettingNotFoundError('language')

        is_echo = self.__pattern.echo(snippet_settings)
        if is_echo is None:
            is_echo = True

        is_output = self.__pattern.output(snippet_settings)
        context = self.__pattern.context(snippet_settings)
        snippet_id = self.__pattern.id(snippet_settings)
        timeout = self.__pattern.timeout(snippet_settings)
        allow_errors = self.__pattern.error(snippet_settings)
        output_type = self.__pattern.output_type(snippet_settings)

        if is_output is None:
            is_output = False if snippet_id is not None else True

        # TODO: user processor name
        processing_manager = ProcessingManager(self.__document_language, None)

        before_result = processing_manager.execute_before()
        result = self.__engine.execute(language, code, context, processing_manager, output_type, timeout, allow_errors)
        after_result = processing_manager.execute_after()

        #result = self.__settings.result_pattern(self.__document_language).result(result)

        if snippet_id is not None or is_output:
            result = processing_manager.result(before_result + result + after_result)

        output = ''

        if snippet_id is not None:
            self.__results.store(snippet_id, result)

        if is_echo:
            # TODO: remove?
            #wrapped_code = self.__settings.result_pattern(self.__document_language).source(code)
            #output = wrapped_code
            output = processing_manager.code(code)

        if is_output:
            if len(output) > 0:
                output += '\n'
            output += result

        return output

    def __process_output(self, settings):
        snippet_id = self.__pattern.id(settings)

        if snippet_id is None:
            raise RequiredSettingNotFoundError('snippet id')

        return self.__results.get(snippet_id)
