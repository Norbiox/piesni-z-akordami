from flask import Blueprint, render_template, request

from lyrics_chordifier.models import Hymn

from .db import get_database
from .repository import HymnRepository

blueprint = Blueprint("views", __name__)


@blueprint.route("/", methods=["GET"])
def index() -> str:
    repo = HymnRepository(get_database())
    return render_template("index.html", hymns=sorted(repo.get_hymns(), key=lambda x: x.number))


@blueprint.route("/edit/<uid>", methods=["GET"])
def edit(uid: str) -> str:
    repo = HymnRepository(get_database())
    return render_template("edit.html", hymn=repo.get_hymn_by_uid(uid))


@blueprint.route("/add_chord/<uid>", methods=["POST"])
def add_chord(uid: str) -> str:
    line = int(request.json["line"])
    character = int(request.json["character"])
    chord = request.json["chord"] or ""

    repo = HymnRepository(get_database())
    hymn: Hymn = repo.get_hymn_by_uid(uid)
    hymn.set_chord(line, character, chord)
    repo.save_hymn(hymn)

    return "OK"
