import os

import ZODB
import ZODB.FileStorage
from loguru import logger
from tqdm import tqdm

from .models import Hymn


def create_database(hymns_texts_directory: str, db_path: str) -> ZODB.DB:
    """Create an instance of ZODB database"""
    logger.info("Creating ZODB database")
    database = ZODB.DB(ZODB.FileStorage.FileStorage(db_path))
    with database.transaction() as connection:
        if not connection.root():
            logger.info(f"Inserting hymns...")
            for file in tqdm(os.listdir(hymns_texts_directory)):
                hymn = Hymn.from_text(
                    file,
                    open(os.path.join(hymns_texts_directory, file), "r", encoding="utf-8").read(),
                )
                connection.add(hymn)
    return database
