
class InvalidLanguageNameError(Exception):
    """Invalid language used in snippet"""

    def __init__(self, name, available):
        self.name = name
        self.available = available

    def __str__(self):
        string = str.format("Kernel for language '{0}' not found. Available languages: \n", self.name)

        for name in self.available:
            string += str.format("\t'{0}'\n", name)

        return string
