#!/usr/bin/env python3
"""Independent fail-closed verifier for the projective transport selector."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
import tempfile

import sympy as sp


BASE = "75c62d1a357821d4957588e640ba03f0bc0f285e"
PREREG = "9a357c525a31c6f4066e929b8f798f09773c4358"
VERDICT = (
    "CONFORMAL_NULL_GEODESIC_PROPAGATION_DERIVED_CONDITIONAL; "
    "LEVI_CIVITA_TANGENT_RAY_COMPARISON_CSN_REPRESENTATIVE_DEPENDENT; "
    "CONDITIONAL_STATIC_PHI_ROUTE_SELECTS_ONLY_A_LONGITUDINAL_NULL_PAIR; "
    "PHI_ANGULAR_PHYSICAL_SECTION_UNDERDETERMINED; "
    "CONFORMAL_TRACTOR_AND_HOPF_CONNECTIONS_TRANSPORT_REPRESENTATION_DATA_BUT_DO_NOT_SELECT_A_SECTION; "
    "GLOBAL_HOLONOMY_AND_PROJECTIVE_TO_PHYSICAL_SOLDERING_OPEN; "
    "PHYSICAL_PROJECTIVE_REALIZATION_GATE_NOT_PASSED"
)

EXPECTED_SOURCES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "CANON.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md",
    "transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv",
    "transverse_reciprocal_realization_selector_2026-07-19/DERIVATION_RESULT.json",
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md",
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv",
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md",
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md",
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
    "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md",
    "copresence_causal_accessibility_selector_2026-07-19/STATUS_LEDGER.tsv",
    "reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md",
    "reciprocal_clock_optical_scale_selector_2026-07-19/STATUS_LEDGER.tsv",
}

EXPECTED_CANDIDATES = {
    "T01": ("CONFORMAL_NULL_GEODESIC_SPRAY", "PROPAGATION_ONLY_NOT_SELECTION"),
    "T02": ("LEVI_CIVITA_HORIZONTAL_TRANSPORT", "REPRESENTATIVE_DEPENDENT"),
    "T03": ("CONFORMAL_CARTAN_TRACTOR_TRANSPORT", "REPRESENTATION_TRANSPORT_NO_SECTION"),
    "T04": ("PHI_GRADIENT_LONGITUDINAL_SELECTOR", "CONDITIONAL_LONGITUDINAL_PAIR_ONLY"),
    "T05": ("PHI_ANGULAR_HESSIAN_CURVATURE_SELECTOR", "PHYSICAL_SECTION_UNDERDETERMINED"),
    "T06": ("HOPF_PROJECTIVE_CONNECTION", "VERTICAL_REPRESENTATION_NOT_BASE_SECTION"),
    "T07": ("GLOBAL_SECTION_HOLONOMY", "GLOBAL_SECTION_HOLONOMY_OPEN"),
    "T08": ("FINITE_CELL_BOOTSTRAP", "NO_CURRENT_SELECTOR_OPERATOR"),
}

EXPECTED_LEDGER = {
    "R01": "DERIVED_CONDITIONAL",
    "R02": "DERIVED_CONDITIONAL",
    "R03": "PROPAGATION_DERIVED_CONDITIONAL",
    "R04": "NO_SELECTION",
    "R05": "CSN_COMPATIBLE_ALONG_RAY",
    "R06": "REPRESENTATIVE_DEPENDENT",
    "R07": "CANONICAL_CONDITIONAL_REPRESENTATION_TRANSPORT",
    "R08": "TYPE_GATE_OPEN",
    "R09": "CSN_INVARIANT_WHERE_NONZERO",
    "R10": "BRANCHED",
    "R11": "CONDITIONAL_LONGITUDINAL_NULL_PAIR",
    "R12": "UNDERDETERMINED",
    "R13": "REPRESENTATIVE_DEPENDENT",
    "R14": "CSN_COMPATIBLE_CONDITIONAL",
    "R15": "CONDITIONAL_STRATIFIED",
    "R16": "NO_TRACEFREE_AXIS",
    "R17": "CONDITIONAL_STRATIFIED",
    "R18": "DERIVED_CONDITIONAL_VERTICAL",
    "R19": "SECTION_REQUIRED",
    "R20": "DISTINCT",
    "R21": "HOLONOMY_DEPENDENT",
    "R22": "NO_CURRENT_OPERATOR",
    "R23": "NO_CURRENT_OPERATOR",
    "R24": "NOT_PASSED",
    "R25": "OPEN_NOT_ACTIVATED",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(repo: pathlib.Path, *command: str, binary: bool = False):
    result = subprocess.run(
        list(command), cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed {command}: {error}")
    return result.stdout


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    return run(repo, "git", *args, binary=binary)


def rows(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source(repo: pathlib.Path, path: str) -> str:
    return str(git(repo, "show", f"{BASE}:{path}"))


def reject(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        return {"name": name, "result": "PASS_REJECTED"}
    raise AssertionError(f"catch-proof accepted corruption: {name}")


def validate_prereg(repo: pathlib.Path, package: pathlib.Path) -> None:
    current = package / "PREREGISTRATION.md"
    committed = bytes(git(repo, "show", f"{PREREG}:projective_transport_section_selector_2026-07-19/PREREGISTRATION.md", binary=True))
    assert current.read_bytes() == committed
    text = committed.decode("utf-8")
    assert BASE in text
    assert "OBSERVING" in text
    assert "CONFORMAL_NULL_GEODESIC_SPRAY" in text
    assert "PHI_ANGULAR_HESSIAN_CURVATURE_SELECTOR" in text
    assert "PHYSICAL_PROJECTIVE_REALIZATION_GATE_NOT_PASSED" in text
    assert "No carrier adoption" in text


def validate_sources(repo: pathlib.Path, inventory: list[dict[str, str]]) -> None:
    assert len(inventory) == 18
    assert {row["current_path"] for row in inventory} == EXPECTED_SOURCES
    assert len({row["current_path"] for row in inventory}) == 18
    for row in inventory:
        path = row["current_path"]
        payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        assert row["blob_oid"] == str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        assert row["sha256"] == sha(payload)
        assert int(row["size_bytes"]) == len(payload)
        assert row["last_commit"] == str(git(repo, "log", "-1", "--format=%H", BASE, "--", path)).strip()


def validate_source_semantics(repo: pathlib.Path, overrides: dict[str, str] | None = None) -> None:
    overrides = overrides or {}
    texts = {path: overrides.get(path, source(repo, path)) for path in EXPECTED_SOURCES}
    assert "[g]_{\\rm CSN}" in texts["UDT_NATIVE_ACTION_COLD_PACKET.md"]
    assert "the transverse spatial block or full time-live geometry" in texts["UDT_NATIVE_ACTION_COLD_PACKET.md"]
    assert "\\Omega(x)^2g_{\\mu\\nu}:\\Omega(x)>0" in texts["UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"]
    assert "not silently inferred from the word “bootstraps.”" in texts["UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"]
    assert "a section choosing one projective direction at every event" in texts["transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md"]
    assert "a sphere fiber is not a chosen field" in texts["native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md"]
    assert "positive common-scale change does not alter who can causally reach whom" in texts["copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md"]


def validate_candidates(candidates: list[dict[str, str]]) -> None:
    assert len(candidates) == 8
    assert len({row["family_id"] for row in candidates}) == 8
    assert {row["family_id"] for row in candidates} == set(EXPECTED_CANDIDATES)
    for row in candidates:
        assert (row["family"], row["physical_section_status"]) == EXPECTED_CANDIDATES[row["family_id"]]
    t05 = next(row for row in candidates if row["family_id"] == "T05")
    assert all(token in t05["exact_positive_result"] for token in ("Petrov II", "III", "N"))
    assert "Petrov I D O" in t05["obstruction_or_limit"]
    t06 = next(row for row in candidates if row["family_id"] == "T06")
    assert "requires z(x) or n(x)" in t06["obstruction_or_limit"]


def validate_ledger(ledger: list[dict[str, str]]) -> None:
    assert len(ledger) == 25
    assert len({row["claim_id"] for row in ledger}) == 25
    assert {row["claim_id"] for row in ledger} == set(EXPECTED_LEDGER)
    for row in ledger:
        assert row["status"] == EXPECTED_LEDGER[row["claim_id"]]
    assert "every null ray" in next(row for row in ledger if row["claim_id"] == "R04")["basis"]
    assert "C(X,k)=aX" in next(row for row in ledger if row["claim_id"] == "R06")["basis"]
    assert "zero null timelike and spacelike" in next(row for row in ledger if row["claim_id"] == "R10")["basis"]
    assert "Petrov II III and N" in next(row for row in ledger if row["claim_id"] == "R17")["basis"]
    assert "requires a map z(x) or n(x)" in next(row for row in ledger if row["claim_id"] == "R19")["basis"]
    assert "identity fixes all rays" in next(row for row in ledger if row["claim_id"] == "R21")["dependency_or_limit"]
    assert next(row for row in ledger if row["claim_id"] == "R24")["status"] == "NOT_PASSED"


def validate_algebra(algebra: dict) -> None:
    assert algebra["status"] == "PASS"
    assert algebra["check_count"] == 54
    assert len(algebra["checks"]) == 54
    assert set(algebra["checks"].values()) == {"PASS"}
    assert algebra["verdict"] == VERDICT
    classification = algebra["classification"]
    assert classification["ray_propagation"] == "DERIVED_CONDITIONAL_AFTER_4D_CONFORMAL_LORENTZ_READOUT"
    assert classification["levi_civita_arbitrary_direction_transport"] == "REPRESENTATIVE_DEPENDENT_NOT_CSN_INVARIANT"
    assert classification["normal_conformal_tractor_connection"] == "CANONICAL_CONDITIONAL_REPRESENTATION_TRANSPORT_NOT_TANGENT_NULL_SECTION"
    assert classification["static_phi_route"] == "CONDITIONAL_LONGITUDINAL_NULL_PAIR_ONLY_REQUIRES_TIME_DIRECTION"
    assert "TYPES_II_III_N" in classification["weyl_principal_null_route"]
    assert classification["hopf_connection"] == "VERTICAL_REPRESENTATION_CONNECTION; SPACETIME_PULLBACK_REQUIRES_SECTION"
    assert classification["phi_angular_physical_section"] == "UNDERDETERMINED_NOT_DERIVED"
    assert classification["physical_projective_realization_gate"] == "NOT_PASSED"
    assert set(algebra["counterfamilies"]) == {
        "flat_trivial_phi_many_sections",
        "reciprocal_warped_transverse_so2",
        "generic_noncommuting_holonomy",
        "single_axis_holonomy_pair",
        "hopf_connection_without_base_map",
    }


def validate_report(report: str) -> None:
    required = [
        VERDICT,
        "the road system for light",
        "Propagation:",
        "X_(fH)=f X_H + H X_f",
        "a X",
        "rank six",
        "Complete `d phi` branch census",
        "p^b nabla_b p_a = (1/2) nabla_a(P)=0",
        "Petrov types II, III, and N",
        "A principal null direction is also not automatically geodesic",
        "a=z-star A",
        "[k_x] in Fix(Hol_x)",
        "UNDERDETERMINED_NOT_DERIVED",
        "No carrier or fixed round target is derived",
        "globally null/eikonal `d phi`",
    ]
    for token in required:
        assert token in report, token
    lower = report.lower()
    forbidden = [
        "the carrier is derived",
        "petrov type is forced by udt",
        "physical_projective_realization_gate_passed",
        "bootstrap selects the section",
        "the hopf connection creates the spacetime section",
        "the cap gate is activated",
    ]
    for token in forbidden:
        assert token not in lower, token


def independent_exact() -> dict[str, str]:
    q, p0, p1, w = sp.symbols("q p0 p1 w", real=True)
    H = (-p0**2 + p1**2) / 2
    f = sp.exp(-2 * w * q)
    XH = sp.Matrix([-p0, p1, 0, 0])
    XfH = sp.Matrix([sp.diff(f * H, p0), sp.diff(f * H, p1), 0, -sp.diff(f * H, q)])
    Xf = sp.Matrix([0, 0, 0, -sp.diff(f, q)])
    assert sp.simplify(XfH - f * XH - H * Xf) == sp.zeros(4, 1)
    assert sp.simplify((XfH - f * XH).subs(p1, p0)) == sp.zeros(4, 1)

    eta = sp.diag(-1, 1, 1, 1)
    a = sp.symbols("a", real=True, nonzero=True)
    k = sp.Matrix([1, 0, 0, 1])
    X = sp.Matrix([0, 1, 0, 0])
    dw = sp.Matrix([0, 0, 0, a])
    delta = X * (k.T * dw)[0] + k * (X.T * dw)[0] - (X.T * eta * k)[0] * eta.inv() * dw
    assert sp.simplify(delta - a * X) == sp.zeros(4, 1)
    assert sp.Matrix.hstack(k, delta.subs(a, 1)).rank() == 2

    s = sp.symbols("s", real=True)
    path_X = sp.Matrix([0, 0, 1, 0])
    path_dw = sp.Matrix([0, a, 0, 0])
    v = sp.Matrix([1, sp.cos(a * s), -sp.sin(a * s), 0])
    C = path_X * (v.T * path_dw)[0] + v * (path_X.T * path_dw)[0] - (path_X.T * eta * v)[0] * eta.inv() * path_dw
    assert sp.simplify(sp.diff(v, s) + C) == sp.zeros(4, 1)
    assert sp.simplify((v.T * eta * v)[0]) == 0

    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([0, 1, 0, 0])
    assert (u + n).dot(eta * (u + n)) == 0
    assert (u - n).dot(eta * (u - n)) == 0

    pA = sp.Matrix([1, 0])
    wA = sp.Matrix([0, 1])
    shift = -wA * pA.T - pA * wA.T
    shift_stf = shift - sp.trace(shift) * sp.eye(2) / 2
    assert shift_stf == sp.Matrix([[0, -1], [-1, 0]])
    assert sp.zeros(2) == sp.zeros(2) - sp.trace(sp.zeros(2)) * sp.eye(2) / 2

    b = sp.symbols("b")
    assert sorted(sp.roots(b**2 * (b - 1) * (b + 1), b).values()) == [1, 1, 2]
    assert sorted(sp.roots(b**3 * (b - 1), b).values()) == [1, 3]
    assert sp.roots(b**4, b) == {sp.Integer(0): 4}

    eta_h = sp.symbols("eta_h", real=True)
    A1, A2 = sp.cos(eta_h)**2, sp.sin(eta_h)**2
    assert sp.simplify(A1 + A2 - 1) == 0

    Rz = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    Rx = sp.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    assert len((Rz - sp.eye(3)).nullspace()) == 1
    stacked = (Rz - sp.eye(3)).col_join(Rx - sp.eye(3))
    assert stacked.nullspace() == []
    assert len(sp.zeros(3).nullspace()) == 3
    return {
        "null_hamiltonian_conformal_identity": "PASS",
        "null_shell_projective_spray": "PASS",
        "arbitrary_levi_civita_discrepancy": "PASS",
        "integrated_parallel_transport_counterexample": "PASS",
        "conditional_longitudinal_null_pair": "PASS",
        "angular_hessian_conformal_branching": "PASS",
        "petrov_multiplicity_selectors": "PASS",
        "hopf_vertical_connection": "PASS",
        "holonomy_fixed_set_census": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent

    validate_prereg(repo, package)
    inventory = rows(package / "SOURCE_INVENTORY.tsv")
    candidates = rows(package / "CANDIDATE_FAMILY.tsv")
    ledger = rows(package / "STATUS_LEDGER.tsv")
    algebra = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    validate_sources(repo, inventory)
    validate_source_semantics(repo)
    validate_candidates(candidates)
    validate_ledger(ledger)
    validate_algebra(algebra)
    validate_report(report)
    independent = independent_exact()

    with tempfile.TemporaryDirectory(prefix="projective_transport_replay_") as temp:
        replay = pathlib.Path(temp) / "DERIVATION_RESULT.json"
        process = subprocess.run(
            [sys.executable, str(package / "derive_projective_transport_selector.py"), "--output", str(replay)],
            cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        assert process.returncode == 0, process.stderr
        assert process.stderr == ""
        assert replay.read_bytes() == (package / "DERIVATION_RESULT.json").read_bytes()

    catches: list[dict[str, str]] = []
    ledger_mutations = [
        ("R03", "SELECTS_UNIQUE_RAY", "propagation_promoted_to_selection"),
        ("R04", "PHYSICAL_SECTION_DERIVED", "all_ray_spray_promoted"),
        ("R06", "CSN_INVARIANT", "levi_civita_representative_dependence_removed"),
        ("R08", "TANGENT_SECTION_DERIVED", "tractor_type_gate_removed"),
        ("R10", "ONLY_NULL_BRANCH", "dphi_branch_census_filtered"),
        ("R11", "UNCONDITIONAL_UNIQUE_SECTION", "static_time_premise_removed"),
        ("R13", "CSN_INVARIANT_GENERAL", "angular_hessian_promotion"),
        ("R15", "GLOBAL_PERIODIC_AXES", "hessian_stratum_promotion"),
        ("R17", "UDT_FORCES_PETROV_N", "petrov_type_promotion"),
        ("R18", "PHYSICAL_SPACETIME_CONNECTION", "hopf_vertical_type_removed"),
        ("R19", "SECTION_DERIVED", "hopf_pullback_circularity_removed"),
        ("R21", "UNIQUE_HOLONOMY_SECTION", "holonomy_census_removed"),
        ("R22", "FINITE_CELL_SELECTS_RAY", "finite_cell_scope_inflation"),
        ("R23", "BOOTSTRAP_SELECTS_RAY", "bootstrap_scope_inflation"),
        ("R24", "PASSED", "physical_gate_promotion"),
        ("R25", "CAP_ACTIVATED", "downstream_gate_activation"),
    ]
    for claim_id, status, name in ledger_mutations:
        changed = copy.deepcopy(ledger)
        next(row for row in changed if row["claim_id"] == claim_id)["status"] = status
        catches.append(reject(name, lambda data=changed: validate_ledger(data)))

    catches.append(reject("missing_candidate", lambda: validate_candidates(candidates[:-1])))
    catches.append(reject("duplicate_candidate", lambda: validate_candidates(candidates + [copy.deepcopy(candidates[0])])))
    changed_candidates = copy.deepcopy(candidates)
    next(row for row in changed_candidates if row["family_id"] == "T01")["physical_section_status"] = "UNIQUE_SECTION"
    catches.append(reject("spray_candidate_promoted", lambda: validate_candidates(changed_candidates)))
    changed_candidates = copy.deepcopy(candidates)
    next(row for row in changed_candidates if row["family_id"] == "T05")["obstruction_or_limit"] = "UDT forces Petrov N"
    catches.append(reject("petrov_counterstrata_removed", lambda: validate_candidates(changed_candidates)))
    changed_candidates = copy.deepcopy(candidates)
    next(row for row in changed_candidates if row["family_id"] == "T06")["obstruction_or_limit"] = "connection creates n(x)"
    catches.append(reject("hopf_section_circularity_removed", lambda: validate_candidates(changed_candidates)))

    bad_source = copy.deepcopy(inventory)
    bad_source[0]["sha256"] = "0" * 64
    catches.append(reject("source_hash_mutation", lambda: validate_sources(repo, bad_source)))
    cold_path = "UDT_NATIVE_ACTION_COLD_PACKET.md"
    cold = source(repo, cold_path)
    catches.append(reject(
        "transverse_open_slot_removed",
        lambda: validate_source_semantics(repo, {cold_path: cold.replace("the transverse spatial block or full time-live geometry", "the selected projective carrier section")}),
    ))
    prior_path = "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md"
    prior = source(repo, prior_path)
    catches.append(reject(
        "prior_section_gate_removed",
        lambda: validate_source_semantics(repo, {prior_path: prior.replace("a section choosing one projective direction at every event", "a derived section")}),
    ))

    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["levi_civita_arbitrary_direction_transport"] = "CSN_INVARIANT"
    catches.append(reject("algebra_levi_civita_promotion", lambda: validate_algebra(bad_algebra)))
    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["normal_conformal_tractor_connection"] = "PHYSICAL_TANGENT_SECTION"
    catches.append(reject("algebra_tractor_promotion", lambda: validate_algebra(bad_algebra)))
    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["phi_angular_physical_section"] = "DERIVED"
    catches.append(reject("algebra_phi_angular_promotion", lambda: validate_algebra(bad_algebra)))
    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["physical_projective_realization_gate"] = "PASSED"
    catches.append(reject("algebra_physical_gate_promotion", lambda: validate_algebra(bad_algebra)))
    bad_report = report.replace("the road system for light", "the carrier is derived")
    catches.append(reject("report_carrier_overclaim", lambda: validate_report(bad_report)))
    bad_report = report.replace("No current result says that theorem is true", "Petrov type is forced by UDT")
    catches.append(reject("report_petrov_overclaim", lambda: validate_report(bad_report)))

    result = {
        "status": "PASS_SELF_CONSISTENCY",
        "verification_class": "BASE_PINNED_SOURCES; BYTE_IDENTICAL_REPLAY; INDEPENDENT_CONFORMAL_TRANSPORT_ALGEBRA; CATCH_PROOFS; FRESH_SEMANTIC_REVIEW_SEPARATE",
        "base": BASE,
        "preregistration_commit": PREREG,
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "source_rows": len(inventory),
        "candidate_rows": len(candidates),
        "ledger_rows": len(ledger),
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
        f"VERIFIER PASS sources={len(inventory)}/18 candidates={len(candidates)}/8 "
        f"ledger={len(ledger)}/25 algebra={algebra['check_count']}/54 catches={len(catches)}/{len(catches)}"
    )
    print(VERDICT)


if __name__ == "__main__":
    main()
