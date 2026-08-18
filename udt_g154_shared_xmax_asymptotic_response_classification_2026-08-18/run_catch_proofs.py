#!/usr/bin/env python3
"""Mutation catch proofs for the G154 package verifier."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from verify_package import HERE, verify_payloads


def caught(production: dict[str, object], independent: dict[str, object], report: str) -> bool:
    try:
        verify_payloads(production, independent, report)
    except AssertionError:
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks: dict[str, bool] = {}

    mutation = copy.deepcopy(production)
    mutation["status"] = "FAIL"
    checks["production_status"] = caught(mutation, independent, report)

    mutation = copy.deepcopy(production)
    mutation["checks"]["mobius_composition_exact"] = False
    checks["production_boolean"] = caught(mutation, independent, report)

    mutation = copy.deepcopy(production)
    mutation["fixed_scale_limits"]["finite_live"]["1"] = "0"
    checks["class_limit"] = caught(mutation, independent, report)

    mutation_independent = copy.deepcopy(independent)
    mutation_independent["checks"]["source_manifest_hashes"] = False
    checks["independent_source_check"] = caught(production, mutation_independent, report)

    checks["report_landing"] = caught(
        production,
        independent,
        report.replace("EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED", "REMOVED", 1),
    )
    checks["review_guard"] = caught(
        production,
        independent,
        report.replace("repair-only follow-up passed", "follow-up missing", 1),
    )

    result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
