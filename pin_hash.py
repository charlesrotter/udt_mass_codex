"""EOL-tolerant SHA-256 helpers for sealed pin comparisons.

Pins in this repo were sealed under mixed line-ending conditions: some on LF
(Linux/CI), some on CRLF (Windows working trees). Working trees with
core.autocrlf=true may also materialize LF blobs as CRLF.

A pin matches if ANY of these hex digests equals the sealed value:
- raw bytes as on disk
- bytes with CR LF / bare CR normalized to LF
- LF-only bytes expanded to CRLF (for seals taken on CRLF of the same text)
"""

from __future__ import annotations

import hashlib


def normalize_eol(payload: bytes) -> bytes:
    """Map CRLF and bare CR to LF."""
    return payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def pin_sha256(payload: bytes) -> str:
    """Return hex SHA-256 of EOL-normalized payload (LF form)."""
    return hashlib.sha256(normalize_eol(payload)).hexdigest()


def pin_matches(payload: bytes, expected: str) -> bool:
    """True if payload matches a sealed pin under raw, LF, or CRLF text forms."""
    raw = hashlib.sha256(payload).hexdigest()
    if raw == expected:
        return True
    lf = normalize_eol(payload)
    if hashlib.sha256(lf).hexdigest() == expected:
        return True
    # If payload is LF text, also try CRLF expansion of that text.
    if b"\r\n" not in payload and b"\n" in payload:
        crlf = lf.replace(b"\n", b"\r\n")
        if hashlib.sha256(crlf).hexdigest() == expected:
            return True
    return False
