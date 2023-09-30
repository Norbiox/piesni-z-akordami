from flask import Blueprint, render_template, current_app as app

from .db import create_database
from .repository import HymnRepository

blueprint = Blueprint("views", __name__)


@blueprint.route("/", methods=["GET"])
def index() -> str:
    database = create_database(app.config["HYMNS_PATH"], app.config["DATABASE_PATH"])
    repo = HymnRepository(database)
    return render_template("index.html", hymns=repo.get_hymns())


@blueprint.route("/edit/<uid>", methods=["GET"])
def edit(uid: str) -> str:
    database = create_database(app.config["HYMNS_PATH"], app.config["DATABASE_PATH"])
    repo = HymnRepository(database)
    return render_template("edit.html", hymn=repo.get_hymn_by_uid(uid))
