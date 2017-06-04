#!/bin/sh

set -xe

flake8 notes-bot
pydocstyle notes-bot
rstcheck README.rst
isort --recursive --check-only notes-bot