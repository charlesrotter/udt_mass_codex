#!/usr/bin/env python3
"""Semantic hostile controls for the bounded G313 landing."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


BASELINE = {
    "trace_coefficient": "1/4",
    "bianchi_scope": "connected_constancy_only",
    "all_einstein_constant_curvature": False,
    "weyl_active_witness": True,
    "xmax_identified": False,
    "unique_round_universe": False,
    "bootstrap_compatible": True,
    "global_predicate_is_local_memory": False,
    "cosh_q_constant": "1",
    "explicit_product_ricci_verified": True,
    "product_cauchy_proof_present": True,
    "bootstrap_equal_jet_factorization_verified": True,
}


def defects(claim: dict) -> list[str]:
    found = []
    if claim["trace_coefficient"] != "1/4":
        found.append("wrong_trace_coefficient")
    if claim["bianchi_scope"] != "connected_constancy_only":
        found.append("bianchi_magnitude_promotion")
    if claim["all_einstein_constant_curvature"]:
        found.append("weyl_erasure")
    if not claim["weyl_active_witness"]:
        found.append("witness_erasure")
    if claim["xmax_identified"]:
        found.append("xmax_smuggle")
    if claim["unique_round_universe"]:
        found.append("round_history_promotion")
    if not claim["bootstrap_compatible"]:
        found.append("locality_bootstrap_confusion")
    if claim["global_predicate_is_local_memory"]:
        found.append("selector_response_type_confusion")
    if claim["cosh_q_constant"] != "1":
        found.append("cosh_residual_constant_mutation")
    if not claim["explicit_product_ricci_verified"]:
        found.append("explicit_product_ricci_erasure")
    if not claim["product_cauchy_proof_present"]:
        found.append("product_cauchy_proof_erasure")
    if not claim["bootstrap_equal_jet_factorization_verified"]:
        found.append("bootstrap_factorization_erasure")
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if defects(BASELINE):
        raise AssertionError("baseline must be clean")
    mutations = [
        ("wrong_trace_coefficient", "trace_coefficient", "1/3"),
        ("bianchi_magnitude_promotion", "bianchi_scope", "fixes_numerical_value"),
        ("weyl_erasure", "all_einstein_constant_curvature", True),
        ("witness_erasure", "weyl_active_witness", False),
        ("xmax_smuggle", "xmax_identified", True),
        ("round_history_promotion", "unique_round_universe", True),
        ("locality_bootstrap_confusion", "bootstrap_compatible", False),
        ("selector_response_type_confusion", "global_predicate_is_local_memory", True),
        ("cosh_residual_constant_mutation", "cosh_q_constant", "2"),
        ("explicit_product_ricci_erasure", "explicit_product_ricci_verified", False),
        ("product_cauchy_proof_erasure", "product_cauchy_proof_present", False),
        (
            "bootstrap_factorization_erasure",
            "bootstrap_equal_jet_factorization_verified",
            False,
        ),
    ]
    rows = []
    for expected, key, value in mutations:
        mutant = copy.deepcopy(BASELINE)
        mutant[key] = value
        observed = defects(mutant)
        if expected not in observed:
            raise AssertionError(f"mutation not caught: {expected}")
        rows.append({"mutation": expected, "caught": True, "observed_defects": observed})

    result = {
        "status": "PASS",
        "baseline_clean": True,
        "mutations_registered": len(mutations),
        "mutations_caught": len(rows),
        "rows": rows,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
