"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='NotesBot',

    version='1.0',

    description='A Discord bot to manage your grades',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/Gandus10/NotesBot',

    # Author details
    author='Laurent Gander & Sylvain Renaud',
    author_email='laurent.gander@he-arc.ch & sylvain.renaud@he-arc.ch',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    keywords='discord bot grades notes',

    install_requires=(
        'aiohttp>=2.1.0',
        'discord.py==0.16.8'
    ),


    extras_require={
        'qa': ['flake8', 'isort', 'pydocstyle', 'rstcheck'],
    },
)