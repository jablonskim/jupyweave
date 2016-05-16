from jupyweave.jupyweave import JuPyWeave
from jupyweave.install_files import main as install_main
from sys import argv


def main():
    program = JuPyWeave(argv)
    program.process()


def install():
    install_main()
