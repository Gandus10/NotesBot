#!/bin/sh

set -xe

flake8 projetBot
pydocstyle projetBot
rstcheck README.rst
isort --recursive --check-only projetBot