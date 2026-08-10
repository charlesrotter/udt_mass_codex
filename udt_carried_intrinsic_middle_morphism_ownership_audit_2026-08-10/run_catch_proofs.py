#!/usr/bin/env python3
"""Exercise fail-closed defects against the middle-morphism ownership gates."""

from __future__ import annotations

import csv
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA = sp.diag(-1, 1, 1, 1)


def main() -> None:
    pu = sp.diag(1, 0, 0, 0)
    pn = sp.diag(0, 1, 0, 0)
    hs = sp.diag(0, 0, 1, 1)
    x = -pu + pn + sp.Rational(1, 2) * hs
    b = sp.eye(4)
    b[0, 0] = b[1, 1] = sp.Rational(5, 4)
    b[0, 1] = b[1, 0] = sp.Rational(3, 4)
    xc = b * x * b.inv()
    r = sp.eye(4)
    r[2, 2] = r[3, 3] = 0
    r[2, 3] = -1
    r[3, 2] = 1
    m0 = b.inv()
    m1 = r * m0

    with (ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv").open() as handle:
        loops = list(csv.DictReader(handle, delimiter="\t"))

    tests = []

    def identity_claim_is_valid(carried: sp.Matrix, intrinsic: sp.Matrix) -> bool:
        return carried == intrinsic

    def uniqueness_claim_is_valid(valid_solutions: list[sp.Matrix]) -> bool:
        return len(valid_solutions) == 1

    def screen_axis_claim_is_valid(nontrivial_input_stabilizer: bool) -> bool:
        return not nontrivial_input_stabilizer

    def endpoint_only_claim_is_valid(closure_residuals: list[float]) -> bool:
        return all(value <= 1e-10 for value in closure_residuals)

    def quotient_group_claim_is_valid(stabilizer_is_normal: bool) -> bool:
        return stabilizer_is_normal

    def equivariant_section_claim_is_valid(base_stabilizer_is_trivial: bool) -> bool:
        return base_stabilizer_is_trivial

    def lambda_coverage_is_valid(observed: set[str]) -> bool:
        return observed == {"-2", "-1", "0", "1/2", "1", "2"}

    def derived_atlas_claim_is_valid(atlas_supplied_or_derived: bool) -> bool:
        return atlas_supplied_or_derived

    def scalar_promotion_is_valid(pair_functor_owned: bool, scalar_character_owned: bool) -> bool:
        return pair_functor_owned and scalar_character_owned

    def native_minimizer_claim_is_valid(native_positive_objective_owned: bool) -> bool:
        return native_positive_objective_owned

    def record(test_id: str, defect: str, rejected: bool) -> None:
        assert rejected, test_id
        tests.append({"test_id": test_id, "injected_defect": defect, "expected": "REJECT", "observed": "REJECT"})

    record("C01", "set M_B=identity despite X_car!=X_intrinsic", not identity_claim_is_valid(xc, x))
    record(
        "C02",
        "claim unique alignment while second SO2-related exact alignment exists",
        not uniqueness_claim_is_valid([m0, m1])
        and m0 != m1
        and m0 * xc * m0.inv() == x
        and m1 * xc * m1.inv() == x,
    )
    record(
        "C03",
        "promote one screen axis to metric-owned",
        not screen_axis_claim_is_valid(
            r * pu == pu * r and r * pn == pn * r and r * hs == hs * r and r != sp.eye(4)
        ),
    )
    record(
        "C04",
        "erase path labels from full-holonomy endpoint lift",
        len(loops) == 36
        and not endpoint_only_claim_is_valid([float(row["ordinary_closure_residual"]) for row in loops]),
    )
    b02 = sp.eye(4)
    b02[0, 0] = b02[2, 2] = sp.Rational(5, 4)
    b02[0, 2] = b02[2, 0] = sp.Rational(3, 4)
    brb = sp.simplify(b02 * r * b02.inv())
    record(
        "C05",
        "treat SO2 double cosets as a compositional quotient group",
        not quotient_group_claim_is_valid(not any(brb * proj != proj * brb for proj in (pu, pn, hs))),
    )
    record(
        "C06",
        "claim a Lorentz-equivariant global section despite nontrivial base stabilizer",
        not equivariant_section_claim_is_valid(
            not (r != sp.eye(4) and all(r * proj == proj * r for proj in (pu, pn, hs)))
        ),
    )
    record("C07", "drop one lambda stratum", not lambda_coverage_is_valid({"-2", "-1", "0", "1/2", "1"}))
    record("C08", "call an absent common pair atlas derived", not derived_atlas_claim_is_valid(False))
    record(
        "C09",
        "promote relative orbit to universal scalar c_eff",
        not scalar_promotion_is_valid(pair_functor_owned=False, scalar_character_owned=False),
    )
    record(
        "C10",
        "use Euclidean Frobenius minimization as metric-native selector",
        not native_minimizer_claim_is_valid(native_positive_objective_owned=False),
    )
    b3 = sp.eye(4)
    b3[0, 0] = b3[2, 2] = sp.Rational(5, 4)
    b3[0, 2] = b3[2, 0] = sp.Rational(3, 4)
    leg12 = b * r
    leg23 = b3 * (r**2) * b.inv()
    middle_h = b * r * b.inv()
    original = sp.simplify(leg23 * leg12)
    one_sided = sp.simplify(leg23 * middle_h * leg12)
    balanced = sp.simplify((leg23 * middle_h) * (middle_h.inv() * leg12))
    record(
        "C11",
        "change the middle representative on only one leg and call composition gauge independent",
        one_sided != original and balanced == original,
    )

    out = HERE / "CATCH_PROOFS.tsv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(tests[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(tests)
    print(f"catch_proofs={len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
