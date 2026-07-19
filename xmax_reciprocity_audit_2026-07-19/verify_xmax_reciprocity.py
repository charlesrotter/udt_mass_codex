#!/usr/bin/env python3
"""Independent matrix/pullback verifier and fail-closed semantic catches."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "35a7423e018e67c1aa02aef8932d0c92f036bd4b"
RESULT = HERE / "DERIVATION_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(data: dict) -> None:
    require(data["schema"] == "udt-xmax-reciprocity-audit-1.0", "schema changed")
    require(len(data["checks"]) == 50 and all(value == "PASS" for value in data["checks"].values()), "algebra census/failure")
    bounded = data["bounded_composition"]
    require(bounded["multiplicative_character"] == "A(xi composed eta)=A(xi)A(eta)", "multiplicative character lost")
    require(bounded["reversal_character"] == "A(-xi)=1/A(xi)", "reversal reciprocity lost")
    require(
        bounded["classification"]
        == "EXACT_WITHIN_WORKING_XMAX_PLUS_CHOSEN_FRACTIONAL_LINEAR_XR1_LAW_SIGNED_ORIENTED_DOMAIN_AND_ADDITIVE_COORDINATE_TO_METRIC_PHI_IDENTIFICATION",
        "chosen XR1/metric-phi premises lost or promoted",
    )
    alternative = data["alternative_bounded_group_countermodel"]
    require(
        alternative["classification"]
        == "EXACT_COUNTERMODEL_FINITE_BOUND_COMPOSITION_REVERSAL_AND_REGULARITY_DO_NOT_FORCE_FRACTIONAL_LINEAR_XR1_OR_MULTIPLICATIVE_A",
        "alternative bounded countergroup lost",
    )
    require(
        alternative["witness"]
        == {
            "xi": "1/sqrt(2)",
            "xi_boxplus_xi": "2/sqrt(5)",
            "A_of_composition": "9 - 4*sqrt(5)",
            "A_product": "17 - 12*sqrt(2)",
        },
        "alternative bounded countergroup witness changed",
    )
    involutions = data["candidate_involutions"]
    require("NOT_INTERNAL" in involutions["arithmetic_x_to_X2_over_x"]["classification"], "arithmetic inverse promoted")
    require("NOT_POSITIONAL_REVERSAL" in involutions["boundary_complement"]["classification"], "complement promoted")
    require("NOT_SELF_MAP" in involutions["scale_dual"]["classification"], "scale duality domain omitted")
    metric = data["metric_symmetry"]
    require(metric["spatial_ratio_witnesses_alpha_one_third"] == {"xi_0": "32/81", "xi_half": "512/625"}, "metric counterwitness changed")
    require(metric["classification"].startswith("XR1_RECENTERING_NOT_ISOMETRY_OR_CSN_EQUIVALENCE"), "metric symmetry promoted")
    angular = data["angular_extension"]
    require(angular["counterfamily_result"].endswith("MINUS_ONE_ZERO_OR_PLUS_ONE"), "angular counterfamily lost")
    require(
        angular["conditional_isotropic_group"]["status"]
        == "CHOSE_CONDITIONAL_COMPARISON_NOT_DERIVED_FROM_1D_XR1_OR_ISOTROPY_HOMOGENEITY_ALONE",
        "conditional group promoted",
    )
    require(angular["flat_isotropic_counterextension"]["translation_algebra"] == "[Tx,Ty]=0", "flat isotropic counterextension lost")
    scale = data["scale_and_boundary"]
    require(scale["finite_cell_comparison"]["classification"] == "DISTINCT_OBJECTS_UNLESS_A_NEW_GLOBAL_MAP_IS_DERIVED", "seal silently identified")
    adjudication = data["adjudication"]
    require(adjudication["action"].startswith("NOT_SELECTED"), "action promoted")
    require(adjudication["copresence"].endswith("NOT_A_TRANSFORMATION_OR_ACTION_SELECTOR"), "co-presence promoted")
    require("FINITE_XMAX_AND_GENERIC_GROUP_AXIOMS_DO_NOT_FORCE_XR1" in data["maximum_conclusion"], "XR1 uniqueness caveat lost")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    before = sha256(RESULT)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_xmax_reciprocity.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=180, check=False,
    )
    require(replay.returncode == 0, f"derivation replay failed: {replay.stderr}")
    require(not replay.stderr, "derivation replay emitted stderr")
    require(sha256(RESULT) == before, "derivation replay changed result")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_derivation_and_contract"] = "PASS"

    # Independent projective-matrix representation.  This route does not call
    # the primary composition helper.
    xi, eta = sp.symbols("xi eta", real=True)
    matrix = lambda value: sp.Matrix([[1, value], [value, 1]])
    composed = sp.cancel((xi + eta) / (1 + xi * eta))
    require(sp.simplify(matrix(xi) * matrix(eta) - (1 + xi * eta) * matrix(composed)) == sp.zeros(2), "projective composition mismatch")
    plus = sp.Matrix([1, 1]); minus = sp.Matrix([1, -1])
    require(sp.simplify(matrix(xi) * plus - (1 + xi) * plus) == sp.zeros(2, 1), "plus eigenline mismatch")
    require(sp.simplify(matrix(xi) * minus - (1 - xi) * minus) == sp.zeros(2, 1), "minus eigenline mismatch")
    ratio = (1 - xi) / (1 + xi)
    ratio_product = sp.cancel((1 - composed) / (1 + composed))
    require(sp.simplify(ratio_product - ratio * ratio.subs(xi, eta)) == 0, "independent A character mismatch")
    require(sp.simplify(ratio * ratio.subs(xi, -xi) - 1) == 0, "independent reversal mismatch")
    checks["independent_projective_matrix_character"] = "PASS"

    # Independent conjugated-addition countergroup. This establishes that a
    # finite bound and smooth reversible group law do not select XR1.
    u = sp.symbols("u", real=True)
    compactify = lambda value: value / sp.sqrt(1 + value**2)
    require(sp.simplify(sp.diff(compactify(u), u) - (1 + u**2) ** sp.Rational(-3, 2)) == 0, "alternative compactification regularity mismatch")
    require(sp.limit(compactify(u), u, sp.oo) == 1 and sp.limit(compactify(u), u, -sp.oo) == -1, "alternative endpoints mismatch")
    alt_xi = 1 / sp.sqrt(2)
    alt_composed = compactify(2)
    alt_A_composed = sp.radsimp((1 - alt_composed) / (1 + alt_composed))
    alt_A_product = sp.expand(sp.radsimp(((1 - alt_xi) / (1 + alt_xi)) ** 2))
    require(sp.simplify(alt_A_composed - (9 - 4 * sp.sqrt(5))) == 0, "alternative composition witness mismatch")
    require(sp.simplify(alt_A_product - (17 - 12 * sp.sqrt(2))) == 0, "alternative A-product witness mismatch")
    require(sp.simplify(alt_A_composed - alt_A_product) != 0, "generic bounded group falsely made A multiplicative")
    checks["independent_alternative_bounded_group_countermodel"] = "PASS"

    # Independent tensor-component pullback at two exact points.
    alpha = sp.Rational(1, 3)
    transformed = (xi - alpha) / (1 - alpha * xi)
    derivative = sp.diff(transformed, xi)
    A = lambda value: (1 - value) / (1 + value)
    time_ratio = sp.factor(A(transformed) / A(xi))
    radial_ratio = sp.factor((A(xi) / A(transformed)) * derivative**2)
    require(sp.simplify(time_ratio - 2) == 0, "independent time ratio mismatch")
    radial_samples = [sp.simplify(radial_ratio.subs(xi, point)) for point in (0, sp.Rational(1, 2))]
    require(radial_samples == [sp.Rational(32, 81), sp.Rational(512, 625)], "independent radial samples mismatch")
    require(radial_samples[0] != radial_samples[1], "radial ratio falsely constant")
    checks["independent_metric_pullback_counterwitness"] = "PASS"

    # Independent endpoint and angular calculations.
    theta, phi = sp.symbols("theta phi", positive=True)
    proper = sp.integrate(1 + sp.cos(theta), (theta, 0, sp.pi / 2))
    require(proper == 1 + sp.pi / 2, "proper endpoint integral mismatch")
    optical = -xi - 2 * sp.log(1 - xi)
    require(sp.limit(optical, xi, 1, dir="-") == sp.oo, "optical endpoint not divergent")
    warp_results = []
    for warp in (phi, sp.sinh(phi), sp.sin(phi)):
        warp_results.append((sp.simplify(-sp.diff(warp, phi, 2) / warp), sp.simplify((1 - sp.diff(warp, phi) ** 2) / warp**2)))
    require(warp_results == [(0, 0), (-1, -1), (1, 1)], "angular warp counterfamily mismatch")
    checks["independent_endpoint_and_angular_counterfamily"] = "PASS"

    # Independent non-collinear generator commutator.
    Kx = sp.zeros(4); Kx[0, 1] = Kx[1, 0] = 1
    Ky = sp.zeros(4); Ky[0, 2] = Ky[2, 0] = 1
    commutator = Kx * Ky - Ky * Kx
    require(commutator[1, 2] == 1 and commutator[2, 1] == -1 and sum(abs(v) for v in commutator) == 2, "generator commutator mismatch")
    Tx = sp.zeros(4); Tx[1, 0] = 1
    Ty = sp.zeros(4); Ty[2, 0] = 1
    require(Tx * Ty - Ty * Tx == sp.zeros(4), "flat isotropic translation commutator mismatch")
    checks["independent_conditional_and_flat_angular_algebras"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=90, check=False,
    )
    require(inventory_run.returncode == 0, f"source replay failed: {inventory_run.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory changed")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 13 and len({row["path"] for row in sources}) == 13, "source census mismatch")
    xmax_source = next(row for row in sources if row["path"] == "simple_metric_xmax_POSTULATE.md")
    require(xmax_source["source_class"] == "POST_JULY_WORKING_LEAD", "Xmax source promoted")
    checks["source_inventory_replay"] = "PASS"

    candidates = read_tsv(HERE / "RECIPROCITY_CANDIDATE_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(candidates) == 13 and len({row["id"] for row in candidates}) == 13, "candidate ledger mismatch")
    require(len(statuses) == 14 and len({row["id"] for row in statuses}) == 14, "status ledger mismatch")
    require(
        next(row for row in statuses if row["id"] == "S01")["status"]
        == "EXACT_WITHIN_WORKING_XMAX_PLUS_CHOSEN_XR1_AND_METRIC_PHI_JOIN",
        "conditional stamp lost",
    )
    require(next(row for row in statuses if row["id"] == "S01B")["status"] == "REFUTED_IMPLICATION", "countermodel status lost")
    require(next(row for row in statuses if row["id"] == "S12")["status"] == "LEAD_NOT_ADOPTED", "lead promoted")
    checks["ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat_report = " ".join(report.split())
    for phrase in (
        "Within the historical **fractional-linear** `X_max` composition law",
        "not a consequence of a finite bound alone",
        "exact smooth bounded countergroup",
        "does not preserve the currently pinned reciprocal radial metric",
        "radial Xmax reciprocity does not select flat, hyperbolic, or spherical angular completion",
        "An exact flat counterextension",
        "Silent identification with the finite-cell seal fails",
        "not a premise adopted by this audit",
        "Xmax reciprocity has not decided between them",
    ):
        require(phrase in flat_report, f"report disclosure missing: {phrase}")
    for forbidden in (
        "Xmax reciprocity derives the complete action",
        "the finite-cell seal is the Xmax boundary",
        "SO(1,3) is the native UDT position group",
        "co-presence selects the action",
    ):
        require(forbidden not in report, f"forbidden promotion: {forbidden}")
    checks["report_contract"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_controls = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md", "CANON.md"}
    require(not forbidden_controls.intersection(changed), f"forbidden controls changed: {forbidden_controls.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["bounded_composition"]["classification"] = "UNCONDITIONAL_NATIVE_LAW"
    expect_failure("chosen_XR1_and_metric_phi_premises_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    del mutation["alternative_bounded_group_countermodel"]
    expect_failure("alternative_bounded_countergroup_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["alternative_bounded_group_countermodel"]["classification"] = "XR1_UNIQUE"
    expect_failure("finite_bound_falsely_promotes_XR1_uniqueness", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["bounded_composition"]["multiplicative_character"] = "absent"
    expect_failure("multiplicative_character_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["candidate_involutions"]["arithmetic_x_to_X2_over_x"]["classification"] = "INTERNAL_RECIPROCITY"
    expect_failure("arithmetic_inverse_domain_failure_hidden", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["metric_symmetry"]["classification"] = "FULL_METRIC_ISOMETRY"
    expect_failure("metric_counterwitness_ignored", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["angular_extension"]["counterfamily_result"] = "UNIQUE_HYPERBOLIC_ANGULAR_SECTOR"
    expect_failure("angular_counterfamily_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["angular_extension"]["conditional_isotropic_group"]["status"] = "NATIVE_DERIVED"
    expect_failure("conditional_position_group_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["angular_extension"]["flat_isotropic_counterextension"]["translation_algebra"] = "[Tx,Ty]=-Jz"
    expect_failure("flat_isotropic_counterextension_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["scale_and_boundary"]["finite_cell_comparison"]["classification"] = "SAME_BOUNDARY"
    expect_failure("seal_Xmax_identification_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["action"] = "EH_DERIVED"
    expect_failure("action_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["copresence"] = "ACTION_SELECTOR"
    expect_failure("copresence_promoted", lambda: validate(mutation), catches)

    output = {
        "schema": "udt-xmax-reciprocity-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "projective_matrix_character": "PASS",
            "alternative_bounded_group_A_composition": "9 - 4*sqrt(5)",
            "alternative_bounded_group_A_product": str(alt_A_product),
            "time_ratio_alpha_one_third": str(time_ratio),
            "radial_ratio_xi_zero": str(radial_samples[0]),
            "radial_ratio_xi_half": str(radial_samples[1]),
            "proper_endpoint_over_X": str(proper),
            "angular_curvature_classes": [[str(a), str(b)] for a, b in warp_results],
            "flat_translation_commutator": "zero",
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
