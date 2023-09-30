from __future__ import annotations

import roman


class Hymn:
    def __init__(
        self,
        uid: str,
        title: str,
        lyrics: tuple[tuple[str]],
        chords: tuple[tuple[str]] | None = None,
        chords_verified: bool = False,
    ):
        self._uid: str = uid
        self._title: str = title
        self._lyrics: tuple[tuple[str]] = lyrics
        chords = chords or tuple(tuple("" for _ in line) for line in lyrics)
        self._validate_chords(chords)
        self._chords: tuple[tuple[str]] = chords
        self.chords_verified = chords_verified

    @classmethod
    def from_text(cls, uid: str, text: str) -> Hymn:
        """Creates hymn from text"""
        return cls(uid, title(text), lyrics(text))

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def title(self) -> str:
        return self._title

    @property
    def lyrics(self) -> tuple[tuple[str]]:
        return self._lyrics

    @property
    def chords(self) -> tuple[tuple[str]]:
        return self._chords

    @chords.setter
    def chords(self, new_chords: tuple[tuple[str]]) -> None:
        self._validate_chords(new_chords)
        self._chords = new_chords

    @property
    def has_chords(self) -> bool:
        """Checks if hymn has any chords

        >>> hymn = Hymn("x", "Title", (("A", "n"), ("L", "i", "n", "e")))
        >>> hymn.has_chords
        False
        >>> hymn.chords = (("", ""), ("C", "", "", ""))
        >>> hymn.has_chords
        True
        """
        return any(''.join(line) for line in self.chords)

    @property
    def number(self) -> int:
        """Returns hymn number"""
        num = self.title.split()[0].strip(".")
        try:
            return int(num)
        except ValueError:
            return 875 + roman.fromRoman(num)

    def _validate_chords(self, chords: tuple[tuple[str]]) -> None:
        """Checks validity of set of chords versus hymns lyrics

        >>> hymn = Hymn.from_text("test", "1. Title\\nLine1")
        >>> hymn._validate_chords(()) # missing lines
        Traceback (most recent call last):
            ...
        ValueError: Wrong number of lines: expected 1, got 0
        >>> hymn._validate_chords((("", "", "", "", ""), ("", ""))) # too many lines
        Traceback (most recent call last):
            ...
        ValueError: Wrong number of lines: expected 1, got 2
        >>> hymn._validate_chords((("", "", "", ""),))  # missing character
        Traceback (most recent call last):
            ...
        ValueError: Line 1 - wrong number of chords: expected 5, got 4
        >>> hymn._validate_chords((("", "", "", "", "", ""),))  # too many characters
        Traceback (most recent call last):
            ...
        ValueError: Line 1 - wrong number of chords: expected 5, got 6
        """
        if len(chords) != len(self.lyrics):
            raise ValueError(
                f"Wrong number of lines: expected {len(self.lyrics)}, got {len(chords)}"
            )
        for i, (chords_line, lyrics_line) in enumerate(zip(chords, self.lyrics)):
            if len(chords_line) != len(lyrics_line):
                raise ValueError(
                    f"Line {i+1} - wrong number of chords: expected {len(lyrics_line)}, got {len(chords_line)}"
                )

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "title": self.title,
            "lyrics": self.lyrics,
            "chords": self.chords,
            "chords_verified": self.chords_verified,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Hymn:
        hymn = cls(**data)
        return hymn


def title(hymn: str) -> str:
    """Returns title of hymn found in it's first line

    >>> title("1. Title\\n\\nLine1\\n\\nLine2")
    '1. Title'
    """
    return hymn.split("\n")[0]


def lyrics(hymn: str) -> tuple[tuple[str]]:
    """Returns lyrics of hymn as characters per line

    >>> lyrics("1. Title\\nLine1\\nLine2")
    (('L', 'i', 'n', 'e', '1'), ('L', 'i', 'n', 'e', '2'))
    >>> lyrics("1. Title\\n\\nLine1\\n\\nLine2")
    (('L', 'i', 'n', 'e', '1'), ('L', 'i', 'n', 'e', '2'))
    >>> lyrics("1. Title\\nLine with spaces")
    (('L', 'i', 'n', 'e', ' ', 'w', 'i', 't', 'h', ' ', 's', 'p', 'a', 'c', 'e', 's'),)
    """
    return tuple(tuple(line) for line in hymn.replace("\n\n", "\n").split("\n")[1:])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
