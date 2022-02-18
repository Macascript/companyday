from crypt import methods
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://app:companyday@macascript.com/companyday"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/registered", methods=["GET","POST"])
def profile():
    if request.method == "POST":
        # TODO: distintos parámetros que recibe del formulario
        name = request.form["name"]


if __name__ == '__main__':
    app.run(port=5000,debug=True)