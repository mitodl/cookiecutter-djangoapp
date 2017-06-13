#!/bin/bash
set -eo pipefail

docker build -t mitodl/{{ cookiecutter.project_name }}_web_travis_next -f Dockerfile .
docker build -t mitodl/{{ cookiecutter.project_name }}_watch_travis -f travis/Dockerfile-travis-watch-build .

docker push mitodl/{{ cookiecutter.project_name }}_web_travis_next
docker push mitodl/{{ cookiecutter.project_name }}_watch_travis
