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
EXTERNAL_PREREG_COMMIT = "0585ba28"
EXTERNAL_SCRIPT_SHA256 = "e9dd2cad59ebd8982dd3d2af4f65d94589f3b6d9491429bc4443871057c0a79f"
EXTERNAL_OUTPUT_SHA256 = "921bd14a2c94888f6740d49138aa247dec033c2e7e02edc46bfdb8516457895d"


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


def verify_external_payloads(
    final_result: dict[str, object],
    first_result: dict[str, object],
    adjudication: str,
    supplied_output: str,
) -> None:
    adjudication_flat = " ".join(adjudication.split())
    require(final_result.get("status") == "PASS", "external independent final status")
    require(
        final_result.get("landing") == "ACCEPT_CONFORMAL_NETWORK_NONSELECTION_WITH_CAVEATS",
        "external independent landing",
    )
    require(all(final_result["checks"].values()), "external independent checks")
    require(len(final_result["checks"]) == 12, "external independent check count")
    require(first_result.get("status") == "FAIL", "external first run preserved failure")
    require(
        first_result["checks"]["divergent_class_four_orders"] is False,
        "external first run expected tail failure",
    )
    require(
        sum(not value for value in first_result["checks"].values()) == 1,
        "external first run only expected tail failure",
    )
    require(
        "CONFORMAL_NETWORK_NONSELECTION__CURRENT_IDENTITIES_ONLY_EVALUATE_SUPPLIED_HISTORY"
        in adjudication_flat,
        "external adjudication primary landing",
    )
    require("different complete network" in adjudication_flat, "full-network caveat")
    require("not declared gauge" in adjudication_flat, "common-scale physical caveat")
    require("permissive bookkeeping" in adjudication_flat, "kappa descent caveat")
    require("ALL CHECKS PASSED" in supplied_output, "supplied successful output")


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


def verify_external_preregistration() -> None:
    path = (
        "udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/"
        "EXTERNAL_REVIEW_VERIFICATION_PREREGISTRATION.md"
    )
    committed = subprocess.run(
        ["git", "show", f"{EXTERNAL_PREREG_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    require(
        "PREREGISTERED_AFTER_EXTERNAL_RESULT__BEFORE_INDEPENDENT_LOCAL_IMPLEMENTATION" in committed,
        "external verification preregistration stamp",
    )
    changed = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", EXTERNAL_PREREG_COMMIT],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    require(changed == [path], "external preregistration commit scope")


def verify_external_supplied_replay() -> None:
    script = HERE / "udt_g154_common_scale_checks.py"
    output = HERE / "udt_g154_common_scale_checks_output.txt"
    require(hashlib.sha256(script.read_bytes()).hexdigest() == EXTERNAL_SCRIPT_SHA256, "external script hash")
    require(hashlib.sha256(output.read_bytes()).hexdigest() == EXTERNAL_OUTPUT_SHA256, "external output hash")
    replay = subprocess.run(
        ["python3", str(script)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    require(replay == output.read_text(encoding="utf-8"), "external supplied stdout replay")


def verify_external_manifest() -> None:
    with (HERE / "EXTERNAL_REVIEW_EVIDENCE_MANIFEST.tsv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 4, "external evidence manifest row count")
    for row in rows:
        path = ROOT / row["path"]
        require(path.is_file(), f"external evidence payload present: {row['path']}")
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"],
            f"external evidence payload hash: {row['path']}",
        )


def verify() -> dict[str, object]:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    external_final = json.loads((HERE / "EXTERNAL_REVIEW_INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    external_first = json.loads((HERE / "EXTERNAL_REVIEW_INDEPENDENT_FIRST_RUN.json").read_text(encoding="utf-8"))
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    supplied_output = (HERE / "udt_g154_common_scale_checks_output.txt").read_text(encoding="utf-8")
    verify_payloads(production, independent, report)
    verify_external_payloads(external_final, external_first, adjudication, supplied_output)
    verify_manifest()
    verify_preregistration()
    verify_external_preregistration()
    verify_external_supplied_replay()
    verify_external_manifest()
    return {
        "status": "PASS",
        "preregistered_commit": PREREG_COMMIT,
        "production_check_count": len(production["checks"]),
        "independent_check_count": len(independent["checks"]),
        "external_independent_check_count": len(external_final["checks"]),
        "manifest_rows": 7,
        "external_manifest_rows": 4,
        "primary_landing": "CONFORMAL_NETWORK_NONSELECTION__CURRENT_IDENTITIES_ONLY_EVALUATE_SUPPLIED_HISTORY",
        "g154_sublanding": "EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED",
        "fresh_adversarial_review": "REPAIR_FOLLOWUP_PASS",
        "cold_external_review": "INDEPENDENT_LOCAL_REPLAY_PASS_WITH_CAVEATS",
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
