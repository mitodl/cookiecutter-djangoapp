#!/bin/bash
set -euf -o pipefail

export TEMPDIR="$(mktemp -d)"
cookiecutter . -o "$TEMPDIR" --no-input
echo "Tempdir is $TEMPDIR"

export BASEDIR="$(find "$TEMPDIR" -name apt.txt -printf '%h\n')"
export PROJECT_NAME="$(basename "$BASEDIR")"
cd "$BASEDIR"
cp "$BASEDIR"/.env.example "$BASEDIR"/.env
pip-compile

# make sure nvm is available
export NVM_DIR="$(mktemp -d)"
echo "NVM tempdir is $NVM_DIR"
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
# This will use package.json to figure out the version to install
source "$NVM_DIR/nvm.sh"
NODE_VERSION=$(cat package.json | jq -r '.engines.node')
echo "Installing node $NODE_VERSION"
# I'm not sure why I need to do this, I think there's some env var interfering with nvm install
bash -c "source $NVM_DIR/nvm.sh; nvm install $NODE_VERSION"
echo "Using node $NODE_VERSION"
nvm use $NODE_VERSION
echo "Node version is..."
node --version

# make sure that docker-compose.yml has a valid syntax
docker-compose ps

# Make sure we start with a fresh container
docker-compose -f docker-compose.yml -f docker-compose.travis.yml kill
docker-compose -f docker-compose.yml -f docker-compose.travis.yml rm -f
docker-compose -f docker-compose.yml -f docker-compose.travis.yml build --no-cache
docker-compose -f docker-compose.yml -f docker-compose.travis.yml run db echo  # create database
docker-compose -f docker-compose.yml -f docker-compose.travis.yml run web pytest

echo "Installing packages..."
docker-compose -f docker-compose.yml -f docker-compose.travis.yml run watch yarn install
echo "Running JS tests..."
docker-compose -f docker-compose.yml -f docker-compose.travis.yml run watch ./travis/js_tests.sh

echo "Success!"
