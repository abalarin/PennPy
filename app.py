from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from data import Products

# Creating a navbar object
topbar = Navbar('MyBar',
    View('Home', 'index'),
    View('Profile', 'profile'),
)

Products = Products()

def create_app():

  #Instantiate Application
  app = Flask(__name__)
  Bootstrap(app)

  # NAV Bar config
  nav = Nav()
  nav.register_element('top', topbar)

  # [...]
  # later on, initialize your app:
  nav.init_app(app)

  # Routes
  @app.route('/')
  def index():
      return render_template("index.html", products = Products)

  @app.route('/profile')
  def profile():
      return render_template("profile.html")

  return app
