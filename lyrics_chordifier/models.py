from __future__ import annotations


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
