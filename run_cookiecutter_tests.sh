#!/bin/bash
set -euf -o pipefail

export TEMPDIR="$(mktemp -d)"
cookiecutter . -o "$TEMPDIR" --no-input

export TOXINI_DIR=$(find "$TEMPDIR" -name tox.ini -printf '%h\n')
cd "$TOXINI_DIR"
cp "$TOXINI_DIR"/.env.example "$TOXINI_DIR"/.env
docker-compose -f travis-docker-compose.yml build
docker-compose -f travis-docker-compose.yml run web tox

rm -rf "$TEMPDIR"
