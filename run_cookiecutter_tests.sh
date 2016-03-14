#!/bin/bash
set -euf -o pipefail

export TEMPDIR="$(mktemp -d)"
cookiecutter . -o "$TEMPDIR" --no-input

export TOXINI_DIR=$(find "$TEMPDIR" -name tox.ini -printf '%h\n')
cd "$TOXINI_DIR"
docker-compose build
docker-compose run web tox

rm -rf "$TEMPDIR"
