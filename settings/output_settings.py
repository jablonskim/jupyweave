from os.path import basename, splitext, join


class OutputSettings:
    """Represents output settings"""

    def __init__(self, settings_data):
        """Initialization"""
        self.__results_base = settings_data['results_base']
        self.__filename = settings_data['filename']
        self.__data_dir = settings_data['data_dir']

        self.__name_pattern = settings_data['patterns']['name']
        self.__extension_pattern = settings_data['patterns']['extension']

    def data_directory(self, input_path):
        """Returns data directory location"""
        name, ext = OutputSettings.__extract_name_ext(input_path)

        base_dir = self.__replace_patterns(self.__results_base, name, ext)
        img_dir = self.__replace_patterns(self.__data_dir, name, ext)

        return join(base_dir, img_dir)

    def data_dir_url(self, input_path):
        """Returns data directory url"""
        name, ext = OutputSettings.__extract_name_ext(input_path)
        return self.__replace_patterns(self.__data_dir, name, ext)

    def output_filename(self, input_path):
        """Returns output filename"""
        name, ext = OutputSettings.__extract_name_ext(input_path)

        base_dir = self.__replace_patterns(self.__results_base, name, ext)
        out_file = self.__replace_patterns(self.__filename, name, ext)

        return join(base_dir, out_file)

    @staticmethod
    def __extract_name_ext(input_path):
        """Extracts name and extension from path"""
        filename = basename(input_path)
        return splitext(filename)

    def __replace_patterns(self, path, name, ext):
        """Replaces patterns with name and extension"""
        return path.replace(self.__name_pattern, name).replace(self.__extension_pattern, ext)
