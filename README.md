# Grader

[![Build Status](https://travis-ci.org/samupl/python-parametrized-tests.svg?branch=master)](https://travis-ci.org/samupl/python-parametrized-tests)

## Requirements

The best way to run grader is to use the virtualenv. Create the virtualenv using the following set of commands:

```
virtualenv -p $(which python3.4) grader-venv
source grader-venv/bin/activate
pip install -r requirements.txt
```

The `virtualenv` creates a Python Virtual Environment. This command should only be run once.

The `source` commands makes your current shell use the virtual environments (it's a wrapper that automatically sets proper environment variables)

The `pip install -r requirements.txt` makes sure your Python Virtual Environment has up-to-date packages required by the grader software to run.

## Installation / Upgrading

After fetching the latest source for grader, be sure to run the following commands:

```
source grader-venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

The `pip` command, as stated before, makes sure that up-to-date packages required by the grader software are installed in the virtual environment.

The `manage.py migrate` command runs all database migrations that have not yet been applied to the database.

When run first time, `manage.py` migrate will populate the database schema. When it's being run with an existing database, it will apply all migrations to make the database schema up-to-date, without losing any data.

## Running the development server (front-end)

You can run a _development_ server using the following command:

```
source grader-venv/bin/activate
python manage.py runserver
```

A software system-check will run, and after a brief moment you should see a message that a local development server has started.

This way you can view the front-end and manage the software (from its web interface) without actually installing any web server or application server.

Please note that `runserver` starts a single-threaded, *development* server, which has some benefits to developers, but is generally slow and not production-ready.

## Production deployment

Django can be deployed using WSGI.

Official documentation: https://docs.djangoproject.com/en/1.9/howto/deployment/

Gunicorn deployment: https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/gunicorn/

Apache + mod_wsgi deployment: https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/

Full documentation on deploying the grader system will be written soon.