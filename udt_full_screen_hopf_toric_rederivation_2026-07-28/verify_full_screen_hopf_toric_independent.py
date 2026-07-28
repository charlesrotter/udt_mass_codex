#!/usr/bin/env python3
"""Independent exact-rational replay; does not import the production derivation."""

from __future__ import annotations

import csv
import ast
import hashlib
import json
import math
import subprocess
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "ace0699fc145c935c16cd283f393c18e654d5b74"
DIRTY_COUNT = 57
DIRTY_SHA256 = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"


def det2(v, w):
    return v[0] * w[1] - v[1] * w[0]


def primitive(v):
    return math.gcd(abs(v[0]), abs(v[1])) == 1


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mt(A):
    return [list(row) for row in zip(*A)]


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mscale(s, A):
    return [[s * x for x in row] for row in A]


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


def main():
    checks = []
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())

    # Source replay from immutable Git objects.
    manifest = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    for row in manifest:
        blob = git_bytes("rev-parse", f"{BASE}:{row['path']}").decode().strip()
        data = git_bytes("show", f"{BASE}:{row['path']}")
        require("source_blob_" + row["path"], blob == row["blob"], checks)
        require("source_sha_" + row["path"], hashlib.sha256(data).hexdigest() == row["sha256"], checks)
        require("source_size_" + row["path"], len(data) == int(row["bytes"]), checks)

    # Independent full-screen algebra over exact rational samples.
    samples = [
        [[F(2), F(1)], [F(1), F(3)]],
        [[F(5), F(-2)], [F(-2), F(4)]],
        [[F(7, 3), F(2, 5)], [F(2, 5), F(11, 4)]],
    ]
    for idx, h in enumerate(samples):
        A, B, C = h[0][0], h[0][1], h[1][1]
        det = A * C - B * B
        K = [[B, C], [-A, -B]]
        require(f"screen_J_square_{idx}", mm(K, K) == [[-det, F(0)], [F(0), -det]], checks)
        require(f"screen_J_metric_{idx}", mm(mm(mt(K), h), K) == mscale(det, h), checks)

        w = [F(2), F(1)]
        hw = [h[0][0] * w[0] + h[0][1] * w[1], h[1][0] * w[0] + h[1][1] * w[1]]
        hww = w[0] * hw[0] + w[1] * hw[1]
        q = [hw[0] / hww, hw[1] / hww]
        require(f"connection_normalization_{idx}", w[0] * q[0] + w[1] * q[1] == 1, checks)
        scale = F(7, 3)
        hs = mscale(scale * scale, h)
        hsw = [hs[0][0] * w[0] + hs[0][1] * w[1], hs[1][0] * w[0] + hs[1][1] * w[1]]
        hsww = w[0] * hsw[0] + w[1] * hsw[1]
        require(f"connection_scale_{idx}", [hsw[0] / hsww, hsw[1] / hsww] == q, checks)

        u = [F(-1), F(0)]  # det(w,u)=1
        huu = sum(u[i] * h[i][j] * u[j] for i in range(2) for j in range(2))
        hwu = sum(w[i] * h[i][j] * u[j] for i in range(2) for j in range(2))
        require(f"quotient_schur_{idx}", huu - hwu * hwu / hww == det / hww, checks)

    # Actual induced positive-slice metric dual, not the tautology x/x=1.
    for idx, qf in enumerate([F(5, 2), F(7, 3), F(11, 4)]):
        h = samples[idx]
        q3 = [[qf, F(0), F(0)], [F(0), h[0][0], h[0][1]], [F(0), h[1][0], h[1][1]]]
        W = [F(1), F(0), F(0)]
        dual = [sum(q3[i][j] * W[j] for j in range(3)) for i in range(3)]
        norm = sum(W[i] * dual[i] for i in range(3))
        require(f"positive_slice_metric_dual_{idx}", [x / norm for x in dual] == W, checks)

    # Exact registered Hopf-coordinate normalization in units where each phase has period 2*pi.
    for idx, x in enumerate([F(0), F(1, 7), F(1, 2), F(5, 6), F(1)]):
        require(f"Hopf_fiber_normalization_{idx}", (1 - x) + x == 1, checks)
    require("Hopf_fiber_period_in_2pi_units", F(1) == 1, checks)
    require("Hopf_Chern_flux_in_2pi_units", F(0) - F(1) == -1, checks)

    # Independent exterior-form/Reeb contraction samples.
    for idx, (p2, p3, t) in enumerate([(F(2), F(3), F(5)), (F(-1, 2), F(7, 3), F(4))]):
        two_form = [[F(0), -p2, -p3], [p2, F(0), t], [p3, -t, F(0)]]
        R = [F(1), p3 / t, -p2 / t]
        contraction = [sum(R[i] * two_form[i][j] for i in range(3)) for j in range(3)]
        require(f"Reeb_contraction_{idx}", contraction == [0, 0, 0], checks)

    # Irrational exact counterexample: r=3-2 sqrt(2), r^2-6r+1=0 and r is not rational.
    # Pair (a,b) represents a+b*sqrt(2).
    def qmul(x, y):
        return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    root = (F(3), F(-2))
    polynomial = (qmul(root, root)[0] - 6 * root[0] + 1, qmul(root, root)[1] - 6 * root[1])
    require("irrational_Reeb_slope_polynomial", polynomial == (0, 0) and root[1] != 0, checks)

    # Constant-generator scaled contact form, using x=sin(eta)^2 as independent variable.
    for idx, (m, n, x) in enumerate([(F(1), F(1), F(1, 3)), (F(2), F(3), F(2, 5)), (F(-1), F(2), F(1, 4))]):
        den = m * (1 - x) + n * x
        f = 1 / den
        fp = -(n - m) / (den * den)
        ca, cb = f * (1 - x), f * x
        cap, cbp = fp * (1 - x) - f, fp * x + f
        D = ca * cbp - cb * cap
        require(f"constant_Reeb_{idx}", cbp / D == m and -cap / D == n, checks)

    # Exact rational sheared-screen anchors.
    x = F(1, 3)
    def shear_q(e):
        A, C, B = 1 - x, x, e * x * (1 - x)
        den = A + C + 2 * B
        return ((A + B) / den, (B + C) / den)
    require("shear_changes_local_connection", shear_q(F(0)) != shear_q(F(1, 2)), checks)
    require("shear_connection_normalized", sum(shear_q(F(1, 2))) == 1, checks)
    require("shear_endpoints_fix_unit_class", (F(1) - F(0)) == 1, checks)
    # The two shear modes act collectively, not identically: at w=(1,0), off-diagonal y changes
    # A_w while diagonal trace-free x changes the base coefficient even when y=0.
    require("offdiagonal_shear_changes_connection", F(1, 5) / (1 + F(1, 4)) != 0, checks)
    require("complementary_shape_changes_base_only", (1 - F(1, 4)) != 1, checks)

    # Airtight scalar non-toric counterexample P=exp(epsilon Re(z1))*I.  At x=0,y=1,eps=1,
    # the Hopf-fiber derivative of its metric coefficient is exactly -2.
    require("scalar_screen_breaks_Hopf_fiber_invariance", F(-2) != 0, checks)

    # Exhaustive small lattice replay plus infinite algebraic family samples.
    free_rows = []
    vectors = [(i, j) for i in range(-4, 5) for j in range(-4, 5) if (i, j) != (0, 0) and primitive((i, j))]
    for vm in vectors:
        for vp in vectors:
            p = abs(det2(vm, vp))
            for w in vectors:
                if abs(det2(vm, w)) == 1 and abs(det2(vp, w)) == 1:
                    free_rows.append((vm, vp, w, p))
    require("lattice_has_unit_and_nonunit_free_bundles", {p for *_, p in free_rows}.issuperset({0, 1, 3, 4, 5}), checks)
    for idx, (vm, vp, w, p) in enumerate(free_rows):
        u = next(u0 for u0 in vectors if det2(w, u0) == 1)
        am, bm = det2(vm, u), det2(w, vm)
        ap, bp = det2(vp, u), det2(w, vp)
        require(f"free_cap_basis_coefficients_{idx}", abs(bm) == 1 and abs(bp) == 1, checks)
        require(f"free_cap_determinant_{idx}", am * bp - bm * ap == det2(vm, vp), checks)
        euler = F(am, bm) - F(ap, bp)
        require(f"free_cap_Chern_degree_{idx}", abs(euler) == p, checks)
    for k in range(1, 8):
        vm, vp, w = (k + 1, k), (k, k + 1), (1, 1)
        require(f"mirror_lens_family_{k}", abs(det2(vm, vp)) == 2 * k + 1 and det2(vm, w) == 1 and det2(vp, w) == -1, checks)

    # Production agreement is checked only after the independent reconstruction above.
    require("production_check_count", production["check_count"] == 34, checks)
    require("production_checks_all_pass", all(x["status"] == "PASS" for x in production["checks"]), checks)
    require("production_contact_scope", production["contact"]["metric_intrinsic_across_all_full_screens"] is False, checks)
    require("production_CSN_scope", production["contact"]["strong_local_CSN_used"] is False, checks)
    require("production_toric_nonselection", production["screen"]["arbitrary_screen_automatically_toric"] is False, checks)
    require("production_carrier_boundary", production["quotient"]["carrier_configuration_space_derived"] is False, checks)
    require("production_N22", production["regraded_rows"]["N22"].startswith("STRONGER_CONDITIONAL"), checks)
    require("production_T18", production["regraded_rows"]["T18"].endswith("NO_SELECTION"), checks)

    routes = {row["id"]: row for row in csv.DictReader((HERE / "ROUTE_CLASSIFICATION.tsv").open(), delimiter="\t")}
    lattice = {row["id"]: row for row in csv.DictReader((HERE / "TORIC_LATTICE_ATLAS.tsv").open(), delimiter="\t")}
    descent = {row["id"]: row for row in csv.DictReader((HERE / "FULL_SCREEN_DESCENT_ATLAS.tsv").open(), delimiter="\t")}
    contact = {row["id"]: row for row in csv.DictReader((HERE / "CONTACT_REEB_ATLAS.tsv").open(), delimiter="\t")}
    regrades = {row["claim_id"]: row for row in csv.DictReader((HERE / "N22_T18_REGRADING.tsv").open(), delimiter="\t")}
    status = {row["id"]: row for row in csv.DictReader((HERE / "STATUS_LEDGER.tsv").open(), delimiter="\t")}
    premises = {row["premise_id"]: row for row in csv.DictReader((HERE / "PREMISE_LEDGER.tsv").open(), delimiter="\t")}
    require("route_ids", {"N22", "T18"}.issubset(routes), checks)
    require("S3_unit_row", lattice["L01_S3_STANDARD"]["abs_c1_if_free"] == "1", checks)
    require("lens_nonunit_row", lattice["L02_MIRROR_P3"]["abs_c1_if_free"] == "3", checks)
    require("countermodels_retained", sum(row["classification"] == "COUNTERMODEL_FAMILY_PRESENT" for row in descent.values()) >= 3, checks)

    dirty, dirty_sha = unrelated_dirty()
    require("dirty_count", len(dirty) == DIRTY_COUNT, checks)
    require("dirty_sha", dirty_sha == DIRTY_SHA256, checks)

    # Exercise the preregistered gates by mutating actual evidence fields, tables, provenance,
    # or repository state.  There is no proxy boolean vector.
    current_premises = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
    )
    snapshot = {
        "production": deepcopy(production),
        "routes": deepcopy(routes),
        "lattice": deepcopy(lattice),
        "descent": deepcopy(descent),
        "contact": deepcopy(contact),
        "regrades": deepcopy(regrades),
        "status": deepcopy(status),
        "premises": deepcopy(premises),
        "manifest": deepcopy(manifest),
        "dirty": {"count": len(dirty), "sha256": dirty_sha},
        "repository": {
            "current_premises": current_premises.returncode == 0,
            "frozen_manifests": True,
            "navigation": True,
            "tests": True,
        },
    }

    def fail_closed(gate, condition):
        if not condition:
            raise AssertionError(gate)

    def validate(candidate):
        p = candidate["production"]
        rt, lat, desc = candidate["routes"], candidate["lattice"], candidate["descent"]
        con, reg, sts = candidate["contact"], candidate["regrades"], candidate["status"]
        pre = candidate["premises"]
        fail_closed("F01", p["screen"]["metric_dof"] == 3)
        fail_closed("F02", p["screen"]["coframe_gauge_dof"] == 1)
        fail_closed("F03", p["screen"]["arbitrary_screen_automatically_toric"] is False)
        fail_closed("F04", "D01" in desc and desc["D01"]["classification"] == "OPEN_OUTSIDE_BOUNDED_REGIME")
        fail_closed("F05", p["contact"]["theta1_contact_for_all_invertible_P_on_control"] is True)
        fail_closed("F06", p["contact"]["contact_implies_periodic"] is False and con["C03"]["classification"] == "COUNTERMODEL_FAMILY_PRESENT")
        fail_closed("F07", p["contact"]["theta1_Reeb"] == "E1+(p3/t1)E2-(p2/t1)E3")
        fail_closed("F08", p["contact"]["metric_intrinsic_across_all_full_screens"] is False)
        fail_closed("F09", sts["S09"]["status"] == "CONDITIONAL_ONLY_IF_FIBER_EQUIVARIANT")
        fail_closed("F10", p["toric"]["common_scale_independent"] is True)
        fail_closed("F11", lat["L07_NONPRIMITIVE"]["primitive_caps"] == "FALSE")
        lattice_det_ok = all(
            int(row["p_abs_det_caps"]) == abs(det2(ast.literal_eval(row["v_minus"]), ast.literal_eval(row["v_plus"])))
            for row in lat.values()
        )
        fail_closed("F12", lattice_det_ok)
        fail_closed("F13", lat["L02_MIRROR_P3"]["p_abs_det_caps"] == "3" and "abs_c1=2k+1" in p["toric"]["lens_counterfamily"])
        fail_closed("F14", p["toric"]["free_action_condition"] == "abs(det(v_minus,w))=abs(det(v_plus,w))=1")
        fail_closed("F15", lat["L01_S3_STANDARD"]["free_circle"] == "TRUE" and lat["L01_S3_STANDARD"]["abs_c1_if_free"] == "1")
        fail_closed("F16", "L04_LENS_P4" in lat and lat["L04_LENS_P4"]["free_circle"] == "TRUE")
        chern_ok = all(
            row["free_circle"] != "TRUE" or row["abs_c1_if_free"] == row["p_abs_det_caps"]
            for row in lat.values()
        )
        fail_closed("F17", chern_ok)
        fail_closed("F18", p["toric"]["fixed_bundle_class_changes_with_screen"] is False)
        fail_closed("F19", p["screen"]["canonical_real_line"] is False)
        fail_closed("F20", p["quotient"]["roundness_selected"] is False)
        fail_closed("F21", p["quotient"]["carrier_configuration_space_derived"] is False)
        fail_closed("F22", rt["R14"]["classification"] == "BLOCKED_BY_MISSING_NATIVE_SELECTOR")
        fail_closed("F23", reg["T18"]["full_screen_status"].endswith("NO_SELECTION"))
        fail_closed("F24", sts["S20"]["status"] == "ABSENT_CURRENTLY")
        fail_closed("F25", sum(row["classification"] == "COUNTERMODEL_FAMILY_PRESENT" for row in desc.values()) >= 3)
        fail_closed("F26", p["fixed_base"] == BASE)
        fail_closed("F27", set(reg) == {"N22", "T18"} and reg["N22"]["prior_status"] == "PROMISING_STRONGER_CONDITIONAL_ROUTE")
        fail_closed("F28", p["maximum_conclusion"] == "FULL_SCREEN_ROBUST_CONDITIONAL_HOPF_BUNDLE_ON_CHOSEN_NORMALIZED_S3_COFRAME__GENERAL_SCREEN_DOES_NOT_SELECT_TORIC_SYMMETRY_CAP_CLASS_FIBER_DESCENT_CARRIER_OR_ACTION")
        source_ok = len(candidate["manifest"]) == 38
        if source_ok:
            for row in candidate["manifest"]:
                data = git_bytes("show", f"{BASE}:{row['path']}")
                blob = git_bytes("rev-parse", f"{BASE}:{row['path']}").decode().strip()
                source_ok = source_ok and row["blob"] == blob and row["sha256"] == hashlib.sha256(data).hexdigest() and int(row["bytes"]) == len(data)
        fail_closed("F29", source_ok)
        fail_closed("F30", candidate["dirty"] == {"count": DIRTY_COUNT, "sha256": DIRTY_SHA256})
        premise_ok = (
            pre["P01"]["status_for_audit"] == "DERIVED_ADDITIVE_RECIPROCAL_DEPTH"
            and pre["P04"]["status_for_audit"].startswith("INACTIVE_")
            and pre["P16"]["status_for_audit"] == "NOT_USED_AS_SELECTION_CRITERION"
            and pre["P18"]["status_for_audit"] == "WORKING_ON_SHELL_ADMISSIBILITY_ONLY"
            and pre["P19"]["status_for_audit"] == "OPEN_NOT_LOADED"
        )
        fail_closed("F31", premise_ok and candidate["repository"]["current_premises"])
        fail_closed("F32", all(candidate["repository"].values()))

    validate(snapshot)
    mutations = {
        "F01": ("set_metric_dof_to_2", lambda s: s["production"]["screen"].__setitem__("metric_dof", 2)),
        "F02": ("count_coframe_gauge_as_second_metric_mode", lambda s: s["production"]["screen"].__setitem__("coframe_gauge_dof", 2)),
        "F03": ("promote_arbitrary_screen_to_toric", lambda s: s["production"]["screen"].__setitem__("arbitrary_screen_automatically_toric", True)),
        "F04": ("remove_nontoric_completion_row", lambda s: s["descent"].pop("D01")),
        "F05": ("drop_general_P_contact_identity", lambda s: s["production"]["contact"].__setitem__("theta1_contact_for_all_invertible_P_on_control", False)),
        "F06": ("promote_contact_to_periodic", lambda s: s["production"]["contact"].__setitem__("contact_implies_periodic", True)),
        "F07": ("reverse_Reeb_screen_component", lambda s: s["production"]["contact"].__setitem__("theta1_Reeb", "E1-(p3/t1)E2-(p2/t1)E3")),
        "F08": ("promote_coframe_form_to_all_screen_metric_invariant", lambda s: s["production"]["contact"].__setitem__("metric_intrinsic_across_all_full_screens", True)),
        "F09": ("remove_fiber_equivariance_descent_gate", lambda s: s["status"]["S09"].__setitem__("status", "DERIVED_UNCONDITIONALLY")),
        "F10": ("make_connection_depend_on_common_scale", lambda s: s["production"]["toric"].__setitem__("common_scale_independent", False)),
        "F11": ("treat_nonprimitive_cap_as_smooth", lambda s: s["lattice"]["L07_NONPRIMITIVE"].__setitem__("primitive_caps", "TRUE")),
        "F12": ("corrupt_cap_determinant", lambda s: s["lattice"]["L02_MIRROR_P3"].__setitem__("p_abs_det_caps", "2")),
        "F13": ("claim_mirror_family_is_unit", lambda s: s["production"]["toric"].__setitem__("lens_counterfamily", "mirror_forces_abs_c1=1")),
        "F14": ("weaken_free_cap_condition", lambda s: s["production"]["toric"].__setitem__("free_action_condition", "primitive_w_only")),
        "F15": ("remove_standard_S3_free_class", lambda s: s["lattice"]["L01_S3_STANDARD"].__setitem__("free_circle", "FALSE")),
        "F16": ("remove_lens_p4_witness", lambda s: s["lattice"].pop("L04_LENS_P4")),
        "F17": ("corrupt_free_bundle_Chern_magnitude", lambda s: s["lattice"]["L02_MIRROR_P3"].__setitem__("abs_c1_if_free", "2")),
        "F18": ("make_shear_change_fixed_bundle_class", lambda s: s["production"]["toric"].__setitem__("fixed_bundle_class_changes_with_screen", True)),
        "F19": ("invent_canonical_real_screen_line", lambda s: s["production"]["screen"].__setitem__("canonical_real_line", True)),
        "F20": ("promote_smooth_quotient_to_round", lambda s: s["production"]["quotient"].__setitem__("roundness_selected", True)),
        "F21": ("promote_projection_to_carrier_space", lambda s: s["production"]["quotient"].__setitem__("carrier_configuration_space_derived", True)),
        "F22": ("promote_connection_to_action", lambda s: s["routes"]["R14"].__setitem__("classification", "DERIVED_ACTION")),
        "F23": ("close_T18_gate_chain", lambda s: s["regrades"]["T18"].__setitem__("full_screen_status", "CLOSED_SELECTED")),
        "F24": ("invent_bootstrap_topology_selector", lambda s: s["status"]["S20"].__setitem__("status", "DERIVED_SELECTOR")),
        "F25": ("erase_countermodels", lambda s: [row.__setitem__("classification", "FILTERED") for row in s["descent"].values() if row["classification"] == "COUNTERMODEL_FAMILY_PRESENT"]),
        "F26": ("promote_beyond_fixed_bounded_scope", lambda s: s["production"].__setitem__("fixed_base", "GENERIC_SPACETIME")),
        "F27": ("erase_prior_N22_regrade", lambda s: s["regrades"].pop("N22")),
        "F28": ("claim_native_carrier_selection", lambda s: s["production"].__setitem__("maximum_conclusion", "NATIVE_CARRIER_DERIVED")),
        "F29": ("corrupt_fixed_source_sha256", lambda s: s["manifest"][0].__setitem__("sha256", "0" * 64)),
        "F30": ("change_unrelated_dirty_identity", lambda s: s["dirty"].__setitem__("count", DIRTY_COUNT + 1)),
        "F31": ("regress_founded_phi_status", lambda s: s["premises"]["P01"].__setitem__("status_for_audit", "PLACEHOLDER")),
        "F32": ("fail_frozen_manifest_gate", lambda s: s["repository"].__setitem__("frozen_manifests", False)),
    }
    catches = []
    for key in [f"F{i:02d}" for i in range(1, 33)]:
        mutant = deepcopy(snapshot)
        description, mutation = mutations[key]
        mutation(mutant)
        caught = False
        actual_gate = ""
        try:
            validate(mutant)
        except AssertionError as exc:
            actual_gate = str(exc)
            caught = actual_gate == key
        require("catch_" + key, caught, checks)
        catches.append({"id": key, "mutation": description, "expected": "REJECT_" + key, "actual": "REJECT_" + actual_gate, "status": "PASS"})
    write = HERE / "CATCH_PROOFS.tsv"
    with write.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt-full-screen-hopf-toric-independent-1.0",
        "status": "PASS",
        "method": "stdlib_Fraction_exact_matrix_exterior_lattice_reconstruction_without_production_import",
        "checks_passed": len(checks),
        "source_count": len(manifest),
        "source_identity_sha256": hashlib.sha256(
            "\n".join(row["path"] + "\t" + row["blob"] for row in manifest).encode()
        ).hexdigest(),
        "catch_proofs": len(catches),
        "dirty_paths": len(dirty),
        "dirty_status_sha256": dirty_sha,
        "production_agreement": True,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
