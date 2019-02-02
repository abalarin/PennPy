from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

topbar = Navbar('MyBar',
    View('Home', 'index'),
    View('Profile', 'profile'),
)

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  nav = Nav()
  nav.register_element('top', topbar)

  # [...]
  # later on, initialize your app:
  nav.init_app(app)

  @app.route('/')
  def index():
      return render_template("index.html")

  @app.route('/profile')
  def profile():
      return render_template("profile.html")

  return app

# do something with app...
