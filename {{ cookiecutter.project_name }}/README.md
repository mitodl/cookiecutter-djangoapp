# {{ cookiecutter.project_name }}
{{ cookiecutter.description }}

## Major Dependencies
- Docker
  - OSX recommended install method: [Download from Docker website](https://docs.docker.com/mac/)
- docker-compose
  - Recommended install: pip (`pip install docker-compose`)
- Virtualbox (https://www.virtualbox.org/wiki/Downloads)
- _(OSX only)_ Node/NPM, and Yarn
  - OSX recommended install method: [Installer on Node website](https://nodejs.org/en/download/)
  - No specific version has been chosen yet.

## (OSX only) Getting your machine Docker-ready

#### Create your docker container:

The following commands create a Docker machine named ``{{ cookiecutter.project_name }}``, start the
container, and configure environment variables to facilitate communication
with the edX instance.

    docker-machine create --driver virtualbox {{ cookiecutter.project_name }}
    docker-machine start {{ cookiecutter.project_name }}
    # 'docker-machine env (machine)' prints export commands for important environment variables
    eval "$(docker-machine env {{ cookiecutter.project_name }})"


## Docker Container Configuration and Start-up

#### 1) Create your ``.env`` file

This file should be copied from the example in the codebase:

    cp .env.example .env

#### 2) _(OSX only)_ Set up and run the webpack dev server on your host machine

In the development environment, our static assets are served from the webpack
dev server. When this environment variable is set, the script sources will
look for the webpack server at that host instead of the host where Docker is running.

You'll need to install the [yarn](https://yarnpkg.com/en/docs/cli/)
package manager. You can do:

    sudo node ./scripts/install_yarn.js

To install it. Nice! You can check which version is installed in
`package.json` to be make you're getting the version we are
standardized on.

Now, in a separate terminal tab, use the webpack helper script to install npm modules and run the dev server:

    ./webpack_dev_server.sh --install

The ``--install`` flag is only needed if you're starting up for the first time, or if updates have been made
to the packages in ``./package.json``. If you've installed those packages and there are no ``./package.json``
updates, you can run this without the ``--install`` flag: ``./webpack_dev_server.sh``

**DEBUGGING NOTE:** If you see an error related to node-sass when you run this script, try running
``yarn install`` again.

#### 3) Build the containers
Run this command:

    docker-compose build

You will also need to run this command whenever ``requirements.txt`` or ``test_requirements.txt`` change.

#### 4) Run migrations
Create the database tables from the Django models:

    docker-compose run web ./manage.py migrate

#### 5) Run the container

Start Django, PostgreSQL, and other related services:

    docker-compose up

In another terminal tab, navigate to the {{ cookiecutter.project_name }} directory
and add a superuser in the now-running Docker container:

    docker-compose run web ./manage.py createsuperuser

You should now be able to do the following:

1. Visit {{ cookiecutter.project_name }} in your browser on port `{{ cookiecutter.port }}`. _(OSX Only)_ Docker auto-assigns
 the container IP. Run ``docker-machine ip`` to see it. Your {{ cookiecutter.project_name }} URL will
 be something like this: ``192.168.99.100:{{ cookiecutter.port }}``.

## Running Commands and Testing

As shown above, manage commands can be executed on the Docker-contained
{{ cookiecutter.project_name }} app. For example, you can run a Python shell with the following command:

    docker-compose run web ./manage.py shell

Tests should be run in the Docker container, not the host machine. They can be run with the following commands:

    # Run the full suite
    ./test_suite.sh
    # Run Python tests only
    docker-compose run --rm web pytest
    # Single file test
    docker-compose run --rm web pytest /path/to/test.py
    # Run the JS tests with coverage report
    docker-compose run --rm watch npm run-script coverage
    # run the JS tests without coverage report
    docker-compose run --rm watch npm test
    # run a single JS test file
    docker-compose run --rm watch npm run-script singleTest /path/to/test.js
    # Run the JS linter
    docker-compose run --rm watch npm run-script lint
    # Run SCSS linter
    docker-compose run --rm watch npm run scss_lint


### Running the app in a notebook

This repo includes a config for running a [Jupyter notebook](https://jupyter.org/) in a
Docker container. This enables you to do in a Jupyter notebook anything you might
otherwise do in a Django shell. To get started:

- Copy the example file
    ```bash
    # Choose any name for the resulting .ipynb file
    cp localdev/app.ipynb.example localdev/app.ipynb
    ```
- Build the `notebook` container _(for first time use, or when requirements change)_
    ```bash
    docker-compose -f docker-compose-notebook.yml build
    ```
- Run all the standard containers (`docker-compose up`)
- In another terminal window, run the `notebook` container
    ```bash
    docker-compose -f docker-compose-notebook.yml run --rm --service-ports notebook
    ```
- Visit the running notebook server in your browser. The `notebook` container log output will
  indicate the URL and `token` param with some output that looks like this:
    ```
    notebook_1  |     To access the notebook, open this file in a browser:
    notebook_1  |         file:///home/mitodl/.local/share/jupyter/runtime/nbserver-8-open.html
    notebook_1  |     Or copy and paste one of these URLs:
    notebook_1  |         http://(2c19429d04d0 or 127.0.0.1):8080/?token=2566e5cbcd723e47bdb1b058398d6bb9fbf7a31397e752ea
    ```
  Here is a one-line command that will produce a browser-ready URL from that output. Run this in a separate terminal:
    ```bash
    docker logs $(docker ps --format '{{ "{{" }}.Names}}' | grep "_notebook_run_") | grep -E "http://(.*):8080[^ ]+\w" | tail -1 | sed -e 's/^[[:space:]]*//'
    ```
  OSX users can pipe that output to `xargs open` to open a browser window directly with the URL from that command.
- Navigate to the `.ipynb` file that you created and click it to run the notebook
- Execute the first block to confirm it's working properly (click inside the block
  and press Shift+Enter)

From there, you should be able to run code snippets with a live Django app just like you
would in a Django shell.


## Commits

To ensure commits to github are safe, you should install the following first:
```
pip install pre_commit
pre-commit install
```

To automatically install precommit hooks when cloning a repo, you can run this:
```
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir ~/.git-template
```    
