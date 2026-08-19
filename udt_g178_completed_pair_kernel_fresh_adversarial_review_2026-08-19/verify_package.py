#!/usr/bin/env python3
"""Verify the banked G178 external-review evidence without modifying files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md":
        "490fd476149d5171c981e03829be67f3abc4913e1aa2e11268d7516aaf02fb15",
    "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz":
        "c43501c1c335dcff1c03959fb5a74229cc676f63afe7e775a0fc151c4a99d7ae",
}
for name, expected in EXPECTED.items():
    actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"hash mismatch: {name}: {actual} != {expected}")

raw = (ROOT / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_text(encoding="utf-8")
if not raw.startswith("G176_G177_ACCEPTED_WITH_STATED_BOUNDS\n"):
    raise SystemExit("external landing changed")
for required in (
    "No sign error appeared.",
    "I found no residual common factor",
    "the scalar is not smuggled in whole",
    "Pair reversal is not the same operation as spatial-coordinate reversal.",
    "The only necessary caution is scope",
):
    if required not in raw:
        raise SystemExit(f"external-review boundary missing: {required}")

result = json.loads((ROOT / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
if result["landing"] != "G176_G177_ACCEPTED_WITH_STATED_BOUNDS":
    raise SystemExit("verification landing changed")
if result["scope_sha256"] != (
    "152c55aeac85d816a711f474a043a510dcfa808589237418ce8e8510262e0ffe"
):
    raise SystemExit("scope hash changed")

print(json.dumps(result, sort_keys=True))
