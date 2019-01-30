# pytest-django-tutorial

Meme generator app for the pytest-django talk at the SF Django meetup.

Slides for this talk are [here](https://docs.google.com/presentation/d/1lvk9-XvdP13aX0vsgFUdDSpvATAh5aD9TXy0voaH0qA/edit?usp=sharing)

## Running the Project Remotely

Deploy to Heroku with the button below

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wesleykendall/pytest-django-tutorial)

## Local Project Setup

Clone this repo:

```
git clone git@github.com:wesleykendall/pytest-django-tutorial.git
```

And change into the main directory:

```
cd pytest-django-tutorial
```

### Notes for Mac Users

Be sure to install brew in order to set up some of the dependencies for local development.

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

If that doesn't work, you may need to install xcode:

```
xcode-select --install
```

### Pyenv Setup

The local setup assumes you have pyenv installed. In order to install pyenv, either view instructions [here](https://github.com/pyenv/pyenv#installation) or try the following if you are on Mac and have brew installed:

```
brew install pyenv
```

Update your `~/.bash_profile` with the following lines:

```
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
```

After that, do:

```
source ~/.bash_profile
```

### Django App Setup

This project assumes you have a running version of Postgresql. If you are on a Mac, it will automatially install and run Postgres with `brew`.

Type `make setup` to initialize the virtualenv (with pipenv), install all dependencies, and provision the Postgres database for this project. Migrations will also be executed.

## Running the Project Locally

In order to run the project locally, you'll need to set some environment variables in your `.env` file. Open your `.env` file and adjust the `DJANGO_IMG_FLIP_USER` value to be the value of your `imgflip.com` username. Do the same for the `DJANGO_IMG_FLIP_PASSWORD` field. You need an `imgflip.com` account in order to run the project.

Activate your pipenv shell with `pipenv shell` and then type `python manage.py runserver`. You can also type `pipenv run python manage.py runserver`. The website can be accessed at `127.0.0.1:8000`

## Running Tests

Activate your virtualenv with `pipenv shell` and type `pytest` to run tests. You can also type `pipenv run pytest`

