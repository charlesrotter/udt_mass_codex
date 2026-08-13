#!/usr/bin/env python3
"""Verify the frozen R0 angular-pattern preregistration without evaluating a pattern."""

from __future__ import annotations

import csv
import gzip
import hashlib
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = {
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "DATA_MANIFEST.tsv",
    "SOURCE_MANIFEST.tsv",
    "DOWNLOAD_LEDGER.tsv",
    "METHOD_MAP.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
}
FORBIDDEN = {
    "PATTERN_ATLAS.tsv",
    "COVARIANCE.npy",
    "RESULT.json",
    "AUDIT_REPORT.md",
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(16 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_value(card: str) -> object:
    """Parse the small FITS value subset needed by this verifier."""
    raw = card[10:80].split("/", 1)[0].strip()
    if raw.startswith("'"):
        return raw.strip().strip("'").strip()
    if raw in {"T", "F"}:
        return raw == "T"
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw.replace("D", "E"))
        except ValueError:
            return raw


def read_header(handle: gzip.GzipFile) -> dict[str, object]:
    header: dict[str, object] = {}
    found_end = False
    while not found_end:
        block = handle.read(2880)
        assert len(block) == 2880, "truncated FITS header"
        for offset in range(0, 2880, 80):
            card = block[offset : offset + 80].decode("ascii")
            key = card[:8].strip()
            if key == "END":
                found_end = True
                break
            if key and card[8:10] == "= ":
                header[key] = parse_value(card)
    return header


def skip_hdu_data(handle: gzip.GzipFile, header: dict[str, object]) -> None:
    bitpix = abs(int(header.get("BITPIX", 8)))
    naxis = int(header.get("NAXIS", 0))
    axes = [int(header.get(f"NAXIS{i}", 0)) for i in range(1, naxis + 1)]
    elements = math.prod(axes) if axes else 0
    size = (bitpix // 8) * elements
    size = (size + int(header.get("PCOUNT", 0))) * int(header.get("GCOUNT", 1))
    padded = ((size + 2879) // 2880) * 2880
    if padded:
        handle.seek(padded, 1)


def read_table_schema(path: Path) -> tuple[int, set[str]]:
    """Read only the first two FITS headers from a gzip stream."""
    with gzip.open(path, "rb") as handle:
        primary = read_header(handle)
        skip_hdu_data(handle, primary)
        table = read_header(handle)
    fields = int(table["TFIELDS"])
    names = {str(table[f"TTYPE{i}"]) for i in range(1, fields + 1)}
    return int(table["NAXIS2"]), names


def main() -> int:
    full_hash = "--full-hash" in sys.argv[1:]
    missing = sorted(name for name in REQUIRED if not (ROOT / name).is_file())
    present_forbidden = sorted(name for name in FORBIDDEN if (ROOT / name).exists())
    assert not missing, f"missing preregistration files: {missing}"
    assert not present_forbidden, f"outcome artifacts exist before execution: {present_forbidden}"

    premises = read_tsv("PREMISE_LEDGER.tsv")
    gates = read_tsv("FALSIFICATION_CONTRACT.tsv")
    data = read_tsv("DATA_MANIFEST.tsv")
    sources = read_tsv("SOURCE_MANIFEST.tsv")

    assert len(premises) == 18
    assert len(gates) == 14
    assert len(data) == 8
    assert len(sources) == 10
    assert len({row["id"] for row in premises}) == len(premises)
    assert len({row["gate"] for row in gates}) == len(gates)
    assert {row["kind"] for row in data} == {"data", "random"}
    assert {row["sample"] for row in data} == {"LOWZ", "CMASS"}
    assert {row["cap"] for row in data} == {"North", "South"}

    for row in data:
        path = Path(row["path"])
        assert path.is_file(), f"missing data file: {path}"
        assert path.stat().st_size == int(row["bytes"]), f"byte mismatch: {path}"
        rows, names = read_table_schema(path)
        assert rows == int(row["rows"]), f"row mismatch: {path}"
        allowed = set(row["allowed_fields"].split(","))
        assert allowed <= names, f"missing allowed field in {path}: {sorted(allowed - names)}"
        if full_hash:
            assert sha256(path) == row["sha256"], f"SHA-256 mismatch: {path}"

    text = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for forbidden_term in ("D_M", "D_H", "D_V", "r_d", "WEIGHT_FKP"):
        assert forbidden_term in text, f"missing explicit exclusion: {forbidden_term}"

    mode = "full hashes" if full_hash else "size/row/schema"
    print(
        f"PASS: R0 preregistration ({len(premises)} premises, {len(gates)} gates, "
        f"{len(data)} inputs; {mode}; no outcome artifacts)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
