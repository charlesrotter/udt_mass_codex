#!/usr/bin/env python3
"""Fail-closed no-write package replay for G219."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import csv
import copy
import sys
from pathlib import Path

import sympy as sp

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv",
    "REPAIR_PREREGISTRATION.md",
    "derive_clock_arrow_protocols.py", "verify_clock_arrow_independent.py", "run_catch_proofs.py",
    "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    "PROTOCOL_ATLAS.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv", "ADVERSARIAL_REVIEW_REQUEST.md", "FRESH_ADVERSARIAL_REVIEW.md",
    "VERIFICATION_RESULT.json",
)


def canonical_protocol_contract() -> dict[str, dict[str, str]]:
    """Independent symbolic construction of the registered protocol payload."""
    eta, a, b, length = sp.symbols("eta a b L", real=True)
    a_radar, a_minus = sp.symbols("a_radar a_minus", real=True)
    C, S, E = sp.cosh(eta), sp.sinh(eta), sp.exp(eta)

    def record(lhs: str, rhs: sp.Expr, source: sp.Symbol) -> dict[str, str]:
        rhs = sp.simplify(rhs)
        slope = sp.simplify(sp.diff(rhs, source))
        depth = sp.simplify(sp.expand_log(-sp.log(slope), force=True))
        return {
            "map": f"{lhs}={sp.sstr(rhs)}",
            "slope": sp.sstr(slope),
            "depth": sp.sstr(depth),
            "map_canonical": sp.srepr(rhs),
            "slope_canonical": sp.srepr(slope),
            "depth_canonical": sp.srepr(depth),
        }

    return {
        "null_A_emit_to_B_receive": record("b", E * (a + length), a),
        "A_Fermi": record("b", a / C, a),
        "B_Fermi_as_A_to_B_relation": record("b", C * a + S * length, a),
        "A_radar_simultaneity": record("b", a_radar / C, a_radar),
        "null_mathematical_inverse": record("a", sp.exp(-eta) * b - length, b),
        "future_return_B_to_A": record("a_plus", E * b + length, b),
        "A_echo": record("a_plus", length + sp.exp(2 * eta) * (a_minus + length), a_minus),
    }


def protocol_payload_valid(protocols: dict[str, dict[str, str]]) -> bool:
    return protocols == canonical_protocol_contract()


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot() -> dict[str, str]:
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in REQUIRED}


def main() -> None:
    for name in REQUIRED:
        assert (HERE / name).is_file(), name
    before = snapshot()
    production = load("g219_production", "derive_clock_arrow_protocols.py").derive()
    independent = load("g219_independent", "verify_clock_arrow_independent.py").verify()
    caught = load("g219_catches", "run_catch_proofs.py").catches()
    registered = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    registered_independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    registered_catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    assert production["manifest_files"] == 11
    assert len(production["checks"]) == registered["symbolic_checks"] == 18
    assert all(production["checks"].values()) and registered["all_checks_pass"]
    assert registered["landing"] == "SCALAR_CHAIN_FACTORS_THROUGH_ONE_CLOCK_ARROW__PROTOCOL_REMAINS_QUERY_TYPED"
    assert not registered["protocol_uniqueness"] and not registered["full_timelive_history_derived"]
    assert independent["cases"] == 3684 and independent["assertions"] == 44822
    assert independent == {
        "cases": registered_independent["cases"],
        "assertions": registered_independent["assertions"],
        "exact": registered_independent["exact"],
        "implementation": registered_independent["implementation"],
    }
    assert registered_independent["all_checks_pass"]
    assert len(caught) == registered_catches["count"] == 10 and all(caught.values())
    assert registered_catches["all_caught"]
    assert verification == {
        "status": "PASS",
        "landing": registered["landing"],
        "source_count": 11,
        "exact_checks": 18,
        "independent_cases": 3684,
        "independent_exact_checks": 44822,
        "hostile_catches": 10,
        "protocol_mutation_guard": True,
        "no_write_replay": True,
        "fresh_adversarial_review": "ACCEPT_AFTER_PREREGISTERED_EVIDENCE_REPAIRS",
        "full_timelive_orchestra_derived": False,
        "physical_protocol_selected": False,
    }
    assert set(caught) == set(registered_catches["mutations"])
    assert protocol_payload_valid(production["protocols"])
    mutated_protocols = copy.deepcopy(production["protocols"])
    mutated_protocols["null_A_emit_to_B_receive"]["slope_canonical"] = "exp(-eta)"
    assert not protocol_payload_valid(mutated_protocols), "protocol production mutation escaped"
    with (HERE / "PROTOCOL_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        atlas = {row["protocol"]: row for row in csv.DictReader(handle, delimiter="\t")}
    mapping = {
        "outgoing_null_A_to_B": "null_A_emit_to_B_receive",
        "A_Fermi": "A_Fermi",
        "B_Fermi_as_A_to_B": "B_Fermi_as_A_to_B_relation",
        "A_radar_simultaneity": "A_radar_simultaneity",
        "null_mathematical_inverse": "null_mathematical_inverse",
        "future_return_B_to_A": "future_return_B_to_A",
        "A_echo": "A_echo",
    }
    assert set(atlas) == set(mapping)
    for atlas_key, production_key in mapping.items():
        expected = production["protocols"][production_key]
        assert atlas[atlas_key]["map"] == expected["map"]
        assert atlas[atlas_key]["slope_r"] == expected["slope"]
        assert atlas[atlas_key]["depth_delta"] == expected["depth"]
    assert snapshot() == before, "registered package mutated during replay"
    print("PASS: G219 11 sources; 18 symbolic; 44,822 independent; 10 catches; protocol-mutation guard; no-write")


if __name__ == "__main__":
    main()
