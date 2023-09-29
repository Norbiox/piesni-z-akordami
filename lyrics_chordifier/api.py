from flask import Blueprint, current_app as app

from .repository import S3ApplicactionRepository
from .s3 import get_s3_client

blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/hymn/<name>", methods=["GET"])
def hymn(name: str):
    repo = S3ApplicactionRepository(get_s3_client(app), None)
    return repo.get_hymn(name)


@blueprint.route("/hymns", methods=["GET"])
def hymns():
    repo = S3ApplicactionRepository(get_s3_client(app), None)
    return repo.get_hymns()


@blueprint.route("/hymns_with_lyrics", methods=["GET"])
def hymns_with_lyrics():
    repo = S3ApplicactionRepository(get_s3_client(app), None)
    return repo.get_hymns_with_lyrics()
