"""Correct filename-token boundary rules for the R1A correction layer."""

from __future__ import annotations


LEFT_CONTINUATION = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
)
RIGHT_CONTINUATION = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
)


def is_reference_at(text: str, start: int, token: str) -> bool:
    """Return whether token at start is a standalone filename reference.

    A trailing period is punctuation unless it begins an alphanumeric filename
    suffix. Thus ``file.md.`` matches while ``file.md.bak`` does not.
    """

    if not text.startswith(token, start):
        return False
    if start and text[start - 1] in LEFT_CONTINUATION:
        return False
    end = start + len(token)
    if end == len(text):
        return True
    following = text[end]
    if following in RIGHT_CONTINUATION:
        return False
    if following == "." and end + 1 < len(text):
        return text[end + 1] not in RIGHT_CONTINUATION
    return True


def occurrences(text: str, token: str) -> list[int]:
    found: list[int] = []
    start = 0
    while True:
        start = text.find(token, start)
        if start < 0:
            return found
        if is_reference_at(text, start, token):
            found.append(start)
        start += len(token)


def catchproof() -> dict[str, str]:
    assert occurrences("See file.md.", "file.md")
    assert occurrences("See file.md)", "file.md")
    assert not occurrences("Backup file.md.bak", "file.md")
    return {
        "sentence_period_detected": "PASS",
        "closing_parenthesis_detected": "PASS",
        "backup_suffix_rejected": "PASS",
    }
