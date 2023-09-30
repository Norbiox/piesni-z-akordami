import os

from loguru import logger
from tinydb import TinyDB
from tqdm import tqdm

from .models import Hymn


def create_database(hymns_texts_directory: str, db_path: str) -> TinyDB:
    """Create an instance of TinyDB database"""
    logger.info("Creating database...")
    database = TinyDB(db_path)
    if database.all():
        return database

    logger.info(f"Inserting hymns...")
    for file in tqdm(os.listdir(hymns_texts_directory)):
        with open(os.path.join(hymns_texts_directory, file), "r", encoding="utf-8") as body:
            database.insert(Hymn.from_text(file, body.read()).to_dict())
    return database
