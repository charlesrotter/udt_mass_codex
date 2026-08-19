#!/usr/bin/env python3
"""Independent fail-closed verification of saved G177 evidence."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    manifest = (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    require(len(manifest) == 10, "nine-source manifest required")
    for row in manifest[1:]:
        expected, relative, _role = row.split("\t")
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        if actual != expected and relative == "AGENTS.md":
            frozen = subprocess.run(
                ["git", "show", f"1dadbb04:{relative}"],
                cwd=REPO,
                capture_output=True,
                check=False,
            )
            require(frozen.returncode == 0, "cannot read frozen AGENTS.md blob")
            actual = hashlib.sha256(frozen.stdout).hexdigest()
        require(actual == expected, relative)

    audit = json.loads((ROOT / "AUDIT_RESULT.json").read_text(encoding="utf-8"))
    ast_result = json.loads((ROOT / "AST_DEPENDENCY_CENSUS.json").read_text(encoding="utf-8"))
    reconstruction = json.loads((ROOT / "INDEPENDENT_RECONSTRUCTION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "SCAFFOLD_DELETION_CATCHES.json").read_text(encoding="utf-8"))
    require(audit["pass"] is True and audit["source_hash_count"] == 9, "audit result")
    require(ast_result["pass"] is True and not ast_result["present_banned_identifiers"], "AST census")
    require(reconstruction["trials"] == 25_000, "trial count")
    require(reconstruction["exact_assertions"] == 200_000, "assertion count")
    require(catches["count"] == 28 and catches["pass"] is True, "deletion catches")

    # Four hand-recomputed raw matrices, independent of both production scripts.
    witnesses = (
        (Fraction(-4), Fraction(1), Fraction(3)),
        (Fraction(-9, 4), Fraction(-2, 3), Fraction(5, 2)),
        (Fraction(-1, 7), Fraction(5, 6), Fraction(11, 3)),
        (Fraction(-16, 9), Fraction(0), Fraction(7, 5)),
    )
    for h00, h01, h11 in witnesses:
        determinant = h00 * h11 - h01 * h01
        T2 = -h00
        L2 = h11 - h01 * h01 / h00
        m2 = -determinant
        require(determinant < 0 and T2 > 0 and L2 > 0, "witness regularity")
        require(T2 * L2 == m2, "witness identity")
        require(determinant / m2 == -1, "witness normalization")

    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (ROOT / "LOAD_BEARING_DEPENDENCY.tsv").read_text(encoding="utf-8")
    for token in (
        "SCAFFOLD_FREE_BOUNDED_KERNEL",
        "PHYSICAL_EVENT_AND_GERM_REALIZATION_REMAINS_OPEN",
        "D06\tm=T*L_sigma=sqrt(-det h_sigma)",
    ):
        require(token in report + ledger, f"missing semantic token: {token}")

    result = {
        "audit": "G177",
        "status": "PASS__VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_REVIEW_PENDING",
        "source_hashes": 9,
        "independent_trials": 25_000,
        "independent_exact_assertions": 200_000,
        "deletion_catches": 28,
        "hand_witnesses": len(witnesses),
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
