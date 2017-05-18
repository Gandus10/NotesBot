"""Travis bot for Discord."""

from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discord-notes-bot',
    version='0.0.1.dev20170516',  # see PEP-0440
    author='Sylvain Renaud and Laurent Gander',
    author_email='sylvain.renaud@he-arc.ch, laurent.gander@he-arc.ch',
    homepage='https://github.com/Gandus10/projetBot',
    description=__doc__,
    long_description=long_description,
    packages=find_packages(exclude=('contrib', 'docs', 'tests')),
    keywords='discord asyncio bot',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
    ),
    install_requires=(
        'aiohttp>=2.0.0',
        'PyOpenSSL>=17.0.0'
    ),
    extras_require={
        'fast': ('cchardet', 'aiodns'),  # making it faster (recommended)
        'qa': ('flake8', 'isort', 'pycodestyle', 'pydocstyle', 'rstcheck'),
    }
)
