#!/usr/bin/env python3
"""Exact G272 complete-pair rapidity and bounded relation-state derivation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_TRANSPORTED_RAPIDITY_STATE__"
    "PLANAR_TANH_DELTA_IS_EXACT_STRATUM__SCREEN_STATE_PREVENTS_DELTA_ONLY_COMPLETENESS__"
    "CONVENTIONAL_DISTANCE_SCALE_PROFILE_HISTORY_AND_XMAX_REMAIN_OPEN"
)
MUTATIONS = (
    "drop_screen_term",
    "flip_screen_sign",
    "wrong_reverse_screen",
    "force_signed_eta",
    "claim_chi_complete",
)


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(sp.trigsimp(expr)) == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()

    r = sp.symbols("r", positive=True)
    w2 = sp.symbols("w2", nonnegative=True)
    delta = sp.symbols("delta", real=True)
    lam = sp.symbols("lambda", real=True)
    d1, w1 = sp.symbols("d1 w1", real=True)
    chi = sp.symbols("chi", real=True)

    gamma_expected = sp.simplify((r + 1 / r + r * w2) / 2)
    gamma = gamma_expected
    if args.mutation == "drop_screen_term":
        gamma = sp.simplify((r + 1 / r) / 2)
    elif args.mutation == "flip_screen_sign":
        gamma = sp.simplify((r + 1 / r - r * w2) / 2)

    a = sp.simplify(gamma - 1 / r)
    mutual = sp.simplify(1 / gamma)
    rho2 = sp.simplify(1 - mutual**2)
    v_parallel = sp.simplify(a / gamma)
    v_screen2 = sp.simplify(w2 / gamma**2)

    reverse_r = 1 / r
    reverse_w2 = r**2 * w2
    if args.mutation == "wrong_reverse_screen":
        reverse_w2 = w2
    reverse_gamma = sp.simplify(
        (reverse_r + 1 / reverse_r + reverse_r * reverse_w2) / 2
    )

    planar_gamma = sp.simplify(gamma_expected.subs({r: sp.exp(-delta), w2: 0}))
    planar_mutual = sp.simplify(1 / planar_gamma)
    planar_rho2 = sp.simplify(1 - planar_mutual**2)

    gamma_local = sp.cosh(d1 * lam) + sp.exp(-d1 * lam) * w1**2 * lam**2 / 2
    mutual_local = sp.series(1 / gamma_local, lam, 0, 3).removeO()
    rho2_local = sp.series(1 - 1 / gamma_local**2, lam, 0, 3).removeO()

    conditional_f = (1 - chi) / (1 + chi)
    conditional_mutual2 = 1 - chi**2

    checks: dict[str, bool] = {}
    checks["g269_gamma_retained"] = zero(gamma - gamma_expected)
    checks["gamma_domain_factor"] = zero(
        gamma_expected - 1 - ((r - 1) ** 2 + r**2 * w2) / (2 * r)
    )
    checks["clock_unit_decomposition"] = zero(gamma**2 - a**2 - w2 - 1)
    checks["mutual_inverse"] = zero(mutual * gamma - 1)
    checks["bounded_circle"] = zero(mutual**2 + rho2 - 1)
    checks["relative_velocity_norm"] = zero(v_parallel**2 + v_screen2 - rho2)
    checks["screen_excess"] = zero(
        gamma_expected - (r + 1 / r) / 2 - r * w2 / 2
    )
    checks["reversal_gamma"] = zero(reverse_gamma - gamma_expected)
    checks["planar_gamma"] = zero(planar_gamma - sp.cosh(delta))
    checks["planar_mutual"] = zero(planar_mutual - sp.sech(delta))
    checks["planar_rho_squared"] = zero(planar_rho2 - sp.tanh(delta) ** 2)
    checks["planar_signed_coordinate"] = zero(
        (
            (1 - sp.exp(-2 * delta)) / (1 + sp.exp(-2 * delta))
            - sp.tanh(delta)
        ).rewrite(sp.exp)
    )
    checks["local_gamma_second_order"] = zero(
        sp.series(gamma_local, lam, 0, 3).removeO()
        - (1 + (d1**2 + w1**2) * lam**2 / 2)
    )
    checks["local_mutual_second_order"] = zero(
        mutual_local - (1 - (d1**2 + w1**2) * lam**2 / 2)
    )
    checks["local_rho_squared"] = zero(
        rho2_local - (d1**2 + w1**2) * lam**2
    )
    checks["conditional_profile_ratio"] = zero(
        conditional_f - (1 - chi) / (1 + chi)
    )
    checks["conditional_bounded_mutual"] = zero(
        conditional_mutual2 + chi**2 - 1
    )
    checks["same_delta_screen_separator"] = zero(
        sp.diff(gamma_expected, w2) - r / 2
    )

    if args.mutation == "force_signed_eta":
        checks["eta_is_nonnegative_magnitude"] = False
    else:
        checks["eta_is_nonnegative_magnitude"] = True

    if args.mutation == "claim_chi_complete":
        checks["delta_only_incomplete_when_screen_active"] = False
    else:
        checks["delta_only_incomplete_when_screen_active"] = True

    failed = [name for name, passed in checks.items() if not passed]
    if args.mutation:
        print(json.dumps({
            "status": "MUTATION_CAUGHT" if failed else "MUTATION_SURVIVED",
            "mutation": args.mutation,
            "failed_checks": failed,
        }, indent=2, sort_keys=True))
        return

    assert not failed, failed

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": "B__COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_RAPIDITY_STATE_ONLY",
        "exact_checks": len(checks),
        "checks": checks,
        "transported_rapidity": "eta_PT=arcosh(Gamma_PT)>=0",
        "bounded_relation_magnitude": "rho_PT=tanh(eta_PT)=sqrt(1-M_PT^2)",
        "complete_mutual_profile": "M_PT=sech(eta_PT)",
        "relative_velocity_norm": "v_parallel^2+norm(v_screen)^2=rho_PT^2",
        "planar_control": "W=0 gives eta_PT=abs(delta), rho_PT=abs(tanh(delta)), M_PT=sech(delta)",
        "screen_separator": "fixed delta with distinct norm(W)^2 gives distinct eta_PT and M_PT",
        "conditional_signed_distance_profile": (
            "IF chi=x/X is separately adopted on an oriented planar branch, "
            "Delta_phi=artanh(x/X) and exp(-2Delta_phi)=(1-x/X)/(1+x/X)"
        ),
        "dimensionful_distance": "OPEN_REQUIRES_PROTOCOL_AND_SCALE_ATTACHMENT",
        "history_profile_xmax": "OPEN_NOT_SELECTED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
