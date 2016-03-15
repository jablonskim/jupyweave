#!/usr/bin/env python3

from sys import argv, exit
from settings.settings import Settings
from processor import Processor
from exceptions.snippet_errors import SnippetSyntaxError
from exceptions.settings_errors import InvalidConfigurationError

DEFAULT_CONFIG_FILE_NAME = 'defconfig.json'


class JuPyWeave:

    def __init__(self, args):
        self.arguments = args
        self.config_file, self.filenames = self.parse_args()
        self.processors = []

        if len(self.filenames) == 0:
            self.usage()

        try:
            self.settings = Settings(self.config_file)
        except (InvalidConfigurationError, SnippetSyntaxError) as e:
            JuPyWeave.exit_error(e)
        except Exception as e:
            JuPyWeave.exit_error(e)

    def usage(self):
        print('Usage: %s [--config=filename] file1 [file2 ...]' % self.arguments[0])
        exit()

    @staticmethod
    def exit_error(error_msg):
        print(error_msg)
        exit()

    def parse_args(self):
        args = self.arguments[1:]
        cfg_prefix = '--config='
        filenames = []
        config = DEFAULT_CONFIG_FILE_NAME

        for arg in args:
            if arg.startswith(cfg_prefix):
                config = arg[len(cfg_prefix):]
            else:
                filenames.append(arg)

        return config, filenames

    def process(self):
        self.processors = Processor.create_processors(self.filenames, self.settings)

        for i, processor in enumerate(self.processors):
            proc_str = str.format('Processing file {0}/{1} [{2}]:', i + 1, len(self.processors), processor.get_filename())
            print(proc_str)

            try:
                processor.process()
            except FileNotFoundError as e:
                print('\tError: File %s not found' % e.filename)
            except Exception as e:
                print('\t%s' % e)

        print()


def main():
    program = JuPyWeave(argv)
    program.process()

if __name__ == '__main__':
    main()
