
class ProcessingError(Exception):
    """Base exception for processing errors"""

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return self.__msg


class KernelClientStartingError(ProcessingError):
    """Class represents error while starting kernel"""

    def __init__(self, language):
        super(KernelClientStartingError, self).__init__('Initialization of %s Kernel client failed' % language)


class ExecutionTimeoutError(ProcessingError):
    """Class represents timeout during executing code"""

    def __init__(self, code):
        code = code.replace('\n', '\n\t\t')
        super(ExecutionTimeoutError, self).__init__('Timeout while executing code snippet: \n\t\t%s' % code)


class TimeoutValueError(ProcessingError):
    """Class representing timeout value error"""

    def __init__(self, value):
        super(TimeoutValueError, self).__init__('Invalid value of \'timeout\' snippet setting: %s' % value)


class InvalidSnippetError(ProcessingError):
    """Invalid snippet error"""
    def __init__(self):
        super(InvalidSnippetError, self).__init__('Invalid snippet')


class RequiredSettingNotFoundError(ProcessingError):
    """Snippet's required setting is missing"""

    def __init__(self, name):
        super(RequiredSettingNotFoundError, self).__init__('Required snippet setting for \'%s\' configuration not found' % name)


class ToManySettingOccurencesError(Exception):
    # TODO
    pass


class InvalidBoolValueError(Exception):
    # TODO
    pass


class ResultNotFoundError(Exception):
    # TODO
    pass
