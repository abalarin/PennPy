from flask import Blueprint, render_template
from PennPy.endpoints.products.routes import get_products

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/*')
def index():
    return render_template("index.html", products = get_products())

# @main.route('/slider')
# def silder():
#     # print(get_products())
#     # print(prods)
#     return render_template("slider_test.html")

@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)
