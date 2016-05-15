from .jupyweave import JuPyWeave
from sys import argv


def main():
    program = JuPyWeave(argv)
    program.process()

if __name__ == '__main__':
    main()
