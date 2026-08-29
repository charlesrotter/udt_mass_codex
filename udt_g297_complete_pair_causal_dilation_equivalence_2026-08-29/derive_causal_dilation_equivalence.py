#!/usr/bin/env python3
"""Dependency-free exact checks for the bounded G297 derivation."""

from fractions import Fraction as F
import json
from pathlib import Path


def require(name, condition, checks):
    if not condition:
        raise AssertionError(name)
    checks[name] = True


def radar_rate(outgoing_slope, return_slope):
    """db/d[(a_minus+a_plus)/2] from the two physical null-leg slopes."""
    return F(2, 1) / (F(1, 1) / outgoing_slope + return_slope)


def moving_flat(q):
    # q=exp(eta), cosh=(q+q^-1)/2, sinh=(q-q^-1)/2.
    gamma = (q + F(1, 1) / q) / 2
    mutual = F(1, 1) / gamma
    a_radar = radar_rate(q, q)
    # The B-centered diamond assigns A-event a the B-radar midpoint
    # beta_B(a)=[q^-1(a-L)+q(a+L)]/2, so da/d beta_B is reciprocal to
    # the displayed derivative; the intercept L drops out.
    beta_b_prime = (F(1, 1) / q + q) / 2
    b_radar = F(1, 1) / beta_b_prime
    return {
        "gamma": gamma,
        "mutual": mutual,
        "a_radar": a_radar,
        "b_radar": b_radar,
        "outgoing": q,
        "inverse": F(1, 1) / q,
        "future_return": q,
        "b_fermi": gamma,
    }


def static_lapse(p):
    # p=N_B/N_A.  The same fixed-radius null travel time cancels from first germs.
    a_sees_b = radar_rate(p, F(1, 1) / p)
    b_sees_a = radar_rate(F(1, 1) / p, p)
    mutual = F(2, 1) / (p + F(1, 1) / p)
    return a_sees_b, b_sees_a, mutual


def transport_screen(r, w2):
    gamma = (r + F(1, 1) / r) / 2 + r * w2 / 2
    mutual = F(1, 1) / gamma
    planar = F(2, 1) / (r + F(1, 1) / r)
    return gamma, mutual, planar


def w1_completion(T, L, beta):
    h00 = -(T * T)
    h01 = -(T * T) * beta
    h11 = L * L - (T * T) * beta * beta
    det = h00 * h11 - h01 * h01
    m = T * L
    Ls = L / m
    return h00, h01, h11, det, m, T * Ls


def null_hessian(Txx, Txy, Tyy):
    # Reconstruct -Hessian(a) by exact centered differences from samples of
    # a(x,y)=-1/2(Txx*x^2+2*Txy*x*y+Tyy*y^2), rather than returning T directly.
    def a(x, y):
        return -F(1, 2) * (Txx * x * x + 2 * Txy * x * y + Tyy * y * y)

    hx, hy = F(2, 3), F(3, 5)
    dxx = (a(hx, 0) - 2 * a(0, 0) + a(-hx, 0)) / (hx * hx)
    dyy = (a(0, hy) - 2 * a(0, 0) + a(0, -hy)) / (hy * hy)
    dxy = (
        a(hx, hy) - a(hx, -hy) - a(-hx, hy) + a(-hx, -hy)
    ) / (4 * hx * hy)
    return ((-dxx, -dxy), (-dxy, -dyy))


