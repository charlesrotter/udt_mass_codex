#!/usr/bin/env python3
"""Exact symmetry algebra for the metric-natural selector possibility/no-go audit."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "e7ea5936eaecbab626db0f30e12a8be4630b5dd7"


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def vec(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[i, j] for i in range(matrix.rows) for j in range(matrix.cols)])


def linear_rank(expressions: list[sp.Expr], variables: list[sp.Symbol]) -> int:
    return int(sp.linear_eq_to_matrix(expressions, variables)[0].rank())


def source_replay() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        result = subprocess.run(["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode:
            raise RuntimeError(result.stderr.decode("utf-8", "replace"))
        if len(result.stdout) != int(row["size_bytes"]):
            raise AssertionError(f"source size mismatch {row['path']}")
        if hashlib.sha256(result.stdout).hexdigest() != row["sha256"]:
            raise AssertionError(f"source hash mismatch {row['path']}")
    return len(rows)


def main() -> None:
    eta = sp.diag(-1, 1, 1, 1)

    def basis_matrix(entries: list[tuple[int, int, int]]) -> sp.Matrix:
        out = sp.zeros(4)
        for i, j, value in entries:
            out[i, j] = value
        return out

    # Boosts and rotations in the defining Lorentz representation.
    K01 = basis_matrix([(0, 1, 1), (1, 0, 1)])
    K02 = basis_matrix([(0, 2, 1), (2, 0, 1)])
    K03 = basis_matrix([(0, 3, 1), (3, 0, 1)])
    J12 = basis_matrix([(1, 2, 1), (2, 1, -1)])
    J13 = basis_matrix([(1, 3, 1), (3, 1, -1)])
    J23 = basis_matrix([(2, 3, 1), (3, 2, -1)])
    lorentz = [K01, K02, K03, J12, J13, J23]
    if any(B.T * eta + eta * B != sp.zeros(4) for B in lorentz):
        raise AssertionError("Lorentz basis convention failed")

    # so(1,3) is perfect: its commutators span all six generators.
    basis_vectors = sp.Matrix.hstack(*(vec(B) for B in lorentz))
    bracket_coordinates = []
    bracket_matrices = []
    for i, A in enumerate(lorentz):
        for B in lorentz[i + 1:]:
            bracket = A * B - B * A
            bracket_matrices.append(bracket)
            solution = basis_vectors.gauss_jordan_solve(vec(bracket))[0]
            bracket_coordinates.append(solution)
    bracket_span_rank = int(sp.Matrix.hstack(*(vec(B) for B in bracket_matrices)).rank())
    character_constraint_rank = int(sp.Matrix.hstack(*bracket_coordinates).T.rank())
    character_nullity = 6 - character_constraint_rank
    if (bracket_span_rank, character_constraint_rank, character_nullity) != (6, 6, 0):
        raise AssertionError("Lorentz perfectness/character result failed")

    # Full-isotropy fixed vectors/covectors and endomorphism commutant.
    fixed_vector_rank = int(sp.Matrix.vstack(*lorentz).rank())
    fixed_covector_rank = int(sp.Matrix.vstack(*(B.T for B in lorentz)).rank())
    xs = sp.symbols("x0:16")
    X = sp.Matrix(4, 4, xs)
    full_commutator_equations = []
    for B in lorentz:
        full_commutator_equations.extend(vec(X * B - B * X))
    full_commutant_rank = linear_rank(full_commutator_equations, list(xs))
    full_commutant_nullity = 16 - full_commutant_rank
    if (fixed_vector_rank, fixed_covector_rank, full_commutant_nullity) != (4, 4, 1):
        raise AssertionError("full isotropy ranks failed")

    self_adjoint = list(vec(X.T * eta - eta * X))
    e0, e1 = sp.eye(4)[:, 0], sp.eye(4)[:, 1]

    def reduction_rank(stabilizer: list[sp.Matrix], eigen_constraints: list[sp.Matrix]) -> tuple[int, int]:
        equations = list(self_adjoint)
        for B in stabilizer:
            equations.extend(vec(X * B - B * X))
        equations.extend(eigen_constraints)
        rank = linear_rank(equations, list(xs))
        return rank, 16 - rank

    observer_rank, observer_nullity = reduction_rank(
        [J12, J13, J23], list(X * e0 + e0)
    )
    pair_rank, pair_nullity = reduction_rank(
        [J23], list(X * e0 + e0) + list(X * e1 - e1)
    )
    ruler_rank, ruler_nullity = reduction_rank(
        [K02, K03, J23], list(X * e1 - e1)
    )
    if (observer_nullity, pair_nullity, ruler_nullity) != (1, 1, 1):
        raise AssertionError("reduced-family nullities failed")

    a = sp.symbols("a", real=True)
    observer_family = sp.diag(-1, a, a, a)
    pair_family = sp.diag(-1, 1, a, a)
    ruler_family = sp.diag(a, 1, a, a)
    for family, stabilizer, constraints in [
        (observer_family, [J12, J13, J23], [observer_family * e0 + e0]),
        (pair_family, [J23], [pair_family * e0 + e0, pair_family * e1 - e1]),
        (ruler_family, [K02, K03, J23], [ruler_family * e1 - e1]),
    ]:
        if family.T * eta - eta * family != sp.zeros(4):
            raise AssertionError("reduced family not self-adjoint")
        if any(family * B - B * family != sp.zeros(4) for B in stabilizer):
            raise AssertionError("reduced family not equivariant")
        if any(value != 0 for matrix in constraints for value in matrix):
            raise AssertionError("reduced eigen constraint failed")

    # A supplied observer line plus no distinguished ruler forces all spatial
    # eigenvalues equal. Requiring the founded +1 ruler eigenvalue then fixes a=+1.
    observer_plus_one = observer_family.subs(a, 1)
    # Dually, a supplied ruler line plus no observer forces a=-1 on the complement.
    ruler_minus_one = ruler_family.subs(a, -1)

    # Holonomy centralizers of the ordered-pair diagonal family.
    lam = sp.symbols("lambda", real=True)
    Xlam = sp.diag(-1, 1, lam, lam)
    cs = sp.symbols("c0:6")
    A = sum((coefficient * generator for coefficient, generator in zip(cs, lorentz)), sp.zeros(4))
    holonomy_rows = []
    for value, label in [(2, "GENERIC_LAMBDA_2"), (1, "LAMBDA_PLUS_ONE"), (-1, "LAMBDA_MINUS_ONE"), (0, "LAMBDA_ZERO")]:
        equations = list(vec((A * Xlam - Xlam * A).subs(lam, value)))
        rank = linear_rank(equations, list(cs))
        holonomy_rows.append({
            "stratum": label, "lambda": value, "centralizer_rank_constraints": rank,
            "centralizer_dimension_in_so13": 6 - rank,
            "full_holonomy_descent": "FAIL" if 6 - rank < 6 else "PASS",
        })
    if [row["centralizer_dimension_in_so13"] for row in holonomy_rows] != [1, 3, 3, 1]:
        raise AssertionError("holonomy centralizer dimensions failed")

    # Non-collinear comparison has an angular commutator.
    boost_commutator = K01 * K02 - K02 * K01
    angular_commutator_nonzero = boost_commutator != sp.zeros(4)
    angular_commutator_in_rotation_span = int(sp.Matrix.hstack(vec(J12), vec(boost_commutator)).rank()) == 1
    if not (angular_commutator_nonzero and angular_commutator_in_rotation_span):
        raise AssertionError("boost angular commutator failed")

    # Endpoint cocycle and invariant-interval controls.
    fp, fq, fr = sp.symbols("f_p f_q f_r")
    endpoint_cocycle = sp.simplify((fq - fp) + (fr - fq) - (fr - fp)) == 0
    # Timelike points p=(0,0), q=(2,0), r=(4,1).
    interval_defect = sp.simplify(2 + sp.sqrt(3) - sp.sqrt(15))
    invariant_interval_nonadditive = interval_defect != 0
    if not endpoint_cocycle or not invariant_interval_nonadditive:
        raise AssertionError("depth controls failed")

    # Finite integration of each supplied constant generator is exact.
    s, t = sp.symbols("s t", real=True)
    finite_pair_composition = all(
        sp.simplify(value) == 0
        for value in (sp.exp(s * pair_family) * sp.exp(t * pair_family) - sp.exp((s + t) * pair_family))
    )
    if not finite_pair_composition:
        raise AssertionError("finite family integration failed")

    source_count = source_replay()

    rank_rows = [
        {"test": "LIE_BRACKET_SPAN", "equations_or_ambient": 6, "rank": bracket_span_rank, "nullity": 0, "ruling": "so(1,3)_IS_PERFECT"},
        {"test": "REAL_CHARACTER_CONSTRAINT", "equations_or_ambient": 6, "rank": character_constraint_rank, "nullity": character_nullity, "ruling": "ONLY_ZERO_CONTINUOUS_CHARACTER"},
        {"test": "FULL_ISOTROPY_FIXED_VECTOR", "equations_or_ambient": 4, "rank": fixed_vector_rank, "nullity": 4-fixed_vector_rank, "ruling": "NO_NONZERO_FIXED_VECTOR"},
        {"test": "FULL_ISOTROPY_FIXED_COVECTOR", "equations_or_ambient": 4, "rank": fixed_covector_rank, "nullity": 4-fixed_covector_rank, "ruling": "NO_NONZERO_FIXED_COVECTOR"},
        {"test": "FULL_LORENTZ_ENDOMORPHISM_COMMUTANT", "equations_or_ambient": 16, "rank": full_commutant_rank, "nullity": full_commutant_nullity, "ruling": "SCALAR_IDENTITY_ONLY"},
        {"test": "OBSERVER_LINE_SO3_REDUCTION", "equations_or_ambient": 16, "rank": observer_rank, "nullity": observer_nullity, "ruling": "diag(-1,a,a,a)"},
        {"test": "ORDERED_PAIR_SO2_REDUCTION", "equations_or_ambient": 16, "rank": pair_rank, "nullity": pair_nullity, "ruling": "diag(-1,+1,a,a)"},
        {"test": "RULER_LINE_SO12_REDUCTION", "equations_or_ambient": 16, "rank": ruler_rank, "nullity": ruler_nullity, "ruling": "diag(a,+1,a,a)"},
    ]
    write_tsv("SYMMETRY_RANKS.tsv", ["test", "equations_or_ambient", "rank", "nullity", "ruling"], rank_rows)
    write_tsv("HOLONOMY_CENTRALIZER_ATLAS.tsv", list(holonomy_rows[0]), holonomy_rows)

    category_rows = [
        {"category": "I0", "supplied_data": "metric/coframe plus orientations", "exact_result": "full-isotropy forbids a metric-only non-scalar pointwise reciprocal generator", "depth_result": "frame-only character unavailable; base/higher-jet/nonlocal route not exhausted", "lift_result": "POINTWISE_NO_GO_ON_FULL_CLASS", "global_result": "OPEN", "joint_result": "NO_UNIVERSAL_DERIVATION"},
        {"category": "I1", "supplied_data": "all observer endpoint queries", "exact_result": "query law is allowed but full Lorentz comparison has no nontrivial real additive character", "depth_result": "FRAME_ONLY_SCALAR_NO_GO; BASE_COCYCLE_OPEN", "lift_result": "nonabelian full-frame comparison retains angular data", "global_result": "path/groupoid semantics open", "joint_result": "NO_SCALAR_ONLY_JOINT"},
        {"category": "I2", "supplied_data": "timelike observer line or congruence", "exact_result": "SO3 equivariance gives diag(-1,a,a,a); founded spatial +1 fixes a=+1", "depth_result": "not supplied by observer line alone", "lift_result": "UNIQUE_CONDITIONAL_LAMBDA_PLUS_ONE", "global_result": "reduction/descent open", "joint_result": "CONDITIONAL_PARTIAL"},
        {"category": "I3", "supplied_data": "ordered observer/ruler pair", "exact_result": "SO2 equivariance gives diag(-1,+1,lambda,lambda)", "depth_result": "not supplied by pair alone", "lift_result": "REAL_LAMBDA_FAMILY", "global_result": "reduction/descent open", "joint_result": "CONDITIONAL_FAMILY"},
        {"category": "I4", "supplied_data": "path signed depth complete frames", "exact_result": "typed path-groupoid comparison composes exactly", "depth_result": "SUPPLIED", "lift_result": "SUPPLIED_OR_FAMILY", "global_result": "path-labelled; endpoint collapse conditional", "joint_result": "EXACT_GIVEN_INPUTS_NOT_SELECTOR"},
    ]
    write_tsv("INPUT_CATEGORY_OUTCOMES.tsv", list(category_rows[0]), category_rows)

    character_rows = [
        {"object": "continuous_full_Lorentz_to_R_character", "result": "TRIVIAL_ONLY", "evidence": "perfect Lie algebra rank 6 character nullity 0", "scope": "connected full-frame comparison"},
        {"object": "noncollinear_boost_composition", "result": "ANGULAR_COMPONENT_FORCED", "evidence": "[K01,K02] proportional to J12 nonzero", "scope": "infinitesimal/BCH full-frame comparison"},
        {"object": "endpoint_additive_depth", "result": "POTENTIAL_DIFFERENCE_FAMILY", "evidence": "delta=f(q)-f(p)", "scope": "endpoint pair groupoid"},
        {"object": "homogeneous_isometry_invariant_endpoint_depth", "result": "TRIVIAL_UNDER_CONTINUOUS_POINCARE_INVARIANCE", "evidence": "translation additivity gives fixed covector; Lorentz fixed-covector nullity 0", "scope": "flat homogeneous metric-only control"},
        {"object": "metric_interval", "result": "NOT_SIGNED_ADDITIVE_GENERICALLY", "evidence": f"2+sqrt(3)-sqrt(15)={interval_defect}", "scope": "noncollinear timelike triple"},
        {"object": "stationary_Killing_norm_depth", "result": "DERIVED_BOUNDED_BASE_COCYCLE", "evidence": "delta_K=log(Q_p/Q_q)", "scope": "stationary observers intrinsic K line"},
    ]
    write_tsv("CHARACTER_AND_COCYCLE_RESULTS.tsv", list(character_rows[0]), character_rows)

    reduction_rows = [
        {"reduction": "NONE_FULL_SO13", "supplied_or_derived": "NONE", "generator_family": "a I only", "founded_pair_compatible": "NO", "residual": "pointwise non-scalar selector obstructed"},
        {"reduction": "OBSERVER_LINE_SO3", "supplied_or_derived": "SUPPLIED_OR_BRANCH_DERIVED", "generator_family": "diag(-1,a,a,a)", "founded_pair_compatible": "YES_ONLY_a_PLUS_ONE", "residual": "depth and global observer congruence"},
        {"reduction": "RULER_LINE_SO12", "supplied_or_derived": "SUPPLIED_OR_BRANCH_DERIVED", "generator_family": "diag(a,+1,a,a)", "founded_pair_compatible": "YES_ONLY_a_MINUS_ONE", "residual": "clock depth and global ruler reduction"},
        {"reduction": "ORDERED_PAIR_SO2", "supplied_or_derived": "SUPPLIED_OR_BRANCH_DERIVED", "generator_family": "diag(-1,+1,lambda,lambda)", "founded_pair_compatible": "YES_ALL_REAL_LAMBDA", "residual": "lambda depth path and global descent"},
        {"reduction": "FULL_PATH_GROUPOID", "supplied_or_derived": "PATH_DEPTH_FRAMES_SUPPLIED", "generator_family": "transported conjugacy family", "founded_pair_compatible": "YES_CONDITIONAL", "residual": "physical semantics and endpoint collapse"},
    ]
    write_tsv("REDUCED_STRUCTURE_ATLAS.tsv", list(reduction_rows[0]), reduction_rows)

    escape_rows = [
        {"route": "E01", "candidate_escape": "base-dependent natural scalar or one-form", "blocked_by_current_theorem": "NO", "current_grade": "OPEN_FAMILY_NOT_SELECTED", "required_datum": "metric-derived dimensionless potential/one-form and physical meaning"},
        {"route": "E02", "candidate_escape": "stationary intrinsic Killing norm", "blocked_by_current_theorem": "NO", "current_grade": "DERIVED_BOUNDED", "required_datum": "selected stationary branch and arbitrary-observer extension"},
        {"route": "E03", "candidate_escape": "observer-line SO3 reduction", "blocked_by_current_theorem": "NO", "current_grade": "UNIQUE_CONDITIONAL_LAMBDA_PLUS_ONE", "required_datum": "supplied or metric-derived observer congruence plus depth/global descent"},
        {"route": "E04", "candidate_escape": "ordered pair SO2 reduction", "blocked_by_current_theorem": "NO", "current_grade": "CONDITIONAL_REAL_LAMBDA_FAMILY", "required_datum": "pair section lambda depth and descent"},
        {"route": "E05", "candidate_escape": "path-labelled nonabelian comparison", "blocked_by_current_theorem": "NO", "current_grade": "EXACT_GIVEN_INPUTS", "required_datum": "physical path/groupoid semantics and signed cocycle"},
        {"route": "E06", "candidate_escape": "set-valued selector at symmetry/tie strata", "blocked_by_current_theorem": "NO", "current_grade": "OPEN_NOT_SINGLE_VALUED", "required_datum": "physical ontology and transition law"},
        {"route": "E07", "candidate_escape": "higher-jet or nonlocal whole-solution natural construction", "blocked_by_current_theorem": "NO", "current_grade": "UNCLASSIFIED", "required_datum": "explicit operation and all theorem gates"},
    ]
    write_tsv("ESCAPE_ROUTE_LEDGER.tsv", list(escape_rows[0]), escape_rows)

    result = {
        "schema": "udt-metric-natural-joint-selector-nogo-1.0",
        "source_blobs_replayed": source_count,
        "lorentz_bracket_span_rank": bracket_span_rank,
        "continuous_real_character_dimension": character_nullity,
        "full_isotropy_fixed_vector_dimension": 4 - fixed_vector_rank,
        "full_isotropy_fixed_covector_dimension": 4 - fixed_covector_rank,
        "full_lorentz_commutant_dimension": full_commutant_nullity,
        "observer_line_family_dimension": observer_nullity,
        "ordered_pair_family_dimension": pair_nullity,
        "ruler_line_family_dimension": ruler_nullity,
        "observer_line_founded_extension": str(observer_plus_one),
        "ruler_line_founded_extension": str(ruler_minus_one),
        "noncollinear_angular_commutator": True,
        "endpoint_cocycle_family": True,
        "invariant_interval_nonadditive": True,
        "finite_reduced_generators_integrate": True,
        "universal_pointwise_metric_only_non_scalar_lift": "NO_GO",
        "universal_frame_only_nontrivial_additive_depth": "NO_GO",
        "universal_higher_jet_nonlocal_or_base_dependent_joint": "NOT_CLASSIFIED",
        "primary_outcome": "NO_GO_PREMISES_INSUFFICIENT_STOP",
        "secondary_exact_result": "FRAME_ONLY_AND_POINTWISE_METRIC_ONLY_NO_GO;_REDUCED_GROUPOID_ROUTE_REQUIRED",
        "verification_grade": "PENDING_INDEPENDENT_REPLAY",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "gpu_used": False,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
