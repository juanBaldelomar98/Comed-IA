"""Script that handles the Flask interphase"""
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, Response, jsonify
import flask


def start_ui(list_of_jokes: list, graphic) -> flask.app.Flask:
    app = Flask(__name__, static_url_path='/interphase/static')

    @app.route('/')
    def hello():
        # return render_template('base.html')
        return redirect(url_for('base'))

    @app.route("/base/", methods=["GET", "POST"])
    def base():
        return render_template('base.html')

    @app.route('/plot/')
    def plot():
        return Response(graphic.getvalue(), mimetype='image/png')

    @app.route('/script/')
    def script():
        return jsonify(list_of_jokes)
        # return jsonify(
        #     username="a",
        #     email="b",
        #     id="c"
        # )

    return app
