#!/usr/bin/env python
from setuptools import find_packages, setup

# read the contents of README file
from os import path
from io import open  # for Python 2 and 3 compatibility

# get __version__ from _version.py
ver_file = path.join('termax', 'version.py')
with open(ver_file) as f:
    exec(f.read())

this_directory = path.abspath(path.dirname(__file__))


# read the contents of README.md
def readme():
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


# read the contents of requirements.txt
with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='termax',
    version='0.1.0',
    author='Szqub',
    author_email='szqub@example.com',
    description='AI System Administrator Assistant',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Szqub/termax',
    keywords=['LLM', 'deep learning', 'MLOps', 'shell', 'neural networks', 'command line', 'terminal', 'autocomplete'],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "termax=termax.cli.main:app",
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    setup_requires=['setuptools>=38.6.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
