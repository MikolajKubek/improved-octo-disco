from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template("greeting.html", name=name)
