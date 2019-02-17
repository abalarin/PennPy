# This is my Python Web App [PennPy](http://pennpy.com/)
The goal is to make a eCommerce site out of Python and Flask

```
Admin Login: 
username: jdoe
password: rowan
```
## Getting Started
### Required Things

* [Python](https://www.python.org/downloads/)
* [MySQL](https://dev.mysql.com/downloads/mysql/)
* [PIP](https://pip.pypa.io/en/stable/installing/)

## Directory Structure Breakdown
```
Py/
 Py/PennPy/
  Py/PennPy/endpoints/ 		API
  Py/PennPy/static/			Public Resources
  Py/PennPy/templates/		UI - HTML
   Py/PennPy/templates/includes/	HTML Components
  Py/PennPy/__init__.py			App Entry Point
  Py/PennPy/config.py				App dependecies 
 Py/venv/					Virtual Envi
 Py/setup.py	 			framework inits
 Py/readme.md

```

## [MySQL](https://dev.mysql.com/downloads/mysql/) Setup
On installation when you init a databade you should be asked to enter a password, make sure you remember it...
[More SQL Resourcees](https://pypi.org/project/mysqlclient/)

```
# Verify SQLs installed properlly
$ mysql --version
mysql  Ver 8.0.13 for osx10.14 on x86_64 (Homebrew)

# If that breaks, you might need to add mysql to your paths... 
# mine lives here: /usr/local/mysql/bin/
$ export PATH=${PATH}:/path/to/mysql/bin
```

### Create Tables
```
$ mysql -u root -p
# pass prompt

mysql> CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name varchar(100), email varchar(100), username varchar(30), password varchar(100), admin_level int(11), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
mysql> CREATE TABLE product(id varchar(255) PRIMARY KEY, name varchar(100), category varchar(100), price int(11), description varchar(255)); 
```
## [Pip](https://pip.pypa.io/en/stable/installing/) Setup
**pip** is a package management system used to install and manage software packages written in Python. You should already have **Python** installed, which should come with pip, if not:

```
# To install pip, securely download get-pip.py
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py

$ pip --version
pip 19.0.1 from /Library/Python/2.7/site-packages/pip (python 2.7)
```

## Virtualenv Setup
**Virtualenv** is a tool that lets you create an isolated **Python** environment for your project. It creates an environment that has its own installation directories, that doesn’t share dependencies with other **virtualenv** environments.

```
$ pip install virtualenv
```

## [Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) Setup
```
$ pip install Flask
```

## Project Setup

#### Clone this repo

```
$ git clone https://github.com/abalarin/PennPy.git
$ cd PennPy/
```
#### Launch the virtual env container

```
$ source venv/bin/activate
```

### Install dependecies & launch app
```
# Install app dependencies
$ pip install -e .

# Launch app
$ flask run

 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Optional dev mode

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
