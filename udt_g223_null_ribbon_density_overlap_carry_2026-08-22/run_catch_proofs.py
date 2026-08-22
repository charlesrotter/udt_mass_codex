#!/usr/bin/env python3
"""Hostile payload mutations for the G223 contract verifier."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify_package import contained_source_path, validate_payloads


ROOT = Path(__file__).resolve().parent


def main() -> None:
    d0 = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    i0 = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    f0 = json.loads((ROOT / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    mutations = [
        ("derivation_status", "d", "status", "FAIL"),
        ("symbolic_count", "d", "symbolic_checks", 20),
        ("mixed_pairing", "d", "metric_mixed_pairing_canonical", False),
        ("clock_weight", "d", "vertical_density_inverse_clock_weight", False),
        ("closedness_promotion", "d", "chosen_full_representative_closedness_invariant", True),
        ("local_coordinate", "d", "local_interval_fiber_coordinate_exists", False),
        ("global_scalar_promotion", "d", "global_scalar_coordinate_unconditional", True),
        ("vertical_gluing_promotion", "d", "G216_clock_chain_supplies_vertical_gluing", True),
        ("independent_cases", "i", "cases", 19999),
        ("independent_assertions", "i", "exact_rational_assertions", 361000),
        ("counterexample", "i", "same_metric_closedness_counterexample", False),
        ("cross_ribbon_promotion", "i", "cross_ribbon_vertical_gluing_derived", True),
        ("preregistration", "f", "preregistration_commit", "UNFROZEN"),
        ("landing", "f", "landing", "PROMOTED"),
    ]
    rejected: list[str] = []
    for name, target, field, value in mutations:
        d, i, f = copy.deepcopy(d0), copy.deepcopy(i0), copy.deepcopy(f0)
        {"d": d, "i": i, "f": f}[target][field] = value
        try:
            validate_payloads(d, i, f)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(f"mutation survived: {name}")

    path_mutations = ("/tmp/outside_intake", "../outside_intake")
    path_rejected: list[str] = []
    for raw in path_mutations:
        try:
            contained_source_path(raw)
        except AssertionError:
            path_rejected.append(raw)
        else:
            raise AssertionError(f"manifest path mutation survived: {raw}")

    result = {
        "status": "PASS",
        "mutations_attempted": len(mutations),
        "mutations_rejected": len(rejected),
        "rejected": rejected,
        "manifest_path_mutations_attempted": len(path_mutations),
        "manifest_path_mutations_rejected": len(path_rejected),
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: G223 catch proofs; {len(rejected)}/{len(mutations)} mutations rejected")


if __name__ == "__main__":
    main()
