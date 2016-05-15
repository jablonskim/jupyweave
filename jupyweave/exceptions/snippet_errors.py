
class SnippetSyntaxError(Exception):
    """Base class for snippets syntax errors"""

    def __init__(self):
        self.language = None

    def set_language(self, language):
        self.language = language


class EndSnippetSyntaxError(SnippetSyntaxError):
    """Ending snippet syntax error"""

    def __init__(self, illegal_pattern):
        self.pattern = illegal_pattern

    def __str__(self):
        return str.format("Code snippet for '{0}' contains illegal pattern '{1}' in 'end' definition",
                          self.language, self.pattern)


class BeginSnippetSyntaxError(SnippetSyntaxError):
    """Beginning snippet syntax error"""

    def __init__(self, missing_pattern):
        self.pattern = missing_pattern

    def __str__(self):
        return str.format("Missing '{0}' (snippet settings definition) in 'begin' definition for '{1}'",
                          self.pattern, self.language)


class OutputSnippetSyntaxError(SnippetSyntaxError):
    """Outptu snippet syntax error"""

    def __init__(self, missing_pattern):
        self.pattern = missing_pattern

    def __str__(self):
        return str.format("Missing '{0}' (snippet settings definition) in 'output' definition for '{1}'",
                          self.pattern, self.language)


class SettingSnippetSyntaxError(SnippetSyntaxError):
    """Snippet settings syntax error"""

    def __init__(self, name, missing_pattern):
        self.setting_name = name
        self.pattern = missing_pattern

    def __str__(self):
        return str.format("Missing '{0}' (snippet settings definition) in '{2}' definition for '{1}'",
                          self.pattern, self.language, self.setting_name)
