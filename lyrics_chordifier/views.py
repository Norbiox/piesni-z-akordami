from flask import Blueprint, current_app as app, render_template

from lyrics_chordifier.models import title, lyrics

from .repository import S3ApplicactionRepository
from .s3 import get_s3_client

blueprint = Blueprint("views", __name__)


@blueprint.route("/", methods=["GET"])
def index() -> str:
    repo = S3ApplicactionRepository(get_s3_client(app), None)
    hymns = repo.get_hymns()
    hymns_with_lyrics = repo.get_hymns_with_lyrics()
    return render_template("index.html", hymns=hymns, hymns_with_lyrics=hymns_with_lyrics)


@blueprint.route("/edit/<name>", methods=["GET"])
def edit(name: str) -> str:
    repo = S3ApplicactionRepository(get_s3_client(app), None)
    hymn = repo.get_hymn(name)
    return render_template("edit.html", hymn_name=name, hymn_title=title(hymn), lyrics=lyrics(hymn))
