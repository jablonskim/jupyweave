import re
from exceptions.processor_errors import ToManySettingOccurencesError, InvalidBoolValueError, TimeoutValueError
from settings.group_names import GroupName


class Pattern:
    """Regular expressions container. Extracts selected data from strings"""

    def __init__(self, entry, language, echo, output, context, snippet_id, timeout, error):
        """Compiles & initializes regexes"""
        self.__entry = re.compile(entry)
        self.__language = re.compile(language)
        self.__echo = re.compile(echo)
        self.__output = re.compile(output)
        self.__context = re.compile(context)
        self.__id = re.compile(snippet_id)
        self.__timeout = re.compile(timeout)
        self.__error = re.compile(error)

    def entry(self):
        """Returns regex for full entry (code snippet or output snippet)"""
        return self.__entry

    def language(self, string):
        """Extracts language from setting string"""
        return Pattern.__extract_setting(string, self.__language, GroupName.LANGUAGE)

    def echo(self, string):
        """Extracts echo output information from setting string"""
        return Pattern.__convert_to_bool(Pattern.__extract_setting(string, self.__echo, GroupName.ECHO))

    def output(self, string):
        """Extracts result output information from setting string"""
        return Pattern.__convert_to_bool(Pattern.__extract_setting(string, self.__output, GroupName.OUTPUT))

    def context(self, string):
        """Extracts context from setting string"""
        return Pattern.__extract_setting(string, self.__context, GroupName.CONTEXT)

    def id(self, string):
        """Extracts snippet id from setting string"""
        return Pattern.__extract_setting(string, self.__id, GroupName.ID)

    def timeout(self, string):
        """Extracts execution timeout from settings string"""
        timeout = Pattern.__extract_setting(string, self.__timeout, GroupName.TIMEOUT)
        if timeout is None:
            return None

        try:
            return int(timeout) / 1000.0
        except ValueError:
            raise TimeoutValueError(timeout)

    def error(self, string):
        """Extracts error information from string"""
        return Pattern.__convert_to_bool(Pattern.__extract_setting(string, self.__error, GroupName.ALLOW_ERROR))

    @staticmethod
    def __extract_setting(string, regex, group_name):
        items = re.finditer(regex, string)
        items = [item for item in items]

        if len(items) == 0:
            return None

        if len(items) != 1:
            raise ToManySettingOccurencesError(group_name)

        return items[0].group(group_name)

    @staticmethod
    def __convert_to_bool(value):
        if value is None:
            return None

        if value.lower() in ['t', 'true', '1', 'y', 'yes']:
            return True

        if value.lower() in ['f', 'false', '0', 'n', 'no']:
            return False

        raise InvalidBoolValueError(value)
