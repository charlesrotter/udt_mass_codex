"""G415 exact source correspondence; reused TI2 guard pattern, not scientific proof."""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess
from signal_chain_banking_guard import without_signal_chain

NCB1_BANKING_IDS = ("G415",)
NCB1_PREFIXES = (b"G415\t",)
NCB1_PACKAGE = "udt_ncb1_banking_2026-09-12"
NCB1_PINS = {'udt_ncb1_banking_2026-09-12/WORK_ORDER.md': '722fef633200f631ffcc9ed3b53022082f1d97a1167f3c08a574e928b91d39dc', 'udt_ncb1_banking_2026-09-12/BANKING_RECORD.md': '4a888a6552360e71b97372623fe135458a546311c8e73a4ac9e99302e1be8022', 'udt_ncb1_banking_2026-09-12/BANKED_CLAIM.json': '5f3cf970623a4e51a6c19d22feb3850d188dcd0a8541055917f230e2e25f2f42', 'udt_ncb1_banking_2026-09-12/BANKED_ROW.tsv': 'f3f884ce4322e8560ea70f0d6efe9d39b5e754d123a7b768f0d49ad82a833def', 'udt_ncb1_banking_2026-09-12/SOURCE_EVIDENCE_SHA256SUMS': '6eafd142e118c31dfcd004a4ff333ebcefdfd116d9e8c6aded230933cbe34dd8', 'udt_ncb1_banking_2026-09-12/review/REVIEW.md': 'a4c7559f843b298764e50bcead0f4a603961c440bedbb147214056a420172116', 'udt_ncb1_banking_2026-09-12/review/REVIEW_RECEIPT.json': 'e32d6c29b8526f0015ddff7ed668488d64156f13275bed95457bd6ca245e8a8b'}
NCB1_ROW_SHA256 = '05f0ac3a8f0fb77c5c5b3a1f613d011f36f56658d19ce2cc5532e0744b74db84'
NCB1_BASE_SHA256 = '2c27fa4b8931672c44b4d778aab0f2a2631c04a5c586358340db1dc763b74f7e'
NCB1_GUARD_FILES = tuple(NCB1_PINS)


def require(ok, message):
    if not ok:
        raise SystemExit(message)


def without_ncb1(raw: bytes, *, required: bool = False) -> bytes:
    """Project only an authenticated exact G415 from THIS byte snapshot.

    Absence is allowed for isolated historical guards; the current validator requires it.
    No second registry read, unvalidated substitute, or broad prefix deletion is permitted.
    """
    raw = without_signal_chain(raw)
    lines = raw.splitlines(keepends=True)
    selected = [line for line in lines if line.startswith(NCB1_PREFIXES)]
    require(len(selected) <= 1 and (not required or len(selected) == 1),
            "NCB1 current row missing/duplicate")
    if not selected:
        return raw
    require(hashlib.sha256(selected[0]).hexdigest() == NCB1_ROW_SHA256,
            "NCB1 exact row/scope changed")
    return b"".join(line for line in lines if not line.startswith(NCB1_PREFIXES))


def validate_ncb1_banking(root: Path, *, authenticate_sources: bool = True) -> None:
    payloads = {}
    for name, expected in NCB1_PINS.items():
        target = root / name
        require(target.is_file(), f"NCB1 guard file missing: {name}")
        raw = target.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, f"NCB1 guard file changed: {name}")
        payloads[name] = raw
    scope = json.loads(payloads[f"{NCB1_PACKAGE}/BANKED_CLAIM.json"])
    raw = without_signal_chain((root / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes())
    original = without_ncb1(raw, required=True)
    require(hashlib.sha256(original).hexdigest() == NCB1_BASE_SHA256,
            "NCB1 changed an original397 registry byte")
    expected = payloads[f"{NCB1_PACKAGE}/BANKED_ROW.tsv"].splitlines(keepends=True)
    require(raw.splitlines(keepends=True)[:2] == expected, "NCB1 row/header/order changed")
    rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
    by_id = {r["premise_id"]: r for r in rows}
    require(len(rows) == len(by_id) == 398, "NCB1 current398 count/uniqueness changed")
    require(by_id["G415"] == scope["claim"], "NCB1 claim transcription changed")
    require(set(scope["required_registry_ids"]) <= set(by_id) - {"G415"},
            "NCB1 dependency closure changed")
    if not authenticate_sources:
        return
    authority = root / scope["authority_source"]
    require(authority.is_file() and hashlib.sha256(authority.read_bytes()).hexdigest()
            == scope["authority_sha256"], "NCB1 authority source changed")
    entries = [line.split(maxsplit=1) for line in
               payloads[f"{NCB1_PACKAGE}/SOURCE_EVIDENCE_SHA256SUMS"].decode().splitlines()]
    require(len(entries) == len({name for _, name in entries}) == 87,
            "NCB1 original source membership changed")
    for expected_hash, name in entries:
        path = Path(name)
        require(not path.is_absolute() and ".." not in path.parts and
                path.parts[0] == "udt_ne1_clock_beam_geometry_2026-09-12" and
                re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None,
                "NCB1 unsafe source path")
        source = root / path
        require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash,
                f"NCB1 original source evidence changed: {name}")
    frozen = subprocess.run(["git", "show", f"{scope['baseline_head']}:CURRENT_SCIENTIFIC_PREMISES.tsv"],
                            cwd=Path(__file__).resolve().parent, capture_output=True,
                            timeout=15, check=False)
    require(frozen.returncode == 0 and frozen.stdout == original,
            "NCB1 baseline registry correspondence failed")
