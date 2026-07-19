#!/usr/bin/env python3
"""Independent fail-closed verifier for the bootstrap/CSN selector audit."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import pathlib
import platform
import subprocess
import tempfile

import sympy as sp


BASE = "58a3fa8dbc7b4cb7de55313efc361194fdc65114"
PREREG = "4e5b0ba413d83d9c69c972a11517e42b18b52005"
VERDICT = (
    "EXACT_CSN_INVARIANCE_OF_A_CHOSEN_ACTION_IMPLIES_A_GAUGE_NOETHER_IDENTITY_NOT_A_PHI_ANGULAR_EOM; "
    "BOOTSTRAP_SUPPLIES_GLOBAL_ADMISSIBILITY_NOT_CURRENT_LOCAL_SELECTOR; "
    "EIKONAL_UNIQUE_CONDITIONAL_ONLY_WITHIN_LOCAL_DIFF_COVARIANT_METRIC_PLUS_ONE_WEIGHT_ZERO_COVECTOR_HOMOGENEOUS_QUADRATIC_FIRST_JET_SCALAR_CLASS; "
    "ALGEBRAIC_SPECIALITY_CSN_COMPATIBLE_BUT_UNIQUE_PND_NOT_FORCED; "
    "CONDITIONAL_C2_BACH_AND_ZERO_LAMBDA_EH_DO_NOT_FORCE_TARGET; "
    "NO_LOCAL_SELECTOR_FOR_NULL_DPHI_OR_ONE_UNIQUE_REPEATED_PND_IS_DERIVED_FROM_THE_FROZEN_POST_JULY_1_C0_C1_PLUS_CURRENT_CSN_BOOTSTRAP_SOURCE_SET"
)

EXPECTED_SOURCES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "CANON.md",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md",
    "bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv",
    "bootstrap_variation_selector_2026-07-18/PREMISE_LEDGER.tsv",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_RESULT.json",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md",
    "projective_transport_section_selector_2026-07-19/STATUS_LEDGER.tsv",
    "projective_transport_section_selector_2026-07-19/DERIVATION_RESULT.json",
    "reciprocal_metric_null_line_selector_2026-07-19/AUDIT_REPORT.md",
    "reciprocal_metric_null_line_selector_2026-07-19/STATUS_LEDGER.tsv",
    "reciprocal_metric_null_line_selector_2026-07-19/DERIVATION_RESULT.json",
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md",
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
}

EXPECTED_CANDIDATES = {
    "B01": ("CSN_NOETHER_TRACE_IDENTITY", "CONDITIONAL_GAUGE_IDENTITY"),
    "B02": ("RECIPROCAL_PHI_TANGENT_EQUATION", "INDEPENDENT_NOT_FORCED"),
    "B03": ("ANGULAR_TRACEFREE_EQUATION", "INDEPENDENT_NOT_FORCED"),
    "B04": ("BOOTSTRAP_AFTER_SOLUTION_PREDICATE", "CURRENT_SEMANTICS_NO_LOCAL_OPERATOR"),
    "B05": ("BOOTSTRAP_VARIED_GLOBAL_CONSTRAINT", "FORM_ONLY_UNDERDETERMINED"),
    "B06": ("BOOTSTRAP_REPRESENTATIVE_SELECTION", "FORM_ONLY_UNDERDETERMINED"),
    "B07": ("LOCAL_EIKONAL_MINIMALITY", "UNIQUE_CONDITIONAL"),
    "B08": ("WEYL_SPECIALITY_DISCRIMINANT", "CSN_COMPATIBLE_NOT_SELECTED"),
    "B09": ("PHI_WEYL_ALIGNMENT", "NO_FOUNDATION_OPERATOR"),
    "B10": ("CONDITIONAL_C2_BACH", "DOES_NOT_FORCE_TARGET"),
    "B11": ("CONDITIONAL_POST_SCALE_EH", "DOES_NOT_FORCE_TARGET"),
    "B12": ("FINITE_CELL_GLOBAL_CONTINUATION", "NO_CURRENT_POINTWISE_SELECTOR"),
}

EXPECTED_LEDGER = {
    "R01": "FOUNDING", "R02": "FOUNDING", "R03": "DERIVED_EXACT",
    "R04": "DERIVED_CONDITIONAL", "R05": "DERIVED_CONDITIONAL",
    "R06": "REFUTED_EXACT", "R07": "REFUTED_EXACT", "R08": "WORKING",
    "R09": "NOT_PRESENT", "R10": "CONDITIONAL_FORM", "R11": "CONDITIONAL_FORM",
    "R12": "UNDERDETERMINED", "R13": "DERIVED_CONDITIONAL", "R14": "UNIQUE_CONDITIONAL",
    "R15": "NOT_DERIVED", "R16": "DERIVED_CONDITIONAL", "R17": "REFUTED_EXACT",
    "R18": "NOT_PRESENT", "R19": "OBSERVED_EXACT", "R20": "OBSERVED_EXACT",
    "R21": "DERIVED_CONDITIONAL", "R22": "OBSERVED_EXACT", "R23": "OBSERVED_EXACT",
    "R24": "OBSERVED_EXACT", "R25": "REFUTED_WITHIN_CONDITIONAL_CLASS",
    "R26": "REFUTED_WITHIN_CONDITIONAL_CLASS", "R27": "NOT_DERIVED",
    "R28": "NOT_PRESENT", "R29": "NOT_DERIVED_FROM_AUDITED_SOURCE_SET",
    "R30": "NOT_CLAIMED", "R31": "OPEN", "R32": "NOT_DERIVED",
    "R33": "NOT_DERIVED", "R34": "NOT_ACTIVATED",
    "R35": "HISTORICAL_CANON_OUTSIDE_AFFIRMATIVE_AUDIT",
}


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run(repo: pathlib.Path, *command: str, binary: bool = False):
    result = subprocess.run(
        list(command), cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        stderr = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed {command}: {stderr}")
    return result.stdout


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    return run(repo, "git", *args, binary=binary)


def table(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def base_text(repo: pathlib.Path, path: str) -> str:
    return str(git(repo, "show", f"{BASE}:{path}"))


def reject(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        return {"name": name, "result": "PASS_REJECTED"}
    raise AssertionError(f"catch-proof accepted corruption: {name}")


def validate_prereg(repo: pathlib.Path, package: pathlib.Path) -> None:
    registered = bytes(git(repo, "show", f"{PREREG}:bootstrap_csn_phi_angular_selector_2026-07-19/PREREGISTRATION.md", binary=True))
    assert package.joinpath("PREREGISTRATION.md").read_bytes() == registered
    text = registered.decode("utf-8")
    assert BASE in text
    assert "**OBSERVING.**" in text
    assert "CSN_NOETHER_TRACE_IDENTITY" in text
    assert "Kasner exponents `(-2/7,3/7,6/7)`" in text
    assert "No carrier" in text


def validate_sources(repo: pathlib.Path, rows: list[dict[str, str]]) -> None:
    assert len(rows) == 20
    assert len({row["current_path"] for row in rows}) == 20
    assert {row["current_path"] for row in rows} == EXPECTED_SOURCES
    for row in rows:
        path = row["current_path"]
        payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        assert row["blob_oid"] == str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        assert row["sha256"] == sha(payload)
        assert int(row["size_bytes"]) == len(payload)
        assert row["last_commit"] == str(git(repo, "log", "-1", "--format=%H", BASE, "--", path)).strip()
    canon_row = next(row for row in rows if row["current_path"] == "CANON.md")
    assert "C-2026-06-10-3" in canon_row["load_bearing_use"]
    assert "not selector-adjudicated" in canon_row["load_bearing_use"]


def validate_source_semantics(repo: pathlib.Path, overrides: dict[str, str] | None = None) -> None:
    overrides = overrides or {}
    texts = {path: overrides.get(path, base_text(repo, path)) for path in EXPECTED_SOURCES}
    assert "Common-Scale Neutrality declares the first factor calibrational" in texts["UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"]
    assert "whether the action is local" in texts["UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"]
    assert "Stronger local reading" in texts["UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"]
    assert "it is not silently inferred" in texts["UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"]
    assert "separately derived global variational condition" in texts["UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"]
    assert "does not specify the off-shell fields" in texts["bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md"]
    assert "B01 does not entail a unique variation" in texts["bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md"]
    assert "Bootstrap closure | `WORKING`; selector mechanism `OPEN`" in texts["UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md"]
    assert "C-2026-06-10-3" in texts["CANON.md"]
    assert "pre-July CANON entries" in texts["native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md"]
    assert "Petrov types II, III, and N" in texts["projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md"]
    assert "RECIPROCAL_ANISOTROPIC_PETROV_I_COUNTERFAMILY_EXISTS" in texts["reciprocal_metric_null_line_selector_2026-07-19/AUDIT_REPORT.md"]


def validate_candidates(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 12
    assert len({row["family_id"] for row in rows}) == 12
    assert {row["family_id"] for row in rows} == set(EXPECTED_CANDIDATES)
    for row in rows:
        assert (row["family"], row["selector_ruling"]) == EXPECTED_CANDIDATES[row["family_id"]]
    b01 = next(row for row in rows if row["family_id"] == "B01")
    assert b01["foundation_status"] == "CONDITIONAL_ON_CHOSEN_CSN_INVARIANT_ACTION"
    assert "Inhomogeneous" in b01["missing_or_limit"]
    b03 = next(row for row in rows if row["family_id"] == "B03")
    assert "angular shape free" in b03["missing_or_limit"]
    b05 = next(row for row in rows if row["family_id"] == "B05")
    assert "not supplied" in b05["missing_or_limit"]
    b07 = next(row for row in rows if row["family_id"] == "B07")
    assert b07["foundation_status"] == "CONDITIONAL_CLASS"
    assert "nowhere-zero" in b07["missing_or_limit"] and "none is selected" in b07["missing_or_limit"]
    b08 = next(row for row in rows if row["family_id"] == "B08")
    assert "D has two" in b08["missing_or_limit"] and "Weyl tensor vanishes" in b08["missing_or_limit"]


def validate_ledger(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 35
    assert len({row["claim_id"] for row in rows}) == 35
    assert {row["claim_id"] for row in rows} == set(EXPECTED_LEDGER)
    for row in rows:
        assert row["status"] == EXPECTED_LEDGER[row["claim_id"]]
    assert "future complete bootstrap functional" in next(row for row in rows if row["claim_id"] == "R09")["dependency_or_limit"]
    assert "complete-UDT countermodel" in next(row for row in rows if row["claim_id"] == "R25")["dependency_or_limit"]
    assert "No carrier" in next(row for row in rows if row["claim_id"] == "R34")["dependency_or_limit"]


def validate_algebra(data: dict) -> None:
    assert data["status"] == "PASS"
    assert data["check_count"] == 43
    assert len(data["checks"]) == 43
    assert set(data["checks"].values()) == {"PASS"}
    assert data["verdict"] == VERDICT
    exact = data["exact_identities"]
    assert exact["tangent_rank"] == 3
    assert exact["euler_projections"] == {
        "angular_tracefree": "E2 - E3",
        "csn_trace": "E0 + E1 + E2 + E3",
        "reciprocal_phi": "-E0 + E1",
    }
    assert exact["phi_counterprojection"] == "-2"
    assert exact["angular_counterprojection"] == "2"
    assert exact["quadratic_first_jet_coefficient"].startswith("c_quad != 0")
    assert "derivatives of Euler expressions" in exact["csn_noether_general_caveat"]
    assert exact["petrov_root_multiplicities"] == {
        "I": [1, 1, 1, 1], "II": [1, 1, 2], "D": [2, 2],
        "III": [1, 3], "N": [4], "O": [],
    }
    assert exact["petrov_O_sentinel"].startswith("[] means Weyl vanishes")
    assert exact["kasner_exponents"] == ["-2/7", "3/7", "6/7"]
    assert exact["kasner_ricci"] == [["0"] * 4 for _ in range(4)]
    assert exact["kasner_np"] == {
        "psi0": "-3/(49*t**2)", "psi1": "0", "psi2": "9/(49*t**2)",
        "psi3": "0", "psi4": "-3/(49*t**2)",
    }
    assert exact["kasner_pnd_polynomial"] == "-3*(z**2 - 4*z - 1)*(z**2 + 4*z - 1)/(49*t**2)"
    assert exact["kasner_pnd_discriminant"] == "1194393600/(13841287201*t**12)"
    assert exact["kasner_dphi_norm"].startswith("-4*")
    classes = data["operator_classification"]
    assert "CONDITIONAL_ON_EXACT_CSN_INVARIANCE" in classes["CSN_NOETHER_TRACE_IDENTITY"]
    assert classes["BOOTSTRAP_AFTER_SOLUTION_PREDICATE"] == "NO_LOCAL_OPERATOR"
    assert classes["LOCAL_EIKONAL_MINIMALITY"].startswith("UNIQUE_CONDITIONAL")
    assert classes["CONDITIONAL_POST_SCALE_EH"].startswith("ZERO_LAMBDA_VACUUM")
    assert "not a complete matter-bearing UDT universe" in data["scope_caveat"]


def validate_report(report: str) -> None:
    normalized = " ".join(report.split())
    required = [
        VERDICT,
        "They have rank three",
        "off-shell dependency",
        "C-2026-06-10-3",
        "post–July-1",
        "after-solution admissibility condition",
        "the functional `B`",
        "`Sigma` and that normal condition are not supplied",
        "UNIQUE-CONDITIONAL",
        "D | `2,2`",
        "No Einstein dynamics or Goldberg–Sachs implication",
        "g_{\\tau\\tau}g_{xx}=-1",
        "not a complete UDT universe",
        "bootstrap-to-local map",
        "No carrier, complete action, mass, stability, cosmology, or new canon claim follows",
    ]
    for token in required:
        assert token in normalized, token
    forbidden = [
        "csn forces the eikonal equation",
        "petrov d selects one direction",
        "kasner is a complete udt universe",
        "the carrier is derived",
        "bootstrap functional is known",
        "goldberg–sachs proves",
    ]
    lower = report.lower()
    for token in forbidden:
        assert token not in lower, token


def independent_exact() -> dict[str, str]:
    # Independent local linear algebra, not imported from the derivation module.
    common = sp.Matrix([1, 1, 1, 1])
    reciprocal = sp.Matrix([-1, 1, 0, 0])
    shear = sp.Matrix([0, 0, 1, -1])
    assert sp.Matrix.hstack(common, reciprocal, shear).rank() == 3
    assert common.dot(reciprocal) == common.dot(shear) == reciprocal.dot(shear) == 0
    assert common.dot(sp.Matrix([1, -1, 0, 0])) == 0
    assert reciprocal.dot(sp.Matrix([1, -1, 0, 0])) == -2
    assert common.dot(sp.Matrix([0, 0, 1, -1])) == 0
    assert shear.dot(sp.Matrix([0, 0, 1, -1])) == 2

    # Independent analytic Kasner formulas.
    t, tau, z = sp.symbols("t tau z", positive=True)
    p = (-sp.Rational(2, 7), sp.Rational(3, 7), sp.Rational(6, 7))
    assert sum(p) == 1 and sum(value**2 for value in p) == 1
    ricci_tt_coefficient = sp.simplify(sum(p) - sum(value**2 for value in p))
    ricci_spatial_coefficients = [sp.simplify(value * (sum(p) - 1)) for value in p]
    assert ricci_tt_coefficient == 0 and ricci_spatial_coefficients == [0, 0, 0]

    electric = [sp.simplify(value * (value - 1) / t**2) for value in p]
    assert electric == [sp.Rational(18, 49)/t**2, -sp.Rational(12, 49)/t**2, -sp.Rational(6, 49)/t**2]
    assert sum(electric) == 0 and len(set(electric)) == 3
    psi0 = sp.simplify((electric[1] - electric[2]) / 2)
    psi2 = sp.simplify(electric[0] / 2)
    assert psi0 == -sp.Rational(3, 49)/t**2
    assert psi2 == sp.Rational(9, 49)/t**2
    polynomial = sp.factor(psi0 + 6*psi2*z**2 + psi0*z**4)
    expected_polynomial = -3*(z**2 - 4*z - 1)*(z**2 + 4*z - 1)/(49*t**2)
    assert sp.simplify(polynomial - expected_polynomial) == 0
    expected_discriminant = sp.Rational(1194393600, 13841287201)/t**12
    assert sp.simplify(sp.discriminant(polynomial, z) - expected_discriminant) == 0

    t_tau = (sp.Rational(5, 7)*tau)**sp.Rational(7, 5)
    gtt = -sp.diff(t_tau, tau)**2
    gxx = t_tau**(2*p[0])
    assert sp.simplify(gtt*gxx + 1) == 0
    phi = p[0]*sp.log(t_tau)
    assert sp.simplify(gtt + sp.exp(-2*phi)) == 0
    assert sp.simplify(gxx - sp.exp(2*phi)) == 0
    norm = sp.simplify(sp.diff(phi, tau)**2/gtt)
    assert norm.is_negative is True

    omega = sp.symbols("omega", positive=True)
    norm_symbol, delta_symbol = sp.symbols("norm_symbol delta_symbol")
    assert sp.simplify(omega**-2*norm_symbol - norm_symbol/omega**2) == 0
    assert sp.simplify(omega**-12*delta_symbol - delta_symbol/omega**12) == 0

    assert sorted(sp.roots(z**2*(z-1)*(z+1), z).values()) == [1, 1, 2]
    assert sorted(sp.roots(z**2*(z-1)**2, z).values()) == [2, 2]
    assert sorted(sp.roots(z**3*(z-1), z).values()) == [1, 3]
    assert sp.roots(z**4, z) == {0: 4}
    return {
        "independent_tangent_rank": "PASS",
        "independent_trace_counterprojections": "PASS",
        "analytic_kasner_ricci": "PASS",
        "analytic_kasner_electric_weyl": "PASS",
        "analytic_kasner_pnd_discriminant": "PASS",
        "independent_reciprocal_time_map": "PASS",
        "independent_timelike_dphi": "PASS",
        "independent_conformal_zero_sets": "PASS",
        "independent_petrov_multiplicities": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent

    inventory = table(package / "SOURCE_INVENTORY.tsv")
    candidates = table(package / "CANDIDATE_OPERATOR.tsv")
    ledger = table(package / "STATUS_LEDGER.tsv")
    data = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    validate_prereg(repo, package)
    validate_sources(repo, inventory)
    validate_source_semantics(repo)
    validate_candidates(candidates)
    validate_ledger(ledger)
    validate_algebra(data)
    validate_report(report)

    with tempfile.TemporaryDirectory() as temporary:
        replay = pathlib.Path(temporary) / "replay.json"
        run(repo, "python3", str(package / "derive_bootstrap_csn_phi_angular.py"), "--output", str(replay))
        replay_data = json.loads(replay.read_text(encoding="utf-8"))
        assert replay_data == data

    independent = independent_exact()

    catches: list[dict[str, str]] = []
    corrupted = copy.deepcopy(data)
    corrupted["exact_identities"]["tangent_rank"] = 2
    catches.append(reject("dropped_independent_tangent", lambda: validate_algebra(corrupted)))

    corrupted_candidates = copy.deepcopy(candidates)
    next(row for row in corrupted_candidates if row["family_id"] == "B01")["selector_ruling"] = "PHI_EOM_FORCED"
    catches.append(reject("trace_identity_promoted_to_phi_eom", lambda: validate_candidates(corrupted_candidates)))

    corrupted_candidates = copy.deepcopy(candidates)
    next(row for row in corrupted_candidates if row["family_id"] == "B01")["foundation_status"] = "FOUNDING"
    catches.append(reject("noether_identity_detached_from_chosen_action", lambda: validate_candidates(corrupted_candidates)))

    corrupted_candidates = [row for row in candidates if row["family_id"] != "B03"]
    catches.append(reject("angular_tracefree_family_dropped", lambda: validate_candidates(corrupted_candidates)))

    corrupted_candidates = copy.deepcopy(candidates)
    next(row for row in corrupted_candidates if row["family_id"] == "B05")["missing_or_limit"] = "B supplied"
    catches.append(reject("bootstrap_functional_invented", lambda: validate_candidates(corrupted_candidates)))

    corrupted_candidates = copy.deepcopy(candidates)
    next(row for row in corrupted_candidates if row["family_id"] == "B07")["foundation_status"] = "FOUNDING"
    catches.append(reject("eikonal_conditional_class_promoted", lambda: validate_candidates(corrupted_candidates)))

    corrupted_candidates = copy.deepcopy(candidates)
    b07_corrupt = next(row for row in corrupted_candidates if row["family_id"] == "B07")
    b07_corrupt["missing_or_limit"] = b07_corrupt["missing_or_limit"].replace("nowhere-zero", "arbitrary")
    catches.append(reject("eikonal_nowhere_zero_coefficient_dropped", lambda: validate_candidates(corrupted_candidates)))

    corrupted_candidates = copy.deepcopy(candidates)
    next(row for row in corrupted_candidates if row["family_id"] == "B08")["missing_or_limit"] = "D has one unique PND"
    catches.append(reject("petrov_d_called_unique", lambda: validate_candidates(corrupted_candidates)))

    corrupted = copy.deepcopy(data)
    corrupted["exact_identities"]["petrov_root_multiplicities"]["D"] = [2, 1, 1]
    catches.append(reject("petrov_d_multiplicity_mutated", lambda: validate_algebra(corrupted)))

    corrupted = copy.deepcopy(data)
    corrupted["exact_identities"]["petrov_root_multiplicities"]["O"] = [4]
    catches.append(reject("petrov_o_given_selected_line", lambda: validate_algebra(corrupted)))

    corrupted = copy.deepcopy(data)
    corrupted["exact_identities"]["kasner_pnd_discriminant"] = "0"
    catches.append(reject("kasner_petrov_i_counterwitness_removed", lambda: validate_algebra(corrupted)))

    corrupted_ledger = copy.deepcopy(ledger)
    next(row for row in corrupted_ledger if row["claim_id"] == "R26")["status"] = "NATIVE_EH_DERIVED"
    catches.append(reject("einstein_comparison_imported_as_native", lambda: validate_ledger(corrupted_ledger)))

    corrupted_ledger = copy.deepcopy(ledger)
    next(row for row in corrupted_ledger if row["claim_id"] == "R34")["status"] = "CARRIER_ACTIVATED"
    catches.append(reject("carrier_activation", lambda: validate_ledger(corrupted_ledger)))

    corrupted_report = report + "\nKasner is a complete UDT universe.\n"
    catches.append(reject("conditional_witness_called_complete_universe", lambda: validate_report(corrupted_report)))

    corrupted_report = report.replace("C-2026-06-10-3", "HISTORICAL_CANON_HIDDEN")
    catches.append(reject("historical_canon_scope_exception_hidden", lambda: validate_report(corrupted_report)))

    csn_path = "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"
    csn_corrupt = base_text(repo, csn_path).replace("whether the action is local", "")
    catches.append(reject("csn_open_locality_disclosure_removed", lambda: validate_source_semantics(repo, {csn_path: csn_corrupt})))

    bootstrap_path = "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"
    bootstrap_corrupt = base_text(repo, bootstrap_path).replace("it is not silently inferred", "it is inferred")
    catches.append(reject("bootstrap_stronger_local_fork_silently_imported", lambda: validate_source_semantics(repo, {bootstrap_path: bootstrap_corrupt})))

    result = {
        "status": "PASS",
        "mode": "FRESH_INDEPENDENT_ANALYTIC_AND_FAIL_CLOSED_PACKAGE_VERIFICATION",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "base": BASE,
        "preregistration_commit": PREREG,
        "source_rows": len(inventory),
        "candidate_rows": len(candidates),
        "ledger_rows": len(ledger),
        "derivation_checks": data["check_count"],
        "replay_byte_equivalent_json": True,
        "independent_check_count": len(independent),
        "independent_checks": independent,
        "catch_count": len(catches),
        "catch_proofs": catches,
        "verdict": VERDICT,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"VERIFICATION PASS independent={len(independent)} catches={len(catches)}")
    print(VERDICT)


if __name__ == "__main__":
    main()
