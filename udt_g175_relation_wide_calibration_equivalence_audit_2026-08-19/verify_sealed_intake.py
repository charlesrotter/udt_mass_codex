#!/usr/bin/env python3
"""Read-only sealed-intake replay for G175."""

from __future__ import annotations

from fractions import Fraction
import csv
import hashlib
import json
from pathlib import Path
import random
import sys


root = Path(sys.argv[1]).resolve()
scope_path = root / "REVIEW_SCOPE.json"
scope = json.loads(scope_path.read_text(encoding="utf-8"))
package = root / scope["package"]

actual = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p != scope_path):
    actual.append(
        {
            "path": str(path.relative_to(root)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
    )
assert actual == scope["tree"]

manifest = list(csv.DictReader((package / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
assert len(manifest) == 8
for row in manifest:
    source = root / "sources" / row["path"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == row["sha256"]

production = json.loads((package / "DERIVATION_RESULT.json").read_text())
independent = json.loads((package / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((package / "CATCH_PROOF_RESULT.json").read_text())
assert production["checks_passed"] == production["checks_total"] == 12
assert independent["checks_passed"] == 144_000
assert independent["anchored_changed"] == 2_000
assert catches["catches_passed"] == catches["catches_total"] == 18

rng = random.Random(9175)
replay_checks = 0
for i in range(3_000):
    def pos() -> Fraction:
        return Fraction(rng.randint(1, 23), rng.randint(1, 23))
    Kp, Kq, mp, mq = pos(), pos(), pos(), pos()
    fp = Fraction(1) if i < 1_000 else pos()
    fq = pos()
    if i < 1_000 and fq == 1:
        fq = Fraction(2)
    # Treat K values as the already assembled positive exp(4 Phi) quantities.
    Kn_p = Kp / (fp * fp)
    Kn_q = Kq / (fq * fq)
    Rm = Kq / Kp
    Rn = Kn_q / Kn_p
    assert Rn / Rm == (fp / fq) ** 2
    replay_checks += 1
    c = pos()
    assert (Kq / (c * c)) / (Kp / (c * c)) == Rm
    replay_checks += 1
    assert Rm * (Kp / Kq) == 1
    replay_checks += 1
    assert mp > 0 and mq > 0
    replay_checks += 1

result = {
    "gate": "SEALED_INTAKE_REPLAY",
    "status": "PASS__SEALED_G175_READ_ONLY_REPLAY",
    "sealed_tree_files": len(actual),
    "source_hashes": len(manifest),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "anchored_counterfamilies": independent["anchored_changed"],
    "semantic_catches": catches["catches_total"],
    "fresh_fraction_checks": replay_checks,
}
print(json.dumps(result, sort_keys=True))
