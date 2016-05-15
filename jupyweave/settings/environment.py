import platform
from os import environ, path


class Environment:

    SYSTEM_PATH = None
    LOCAL_PATH = None

    @staticmethod
    def get_paths():
        if Environment.SYSTEM_PATH is None or Environment.LOCAL_PATH is None:
            Environment.__set_paths()

        return Environment.LOCAL_PATH, Environment.SYSTEM_PATH

    @staticmethod
    def __set_paths():
        if platform.system() == 'Windows':
            Environment.SYSTEM_PATH = path.join(environ['PROGRAMDATA'], 'jupyweave/')
            Environment.LOCAL_PATH = path.join(environ['APPDATA'], 'jupyweave/')
            return

        if platform.system() == 'Linux':
            Environment.SYSTEM_PATH = path.join('/usr/local/share', 'jupyweave/')
            Environment.LOCAL_PATH = path.join('~/.local/share', 'jupyweave/')
            return

        raise SystemError('System not supported')
