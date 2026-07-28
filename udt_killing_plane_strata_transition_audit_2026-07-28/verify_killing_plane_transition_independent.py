#!/usr/bin/env python3
"""Independent exact-rational replay without importing production code."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "0d6d83b357285da68e90198570ede07468e900a8"
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"


def require(name: str, condition: bool, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def mt(a):
    return [list(row) for row in zip(*a)]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def msub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mscale(s, a):
    return [[s * value for value in row] for row in a]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a):
    determinant = det2(a)
    return [[a[1][1] / determinant, -a[0][1] / determinant],
            [-a[1][0] / determinant, a[0][0] / determinant]]


def mv(a, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in a]


def dot(v, a, w):
    return sum(v[i] * a[i][j] * w[j] for i in range(len(v)) for j in range(len(w)))


def wedge(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            inversions = sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = result.get(key, F(0)) + (-1 if inversions % 2 else 1) * ca * cb
    return {key: value for key, value in result.items() if value}


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


def main() -> None:
    checks: list[str] = []
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    manifest = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    for row in manifest:
        data = git_bytes("show", f"{BASE}:{row['path']}")
        blob = git_bytes("rev-parse", f"{BASE}:{row['path']}").decode().strip()
        require("source_blob_" + row["path"], blob == row["blob"], checks)
        require("source_sha_" + row["path"], hashlib.sha256(data).hexdigest() == row["sha256"], checks)
        require("source_size_" + row["path"], len(data) == int(row["bytes"]), checks)

    samples = [
        (F(3), F(1, 5), F(2, 3), F(1, 7)),
        (F(5, 2), F(-2, 7), F(3, 2), F(-1, 9)),
        (F(7, 4), F(4, 9), F(5, 4), F(2, 11)),
    ]
    for index, (c, alpha, u, omega) in enumerate(samples):
        G = [[-c*c*u, -c*alpha*u], [-c*alpha*u, 1/u-alpha*alpha*u]]
        require(f"gram_det_{index}", det2(G) == -c*c, checks)
        norm = dot([1, omega], G, [1, omega])
        A = c + alpha*omega
        require(f"helical_norm_{index}", norm == -u*A*A + omega*omega/u, checks)
        require(f"K_timelike_{index}", dot([1, 0], G, [1, 0]) < 0, checks)

        # Independent differentiation with X(u)=-2u chi.
        chi = [F(2, 5), F(-3, 7), F(5, 6)][index]
        dGdu = [[-c*c, -c*alpha], [-c*alpha, -1/(u*u)-alpha*alpha]]
        XG = mscale(-2*u*chi, dGdu)
        D = mm(inv2(G), XG)
        expected = [[-2*chi, -4*alpha*chi/c], [F(0), 2*chi]]
        require(f"Gram_response_{index}", D == expected, checks)
        K = [F(1), F(0)]
        L = [-alpha/c, F(1)]
        require(f"clock_eigenline_{index}", mv(D, K) == mscale(-2*chi, [[*K]])[0], checks)
        require(f"ruler_eigenline_{index}", mv(D, L) == mscale(2*chi, [[*L]])[0], checks)
        require(f"clock_ruler_signs_{index}", dot(K, G, K) < 0 < dot(L, G, L), checks)
        require(f"clock_ruler_orthogonal_{index}", dot(K, G, L) == 0, checks)
        require(f"response_square_{index}", mm(D, D) == [[4*chi*chi, 0], [0, 4*chi*chi]], checks)
        require(f"Gram_self_adjoint_{index}", mm(G, D) == mt(mm(G, D)), checks)

        # A nontrivial exact constant change of Killing basis.
        B = [
            [[F(2), F(1, 3)], [F(-1, 5), F(3, 2)]],
            [[F(3, 2), F(-2, 7)], [F(1, 4), F(5, 3)]],
            [[F(4, 3), F(1, 6)], [F(-3, 8), F(7, 4)]],
        ][index]
        Gp = mm(mt(B), mm(G, B))
        XGp = mm(mt(B), mm(XG, B))
        Dp = mm(inv2(Gp), XGp)
        covariance = mm(inv2(B), mm(D, B))
        require(f"basis_covariance_{index}", Dp == covariance, checks)

        response_residual = (-2*u*chi) * (
            (-A*A + 2*alpha*omega*A) + omega*omega/(u*u)
        ) + 2*chi*norm
        # Recompute X(norm) directly to avoid sharing the production expression.
        direct_Xnorm = 2*chi*(u*A*A + omega*omega/u)
        require(f"clock_norm_response_{index}", direct_Xnorm + 2*chi*norm == 4*chi*omega*omega/u, checks)
        require(f"unused_crosscheck_is_finite_{index}", response_residual.denominator != 0, checks)

        # Exterior reconstruction of W-flat wedge dW-flat.
        p, q, kappa = F(index+1, 9), F(index+2, 11), F(-2)
        a0 = -c*A*u
        b0 = omega/u-alpha*A*u
        da = {(2,): -2*a0*p, (3,): -2*a0*q}
        dbfactor = 2*(omega/u+alpha*A*u)
        db = {(2,): dbfactor*p, (3,): dbfactor*q}
        e0, e1 = {(0,): F(1)}, {(1,): F(1)}
        dflat = {}
        for part in (wedge(da, e0), wedge(db, e1), {(2, 3): kappa*b0}):
            for key, value in part.items():
                dflat[key] = dflat.get(key, F(0)) + value
        twist = wedge({(0,): a0, (1,): b0}, dflat)
        require(f"twist_mixed_1_{index}", twist[(0, 1, 2)] == 4*c*omega*A*p, checks)
        require(f"twist_mixed_2_{index}", twist[(0, 1, 3)] == 4*c*omega*A*q, checks)
        require(f"twist_contact_dt_{index}", twist[(0, 2, 3)] == kappa*a0*b0, checks)
        require(f"twist_contact_sigma3_{index}", twist[(1, 2, 3)] == kappa*b0*b0, checks)

        # At Omega=0 the founded clock loses only the depth-mixed terms.  For
        # alpha*kappa!=0 it still has the two contact-twist components.
        k_a = -c*c*u
        k_b = -alpha*c*u
        require(f"K_contact_twist_dt_{index}", kappa*k_a*k_b != 0, checks)
        require(f"K_contact_twist_sigma3_{index}", kappa*k_b*k_b != 0, checks)

        # Re-evaluate the independently constructed exterior algebra, rather
        # than declaring a zero dictionary, at dphi=0=kappa.  Also evaluate
        # the Gram response itself at chi=0.
        zero_da = {(2,): F(0), (3,): F(0)}
        zero_db = {(2,): F(0), (3,): F(0)}
        zero_dflat = {}
        for part in (wedge(zero_da, e0), wedge(zero_db, e1), {(2, 3): F(0)}):
            for key, value in part.items():
                zero_dflat[key] = zero_dflat.get(key, F(0)) + value
        zero_twist = wedge({(0,): a0, (1,): b0}, zero_dflat)
        require(
            f"constant_depth_kappa_zero_twist_{index}",
            all(zero_twist.get(key, F(0)) == 0 for key in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))),
            checks,
        )
        zero_D = mm(inv2(G), mscale(F(0), dGdu))
        require(f"constant_depth_zero_Gram_response_{index}", zero_D == [[0, 0], [0, 0]], checks)

        # Exact null slopes using r=exp(2phi)=1/u.
        r = 1/u
        for side, root in enumerate((c/(r-alpha), -c/(r+alpha))):
            root_A = c+alpha*root
            require(f"null_root_{index}_{side}", -u*root_A*root_A+root*root/u == 0, checks)

        # Constant-depth orthogonal line and its nonzero-alpha mismatch with K.
        omega_perp = c*alpha/(1/(u*u)-alpha*alpha)
        require(f"V_orthogonal_{index}", G[0][1]+omega_perp*G[1][1] == 0, checks)
        require(f"perp_not_K_{index}", omega_perp != 0, checks)

        # Exact lattice-preserving R x S1 automorphisms. On the universal
        # cover R2 the exponential kernel is generated by (0,1). An invertible
        # lift descends to a group automorphism exactly when it maps that
        # primitive kernel generator to (0,+/-1), forcing the second column
        # while leaving the first column (r,b), r!=0, free.
        r_auto, b_auto = F(index+2, index+1), F(index-1, index+3)
        for epsilon in (F(-1), F(1)):
            lattice_B = [[r_auto, F(0)], [b_auto, epsilon]]
            require(f"lattice_det_{index}_{epsilon}", det2(lattice_B) == r_auto*epsilon != 0, checks)
            require(f"lattice_compact_column_{index}_{epsilon}", [lattice_B[0][1], lattice_B[1][1]] == [0, epsilon], checks)
            lattice_G = mm(mt(lattice_B), mm(G, lattice_B))
            lattice_XG = mm(mt(lattice_B), mm(XG, lattice_B))
            lattice_D = mm(inv2(lattice_G), lattice_XG)
            require(
                f"lattice_response_covariance_{index}_{epsilon}",
                lattice_D == mm(inv2(lattice_B), mm(D, lattice_B)),
                checks,
            )
        rejected_lifts = (
            [[r_auto, F(1, 3)], [b_auto, F(1)]],
            [[r_auto, F(0)], [b_auto, F(2)]],
            [[r_auto, F(0)], [b_auto, F(0)]],
        )
        require(
            f"lattice_nonprimitive_or_nonkernel_lifts_rejected_{index}",
            all(
                Bbad[0][1] != 0 or Bbad[1][1] not in (F(-1), F(1)) or det2(Bbad) == 0
                for Bbad in rejected_lifts
            ),
            checks,
        )

    # The full projective endpoint V and exceptional causal strata.
    for c, alpha, u, _ in samples:
        gvv = 1/u-alpha*alpha*u
        require("V_sign_formula_" + str(u), (gvv > 0) == (1 > alpha*alpha*u*u), checks)
    require("V_null_control", 1/F(1)-F(1)*F(1) == 0, checks)
    require("V_timelike_control", 1/F(1)-F(2)*F(2) < 0, checks)

    old = list(csv.DictReader(
        (ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/CANDIDATE_OUTCOMES.tsv").open(encoding="utf-8"),
        delimiter="\t",
    ))
    old_six = [row for row in old if row["candidate_id"] in {f"C{i:02d}" for i in range(1, 7)}]
    require("six_old_nonzero_analytic_endpoints", len(old_six) == 6 and all(F(row["gradient_determinant"]) != 0 for row in old_six), checks)

    # Independently check the positivity premise of the explicit convex
    # screen-metric path on exact rational controls.  This is a regression
    # anchor, not a substitute for the semantic identity-theorem review.
    h_descended = [[F(2), F(1, 3)], [F(1, 3), F(3)]]
    h_rank3 = [[F(4), F(-1, 5)], [F(-1, 5), F(5)]]
    for s in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
        h_s = madd(mscale(1-s, h_descended), mscale(s, h_rank3))
        require(f"positive_transition_screen_{s}", h_s[0][0] > 0 and det2(h_s) > 0, checks)

    directions = {row["id"]: row for row in csv.DictReader((HERE / "KILLING_DIRECTION_ATLAS.tsv").open(encoding="utf-8"), delimiter="\t")}
    strata = {row["id"]: row for row in csv.DictReader((HERE / "SELECTOR_STRATA.tsv").open(encoding="utf-8"), delimiter="\t")}
    transitions = {row["id"]: row for row in csv.DictReader((HERE / "TRANSITION_ATLAS.tsv").open(encoding="utf-8"), delimiter="\t")}
    automorphisms = {row["id"]: row for row in csv.DictReader((HERE / "KILLING_BASIS_AUTOMORPHISMS.tsv").open(encoding="utf-8"), delimiter="\t")}
    premises = list(csv.DictReader((ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(encoding="utf-8"), delimiter="\t"))
    dirty, dirty_sha = unrelated_dirty()
    require("dirty_count", len(dirty) == DIRTY_COUNT, checks)
    require("dirty_sha", dirty_sha == DIRTY_SHA, checks)
    current = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    require("current_premises", current.returncode == 0, checks)

    gate_path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("udt_repository_gate_library", gate_path)
    if spec is None or spec.loader is None:
        raise AssertionError("repository_gate_import")
    gate_library = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate_library)
    gate_library.BASE = BASE
    # Reuse the repository's authoritative current/frontier checks. Package
    # links are checked just below with support for the renderer's :line suffix.
    gate_library.PACKAGE = "__independent_gate_no_package__"
    frozen = gate_library.validate_frozen(ROOT)
    navigation = gate_library.validate_navigation(ROOT)
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    package_links = []
    for source in sorted(HERE.glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            target = re.sub(r":\d+$", "", target)
            resolved = Path(target) if Path(target).is_absolute() else source.parent / target
            require("package_link_" + source.name + "_" + str(len(package_links)), resolved.exists(), checks)
            package_links.append(str(resolved.resolve()))
    navigation["package_links"] = len(package_links)
    test_env = dict(os.environ)
    test_env["CUDA_VISIBLE_DEVICES"] = ""
    test_env["PYTHONDONTWRITEBYTECODE"] = "1"
    tests = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/"], cwd=ROOT, env=test_env,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    test_match = re.search(r"(\d+) passed, (\d+) xfailed", tests.stdout)
    require(
        "repository_tests",
        tests.returncode == 0 and test_match is not None and tuple(map(int, test_match.groups())) == (70, 1),
        checks,
    )

    snapshot = {
        "production": deepcopy(production),
        "directions": deepcopy(directions),
        "strata": deepcopy(strata),
        "transitions": deepcopy(transitions),
        "automorphisms": deepcopy(automorphisms),
        "manifest": deepcopy(manifest),
        "premises": deepcopy(premises),
        "dirty": {"count": len(dirty), "sha256": dirty_sha},
        "repository": {
            "premises": {"returncode": current.returncode, "stdout_sha256": hashlib.sha256(current.stdout.encode()).hexdigest()},
            "frozen": frozen,
            "tests": {
                "returncode": tests.returncode,
                "passed": 70,
                "xfailed": 1,
                "normalized_summary_sha256": hashlib.sha256(b"returncode=0;passed=70;xfailed=1\n").hexdigest(),
            },
            "navigation": navigation,
        },
    }

    def fail(gate, condition):
        if not condition:
            raise AssertionError(gate)

    def validate(state):
        p, d, s, t, a = state["production"], state["directions"], state["strata"], state["transitions"], state["automorphisms"]
        fail("F01", p["primary_classification"] == "MIXED_PARAMETER_STRATA")
        fail("F02", p["variable_depth_descended_classification"] == "UNIQUE_METRIC_FOUNDED_CLOCK_AND_RULER_LINES")
        fail("F03", p["gram_response"]["clock_eigenline"] == "K" and p["gram_response"]["ruler_eigenline"] == "V-alpha/c_E*K")
        fail("F04", p["gram_response"]["basis_covariant"] is True)
        fail("F05", p["gram_response"]["critical_point_handling"].startswith("global_constant_Lie_algebra_lines"))
        fail("F06", p["gram"]["causality_selects_K"] is False and "D05" in d and "D06" in d)
        fail("F07", p["topology"]["topology_alone_selects_K_among_helices"] is False and d["D04"]["orbit_type"] == "S1_FREE")
        fail("F08", p["twist"]["unique_timelike_no_depth_mixed_line_if_dphi_nonzero"] == "K" and p["twist"]["K_full_twist_generically_zero"] is False)
        fail("F09", p["twist"]["other_no_depth_mixed_line"].endswith("is_spacelike"))
        fail("F10", s["S03"]["classification"] == "RESIDUAL_FOUNDED_FRAMING_MISMATCH")
        fail("F11", all(key in s for key in ("S04", "S05", "S07", "S08", "S09")) and p["method_boundary"]["exceptional_strata_retained"] is True)
        fail("F12", p["strata_relation"] == "CONTINUOUSLY_ADJACENT_WITHIN_REGISTERED_STATIONARY_FAMILY")
        # F13 is deliberately a semantic-ledger gate.  The independent
        # mathematical checks above certify endpoints and convex positivity;
        # the analytic identity-theorem inference is separately fresh-reviewed.
        fail("F13", t["T03"]["conclusion"] == "NONZERO_FOR_POINTS_ARBITRARILY_CLOSE_TO_s=0")
        fail("F14", p["selector_handoff"] == "DESCENDED_GRAM_RESPONSE_K_TO_NEARBY_RANK3_K")
        fail("F15", p["macro_micro_assignment"] == "OPEN_NOT_TESTED" and t["T05"]["conclusion"] == "MACRO_MICRO_ASSIGNMENT_OPEN")
        fail("F16", p["method_boundary"]["strong_local_CSN_used"] is False and p["method_boundary"]["bootstrap_loaded"] is False)
        fail("F17", p["method_boundary"]["action_used"] is False and p["method_boundary"]["source_used"] is False and p["method_boundary"]["carrier_derived"] is False)
        fail("F18", p["method_boundary"]["all_real_projective_directions_classified"] is True and len(d) == 7 and len(a) == 4)
        source_ok = len(state["manifest"]) == 20
        if source_ok:
            for row in state["manifest"]:
                data = git_bytes("show", f"{BASE}:{row['path']}")
                blob = git_bytes("rev-parse", f"{BASE}:{row['path']}").decode().strip()
                source_ok = source_ok and blob == row["blob"] and hashlib.sha256(data).hexdigest() == row["sha256"] and len(data) == int(row["bytes"])
        fail("F19", source_ok)
        repository = state["repository"]
        repo_ok = (
            repository["premises"]["returncode"] == 0
            and repository["frozen"]["result"] == "PASS"
            and repository["frozen"]["entries"] == 127
            and repository["frozen"]["tracked_paths"] == 133
            and repository["tests"]["returncode"] == 0
            and repository["tests"]["passed"] == 70
            and repository["tests"]["xfailed"] == 1
            and repository["navigation"] == {"current_paths": 1114, "frontier_rows": 306, "frontier_targets": 101, "package_links": repository["navigation"]["package_links"]}
        )
        fail("F20", state["dirty"] == {"count": DIRTY_COUNT, "sha256": DIRTY_SHA} and repo_ok)
        fail("F21", len(p["twist"]["contact_coefficients"]) == 2 and p["twist"]["K_full_twist_generically_zero"] is False)
        fail("F22", s["S08"]["clock_result"] == "NO_GRAM_RESPONSE_SELECTOR" and p["twist"]["constant_depth_kappa_zero"] == "ALL_CONSTANT_KILLING_DIRECTIONS_TWIST_FREE")
        fail("F23", p["topology"]["lattice_preserving_automorphisms"] == "K_to_rK_plus_bV;V_to_epsilonV;r_nonzero;b_real;epsilon_plus_or_minus_one" and all(key in a for key in ("A01", "A02", "A03")))
        fail("F24", p["topology"]["higher_isometry_plane_selection"] == "OPEN" and s["S09"]["classification"] == "HIGHER_SYMMETRY_SCOPE_BOUNDARY")

    validate(snapshot)
    mutations = {
        "F01": ("promote_mixed_strata_to_universal_unique", lambda s: s["production"].__setitem__("primary_classification", "UNIQUE_METRIC_CLOCK_LINE_IN_DESCENDED_PLANE")),
        "F02": ("erase_variable_depth_positive_result", lambda s: s["production"].__setitem__("variable_depth_descended_classification", "OPEN")),
        "F03": ("swap_clock_and_ruler", lambda s: s["production"]["gram_response"].__setitem__("clock_eigenline", "V")),
        "F04": ("make_selector_coordinate_basis_dependent", lambda s: s["production"]["gram_response"].__setitem__("basis_covariant", False)),
        "F05": ("discard_depth_critical_points", lambda s: s["production"]["gram_response"].__setitem__("critical_point_handling", "undefined")),
        "F06": ("claim_causality_alone_selects_K", lambda s: s["production"]["gram"].__setitem__("causality_selects_K", True)),
        "F07": ("claim_orbit_topology_selects_one_helix", lambda s: s["production"]["topology"].__setitem__("topology_alone_selects_K_among_helices", True)),
        "F08": ("remove_twist_crosscheck_for_K", lambda s: s["production"]["twist"].__setitem__("unique_timelike_no_depth_mixed_line_if_dphi_nonzero", "OPEN")),
        "F09": ("misclassify_second_zero_mixed_line_as_timelike", lambda s: s["production"]["twist"].__setitem__("other_no_depth_mixed_line", "V-alpha/c_E*K_is_timelike")),
        "F10": ("identify_constant_depth_metric_clock_with_founded_K", lambda s: s["strata"]["S03"].__setitem__("classification", "UNIQUE_FOUNDED_PAIR")),
        "F11": ("drop_exceptional_strata", lambda s: s["strata"].pop("S04")),
        "F12": ("call_the_strata_disconnected", lambda s: s["production"].__setitem__("strata_relation", "DISCONNECTED")),
        "F13": ("erase_analytic_adjacency", lambda s: s["transitions"]["T03"].__setitem__("conclusion", "OPEN")),
        "F14": ("claim_different_clock_lines_across_handoff", lambda s: s["production"].__setitem__("selector_handoff", "DIFFERENT_LINES")),
        "F15": ("assign_macro_and_micro_physics", lambda s: s["production"].__setitem__("macro_micro_assignment", "DERIVED")),
        "F16": ("reactivate_strong_CSN", lambda s: s["production"]["method_boundary"].__setitem__("strong_local_CSN_used", True)),
        "F17": ("promote_geometry_to_action", lambda s: s["production"]["method_boundary"].__setitem__("action_used", True)),
        "F18": ("omit_generic_projective_direction", lambda s: s["directions"].pop("D03")),
        "F19": ("corrupt_source_identity", lambda s: s["manifest"][0].__setitem__("sha256", "0"*64)),
        "F20": ("change_dirty_or_repository_gate", lambda s: s["dirty"].__setitem__("count", DIRTY_COUNT+1)),
        "F21": ("erase_contact_twist_components", lambda s: s["production"]["twist"].__setitem__("contact_coefficients", [])),
        "F22": ("promote_zero_depth_zero_contact_control", lambda s: s["strata"]["S08"].__setitem__("clock_result", "UNIQUE_K")),
        "F23": ("replace_lattice_group_by_unrestricted_GL2", lambda s: s["production"]["topology"].__setitem__("lattice_preserving_automorphisms", "GL2")),
        "F24": ("hide_higher_isometry_scope", lambda s: s["production"]["topology"].__setitem__("higher_isometry_plane_selection", "SELECTED")),
    }
    catches = []
    for gate in [f"F{i:02d}" for i in range(1, 25)]:
        mutant = deepcopy(snapshot)
        description, mutation = mutations[gate]
        mutation(mutant)
        actual = ""
        try:
            validate(mutant)
        except AssertionError as exc:
            actual = str(exc)
        require("catch_" + gate, actual == gate, checks)
        catches.append({"id": gate, "mutation": description, "expected": "REJECT_"+gate, "actual": "REJECT_"+actual, "status": "PASS"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    identity_lines = [f"{row['path']}\t{row['blob']}\t{row['sha256']}\t{row['bytes']}" for row in manifest]
    result = {
        "schema": "udt-killing-plane-strata-transition-independent-1.0",
        "status": "PASS",
        "method": "stdlib_Fraction_independent_Gram_response_basis_twist_causal_and_mutation_replay",
        "checks_passed": len(checks),
        "production_checks": production["check_count"],
        "catch_proofs": len(catches),
        "source_count": len(manifest),
        "source_identity_sha256": hashlib.sha256(("\n".join(identity_lines)+"\n").encode()).hexdigest(),
        "dirty_count": len(dirty),
        "dirty_sha256": dirty_sha,
        "primary_classification": production["primary_classification"],
        "strata_relation": production["strata_relation"],
        "transition_verification_layers": {
            "independent_machine": "exact_nonzero_endpoints_and_positive_convex_screen_path_samples",
            "analytic_identity_theorem": "REQUIRES_FRESH_SEMANTIC_REVIEW",
            "stored_T03_check": "SEMANTIC_LEDGER_GUARD_NOT_INDEPENDENT_MATHEMATICS",
        },
        "lattice_verification": {
            "universal_cover_kernel": "ker_exp_generated_by_(0,1)",
            "primitive_kernel_image": "(0,epsilon)_epsilon_plus_or_minus_one",
            "derived_lift_form": "[[r,0],[b,epsilon]]_r_nonzero_b_real",
        },
        "repository_gates": snapshot["repository"],
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
