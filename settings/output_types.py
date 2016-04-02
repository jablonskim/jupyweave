from enum import Enum
import re


class OutputTypes:

    class Types(Enum):
        Stdout = 1
        Stderr = 2
        Result = 3
        Image = 4

    def __init__(self, types_str):
        self.__types = self.__parse_types(types_str)

    def is_enabled(self, type_str):
        type_str = type_str.lower()

        if type_str == 'stdout':
            return OutputTypes.Types.Stdout in self.__types

        if type_str == 'stderr':
            return OutputTypes.Types.Stderr in self.__types

        if 'text' in type_str:
            return OutputTypes.Types.Result in self.__types

        if 'image' in type_str:
            return OutputTypes.Types.Image in self.__types

    @staticmethod
    def __parse_types(types_str):
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

        if 'all' in types_tokens:
            types.add(OutputTypes.Types.Stdout)
            types.add(OutputTypes.Types.Stderr)
            types.add(OutputTypes.Types.Result)
            types.add(OutputTypes.Types.Image)

        return types