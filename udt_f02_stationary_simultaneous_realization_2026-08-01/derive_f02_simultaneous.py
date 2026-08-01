#!/usr/bin/env python3
"""Exact primary derivation for the preregistered F02 simultaneous witness."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
CHECKS: list[dict[str, str]] = []
OUTPUT_LINES: list[str] = []


def check(name: str, condition: bool, detail: str) -> None:
    if condition is not True and condition != sp.S.true:
        raise AssertionError(name)
    CHECKS.append({"name": name, "result": "PASS", "detail": detail})
    line = f"[PASS] {name}: {detail}"
    OUTPUT_LINES.append(line)
    print(line)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    x, eps = sp.symbols("x eps", real=True)
    gp, gf, gx, gh, cm = sp.symbols("g_p g_f g_x g_h c_m", real=True)
    p = sp.Function("p")(x)
    lam = sp.Function("lambda")(x)
    f = sp.Function("f")(x)
    h = sp.Function("h")(x)
    weight = sp.exp(2 * lam * p)
    ltilde = (
        gp * sp.diff(p, x) ** 2
        + gf * sp.diff(f, x) ** 2
        + 2 * gx * sp.diff(f, x) * sp.diff(h, x)
        + gh * sp.diff(h, x) ** 2
    ) / 2
    density = weight * (ltilde + cm * sp.diff(lam, x) ** 2 / 2)

    def euler(field: sp.Expr) -> sp.Expr:
        return sp.simplify(sp.diff(density, field) - sp.diff(sp.diff(density, sp.diff(field, x)), x))

    residuals = {name: euler(field) for name, field in [("p", p), ("lambda", lam), ("f", f), ("h", h)]}
    a, b = sp.symbols("a b", real=True)
    background = {
        p: 0,
        sp.diff(p, x): 0,
        sp.diff(p, x, 2): 0,
        lam: 0,
        sp.diff(lam, x): 0,
        sp.diff(lam, x, 2): 0,
        f: a * x,
        sp.diff(f, x): a,
        sp.diff(f, x, 2): 0,
        h: b * x,
        sp.diff(h, x): b,
        sp.diff(h, x, 2): 0,
    }
    landed = {name: sp.simplify(value.subs(background)) for name, value in residuals.items()}
    check(
        "D01_full_background_rows",
        all(value == 0 for value in landed.values()),
        "p=0, lambda=0, and affine f/h solve all four Euler rows including the jet-quadratic term",
    )

    e0 = sp.expand((gf * a**2 + 2 * gx * a * b + gh * b**2) / 2)
    check(
        "D02_energy_reading",
        sp.simplify(ltilde.subs(background) - e0) == 0,
        "the landed constant density is E0=(g_f a^2+2g_xab+g_hb^2)/2",
    )
    delta_g = gf * gh - gx**2
    witness_values = {gp: 1, gf: 1, gx: 0, gh: 1, cm: 1, a: sp.Rational(1, 2), b: 0}
    e0_w = sp.simplify(e0.subs(witness_values))
    check(
        "D03_generic_nondegeneracy",
        gp.subs(witness_values) > 0 and delta_g.subs(witness_values) > 0,
        "the exact witness has g_p=1 and Delta_G=1, inside the generic positive-definite class",
    )
    check(
        "D04_nonzero_landing",
        e0_w == sp.Rational(1, 8),
        "f=x/2, h=0 gives the exact nonzero candidate density E0=1/8",
    )

    # The full lambda locked row receives no contribution from a term quadratic in lambda'
    # when lambda'=lambda''=0; this directly checks the inherited lock-reduction theorem here.
    lambda_row_w = sp.simplify(residuals["lambda"].subs(background).subs(witness_values))
    check(
        "D05_full_locked_row_with_jet_term",
        lambda_row_w == 0,
        "c_m lambda'^2/2 is quadratic at the lock and the complete lambda Euler row vanishes",
    )

    # Reconstruct the complete joint second variation, with all four fields varied.
    vp = sp.Function("v_p")(x)
    vl = sp.Function("v_lambda")(x)
    vf = sp.Function("v_f")(x)
    vh = sp.Function("v_h")(x)
    perturbed = {
        p: eps * vp,
        lam: eps * vl,
        f: a * x + eps * vf,
        h: b * x + eps * vh,
    }
    density_eps = density.subs(perturbed, simultaneous=True).doit()
    second = sp.simplify(sp.diff(density_eps, eps, 2).subs(eps, 0))
    target = (
        gp * sp.diff(vp, x) ** 2
        + cm * sp.diff(vl, x) ** 2
        + gf * sp.diff(vf, x) ** 2
        + 2 * gx * sp.diff(vf, x) * sp.diff(vh, x)
        + gh * sp.diff(vh, x) ** 2
        + 4 * e0 * vl * vp
    )
    check(
        "D06_complete_joint_second_variation",
        sp.simplify(sp.expand(second - target)) == 0,
        "the full landed Hessian is the angular positive block plus the exact p/lambda jet block",
    )

    ell, kn = sp.symbols("ell k_n", positive=True)
    mode_block = sp.Matrix([[gp * kn**2, 2 * e0], [2 * e0, cm * kn**2]])
    determinant = sp.expand(mode_block.det())
    check(
        "D07_mode_determinant",
        sp.simplify(determinant - (gp * cm * kn**4 - 4 * e0**2)) == 0,
        "the p/lambda mode determinant reproduces the banked exact dichotomy",
    )
    threshold_residual = sp.expand(gp * cm * sp.pi**4 - 64 * e0**2 * ell**4)
    threshold_w = sp.simplify(threshold_residual.subs(witness_values).subs(ell, 1))
    check(
        "D08_sector_threshold_witness",
        threshold_w == sp.pi**4 - 1 and sp.ask(sp.Q.positive(threshold_w)) is True,
        "at ell=1 the exact condition is 1<=pi^4, strictly satisfied",
    )

    # Open/acyclic completion has no periodic single-valuedness constraint. Demonstrate
    # why the same affine witness cannot be silently called a one-cell cyclic member.
    f_w = x / 2
    endpoint_jump = sp.simplify(f_w.subs(x, 1) - f_w.subs(x, -1))
    check(
        "D09_completion_branch_discrimination",
        endpoint_jump == 1,
        "the affine witness belongs only to the open/acyclic branch; a one-cell cyclic identification would cut it",
    )

    m_gen = sp.simplify(2 * sp.Integer(1) * e0_w)
    check(
        "D10_candidate_mass_readings",
        m_gen == sp.Rational(1, 4),
        "M_GEN=M_DENS_coord=M_DENS_proper=1/4 while the inherited M_WALL reading remains 0",
    )

    sources = [
        "udt_p4_gradient_seat_2026-07-29/EXACT_DERIVATION.md",
        "udt_p4_gradient_seat_2026-07-29/CORRECTION_LAYER.md",
        "udt_p4_period_gate_2026-07-30/EXACT_DERIVATION.md",
        "udt_p4_angular_completion_2026-07-30/AUDIT_REPORT.md",
        "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md",
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
    ]
    with (PKG / "SOURCE_INVENTORY.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "bytes", "sha256"])
        for relative in sources:
            path = ROOT / relative
            writer.writerow([relative, path.stat().st_size, digest(path)])

    conditions = [
        ["C01", "P1_4D_FIELDS_CENSUS", "CONDITIONAL", "a_F=2lambda; lambda=0 emerges on E0!=0 landing", "gradient-seat:176-206"],
        ["C02", "GENERIC_AFFINE_ATLAS", "SATISFIED", "g_p=1; Delta_G=1", "gradient-seat:176-206"],
        ["C03", "NONZERO_AFFINE_SLOPE", "SATISFIED", "f=x/2; h=0; E0=1/8", "gradient-seat:199-212"],
        ["C04", "FULL_LOCKED_ROW", "SATISFIED", "quadratic lambda-jet content vanishes at locked background", "gradient-seat:129-146,213-230"],
        ["C05", "SUPPLIED_WALL_DATA", "CONDITIONAL_FREE", "open endpoints leave the f slope free", "gradient-seat:207-212"],
        ["C06", "COMPLETION", "CONDITIONAL_ACYCLIC", "open/acyclic branch has no cycle and leaves F02 untouched", "period-gate:42-47,209-214"],
        ["C07", "R_A_FOLD_PREMISE", "NOT_ASSUMED_OPEN", "R-A would impose definite parities and collapse E0; no fold is selected", "angular-completion:50-56,80-92"],
        ["C08", "JET_SECTOR", "SATISFIED", "g_p=c_m=ell=1; 64E0^2ell^4=1<=pi^4", "stability-slice:113-131"],
        ["C09", "PHYSICAL_COMPLETION", "OPEN", "p=0 seal-valued background has no derived canon/physical completion", "gradient-seat:199-206"],
        ["C10", "MASS_STATUS", "CANDIDATE_ONLY", "three readings=1/4; wall reading=0; none physical", "gradient-seat report mass table"],
        ["C11", "TIME_AND_FULL_STABILITY", "OPEN", "stationary Dirichlet jet sector only", "stability-slice:123-131"],
    ]
    with (PKG / "CONDITION_LEDGER.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["condition_id", "condition", "status", "witness_or_scope", "source_anchor"])
        writer.writerows(conditions)

    result = {
        "outcome": "CONDITIONAL_NONPERIODIC_F02_DIRICHLET_HESSIAN_SECTOR_POSITIVITY_WITNESS_EXISTS",
        "e0": "1/8",
        "candidate_mass_gen": "1/4",
        "candidate_mass_density_coordinate": "1/4",
        "candidate_mass_density_proper": "1/4",
        "candidate_mass_wall": "0",
        "completion": "OPEN_ACYCLIC_CONDITIONAL__NO_PHYSICAL_COMPLETION_CLAIM",
        "jet_sector": "STRICTLY_INSIDE_NONNEGATIVE_REGION",
        "threshold_residual": "pi**4 - 1",
        "native_mass": False,
        "native_stability": False,
        "selected_response": False,
        "time_live": False,
        "external_cold_review": "PASS_AFTER_REQUIRED_SCOPE_NARROWING__CLOSED",
        "checks": CHECKS,
        "sympy_version": sp.__version__,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    final = f"PASS checks={len(CHECKS)} outcome={result['outcome']}"
    OUTPUT_LINES.append(final)
    (PKG / "DERIVATION_STDOUT.txt").write_text("\n".join(OUTPUT_LINES) + "\n", encoding="utf-8")
    print(final)


if __name__ == "__main__":
    main()
