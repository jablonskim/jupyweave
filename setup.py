from setuptools import setup, find_packages
from setuptools.command.install import install
import platform
from os import makedirs, path, environ, listdir
from shutil import copy


class PostInstall(install):

    def copy_files(self, source_dir, destination_dir, ftype):
        for file in listdir(source_dir):
            if file.endswith(ftype):
                copy(path.join(source_dir, file), destination_dir)

    def run(self):
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

            self.copy_files(path.join(here, 'configs/'), path.join(system_path, cfg), '.json')
            self.copy_files(path.join(here, 'user_processors/'), path.join(system_path, prc), '.py')

        install.run(self)

setup(
    name='jupyweave',
    version='0.1.0',

    description='',  # TODO
    long_description='',  # TODO

    url='https://github.com/jablonskim/jupyweave',

    author='Mateusz Jablonski',
    author_email='mjablonski92@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Documentation',
        'Topic :: Text Processing :: Markup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='jupyweave literate programming',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=['pygments', 'jupyter', 'jupyter_client'],
    package_data={},  # TODO

    entry_points={
        'console_scripts': ['jupyweave=jupyweave:main']
    },

    cmdclass={
        'install': PostInstall
    }
)
