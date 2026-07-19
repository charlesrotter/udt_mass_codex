#!/usr/bin/env python3
"""Fail-closed verifier for the angular-toric closure selector audit."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import math
import pathlib
import platform
import subprocess
import sys
import tempfile

import sympy as sp


BASE = "cc7b08381281fa104661df5b6af9fb030cabac95"
PREREG = "d8b964d7e383b9e68c76a060e3ed98e4336cc994"
PREREG_SHA256 = "6628c38cc85f3873e52de12fb0578493f340fc9a86c35f416a95869900f5c264"
VERDICT = (
    "S3_AND_FREE_HOPF_ACTION_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES; "
    "RECIPROCITY_CSN_FINITE_CELL_AND_BOOTSTRAP_DO_NOT_SELECT_THOSE_PREMISES; "
    "FIRST_MISSING_GATE_TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY; "
    "CONDITIONAL_SECOND_GATE_FINITE_CELL_CAP_COMPLETION_OPEN"
)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    completed = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"git {' '.join(args)} failed: {error}")
    return completed.stdout


def table_text(payload: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(payload), delimiter="\t"))


def table(path: pathlib.Path) -> list[dict[str, str]]:
    return table_text(path.read_text(encoding="utf-8"))


def reject(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError) as exc:
        return {"name": name, "result": "PASS", "caught": type(exc).__name__}
    raise AssertionError(f"catch-proof accepted corruption: {name}")


def validate_prereg(repo: pathlib.Path, package: pathlib.Path) -> None:
    assert str(git(repo, "rev-parse", f"{PREREG}^")).strip() == BASE
    changed = str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG)).splitlines()
    assert changed == ["angular_toric_closure_selector_2026-07-19/PREREGISTRATION.md"]
    assert sha((package / "PREREGISTRATION.md").read_bytes()) == PREREG_SHA256


def validate_sources(repo: pathlib.Path, rows: list[dict[str, str]]) -> None:
    assert len(rows) == 12
    paths = [row["current_path"] for row in rows]
    assert len(set(paths)) == 12
    for row in rows:
        path = row["current_path"]
        payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        assert row["blob_oid"] == str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        assert row["sha256"] == sha(payload)
        assert int(row["size_bytes"]) == len(payload)
        assert row["last_commit"] == str(git(repo, "log", "-1", "--format=%H", BASE, "--", path)).strip()


def source_text(repo: pathlib.Path, path: str, replacements: dict[str, str] | None = None) -> str:
    replacements = replacements or {}
    if path in replacements:
        return replacements[path]
    return str(git(repo, "show", f"{BASE}:{path}"))


def validate_source_semantics(repo: pathlib.Path, replacements: dict[str, str] | None = None) -> None:
    required = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md": [
            "the transverse spatial block or full time-live geometry",
            "any slot identification retain their separately ledgered non-derived statuses",
            "that parity statement does not select the action's boundary functional",
            "This principle is a global selection requirement, not a ready-made local field equation",
        ],
        "CANON.md": [
            "## C-2026-06-10-2: The finite-cell canon",
            "Dilation is monotone on a finite domain terminated by a",
            "physical boundary, mirrored across phi -> -phi",
            "## C-2026-07-04-1 — Seal-involution SECTOR SPLIT",
            "φ is odd under σ_φ",
            "Dirichlet φ(r_s)=0",
        ],
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": [
            "Omega(x)>0",
            "the finite-cell boundary functional",
            "the matter carrier",
        ],
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": [
            "The full time-live volume and boundary are not yet derived",
            "No nonlocal insertion",
            "Primary global reading",
        ],
        "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md": [
            "does **not** select whether fundamental variation occurs before",
            "does **not** derive a two-stage bridge",
            "does not specify the off-shell fields, action, admissible",
        ],
        "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md": [
            "does not put its reciprocal pair into two",
            "periodic spatial angular slots",
            "different primitive collapse cycles have determinant",
            "lens-space",
            "not the full carrier configuration space `Map(S3,S2)`",
        ],
    }
    for path, tokens in required.items():
        payload = source_text(repo, path, replacements)
        for token in tokens:
            assert token in payload, f"missing source token {path}: {token}"
    c1 = source_text(repo, "UDT_NATIVE_ACTION_COLD_PACKET.md", replacements)
    assert "the selected transverse spatial torus" not in c1
    assert "finite-cell canon selects S3" not in c1
    bootstrap = source_text(repo, "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", replacements)
    assert "bootstrap selects S3" not in bootstrap
    assert "topology-ranking equation" not in bootstrap
    canon = source_text(repo, "CANON.md", replacements)
    start = canon.index("## C-2026-06-10-2: The finite-cell canon")
    end = canon.index("## C-2026-06-10-3", start)
    finite_section = canon[start:end]
    assert "angular torus" not in finite_section.lower()
    assert "hopf" not in finite_section.lower()
    start = canon.index("## C-2026-07-04-1")
    end = canon.find("\n## ", start + 4)
    seal_section = canon[start:] if end < 0 else canon[start:end]
    assert "angular torus" not in seal_section.lower()
    assert "hopf" not in seal_section.lower()


def validate_ledger(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 18
    ids = [row["claim_id"] for row in rows]
    assert ids == [f"T{number:02d}" for number in range(1, 19)]
    assert len(set(ids)) == 18
    by_id = {row["claim_id"]: row for row in rows}
    expected = {
        "T02": "OPEN",
        "T03": "GENERIC_RECIPROCAL_NORMAL_FORM",
        "T05": "TOPOLOGY_UNDERDETERMINED",
        "T06": "S3_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES",
        "T07": "ALLOWED_FAMILY",
        "T08": "EXACT_DOUBLE_COVER_LOCAL_PARITY_WITNESS",
        "T09": "NOT_UNIQUE",
        "T11": "CONDITIONAL_CSN_INVARIANT",
        "T12": "WEIGHTS_UNIQUE_CONDITIONAL",
        "T13": "DISCRETE_CHIRALITY_OPEN",
        "T14": "CONDITIONAL_UNIT_COMPATIBILITY_WITNESS",
        "T15": "BOUNDARY_SCOPE_TOO_WEAK",
        "T16": "NO_TOPOLOGY_RANKING_LAW",
        "T17": "OPEN",
        "T18": "TWO_STAGE_OPEN_GATE_CHAIN",
    }
    for claim_id, status in expected.items():
        assert by_id[claim_id]["status"] == status, (claim_id, by_id[claim_id]["status"])
    assert "separately unselected" in by_id["T06"]["dependency_or_limit"]
    assert "w=0 gives full U1" in by_id["T12"]["basis"]
    assert "finite physical mirrored boundary/fold" in by_id["T15"]["basis"]
    assert "no spatial infinity" in by_id["T15"]["basis"]
    assert "first missing gate" in by_id["T18"]["dependency_or_limit"]
    assert "conditional on passing it" in by_id["T18"]["dependency_or_limit"]


def validate_candidates(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 15
    ids = [row["family_id"] for row in rows]
    assert ids == [f"F{number:02d}" for number in range(1, 16)]
    assert len(set(ids)) == 15
    by_id = {row["family_id"]: row for row in rows}
    assert by_id["F02"]["foundation_compatibility"] == "CONDITIONAL_DOUBLE_COVER_LOCAL_PARITY_WITNESS_ONLY"
    assert by_id["F02"]["within_toric_status"] == "EXACT_KINEMATIC_MIRROR_WITNESS"
    assert by_id["F04"]["within_toric_status"] == "UNIQUE_IF_GLOBAL_DIAGONAL_EIGENCAPS_SUPPLIED"
    assert by_id["F05"]["within_toric_status"] == "SMOOTH_PRIMITIVE_LENS_CLASS"
    assert by_id["F06"]["within_toric_status"] == "SMOOTH_PRIMITIVE_LENS_CLASS"
    assert by_id["F09"]["within_toric_status"] == "EXACT_NONCONFORMAL_WITNESS"
    assert by_id["F12"]["within_toric_status"] == "ORBIFOLD_QUOTIENT_WITH_EXCEPTIONAL_STABILIZER"
    assert by_id["F13"]["within_toric_status"] == "GENERAL_SMOOTH_LENS_FAMILY"
    assert by_id["F14"]["within_toric_status"] == "OPEN_GLOBAL_COMPLETION_FAMILY"
    assert by_id["F15"]["within_toric_status"] == "EFFECTIVE_ACTION_WITH_FIXED_CIRCLE_FULL_U1_STABILIZER"
    assert all(row["foundation_compatibility"] != "UDT_SELECTED" for row in rows)


def independent_exact() -> dict:
    examples = {
        "p0_same_cycle": ((1, 1), (1, 1)),
        "p1_axis_exchange": ((1, 0), (0, 1)),
        "p3_mirror_exchange": ((2, 1), (1, 2)),
        "p5_mirror_exchange": ((3, 2), (2, 3)),
    }
    determinants = {
        name: abs(left[0] * right[1] - left[1] * right[0])
        for name, (left, right) in examples.items()
    }
    assert determinants == {
        "p0_same_cycle": 0, "p1_axis_exchange": 1,
        "p3_mirror_exchange": 3, "p5_mirror_exchange": 5,
    }
    assert all(math.gcd(abs(x), abs(y)) == 1 for pair in examples.values() for x, y in pair)
    additional = {
        "p7": ((4, 3), (3, 4)), "p8": ((3, 1), (1, 3)),
        "p9": ((5, 4), (4, 5)), "p15": ((4, 1), (1, 4)),
    }
    additional_determinants = {
        name: abs(left[0] * right[1] - left[1] * right[0])
        for name, (left, right) in additional.items()
    }
    assert additional_determinants == {"p7": 7, "p8": 8, "p9": 9, "p15": 15}
    additional_primitivity = {
        name: [math.gcd(abs(x), abs(y)) for x, y in (left, right)]
        for name, (left, right) in additional.items()
    }
    assert all(value == 1 for values in additional_primitivity.values() for value in values)
    additional_smith = {
        name: [1, additional_determinants[name]] for name in additional
    }

    def stabilizer_order(weight: int) -> int | str:
        return "U1" if weight == 0 else abs(weight)

    effective = [
        (m, n) for m in range(-8, 9) for n in range(-8, 9)
        if (m, n) != (0, 0) and math.gcd(abs(m), abs(n)) == 1
    ]
    orders = {pair: (stabilizer_order(pair[0]), stabilizer_order(pair[1])) for pair in effective}
    free = sorted(pair for pair, endpoint_orders in orders.items() if endpoint_orders == (1, 1))
    assert free == [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    assert orders[(0, 1)] == ("U1", 1) and orders[(1, 0)] == (1, "U1")

    eta = sp.symbols("eta", real=True)
    f, g = sp.cos(eta) ** 2, sp.sin(eta) ** 2
    connection_integrals = {}
    charges = {}
    for m, n in free:
        a, b = m * f, n * g
        density = sp.simplify(b * sp.diff(a, eta) - a * sp.diff(b, eta))
        integral = sp.simplify(sp.integrate(density, (eta, 0, sp.pi / 2)) * (2 * sp.pi) ** 2)
        charge = sp.simplify(-integral / (4 * sp.pi**2))
        assert charge == m * n
        key = f"({m},{n})"
        connection_integrals[key] = str(integral)
        charges[key] = int(charge)
    assert set(charges.values()) == {-1, 1}

    epsilon = sp.Rational(1, 3)
    h = 1 + epsilon * sp.sin(2 * eta) ** 2
    assert sp.trigsimp(h.subs(eta, -eta) - h) == 0
    assert sp.trigsimp(sp.cos(-eta) - sp.cos(eta)) == 0
    assert sp.trigsimp(sp.sin(-eta) + sp.sin(eta)) == 0
    x = sp.symbols("x", real=True)
    right_h = sp.trigsimp(h.subs(eta, sp.pi / 2 - x))
    right_collapse = sp.sin(x)
    right_spectator = sp.cos(x)
    assert sp.trigsimp(right_h.subs(x, -x) - right_h) == 0
    assert sp.trigsimp(right_collapse.subs(x, -x) + right_collapse) == 0
    assert sp.trigsimp(right_spectator.subs(x, -x) - right_spectator) == 0
    midpoint_h = h.subs(eta, sp.pi / 4)
    ratio_difference = 2 * (midpoint_h**2 - 1)
    assert ratio_difference == sp.Rational(14, 9)

    phi = sp.symbols("phi", real=True)
    common = 1 / (2 * sp.cosh(2 * phi))
    csn_cap_limits = [sp.limit(common, phi, -sp.oo), sp.limit(common, phi, sp.oo)]
    assert csn_cap_limits == [0, 0] and common.subs(phi, 0) > 0

    sigma = sp.symbols("sigma", real=True)
    phi_periodic = sp.sin(sigma)
    metric = sp.diag(1, sp.exp(-2 * phi_periodic), sp.exp(2 * phi_periodic))
    swap = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    assert sp.simplify(swap.T * metric.subs(sigma, -sigma) * swap - metric) == sp.zeros(3)
    assert sp.simplify(sp.det(metric) - 1) == 0
    assert sp.diff(phi_periodic, sigma).subs(sigma, 0) == 1
    finite_interval_positive = [
        sp.exp(sign * 2 * value) > 0
        for sign in (-1, 1) for value in (-sp.Rational(1, 2), sp.Rational(1, 2))
    ]
    assert all(finite_interval_positive)
    return {
        "determinants": determinants,
        "additional_mirror_determinants": additional_determinants,
        "additional_mirror_primitivity": additional_primitivity,
        "additional_mirror_smith_classes": additional_smith,
        "free_weights": [list(pair) for pair in free],
        "zero_weight_stabilizers": {"(0,1)": list(orders[(0, 1)]), "(1,0)": list(orders[(1, 0)])},
        "connection_integrals": connection_integrals,
        "charges": charges,
        "nonround_ratio_difference": str(ratio_difference),
        "cap_all_order_parity": "PASS",
        "csn_cap_limits": [str(value) for value in csn_cap_limits],
        "periodic_mirror_witness": "PASS_LOCAL_PARITY_ONLY",
        "finite_interval_positive_orbits": "PASS",
    }


def validate_algebra(result: dict) -> None:
    assert result["status"] == "PASS"
    assert result["check_count"] == 25
    assert len(result["checks"]) == 25 and set(result["checks"].values()) == {"PASS"}
    exact = result["exact_identities"]
    assert exact["collapse_determinant_classes"] == {
        "p0_same_cycle": 0, "p1_axis_exchange": 1,
        "p3_mirror_exchange": 3, "p5_mirror_exchange": 5,
    }
    assert exact["collapse_smith_classes"] == {
        "p0_same_cycle": [1, 0], "p1_axis_exchange": [1, 1],
        "p3_mirror_exchange": [1, 3], "p5_mirror_exchange": [1, 5],
    }
    assert exact["additional_mirror_determinants"] == {"p7": 7, "p8": 8, "p9": 9, "p15": 15}
    assert exact["additional_mirror_primitivity"] == {
        "p7": [1, 1], "p8": [1, 1], "p9": [1, 1], "p15": [1, 1],
    }
    assert exact["additional_mirror_smith_classes"] == {
        "p7": [1, 7], "p8": [1, 8], "p9": [1, 9], "p15": [1, 15],
    }
    assert exact["left_cap_parity"] == {"H": "even", "collapse": "odd", "spectator": "even"}
    assert exact["right_cap_parity"] == {"H": "even", "collapse": "odd", "spectator": "even"}
    assert exact["round_common_scale_cap_limits"] == ["0", "0"]
    assert exact["radial_orbit_ratio_difference_at_midpoint"] == "14/9"
    assert exact["free_effective_weights"] == [[-1, -1], [-1, 1], [1, -1], [1, 1]]
    assert exact["zero_weight_stabilizer_orders"] == {"(0,1)": ["U1", 1], "(1,0)": [1, "U1"]}
    charges = {
        key: value["registered_charge"]
        for key, value in exact["free_weight_connection_data"].items()
    }
    assert charges == {"(-1,-1)": "1", "(-1,1)": "-1", "(1,-1)": "-1", "(1,1)": "1"}
    classification = result["classification"]
    assert classification["global_diagonal_two_eigencaps"] == "S3_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES"
    assert classification["exchange_mirror_without_eigencap_rule"] == "TOPOLOGY_UNDERDETERMINED"
    assert classification["general_toric_completion"] == "P0_P1_LENS_P_GREATER_1_INCOMPLETE_AND_NONCOMPACT_FAMILIES_REMAIN"
    assert classification["round_completion"] == "NOT_UNIQUE_EVEN_WITHIN_SMOOTH_MIRROR_S3_CLASS"
    assert classification["registered_udt_selection"] == "SPATIAL_TORUS_SLOT_CAP_AND_QUOTIENT_NOT_SELECTED"
    assert classification["first_missing_gate"] == "TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY"
    assert classification["conditional_second_gate"] == "FINITE_CELL_CAP_COMPLETION"
    assert result["maximum_verdict"] == VERDICT


def validate_report(report: str) -> None:
    required = [
        "S3_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES",
        "Primitive mirror pairs realize multiple determinant classes",
        "`S2 x S1` in the standard orientable same-cycle",
        "admissible gluing integer `q`",
        "double-cover/local-parity witness",
        "not a direct countermodel to the complete physical finite-cell canon",
        "monotone finite domain terminated by a physical mirrored boundary/fold",
        "no spatial infinity",
        "They are not related by a positive full-metric conformal rescaling",
        "analytic cap parity to all orders",
        "only when",
        "|m|=|n|=1",
        "the full `U(1)` when `m=0",
        "Bootstrap could eventually select among complete solutions",
        "missing law itself",
        "TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY",
        "FINITE_CELL_CAP_COMPLETION",
        "No temporal direction was compactified",
        "No existing soliton or particle evidence was used as a selection criterion",
    ]
    for token in required:
        assert token in report, token
    forbidden = [
        "UDT selects S3",
        "reciprocity forces S3",
        "bootstrap selects the Hopfion",
        "the carrier is derived",
        "the action follows",
    ]
    lower = report.lower()
    for token in forbidden:
        assert token.lower() not in lower, token


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent

    validate_prereg(repo, package)
    sources = table(package / "SOURCE_INVENTORY.tsv")
    ledger = table(package / "STATUS_LEDGER.tsv")
    candidates = table(package / "CANDIDATE_FAMILY.tsv")
    algebra = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    validate_sources(repo, sources)
    validate_source_semantics(repo)
    validate_ledger(ledger)
    validate_candidates(candidates)
    validate_algebra(algebra)
    validate_report(report)
    independent = independent_exact()

    with tempfile.TemporaryDirectory(prefix="angular_toric_replay_") as temp:
        replay = pathlib.Path(temp) / "DERIVATION_RESULT.json"
        completed = subprocess.run(
            [sys.executable, str(package / "derive_angular_toric_selector.py"), "--output", str(replay)],
            cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        assert completed.returncode == 0, completed.stderr
        assert completed.stderr == ""
        assert replay.read_bytes() == (package / "DERIVATION_RESULT.json").read_bytes()

    catches: list[dict[str, str]] = []
    mutations = [
        ("T02", "SPATIAL_TORUS_DERIVED", "spatial_slot_promotion"),
        ("T05", "S3_SELECTED_BY_MIRROR", "mirror_determinant_overclaim"),
        ("T06", "S3_UNCONDITIONALLY_SELECTED", "conditional_s3_promotion"),
        ("T07", "EXCLUDED", "lens_family_deleted"),
        ("T08", "INVALID", "finite_no_cap_countermodel_deleted"),
        ("T09", "ROUND_UNIQUE", "smoothness_round_overclaim"),
        ("T11", "CSN_SUPPLIES_CAPS", "positive_csn_crosses_caps"),
        ("T12", "UDT_SELECTED_HOPF_ACTION", "free_action_promotion"),
        ("T14", "CARRIER_DERIVED", "quotient_promoted_to_carrier"),
        ("T15", "FINITE_CELL_SELECTS_S3", "finite_cell_scope_inflation"),
        ("T16", "BOOTSTRAP_SELECTS_S3", "bootstrap_scope_inflation"),
        ("T17", "ACTION_DERIVED", "open_action_promotion"),
    ]
    for claim_id, status, name in mutations:
        changed = copy.deepcopy(ledger)
        next(row for row in changed if row["claim_id"] == claim_id)["status"] = status
        catches.append(reject(name, lambda data=changed: validate_ledger(data)))

    missing_lens = [row for row in candidates if row["family_id"] != "F05"]
    catches.append(reject("missing_lens_counterfamily", lambda: validate_candidates(missing_lens)))
    duplicate = copy.deepcopy(candidates) + [copy.deepcopy(candidates[0])]
    catches.append(reject("duplicate_candidate", lambda: validate_candidates(duplicate)))
    exceptional_free = copy.deepcopy(candidates)
    next(row for row in exceptional_free if row["family_id"] == "F12")["within_toric_status"] = "FREE_SMOOTH_QUOTIENT"
    catches.append(reject("exceptional_action_mislabeled_free", lambda: validate_candidates(exceptional_free)))

    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["exact_identities"]["collapse_determinant_classes"]["p3_mirror_exchange"] = 1
    catches.append(reject("mirror_p3_mutation", lambda: validate_algebra(bad_algebra)))
    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["registered_udt_selection"] = "S3_SELECTED"
    catches.append(reject("algebra_selection_promotion", lambda: validate_algebra(bad_algebra)))

    bad_inventory = copy.deepcopy(sources)
    bad_inventory[0]["sha256"] = "0" * 64
    catches.append(reject("source_hash_mutation", lambda: validate_sources(repo, bad_inventory)))
    c1_path = "UDT_NATIVE_ACTION_COLD_PACKET.md"
    c1 = source_text(repo, c1_path)
    bad_c1 = c1.replace(
        "the transverse spatial block or full time-live geometry",
        "the selected transverse spatial torus",
    )
    catches.append(reject(
        "transverse_open_disclosure_removed",
        lambda: validate_source_semantics(repo, {c1_path: bad_c1}),
    ))
    bootstrap_path = "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"
    bootstrap = source_text(repo, bootstrap_path)
    bad_bootstrap = bootstrap.replace(
        "The full time-live volume and boundary are not yet derived",
        "The full time-live volume and S3 boundary are selected",
    )
    catches.append(reject(
        "bootstrap_boundary_open_disclosure_removed",
        lambda: validate_source_semantics(repo, {bootstrap_path: bad_bootstrap}),
    ))
    contradictory_bootstrap = bootstrap + "\nbootstrap selects S3\n"
    catches.append(reject(
        "bootstrap_required_tokens_plus_contradiction_rejected",
        lambda: validate_source_semantics(repo, {bootstrap_path: contradictory_bootstrap}),
    ))
    canon_path = "CANON.md"
    canon = source_text(repo, canon_path)
    contradictory_canon = canon.replace(
        "physical boundary, mirrored across phi -> -phi.",
        "physical boundary, mirrored across phi -> -phi. The angular torus selects S3.",
    )
    catches.append(reject(
        "canon_required_tokens_plus_angular_contradiction_rejected",
        lambda: validate_source_semantics(repo, {canon_path: contradictory_canon}),
    ))
    bad_report = report.replace(
        "Within precisely that supplied\nclass, `S3` is not an aesthetic choice: it is `UNIQUE-CONDITIONAL`.",
        "UDT selects S3 unconditionally.",
    )
    catches.append(reject("report_s3_overclaim", lambda: validate_report(bad_report)))

    result = {
        "status": "PASS_SELF_CONSISTENCY",
        "verification_class": "BASE_PINNED_SOURCES; BYTE_IDENTICAL_REPLAY; INDEPENDENT_LATTICE_WEIGHT_ARITHMETIC; CATCH_PROOFS; FRESH_SEMANTIC_REVIEW_SEPARATE",
        "base": BASE,
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "source_rows": len(sources),
        "ledger_rows": len(ledger),
        "candidate_rows": len(candidates),
        "algebra_checks": algebra["check_count"],
        "derivation_replay": "PASS_BYTE_IDENTICAL",
        "independent_exact": independent,
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "preregistration_sha256": sha((package / "PREREGISTRATION.md").read_bytes()),
        "source_inventory_sha256": sha((package / "SOURCE_INVENTORY.tsv").read_bytes()),
        "derivation_result_sha256": sha((package / "DERIVATION_RESULT.json").read_bytes()),
        "candidate_family_sha256": sha((package / "CANDIDATE_FAMILY.tsv").read_bytes()),
        "status_ledger_sha256": sha((package / "STATUS_LEDGER.tsv").read_bytes()),
        "audit_report_sha256": sha((package / "AUDIT_REPORT.md").read_bytes()),
        "verdict": VERDICT,
    }
    pathlib.Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"VERIFIER PASS sources={len(sources)}/12 candidates={len(candidates)}/15 "
        f"ledger={len(ledger)}/18 algebra={algebra['check_count']}/25 catches={len(catches)}/{len(catches)}"
    )
    print(VERDICT)


if __name__ == "__main__":
    main()
