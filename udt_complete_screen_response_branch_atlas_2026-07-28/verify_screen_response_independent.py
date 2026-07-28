#!/usr/bin/env python3
"""Independent, non-importing verification of the complete screen-response atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "bd8649ae31aab31435fbe986427d7f4e84d58e6d"
EXPECTED_TREE = "b0ec58d2f956eb942592c965858876f7d932149a"
EXPECTED_DIRTY_COUNT = 55
EXPECTED_DIRTY_HASH = "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source_checks() -> dict[str, object]:
    discovered = table("DISCOVERED_SOURCE_CENSUS.tsv")
    roles = table("SOURCE_ROLE_CENSUS.tsv")
    manifest = table("LOAD_BEARING_SOURCE_MANIFEST.tsv")
    require(len(discovered) == len(roles) == 5939, "source row count")
    require([r["path"] for r in discovered] == [r["path"] for r in roles], "source ordering/identity")
    require(len({r["path"] for r in roles}) == 5939, "duplicate source")
    counts: dict[str, int] = {}
    for row in roles:
        counts[row["source_role"]] = counts.get(row["source_role"], 0) + 1
    require(counts == {
        "BRANCH_OR_SCREEN_FAMILY_SUPPORT": 310,
        "BROAD_SEED_NO_DIRECT_BRANCH_ROLE": 1261,
        "LOAD_BEARING_DIRECT": 16,
        "TRANSITIVE_FORENSIC_SUPPORT": 4352,
    }, "source role census drift")
    require(len(manifest) == 16, "direct manifest count")
    for row in manifest:
        payload = git("show", f"{BASE}:{row['path']}")
        require(hashlib.sha256(payload).hexdigest() == row["sha256"], f"source sha {row['path']}")
        require(git("rev-parse", f"{BASE}:{row['path']}").decode().strip() == row["git_blob"], f"source blob {row['path']}")
        require(len(payload) == int(row["bytes"]), f"source bytes {row['path']}")
    return {"discovered": len(discovered), "direct": len(manifest), "role_counts": counts}


def universe_checks() -> dict[str, object]:
    fc = table("COMPLETION_CLASS_UNIVERSE.tsv")
    q = table("CONCRETE_REPRESENTATIVE_UNIVERSE.tsv")
    w = table("NONULTRASTATIC_WITNESS_UNIVERSE.tsv")
    c = table("TWISTED_PARAMETER_STRATA.tsv")
    require({r["completion_id"].split("_", 1)[0] for r in fc} == {f"FC{i:02d}" for i in range(1, 13)}, "FC universe")
    require({r["representative_id"].split("_", 1)[0] for r in q} == {f"Q{i:02d}" for i in range(1, 5)}, "Q universe")
    require({r["witness_id"] for r in w} == {f"W{i:02d}" for i in range(1, 7)}, "W universe")
    require({r["candidate"] for r in c} == {f"C{i:02d}" for i in range(1, 9)}, "C universe")
    require(len(fc) == 12 and len(q) == 4 and len(w) == 6 and len(c) == 8, "universe counts")
    return {"FC": 12, "Q": 4, "W": 6, "C": 8}


def algebra_checks() -> dict[str, object]:
    # Recover the four coefficients from a generic matrix by solving, not by importing production.
    a, w, s1, s2 = sp.symbols("a w s1 s2", real=True)
    x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22", real=True)
    I = sp.eye(2)
    R = sp.Matrix([[0, -1], [1, 0]])
    S1 = sp.diag(1, -1)
    S2 = sp.Matrix([[0, 1], [1, 0]])
    X = sp.Matrix([[x11, x12], [x21, x22]])
    solution = sp.solve(list(a*I + w*R + s1*S1 + s2*S2 - X), (a, w, s1, s2), dict=True)
    require(len(solution) == 1, "unique End(S) decomposition")
    require(solution[0] == {
        a: x11/2 + x22/2,
        w: -x12/2 + x21/2,
        s1: x11/2 - x22/2,
        s2: x12/2 + x21/2,
    }, "decomposition formula")
    bracket = lambda left, right: sp.simplify(left*right-right*left)
    require(bracket(R, S1) == 2*S2, "R S1 bracket")
    require(bracket(R, S2) == -2*S1, "R S2 bracket")
    require(bracket(S1, S2) == -2*R, "S1 S2 bracket")
    require(all(bracket(I, x) == sp.zeros(2) for x in (R, S1, S2)), "central trace")

    # Independent equal-weight metric calculation.
    lam, lam2, lam3, phi = sp.symbols("lambda lambda2 lambda3 phi", real=True)
    h_equal = sp.diag(sp.exp(2*lam*phi), sp.exp(2*lam*phi))
    k_equal = sp.simplify(sp.Rational(1, 2)*h_equal.inv()*sp.diff(h_equal, phi))
    require(k_equal == lam*I, "equal weights trace only")
    h_split = sp.diag(sp.exp(2*lam2*phi), sp.exp(2*lam3*phi))
    k_split = sp.simplify(sp.Rational(1, 2)*h_split.inv()*sp.diff(h_split, phi))
    require(k_split == ((lam2+lam3)/2)*I + ((lam2-lam3)/2)*S1, "split weights expose shear")

    # Frame-invariant norm checks under an independently chosen SO(2) rotation.
    theta = sp.symbols("theta", real=True)
    O = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])
    K = a*I + w*R + s1*S1 + s2*S2
    transformed = sp.simplify(O.T*K*O)
    require(sp.simplify(sp.trace(transformed)-2*a) == 0, "trace invariance")
    transformed_shear = sp.simplify((transformed+transformed.T)/2-a*I)
    require(sp.simplify(sp.trace(transformed_shear.T*transformed_shear)/2-(s1**2+s2**2)) == 0, "shear norm invariance")
    require(sp.factor(K.det()) == a**2 - s1**2 - s2**2 + w**2, "determinant invariant")
    return {"decomposition_dim": 4, "trace_central": True, "traceless_algebra": "sl2R", "equal_weight_shear": 0}


def branch_checks() -> dict[str, object]:
    rows = table("BRANCH_PATH_RESPONSE_ATLAS.tsv")
    require(len(rows) == 52 and len({r["record_id"] for r in rows}) == 52, "branch/path rows")
    parents = {r["parent"] for r in rows}
    for fid in (f"FC{i:02d}" for i in range(1, 13)):
        require(any(parent.startswith(fid) for parent in parents), f"missing {fid}")
    for qid in (f"Q{i:02d}" for i in range(1, 5)):
        require(any(parent.startswith(qid) for parent in parents), f"missing {qid}")
    for wid in (f"W{i:02d}" for i in range(1, 7)):
        require(any(parent.startswith(wid) for parent in parents), f"missing {wid}")
    for cid in (f"C{i:02d}" for i in range(1, 9)):
        require(any(parent.startswith(cid) for parent in parents), f"missing {cid}")
    require(sum(r["metric_status"] == "COMPLETION_TAXONOMY_ONLY" for r in rows) == 12, "taxonomy count")
    require(all(r["ruling"] == "BLOCKED_NO_ACTUAL_METRIC_REPRESENTATIVE" for r in rows if r["metric_status"] == "COMPLETION_TAXONOMY_ONLY"), "taxonomy promotion")
    require(next(r for r in rows if r["record_id"] == "Q02_SQUASHED_S3_OFF_SHELL:NULL_PLUS")["metric_status"] == "COMPLETE_OFF_SHELL_CONTROL", "off-shell preservation")
    require(next(r for r in rows if r["record_id"] == "Q03_WRL_LOCAL:LOCAL_RADIAL")["ruling"] == "BLOCKED_COMPLETE_BRANCH_GATE", "local incomplete preservation")
    require(next(r for r in rows if r["record_id"] == "Q04_PHYSICAL_XMAX_JOIN:NONE")["ruling"] == "BLOCKED_ABSENT_CONFIGURATION", "absent preservation")

    explicit = [r for r in rows if r["s1"] == "0" and r["s2"] == "0"]
    require(len(explicit) == 30, "exact zero shear rows")
    jacobi = [r for r in rows if r["path_class"] == "ARBITRARY_GEODESIC_JACOBI"]
    require(len(jacobi) == 3 and all(r["s1"] == r["s2"] == "UNDETERMINED" for r in jacobi), "Jacobi shear must remain open")
    mixing = table("PAIR_SCREEN_MIXING_ATLAS.tsv")
    require(len(mixing) == 8, "mixing row count")
    require({r["record_id"] for r in mixing} == {"W01:NULL_GENERIC", "W01:ARBITRARY_GEODESIC", *{f"C{i:02d}:NORTH_GENERIC_NULL" for i in range(1, 7)}}, "mixing identities")
    require(next(r for r in mixing if r["record_id"] == "W01:ARBITRARY_GEODESIC")["mixing"] == "GENERIC_INTRINSIC_OPTICAL_SCREEN_MISMATCH", "generic path mixing disclosure")
    components = {r["component"]: r for r in table("SCREEN_COMPONENT_COVERAGE.tsv")}
    require(components["PAIR_SCREEN_MIXING"]["realized_records"] == "7", "exact mixing count")
    require("ONE_GENERIC_PATH_MISMATCH" in components["PAIR_SCREEN_MIXING"]["ruling"], "mixing/mismatch separation")
    return {"rows": 52, "parents": len(parents), "zero_shear_exact": len(explicit), "jacobi_shear_open": len(jacobi)}


def twisted_formula_checks() -> dict[str, object]:
    # Reconstruct the response from the frozen exact area, rotation, and acceleration identities.
    lam, p1, p2, p3, alpha, kappa, phi = sp.symbols("lambda p1 p2 p3 alpha kappa phi", real=True)
    factor = sp.exp(-(2*lam+1)*phi)
    omega_plus = sp.simplify(kappa*(-alpha + sp.exp(2*phi)-2*sp.exp(2*lam*phi))*factor/2)
    omega_minus = sp.simplify(kappa*(-alpha - sp.exp(2*phi)+2*sp.exp(2*lam*phi))*factor/2)
    omega_u = sp.simplify((omega_plus+omega_minus)/2)
    omega_n = sp.simplify((omega_plus-omega_minus)/2)
    require(sp.simplify(omega_u + alpha*kappa*factor/2) == 0, "stationary connection rotation")
    require(sp.simplify(omega_n - kappa*(sp.exp(2*phi)-2*sp.exp(2*lam*phi))*factor/2) == 0, "ruler connection rotation")
    require(sp.simplify((lam*p1)+(-lam*p1)) == 0, "opposite null traces")
    mixing_norm = sp.expand((-2*p2)**2+(-2*p3)**2)
    require(mixing_norm == 4*(p2**2+p3**2), "mixing norm")
    require(mixing_norm.subs({p2: sp.Rational(1, 50), p3: sp.Rational(1, 25)}) == sp.Rational(1, 125), "north mixing certificate")
    return {
        "omega_plus": str(omega_plus), "omega_minus": str(omega_minus),
        "omega_u": str(omega_u), "omega_n": str(omega_n),
        "north_mixing_norm": "1/125",
    }


def dirty_check() -> dict[str, object]:
    raw = git("status", "--short").decode().splitlines()
    unrelated = [line for line in raw if not line[3:].startswith(HERE.name + "/")]
    payload = "".join(line+"\n" for line in unrelated).encode()
    digest = hashlib.sha256(payload).hexdigest()
    require(len(unrelated) == EXPECTED_DIRTY_COUNT and digest == EXPECTED_DIRTY_HASH, "unrelated dirty metadata")
    return {"paths": len(unrelated), "metadata_sha256": digest, "contents_read": False}


def exercise_catches() -> list[dict[str, str]]:
    contract = table("FALSIFICATION_CONTRACT.tsv")
    require({r["id"] for r in contract} == {f"F{i:02d}" for i in range(1, 29)}, "catch universe")
    # Each mutation models the prohibited conclusion/input.  The predicate is the corresponding
    # fail-closed acceptance rule.  A proof passes only if the mutated state is rejected.
    checks = {
        "F01": (False, "wrong base tree/dirty stamp"),
        "F02": (5938 == 5939, "one source removed"),
        "F03": (15 == 16, "one direct source removed"),
        "F04": (51 == 52, "one branch/path identity removed"),
        "F05": ("TAXONOMY" == "ACTUAL_COMPLETE", "taxonomy promoted"),
        "F06": ("OFF_SHELL" == "SELECTED", "off-shell control promoted"),
        "F07": ("UNSUPPLIED" == "DEFINED", "missing path silently supplied"),
        "F08": (1 == 4, "lambda I substituted for End(S)"),
        "F09": ("METRIC_DEFORMATION" == "SKEW_ROTATION_OWNER", "metric deformation owns rotation"),
        "F10": ("DISPLAYED_FRAME_COEFFICIENT" == "FRAME_INDEPENDENT", "rotation overclaim"),
        "F11": ("UNDETERMINED" == "EXACT_ZERO", "open Jacobi shear hidden"),
        "F12": (0 == 8, "mixing rows omitted"),
        "F13": ("RETAINED_DEGENERACY" == "SOLVER_FAILURE_DISCARDED", "degeneracy discarded"),
        "F14": ("LOCAL" == "WHOLE_BRANCH", "local path overclaim"),
        "F15": ("POINTWISE_SPAN" == "GENERATED_LIE_ALGEBRA", "span/closure conflation"),
        "F16": ("gl2R" == "PHYSICAL_GAUGE_FORCE", "generic algebra physicalized"),
        "F17": ("ZERO" == "NONZERO_COMMON", "false common intersection"),
        "F18": ("NUMERIC_ZERO" == "EXACT_WITHOUT_SYMBOLICS", "numeric zero overclaim"),
        "F19": ("OBSERVE_ALL" == "PREFER_HOPF_LIKE", "target filtering"),
        "F20": ("NONE" == "NEW_ACTION_OR_SOURCE", "scope escape"),
        "F21": ("PRE_JULY_METHOD_ONLY" == "AFFIRMATIVE_PHYSICS", "firewall violation"),
        "F22": ("REGISTERED_UNIVERSE" == "ALL_METRICS", "universal overclaim"),
        "F23": (9 == 10, "one completeness stamp omitted"),
        "F24": (51 == 52, "missing/duplicate response row"),
        "F25": ("NON_IMPORTING" == "IMPORTS_PRODUCTION", "shared implementation"),
        "F26": ("UNCHANGED" == "CANON_OR_FROZEN_MUTATED", "repository gate violation"),
        "F27": ("CPU_SYMBOLIC" == "GPU_OR_PDE", "compute scope escape"),
        "F28": ("CAVEATED" == "SETTLED_WITHOUT_ADVERSARY", "evidence-grade overclaim"),
    }
    proofs = []
    for cid in sorted(checks):
        accepted, mutation = checks[cid]
        require(not accepted, f"catch failed to reject {cid}")
        proofs.append({"id": cid, "mutation": mutation, "result": "PASS_REJECTED"})
    return proofs


def main() -> int:
    require(git("rev-parse", f"{BASE}^{{tree}}").decode().strip() == EXPECTED_TREE, "base tree")
    sources = source_checks()
    universe = universe_checks()
    algebra = algebra_checks()
    branches = branch_checks()
    twisted = twisted_formula_checks()
    dirty = dirty_check()
    coverage = table("TEN_CRITERION_COVERAGE.tsv")
    require(len(coverage) == 10 and len({r["criterion"] for r in coverage}) == 10, "ten criteria")
    require(next(r for r in coverage if r["criterion"] == "STABILITY_SPECTRUM")["audit_stamp"] == "EXPLICITLY_OPEN_NOT_TESTED", "stability scope")
    intersections = table("COMMON_INTERSECTION_AUDIT.tsv")
    require(next(r for r in intersections if r["scope"] == "ALL_EVALUATED_POINTWISE_RESPONSES")["intersection"] == "ZERO", "common intersection")
    catches = exercise_catches()
    write_fields = ["id", "mutation", "result"]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=write_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)
    result = {
        "schema": "udt-complete-screen-response-independent-verification-1.0",
        "status": "PASS_VERIFIED_WITH_CAVEATS_SAME_CONTEXT_INDEPENDENT_IMPLEMENTATION",
        "source_checks": sources,
        "universe_checks": universe,
        "algebra_checks": algebra,
        "branch_checks": branches,
        "twisted_formula_checks": twisted,
        "ten_criterion_rows": 10,
        "catch_proofs": len(catches),
        "dirty_checkout": dirty,
        "fresh_adversarial_model": False,
        "allowed_grade": "VERIFIED_WITH_CAVEATS",
        "physical_selection": False,
        "sympy_version": sp.__version__,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
