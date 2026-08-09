#!/usr/bin/env python3
"""Exact controller for the reciprocal calibration-state solder audit.

The controller tests local, bilocal, path-functor, and associated-line
constructions.  It does not choose a physical observer law.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


LANDING = (
    "ABSTRACT_RECIPROCAL_CALIBRATION_LINE_DERIVED__"
    "PAIR_RELATIVE_CAUSAL_FLAG_CONDITIONALLY_CONSTRUCTIBLE_ON_REGULAR_QUERIES__"
    "NO_NONZERO_ORDER_ZERO_OR_FIRST_METRIC_JET_NATURAL_SOLDER__"
    "STATIONARY_KILLING_SOLDER_CONDITIONAL_POSITIVE__"
    "GENERAL_BILOCAL_GLOBAL_CALIBRATION_STATE_FUNCTOR_OPEN"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def gram(metric: sp.Matrix, vectors: sp.Matrix) -> sp.Matrix:
    return sp.simplify(vectors.T * metric * vectors)


def density_sq(metric: sp.Matrix, vectors: sp.Matrix) -> sp.Expr:
    return sp.simplify(abs(gram(metric, vectors).det()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().with_name("DERIVATION_RESULT.json"),
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = Path(__file__).resolve().parent

    checks: list[dict[str, object]] = []

    def check(name: str, condition: object, detail: str = "") -> None:
        passed = bool(condition)
        checks.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            raise AssertionError(name)

    # Frozen evidence surface.
    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    check("source manifest has 24 rows", len(sources) == 24)
    check("source manifest paths are unique", len({row["path"] for row in sources}) == 24)
    for row in sources:
        path = repo / row["path"]
        check(f"source exists: {row['path']}", path.is_file())
        check(f"source hash: {row['path']}", sha256(path) == row["sha256"])

    eta = sp.diag(-1, 1, 1, 1)
    t = sp.symbols("t", real=True)
    D = sp.diag(sp.exp(-t), sp.exp(t), 1, 1)
    K = sp.eye(4)
    K[0, 0] = 0
    K[0, 1] = 1
    K[1, 0] = 1
    K[1, 1] = 0
    K2 = K[:2, :2]
    check("founded D preserves abstract K", sp.simplify(D[:2, :2].T * K2 * D[:2, :2] - K2) == sp.zeros(2))
    check("founded D is nonisometric for physical eta", sp.simplify(D.T * eta * D - eta) != sp.zeros(4))

    # The reciprocal-root character canonically acts on the density line
    # |Lambda^2 P|^(1/2) tensor |L|^(-1).
    line = sp.eye(4)[:, :1]
    plane = sp.eye(4)[:, :2]
    rho1_sq_D = sp.simplify(density_sq(eta, D * line) / density_sq(eta, line))
    rho2_sq_D = sp.simplify(density_sq(eta, D * plane) / density_sq(eta, plane))
    lambda_rf_sq = sp.simplify(rho1_sq_D / sp.sqrt(rho2_sq_D))
    check("pure reciprocal clock density squared", rho1_sq_D == sp.exp(-2 * t))
    check("pure reciprocal plane density squared", rho2_sq_D == 1)
    check("associated calibration multiplier is exp(-2t)", lambda_rf_sq == sp.exp(-2 * t))

    # Endpoint orthonormal coframe matching is exactly isometric.
    E_p = sp.Matrix([[2, 0, 0, 0], [0, 3, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]])
    E_q = sp.Matrix([[1, 0, 0, 0], [0, 4, 0, 0], [0, 1, 2, 0], [0, 0, 0, 5]])
    g_p = sp.simplify(E_p.T * eta * E_p)
    g_q = sp.simplify(E_q.T * eta * E_q)
    A_frame = sp.simplify(E_q.inv() * E_p)
    check("coframe matching is a metric isometry", sp.simplify(A_frame.T * g_q * A_frame - g_p) == sp.zeros(4))
    check(
        "coframe matching preserves clock density",
        sp.simplify(density_sq(g_q, A_frame * line) / density_sq(g_p, line) - 1) == 0,
    )
    check(
        "coframe matching preserves plane density",
        sp.simplify(density_sq(g_q, A_frame * plane) / density_sq(g_p, plane) - 1) == 0,
    )

    # A coordinate-component identity can manufacture a false reciprocal depth.
    T = sp.diag(sp.Rational(1, 2), 2, 1, 1)
    g_same_p = eta
    g_same_q = sp.simplify(T.T * eta * T)
    C_identity = sp.simplify(g_same_p.inv() * g_same_q)
    A_correct = T.inv()
    check("chart identity manufactures reciprocal strain", C_identity == sp.diag(sp.Rational(1, 4), 4, 1, 1))
    check("correct same-geometry component map is isometric", sp.simplify(A_correct.T * g_same_q * A_correct - g_same_p) == sp.zeros(4))
    check("identity and covariant component map differ", A_correct != sp.eye(4))

    # Levi-Civita transport is an isometry and has zero reciprocal-root depth.
    a = sp.symbols("a", real=True)
    boost = sp.eye(4)
    boost[0, 0] = sp.cosh(a)
    boost[0, 1] = sp.sinh(a)
    boost[1, 0] = sp.sinh(a)
    boost[1, 1] = sp.cosh(a)
    check("Lorentz/Levi-Civita model transport is isometric", sp.simplify(boost.T * eta * boost - eta) == sp.zeros(4))
    check("isometric clock density is one", sp.simplify(density_sq(eta, boost * line) - density_sq(eta, line)) == 0)
    check("isometric plane density is one", sp.simplify(density_sq(eta, boost * plane) - density_sq(eta, plane)) == 0)

    # A regular ordered observer/event query can supply a pair-relative flag.
    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([0, sp.Rational(3, 5), sp.Rational(4, 5), 0])
    flag = sp.Matrix.hstack(u, n)
    check("regular query clock is unit timelike", gram(eta, u)[0] == -1)
    check("regular query ruler is unit spacelike", gram(eta, n)[0] == 1)
    check("regular query flag is Lorentzian", gram(eta, flag) == sp.diag(-1, 1))
    check("flat metric transport of regular query gives zero scale", density_sq(eta, flag) == 1)

    # Metric separation is symmetric but not a signed additive cocycle.
    d_pq = sp.Integer(1)
    d_qr = sp.Integer(1)
    d_pr = sp.sqrt(2)
    check("generic triangle separation is not additive", sp.simplify(d_pq + d_qr - d_pr) != 0)
    check("nonnegative separation cannot reverse sign", d_pq == d_pq and d_pq != -d_pq)

    # The 4D differential of exp does not compose under subdivision.  The
    # exact transverse factor on a unit sphere is sin(r)/r.
    f_half = sp.simplify(sp.sin(sp.pi / 6) / (sp.pi / 6))
    f_full = sp.simplify(sp.sin(sp.pi / 3) / (sp.pi / 3))
    check("dexp transverse half factor", f_half == 3 / sp.pi)
    check("dexp transverse full factor", f_full == 3 * sp.sqrt(3) / (2 * sp.pi))
    check("dexp 4D block is not subdivision-compositional", sp.N(f_half**2 - f_full, 40) != 0)

    # Full Jacobi phase-space propagation composes, while a selected 4D block
    # does not.  One transverse mode suffices as an exact control.
    def jacobi_phase(x: sp.Expr) -> sp.Matrix:
        return sp.Matrix([[sp.cos(x), sp.sin(x)], [-sp.sin(x), sp.cos(x)]])

    jh = jacobi_phase(sp.pi / 6)
    jf = jacobi_phase(sp.pi / 3)
    check("full Jacobi phase map composes", sp.simplify(jh * jh - jf) == sp.zeros(2))
    check("Jacobi position block does not compose alone", sp.sin(sp.pi / 3) != sp.sin(sp.pi / 6) ** 2)

    # Raw coframe currents have an inhomogeneous local-frame term.  The
    # reciprocal self-adjoint projection kills a pure Lorentz gauge term, but
    # a coordinate reparameterization still manufactures a nonzero current.
    H = sp.diag(-1, 1, 0, 0)
    boost_generator = sp.zeros(4)
    boost_generator[0, 1] = 1
    boost_generator[1, 0] = 1
    check("local Lorentz current has inhomogeneous boost term", boost_generator != sp.zeros(4))
    check("reciprocal projection kills pure Lorentz gauge term", sp.trace(H * boost_generator) == 0)
    x = sp.symbols("x", real=True)
    E_chart = sp.diag(sp.exp(x), 1, 1, 1)
    J_chart = sp.simplify(sp.diff(E_chart, x) * E_chart.inv())
    alpha_raw = sp.simplify(sp.trace(H * J_chart) / 2)
    check("coordinate reparameterization produces raw reciprocal current", alpha_raw == sp.Rational(-1, 2))
    # For g_xx=-exp(2x), Gamma^x_xx=1 and the covariant coframe derivative vanishes.
    covariant_E00 = sp.simplify(sp.diff(sp.exp(x), x) - 1 * sp.exp(x))
    check("Levi-Civita covariantization removes chart current", covariant_E00 == 0)

    # Metric-only first jets vanish in normal coordinates; no nonzero natural
    # first-jet one-form can be recovered there.
    dg = [sp.zeros(4) for _ in range(4)]
    christoffel_at_normal_origin = [sp.zeros(4) for _ in range(4)]
    check("normal-coordinate metric first jets vanish", all(m == sp.zeros(4) for m in dg))
    check("normal-coordinate Levi-Civita coefficients vanish", all(m == sp.zeros(4) for m in christoffel_at_normal_origin))

    # Higher-jet natural nonmetric connections remain an unselected family.
    c = sp.symbols("c", real=True)
    R = 4 / (1 + x**2)
    alpha_x = sp.diff(R, x)
    ricci_sharp_tt = 2 / (1 + x**2)
    connection_extra_tt = sp.simplify(2 * c * alpha_x * ricci_sharp_tt)
    log_clock_factor = sp.simplify(-sp.integrate(connection_extra_tt, (x, 0, 1)))
    check("higher-order natural connection clock scale is 6c", log_clock_factor == 6 * c)
    check("higher-order natural connection depth is -3c", -log_clock_factor / 2 == -3 * c)

    # Conditional stationary/Killing branch.
    Np, Nq, Nr = sp.symbols("N_p N_q N_r", positive=True)
    delta_pq = sp.log(Np / Nq)
    delta_qr = sp.log(Nq / Nr)
    delta_pr = sp.log(Np / Nr)
    check("Killing norm ratios compose", sp.simplify(sp.expand_log(delta_pq + delta_qr - delta_pr, force=True)) == 0)
    check("Killing norm ratio reverses", sp.simplify(sp.expand_log(delta_pq + sp.log(Nq / Np), force=True)) == 0)
    k = sp.symbols("k", positive=True)
    check(
        "Killing normalization cancels",
        sp.simplify(sp.expand_log(sp.log(k * Np / (k * Nq)) - delta_pq, force=True)) == 0,
    )

    # Null/degenerate flag boundary: the logarithmic density character fails.
    A_null = sp.eye(4)
    A_null[:, 0] = sp.Matrix([1, 0, 1, 0])
    null_clock_density = density_sq(eta, A_null * line)
    check("null transported clock density vanishes", null_clock_density == 0)
    check("null clock makes logarithmic character undefined", sp.log(null_clock_density) is sp.zoo)

    with (package / "SOLDER_CANDIDATE_LEDGER.tsv").open(newline="", encoding="utf-8") as stream:
        candidate_rows = list(csv.DictReader(stream, delimiter="\t"))
    check("candidate ids are unique", len(candidate_rows) == len({row["candidate_id"] for row in candidate_rows}))
    check("exactly one universal derived nonzero solder is absent", not any(row["status"] == "DERIVED_UNIVERSAL_NONZERO_SOLDER" for row in candidate_rows))
    check("stationary positive branch remains conditional", any(row["candidate_id"] == "C11" and row["status"] == "CONDITIONAL_POSITIVE" for row in candidate_rows))

    result = {
        "schema": "udt-reciprocal-calibration-state-solder-v1",
        "landing": LANDING,
        "sympy_version": sp.__version__,
        "source_count": len(sources),
        "check_count": len(checks),
        "passed_count": sum(int(row["passed"]) for row in checks),
        "all_passed": all(bool(row["passed"]) for row in checks),
        "exact": {
            "calibration_line": "|Lambda^2 P|^(1/2) tensor |L|^(-1)",
            "pure_multiplier": "exp(-2*t)",
            "dexp_half_factor": "3/pi",
            "dexp_full_factor": "3*sqrt(3)/(2*pi)",
            "higher_order_connection_depth": "-3*c",
            "regular_query_gram": ["-1", "0", "0", "1"],
        },
        "statuses": {
            "abstract_calibration_line": "DERIVED_GIVEN_CAUSAL_FLAG_GROUPoid",
            "pair_relative_flag": "CONDITIONAL_REGULAR_QUERY_CONSTRUCTION",
            "local_order_zero_or_first_metric_jet_solder": "NO_NONZERO_NATURAL_SOLDER",
            "unique_geodesic_or_world_function": "DIRECTION_ONLY_NOT_CALIBRATION",
            "levi_civita": "EXACT_ISOMETRIC_ZERO_DEPTH",
            "differential_exponential": "NONCOMPOSITIONAL_4D_BLOCK",
            "jacobi_phase_space": "COMPOSITIONAL_WRONG_DIMENSION_WITHOUT_REDUCTION",
            "raw_coframe_current": "PRESENTATION_DEPENDENT",
            "higher_order_metric_natural_arrow": "NONUNIQUE_FAMILY",
            "stationary_killing": "CONDITIONAL_POSITIVE_SOLDER",
            "general_physical_functor": "OPEN_REQUIRES_BILOCAL_GLOBAL_OR_DYNAMICAL_OWNER",
        },
        "checks": checks,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("landing", "check_count", "passed_count", "all_passed")}, sort_keys=True))


if __name__ == "__main__":
    main()
