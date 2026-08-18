#!/usr/bin/env python3
"""Package-level verifier for G154."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "f5946fa0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_payloads(production: dict[str, object], independent: dict[str, object], report: str) -> None:
    report_flat = " ".join(report.split())
    require(production.get("status") == "PASS", "production status")
    require(independent.get("status") == "PASS", "independent status")
    require(all(production["checks"].values()), "production checks")
    require(all(independent["checks"].values()), "independent checks")
    require(
        production.get("landing_candidate")
        == "EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED",
        "landing candidate",
    )
    require(
        production["normalized_composition_countermodel"]
        == {
            "composition_residual": "0",
            "scale_derivative": "1",
            "scale_field": "X_star + q",
        },
        "normalized composition countermodel",
    )
    require(production["fixed_scale_limits"]["quiet"] == {"-1": "0", "1": "0"}, "quiet class")
    require(
        production["fixed_scale_limits"]["finite_live"]
        == {"-1": "-4*X_star/3", "1": "4*X_star/3"},
        "finite class",
    )
    require(
        production["fixed_scale_limits"]["divergent"] == {"-1": "-oo", "1": "oo"},
        "divergent class",
    )
    require(
        len(set(production["fixed_nonconvergent_subsequences"].values())) == 2,
        "nonconvergent class",
    )
    require(production["cancellation"]["response"] == "0", "cancellation response")
    require(
        "EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED" in report_flat,
        "report landing",
    )
    require("same `phi(q)`, the same `rho(q)`, and the same `X_*`" in report_flat, "same-profile scope")
    require("repair-only follow-up passed" in report_flat, "review follow-up record")
    require((HERE / "FRESH_ADVERSARIAL_REVIEW.md").is_file(), "fresh review evidence")
    require((HERE / "FRESH_ADVERSARIAL_FOLLOWUP.md").is_file(), "fresh follow-up evidence")


def verify_manifest() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 7, "manifest row count")
    for row in rows:
        path = row["source_path"]
        payload = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        require(hashlib.sha256(payload).hexdigest() == row["sha256"], f"preregistered manifest hash: {path}")


def verify_preregistration() -> None:
    committed = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/PREREGISTRATION.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    require("PREREGISTERED_BEFORE_DERIVATION" in committed, "preregistration stamp")
    require("QUIET" in committed and "FINITE_LIVE" in committed, "preregistered classes")
    require("DIVERGENT" in committed and "NONCONVERGENT" in committed, "preregistered classes")
    tree = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", PREREG_COMMIT,
         "udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    require(len(tree) == 2, "outcome files existed in preregistration commit")


def verify() -> dict[str, object]:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    verify_payloads(production, independent, report)
    verify_manifest()
    verify_preregistration()
    return {
        "status": "PASS",
        "preregistered_commit": PREREG_COMMIT,
        "production_check_count": len(production["checks"]),
        "independent_check_count": len(independent["checks"]),
        "manifest_rows": 7,
        "primary_landing": "EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED",
        "fresh_adversarial_review": "REPAIR_FOLLOWUP_PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
