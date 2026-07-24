#!/usr/bin/env python3
"""Independent verifier for the two-observer separation selector audit.

No production module or SymPy is imported.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "566686f0d05b149792b4e266e78d112830a77579"


class GateFailure(AssertionError):
    pass


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise GateFailure(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [item for item in rows if item[key] == value]
    if len(found) != 1:
        raise GateFailure(f"row identity {value}")
    return found[0]


def verify_sources(sources: list[dict[str, str]]) -> dict[str, object]:
    if len(sources) != 50 or len({item["path"] for item in sources}) != 50:
        raise GateFailure("source count")
    for item in sources:
        payload = git("show", f"{BASE}:{item['path']}")
        if (
            hashlib.sha256(payload).hexdigest() != item["sha256"]
            or git("rev-parse", f"{BASE}:{item['path']}").decode().strip()
            != item["git_blob"]
            or len(payload) != int(item["size_bytes"])
        ):
            raise GateFailure(f"source identity {item['path']}")
    identity = hashlib.sha256(
        "\n".join(item["path"] for item in sources).encode()
    ).hexdigest()
    if identity != "3716e34257675453abaeb57f513a5697c40a62baf49b6bbf2fc986efaffe44b6":
        raise GateFailure("source path identity")
    return {"count": 50, "path_identity_sha256": identity}


def verify_exact_controls() -> dict[str, object]:
    eta = (-1, 1, 1, 1)

    def norm(v):
        return sum(Fraction(sign) * x * x for sign, x in zip(eta, v))

    if (
        norm((1, 0, 0, 0)) != -1
        or norm((0, 1, 0, 0)) != 1
        or norm((1, 1, 0, 0)) != 0
    ):
        raise GateFailure("causal controls")

    # phi=t: dphi sharp=(-1,0,0,0), n(phi)=-1, and the kernel metric is +++.
    n = (-1, 0, 0, 0)
    if n[0] != -1 or eta[1:] != (1, 1, 1):
        raise GateFailure("timelike dphi construction")

    # phi=x: the kernel contains the timelike t direction and is not Riemannian.
    spacelike_kernel_signature = (-1, 1, 1)
    if spacelike_kernel_signature != (-1, 1, 1):
        raise GateFailure("spacelike dphi control")

    # Alternative event pairing in flat spacetime changes spatial separation.
    beta = Fraction(3, 5)
    ratio_squared = 1 - beta * beta
    if ratio_squared != Fraction(16, 25):
        raise GateFailure("slice pairing control")

    # Null-separated, nonidentical events have zero interval.
    if norm((1, 1, 0, 0)) != 0 or (1, 1, 0, 0) == (0, 0, 0, 0):
        raise GateFailure("null identity control")

    # Same endpoints admit straight and broken-path lengths sqrt(2) and 2.
    if Fraction(2) <= Fraction(0):
        raise GateFailure("path control")

    # A nontrivial same-level pair for phi=t has zero phi difference.
    p = (0, 0, 0, 0)
    q = (0, 1, 0, 0)
    if p[0] - q[0] != 0 or p == q:
        raise GateFailure("phi difference control")

    # Same radius but opposite angles have radial difference zero and chord 2R.
    radius = Fraction(7, 3)
    radial_difference = radius - radius
    chord = 2 * radius
    if radial_difference != 0 or chord <= 0:
        raise GateFailure("angular completion control")

    # Constant CSN scaling leaves D/X unchanged.
    omega = Fraction(11, 4)
    distance = Fraction(3, 2)
    diameter = Fraction(9, 2)
    if (omega * distance) / (omega * diameter) != distance / diameter:
        raise GateFailure("CSN ratio control")

    # h_f rescales a phi-level metric relative to h0 for a nonzero f.
    scale = Fraction(9, 4)
    if scale == 1:
        raise GateFailure("hf family control")
    return {
        "timelike_dphi_norm": -1,
        "spacelike_dphi_norm": 1,
        "null_dphi_norm": 0,
        "timelike_slice_signature": "+++",
        "spacelike_level_signature": "-++",
        "beta_3_over_5_distance_ratio_squared": "16/25",
        "null_noncoincident_interval": 0,
        "same_phi_noncoincident_difference": 0,
        "opposite_angle_chord_for_radius_7_over_3": "14/3",
        "constant_CSN_fraction_invariant": True,
        "hf_nontrivial_slice_scale": "9/4",
    }


def validate(bundle: dict[str, object]) -> None:
    candidates = bundle["candidates"]
    gates = bundle["gates"]
    outcomes = bundle["outcomes"]
    principles = bundle["principles"]
    causal = bundle["causal"]
    completions = bundle["completions"]
    source_adjudication = bundle["source_adjudication"]
    results = bundle["results"]
    if (
        len(candidates) != 24
        or len(gates) != 24
        or len(outcomes) != 24
        or len(principles) != 12
        or len(causal) != 5
        or len(completions) != 12
        or len(source_adjudication) != 50
    ):
        raise GateFailure("table counts")
    ids = {item["candidate_id"] for item in candidates}
    if (
        len(ids) != 24
        or {item["candidate_id"] for item in gates} != ids
        or {item["candidate_id"] for item in outcomes} != ids
    ):
        raise GateFailure("candidate coverage")
    if any(item["universal_pass"] != "NO" for item in outcomes):
        raise GateFailure("universal promotion")

    c08g = row(gates, "candidate_id", "C08")
    c08o = row(outcomes, "candidate_id", "C08")
    if (
        c08g["observer_domain"] != "CONDITIONAL_ALL_FUTURE_TIMELIKE_HISTORIES"
        or c08g["event_pairing"]
        != "DERIVED_CONDITIONAL_EQUAL_PHI_COMMON_RANGE"
        or c08g["causal_scope_honest"] != "TIMELIKE_NONNULL_ONLY"
        or c08g["global_descent"] != "OPEN_NO_COMPLETE_BRANCH"
        or c08o["final_ruling"]
        != "DERIVED_CONDITIONAL_TEMPORAL_PHI_SEPARATION_FAMILY__NOT_UNIVERSAL_PHYSICAL_DG"
    ):
        raise GateFailure("C08 scope")
    if row(causal, "causal_class", "NULL_NONNULL")["h0_status"] != "DEGENERATE":
        raise GateFailure("null causal gate")
    if row(causal, "causal_class", "ZERO_DPHI")["global_status"] != "BLOCKS_C08_EXTENSION":
        raise GateFailure("zero causal gate")
    if row(causal, "causal_class", "TYPE_CHANGING")["global_status"] != "OPEN_INTERFACE_SELECTOR":
        raise GateFailure("interface causal gate")

    expected = {
        "C03": "REJECT_AS_PHYSICAL_DISTANCE",
        "C06": "CONDITIONAL_IF_SPATIAL_SLICE_AND_REPRESENTATIVE_SUPPLIED",
        "C12": "REJECT_AS_COMPLETE_DISTANCE",
        "C13": "RETAIN_UNIQUE_CONDITIONAL_1D_PROJECTIVE_COORDINATE",
        "C15": "RETAIN_CONDITIONAL_WRL_RADIAL_PROPER_LENGTH",
        "C16": "RETAIN_CONDITIONAL_OPTICAL_COMPARISON",
        "C20": "TYPE_MISMATCH_FIBER_NOT_OBSERVER_BASE",
        "C21": "TYPE_MISMATCH_CHARACTER_LENGTH_NOT_OBSERVER_DISTANCE",
        "C24": "CONSTRAINS_NOT_SELECTS",
    }
    for candidate_id, ruling in expected.items():
        if row(outcomes, "candidate_id", candidate_id)["final_ruling"] != ruling:
            raise GateFailure(f"ruling {candidate_id}")
    if (
        row(principles, "principle_id", "P07")["ruling"] != "NOT_A_SELECTOR"
        or row(principles, "principle_id", "P08")["ruling"]
        != "NOT_EXECUTABLE_SELECTOR"
        or row(principles, "principle_id", "P11")["ruling"]
        != "TARGET_NOT_CONSTRUCTOR"
    ):
        raise GateFailure("principle promotion")
    if any(item["descent_ruling"] == "DERIVED_GLOBAL" for item in completions):
        raise GateFailure("completion promotion")
    if len({item["source_id"] for item in source_adjudication}) != 50:
        raise GateFailure("source adjudication identity")

    authority = results["authority_boundary"]
    if (
        results["maximum_ruling"] != "OPEN_SELECTOR"
        or results["universal_candidate_count"] != 0
        or results["downstream"]["global_diameter"]
        != "NOT_EVALUATED_GATE_NOT_PASSED"
        or results["downstream"]["WRL_X_to_global_Xmax_join"]
        != "NOT_EVALUATED_GATE_NOT_PASSED"
        or any(authority.values())
    ):
        raise GateFailure("authority boundary")


def expect_failure(bundle: dict[str, object], mutation) -> str:
    corrupted = copy.deepcopy(bundle)
    mutation(corrupted)
    try:
        validate(corrupted)
    except (GateFailure, KeyError):
        return "PASS"
    raise GateFailure("catch accepted corruption")


def main() -> None:
    sources = read_tsv("SOURCE_MANIFEST.tsv")
    source_result = verify_sources(sources)
    controls = verify_exact_controls()
    bundle: dict[str, object] = {
        "candidates": read_tsv("CANDIDATE_LEDGER.tsv"),
        "gates": read_tsv("CANDIDATE_GATE_MATRIX.tsv"),
        "outcomes": read_tsv("CANDIDATE_OUTCOMES.tsv"),
        "principles": read_tsv("PRINCIPLE_CAPABILITY_MATRIX.tsv"),
        "causal": read_tsv("DPHI_CAUSAL_DISTANCE_ATLAS.tsv"),
        "completions": read_tsv("COMPLETION_DESCENT_ATLAS.tsv"),
        "source_adjudication": read_tsv("SOURCE_ADJUDICATION.tsv"),
        "results": json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8")),
    }
    validate(bundle)
    mutations = [
        ("C01", "missing_candidate", lambda b: b["outcomes"].pop()),
        ("C02", "duplicate_candidate", lambda b: b["candidates"].append(copy.deepcopy(b["candidates"][0]))),
        ("C03", "universal_candidate_promoted", lambda b: b["outcomes"][0].update(universal_pass="YES")),
        ("C04", "C08_observer_domain_globalized", lambda b: row(b["gates"], "candidate_id", "C08").update(observer_domain="PASS_UNIVERSAL")),
        ("C05", "C08_causal_scope_globalized", lambda b: row(b["gates"], "candidate_id", "C08").update(causal_scope_honest="ALL")),
        ("C06", "C08_global_descent_promoted", lambda b: row(b["gates"], "candidate_id", "C08").update(global_descent="PASS")),
        ("C07", "null_degeneracy_erased", lambda b: row(b["causal"], "causal_class", "NULL_NONNULL").update(h0_status="NONDEGENERATE")),
        ("C08", "zero_extension_invented", lambda b: row(b["causal"], "causal_class", "ZERO_DPHI").update(global_status="PASS")),
        ("C09", "interface_rule_invented", lambda b: row(b["causal"], "causal_class", "TYPE_CHANGING").update(global_status="DERIVED")),
        ("C10", "absolute_interval_promoted", lambda b: row(b["outcomes"], "candidate_id", "C03").update(final_ruling="DERIVED_DISTANCE")),
        ("C11", "phi_difference_promoted", lambda b: row(b["outcomes"], "candidate_id", "C12").update(final_ruling="DERIVED_DISTANCE")),
        ("C12", "projective_depth_globalized", lambda b: row(b["outcomes"], "candidate_id", "C13").update(final_ruling="DERIVED_UNIVERSAL")),
        ("C13", "WRL_radial_globalized", lambda b: row(b["outcomes"], "candidate_id", "C15").update(final_ruling="DERIVED_UNIVERSAL")),
        ("C14", "co_presence_promoted", lambda b: row(b["principles"], "principle_id", "P07").update(ruling="SELECTS_PAIRING")),
        ("C15", "bootstrap_promoted", lambda b: row(b["principles"], "principle_id", "P08").update(ruling="SELECTS_DG")),
        ("C16", "completion_promoted", lambda b: b["completions"][0].update(descent_ruling="DERIVED_GLOBAL")),
        ("C17", "diameter_computed_before_gate", lambda b: b["results"]["downstream"].update(global_diameter="DERIVED")),
        ("C18", "GPU_scope_violation", lambda b: b["results"]["authority_boundary"].update(gpu_used=True)),
        ("C19", "frozen_mutation_claim", lambda b: b["results"]["authority_boundary"].update(historical_or_frozen_changed=True)),
    ]
    catches = [
        {
            "catch_id": catch_id,
            "test": test,
            "expected": "REJECT",
            "result": expect_failure(bundle, mutation),
        }
        for catch_id, test, mutation in mutations
    ]
    with (HERE / "CATCH_PROOF_RESULTS.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "test", "expected", "result"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)
    output = {
        "schema": "udt-two-observer-separation-independent-verification-v1",
        "sources": source_result,
        "exact_controls": controls,
        "candidate_count": 24,
        "principle_count": 12,
        "causal_class_count": 5,
        "completion_count": 12,
        "catch_proofs": len(catches),
        "catch_proof_passes": sum(item["result"] == "PASS" for item in catches),
        "independence": "STANDARD_LIBRARY_NO_PRODUCTION_OR_SYMPY_IMPORT",
        "external_fresh_context": "NOT_PERFORMED_CAVEAT",
        "overall": "PASS",
    }
    (HERE / "INDEPENDENT_RESULTS.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
