#!/usr/bin/env python3

from sys import argv, exit

from exceptions.engine_errors import InvalidLanguageNameError
from exceptions.processor_errors import ProcessingError
from exceptions.settings_errors import InvalidConfigurationError
from exceptions.snippet_errors import SnippetSyntaxError
from core.document_processor import DocumentProcessor
from settings.settings import Settings


class JuPyWeave:
    """Applications main class"""

    DEFAULT_CONFIG_FILE_NAME = 'defconfig.json'

    def __init__(self, args):
        """Loads settings and filenames"""
        self.__arguments = args
        self.__config_file, self.__filenames = self.__parse_args()
        self.__document_processors = []

        if len(self.__filenames) == 0:
            self.__usage()

        try:
            self.__settings = Settings(self.__config_file)
        except (InvalidConfigurationError, SnippetSyntaxError) as e:
            JuPyWeave.exit_error(e)
        except Exception as e:
            JuPyWeave.exit_error(e)

    def process(self):
        """Processing documents"""
        self.__document_processors = DocumentProcessor.create_processors(self.__filenames, self.__settings)

        for i, processor in enumerate(self.__document_processors):
            proc_str = str.format('\nProcessing file {0}/{1} [{2}]:', i + 1, len(self.__document_processors),
                                  processor.get_filename())
            print(proc_str)

            try:
                processor.process()
            except FileNotFoundError as e:
                print(JuPyWeave.__add_indentation('\n\nError: File %s not found' % e.filename))
            except (ProcessingError, InvalidLanguageNameError) as e:
                print(JuPyWeave.__add_indentation('\n\nError: %s' % e))
            except Exception as e:
                print(JuPyWeave.__add_indentation('\n\nError: %s' % e))

        print()

    @staticmethod
    def exit_error(error_msg):
        print(error_msg)
        exit()

    def __usage(self):
        print('Usage: %s [--config=filename] file1 [file2 ...]' % self.__arguments[0])
        exit()

    @staticmethod
    def __add_indentation(string):
        return ''.join([str.format('\t{0}\n', line) for line in string.splitlines()])

    def __parse_args(self):
        args = self.__arguments[1:]
        cfg_prefix = '--config='
        filenames = []
        config = JuPyWeave.DEFAULT_CONFIG_FILE_NAME

        for arg in args:
            if arg.startswith(cfg_prefix):
                config = arg[len(cfg_prefix):]
            else:
                filenames.append(arg)

        return config, filenames


def main():
    program = JuPyWeave(argv)
    program.process()

if __name__ == '__main__':
    main()
