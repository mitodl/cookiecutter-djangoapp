import re


def main():
    # Make sure the project name is all lowercase
    if not re.match(r'^[_a-z0-9]+$', '{{ cookiecutter.project_name }}'):
        raise Exception("project_name must contain only lowercase letters, numbers or underscores")


if __name__ == "__main__":
    main()
