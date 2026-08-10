#!/usr/bin/env python3
"""Exact production derivation for carried/intrinsic middle-morphism ownership."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAMBDAS = [sp.Rational(-2), sp.Rational(-1), sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(2)]
ETA = sp.diag(-1, 1, 1, 1)
I4 = sp.eye(4)


def boost(i: int, j: int, ch: sp.Rational, sh: sp.Rational) -> sp.Matrix:
    out = sp.eye(4)
    out[i, i] = ch
    out[j, j] = ch
    out[i, j] = sh
    out[j, i] = sh
    return out


def rotation(i: int, j: int) -> sp.Matrix:
    """Exact positive quarter turn in a spacelike coordinate plane."""
    out = sp.eye(4)
    out[i, i] = 0
    out[j, j] = 0
    out[i, j] = -1
    out[j, i] = 1
    return out


def lorentz_basis() -> list[sp.Matrix]:
    basis = []
    for j in (1, 2, 3):
        mat = sp.zeros(4)
        mat[0, j] = 1
        mat[j, 0] = 1
        basis.append(mat)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        mat = sp.zeros(4)
        mat[i, j] = 1
        mat[j, i] = -1
        basis.append(mat)
    assert all(mat.T * ETA + ETA * mat == sp.zeros(4) for mat in basis)
    return basis


def stacked_rank(mats: list[sp.Matrix]) -> int:
    columns = [sp.Matrix(mat).reshape(16, 1) for mat in mats]
    return int(sp.Matrix.hstack(*columns).rank())


def centralizer_dimension(objects: list[sp.Matrix]) -> int:
    basis = lorentz_basis()
    columns = []
    for generator in basis:
        pieces = [(generator * obj - obj * generator).reshape(16, 1) for obj in objects]
        columns.append(sp.Matrix.vstack(*pieces))
    return len(basis) - int(sp.Matrix.hstack(*columns).rank())


def is_lorentz(mat: sp.Matrix) -> bool:
    return sp.simplify(mat.T * ETA * mat - ETA) == sp.zeros(4)


def max_abs_exact(mat: sp.Matrix) -> sp.Expr:
    vals = [abs(sp.simplify(value)) for value in mat]
    return max(vals, key=lambda value: float(value))


def read_prior_path_counts() -> dict[str, int | float]:
    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOCAL_NABLA_X.tsv").open() as handle:
        local = list(csv.DictReader(handle, delimiter="\t"))
    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv").open() as handle:
        loops = list(csv.DictReader(handle, delimiter="\t"))
    return {
        "local_rows": len(local),
        "local_nonzero_clock_ruler": sum(float(row["clock_ruler"]) > 0 for row in local),
        "loop_rows": len(loops),
        "loop_nonidentity": sum(float(row["nonidentity_max"]) > 1e-10 for row in loops),
        "loop_ordinary_closure_failures": sum(float(row["ordinary_closure_residual"]) > 1e-10 for row in loops),
        "loop_composition_passes": sum(float(row["composition_residual"]) < 1e-10 for row in loops),
        "min_ordinary_closure_residual": min(float(row["ordinary_closure_residual"]) for row in loops),
    }


def main() -> None:
    pu = sp.diag(1, 0, 0, 0)
    pn = sp.diag(0, 1, 0, 0)
    hs = sp.diag(0, 0, 1, 1)

    # A rational proper-orthochronous boost gives one exact carried/intrinsic mismatch witness.
    b01 = boost(0, 1, sp.Rational(5, 4), sp.Rational(3, 4))
    m0 = b01.inv()
    r23 = rotation(2, 3)
    m1 = r23 * m0
    assert is_lorentz(b01) and is_lorentz(m0) and is_lorentz(r23) and is_lorentz(m1)
    assert b01.det() == m0.det() == r23.det() == m1.det() == 1
    assert b01[0, 0] > 0 and m0[0, 0] > 0

    rows = []
    for lam in LAMBDAS:
        x_int = -pu + pn + lam * hs
        x_car = sp.simplify(b01 * x_int * b01.inv())
        pc_u = sp.simplify(b01 * pu * b01.inv())
        pc_n = sp.simplify(b01 * pn * b01.inv())
        pc_h = sp.simplify(b01 * hs * b01.inv())

        assert x_car != x_int
        for morphism in (m0, m1):
            assert sp.simplify(morphism * x_car * morphism.inv() - x_int) == sp.zeros(4)
            assert sp.simplify(morphism * pc_u * morphism.inv() - pu) == sp.zeros(4)
            assert sp.simplify(morphism * pc_n * morphism.inv() - pn) == sp.zeros(4)
            assert sp.simplify(morphism * pc_h * morphism.inv() - hs) == sp.zeros(4)
        assert m0 != m1

        grading_dim = centralizer_dimension([x_int])
        flag_dim = centralizer_dimension([pu, pn, hs])
        expected = 3 if lam in (-1, 1) else 1
        assert grading_dim == expected
        assert flag_dim == 1
        rows.append(
            {
                "branch_id": f"C{LAMBDAS.index(lam) + 1:02d}",
                "lambda": str(lam),
                "grading_stabilizer_dimension": grading_dim,
                "complete_projector_stabilizer_dimension": flag_dim,
                "identity_reset": "REFUTED_ON_NONPARALLEL_PATHS",
                "alignment_existence": "DERIVED_LOCAL_REGULAR_SAME_LAMBDA",
                "alignment_uniqueness": "REFUTED_CONTINUOUS_SO2_TORSOR",
                "owned_relative_object": "PATH_LABELLED_SO2_ALIGNMENT_BITORSOR_WITH_BALANCED_COMPOSITION",
                "representative_morphism": "NOT_SELECTED_AND_NOT_NEEDED_FOR_PROJECTOR_COMPOSITION",
            }
        )

    # The screen stabilizer is not normal, so its double-coset space has no inherited group law.
    b02 = boost(0, 2, sp.Rational(5, 4), sp.Rational(3, 4))
    conjugated_screen_rotation = sp.simplify(b02 * r23 * b02.inv())
    nonnormal_witness = any(
        sp.simplify(conjugated_screen_rotation * proj - proj * conjugated_screen_rotation) != sp.zeros(4)
        for proj in (pu, pn, hs)
    )
    assert nonnormal_witness

    # Exact obstruction to a Lorentz-equivariant section G/H -> G at the base flag.
    screen_stabilizes_base = all(sp.simplify(r23 * proj - proj * r23) == sp.zeros(4) for proj in (pu, pn, hs))
    screen_is_nontrivial = r23 != I4
    equivariant_section_obstructed = screen_stabilizes_base and screen_is_nontrivial
    assert equivariant_section_obstructed

    # Gauge-related representatives change while the double coset does not.
    relative_representative = b01
    gauge_changed_representative = sp.simplify(r23.inv() * relative_representative)
    assert relative_representative != gauge_changed_representative

    # Three-reduction control: balanced bitorsor composition is representative-independent.
    g1 = I4
    g2 = b01
    g3 = b02
    h_a = r23
    h_b = r23**2
    m12 = sp.simplify(g2 * h_a * g1.inv())
    m23 = sp.simplify(g3 * h_b * g2.inv())
    m13 = sp.simplify(m23 * m12)
    middle_stabilizer = sp.simplify(g2 * r23 * g2.inv())
    m23_gauge = sp.simplify(m23 * middle_stabilizer)
    m12_gauge = sp.simplify(middle_stabilizer.inv() * m12)
    assert sp.simplify(m23_gauge * m12_gauge - m13) == sp.zeros(4)
    for projector in (pu, pn, hs):
        reduction_1 = sp.simplify(g1 * projector * g1.inv())
        reduction_3 = sp.simplify(g3 * projector * g3.inv())
        assert sp.simplify(m13 * reduction_1 * m13.inv() - reduction_3) == sp.zeros(4)

    path_counts = read_prior_path_counts()
    assert path_counts["local_rows"] == path_counts["local_nonzero_clock_ruler"] == 18
    assert path_counts["loop_rows"] == path_counts["loop_nonidentity"] == 36
    assert path_counts["loop_rows"] == path_counts["loop_ordinary_closure_failures"] == 36
    assert path_counts["loop_rows"] == path_counts["loop_composition_passes"] == 36

    atlas_path = HERE / "MIDDLE_MORPHISM_ATLAS.tsv"
    with atlas_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "primary_landing": "GAUGE_GROUPOID_ALREADY_SUFFICIENT_FOR_PROJECTOR_ALIGNMENT__CALIBRATION_DESCENT_OPEN",
        "scope": "C01-C06 regular twisted-S3 configurations; supplied regular paths",
        "lambda_rows": len(rows),
        "grading_stabilizer_dimensions": {row["lambda"]: row["grading_stabilizer_dimension"] for row in rows},
        "complete_projector_stabilizer_dimensions": {
            row["lambda"]: row["complete_projector_stabilizer_dimension"] for row in rows
        },
        "two_distinct_exact_projector_alignments": True,
        "alignment_difference_max_abs": str(max_abs_exact(m1 - m0)),
        "screen_stabilizer_nontrivial": screen_is_nontrivial,
        "screen_stabilizer_nonnormal": nonnormal_witness,
        "left_equivariant_adapted_frame_section_obstructed": equivariant_section_obstructed,
        "double_coset_is_compositional_group": False,
        "balanced_bitorsor_composition_exact": True,
        "balanced_composition_representative_independent": True,
        "path_counts": path_counts,
        "owned": [
            "intrinsic endpoint projector triple",
            "path-carried endpoint projector triple",
            "their path-labelled relative orbit/double-coset shadow",
            "the full nonempty SO(2)-bitorsor of regular projector alignments",
            "balanced representative-free composition of alignment bitorsors",
        ],
        "open": [
            "one canonical middle-morphism representative (not needed for projector composition)",
            "one coherent global section/trivialization",
            "one physical pair atlas or pair-relation functor",
            "universal mixed scalar reciprocal law and c_eff",
        ],
        "conditional": [
            "a common supplied pair atlas can provide an overlap representative",
            "a supplied full screen frame can choose a representative but adds gauge data",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
