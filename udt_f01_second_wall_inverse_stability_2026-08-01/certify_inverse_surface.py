#!/usr/bin/env python3
"""Validated inverse-stability surface for the conditional F01 wall-germ slice."""

from __future__ import annotations

import csv
import json
import platform
from fractions import Fraction
from pathlib import Path

import mpmath as mp
from mpmath import iv
import sympy as sp


OUT = Path(__file__).resolve().parent
S_LO = "1.68102"
S_HI = "1.68103"
COARSE_PARTS = 4096
FINE_PARTS = 8192
ALPHAS = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 1))


def endpoints(value) -> list[str]:
    lower = iv.nstr(value.a, 80).lstrip("[").split(",", 1)[0]
    upper = iv.nstr(value.b, 80).lstrip("[").split(",", 1)[0]
    return [lower, upper]


def bounds(value) -> tuple[float, float]:
    return float(value.a), float(value.b)


def overlaps(left, right) -> bool:
    la, lb = bounds(left)
    ra, rb = bounds(right)
    return max(la, ra) <= min(lb, rb)


def root_equation(s):
    u = 2 * s - 1
    return (
        u * iv.log((u * u + 1) / 2)
        - 2 * u
        + 2 * iv.atan2(u, iv.mpf(1))
        - 2
        + iv.pi / 2
    ) / s


def symbolic_controls() -> dict[str, bool]:
    x, s = sp.symbols("x s", real=True, positive=True)
    w = s**2 * x**2 / 2 + (s**2 - s) * x + 1 + s**2 / 2 - s
    wp = sp.diff(w, x)
    logw = sp.log(w)
    lop = lambda value: sp.factor(-sp.diff(w * sp.diff(value, x), x) - s**2 * value / w)
    v1 = wp / w
    v2 = 1 - 1 / w
    source = s**2 * (-1 + (1 - logw) / w)
    u_part = 1 - logw
    w_right = sp.factor(w.subs(x, 1))
    u_d = u_part + v1 / s - (w_right * (1 - sp.log(w_right)) + 2 * s - 1) / (w_right - 1) * v2
    u_f = u_part + v1 / s - v2 / (2 * s - 1)
    phi_d = -1 / s**2 - v1 / s**3 + v2 / (s * (s - 1))
    phi_f = -1 / s**2 - v1 / s**3 + 2 * v2 / (s * (2 * s - 1))
    t = lambda value: sp.factor(w * sp.diff(value, x) + wp * value)

    # Symbolic two-by-two Sherman-Morrison check.
    a, b, c, tau = sp.symbols("a b c tau", nonzero=True)
    g1, g2, l1, l2 = sp.symbols("g1 g2 l1 l2")
    amat = sp.Matrix([[a, b], [b, c]])
    gv = sp.Matrix([g1, g2])
    lv = sp.Matrix([l1, l2])
    ainv = amat.inv()
    updated = amat + tau * gv * gv.T
    sm = ainv - tau * ainv * gv * gv.T * ainv / (1 + tau * (gv.T * ainv * gv)[0])
    schur_direct = (lv.T * updated.inv() * lv)[0]
    schur_sm = (lv.T * sm * lv)[0]

    # Finite aligned angular-trace wall germ.  beta is normalized so its direct
    # trace term is s^2 beta z^2; the bulk angular compliance is J/s^2.
    beta, j, q, z, tt = sp.symbols("beta j q z tt", positive=True)
    tau_beta = s**2 * beta / (1 + beta * j)
    zstar = q / (1 + beta * j)
    scalar_trace_form = s**2 * (q - z) ** 2 / j + s**2 * beta * z**2
    beta_inverse = tt / (s**2 - tt * j)

    controls = {
        "quadratic_identity": sp.simplify(wp**2 + s**2 - 2 * s**2 * w) == 0,
        "u_D_equation": sp.simplify(lop(u_d) + source) == 0,
        "u_D_boundaries": sp.simplify(u_d.subs(x, -1)) == 0 and sp.simplify(u_d.subs(x, 1)) == 0,
        "u_F_equation": sp.simplify(lop(u_f) + source) == 0,
        "u_F_boundaries": sp.simplify(u_f.subs(x, -1)) == 0 and sp.simplify((t(u_f) + logw * wp).subs(x, 1)) == 0,
        "phi_D_equation": sp.simplify(lop(phi_d) - 1 / w) == 0,
        "phi_D_boundaries": sp.simplify(phi_d.subs(x, -1)) == 0 and sp.simplify(phi_d.subs(x, 1)) == 0,
        "phi_F_equation": sp.simplify(lop(phi_f) - 1 / w) == 0,
        "phi_F_boundaries": sp.simplify(phi_f.subs(x, -1)) == 0 and sp.simplify(t(phi_f).subs(x, 1)) == 0,
        "sherman_morrison": sp.simplify(schur_direct - schur_sm) == 0,
        "finite_beta_elimination": sp.simplify(scalar_trace_form.subs(z, zstar) - tau_beta * q**2) == 0,
        "tau_beta_zero": sp.simplify(tau_beta.subs(beta, 0)) == 0,
        "tau_beta_monotone": sp.simplify(sp.diff(tau_beta, beta) - s**2 / (1 + beta * j) ** 2) == 0,
        "tau_beta_infinite_limit": sp.simplify(sp.limit(tau_beta, beta, sp.oo) - s**2 / j) == 0,
        "tau_beta_inverse": sp.simplify(tau_beta.subs(beta, beta_inverse) - tt) == 0,
    }
    if not all(controls.values()):
        raise AssertionError(controls)
    return controls


