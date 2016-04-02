from os import makedirs
from os.path import join, dirname
import uuid


class OutputManager:

    def __init__(self, output_settings, input_filename):
        self.__data_dir = output_settings.data_directory(input_filename)
        self.__data_dir_url = output_settings.data_dir_url(input_filename)
        self.__output_filename = output_settings.output_filename(input_filename)

    def save_data(self, data, extension):
        makedirs(self.__data_dir, exist_ok=True)

        filename = str.format('img_{0}{1}', str(uuid.uuid4()), extension)
        file_path = join(self.__data_dir, filename)
        file_url = join(self.__data_dir_url, filename)

        with open(file_path, 'wb') as f:
            f.write(data)

        return file_url

    def save_document(self, data):
        makedirs(dirname(self.__output_filename), exist_ok=True)

        with open(self.__output_filename, 'w', encoding='utf8') as f:
            f.write(data)
