"""Application service"""
from typing import Protocol

from .models import Hymn
from .repository import ApplicationRepository


class AbstractHymnsService(Protocol):
    """Abstract service for hymns lyrics and chords"""

    def get_hymn_by_name(self, name: str) -> Hymn:
        """Returns hymn"""
        raise NotImplementedError()

    def update_hymns_chords(self, name: str, chords: tuple[tuple[str]]) -> None:
        """Updates hymns chords"""
        raise NotImplementedError()


class HymnsService(AbstractHymnsService):
    """Implementation of AbstractHymnsService"""

    repository: ApplicationRepository

    def __init__(self, repository: ApplicationRepository):
        self.repository = repository
