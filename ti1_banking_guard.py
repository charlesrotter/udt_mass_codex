"""G413 exact source correspondence; neither a scientific proof nor model attestation."""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess

TI1_BANKING_IDS = ("G413",)
TI1_PREFIXES = (b"G413\t",)
TI1_PACKAGE = "udt_ti1_banking_2026-09-11"
TI1_PINS = {'udt_ti1_banking_2026-09-11/BANKED_ROW.tsv': 'ef0298d22339dc18b26cce48ac816a60cd20e01129883a10217c694e0289729e', 'udt_ti1_banking_2026-09-11/BANKED_CLAIM.json': '31f53492a1a9746c2337d5cdbd04df0c1e8ac1aed5d85050a7cb49ebce260ab6', 'udt_ti1_banking_2026-09-11/BANKING_RECORD.md': '08216184fd508d84e6e6fd263a0499595ed1926dc9b550007a3f0328e970b89e', 'udt_ti1_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS': '96bf840ce3dbba2d2cb59d76f300a3241f533c72b813f435ff59805cbb83ea63', 'udt_ti1_banking_2026-09-11/WORK_ORDER.md': 'a9c0fdf8517dd92b2e5e8e3354a139c7e28b93150fb8618a9ffed883752485f6'}
TI1_ROW_SHA256 = '6954138c293482820332a9298bb3bebff277f9c8dd99f1fcec51c725f2f341dd'
TI1_BASE_SHA256 = '6fc63338cf5562d72d0313e2376474ad9ac908841a64e82fc74e0bc93b8ae43a'
# Sealed fresh banking review; post-repair full audit is a separate execution gate.
TI1_PINS.update({'udt_ti1_banking_2026-09-11/review/REVIEW.md': 'db42763d2df7a8584b5095b05afe25f06425c5ff1be5cc6b622d5b68a09eb0e2', 'udt_ti1_banking_2026-09-11/review/REVIEW_RECEIPT.json': '78f45b81e5271d15ea510e8d97b3458f625bf3a04cc8360cd4a14885c6cc77a8'})
TI1_GUARD_FILES = tuple(TI1_PINS)


def require(ok, message):
    if not ok:
        raise SystemExit(message)


def without_ti1(raw: bytes, *, required: bool = False) -> bytes:
    """Project only an authenticated exact G413 from THIS byte snapshot.

    Absence is allowed for isolated historical guards; the current validator requires it.
    No second registry read, unvalidated substitute, or broad prefix deletion is permitted.
    """
    lines = raw.splitlines(keepends=True)
    selected = [line for line in lines if line.startswith(TI1_PREFIXES)]
    require(len(selected) <= 1 and (not required or len(selected) == 1),
            "TI1 current row missing/duplicate")
    if not selected:
        return raw
    require(hashlib.sha256(selected[0]).hexdigest() == TI1_ROW_SHA256,
            "TI1 exact row/scope changed")
    return b"".join(line for line in lines if not line.startswith(TI1_PREFIXES))


def validate_ti1_banking(root: Path, *, authenticate_sources: bool = True) -> None:
    payloads = {}
    for name, expected in TI1_PINS.items():
        target = root / name
        require(target.is_file(), f"TI1 guard file missing: {name}")
        raw = target.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, f"TI1 guard file changed: {name}")
        payloads[name] = raw
    scope = json.loads(payloads[f"{TI1_PACKAGE}/BANKED_CLAIM.json"])
    raw = (root / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
    original = without_ti1(raw, required=True)
    require(hashlib.sha256(original).hexdigest() == TI1_BASE_SHA256,
            "TI1 changed an original395 registry byte")
    expected = payloads[f"{TI1_PACKAGE}/BANKED_ROW.tsv"].splitlines(keepends=True)
    require(raw.splitlines(keepends=True)[:2] == expected, "TI1 row/header/order changed")
    rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
    by_id = {r["premise_id"]: r for r in rows}
    require(len(rows) == len(by_id) == 396, "TI1 current396 count/uniqueness changed")
    require(by_id["G413"] == scope["claim"], "TI1 claim transcription changed")
    require(set(scope["required_registry_ids"]) <= set(by_id) - {"G413"},
            "TI1 dependency closure changed")
    if not authenticate_sources:
        return
    authority = root / scope["authority_source"]
    require(authority.is_file() and hashlib.sha256(authority.read_bytes()).hexdigest()
            == scope["authority_sha256"], "TI1 authority source changed")
    entries = [line.split(maxsplit=1) for line in
               payloads[f"{TI1_PACKAGE}/SOURCE_EVIDENCE_SHA256SUMS"].decode().splitlines()]
    require(len(entries) == len({name for _, name in entries}) == 103,
            "TI1 original source membership changed")
    for expected_hash, name in entries:
        path = Path(name)
        require(not path.is_absolute() and ".." not in path.parts and
                path.parts[0] == "udt_two_shape_nonlinear_interaction_2026-09-11" and
                re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None,
                "TI1 unsafe source path")
        source = root / path
        require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash,
                f"TI1 original source evidence changed: {name}")
    frozen = subprocess.run(["git", "show", f"{scope['baseline_head']}:CURRENT_SCIENTIFIC_PREMISES.tsv"],
                            cwd=Path(__file__).resolve().parent, capture_output=True,
                            timeout=15, check=False)
    require(frozen.returncode == 0 and frozen.stdout == original,
            "TI1 baseline registry correspondence failed")
