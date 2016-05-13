import io
import re
from os.path import splitext

from exceptions.processor_errors import InvalidSnippetError, RequiredSettingNotFoundError, \
    ToManyDefaultSettingsOccurencesError, IllagalSettingOccurenceError
from core.kernel_engine import KernelEngine
from core.output_manager import OutputManager
from core.result_manager import ResultManager
from core.processing_manager import ProcessingManager
from settings.group_names import GroupName
from settings.align_types import ImageAlignType


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
        self.__has_default_snippets_settings = False

        self.__default_language = None
        self.__default_echo = True
        self.__default_output = None
        self.__default_context = None
        self.__default_timeout = None
        self.__default_error = False
        self.__default_output_type = None
        self.__default_processor = None
        self.__default_echo_lines = None
        self.__default_image_name = None
        self.__default_image_width = None
        self.__default_image_height = None
        self.__default_image_aligh = ImageAlignType.Default

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

        data = re.sub(self.__pattern.default_settings(), self.__process_default_snippet_settings, data)
        data = re.sub(self.__pattern.entry(), self.__process_entry, data)

        if self.__number_of_snippets == 0:
            print('\tNo snippets found.')

        self.__output_manager.save_document(data)

    def get_filename(self):
        """Returns processed file name"""
        return self.__document_file_name

    def __get_language_by_extension(self, name):
        """Gets language by extension, based on configuration"""
        extension = splitext(name)[1].strip('.')
        languages = self.__settings.languages_by_extension(extension)

        if len(languages) == 1:
            return languages[0]

        if len(languages) == 0:
            return self.__ask_for_language(name, self.__settings.languages())

        return self.__ask_for_language(name, languages)

    @staticmethod
    def __ask_for_language(filename, languages):
        """Ask user for language for unknown extension"""
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

    def __process_default_snippet_settings(self, entry):
        """Process default snippets settings"""
        if self.__has_default_snippets_settings:
            raise ToManyDefaultSettingsOccurencesError()

        self.__has_default_snippets_settings = True

        settings_string = entry.group(GroupName.DEFAULT_SETTINGS)

        snippet_id = self.__pattern.id(settings_string)
        if snippet_id is not None:
            raise IllagalSettingOccurenceError('snippet_id')

        language = self.__pattern.language(settings_string)
        if language is not None:
            self.__default_language = language

        is_echo = self.__pattern.echo(settings_string)
        if is_echo is not None:
            self.__default_echo = is_echo

        is_output = self.__pattern.output(settings_string)
        if is_output is not None:
            self.__default_output = is_output

        context = self.__pattern.context(settings_string)
        if context is not None:
            self.__default_context = context

        timeout = self.__pattern.timeout(settings_string)
        if timeout is not None:
            self.__default_timeout = timeout

        allow_errors = self.__pattern.error(settings_string)
        if allow_errors is not None:
            self.__default_error = allow_errors

        output_type = self.__pattern.output_type(settings_string)
        if output_type is not None:
            self.__default_output_type = output_type

        processor = self.__pattern.processor(settings_string)
        if processor is not None:
            self.__default_processor = processor

        echo_lines = self.__pattern.echo_lines(settings_string)
        if echo_lines is not None:
            self.__default_echo_lines = echo_lines

        image_name = self.__pattern.image_name(settings_string)
        if image_name is not None:
            self.__default_image_name = image_name

        image_width = self.__pattern.image_width(settings_string)
        if image_width is not None:
            self.__default_image_width = image_width

        image_height = self.__pattern.image_height(settings_string)
        if image_height is not None:
            self.__default_image_height = image_height

        image_align = self.__pattern.image_align(settings_string)
        if image_align is not None:
            self.__default_image_align = image_align

        return ''

    def __process_entry(self, entry):
        """Process code snippet or output snippet"""
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
        """Process code snippet"""
        language = self.__pattern.language(snippet_settings)

        if language is None:
            language = self.__default_language

        if language is None:
            raise RequiredSettingNotFoundError('language')

        is_echo = self.__pattern.echo(snippet_settings)
        if is_echo is None:
            is_echo = self.__default_echo

        is_output = self.__pattern.output(snippet_settings)
        if is_output is None:
            is_output = self.__default_output

        context = self.__pattern.context(snippet_settings)
        if context is None:
            context = self.__default_context

        snippet_id = self.__pattern.id(snippet_settings)

        timeout = self.__pattern.timeout(snippet_settings)
        if timeout is None:
            timeout = self.__default_timeout

        allow_errors = self.__pattern.error(snippet_settings)
        if allow_errors is None:
            allow_errors = self.__default_error

        output_type = self.__pattern.output_type(snippet_settings)
        if output_type is None:
            output_type = self.__default_output_type

        processor = self.__pattern.processor(snippet_settings)
        if processor is None:
            processor = self.__default_processor

        echo_lines = self.__pattern.echo_lines(snippet_settings)
        if echo_lines is None:
            echo_lines = self.__default_echo_lines

        if is_output is None:
            is_output = False if snippet_id is not None else True

        image_name = self.__pattern.image_name(snippet_settings)
        if image_name is None:
            image_name = self.__default_image_name

        image_width = self.__pattern.image_width(snippet_settings)
        if image_width is None:
            image_width = self.__default_image_width

        image_height = self.__pattern.image_height(snippet_settings)
        if image_height is None:
            image_height = self.__default_image_height

        image_align = self.__pattern.image_align(snippet_settings)
        if image_align is None:
            image_align = self.__default_image_align

        image_settings = (image_name, image_width, image_height, image_align)

        executor = lambda code, manager: self.__engine.execute(language, code, context, manager, output_type, None, False)
        processing_manager = ProcessingManager(self.__document_language, language, snippet_settings,
                                               processor, self.__output_manager, executor, image_settings)

        before_result = processing_manager.execute_before()
        result = self.__engine.execute(language, code, context, processing_manager, output_type, timeout, allow_errors)
        after_result = processing_manager.execute_after()

        if snippet_id is not None or is_output:
            result = processing_manager.result(before_result + result + after_result)

        output = ''

        if snippet_id is not None:
            self.__results.store(snippet_id, result)

        if is_echo:
            code = code.strip('\n')
            output = processing_manager.code(self.apply_echo_lines(echo_lines, code))

        if is_output:
            if len(output) > 0:
                output += '\n'
            output += result

        return output

    def apply_echo_lines(self, echo_lines, code):
        """Removes hidden lines from code"""
        if echo_lines is None:
            return code

        code_lines = code.split('\n')
        final_lines = []

        for i, code_line in enumerate(code_lines):
            visible = i + 1 in echo_lines[1]
            if echo_lines[0]:
                visible = not visible

            if visible:
                final_lines.append(code_line)

        return '\n'.join(final_lines)

    def __process_output(self, settings):
        """Processes output snippet"""
        snippet_id = self.__pattern.id(settings)

        if snippet_id is None:
            raise RequiredSettingNotFoundError('snippet id')

        return self.__results.get(snippet_id)
