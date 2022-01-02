
from flask import Flask, redirect, url_for, render_template
import os
import sys
sys.path.insert(0, os.getcwd()+"/src/microservices")
from recommendation import get_recommended_movie

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<title>")
def getMovies(title):
    return render_template("recommendation.html", movies=get_recommended_movie(title))


if __name__ == '__main__':
    app.run()
