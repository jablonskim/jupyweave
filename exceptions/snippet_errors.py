
class SnippetSyntaxError(Exception):

    def __init__(self):
        self.language = None

    def set_language(self, language):
        self.language = language


class EndSnippetSyntaxError(SnippetSyntaxError):

    def __init__(self, illegal_pattern):
        self.pattern = illegal_pattern

    def __str__(self):
        return str.format("Code snippet for '{0}' contains illegal pattern '{1}' in 'end' definition",
                          self.language, self.pattern)


class BeginSnippetSyntaxError(SnippetSyntaxError):

    def __init__(self, missing_pattern):
        self.pattern = missing_pattern

    def __str__(self):
        return str.format("Missing '{0}' (snippet settings definition) in 'begin' definition for '{1}'",
                          self.pattern, self.language)
