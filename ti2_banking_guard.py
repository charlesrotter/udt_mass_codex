"""G414 exact source correspondence; neither a scientific proof nor model attestation."""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess

TI2_BANKING_IDS = ("G414",)
TI2_PREFIXES = (b"G414\t",)
TI2_PACKAGE = "udt_ti2_banking_2026-09-11"
TI2_PINS = {'udt_ti2_banking_2026-09-11/BANKED_ROW.tsv': '47c8accb0510828ddaf1483e5805cd374d62d51f49617cb5813c3b00e5d459f4', 'udt_ti2_banking_2026-09-11/BANKED_CLAIM.json': '1d677b22d8aa9cfe99893e1893215010e69a30a7ea305b60fcdc1df33ab3db6c', 'udt_ti2_banking_2026-09-11/BANKING_RECORD.md': '47e89ed7551c7a842fc58504a0e10c1708f70915d1a69eef7fc4a914c062d093', 'udt_ti2_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS': '41b3523f8d684a7a61aa2d896f1e43fec3627551eda4de8559585c58a5c16f53', 'udt_ti2_banking_2026-09-11/WORK_ORDER.md': '41eb3a4d910d6ceb62f9fd02219d367c8417f1240046973145a52d46750e08de'}
TI2_ROW_SHA256 = 'fb04d470da1c8bc044048280838c561a2e373f9d39e24657cce5b93070755111'
TI2_BASE_SHA256 = '2491607030f80e6f0557cc7ed7ee7487d3637e357e0da520f8432b67190b25db'
# Fresh source-exposed banking review; actual full397 execution remains separate.
TI2_PINS.update({'udt_ti2_banking_2026-09-11/review/REVIEW.md': 'a67d9c4d2c455e74a2eef144cbd4273ccdb045b948c18fa832104f3ac4715fc4', 'udt_ti2_banking_2026-09-11/review/REVIEW_RECEIPT.json': 'fe8ca6f6d67b1a07500270a293d0adff193a338f5e6672910c45aad7332708ab'})
TI2_GUARD_FILES = tuple(TI2_PINS)


def require(ok, message):
    if not ok:
        raise SystemExit(message)


def without_ti2(raw: bytes, *, required: bool = False) -> bytes:
    """Project only an authenticated exact G414 from THIS byte snapshot.

    Absence is allowed for isolated historical guards; the current validator requires it.
    No second registry read, unvalidated substitute, or broad prefix deletion is permitted.
    """
    lines = raw.splitlines(keepends=True)
    selected = [line for line in lines if line.startswith(TI2_PREFIXES)]
    require(len(selected) <= 1 and (not required or len(selected) == 1),
            "TI2 current row missing/duplicate")
    if not selected:
        return raw
    require(hashlib.sha256(selected[0]).hexdigest() == TI2_ROW_SHA256,
            "TI2 exact row/scope changed")
    return b"".join(line for line in lines if not line.startswith(TI2_PREFIXES))


def validate_ti2_banking(root: Path, *, authenticate_sources: bool = True) -> None:
    payloads = {}
    for name, expected in TI2_PINS.items():
        target = root / name
        require(target.is_file(), f"TI2 guard file missing: {name}")
        raw = target.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, f"TI2 guard file changed: {name}")
        payloads[name] = raw
    scope = json.loads(payloads[f"{TI2_PACKAGE}/BANKED_CLAIM.json"])
    raw = (root / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
    original = without_ti2(raw, required=True)
    require(hashlib.sha256(original).hexdigest() == TI2_BASE_SHA256,
            "TI2 changed an original396 registry byte")
    expected = payloads[f"{TI2_PACKAGE}/BANKED_ROW.tsv"].splitlines(keepends=True)
    require(raw.splitlines(keepends=True)[:2] == expected, "TI2 row/header/order changed")
    rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
    by_id = {r["premise_id"]: r for r in rows}
    require(len(rows) == len(by_id) == 397, "TI2 current397 count/uniqueness changed")
    require(by_id["G414"] == scope["claim"], "TI2 claim transcription changed")
    require(set(scope["required_registry_ids"]) <= set(by_id) - {"G414"},
            "TI2 dependency closure changed")
    if not authenticate_sources:
        return
    authority = root / scope["authority_source"]
    require(authority.is_file() and hashlib.sha256(authority.read_bytes()).hexdigest()
            == scope["authority_sha256"], "TI2 authority source changed")
    entries = [line.split(maxsplit=1) for line in
               payloads[f"{TI2_PACKAGE}/SOURCE_EVIDENCE_SHA256SUMS"].decode().splitlines()]
    require(len(entries) == len({name for _, name in entries}) == 120,
            "TI2 original source membership changed")
    for expected_hash, name in entries:
        path = Path(name)
        require(not path.is_absolute() and ".." not in path.parts and
                path.parts[0] == "udt_two_shape_evolution_2026-09-11" and
                re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None,
                "TI2 unsafe source path")
        source = root / path
        require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash,
                f"TI2 original source evidence changed: {name}")
    frozen = subprocess.run(["git", "show", f"{scope['baseline_head']}:CURRENT_SCIENTIFIC_PREMISES.tsv"],
                            cwd=Path(__file__).resolve().parent, capture_output=True,
                            timeout=15, check=False)
    require(frozen.returncode == 0 and frozen.stdout == original,
            "TI2 baseline registry correspondence failed")
