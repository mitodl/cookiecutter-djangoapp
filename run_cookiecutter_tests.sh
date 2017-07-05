#!/bin/bash
set -euf -o pipefail

export TEMPDIR="$(mktemp -d)"
cookiecutter . -o "$TEMPDIR" --no-input

export TOXINI_DIR=$(find "$TEMPDIR" -name tox.ini -printf '%h\n')
cd "$TOXINI_DIR"
cp "$TOXINI_DIR"/.env.example "$TOXINI_DIR"/.env
pip-compile

# make sure that docker-compose.yml has a valid syntax
docker-compose ps

# Make sure we start with a fresh container
docker-compose -f travis-docker-compose.yml kill
docker-compose -f travis-docker-compose.yml rm -f
docker-compose -f travis-docker-compose.yml build --no-cache

docker-compose -f travis-docker-compose.yml run web tox

docker build -t travis-watch -f ./Dockerfile-node .
docker run travis-watch bash ./travis/js_tests.sh

echo "Success!"
