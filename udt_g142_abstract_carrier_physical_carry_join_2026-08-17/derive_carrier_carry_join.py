#!/usr/bin/env python3
"""Exact production algebra for G142."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(value) == 0 for value in matrix)


def main() -> None:
    checks: list[str] = []

    TA, LA, TB, LB, TC, LC = sp.symbols("T_A L_A T_B L_B T_C L_C", positive=True)
    rA, rB, rC = sp.symbols("r_A r_B r_C", real=True)
    aBA, dBA, aCB, dCB, aCA, dCA = sp.symbols(
        "a_BA d_BA a_CB d_CB a_CA d_CA", positive=True
    )
    mBA, mCB, mCA = sp.symbols("m_BA m_CB m_CA", real=True)

    def upper(a, u, d):
        return sp.Matrix([[a, u], [0, d]])

    RA, RB, RC = upper(TA, rA, LA), upper(TB, rB, LB), upper(TC, rC, LC)
    MBA, MCB = upper(aBA, mBA, dBA), upper(aCB, mCB, dCB)
    MCA_composed = MCB * MBA
    MCA_independent = upper(aCA, mCA, dCA)

    def total(R_target, M_target_source, R_source):
        return R_target * M_target_source * R_source.inv()

    CBA = total(RB, MBA, RA)
    CCB = total(RC, MCB, RB)
    CCA_composed = total(RC, MCA_composed, RA)
    require(zero(CCB * CBA - CCA_composed), "total_transition_composes_when_carry_composes", checks)

    # The direct carry is independent here: this is the non-tautological converse/obstruction test.
    CCA_independent = total(RC, MCA_independent, RA)
    total_obstruction = CCB * CBA - CCA_independent
    carry_obstruction = MCB * MBA - MCA_independent
    require(zero(RC.inv() * total_obstruction * RA - carry_obstruction),
            "composition_obstruction_exactly_carry_obstruction", checks)
    red_subs = {
        TA: 2, LA: 3, TB: 5, LB: 7, TC: 11, LC: 13,
        rA: sp.Rational(1, 3), rB: sp.Rational(-2, 5), rC: sp.Rational(3, 7),
        aBA: sp.Rational(3, 2), dBA: sp.Rational(4, 3), mBA: sp.Rational(1, 9),
        aCB: sp.Rational(5, 3), dCB: sp.Rational(7, 4), mCB: sp.Rational(-1, 6),
        aCA: sp.Rational(9, 8), dCA: sp.Rational(10, 9), mCA: sp.Rational(2, 11),
    }
    require(not zero(total_obstruction.subs(red_subs)) and not zero(carry_obstruction.subs(red_subs)),
            "off_closure_red_case_has_nonzero_matched_obstructions", checks)

    MAB = MBA.inv()
    CAB = total(RA, MAB, RB)
    require(zero(CAB * CBA - sp.eye(2)), "total_transition_reverses", checks)
    require(CBA[1, 0] == CCB[1, 0] == CCA_composed[1, 0] == CCA_independent[1, 0] == 0,
            "flag_preserving_total_is_upper_triangular", checks)

    # Independent endpoint carrier gauges.
    pA0, pA1, pB0, pB1 = sp.symbols("p_A0 p_A1 p_B0 p_B1", positive=True)
    pAu, pBu = sp.symbols("p_Au p_Bu", real=True)
    PA, PB = upper(pA0, pAu, pA1), upper(pB0, pBu, pB1)
    RAp, RBp = RA * PA, RB * PB
    MBAp = PB.inv() * MBA * PA
    CBAp = total(RBp, MBAp, RAp)
    require(zero(CBAp - CBA), "total_transition_endpoint_gauge_invariant", checks)
    require(not zero(RBp - RB) and not zero(RAp - RA),
            "endpoint_factors_individually_gauge_variant", checks)

    # Work with positive diagonal ratios rather than branch-sensitive symbolic logarithms.
    grading_CBA = sp.cancel(CBA[1, 1] / CBA[0, 0])
    endpoint_ratio = sp.cancel((LB / TB) / (LA / TA))
    carry_ratio = sp.cancel(dBA / aBA)
    require(sp.cancel(grading_CBA - endpoint_ratio * carry_ratio) == 0,
            "total_grading_is_endpoint_times_carry_ratio", checks)
    require(sp.cancel((CCB * CBA)[1, 1] / (CCB * CBA)[0, 0]
                      - (CCB[1, 1] / CCB[0, 0]) * grading_CBA) == 0,
            "grading_character_composes", checks)
    require(sp.cancel((CAB[1, 1] / CAB[0, 0]) * grading_CBA - 1) == 0,
            "grading_character_reverses", checks)
    require(sp.cancel(CBA.det() - (TB * LB) / (TA * LA) * MBA.det()) == 0,
            "common_scale_character_separate", checks)

    # Carry grading alone is presentation-dependent; only the total grading is invariant.
    carry_ratio_prime = sp.cancel(MBAp[1, 1] / MBAp[0, 0])
    gauge_shifted_carry_ratio = sp.cancel(carry_ratio * (pA1 / pA0) / (pB1 / pB0))
    require(sp.cancel(carry_ratio_prime - gauge_shifted_carry_ratio) == 0,
            "carry_grading_gauge_shift_exact", checks)

    # In a fixed matched presentation, reciprocal-neutral carry recovers G141's scalar grading.
    s = sp.symbols("s", positive=True)
    n = sp.symbols("n", real=True, nonzero=True)
    Mneutral = upper(s, n, s)
    Cneutral = total(RB, Mneutral, RA)
    require(sp.cancel(Cneutral[1, 1] / Cneutral[0, 0] - endpoint_ratio) == 0,
            "G141_scalar_grading_recovered_for_neutral_carry_in_fixed_matched_presentation", checks)
    require(Mneutral != sp.eye(2), "neutral_carry_need_not_be_identity", checks)
    require(Mneutral[0, 1] != 0, "neutral_carry_retains_unipotent_shift", checks)
    require(sp.cancel(Mneutral.det() - s**2) == 0,
            "neutral_carry_may_retain_common_scale", checks)

    # Pure reciprocal representation and exact same-endpoint nonselection countermodel.
    z = sp.symbols("z", positive=True)
    D = sp.diag(1 / z, z)
    require(sp.cancel(D[1, 1] / D[0, 0] - z**2) == 0,
            "founded_pure_reciprocal_matrix_retained", checks)
    I = sp.eye(2)
    C_identity = total(I, I, I)
    C_depth = total(I, sp.diag(sp.Rational(1, 2), 2), I)
    require(C_identity[1, 1] / C_identity[0, 0] == 1,
            "same_endpoint_identity_carry_zero_depth", checks)
    require(C_depth[1, 1] / C_depth[0, 0] == 4,
            "same_endpoint_reciprocal_carry_nonzero_depth", checks)
    require(C_identity != C_depth, "copresence_and_endpoint_metrics_do_not_select_carry", checks)

    hashes = {}
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative, _role = line.split("\t")
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"source_hash_{Path(relative).parent.name or Path(relative).stem}", checks)
        hashes[relative] = actual

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "landing": {
            "total_transition": "C_BA=R_B M_BA R_A^-1",
            "gauge": "R_i'=R_i P_i; M_BA'=P_B^-1 M_BA P_A; C_BA'=C_BA",
            "grading": "chi(C_BA)=Phi_B-Phi_A+chi(M_BA)",
            "G141_reduction": "in a fixed matched Bplus presentation chi(M_BA)=0 recovers G141 scalar grading; identity carry alone recovers its full transition",
            "ownership": "abstract two-channel representation supplied/chosen in founding; only D(delta) is derived on supplied depth; physical soldering/carry/query not selected by copresence alone",
        },
        "countermodel": {
            "same_endpoint_R_A_R_B": "I",
            "carry_zero": "I; grading ratio 1; chi 0",
            "carry_nonzero": "diag(1/2,2); grading ratio 4; chi log(2)",
        },
        "source_hashes": hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
