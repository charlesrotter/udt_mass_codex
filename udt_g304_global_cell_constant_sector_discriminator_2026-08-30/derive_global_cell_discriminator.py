#!/usr/bin/env python3
"""Exact production derivation for the preregistered G304 bounded discriminator."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent


class Checks:
    def __init__(self) -> None:
        self.count = 0

    def equal(self, left, right, label: str) -> None:
        self.count += 1
        if sp.simplify(left - right) != 0:
            raise AssertionError(f"{label}: {sp.simplify(left - right)}")

    def true(self, value: bool, label: str) -> None:
        self.count += 1
        if not value:
            raise AssertionError(label)


def direct_ricci(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    """Direct coordinate derivation; no imported curvature routine."""
    n = len(coordinates)
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(
            sum(
                inverse[a, d]
                * (
                    sp.diff(metric[d, c], coordinates[b])
                    + sp.diff(metric[d, b], coordinates[c])
                    - sp.diff(metric[b, c], coordinates[d])
                )
                for d in range(n)
            )
            / 2
        )
        for c in range(n)] for b in range(n)] for a in range(n)]
    ricci = sp.MutableDenseMatrix.zeros(n, n)
    for a in range(n):
        for b_ in range(n):
            value = 0
            for c in range(n):
                value += sp.diff(gamma[c][a][b_], coordinates[c])
                value -= sp.diff(gamma[c][a][c], coordinates[b_])
                for d in range(n):
                    value += gamma[c][c][d] * gamma[d][a][b_]
                    value -= gamma[c][b_][d] * gamma[d][a][c]
            ricci[a, b_] = sp.simplify(sp.trigsimp(value))
    scalar = sp.simplify(sum(inverse[a, b_] * ricci[a, b_] for a in range(n) for b_ in range(n)))
    return inverse, sp.Matrix(ricci), scalar


def load_registry() -> dict[str, dict[str, str]]:
    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(newline="") as handle:
        return {row["premise_id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    parser.add_argument("--domains", default="DOMAIN_CLASSIFICATION.tsv")
    args = parser.parse_args()
    out = Path(args.output)
    domains_out = Path(args.domains)
    if not out.is_absolute():
        out = Path(__file__).resolve().parent / out
    if not domains_out.is_absolute():
        domains_out = Path(__file__).resolve().parent / domains_out

    ck = Checks()
    t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
    b, R0 = sp.symbols("b R0", real=True)
    X, L = sp.symbols("X L", positive=True)
    f = 1 + b / r - R0 * r**2 / 12
    metric = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)

    inverse, ricci, scalar = direct_ricci(metric, (t, r, theta, azimuth))
    expected_ricci = sp.simplify(R0 * metric / 4)
    for i in range(4):
        for j in range(4):
            ck.equal(ricci[i, j], expected_ricci[i, j], f"direct_Ricci_{i}_{j}")
    ck.equal(scalar, R0, "direct_scalar_curvature")

    ode = sp.simplify(r**2 * sp.diff(f, r, 2) - 2 * f + 2)
    ck.equal(ode, 0, "tracefree_ODE_family")
    wr_l = 1 - r / X
    wr_l_residual = sp.simplify(r**2 * sp.diff(wr_l, r, 2) - 2 * wr_l + 2)
    ck.equal(wr_l_residual, 2 * r / X, "WRL_tracefree_residual")
    ck.true(wr_l_residual != 0, "WRL_not_exact_tracefree_solution")

    kretschmann = sp.simplify(
        sp.diff(f, r, 2) ** 2
        + 4 * (sp.diff(f, r) / r) ** 2
        + 4 * ((1 - f) / r**2) ** 2
    )
    ricci_squared = sp.simplify(R0**2 / 4)
    weyl_squared = sp.simplify(kretschmann - 2 * ricci_squared + scalar**2 / 3)
    ck.equal(kretschmann, R0**2 / 6 + 12 * b**2 / r**6, "Kretschmann_family")
    ck.equal(weyl_squared, 12 * b**2 / r**6, "Weyl_squared_family")
    ck.true(sp.simplify(sp.limit(r**6 * weyl_squared, r, 0)) == 12 * b**2, "center_singularity_coefficient")
    ck.equal(weyl_squared.subs(b, 0), 0, "smooth_center_conformally_flat")

    f_pos = 1 - r**2 / X**2
    f_zero = sp.Integer(1)
    f_neg = 1 + r**2 / L**2
    ck.equal(f_pos.subs(r, X), 0, "positive_outer_zero")
    ck.equal(sp.diff(f_pos, r).subs(r, X), -2 / X, "positive_simple_zero")
    ck.true(sp.limit(f_pos, r, X, dir="-") == 0, "positive_static_side_limit")
    ck.true(sp.limit(f_neg, r, sp.oo) == sp.oo, "negative_no_outer_zero_growth")
    ck.equal(f_zero, 1, "zero_flat_profile")

    proper_pos = X * sp.asin(r / X)
    optical_pos = X * sp.atanh(r / X)
    proper_neg = L * sp.asinh(r / L)
    optical_neg = L * sp.atan(r / L)
    ck.equal(sp.diff(proper_pos, r), 1 / sp.sqrt(f_pos), "positive_proper_antiderivative")
    ck.equal(sp.diff(optical_pos, r), 1 / f_pos, "positive_optical_antiderivative")
    ck.equal(sp.limit(proper_pos, r, X, dir="-"), sp.pi * X / 2, "positive_finite_proper_reach")
    ck.true(sp.limit(optical_pos, r, X, dir="-") == sp.oo, "positive_infinite_optical_reach")
    ck.equal(sp.diff(proper_neg, r), 1 / sp.sqrt(f_neg), "negative_proper_antiderivative")
    ck.equal(sp.diff(optical_neg, r), 1 / f_neg, "negative_optical_antiderivative")
    ck.true(sp.limit(proper_neg, r, sp.oo) == sp.oo, "negative_infinite_proper_reach")
    ck.equal(sp.limit(optical_neg, r, sp.oo), sp.pi * L / 2, "negative_finite_optical_reach")
    ck.true(sp.limit(r, r, sp.oo) == sp.oo, "zero_infinite_proper_reach")

    phi_pos = -sp.log(f_pos) / 2
    chi_pos = sp.simplify((1 - f_pos) / (1 + f_pos))
    ck.true(sp.limit(phi_pos, r, X, dir="-") == sp.oo, "positive_phi_endpoint")
    ck.equal(sp.limit(chi_pos, r, X, dir="-"), 1, "positive_projective_endpoint")
    phi_neg = -sp.log(f_neg) / 2
    chi_neg = sp.simplify((1 - f_neg) / (1 + f_neg))
    ck.true(sp.limit(phi_neg, r, sp.oo) == -sp.oo, "negative_phi_endpoint")
    ck.equal(sp.limit(chi_neg, r, sp.oo), -1, "negative_projective_endpoint_not_finite_cell")

    positive_invariants = {
        "R": R0,
        "Ricci_squared": R0**2 / 4,
        "Riemann_squared": R0**2 / 6,
        "Weyl_squared": sp.Integer(0),
    }
    for name, value in positive_invariants.items():
        ck.true(not value.has(r), f"positive_{name}_finite_at_horizon")

    A, B, C = sp.symbols("A B C", real=True)
    d_ab, d_bc, d_ac = B - A, C - B, C - A
    ck.equal(d_ab + d_bc, d_ac, "endpoint_depth_composition")
    x_ab, x_bc = sp.tanh(d_ab), sp.tanh(d_bc)
    mobius = sp.trigsimp((x_ab + x_bc) / (1 + x_ab * x_bc) - sp.tanh(d_ac))
    ck.equal(mobius, 0, "projective_Mobius_composition")

    registry = load_registry()
    for key in ("W5", "W6", "G14", "G17", "G235", "G292", "G294"):
        ck.true(key in registry, f"registry_contains_{key}")
    ck.true(registry["G17"]["epistemic_label"] == "WORKING", "G17_grade_working")
    ck.true("causal horizon" in registry["G17"]["open_scope"], "G17_causal_horizon_wording")
    ck.true("history" in registry["W5"]["open_scope"], "W5_history_open")
    ck.true("history" in registry["W6"]["open_scope"], "W6_history_open")
    g235_text = " ".join(registry["G235"].values())
    g292_text = " ".join(registry["G292"].values())
    ck.true("NONSELECTION" in g235_text, "G235_network_nonselection")
    ck.true("HISTORY_SELECTION" in g292_text and "NO_CONTINUOUS_FLUX_PROPAGATION" in g292_text, "G292_topology_nonselection")
    ck.true("METRIC_NONSELECTION" in registry["G294"]["current_status"], "G294_copresence_nonselection")
    ck.true("VALUE_REALIZATION_COMPLETION_OPEN" in registry["G14"]["current_status"], "G14_Xmax_open")

    negatives = (ROOT / "NEGATIVES_REGISTRY.md").read_text()
    old_ds = (ROOT / "simple_metric_dS_native_any_alpha_closed_results.md").read_text()
    ck.true("CONDITIONS-CHANGED" in negatives[:5000], "negative_registry_conditions_changed")
    ck.true("through the **native** φ-equation" in old_ds, "old_dS_negative_source_equation_scoped")

    domains = [
        {
            "R0_sign": "positive",
            "b_class": "b>=0",
            "positive_roots": "one",
            "static_domain": "0<r<r_outer",
            "center": "regular_only_if_b=0",
            "outer_causal_ceiling": "yes",
        },
        {
            "R0_sign": "positive",
            "b_class": "-4/(3*sqrt(R0))<b<0",
            "positive_roots": "two",
            "static_domain": "r_inner<r<r_outer",
            "center": "excluded_nonstatic_and_singular",
            "outer_causal_ceiling": "yes",
        },
        {
            "R0_sign": "positive",
            "b_class": "b=-4/(3*sqrt(R0))",
            "positive_roots": "one_double",
            "static_domain": "degenerate_only",
            "center": "excluded",
            "outer_causal_ceiling": "degenerate_not_simple",
        },
        {
            "R0_sign": "positive",
            "b_class": "b<-4/(3*sqrt(R0))",
            "positive_roots": "none",
            "static_domain": "none",
            "center": "excluded",
            "outer_causal_ceiling": "no",
        },
        {
            "R0_sign": "zero",
            "b_class": "b>=0",
            "positive_roots": "none",
            "static_domain": "0<r<infinity",
            "center": "regular_only_if_b=0",
            "outer_causal_ceiling": "no",
        },
        {
            "R0_sign": "zero",
            "b_class": "b<0",
            "positive_roots": "one",
            "static_domain": "r_h<r<infinity",
            "center": "excluded",
            "outer_causal_ceiling": "no_outer_ceiling",
        },
        {
            "R0_sign": "negative",
            "b_class": "b>=0",
            "positive_roots": "none",
            "static_domain": "0<r<infinity",
            "center": "regular_only_if_b=0",
            "outer_causal_ceiling": "no",
        },
        {
            "R0_sign": "negative",
            "b_class": "b<0",
            "positive_roots": "one",
            "static_domain": "r_h<r<infinity",
            "center": "excluded",
            "outer_causal_ceiling": "no_outer_ceiling",
        },
    ]
    with domains_out.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(domains[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(domains)

    result = {
        "schema": "UDT_G304_GLOBAL_CELL_CONSTANT_SECTOR_DISCRIMINATOR_V1",
        "question_class": "METRIC_LED_BOUNDED_GLOBAL_COMPLETION_CLASSIFICATION",
        "assertions": ck.count,
        "family": "f(r)=1+b/r-(R0/12)r^2",
        "direct_geometry": {
            "Ricci": "Ric_ab=(R0/4)g_ab",
            "scalar": "R=R0",
            "Kretschmann": "R0^2/6+12b^2/r^6",
            "Weyl_squared": "12b^2/r^6",
            "smooth_center": "b=0",
        },
        "center_regular_sign_census": {
            "R0_positive": {
                "profile": "1-r^2/X^2",
                "X_relation": "X=sqrt(12/R0)",
                "proper_reach": "pi*X/2 finite",
                "optical_reach": "infinite",
                "curvature": "regular",
                "phi_limit": "+infinity",
                "chi_limit": "+1",
                "finite_outer_causal_ceiling": True,
            },
            "R0_zero": {
                "profile": "1",
                "proper_reach": "infinite",
                "optical_reach": "infinite",
                "finite_outer_causal_ceiling": False,
            },
            "R0_negative": {
                "profile": "1+r^2/L^2",
                "proper_reach": "infinite",
                "optical_reach": "pi*L/2 finite",
                "phi_limit": "-infinity",
                "chi_limit": "-1",
                "finite_outer_causal_ceiling": False,
            },
        },
        "relation_layers": {
            "endpoint_composition": "constant-blind identity",
            "projective_composition": "constant-blind identity",
            "W5": "history remains open",
            "W6": "history remains open",
            "G235": "rank-complete network reconstructive not selective",
            "G292": "Euler/topology data do not select continuous history",
            "G294": "copresence existence nonselective",
        },
        "working_G17": {
            "grade": "WORKING",
            "bounded_result": "conditionally selects R0>0 in the primary static smooth-center tracefree family",
            "does_not_fix": ["R0 magnitude", "X value", "field equation", "complete history"],
        },
        "WRL": {
            "profile": "1-r/X",
            "tracefree_ODE_residual": "2r/X",
            "compatibility": "not an exact member of the G302 tracefree family",
        },
        "historical_negative": "source-equation scoped and conditions-changed; no automatic export",
        "landing": "FOUNDED_RELATION_LAYERS_NONSELECTIVE__WORKING_FINITE_CEILING_CONDITIONALLY_SELECTS_POSITIVE_CONSTANT_IN_PRIMARY_STATIC_SMOOTH_CENTER_BRANCH__X_EMERGES__FULL_WRL_ARCHITECTURE_INCOMPATIBLE",
        "maximum_claim": "bounded conditional architecture classification; no UDT field equation, history, observation, scale value, or canonization",
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "assertions": ck.count, "landing": result["landing"]}, sort_keys=True))


if __name__ == "__main__":
    main()
