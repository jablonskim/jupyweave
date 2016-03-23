
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
        code = code.replace('\n', '\n\t')
        super(ExecutionTimeoutError, self).__init__('Timeout while executing code snippet: \n\t%s' % code)


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


class ToManySettingOccurencesError(ProcessingError):
    """To many same setting occurences in snippet"""

    def __init__(self, name):
        super(ToManySettingOccurencesError, self).__init__('To many occurences of \'%s\' setting in snippet' % name)


class InvalidBoolValueError(ProcessingError):
    """Invalid boolean variable value"""

    def __init__(self, value):
        super(InvalidBoolValueError, self).__init__('Invalid value of boolean variable in snippet settings: %s' % value)


class ResultNotFoundError(ProcessingError):
    """Invalid result id"""

    def __init__(self, rid):
        super(ResultNotFoundError, self).__init__('No result with ID \'%s\'' % rid)


class SnippetRuntimeError(ProcessingError):
    """Exception raised from snippet code"""

    def __init__(self, error):
        super(SnippetRuntimeError, self).__init__('Exception during execution of code snippet\n%s' % error)
