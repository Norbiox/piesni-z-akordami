from tinydb import Query, TinyDB
from .models import Hymn


class HymnRepository:
    def __init__(self, database: TinyDB) -> None:
        self.database = database

    def add_hymn(self, hymn: Hymn) -> None:
        if self.database.get(Query().uid == hymn.uid):
            raise ValueError(f"Hymn with uid {hymn.uid} already exists")
        self.database.insert(hymn.to_dict())

    def get_hymns(self) -> list[Hymn]:
        return [Hymn.from_dict(doc) for doc in self.database.all()]

    def get_hymn_by_uid(self, uid: str) -> Hymn:
        hymn = self.database.get(Query().uid == uid)

        if not isinstance(hymn, dict):
            raise ValueError(f"Multiple hymns with uid {uid} found")

        return Hymn.from_dict(hymn)
