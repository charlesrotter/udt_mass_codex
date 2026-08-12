#!/usr/bin/env python3
"""Exercise fail-closed G83 verifier mutations without changing disk evidence."""

from __future__ import annotations

import copy
import csv
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_package.py"
    spec = importlib.util.spec_from_file_location("g83_verify_for_catches", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rejected(callable_) -> bool:
    try:
        callable_()
    except (AssertionError, KeyError, ValueError):
        return True
    return False


def main() -> None:
    verify = load_verifier()
    strict = rows(HERE / "STRICT_DOMAIN_ATLAS.tsv")
    paths = rows(HERE / "CONTINUED_PATH_ATLAS.tsv")
    recenter = rows(HERE / "RECENTERED_ENDPOINT_LIMIT_ATLAS.tsv")
    checks: dict[str, bool] = {}

    mutant = copy.deepcopy(paths[:-1])
    checks["missing_path_rejected"] = rejected(lambda: verify.validate_paths(mutant))

    mutant = copy.deepcopy(paths)
    mutant[-1] = copy.deepcopy(mutant[0])
    checks["duplicate_path_rejected"] = rejected(lambda: verify.validate_paths(mutant))

    mutant = copy.deepcopy(paths)
    mutant[0]["status"] = "PHYSICAL_XMAX_SELECTED"
    checks["invalid_status_rejected"] = rejected(lambda: verify.validate_paths(mutant))

    mutant = copy.deepcopy(paths)
    reached_index = next(index for index, row in enumerate(mutant) if row["endpoint_reached"].lower() == "true")
    mutant[reached_index]["null_residual"] = "1e-3"
    checks["bad_raw_residual_rejected"] = rejected(lambda: verify.validate_paths(mutant))

    mutant = copy.deepcopy(strict)
    mutant[0]["min_A_on_0_1"] = "0"
    checks["nonpositive_strict_lapse_rejected"] = rejected(lambda: verify.validate_strict(mutant))

    mutant = copy.deepcopy(strict)
    mutant[0]["phi_receiver_to_x_1"] = "inf"
    checks["infinite_strict_depth_rejected"] = rejected(lambda: verify.validate_strict(mutant))

    mutant = copy.deepcopy(recenter)
    for row in mutant:
        row["proper_limit_over_R"] = "3"
    checks["false_receiver_independence_rejected"] = rejected(lambda: verify.validate_recenter(mutant))

    mutant = copy.deepcopy(recenter)
    mutant[0]["ownership"] = "PHYSICAL_XMAX"
    checks["continuation_promotion_rejected"] = rejected(lambda: verify.validate_recenter(mutant))

    assert all(checks.values())
    payload = {
        "schema": "UDT_CMB_G83_CATCH_PROOFS_V1",
        "all_passed": True,
        "count": len(checks),
        "checks": checks,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
