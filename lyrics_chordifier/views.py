from flask import Blueprint, render_template

from .db import get_database
from .repository import HymnRepository

blueprint = Blueprint("views", __name__)


@blueprint.route("/", methods=["GET"])
def index() -> str:
    repo = HymnRepository(get_database())
    return render_template("index.html", hymns=repo.get_hymns())


@blueprint.route("/edit/<uid>", methods=["GET"])
def edit(uid: str) -> str:
    repo = HymnRepository(get_database())
    return render_template("edit.html", hymn=repo.get_hymn_by_uid(uid))
