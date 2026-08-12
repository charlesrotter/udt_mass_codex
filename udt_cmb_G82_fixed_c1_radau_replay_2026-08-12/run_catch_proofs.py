#!/usr/bin/env python3
"""Exercise fail-closed mutations against the G82 saved-artifact verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_result_independent.py"
    spec = importlib.util.spec_from_file_location("g82_verify", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    verifier = load_verifier()
    base = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    manifest = verifier.rows(HERE / "SOURCE_MANIFEST.tsv")

    mutations = {
        "wrong_control": lambda p, m: p["control"].__setitem__("control_id", "C0_RADIAL_ROTATED"),
        "dop853_masquerade": lambda p, m: p["method"].__setitem__("integrator", "DOP853"),
        "changed_rtol": lambda p, m: p["method"].__setitem__("rtol", 1.0e-7),
        "changed_atol": lambda p, m: p["method"].__setitem__("atol", 1.0e-7),
        "changed_max_step": lambda p, m: p["method"].__setitem__("max_step", 0.1),
        "loosened_gate": lambda p, m: p.__setitem__("gate", 1.0),
        "false_pass": lambda p, m: p.__setitem__("status", "FAIL"),
        "failed_extra_gate": lambda p, m: p["extra_gates"].__setitem__("radau_not_dop853", False),
        "changed_forward_matrix": lambda p, m: p["control"]["forward_fine_D"][0].__setitem__(0, 9.0),
        "changed_reverse_matrix": lambda p, m: p["control"]["reverse_fine_D"][0].__setitem__(0, 9.0),
        "changed_rotated_matrix": lambda p, m: p["control"]["rotated_fine_D"][0].__setitem__(0, 9.0),
        "source_hash_mutation": lambda p, m: m[0].__setitem__("sha256", "0" * 64),
        "absolute_independence_promotion": lambda p, m: p.__setitem__("authority_boundary", "absolute independence"),
        "selector_promotion": lambda p, m: p.__setitem__("maximum_conclusion_if_pass", "UDT selector derived"),
        "science_promotion": lambda p, m: p.__setitem__("scientific_maximum_unchanged", "CMB prediction derived"),
    }
    caught = {}
    for name, mutate in mutations.items():
        payload = copy.deepcopy(base)
        source_rows = copy.deepcopy(manifest)
        mutate(payload, source_rows)
        try:
            verifier.validate(payload, source_rows)
        except (AssertionError, KeyError, ValueError):
            caught[name] = True
        else:
            caught[name] = False
    result = {
        "schema": "udt-cmb-g82-catch-proofs-v1",
        "status": "PASS" if all(caught.values()) else "FAIL",
        "count": len(caught),
        "catches": caught,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if result["status"] != "PASS":
        raise SystemExit("G82 catch proof failed")


if __name__ == "__main__":
    main()
