from __future__ import annotations


class Hymn:
    def __init__(self, uid: str, title: str, lyrics: tuple[tuple[str]]):
        self._uid: str = uid
        self._title: str = title
        self._lyrics: tuple[tuple[str]] = lyrics
        self._chords: tuple[tuple[str]] | None = None

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
    def chords(self) -> tuple[tuple[str]] | None:
        return self._chords

    @chords.setter
    def chords(self, new_chords: tuple[tuple[str]] | None) -> None:
        self._validate_chords(new_chords)
        self._chords = new_chords

    def _validate_chords(self, chords: tuple[tuple[str]] | None) -> None:
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
        if chords is None:
            return

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
        }

    @classmethod
    def from_dict(cls, data: dict) -> Hymn:
        hymn = cls(data["uid"], data["title"], data["lyrics"])
        hymn.chords = data["chords"]
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
