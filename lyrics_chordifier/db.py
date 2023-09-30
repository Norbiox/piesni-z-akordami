import os

from loguru import logger
from tinydb import TinyDB
from tqdm import tqdm
from flask import current_app, g

from .models import Hymn


def get_database() -> TinyDB:
    """Create an instance of TinyDB database"""
    if "db" not in g:
        g.db = TinyDB(current_app.config["DATABASE_PATH"])

    if g.db.all():
        return g.db

    logger.info(f"Inserting hymns...")
    for file in tqdm(os.listdir(current_app.config["HYMNS_PATH"])):
        filepath = os.path.join(current_app.config["HYMNS_PATH"], file)
        with open(filepath, "r", encoding="utf-8") as body:
            g.db.insert(Hymn.from_text(file, body.read()).to_dict())
    return g.db
