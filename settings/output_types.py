from enum import Enum
import re


class OutputTypes:
    """Class representing visible output types"""

    class Types(Enum):
        """Types"""
        Stdout = 1
        Stderr = 2
        Result = 3
        Image = 4
        Pdf = 5

    def __init__(self, types_str):
        """Initialization from string"""
        self.__types = self.__parse_types(types_str)

    def is_enabled(self, type_str):
        """Checks if given type is visible"""
        type_str = type_str.lower()

        if type_str == 'stdout':
            return OutputTypes.Types.Stdout in self.__types

        if type_str == 'stderr':
            return OutputTypes.Types.Stderr in self.__types

        if 'text' in type_str:
            return OutputTypes.Types.Result in self.__types

        if 'image' in type_str:
            return OutputTypes.Types.Image in self.__types

        if 'application/pdf' in type_str:
            return OutputTypes.Types.Pdf in self.__types

    @staticmethod
    def __parse_types(types_str):
        """Parses types"""
        if types_str is None:
            types_str = 'All'

        types = set()

        types_tokens = [token.lower() for token in re.findall(r'\w+', types_str)]

        if 'stdout' in types_tokens:
            types.add(OutputTypes.Types.Stdout)

        if 'stderr' in types_tokens:
            types.add(OutputTypes.Types.Stderr)

        if 'result' in types_tokens:
            types.add(OutputTypes.Types.Result)

        if 'image' in types_tokens:
            types.add(OutputTypes.Types.Image)

        if 'pdf' in types_tokens:
            types.add(OutputTypes.Types.Pdf)

        if 'all' in types_tokens:
            types.add(OutputTypes.Types.Stdout)
            types.add(OutputTypes.Types.Stderr)
            types.add(OutputTypes.Types.Result)
            types.add(OutputTypes.Types.Image)
            types.add(OutputTypes.Types.Pdf)

        return types
