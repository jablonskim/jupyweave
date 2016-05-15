from jupyweave.jupyweave import JuPyWeave
from sys import argv


def main():
    program = JuPyWeave(argv)
    program.process()
