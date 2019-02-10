# This is my Python Web App
The goal is to make a eCommerce site out of Python and Flask

## Directory Structure Breakdown
```
PennPy/		
	public/		All public content/images will be placed here
	static/		Location of all JS & CSS
	templates/	HTML of all full pages
		includes/	HTML of components, and items that exsist across all pages
	venv/			virtual environment
	app.py			Entry point to the app
	requirments.txt	Required packages init file
```

## Getting Started
You'll first want to make sure you have [Virtualenv](https://virtualenv.pypa.io/en/latest/) installed. Virtualenv is a tool that lets you create an isolated Python environment for your project. It creates an environment that has its own installation directories, that doesn’t share dependencies with other virtualenv environments.

#### For mac:
```
$ pip install virtualenv
```

#### You will also need [Python](https://www.python.org/downloads/) and [Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask)
```
# Check your Python version
$ python --version
Python 3.7.2

# Install Flask
$ pip install Flask
```

#### Clone, venv, install dependencies

```
$ git clone https://github.com/abalarin/PennPy.git
$ cd PennPy/

# Launch you virtual env container
$ source venv/bin/activate

# Install app dependencies
$ pip install -r requirments.txt

# Launch app
$ flask run

 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Optional

You probably want to run this app in dev mode, so that everytime you save a file it propogates on the server & you get stack trace for error displayed on browser

```
$ export FLASK_ENV=development
$ flask run

 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 222-305-860

```

## Setting up SQL

To do...