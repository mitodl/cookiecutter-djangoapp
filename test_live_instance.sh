#!/bin/bash
set -euf -o pipefail

if ! which cookiecutter
then
  echo "Missing cookiecutter executable. Run this command from within a virtualenv, run pip install -r requirements.txt, and try again."
  exit 1
fi

DEPLOYDIR=$(mktemp -d)
echo "Temp directory is $DEPLOYDIR"
COOKIECUTTER_TEMPLATE_DIR="$(pwd)"
cd "$DEPLOYDIR"

cookiecutter "$COOKIECUTTER_TEMPLATE_DIR" -o . --no-input
cd dr_horribles_site
cp .env.example .env
echo "MAILGUN_KEY=fake" >> .env
echo "MAILGUN_URL=fake" >> .env
docker-compose rm -f
docker-compose build
docker-compose up
