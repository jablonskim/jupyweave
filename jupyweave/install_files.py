from os import makedirs, listdir, path, environ
from shutil import copy
import platform


def copy_files(source_dir, destination_dir, ftype):
    for file in listdir(source_dir):
        if file.endswith(ftype):
            copy(path.join(source_dir, file), destination_dir)


def main():
    system_path = None
    local_path = None

    if platform.system() == 'Windows':
        system_path = environ['PROGRAMDATA']
        local_path = environ['APPDATA']

    if platform.system() == 'Linux':
        system_path = '/usr/local/share'
        local_path = '~/.local/share'

    if system_path is not None and local_path is not None:
        cfg = 'jupyweave/config/'
        prc = 'jupyweave/processors/'

        makedirs(path.join(system_path, cfg), exist_ok=True)
        makedirs(path.join(system_path, prc), exist_ok=True)
        makedirs(path.join(local_path, cfg), exist_ok=True)
        makedirs(path.join(local_path, prc), exist_ok=True)

        here = path.dirname(path.realpath(__file__))

        copy_files(path.join(here, 'configs/'), path.join(system_path, cfg), '.json')
        copy_files(path.join(here, 'user_processors/'), path.join(system_path, prc), '.py')

        print('Succesfully installed configurations and user processors.')


if __name__ == '__main__':
    main()