def fields(label: str, s, x):
    w = (s * s / 2) * x * x + (s * s - s) * x + 1 + s * s / 2 - s
    wp = s * s * x + s * s - s
    logw = iv.log(w)
    v1 = wp / w
    v1p = s * s / w - wp * wp / (w * w)
    v2 = 1 - 1 / w
    v2p = wp / (w * w)
    if label == "DIRICHLET":
        wr = 1 - 2 * s + 2 * s * s
        coeff_u = -(wr * (1 - iv.log(wr)) + 2 * s - 1) / (wr - 1)
        coeff_phi = 1 / (s * (s - 1))
    else:
        coeff_u = -1 / (2 * s - 1)
        coeff_phi = 2 / (s * (2 * s - 1))
    u = 1 - logw + v1 / s + coeff_u * v2
    up = -wp / w + v1p / s + coeff_u * v2p
    phi = -1 / (s * s) - v1 / (s**3) + coeff_phi * v2
    phip = -v1p / (s**3) + coeff_phi * v2p
    return w, wp, logw, u, up, phi, phip


def densities(label: str, s, x):
    w, wp, logw, u, up, phi, phip = fields(label, s, x)
    diagonal = s * s * logw * logw * (1 - 1 / w)

    def ell(value, derivative):
        return (
            s * s * value * (1 + logw * (1 - 1 / w))
            + logw * wp * derivative
        )

    return {
        "J": 1 / w,
        "S0": diagonal + ell(u, up),
        "n_green": -u / w,
        "n_direct": ell(phi, phip),
        "m_direct": phi / w,
    }


def integrate(label: str, parts: int):
    s = iv.mpf([S_LO, S_HI])
    totals = {name: iv.mpf(0) for name in ("J", "S0", "n_green", "n_direct", "m_direct")}
    width = mp.mpf(2) / parts
    for index in range(parts):
        lo = mp.mpf(-1) + index * width
        hi = lo + width
        values = densities(label, s, iv.mpf([lo, hi]))
        for name, value in values.items():
            totals[name] += value * iv.mpf(width)
    return totals


def nested(coarse, fine) -> bool:
    ca, cb = bounds(coarse)
    fa, fb = bounds(fine)
    return fa >= ca and fb <= cb


