from flask import Blueprint, render_template, current_app as app

from .db import create_database

blueprint = Blueprint("views", __name__)


@blueprint.route("/", methods=["GET"])
def index() -> str:
    database = create_database(app.config["HYMNS_PATH"], app.config["DATABASE_PATH"])
    with database.transaction() as connection:
        hymns = list(connection.root().values())
    return render_template("index.html", hymns=hymns)


@blueprint.route("/edit/<uid>", methods=["GET"])
def edit(uid: str) -> str:
    database = create_database(app.config["HYMNS_PATH"], app.config["DATABASE_PATH"])
    with database.transaction() as connection:
        hymn = connection.root()[uid]
    return render_template("edit.html", hymn=hymn)
