"""
Install {{ cookiecutter.project_name }} via setuptools
"""
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as testcommand

setup(
    name='{{ cookiecutter.project_name }}',
    version='0.0.0',
    license='AGPLv3',
    author='MIT ODL Engineering',
    author_email='odl-engineering@mit.edu',
    url='http://github.com/mitodl/{{ cookiecutter.project_name }}',
    description="{{ cookiecutter.description|replace("\"","\\\"") }}",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
