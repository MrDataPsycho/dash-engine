from flask import Blueprint, render_template
from flask import redirect
from utils.metaphor import APP_DATA

home = Blueprint('home', __name__)


@home.route('/')
def hello_world():
    return render_template("index.html", app_data=APP_DATA)


# @home.route("/dashboard-mystock")
# def redirect_tpg():
#     return redirect("/stock-today")

@home.route('/dashboard-default')
def redirect_default():
    return redirect("dafault-app")


@home.route('/dashboard-mystock')
def redirect_stock():
    return redirect("/stock-today")


@home.route("/sample")
def bug_in_your_face():
    return "<h1>Look carefully ! Bug In your face !</h1>"


