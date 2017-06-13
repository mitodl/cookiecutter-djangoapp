import os

from piptools.scripts.compile import cli


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def main():
    cli([os.path.join(PROJECT_DIRECTORY, 'requirements.in')])


if __name__ == "__main__":
    main()
