#!/bin/bash
set -euf -o pipefail

export TEMPDIR="$(mktemp -d)"
cookiecutter . -o "$TEMPDIR" --no-input
echo "Tempdir is $TEMPDIR"

export TOXINI_DIR="$(find "$TEMPDIR" -name tox.ini -printf '%h\n')"
export PROJECT_NAME="$(basename "$TOXINI_DIR")"
cd "$TOXINI_DIR"
cp "$TOXINI_DIR"/.env.example "$TOXINI_DIR"/.env
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

docker-compose -f docker-compose.yml -f docker-compose.travis.yml run web tox

# Make a lock file to avoid a COPY failure in the Dockerfile
# First, install the right versions of node and yarn
echo "Installing yarn..."
node ./scripts/install_yarn.js
echo "Installing packages..."
yarn install
docker build --no-cache -f ./travis/Dockerfile-travis-watch-build -t mitodl/${PROJECT_NAME}_watch_travis .
docker build --no-cache -f ./travis/Dockerfile-travis-watch -t travis-watch .
./travis/js_tests.sh

echo "Success!"
