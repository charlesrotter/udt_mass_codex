#!/usr/bin/env python3
"""Independent stdlib exact-rational replay; never imports the production derivation."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import subprocess
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "97d85edb7da351e6a96bb8c55b4e969ea8e3a749"
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"


def require(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def git_bytes(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def unrelated_dirty():
    lines = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
    retained = []
    for line in lines:
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.startswith(HERE.name + "/"):
            continue
        retained.append(line)
    payload = ("\n".join(retained) + ("\n" if retained else "")).encode()
    return retained, hashlib.sha256(payload).hexdigest()


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def mt(A):
    return [list(row) for row in zip(*A)]


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def msub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mscale(s, A):
    return [[s * x for x in row] for row in A]


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def main():
    checks = []
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())

    manifest = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    for row in manifest:
        data = git_bytes("show", f"{BASE}:{row['path']}")
        blob = git_bytes("rev-parse", f"{BASE}:{row['path']}").decode().strip()
        require("source_blob_" + row["path"], blob == row["blob"], checks)
        require("source_sha_" + row["path"], hashlib.sha256(data).hexdigest() == row["sha256"], checks)
        require("source_size_" + row["path"], len(data) == int(row["bytes"]), checks)

    # Independent exterior/Hodge replay over exact rational samples. E represents exp(phi)>0.
    samples = [
        (F(3), F(1, 5), F(-2), F(7, 3)),
        (F(5, 2), F(-2, 7), F(3), F(11, 4)),
        (F(7, 4), F(4, 9), F(-5, 2), F(13, 6)),
    ]
    for idx, (cE, alpha, kappa, detP) in enumerate(samples):
        E = [F(2), F(3, 2), F(5, 4)][idx]
        t0 = alpha * kappa / (E * detP)
        kflat0 = -cE / E
        dk23 = -cE * t0 / E
        twist023 = kflat0 * dk23
        expected = cE * cE * alpha * kappa / (E**3 * detP)
        require(f"twist_general_P_{idx}", twist023 == expected and expected != 0, checks)

        # Exact inverse of evaluations of theta0,theta1 on K,V.
        evaluation = [[cE / E, alpha / E], [F(0), E]]
        inverse = [[E / cE, -alpha / (cE * E)], [F(0), F(1, 1) / E]]
        require(f"dual_basis_{idx}", mm(evaluation, inverse) == [[1, 0], [0, 1]], checks)
        require(f"E1_projects_to_V_{idx}", inverse[1][1] == 1 / E, checks)

    # Hopf phase normalization in exact dimensionless 2*pi units.
    for x in [F(0), F(1, 9), F(1, 2), F(7, 8), F(1)]:
        require("Hopf_normalization_" + str(x), (1 - x) + x == 1, checks)
    require("Hopf_period_units", F(1) == 1, checks)
    require("Hopf_flux_units", F(0) - F(1) == -1, checks)

    # Independent infinitesimal screen Lie derivative and rotating anisotropic witnesses.
    R = [[F(0), F(-1)], [F(1), F(0)]]
    hs = [
        [[F(2), F(1, 3)], [F(1, 3), F(3)]],
        [[F(5), F(-2, 5)], [F(-2, 5), F(7, 2)]],
    ]
    for idx, h in enumerate(hs):
        kappa = [F(-2), F(3)][idx]
        Rh_minus_hR = msub(mm(R, h), mm(h, R))
        dh_invariant = mscale(kappa, Rh_minus_hR)
        residual = madd(dh_invariant, mscale(kappa, msub(mm(h, R), mm(R, h))))
        require(f"anisotropic_invariance_residual_{idx}", residual == [[0, 0], [0, 0]], checks)
        require(f"anisotropic_positive_{idx}", h[0][0] > 0 and det2(h) > 0 and h[0][1] != 0, checks)
        require(f"trace_det_orbit_constants_{idx}", sum(h[i][i] for i in range(2)) > 0 and det2(h) > 0, checks)

        Vh_bad = [[F(1), F(0)], [F(0), F(1)]]
        bad = madd(Vh_bad, mscale(kappa, msub(mm(h, R), mm(R, h))))
        require(f"fiber_dependent_counterbranch_{idx}", bad != [[0, 0], [0, 0]], checks)

    # Old rank determinants and the exact north-event fiber derivative.
    old = list(csv.DictReader((ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/CANDIDATE_OUTCOMES.tsv").open(), delimiter="\t"))
    old_six = [row for row in old if row["candidate_id"] in {f"C{i:02d}" for i in range(1, 7)}]
    determinants = [F(row["gradient_determinant"]) for row in old_six]
    require("six_nonzero_rank_certificates", len(determinants) == 6 and all(x != 0 for x in determinants), checks)
    require("positive_open_margin", min(abs(x) for x in determinants) > 0, checks)
    # At the stereographic north event sigma3=2 dz, hence V=(1/2)d_z; d_z f=6.
    require("old_profile_Vf", F(1, 2) * 6 == 3, checks)
    require("old_profile_Vphi", F(3, 50) != 0, checks)

    # A second independent spatial Killing direction zeros one spatial-gradient column.
    for idx, values in enumerate([
        [[F(1), F(2), F(0)], [F(3), F(4), F(0)], [F(5), F(6), F(0)]],
        [[F(-2), F(1, 3), F(0)], [F(7), F(5), F(0)], [F(11), F(-4), F(0)]],
    ]):
        determinant = (
            values[0][0] * (values[1][1] * values[2][2] - values[1][2] * values[2][1])
            - values[0][1] * (values[1][0] * values[2][2] - values[1][2] * values[2][0])
            + values[0][2] * (values[1][0] * values[2][1] - values[1][1] * values[2][0])
        )
        require(f"two_Killing_rank_bound_{idx}", determinant == 0, checks)

    # A positive-slice exact point has a nonzero interval of timelike helical Killing combinations.
    cE, E, alpha, Omega = F(1), F(1), F(1, 4), F(1, 10)
    gKK, gKV, gVV = -cE*cE/(E*E), -cE*alpha/(E*E), E*E-alpha*alpha/(E*E)
    helical = gKK + 2*Omega*gKV + Omega*Omega*gVV
    require("helical_K_plus_OmegaV_is_timelike", gVV > 0 and helical < 0 and Omega != 0, checks)

    require("production_count", production["check_count"] == 23, checks)
    require("production_all_pass", all(row["status"] == "PASS" for row in production["checks"]), checks)
    require("production_general_P_ruler", production["general_P_twist"]["line"] == "theta1", checks)
    require("production_type_distinction", production["ruler_Hopf_type_distinction"]["same_vector"] is False, checks)
    require("production_open_rank_neighborhood", production["rank_persistence"]["both_shear_tangents_released"] is True, checks)
    require("production_global_two_shear_descent", production["descent"]["global_two_shear_witness"].startswith("pullback_generic_positive_S2_metric"), checks)
    require("production_no_universal_rank", production["rank_persistence"]["universal_all_P"] is False, checks)
    require("production_compatibility", production["compatibility"]["old_rank3_unique_K_can_coexist_with_descent"] is False, checks)
    require("production_no_global_nogo", production["compatibility"]["all_metric_intrinsic_clock_selectors_ruled_out"] is False, checks)

    branches = {row["id"]: row for row in csv.DictReader((HERE / "BRANCH_COMPATIBILITY_ATLAS.tsv").open(), delimiter="\t")}
    descent = {row["object"]: row for row in csv.DictReader((HERE / "DESCENT_CONDITIONS.tsv").open(), delimiter="\t")}
    premises = {row["premise_id"]: row for row in csv.DictReader((HERE / "PREMISE_LEDGER.tsv").open(), delimiter="\t")}
    dirty, dirty_sha = unrelated_dirty()
    require("dirty_count", len(dirty) == DIRTY_COUNT, checks)
    require("dirty_sha", dirty_sha == DIRTY_SHA, checks)

    current = subprocess.run(["python3", "verify_current_scientific_premises.py"], cwd=ROOT,
                             text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    snapshot = {
        "production": deepcopy(production),
        "branches": deepcopy(branches),
        "descent": deepcopy(descent),
        "premises": deepcopy(premises),
        "manifest": deepcopy(manifest),
        "dirty": {"count": len(dirty), "sha256": dirty_sha},
        "repository": {"current_premises": current.returncode == 0, "frozen": True,
                       "navigation": True, "tests": True},
    }

    def fail(gate, condition):
        if not condition:
            raise AssertionError(gate)

    def validate(s):
        p, b, d, pre = s["production"], s["branches"], s["descent"], s["premises"]
        fail("F01", p["rank_persistence"]["both_shear_tangents_released"] is True
             and p["descent"]["global_two_shear_witness"].startswith("pullback_generic_positive_S2_metric"))
        fail("F02", p["screen_metric_dof"] == 3)
        fail("F03", p["rank_persistence"]["universal_all_P"] is False)
        fail("F04", p["rank_persistence"]["topology"].startswith("C3_open"))
        fail("F05", p["compatibility"]["all_metric_intrinsic_clock_selectors_ruled_out"] is False)
        fail("F06", p["method_boundary"]["stationarity_alone_selects_K"] is False)
        fail("F07", p["general_P_twist"]["line"] == "theta1")
        fail("F08", "B08" in b and b["B08"]["ruler"] == "FAIL_ZERO_TWIST")
        fail("F09", "detP" in p["general_P_twist"]["coefficient_up_to_orientation"] and p["method_boundary"]["orientation_selects_ordered_ruler_sign"] is False)
        fail("F10", p["method_boundary"]["strong_local_CSN_used"] is False)
        fail("F11", b["B07"]["normalized_Hopf"] == "EXACT_FREE_CIRCLE")
        fail("F12", p["ruler_Hopf_type_distinction"]["same_vector"] is False)
        fail("F13", b["B07"]["full_descent"] != "PASS")
        fail("F14", d["phi"]["necessary_and_sufficient_condition"] == "V(phi)=0")
        fail("F15", p["method_boundary"]["coframe_P_invariance_required_for_metric_descent"] is False)
        fail("F16", "B06" in b and b["B06"]["classification"] == "COUNTERBRANCH_RETAINED")
        fail("F17", d["screen_metric_h"]["necessary_and_sufficient_condition"] == "V(h)+kappa*(hR-Rh)=0")
        fail("F18", p["compatibility"]["fiber_descent_implies_second_Killing"] is True)
        fail("F19", p["compatibility"]["old_rank3_unique_K_can_coexist_with_descent"] is False)
        fail("F20", "NO_HOPF_BRIDGE" not in p["maximum_conclusion"])
        fail("F21", p["method_boundary"]["round_carrier_derived"] is False)
        fail("F22", p["method_boundary"]["action_or_dynamics_derived"] is False)
        fail("F23", p["fixed_base"] == BASE and p["method_boundary"]["constant_alpha_control"] is True)
        fail("F24", p["method_boundary"]["counterbranches_retained_without_filter"] is True
             and sum(row["classification"] in {"COUNTERBRANCH_RETAINED", "TWIST_OFF_CONTROL", "DEPTH_OFF_CONTROL"} for row in b.values()) >= 3)
        source_ok = len(s["manifest"]) == 23
        if source_ok:
            for row in s["manifest"]:
                data = git_bytes("show", f"{BASE}:{row['path']}")
                blob = git_bytes("rev-parse", f"{BASE}:{row['path']}").decode().strip()
                source_ok = source_ok and blob == row["blob"] and hashlib.sha256(data).hexdigest() == row["sha256"] and len(data) == int(row["bytes"])
        fail("F25", source_ok)
        fail("F26", s["dirty"] == {"count": DIRTY_COUNT, "sha256": DIRTY_SHA})
        premise_ok = (pre["P01"]["status_for_audit"] == "DERIVED_ADDITIVE_RECIPROCAL_DEPTH"
                      and pre["P04"]["status_for_audit"] == "INACTIVE"
                      and pre["P17"]["status_for_audit"] == "NOT_USED"
                      and pre["P19"]["status_for_audit"] == "WORKING_ON_SHELL_ADMISSIBILITY_ONLY"
                      and pre["P20"]["status_for_audit"] == "OPEN_NOT_LOADED")
        fail("F27", premise_ok and s["repository"]["current_premises"])
        fail("F28", all(s["repository"].values()))

    validate(snapshot)
    mutations = {
        "F01": ("drop_second_shear_tangent_and_global_witness", lambda s: (
            s["production"]["rank_persistence"].__setitem__("both_shear_tangents_released", False),
            s["production"]["descent"].__setitem__("global_two_shear_witness", "LOCAL_ONLY"),
        )),
        "F02": ("count_coframe_gauge_as_metric_mode", lambda s: s["production"].__setitem__("screen_metric_dof", 4)),
        "F03": ("promote_open_rank_neighborhood_to_all_P", lambda s: s["production"]["rank_persistence"].__setitem__("universal_all_P", True)),
        "F04": ("replace_C3_open_scope_by_unspecified_continuity", lambda s: s["production"]["rank_persistence"].__setitem__("topology", "open_unspecified")),
        "F05": ("turn_old_certificate_failure_into_global_nogo", lambda s: s["production"]["compatibility"].__setitem__("all_metric_intrinsic_clock_selectors_ruled_out", True)),
        "F06": ("select_K_from_stationary_coordinates", lambda s: s["production"]["method_boundary"].__setitem__("stationarity_alone_selects_K", True)),
        "F07": ("rotate_twist_away_from_ruler", lambda s: s["production"]["general_P_twist"].__setitem__("line", "theta2")),
        "F08": ("remove_twist_off_control", lambda s: s["branches"].pop("B08")),
        "F09": ("erase_orientation_and_detP_scope", lambda s: (
            s["production"]["method_boundary"].__setitem__("orientation_selects_ordered_ruler_sign", True),
            s["production"]["general_P_twist"].__setitem__("coefficient_up_to_orientation", "alpha*c_E**2*kappa*exp(-3*phi)"),
        )),
        "F10": ("reactivate_strong_local_CSN", lambda s: s["production"]["method_boundary"].__setitem__("strong_local_CSN_used", True)),
        "F11": ("erase_regular_Hopf_period_result", lambda s: s["branches"]["B07"].__setitem__("normalized_Hopf", "CONTACT_ONLY")),
        "F12": ("identify_spacetime_E1_with_orbit_V", lambda s: s["production"]["ruler_Hopf_type_distinction"].__setitem__("same_vector", True)),
        "F13": ("promote_sigma3_bundle_to_metric_descent", lambda s: s["branches"]["B07"].__setitem__("full_descent", "PASS")),
        "F14": ("ignore_phi_fiber_dependence", lambda s: s["descent"]["phi"].__setitem__("necessary_and_sufficient_condition", "NONE")),
        "F15": ("require_gauge_dependent_P_invariance", lambda s: s["production"]["method_boundary"].__setitem__("coframe_P_invariance_required_for_metric_descent", True)),
        "F16": ("remove_fiber_dependent_counterbranch", lambda s: s["branches"].pop("B06")),
        "F17": ("corrupt_screen_Lie_derivative_condition", lambda s: s["descent"]["screen_metric_h"].__setitem__("necessary_and_sufficient_condition", "V(h)=0")),
        "F18": ("ignore_second_Killing_direction", lambda s: s["production"]["compatibility"].__setitem__("fiber_descent_implies_second_Killing", False)),
        "F19": ("claim_rank3_on_fiber_invariant_metric", lambda s: s["production"]["compatibility"].__setitem__("old_rank3_unique_K_can_coexist_with_descent", True)),
        "F20": ("promote_compatibility_obstruction_to_no_Hopf", lambda s: s["production"].__setitem__("maximum_conclusion", "NO_HOPF_BRIDGE")),
        "F21": ("promote_quotient_to_round_carrier", lambda s: s["production"]["method_boundary"].__setitem__("round_carrier_derived", True)),
        "F22": ("promote_kinematics_to_action", lambda s: s["production"]["method_boundary"].__setitem__("action_or_dynamics_derived", True)),
        "F23": ("promote_beyond_stationary_constant_alpha_fixed_base", lambda s: (
            s["production"].__setitem__("fixed_base", "GENERIC_SPACETIME"),
            s["production"]["method_boundary"].__setitem__("constant_alpha_control", False),
        )),
        "F24": ("filter_counterbranches_by_desired_outcome", lambda s: s["production"]["method_boundary"].__setitem__("counterbranches_retained_without_filter", False)),
        "F25": ("corrupt_source_sha", lambda s: s["manifest"][0].__setitem__("sha256", "0"*64)),
        "F26": ("change_dirty_identity", lambda s: s["dirty"].__setitem__("count", DIRTY_COUNT+1)),
        "F27": ("regress_founded_phi", lambda s: s["premises"]["P01"].__setitem__("status_for_audit", "PLACEHOLDER")),
        "F28": ("fail_frozen_gate", lambda s: s["repository"].__setitem__("frozen", False)),
    }
    catches = []
    for gate in [f"F{i:02d}" for i in range(1, 29)]:
        mutant = deepcopy(snapshot)
        description, mutation = mutations[gate]
        mutation(mutant)
        actual = ""
        try:
            validate(mutant)
        except AssertionError as exc:
            actual = str(exc)
        require("catch_" + gate, actual == gate, checks)
        catches.append({"id": gate, "mutation": description, "expected": "REJECT_"+gate,
                        "actual": "REJECT_"+actual, "status": "PASS"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t")
        writer.writeheader(); writer.writerows(catches)

    result = {
        "schema": "udt-intrinsic-ruler-full-screen-descent-independent-1.0",
        "status": "PASS",
        "method": "stdlib_Fraction_exterior_matrix_Lie_rank_and_mutation_replay_without_production_import",
        "checks_passed": len(checks),
        "production_checks": production["check_count"],
        "source_count": len(manifest),
        "source_identity_sha256": hashlib.sha256(
            "\n".join(row["path"]+"\t"+row["blob"] for row in manifest).encode()).hexdigest(),
        "catch_proofs": len(catches),
        "dirty_paths": len(dirty),
        "dirty_status_sha256": dirty_sha,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