def main():
    checks = {}

    for q in (F(2, 1), F(3, 2), F(5, 3), F(7, 4), F(11, 5)):
        row = moving_flat(q)
        require(f"flat_A_radar_{q}", row["a_radar"] == row["mutual"], checks)
        require(f"flat_B_radar_{q}", row["b_radar"] == row["mutual"], checks)
        require(f"flat_return_not_inverse_{q}", row["future_return"] != row["inverse"], checks)
        require(f"flat_radar_not_null_{q}", row["a_radar"] != row["outgoing"], checks)
        require(f"flat_radar_not_B_Fermi_{q}", row["a_radar"] != row["b_fermi"], checks)

    nonidentity_witnesses = []
    for p in (F(2, 1), F(3, 2), F(5, 4), F(7, 3)):
        ab, ba, mutual = static_lapse(p)
        require(f"static_A_rate_{p}", ab == p, checks)
        require(f"static_B_rate_{p}", ba == F(1, 1) / p, checks)
        require(f"static_directional_product_{p}", ab * ba == 1, checks)
        require(f"static_naive_scalar_fails_AB_{p}", ab != mutual, checks)
        require(f"static_naive_scalar_fails_BA_{p}", ba != mutual, checks)
        nonidentity_witnesses.append(
            {"p": str(p), "R_A_from_B": str(ab), "R_B_from_A": str(ba), "M_PT": str(mutual)}
        )

    for r in (F(1, 2), F(2, 3), F(3, 2), F(5, 2)):
        gamma0, m0, planar0 = transport_screen(r, F(0, 1))
        require(f"screen_planar_equality_{r}", m0 == planar0, checks)
        require(f"screen_gamma_ge_one_{r}", gamma0 >= 1, checks)
        for w2 in (F(1, 7), F(2, 5), F(3, 2)):
            gamma, mutual, planar = transport_screen(r, w2)
            require(f"screen_strict_{r}_{w2}", mutual < planar, checks)
            require(f"screen_positive_{r}_{w2}", mutual > 0, checks)
            reverse_r = F(1, 1) / r
            reverse_w2 = r * r * w2
            reverse_gamma, reverse_mutual, _ = transport_screen(reverse_r, reverse_w2)
            require(f"screen_reversal_gamma_{r}_{w2}", reverse_gamma == gamma, checks)
            require(f"screen_reversal_mutual_{r}_{w2}", reverse_mutual == mutual, checks)

    for T, L, beta in (
        (F(2), F(3), F(1, 5)),
        (F(5, 2), F(7, 3), F(-2, 7)),
        (F(11, 4), F(9, 5), F(3, 8)),
    ):
        h00, h01, h11, det, m, product = w1_completion(T, L, beta)
        require(f"w1_det_{T}_{L}_{beta}", det == -(T * L) ** 2, checks)
        require(f"w1_density_{T}_{L}_{beta}", m * m == -det, checks)
        require(f"w1_identity_{T}_{L}_{beta}", product == 1, checks)
        require(f"w1_regular_{T}_{L}_{beta}", h00 < 0 and det < 0, checks)

    tidal_cases = []
    for vals in ((F(2), F(3), F(5)), (F(-1), F(4), F(7)), (F(0), F(-2), F(9))):
        matrix = null_hessian(*vals)
        require(f"tide_xx_{vals}", matrix[0][0] == vals[0], checks)
        require(f"tide_xy_{vals}", matrix[0][1] == vals[1] == matrix[1][0], checks)
        require(f"tide_yy_{vals}", matrix[1][1] == vals[2], checks)
        tidal_cases.append([[str(v) for v in row] for row in matrix])

    # Constant homothety multiplies both proper clocks, so every first-germ ratio is unchanged.
    for lam in (F(2), F(3, 2), F(7, 3)):
        numerator, denominator = F(5, 7), F(11, 13)
        require(
            f"homothety_clock_ratio_{lam}",
            (lam * numerator) / (lam * denominator) == numerator / denominator,
            checks,
        )

    result = {
        "landing_candidate": (
            "OWNER_CLARIFICATION_IS_SUBSTANTIVE_BUT_THE_TWO_LEG_COMPLETE_TRANSFER_REMAINS_UNDERDEFINED"
            "__NO_UNIQUE_NONIDENTITY_FORM_YET"
        ),
        "check_count": len(checks),
        "all_pass": all(checks.values()),
        "static_naive_scalar_countermodels": nonidentity_witnesses,
        "tidal_hessian_examples": tidal_cases,
        "qualifications": [
            "radar midpoint conditionally selects only the causal clock-correspondence component",
            "the map from a two-leg causal family to a rank-two complete pair germ remains open",
            "a full directional null-delay family is required before complete screen/tidal reconstruction",
            "W1 evaluates every regular selected pullback and is not itself a metric-history residual",
            "no global history, branch population, scale, field equation, or X_max is selected",
        ],
        "load_bearing_complete_transfer_verified": False,
    }
    output = Path(__file__).with_name("DERIVATION_RESULT.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
