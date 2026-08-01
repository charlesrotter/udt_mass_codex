#!/usr/bin/env python3
"""Exact algebra and registered-census classifier for the F02 completion gate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
CHECKS: list[dict[str, str]] = []
LINES: list[str] = []


def check(name: str, condition: bool, detail: str) -> None:
    if condition is not True and condition != sp.S.true:
        raise AssertionError(name)
    CHECKS.append({"name": name, "result": "PASS", "detail": detail})
    line = f"[PASS] {name}: {detail}"
    LINES.append(line)
    print(line)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    # One-cell affine periodicity.
    L, af, ah = sp.symbols("L a_f a_h", real=True)
    Lpos = sp.symbols("L_pos", positive=True)
    one = sp.solve([sp.Eq(Lpos * af, 0), sp.Eq(Lpos * ah, 0)], [af, ah], dict=True)
    check(
        "D01_one_cell_period_kills_slopes",
        one == [{af: 0, ah: 0}],
        "single-valued affine f/h on a positive-length one-cell cycle forces both slopes to zero",
    )

    # Untwisted multi-cell theorem in a representative exact 2x2 positive-definite family.
    # The analytic theorem is: A=sum_i L_i G_i^-1 is positive definite, hence Ac=0 => c=0.
    L1, L2 = sp.symbols("L_1 L_2", positive=True)
    c1, c2 = sp.symbols("c_1 c_2", real=True)
    c = sp.Matrix([c1, c2])
    G1 = sp.Matrix([[2, 1], [1, 2]])
    G2 = sp.Matrix([[3, 1], [1, 1]])
    A = sp.simplify(L1 * G1.inv() + L2 * G2.inv())
    detA = sp.factor(A.det())
    check(
        "D02_multicell_positive_period_matrix",
        A[0, 0].is_positive is True and sp.ask(sp.Q.positive(detA)) is True,
        "for the exact heterogeneous control A=sum L_i G_i^-1 is positive definite; the general proof is the positive quadratic-form sum",
    )
    solution = sp.solve(list(A * c), [c1, c2], dict=True)
    check(
        "D03_untwisted_multicell_momentum_continuity_kills_slopes",
        solution == [{c1: 0, c2: 0}],
        "ordinary no-source seams give one common momentum c; field closure A c=0 then forces c=0 and every slope G_i^-1 c=0",
    )
    gf, gx, gh = sp.symbols("g_f g_x g_h", real=True)
    Gcommon = sp.Matrix([[gf, gx], [gx, gh]])
    Acommon = sp.simplify((L1 + L2) * Gcommon.inv())
    check(
        "D03b_homogeneous_multicell_no_go_needs_only_nondegeneracy",
        sp.simplify(Acommon.det() - (L1 + L2) ** 2 / Gcommon.det()) == 0,
        "with one common response matrix, det A=(sum L_i)^2/det G is nonzero whenever the inherited Delta_G nondegeneracy holds; positivity is not needed",
    )

    # Freely reversing slopes is not an ordinary seam solution.
    a1, a2 = sp.symbols("a_1 a_2", real=True)
    av = sp.Matrix([a1, a2])
    G = sp.Matrix([[2, 1], [1, 3]])
    jump = sp.simplify(G * (-av) - G * av)
    check(
        "D04_naive_slope_cancellation_has_momentum_jump",
        jump == -2 * G * av and jump != sp.zeros(2, 1),
        "the tempting two-cell slopes a and -a cancel the field period but create the nonzero seam momentum jump -2Ga unless a=0",
    )

    # A sign transition can algebraically absorb the reversal, but only as transition data.
    T = -sp.eye(2)
    transported = sp.simplify(T.inv().T * (G * av))
    next_momentum = G * (-av)
    check(
        "D05_sign_twist_is_algebraically_possible_but_requires_transition",
        transported == next_momentum,
        "T=-I transports momentum consistently with a slope reversal; this is a conditional bundle-chart witness, not a registered F02 completion",
    )
    Gplus = sp.diag(1, -1)
    Gminus = -Gplus
    c_control = sp.Matrix([1, 0])
    slope_plus = Gplus.inv() * c_control
    slope_minus = Gminus.inv() * c_control
    e_plus = sp.simplify((slope_plus.T * Gplus * slope_plus)[0] / 2)
    e_minus = sp.simplify((slope_minus.T * Gminus * slope_minus)[0] / 2)
    check(
        "D05b_indefinite_crossmember_cancellation_control",
        slope_plus + slope_minus == sp.zeros(2, 1)
        and Gplus * slope_plus == Gminus * slope_minus == c_control
        and (e_plus, e_minus) == (sp.Rational(1, 2), sp.Rational(-1, 2)),
        "two equal cells with G2=-G1 indefinite have matching momentum and cancelling field periods with nonzero opposite E0; this changes the response member and loses the positive Hessian sector, so it is a cross-family OPEN control, not a completed F02 witness",
    )

    # Regular cap obstruction. At p=0, x is proper-distance normalized. Smooth invariant
    # f and bh are even in transverse geodesic distance, hence derivatives vanish at a cap.
    x, ell = sp.symbols("x ell", real=True, positive=True)
    f0, h0 = sp.symbols("f_0 h_0", real=True)
    f = f0 + af * x
    h = h0 + ah * x
    cap_solutions = sp.solve([sp.Eq(sp.diff(f, x), 0), sp.Eq(sp.diff(h, x), 0)], [af, ah], dict=True)
    check(
        "D06_one_regular_cap_kills_affine_F02_slopes",
        cap_solutions == [{af: 0, ah: 0}],
        "regular-cap evenness requires df=dbh=0 at the cap; affine F02 profiles therefore have zero slopes globally",
    )
    opposite_caps = sp.solve(
        [sp.Eq(f.subs(x, -ell), -1), sp.Eq(f.subs(x, ell), 1), sp.Eq(sp.diff(f, x), 0)],
        [f0, af],
        dict=True,
    )
    check(
        "D07_two_cap_moment_values_incompatible_with_affine_regularity",
        opposite_caps == [],
        "the registered two-cap values f(-ell)=-1 and f(+ell)=+1 cannot coexist with the cap-required zero derivative of an affine f",
    )

    # Definite wall parity independently kills affine slopes.
    w = sp.symbols("w", real=True)
    affine = f0 + af * w
    even_residual = sp.Poly(sp.expand(affine - affine.subs(w, -w)), w)
    odd_residual = sp.Poly(sp.expand(affine + affine.subs(w, -w)), w)
    check(
        "D08_definite_parity_collapse",
        sp.solve(even_residual.all_coeffs(), [af], dict=True) == [{af: 0}]
        and sp.solve(odd_residual.all_coeffs(), [f0], dict=True) == [{f0: 0}],
        "even affine parity kills slope; odd affine parity kills the intercept, and two definite wall parities eliminate the nonzero F02 landing as banked",
    )

    rows = [
        ["G01", "MIRRORED_QUOTIENT", "REGISTERED_POSTURE_MULTIPLE_LIFTS", "CUT_ON_DEFINITE_PARITY_LIFTS__OPEN_WITHOUT_COMPLETE_COFRAME_LIFT", "R-A/definite parity gives E0=0; quotient periods alone impose nothing; complete lift remains unselected", "angular-completion; complete-coframe-seal"],
        ["G02", "ONE_CELL_TWO_SIDED_CYCLIC", "REGISTERED_GLOBAL_ALTERNATIVE", "NO_NONZERO_F02", "field single-valuedness forces both affine slopes and E0 to zero", "period-gate C6c; D01"],
        ["G03", "HOMOGENEOUS_MULTICELL_CYCLIC", "REGISTERED_CONDITIONAL_CHAIN", "NO_NONZERO_F02_COMMON_NONDEGENERATE_RESPONSE", "one common nondegenerate response matrix plus momentum and field-period closure forces every slope to zero; heterogeneous positive blocks obey the same theorem", "period-gate field periods; D02-D03b"],
        ["G04", "PIECEWISE_CROSSCELL_CYCLIC", "REGISTERED_ONLY_WITH_TRANSITION_OR_SEAM_DATA", "OPEN_INCOMPLETE_TRANSITION_DATA", "raw same-member cancellation violates momentum matching; sign-twisted and indefinite cross-member cancellations exist algebraically, but their F02 coframe/response descent, moving-seam, and J07/J11 data are not registered", "D04-D05b; full-cell atlas J07/J11"],
        ["G05", "OPEN_ACYCLIC_TERMINATED", "REGISTERED_POSTURE_NOT_PHYSICAL_COMPLETION", "LOCAL_WITNESS_SURVIVES__NO_COMPLETE_GLOBAL_WITNESS", "no cycle cuts the slope, but endpoint/boundary functional and physical completion remain open", "F02 local package; seam-closure; period-gate"],
        ["G06", "TWO_CAP_C1_WITH_R_A", "REGISTERED_S3_CLASS_PLUS_SUPPLIED_R_A", "NO_NONZERO_F02", "regular-cap evenness already kills affine slopes; R-A definite parity independently collapses E0", "cap-gluing; angular-completion; D06-D08"],
        ["G07", "TWO_CAP_C1_WITHOUT_R_A", "REGISTERED_S3_CLASS", "NO_NONZERO_F02_FROM_CAP_REGULARITY", "df=dbh=0 at every regular cap is independent of R-A; opposite f cap values also contradict an affine regular profile", "cap-gluing; D06-D07"],
        ["G08", "MIXED_POSTURE_OR_CROSS_FAMILY_JOIN", "TYPED_NOT_COMPLETED", "OPEN_INCOMPLETE_JOIN_DATA", "a nonzero F02 cell can be written locally, but no complete cross-census/cross-pairing first-jet response and seam law is registered", "period-gate mixed posture; full-cell atlas"],
        ["G09", "SAME_CLOSER_TORIC_CLASS", "UNREGISTERED_EXCLUDED", "EXCLUDED_NOT_A_WITNESS", "same-closer completion was package-introduced and fails the registered unimodular two-cap arena", "angular-completion correction layer"],
    ]
    with (PKG / "COMPLETION_CENSUS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["candidate_id", "candidate", "registration", "f02_status", "reason", "source"])
        writer.writerows(rows)

    sources = [
        "udt_f02_stationary_simultaneous_realization_2026-08-01/AUDIT_REPORT.md",
        "udt_p4_gradient_seat_2026-07-29/EXACT_DERIVATION.md",
        "udt_p4_period_gate_2026-07-30/EXACT_DERIVATION.md",
        "udt_p4_period_gate_2026-07-30/derive_period_gate.py",
        "udt_p4_angular_completion_2026-07-30/AUDIT_REPORT.md",
        "udt_p4_seam_closure_derivation_2026-07-30/EXACT_DERIVATION.md",
        "udt_cap_gluing_selector_2026-07-28/EXACT_DERIVATION.md",
        "udt_general_screen_complete_cell_atlas_2026-07-28/COMPLETION_DESCENT_ATLAS.tsv",
        "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
    ]
    with (PKG / "SOURCE_INVENTORY.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "bytes", "sha256"])
        for relative in sources:
            path = ROOT / relative
            writer.writerow([relative, path.stat().st_size, digest(path)])

    result = {
        "outcome": "OPEN_INCOMPLETE_REGISTERED_CLOSURE_DATA",
        "candidate_rows": len(rows),
        "nonzero_complete_witness_found": False,
        "exhaustive_no_witness_proved": False,
        "ordinary_untwisted_cyclic": "NONZERO_F02_EXCLUDED_FOR_COMMON_NONDEGENERATE_RESPONSE__HETEROGENEOUS_POSITIVE_BLOCKS_ALSO_EXCLUDED",
        "regular_cap_completions": "NONZERO_AFFINE_F02_EXCLUDED",
        "open_acyclic": "LOCAL_ONLY__PHYSICAL_COMPLETION_OPEN",
        "transition_twisted_and_mixed_joins": "OPEN_MISSING_COMPLETE_F02_DESCENT_RESPONSE_AND_SEAM_DATA__INDEFINITE_CROSSMEMBER_CONTROL_EXISTS",
        "candidate_mass_readings": "THREE_NONZERO_LABELS_REMAIN_LOCAL_CANDIDATES__M_WALL_ZERO__NONE_PROMOTED",
        "native_mass": False,
        "native_stability": False,
        "selected_completion": False,
        "checks": CHECKS,
        "sympy_version": sp.__version__,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    final = f"PASS checks={len(CHECKS)} outcome={result['outcome']}"
    LINES.append(final)
    (PKG / "DERIVATION_STDOUT.txt").write_text("\n".join(LINES) + "\n", encoding="utf-8")
    print(final)


if __name__ == "__main__":
    main()