def write_controls(controls: dict[str, bool]) -> None:
    with (OUT / "EXACT_CONTROL_LEDGER.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["control", "status"])
        for name, status in controls.items():
            writer.writerow([name, "PASS" if status else "FAIL"])


def write_threshold_surface(report: dict[str, object]) -> None:
    """Emit the certified surface as a compact, machine-readable navigation table."""
    columns = (
        "p_domain", "point_type", "alpha", "t_lo", "t_hi",
        "tau_lo", "tau_hi", "eta_nu_lo", "eta_nu_hi",
        "representative_eta_mu_lo", "representative_eta_mu_hi", "joint_reading",
    )
    with (OUT / "THRESHOLD_SURFACE.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for label, branch in report["branches"].items():
            writer.writerow({
                "p_domain": label,
                "point_type": "FIELD_CROSSING",
                "alpha": "-",
                "t_lo": branch["t_critical_interval"][0],
                "t_hi": branch["t_critical_interval"][1],
                "tau_lo": branch["tau_critical_interval"][0],
                "tau_hi": branch["tau_critical_interval"][1],
                "eta_nu_lo": "+INF",
                "eta_nu_hi": "+INF",
                "representative_eta_mu_lo": "+INF",
                "representative_eta_mu_hi": "+INF",
                "joint_reading": "NO_FINITE_ETA__ZERO_MODE_COUPLES_TO_NU",
            })
            for sample in branch["samples"]:
                writer.writerow({
                    "p_domain": label,
                    "point_type": "ABOVE_CROSSING_SAMPLE",
                    "alpha": sample["alpha"],
                    "t_lo": sample["t_interval"][0],
                    "t_hi": sample["t_interval"][1],
                    "tau_lo": "-",
                    "tau_hi": "-",
                    "eta_nu_lo": sample["eta_critical_interval"][0],
                    "eta_nu_hi": sample["eta_critical_interval"][1],
                    "representative_eta_mu_lo": sample["representative_eta_mu_critical_interval"][0],
                    "representative_eta_mu_hi": sample["representative_eta_mu_critical_interval"][1],
                    "joint_reading": "NONNEGATIVE_IFF_ETA_AT_OR_ABOVE_THRESHOLD",
                })


def main() -> None:
    controls = symbolic_controls()
    write_controls(controls)
    iv.dps = 100
    root_left = root_equation(iv.mpf(S_LO))
    root_right = root_equation(iv.mpf(S_HI))
    if bounds(root_left)[1] >= 0 or bounds(root_right)[0] <= 0:
        raise AssertionError("root bracket lost")

    report = {
        "status": "TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED",
        "scope": "conditional F01 local massive crease root; trace-aligned tau/eta wall-Hessian slice only",
        "root_bracket": [S_LO, S_HI],
        "root_endpoint_intervals": {"left": endpoints(root_left), "right": endpoints(root_right)},
        "coordinate_definitions": {
            "beta": "nonnegative normalized finite aligned angular trace-difference Hessian coordinate before elimination; free-and-explored only",
            "tau": "effective angular-trace rank-one coefficient in A_tau=A0+tau|g><g|",
            "tau_of_beta": "s^2*beta/(1+beta*J)",
            "tau_infinity": "s^2/J; zero-angular-trace R06 field-core limit",
            "R06_endpoint_beta": "+infinity only",
            "t": "tau/tau_infinity",
            "eta": "direct dimensionless nu^2 wall curvature; nu=k*mu",
            "representative_eta_mu": "eta/4 for a_F=a_Fprime=2",
        },
        "branches": {},
        "symbolic_controls": controls,
        "versions": {"python": platform.python_version(), "sympy": sp.__version__, "mpmath": mp.__version__},
        "conclusion_ceiling": "inverse threshold target only; no wall response, boundary, action, carrier, source, matter, time persistence, mass, or bootstrap law selected",
    }

    s_iv = iv.mpf([S_LO, S_HI])
    for label in ("DIRICHLET", "FREE"):
        iv.dps = 80
        coarse = integrate(label, COARSE_PARTS)
        iv.dps = 100
        fine = integrate(label, FINE_PARTS)
        if not all(nested(coarse[name], fine[name]) for name in fine):
            raise AssertionError(f"non-nested interval: {label}")
        if not overlaps(fine["n_green"], fine["n_direct"]):
            raise AssertionError(f"Green/direct n mismatch: {label}")
        # Use the narrower overlap hull only as a comparison; the primary n is the
        # direct Green identity -integral u/w.
        j = fine["J"]
        s0 = fine["S0"]
        n = fine["n_green"]
        if bounds(j)[0] <= 0 or bounds(s0)[0] <= 0 or bounds(n)[0] * bounds(n)[1] <= 0:
            raise AssertionError(f"load-bearing sign not certified: {label}")
        wr = 1 - 2 * s_iv + 2 * s_iv * s_iv
        if label == "DIRICHLET":
            d = 2 / (s_iv - 1)
        else:
            d = 2 * (4 * s_iv * s_iv - 3 * s_iv + 1) / ((2 * s_iv - 1) * wr)
        tau_inf = s_iv * s_iv / j
        tcrit = j / (j + d)
        m_formula = -(j + d) / (s_iv * s_iv)
        tau_crit = -1 / m_formula
        if not overlaps(fine["m_direct"], m_formula):
            raise AssertionError(f"direct/formula m mismatch: {label}")
        if not (0 < bounds(tcrit)[0] < bounds(tcrit)[1] < 1):
            raise AssertionError(f"critical fraction invalid: {label}")
        samples = []
        for alpha_fraction in ALPHAS:
            alpha = iv.mpf(alpha_fraction.numerator) / alpha_fraction.denominator
            t = iv.mpf(1) if alpha_fraction == 1 else (j + alpha * d) / (j + d)
            # Exact simplification of S0 + tau*n^2/(1+tau*m) at the frozen node.
            schur = s0 - s_iv * s_iv * n * n * (j + alpha * d) / (alpha * d * (j + d))
            eta = -schur
            eta_mu = eta / 4
            if bounds(schur)[1] >= 0 or bounds(eta)[0] <= 0:
                raise AssertionError(f"threshold sign not certified: {label} alpha={alpha_fraction}")
            samples.append({
                "alpha": f"{alpha_fraction.numerator}/{alpha_fraction.denominator}",
                "t_interval": endpoints(t),
                "S_nu_interval": endpoints(schur),
                "eta_critical_interval": endpoints(eta),
                "representative_eta_mu_critical_interval": endpoints(eta_mu),
                "field_core": "POSITIVE",
                "joint_condition": "eta>=eta_critical; equality is semidefinite",
            })
        report["branches"][label] = {
            "coarse": {name: endpoints(value) for name, value in coarse.items()},
            "fine": {name: endpoints(value) for name, value in fine.items()},
            "fine_nested_in_coarse": True,
            "n_green_direct_overlap": True,
            "d_interval": endpoints(d),
            "m_formula_interval": endpoints(m_formula),
            "m_direct_formula_overlap": True,
            "tau_infinity_interval": endpoints(tau_inf),
            "t_critical_interval": endpoints(tcrit),
            "tau_critical_interval": endpoints(tau_crit),
            "region_below_crossing": "field index one; no eta can repair",
            "at_crossing": "field zero mode couples to nu because n excludes zero; no finite eta can repair",
            "eta_at_crossing": "+infinity",
            "region_above_crossing": "field core positive; joint nonnegative iff eta>=-S_nu(tau)",
            "samples": samples,
        }

    (OUT / "PRIMARY_CERTIFICATE.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_threshold_surface(report)
    result = {
        "primary_outcome": report["status"],
        "branches": 2,
        "owned_domains_covered": 4,
        "sample_nodes_per_branch": len(ALPHAS),
        "computed_controls_passed": len(controls),
        "computed_controls_total": len(controls),
        "all_certified_eta_thresholds_positive": True,
        "tau_eta_selected": False,
        "complete_wall_hessian_covered": False,
        "gpu_used": False,
    }
    (OUT / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
