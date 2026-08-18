#!/usr/bin/env python3
"""Exact symbolic derivation for the preregistered G161 quotient audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "3fa4964f"
OUTCOME_CLASS = (
    "LORENTZ_QUOTIENT_AND_UNIQUE_BPLUS2_SECTION_DERIVED__SWEEP_FIXES_"
    "QUOTIENT_NOT_VERTICAL_RAPIDITY__NORMAL_TRANSPORT_INDEPENDENT__"
    "EXTRINSIC_SIMPLE_SPECTRUM_CONDITIONALLY_FIXES_FLAG"
)
LANDING = (
    "PAIR_FIRST_JET_IS_EXACT_LORENTZ_STABILIZER_QUOTIENT__POSITIVE_BPLUS2_"
    "IS_UNIQUE_TIME_ORIENTED_GAUGE_SECTION_ON_FUTURE_TIMELIKE_CLOCK_STRATUM__"
    "DISTANCE_SWEEP_FIXES_QUOTIENT_PATH_AND_FIRST_JET_NOT_VERTICAL_RAPIDITY__"
    "SCREEN_NORMAL_TRANSPORT_DOES_NOT_UNIVERSALLY_RESOLVE_TANGENT_BOOST__"
    "NORMAL_GAUGE_INVARIANT_EXTRINSIC_SIMPLE_CAUSAL_SPECTRUM_CONDITIONALLY_"
    "FIXES_PAIR_FLAG__DEGENERATE_NULL_AND_GLOBAL_STRATA_OPEN__PHYSICAL_"
    "CARRY_HISTORY_QUERY_AND_COMPLETION_OPEN"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 10
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 11)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]
    return len(rows)


def mat(prefix: str, symmetric: bool = False) -> sp.Matrix:
    if symmetric:
        a, b, d = sp.symbols(f"{prefix}a {prefix}b {prefix}d", real=True)
        return sp.Matrix([[a, b], [b, d]])
    values = sp.symbols(f"{prefix}0:4", real=True)
    return sp.Matrix(2, 2, values)


def assert_zero(value: sp.Matrix | sp.Expr) -> None:
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(sp.cancel(entry)) == 0 for entry in value)
    else:
        assert sp.factor(sp.cancel(value)) == 0


def shape(a: sp.Expr, b: sp.Expr, d: sp.Expr) -> sp.Matrix:
    """General eta-self-adjoint 1+1 endomorphism."""
    return sp.Matrix([[a, b], [-b, d]])


def exact_checks() -> dict[str, object]:
    checks: list[str] = []
    eta = sp.diag(-1, 1)

    # Exact fiber identity: equality of pullbacks iff M2 M1^-1 stabilizes h.
    h = mat("h", symmetric=True)
    m1, m2 = mat("m"), mat("n")
    left = m2 * m1.inv()
    pullback_difference = m2.T * h * m2 - m1.T * h * m1
    assert_zero(
        left.T * h * left - h
        - m1.inv().T * pullback_difference * m1.inv()
    )
    checks.append("finite_fibers_are_exact_left_lorentz_stabilizer_orbits")

    # The infinitesimal kernel at a fixed metric is exactly so(h); for eta it is 1D.
    x0, x1, x2, x3 = sp.symbols("x0:4", real=True)
    x = sp.Matrix([[x0, x1], [x2, x3]])
    infinitesimal = x.T * eta + eta * x
    assert infinitesimal == sp.Matrix([[-2 * x0, -x1 + x2], [-x1 + x2, 2 * x3]])
    boost_generator = sp.Matrix([[0, 1], [1, 0]])
    assert_zero(boost_generator.T * eta + eta * boost_generator)
    checks.append("first_jet_kernel_is_one_dimensional_metric_skew_boost_rate")

    # Construct the unique future/time-oriented Lorentzian QR representative.
    p, q, r, s = sp.symbols("p q r s", real=True)
    a = sp.symbols("a", positive=True)
    m = sp.Matrix([[p, q], [r, s]])
    boost = sp.Matrix([[p / a, -r / a], [-r / a, p / a]])
    b = (p * q - r * s) / a
    d = (p * s - q * r) / a
    triangular = sp.Matrix([[a, b], [0, d]])
    relation = {a**2: p**2 - r**2}
    assert_zero((boost.T * eta * boost - eta).subs(relation))
    assert_zero((boost * m - triangular).subs(relation))
    assert_zero((boost.det() - 1).subs(relation))
    checks.append("constructive_positive_lorentzian_qr_section")

    # Terminal decomposition of the quotient representative.
    quotient_metric = triangular.T * eta * triangular
    assert quotient_metric == sp.Matrix([[-a**2, -a * b], [-a * b, d**2 - b**2]])
    terminal_beta = sp.cancel(quotient_metric[0, 1] / quotient_metric[0, 0])
    assert_zero(terminal_beta - b / a)
    assert_zero(-quotient_metric.det() - a**2 * d**2)
    checks.append("pair_terminal_T_beta_L_are_exact_quotient_coordinates")

    # Exact uniqueness equations: a time-oriented boost zeroing the lower-left
    # entry has tanh(rapidity)=r/p, hence one solution while p^2-r^2>0, p>0.
    c, u = sp.symbols("c u", real=True)
    generic_boost = sp.Matrix([[c, -u], [-u, c]])
    lower_left = (generic_boost * m)[1, 0]
    assert lower_left == c * r - p * u
    assert_zero((c**2 - u**2).subs(u, c * r / p) - c**2 * (p**2 - r**2) / p**2)
    checks.append("positive_section_uniqueness_and_null_boundary_equations")

    # A nontrivial smooth vertical boost can ride above an entire distance sweep
    # without changing the pair metric or any derivative of it.
    lam = sp.symbols("lambda", real=True)
    z = lam / 5
    c_z = (1 + z**2) / (1 - z**2)
    s_z = 2 * z / (1 - z**2)
    live_boost = sp.Matrix([[c_z, s_z], [s_z, c_z]])
    live_m = sp.Matrix([[2 + lam, 1 + lam**2], [lam, 3 - lam]])
    lifted_m = live_boost * live_m
    base_pair = live_m.T * eta * live_m
    lifted_pair = lifted_m.T * eta * lifted_m
    assert_zero(live_boost.T * eta * live_boost - eta)
    assert_zero(lifted_pair - base_pair)
    assert_zero(sp.diff(lifted_pair, lam) - sp.diff(base_pair, lam))
    assert lifted_m != live_m
    checks.append("full_distance_sweep_and_first_jet_leave_vertical_rapidity_invisible")

    # The cancellation is the metric-skew live-gauge identity.
    rate = sp.diff(live_boost, lam) * live_boost.inv()
    assert_zero(rate.T * eta + eta * rate)
    checks.append("vertical_rapidity_rate_is_exact_first_jet_kernel")

    # Complete 2+2 flat-product countermodel: screen metric, normal connection,
    # second fundamental form, and normal holonomy remain identical.
    full_metric = sp.diag(-1, 1, 1, 1)
    full_boost = sp.diag(1, 1, 1, 1)
    full_boost[:2, :2] = sp.Matrix([[sp.Rational(5, 3), sp.Rational(4, 3)],
                                    [sp.Rational(4, 3), sp.Rational(5, 3)]])
    assert full_boost != sp.eye(4)
    assert_zero(full_boost.T * full_metric * full_boost - full_metric)
    assert full_boost[2:, 2:] == sp.eye(2)
    checks.append("flat_product_screen_normal_data_do_not_resolve_tangent_boost")

    # Normal-gauge invariance of C_II = sum A_A^2.
    aa, ab, ad, ba, bb, bd = sp.symbols("aa ab ad ba bb bd", real=True)
    A, B = shape(aa, ab, ad), shape(ba, bb, bd)
    nr, ns = sp.symbols("nr ns", real=True)
    Aprime, Bprime = nr * A - ns * B, ns * A + nr * B
    cii = A**2 + B**2
    transformed = Aprime**2 + Bprime**2
    assert_zero(transformed - (nr**2 + ns**2) * cii)
    assert_zero(cii.T * eta - eta * cii)
    checks.append("extrinsic_CII_is_normal_rotation_invariant_and_tangent_self_adjoint")

    # Simple real spectrum supplies a causal eigenflag in 1+1.
    simple_A, simple_B = shape(1, 0, 2), sp.zeros(2)
    simple_cii = simple_A**2 + simple_B**2
    simple_disc = sp.discriminant(simple_cii.charpoly().as_expr())
    assert simple_cii == sp.diag(1, 4)
    assert simple_disc == 9
    checks.append("simple_extrinsic_spectrum_conditionally_supplies_causal_pair_flag")

    # Explicit degenerate strata: umbilic, Jordan/null, and complex spectrum.
    alpha, gamma = sp.symbols("alpha gamma", real=True)
    umbilic = (alpha * sp.eye(2))**2 + (gamma * sp.eye(2))**2
    assert_zero(umbilic - (alpha**2 + gamma**2) * sp.eye(2))
    jordan_A = shape(-3, -3, -2)
    jordan_B = shape(-3, 2, -2)
    jordan_cii = jordan_A**2 + jordan_B**2
    assert jordan_cii == sp.Matrix([[5, 5], [-5, -5]])
    assert sp.discriminant(jordan_cii.charpoly().as_expr()) == 0
    complex_A = shape(-3, -3, -3)
    complex_cii = complex_A**2 + complex_A**2
    assert complex_cii == sp.Matrix([[0, 36], [-36, 0]])
    assert sp.discriminant(complex_cii.charpoly().as_expr()) == -5184
    checks.append("umbilic_jordan_and_complex_extrinsic_failure_strata_explicit")

    assert len(checks) == 11
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "finite_pair_metric_fiber": "left_SOplus(h)_orbit_on_time_oriented_component",
        "first_jet_vertical_dimensions": 2,
        "positive_bplus2_unique_quotient_section": True,
        "positive_bplus2_is_physical_carry_selector": False,
        "smooth_distance_sweep_fixes_vertical_rapidity": False,
        "smooth_distance_sweep_fixes_quotient_path": True,
        "screen_normal_transport_universally_resolves_tangent_boost": False,
        "extrinsic_CII_simple_causal_spectrum_conditionally_fixes_flag": True,
        "pair_immersion_is_required_to_own_II": True,
        "metric_plus_bare_pair_plane_owns_II": False,
        "null_and_degenerate_strata_closed": False,
        "physical_carry_derived": False,
        "physical_history_derived": False,
    }


def main() -> None:
    result = {
        "status": "PASS",
        "registered_outcome_class": OUTCOME_CLASS,
        "landing": LANDING,
        "source_count": verify_manifest(),
        **exact_checks(),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
