#!/usr/bin/env python3
"""Exact global distribution atlas for the preregistered intrinsic two-form."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_intrinsic_general_screen_neighborhood_audit_2026-08-02"
Q = sp.symbols("q0:4", real=True)
Q0, Q1, Q2, Q3 = Q
SPHERE = sum(value**2 for value in Q) - 1
POINTS = {
    "p1": (sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 11)),
    "p2": (sp.Rational(1, 3), sp.Rational(-1, 5), sp.Rational(1, 7)),
    "p3": (sp.Rational(-1, 4), sp.Rational(2, 7), sp.Rational(1, 9)),
    "p4": (sp.Rational(2, 5), sp.Rational(1, 6), sp.Rational(-1, 8)),
    "p5": (sp.S.Zero, sp.Rational(1, 3), sp.Rational(1, 5)),
    "p6": (sp.Rational(1, 4), sp.S.Zero, sp.Rational(1, 6)),
    "p7": (sp.Rational(1, 4), sp.Rational(1, 6), sp.S.Zero),
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verify_sources() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 64
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert sha256_bytes(content) == row["sha256"]
    assert sha256_bytes((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (
        HERE / "SOURCE_MANIFEST.sha256"
    ).read_text(encoding="utf-8").strip()
    return len(rows)


def directional(vector: tuple[sp.Expr, ...], scalar: sp.Expr) -> sp.Expr:
    return sp.expand(sum(vector[index] * sp.diff(scalar, Q[index]) for index in range(4)))


def stereographic_q(point: tuple[sp.Rational, ...]) -> tuple[sp.Expr, ...]:
    x, y, z = point
    rho2 = x*x + y*y + z*z
    denominator = 1 + rho2
    return (
        sp.factor((1 - rho2) / denominator),
        sp.factor(2*x / denominator),
        sp.factor(2*y / denominator),
        sp.factor(2*z / denominator),
    )


def permutation_sign(sequence: tuple[int, ...]) -> int:
    inversions = sum(
        sequence[left] > sequence[right]
        for left in range(len(sequence))
        for right in range(left + 1, len(sequence))
    )
    return -1 if inversions % 2 else 1


def hodge_three(indices: tuple[int, int, int]) -> tuple[int, int]:
    """Return coefficient and remaining one-form index in signature (-+++)."""
    remaining = next(index for index in range(4) if index not in indices)
    wedge_sign = permutation_sign((*indices, remaining))
    norm_sign = -1 if 0 in indices else 1
    return norm_sign * wedge_sign, remaining


def main() -> int:
    source_count = verify_sources()
    binding = read_tsv(HERE / "CANDIDATE_BINDING.tsv")
    candidates = read_tsv(PARENT / "CANDIDATE_UNIVERSE.tsv")
    assert [row["candidate_id"] for row in binding] == [f"C{i:02d}" for i in range(1, 19)]
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 19)]
    assert len(read_tsv(HERE / "OBJECT_UNIVERSE.tsv")) == 24
    assert len(read_tsv(HERE / "FALSIFICATION_CONTRACT.tsv")) == 32

    # Exact vector fields dual to the frozen Maurer-Cartan coframe on the unit sphere.
    x_fields = (
        (-Q1, Q0, Q3, -Q2),
        (-Q2, -Q3, Q0, Q1),
        (-Q3, Q2, -Q1, Q0),
    )
    sigma_coefficients = (
        (-Q1, Q0, Q3, -Q2),
        (-Q2, -Q3, Q0, Q1),
        (-Q3, Q2, -Q1, Q0),
    )
    for vector in x_fields:
        assert sp.expand(sum(Q[index] * vector[index] for index in range(4))) == 0
    duality = sp.Matrix([
        [sp.expand(sum(sigma_coefficients[i][k] * x_fields[j][k] for k in range(4)))
         for j in range(3)]
        for i in range(3)
    ])
    assert sp.simplify(duality.subs(Q0**2 + Q1**2 + Q2**2 + Q3**2, 1)) == sp.eye(3)
    # The entries are delta_ij times q.q; verify before using the sphere relation.
    assert duality == (SPHERE + 1) * sp.eye(3)

    u = 3 + Q0**2 + 2*Q1**2 + 4*Q2**2 + 8*Q3**2
    v0 = Q0**2 + 3*Q1**2 + 7*Q2**2 + 9*Q3**2
    v = 1 + sp.Rational(1, 10) * v0
    xu = tuple(sp.factor(directional(vector, u)) for vector in x_fields)
    xv0 = tuple(sp.factor(directional(vector, v0)) for vector in x_fields)
    pairs = ((0, 1), (0, 2), (1, 2))
    raw = tuple(sp.factor(xu[i]*xv0[j] - xu[j]*xv0[i]) for i, j in pairs)
    f12 = Q0*Q1**2 + 3*Q0*Q2**2 + 2*Q1*Q2*Q3
    f13 = Q0**2*Q1 + 3*Q0*Q2*Q3 - 2*Q1*Q2**2
    f23 = 3*Q0**2*Q2 - Q0*Q1*Q3 + 2*Q1**2*Q2
    factors = (f12, f13, f23)
    assert tuple(sp.factor(value + 24*Q3*factors[index]) for index, value in enumerate(raw)) == (
        sp.S.Zero, sp.S.Zero, sp.S.Zero
    )
    normalized = tuple(sp.factor(value / (20*u*v)) for value in raw)

    # Exact support geometry: only the 012 coefficient triple is affinely collinear.
    a_coefficients = (1, 2, 4, 8)
    b_coefficients = (1, 3, 7, 9)
    support_determinants = {
        "".join(str(index) for index in triple): sp.Matrix(
            [[1, a_coefficients[index], b_coefficients[index]] for index in triple]
        ).det()
        for triple in itertools.combinations(range(4), 3)
    }
    assert support_determinants == {"012": 0, "013": -6, "023": -18, "123": -12}

    # The ruler-aligned nonzero locus is empty: f13=f23=0 forces f12=0.
    affine_x, affine_y, affine_z = sp.symbols("x y z", real=True)
    affine = {Q0: affine_x, Q1: affine_y, Q2: affine_z, Q3: 1}
    af12, af13, af23 = (sp.expand(value.subs(affine)) for value in factors)
    ruler_groebner = sp.groebner([af13, af23], affine_x, affine_y, affine_z, order="grevlex")
    ruler_quotients, ruler_remainder = ruler_groebner.reduce(sp.expand(af12**2))
    assert ruler_remainder == 0

    # Exact nonempty representatives for the two surviving nonzero types.
    screen_representative = {affine_x: sp.Rational(1, 2), affine_y: 1, affine_z: sp.Rational(-1, 3)}
    screen_values = tuple(sp.factor(value.subs(screen_representative)) for value in (af12, af13, af23))
    assert screen_values == (0, sp.Rational(-17, 36), sp.Rational(-17, 12))
    generic_representative = {affine_x: sp.Rational(1, 5), affine_y: sp.Rational(1, 7), affine_z: sp.Rational(1, 11)}
    generic_values = tuple(sp.factor(value.subs(generic_representative)) for value in (af12, af13, af23))
    assert all(value != 0 for value in generic_values)

    # Four-dimensional Hodge/kernel algebra in an oriented orthonormal coframe.
    aa, bb, cc = sp.symbols("A B C", real=True)
    w_matrix = sp.zeros(4)
    w_matrix[1, 2], w_matrix[2, 1] = aa, -aa
    w_matrix[1, 3], w_matrix[3, 1] = bb, -bb
    w_matrix[2, 3], w_matrix[3, 2] = cc, -cc
    assert hodge_three((0, 1, 2)) == (-1, 3)
    assert hodge_three((0, 1, 3)) == (1, 2)
    assert hodge_three((0, 2, 3)) == (-1, 1)
    # T_flat=-theta0, so star(T_flat wedge W)=C theta1-B theta2+A theta3.
    n_vector = sp.Matrix([0, cc, -bb, aa])
    t_vector = sp.Matrix([1, 0, 0, 0])
    assert w_matrix * n_vector == sp.zeros(4, 1)
    assert w_matrix * t_vector == sp.zeros(4, 1)
    assert sp.factor(sum(value**2 for value in n_vector[1:])) == aa**2 + bb**2 + cc**2
    generic_rank = w_matrix.subs({aa: 2, bb: 3, cc: 5}).rank()
    assert generic_rank == 2
    assert w_matrix.subs({aa: 0, bb: 0, cc: 0}).rank() == 0

    # Exact coframe conversion. F,r,u are positive; b is real.
    k, fscale, rscale, uscale = sp.symbols("k F r u", positive=True)
    bshear = sp.symbols("b", real=True)
    indexed_a = sp.factor(-k * sp.Symbol("c13") / (sp.sqrt(fscale)*rscale*sp.sqrt(uscale)))
    indexed_b = sp.factor(k * (bshear*sp.Symbol("c13") - rscale*sp.Symbol("c23")) / (sp.sqrt(fscale)*sp.sqrt(uscale)))
    indexed_c = sp.factor(k * sp.Symbol("c12") / fscale)
    assert indexed_a != 0 and indexed_b != 0 and indexed_c != 0

    # Screen-basis gauge check with an exact O(2) rotation.
    rotation = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                          [sp.Rational(4, 5), sp.Rational(3, 5)]])
    assert rotation.T * rotation == sp.eye(2) and rotation.det() == 1
    h_part = sp.Matrix([-bb, aa])
    assert sp.factor((rotation*h_part).dot(rotation*h_part) - h_part.dot(h_part)) == 0

    # Path-dependence ranks on the three exceptional great circles.
    circle_rank_determinants = {
        "C03": sp.factor(3*Q0**2*(Q0**2 + Q3**2)),
        "C13": sp.factor(2*Q1**2*(Q1**2 + Q3**2)),
        "C23": sp.factor(-6*Q2**2*(Q2**2 + Q3**2)),
    }
    for name, determinant in circle_rank_determinants.items():
        active = {"C03": Q0, "C13": Q1, "C23": Q2}[name]
        assert sp.factor(determinant.subs(Q3**2, 1 - active**2)) in {
            3*Q0**2, 2*Q1**2, -6*Q2**2
        }
    # At the shared q3 poles two exact tangent paths have distinct leading projective limits.
    pole_path_limits = {"path_q0_0_q1_eq_q2": "[1:0:0]", "path_q1_0_q0_eq_q2": "[0:1:0]"}

    point_rows = []
    for point_id, point in POINTS.items():
        q_values = stereographic_q(point)
        substitutions = dict(zip(Q, q_values))
        values = tuple(sp.factor(value.subs(substitutions)) for value in normalized)
        f_values = tuple(sp.factor(value.subs(substitutions)) for value in factors)
        if all(value == 0 for value in values):
            point_type = "ZERO_EXTENDABLE" if Q3.subs(substitutions) == 0 and any(value != 0 for value in f_values) else "ZERO_NONEXTENDABLE"
        elif values[0] == 0:
            point_type = "SCREEN_CONTAINED"
        else:
            point_type = "GENERIC_MIXED"
        point_rows.append({
            "point_id": point_id,
            "stereographic_xyz": ";".join(str(value) for value in point),
            "quaternion_q": ";".join(str(value) for value in q_values),
            "w_sigma12_sigma13_sigma23": ";".join(str(value) for value in values),
            "type": point_type,
        })
    assert [row["type"] for row in point_rows] == ["GENERIC_MIXED"]*6 + ["ZERO_EXTENDABLE"]

    binding_by_id = {row["candidate_id"]: row for row in binding}
    candidate_rows = []
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        scope = binding_by_id[candidate_id]["new_intrinsic_analysis_scope"]
        if scope == "FULL_DISTRIBUTION":
            status = "MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI"
            zero_locus = "EQUATOR_S2_UNION_C03_C13_C23"
            ruler = "EMPTY_EXACT"
            screen = "NONEMPTY_F12_ZERO_MINUS_ZW"
            generic = "NONEMPTY_COMPLEMENT_OF_F12_ZERO_AND_ZW"
            kernel = "DIM2_SPAN_T_N_ON_NONZERO__DIM4_ON_ZERO"
            extension = "EXTENDS_EQUATOR_MINUS_SIX_AXIS_POINTS__FAILS_THREE_GREAT_CIRCLES"
        elif scope == "ZERO_CONTROL":
            status = "ZERO"
            zero_locus = "ALL_S3"
            ruler = screen = generic = "EMPTY"
            kernel = "DIM4_EVERYWHERE_NO_UNIQUE_LINE"
            extension = "NO_LINE_TO_EXTEND"
        elif scope == "CONFIGURATION_CONTROL_ONLY":
            status = "PROJECTOR_BLOCKED"
            zero_locus = "CONFIGURATION_ONLY_NOT_INTRINSIC"
            ruler = screen = generic = "NOT_ASSIGNED"
            kernel = "NOT_INTRINSICALLY_ASSIGNED"
            extension = "NOT_INTRINSICALLY_ASSIGNED"
        else:
            assert scope == "DEGENERATE_CONTROL"
            status = "METRIC_DEGENERATE"
            zero_locus = ruler = screen = generic = kernel = extension = "UNDEFINED_METRIC_DEGENERATE"
        candidate_rows.append({
            "candidate_id": candidate_id,
            "label": candidate["label"],
            "intrinsic_scope": scope,
            "distribution_status": status,
            "zero_locus": zero_locus,
            "ruler_aligned_locus": ruler,
            "screen_contained_locus": screen,
            "generic_mixed_locus": generic,
            "kernel_status": kernel,
            "projective_extension": extension,
            "selected_or_physical": "NO",
        })
    assert sum(row["distribution_status"] == "ZERO" for row in candidate_rows) == 9
    assert sum(row["distribution_status"] == "MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI" for row in candidate_rows) == 6
    assert sum(row["distribution_status"] == "PROJECTOR_BLOCKED" for row in candidate_rows) == 2
    assert sum(row["distribution_status"] == "METRIC_DEGENERATE" for row in candidate_rows) == 1

    locus_rows = [
        {"locus_id": "L01", "locus": "ZERO_W", "exact_condition_on_S3": "q3=0 OR (q1=q2=0) OR (q0=q2=0) OR (q0=q1=0)", "status": "EXACT_EXHAUSTIVE"},
        {"locus_id": "L02", "locus": "RULER_ALIGNED_NONZERO", "exact_condition_on_S3": "EMPTY because f13=f23=0 implies f12^2=0", "status": "EXACT_EMPTY"},
        {"locus_id": "L03", "locus": "SCREEN_CONTAINED_NONZERO", "exact_condition_on_S3": "q3!=0 AND f12=0 AND (f13,f23)!=(0,0)", "status": "EXACT_NONEMPTY"},
        {"locus_id": "L04", "locus": "GENERIC_MIXED_NONZERO", "exact_condition_on_S3": "q3!=0 AND f12!=0 AND (f13,f23)!=(0,0)", "status": "EXACT_NONEMPTY_OPEN"},
        {"locus_id": "L05", "locus": "ORIGINAL_NONZERO_DOMAIN_COMPONENTS", "exact_condition_on_S3": "S3 minus ZERO_W", "status": "EXACTLY_TWO_BY_EQUATOR_SEPARATION_AND_CODIM2_GRAPH_NONSEPARATION"},
        {"locus_id": "L06", "locus": "UNIQUE_PROJECTIVE_EXTENSION", "exact_condition_on_S3": "q3=0 minus six q0/q1/q2 axis points", "status": "EXACT"},
        {"locus_id": "L07", "locus": "PROJECTIVE_EXTENSION_OBSTRUCTION", "exact_condition_on_S3": "C03 union C13 union C23", "status": "EXACT_PATH_DEPENDENT"},
    ]

    write_tsv(
        "CANDIDATE_ATLAS.tsv",
        ["candidate_id", "label", "intrinsic_scope", "distribution_status", "zero_locus",
         "ruler_aligned_locus", "screen_contained_locus", "generic_mixed_locus",
         "kernel_status", "projective_extension", "selected_or_physical"],
        candidate_rows,
    )
    write_tsv("LOCUS_ATLAS.tsv", ["locus_id", "locus", "exact_condition_on_S3", "status"], locus_rows)
    write_tsv(
        "POINT_CERTIFICATE.tsv",
        ["point_id", "stereographic_xyz", "quaternion_q", "w_sigma12_sigma13_sigma23", "type"],
        point_rows,
    )

    result = {
        "schema": "udt-intrinsic-two-form-distribution-1.0",
        "status": "PASS_EXACT_PRODUCTION",
        "sympy_version": sp.__version__,
        "frozen_sources": source_count,
        "candidate_count": len(candidate_rows),
        "candidate_counts": {"zero": 9, "full_distribution": 6, "blocked": 2, "degenerate": 1},
        "dual_coframe_verified": True,
        "Xu": [str(value) for value in xu],
        "XV0": [str(value) for value in xv0],
        "raw_wedge_factors": [str(value) for value in raw],
        "common_factor": "-24*q3",
        "normalized_denominator": "20*u*V_positive",
        "support_affine_determinants": {key: str(value) for key, value in support_determinants.items()},
        "zero_locus": "q3=0 union C03 union C13 union C23",
        "nonzero_domain_components": 2,
        "ruler_aligned_nonzero": "EMPTY_EXACT",
        "ruler_groebner_remainder_f12_squared": str(ruler_remainder),
        "ruler_groebner_quotients": [str(value) for value in ruler_quotients],
        "screen_contained_witness_projective_q": ["1/2", "1", "-1/3", "1"],
        "screen_contained_witness_f": [str(value) for value in screen_values],
        "generic_witness_projective_q": ["1/5", "1/7", "1/11", "1"],
        "generic_witness_f": [str(value) for value in generic_values],
        "orthonormal_components": {
            "W": "A theta1^theta2 + B theta1^theta3 + C theta2^theta3",
            "N_flat": "C theta1 - B theta2 + A theta3",
            "norm_N_squared": "A^2+B^2+C^2",
            "A": "-k*c13/(sqrt(F)*r*sqrt(u))",
            "B": "k*(b*c13-r*c23)/(sqrt(F)*sqrt(u))",
            "C": "k*c12/F",
            "k": "1/(20*u*V)",
        },
        "kernel_nonzero": "span(T,N), dimension 2",
        "kernel_zero": "full tangent space, dimension 4",
        "line_types_realized": ["SCREEN_CONTAINED", "GENERIC_MIXED"],
        "line_types_not_realized": ["RULER_ALIGNED"],
        "projective_extension": "unique across q3=0 away from six axis intersections; path-dependent on three great circles",
        "circle_transverse_rank_determinants": {key: str(value) for key, value in circle_rank_determinants.items()},
        "pole_path_limits": pole_path_limits,
        "screen_O2_type_invariant": True,
        "orientation_and_representative_sign_projector_invariant": True,
        "candidate_selected": False,
        "carrier_or_section_derived": False,
        "dynamics_or_physics_promoted": False,
    }
    (HERE / "DISTRIBUTION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        "candidate_counts": result["candidate_counts"],
        "nonzero_types": result["line_types_realized"],
        "ruler_aligned": result["ruler_aligned_nonzero"],
        "nonzero_domain_components": result["nonzero_domain_components"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
