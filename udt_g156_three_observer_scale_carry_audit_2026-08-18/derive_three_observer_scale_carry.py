#!/usr/bin/env python3
"""Exact symbolic derivation for the G156 common-scale carrier/carry audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "b42c771d"
QUALIFIED_LANDING = (
    "PAIR_METRIC_CANONICALLY_SUPPLIES_POSITIVE_HALF_DENSITY_SECTION__"
    "ANY_SUPPLIED_TYPED_CARRY_INDUCES_GAUGE_INVARIANT_LOG_DETERMINANT_CHARACTER__"
    "FULL_CLOSURE_IMPLIES_BUT_IS_NOT_IMPLIED_BY_SCALE_CLOSURE__"
    "OWNED_CHART_OVERLAP_AND_LEVI_CIVITA_CARRIES_ARE_SCALE_FLAT__"
    "ARBITRARY_SUPPLIED_NONISOMETRIC_CARRIES_NEED_NOT_BE_FLAT__"
    "NO_METRIC_OWNED_CROSS_QUERY_CARRY_OR_KAPPA_HISTORY"
)


def read_manifest() -> list[dict[str, str]]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 19
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 20)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]


def exact_checks() -> dict[str, object]:
    checks: list[str] = []
    eta = sp.diag(-1, 1)

    # 1. A regular calibrated pair metric owns its positive metric half-density.
    T, L, beta = sp.symbols("T L beta", positive=True, real=True)
    R = sp.Matrix([[T, T * beta], [0, L]])
    h = sp.simplify(R.T * eta * R)
    assert sp.simplify(h.det() + T**2 * L**2) == 0
    checks.append("pair_metric_half_density_coefficient_is_sqrt_TL")

    # Under a positive-orientation coordinate pullback h' = J^T h J,
    # (-det h') = det(J)^2 (-det h). Positivity gives
    # (-det h')^(1/4) = det(J)^(1/2) (-det h)^(1/4), exactly the
    # transformation of a positive half-density coefficient.
    a, b, c, d = sp.symbols("a b c d", real=True)
    J = sp.Matrix([[a, b], [c, d]])
    hp = sp.simplify(J.T * h * J)
    assert sp.simplify(-hp.det() - J.det() ** 2 * (-h.det())) == 0
    checks.append("positive_half_density_coordinate_covariance")

    # 2. Fully typed total comparison and its determinant/common-scale character.
    TA, LA, bA, TB, LB, bB = sp.symbols(
        "TA LA bA TB LB bB", positive=True, real=True
    )
    m0, m1, mn = sp.symbols("m0 m1 mn", positive=True, real=True)
    RA = sp.Matrix([[TA, TA * bA], [0, LA]])
    RB = sp.Matrix([[TB, TB * bB], [0, LB]])
    M = sp.Matrix([[m0, mn], [0, m1]])
    C = sp.simplify(RB * M * RA.inv())
    det_formula = sp.simplify(C.det() - (TB * LB * m0 * m1) / (TA * LA))
    assert det_formula == 0
    checks.append("total_scale_character_endpoint_plus_carry_formula")

    # The same scalar is the factor comparing pulled-back metric half-densities:
    # exp(2 sigma) = det C = exp(2(kB-kA)) det M.
    half_density_ratio_squared = sp.simplify((TB * LB * M.det()) / (TA * LA))
    assert sp.simplify(half_density_ratio_squared - C.det()) == 0
    checks.append("determinant_character_equals_half_density_carry_squared")

    # 3. Independent endpoint carrier gauges cancel from the total comparison.
    pA0, pA1, pAn, pB0, pB1, pBn = sp.symbols(
        "pA0 pA1 pAn pB0 pB1 pBn", positive=True, real=True
    )
    PA = sp.Matrix([[pA0, pAn], [0, pA1]])
    PB = sp.Matrix([[pB0, pBn], [0, pB1]])
    RAp = RA * PA
    RBp = RB * PB
    Mp = sp.simplify(PB.inv() * M * PA)
    Cp = sp.simplify(RBp * Mp * RAp.inv())
    assert sp.simplify(Cp - C) == sp.zeros(2)
    checks.append("endpoint_gauge_invariance_of_total_scale_carry")

    # 4. Composition and the exact three-observer determinant defect.
    rA0, rA1, rB0, rB1, rC0, rC1 = sp.symbols(
        "rA0 rA1 rB0 rB1 rC0 rC1", positive=True, real=True
    )
    RA0 = sp.diag(rA0, rA1)
    RB0 = sp.diag(rB0, rB1)
    RC0 = sp.diag(rC0, rC1)
    x0, x1, y0, y1, z0, z1 = sp.symbols(
        "x0 x1 y0 y1 z0 z1", positive=True, real=True
    )
    MBA = sp.diag(x0, x1)
    MCB = sp.diag(y0, y1)
    MCA = sp.diag(z0, z1)
    CBA = sp.simplify(RB0 * MBA * RA0.inv())
    CCB = sp.simplify(RC0 * MCB * RB0.inv())
    CCA = sp.simplify(RC0 * MCA * RA0.inv())
    defect_ratio = sp.simplify(CCB.det() * CBA.det() / CCA.det())
    expected_defect_ratio = sp.simplify(MCB.det() * MBA.det() / MCA.det())
    assert sp.simplify(defect_ratio - expected_defect_ratio) == 0
    checks.append("three_observer_scale_defect_cancels_endpoint_kappa")

    composed = sp.simplify(CCB * CBA)
    CCA_closed = sp.simplify(RC0 * (MCB * MBA) * RA0.inv())
    assert sp.simplify(composed - CCA_closed) == sp.zeros(2)
    assert sp.simplify(
        CCB.det() * CBA.det() / CCA_closed.det() - 1
    ) == 0
    checks.append("full_carry_closure_implies_zero_scale_defect")

    # 5. The converse fails: determinant closure sees only GL+(2)/SL(2).
    I = sp.eye(2)
    shear = sp.Matrix([[1, 1], [0, 1]])
    assert shear.det() == 1 and shear != I
    scale_defect_for_shear = sp.simplify(I.det() * I.det() / shear.det())
    assert scale_defect_for_shear == 1 and I * I != shear
    checks.append("zero_scale_defect_does_not_imply_full_carry_closure")

    # 6. One supplied query chart owns an endpoint-exact/flat scale carry.
    JA = sp.Matrix([[2, 1], [0, 3]])
    JB = sp.Matrix([[5, 2], [0, 7]])
    JC = sp.Matrix([[11, 3], [0, 13]])
    M_BA_chart = JB * JA.inv()
    M_CB_chart = JC * JB.inv()
    M_CA_chart = JC * JA.inv()
    assert sp.simplify(M_CB_chart * M_BA_chart - M_CA_chart) == sp.zeros(2)
    assert sp.simplify(
        M_CB_chart.det() * M_BA_chart.det() / M_CA_chart.det() - 1
    ) == 0
    checks.append("single_query_chart_scale_carry_is_endpoint_exact")

    # 7. Genuine same-event overlap and metric-compatible transport are
    # isometries, hence preserve metric volume and have zero scale character.
    boost = sp.Matrix([[sp.Rational(5, 4), sp.Rational(3, 4)],
                       [sp.Rational(3, 4), sp.Rational(5, 4)]])
    assert sp.simplify(boost.T * eta * boost - eta) == sp.zeros(2)
    assert boost.det() == 1
    checks.append("lorentz_isometry_has_zero_metric_scale_character")

    # On the positive upper-triangular overlap gauge, the only oriented
    # Lorentz isometry is the identity.
    aa, nn, dd = sp.symbols("aa nn dd", positive=True, real=True)
    U = sp.Matrix([[aa, nn], [0, dd]])
    residual = sp.simplify(U.T * eta * U - eta)
    # residual[0,0]=1-aa^2=0 with aa>0 => aa=1;
    # residual[0,1]=-aa*nn=0 => nn=0; residual[1,1]=dd^2-1 => dd=1.
    assert residual[0, 0] == 1 - aa**2
    assert residual[0, 1] == -aa * nn
    assert residual[1, 1] == dd**2 - nn**2 - 1
    checks.append("positive_triangular_genuine_overlap_is_identity")

    # 8. Query-supplied nonisometric carries can have a nonzero determinant
    # triangle defect; without a path/loop functor this is not holonomy.
    M_BA_w = sp.eye(2)
    M_CB_w = sp.eye(2)
    M_CA_w = sp.diag(2, 1)
    nonzero_defect_ratio = sp.simplify(
        M_CB_w.det() * M_BA_w.det() / M_CA_w.det()
    )
    assert nonzero_defect_ratio == sp.Rational(1, 2)
    checks.append("supplied_nonisometric_carry_can_have_determinant_triangle_defect")

    assert len(checks) == 12
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "half_density_line": "|Lambda^2 V*|^(1/2)",
        "half_density_positive_ray": "(|Lambda^2 V*|^(1/2))_{>0}",
        "half_density_section": "ell_h=(-det h)^(1/4)|dy0 wedge dy1|^(1/2)",
        "scale_character": "sigma_BA=1/2 log|det C_BA|",
        "scale_character_split": "kappa_B-kappa_A+1/2 log|det M_BA|",
        "three_observer_defect": "Omega_sc=1/2 log|det(M_CB M_BA M_CA^-1)|",
        "scale_quotient_kernel": "B+(2) intersect SL(2) in the declared triangular arena",
        "nonzero_defect_ratio_witness": str(nonzero_defect_ratio),
    }


def main() -> None:
    manifest = read_manifest()
    verify_manifest(manifest)
    result = {
        "status": "PASS",
        "landing": QUALIFIED_LANDING,
        "registered_outcome_class": "CONDITIONAL_FLAT_SCALE_CARRY",
        "source_count": len(manifest),
        "source_snapshot": SOURCE_SNAPSHOT,
        "metric_selects_cross_query_nonisometric_carry": False,
        "metric_selects_kappa_history": False,
        **exact_checks(),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
