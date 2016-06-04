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
    is_admin = None

    if platform.system() == 'Windows':
        system_path = environ['PROGRAMDATA']
        local_path = environ['APPDATA']
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if platform.system() == 'Linux':
        system_path = '/usr/local/share'
        local_path = '~/.local/share'
        from os import getuid
        is_admin = getuid() == 0

    if system_path is not None and local_path is not None:
        cfg = 'jupyweave/config/'
        prc = 'jupyweave/processors/'

        if is_admin:
            makedirs(path.join(system_path, cfg), exist_ok=True)
            makedirs(path.join(system_path, prc), exist_ok=True)
        else:
            makedirs(path.join(local_path, cfg), exist_ok=True)
            makedirs(path.join(local_path, prc), exist_ok=True)

        here = path.dirname(path.realpath(__file__))

        copy_path = system_path if is_admin else local_path

        copy_files(path.join(here, 'configs/'), path.join(copy_path, cfg), '.json')
        copy_files(path.join(here, 'user_processors/'), path.join(copy_path, prc), '.py')

        print('Succesfully installed configurations and user processors in %s.' %
              ('system directory' if is_admin else 'user directory'))


if __name__ == '__main__':
    main()
