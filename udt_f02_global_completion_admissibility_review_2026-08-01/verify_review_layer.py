#!/usr/bin/env python3
"""Fail-closed verification of the append-only F02 external-review layer."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PARENT = ROOT / "udt_f02_global_completion_admissibility_2026-08-01"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


checks: list[dict[str, object]] = []


def check(name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "pass": bool(passed), "detail": detail})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


check(
    "parent_manifest_file_identity",
    sha256(PARENT / "PACKAGE_MANIFEST.sha256")
    == "d15feffade73d8a90dc0e5e99523be6bdb7811a02643a13ef7898e9a63445832",
    "the frozen parent manifest file must remain byte-identical",
)
parent_replay = subprocess.run(
    ["python3", str(PARENT / "verify_package_manifest.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
check(
    "parent_manifest_replay",
    parent_replay.returncode == 0,
    f"parent verifier exit={parent_replay.returncode}",
)
route_c = ROOT / "udt_p4_routeC_shared_static_sector_2026-07-28/EXACT_DERIVATION.md"
check(
    "added_source_identity",
    route_c.stat().st_size == 21110
    and sha256(route_c) == "648546c63542b996081615079deea8df84e2c068f493b9b201fb444c1f2ce163",
    "registered Route-C toric-chart source must match the frozen bytes and SHA-256",
)
review = HERE / "COLD_REVIEW.md"
check(
    "cold_review_identity",
    review.stat().st_size == 4805
    and sha256(review) == "110fc4c9421f73111def5bbf97e4c3778bbaa3975d8b04130e8265e77efd77b9",
    "banked final review must equal the external text with only one terminal newline added",
)
raw_review = HERE / "COLD_REVIEW_RAW.txt"
check(
    "cold_review_raw_identity",
    raw_review.stat().st_size == 4804
    and sha256(raw_review) == "a4b31ade00ac7fc262d9fcb28652bc2f5abea1cc7ccc99be96ecda2710ff29c9",
    "raw final-review output must be preserved byte-identically",
)
transcript = HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt"
check(
    "external_transcript_identity",
    transcript.stat().st_size == 273513
    and sha256(transcript) == "6d0eb68caf7000d80163a3e861e8662d65a1b2e312caecb76c04e79330bee907",
    "raw external-review terminal transcript must be preserved byte-identically",
)
correction = (HERE / "CORRECTION_LAYER.md").read_text(encoding="utf-8")
required = [
    "OPEN_INCOMPLETE_REGISTERED_CLOSURE_DATA",
    "q_B = exp(2 lambda phi) (dx^2 + bh(x) dy^2)",
    "q_B(dx,dx)=exp(2 lambda phi)=1",
    "df/dx -> 0",
    "dbh/dx -> 0",
    "does not select a cap, fold, boundary, action, response law, carrier, source, or physical",
]
check(
    "correction_scope_and_derivation",
    all(token in correction for token in required),
    "correction must close only the normalization premise and preserve all open scopes",
)
source_row = (HERE / "SOURCE_ADDITION.tsv").read_text(encoding="utf-8")
check(
    "source_inventory_addition",
    "648546c63542b996081615079deea8df84e2c068f493b9b201fb444c1f2ce163" in source_row
    and "registered_toric_chart_and_unit_x_weight_source" in source_row,
    "the omitted registered source must be frozen in the append-only layer",
)

result = {
    "status": "PASS",
    "checks_passed": sum(int(row["pass"]) for row in checks),
    "checks_total": len(checks),
    "review_verdict": "PASS-WITH-REQUIRED-REPAIRS",
    "repair_status": "CLOSED_APPEND_ONLY",
    "maximum_conclusion": "OPEN_INCOMPLETE_REGISTERED_CLOSURE_DATA",
    "checks": checks,
}
(HERE / "VERIFICATION_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, indent=2, sort_keys=True))
