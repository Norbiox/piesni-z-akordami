import os

from dotenv import load_dotenv
from flask import Flask, g

from lyrics_chordifier.db import create_database

from .views import blueprint as views_blueprint

load_dotenv()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        HYMNS_PATH=os.getenv("HYMNS_PATH", "hymns"),
        DATABASE_PATH=os.getenv("DATABASE_PATH", "data/database.fs"),
    )

    if not os.path.isdir(app.config["HYMNS_PATH"]):
        raise FileNotFoundError(app.config["HYMNS_PATH"])

    if not os.path.isdir(os.path.dirname(app.config["DATABASE_PATH"])):
        os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]))

    app.register_blueprint(views_blueprint)

    return app
