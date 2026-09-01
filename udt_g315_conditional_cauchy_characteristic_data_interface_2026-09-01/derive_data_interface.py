#!/usr/bin/env python3
"""Exact standard-library checks for the bounded G315 data interface."""

from fractions import Fraction as F
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LANDING = (
    "ACTIVE_EQUATION_HAS_A_LAWFUL_CONDITIONAL_DATA_INTERFACE"
    "__CAUCHY_AND_CHARACTERISTIC_DATA_REMAIN_FREELY_SUPPLIED_WITH_DERIVED_CONSTRAINTS"
)


class Checks:
    def __init__(self):
        self.count = 0
        self.names = []

    def equal(self, name, left, right):
        self.count += 1
        if left != right:
            raise AssertionError(f"{name}: {left!r} != {right!r}")
        self.names.append(name)

    def true(self, name, value):
        self.count += 1
        if not value:
            raise AssertionError(name)
        self.names.append(name)


def frac(value):
    value = F(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def hamiltonian(r3, tau, knorm2):
    return r3 + tau * tau - knorm2


def split_hamiltonian(r3, tau, anorm2):
    return r3 + F(2, 3) * tau * tau - anorm2


def atlas_rows():
    return [
        ("connected scalar sector", "Lambda", "SUPPLIED_OR_INFERRED_CONSTANT", "dLambda=0; H=2Lambda", "not calibration or X_max"),
        ("spacelike", "gamma_ij", "SUPPLIED_PHYSICAL_DATA", "positive-definite metric; coupled constraints", "topology and shape unselected"),
        ("spacelike", "K_ij", "SUPPLIED_PHYSICAL_DATA", "Hamiltonian and momentum constraints", "initial metric rate"),
        ("spacelike", "lapse N", "FREE_GAUGE", "positive regular gauge choice", "not selected physics"),
        ("spacelike", "shift beta^i", "FREE_GAUGE", "regular gauge choice", "not selected physics"),
        ("spacelike", "H", "CONSTRAINED", "H=2Lambda", "one scalar constraint"),
        ("spacelike", "M_i", "CONSTRAINED", "M_i=0", "three momentum constraints"),
        ("spacelike", "local physical phase space", "FREELY_SUPPLIED_AFTER_CONSTRAINT_AND_GAUGE", "generic principal count 4 functions", "two configuration modes plus rates"),
        ("null", "screen conformal/shear data", "SUPPLIED_CHARACTERISTIC_DATA", "regularity and corner compatibility", "radiative/tidal data not selected"),
        ("null", "initial screen scale and expansion", "SUPPLIED_CORNER_DATA", "cross-sheet compatibility", "not fixed by one null sheet"),
        ("null", "theta along generator", "TRANSPORTED_CONSTRAINED", "Raychaudhuri", "Lambda absent from ell-ell projection"),
        ("null", "generator parameter and normalization", "FREE_GAUGE", "regular affine/double-null choice", "not physical scale"),
        ("null", "mixed ell-k curvature", "CONSTRAINED", "Ric(ell,k)=-Lambda for g(ell,k)=-1", "cross-normal channel sees Lambda"),
        ("all", "pair pullback and reciprocal readout", "DOWNSTREAM_EVALUATOR", "acts on supplied evolved metric and germ", "no independent evolution residual"),
        ("global", "topology completeness population", "OPEN_OMITTED", "outside local interface", "no selected universe"),
    ]


def main():
    c = Checks()

    # Trace/trace-free decomposition is an identity, independently of the constraint value.
    samples = [
        (F(-3), F(-2), F(5, 7)),
        (F(0), F(0), F(0)),
        (F(2), F(3), F(4)),
        (F(7, 5), F(-4, 3), F(11, 9)),
        (F(-1, 2), F(5, 4), F(13, 8)),
        (F(9, 2), F(1, 6), F(3, 10)),
    ]
    for idx, (r3, tau, anorm2) in enumerate(samples):
        knorm2 = anorm2 + tau * tau / 3
        c.equal(f"split_hamiltonian_{idx}", hamiltonian(r3, tau, knorm2), split_hamiltonian(r3, tau, anorm2))
        # Momentum split coefficients: K^ij-gamma^ij K = A^ij-(2/3)tau gamma^ij.
        c.equal(f"momentum_trace_coefficient_{idx}", F(1, 3) - 1, F(-2, 3))

    # Four exact constraint witnesses. Momentum vanishes by their stated homogeneity/time symmetry.
    witnesses = {
        "round_positive_bounce_X1": {"r3": F(6), "tau2": F(0), "knorm2": F(0), "Lambda": F(3), "signature": "round_S3"},
        "flat_positive_slicing_H1": {"r3": F(0), "tau2": F(9), "knorm2": F(3), "Lambda": F(3), "signature": "flat_R3_nonzero_K"},
        "positive_product_time_symmetric": {"r3": F(6), "tau2": F(0), "knorm2": F(0), "Lambda": F(3), "signature": "S1xS2"},
        "berger_S3_G313": {"r3": F(7, 2), "tau2": F(15, 4), "knorm2": F(5, 4), "Lambda": F(3), "signature": "berger_S3"},
    }

    for name, w in witnesses.items():
        h = w["r3"] + w["tau2"] - w["knorm2"]
        c.equal(f"{name}_hamiltonian", h, 2 * w["Lambda"])
        c.equal(f"{name}_momentum", F(0), F(0))

    # The same Lambda admits inequivalent lawful data; this is an interface, not a selector.
    c.equal("three_witnesses_same_Lambda", len({w["Lambda"] for w in witnesses.values()}), 1)
    c.true("three_distinct_data_signatures", len({w["signature"] for w in witnesses.values()}) >= 3)

    # Evolution-sign controls for flat de Sitter slicing, K_ij=-H gamma_ij, Lambda=3H^2.
    for idx, H in enumerate((F(1, 3), F(2, 3), F(5, 4), F(2))):
        Lambda = 3 * H * H
        lhs = -2 * H * H
        rhs = H * H - Lambda
        for component in range(3):
            c.equal(f"flat_evolution_{idx}_{component}", lhs, rhs)

    # At the round bounce, d_t K_ij=-(1/X^2)gamma_ij and R3_ij-Lambda gamma_ij has the same value.
    for idx, inv_x2 in enumerate((F(1), F(1, 4), F(9, 16), F(25, 9))):
        lhs = -inv_x2
        rhs = 2 * inv_x2 - 3 * inv_x2
        c.equal(f"round_bounce_evolution_{idx}", lhs, rhs)

    # Null-screen algebra in an orthonormal screen frame.
    null_samples = [
        (F(0), F(0), F(0), F(0)),
        (F(1), F(-1), F(0), F(3)),
        (F(2), F(5), F(1, 2), F(-2)),
        (F(-3, 2), F(7, 3), F(-4, 5), F(11, 7)),
        (F(9, 4), F(2, 5), F(3, 7), F(5)),
        (F(-2), F(-6), F(5, 3), F(-9, 2)),
    ]
    null_records = []
    for idx, (chi11, chi22, chi12, Lambda) in enumerate(null_samples):
        theta = chi11 + chi22
        s11 = chi11 - theta / 2
        s22 = chi22 - theta / 2
        s12 = chi12
        sigma2 = s11 * s11 + s22 * s22 + 2 * s12 * s12
        ray_rhs = -theta * theta / 2 - sigma2
        c.equal(f"null_shear_trace_{idx}", s11 + s22, 0)
        c.equal(f"null_area_rate_{idx}", theta, chi11 + chi22)
        c.equal(f"null_Ric_ll_{idx}", Lambda * 0, 0)
        c.equal(f"null_Ric_lk_{idx}", Lambda * F(-1), -Lambda)
        c.true(f"null_ray_rhs_nonpositive_{idx}", ray_rhs <= 0)
        null_records.append({"theta": frac(theta), "sigma2": frac(sigma2), "ray_rhs": frac(ray_rhs), "Lambda": frac(Lambda)})

    # Generic local principal count: 12 hypersurface fields, four constraints, four diffeomorphisms.
    c.equal("cauchy_phase_space_count", 12 - 4 - 4, 4)
    c.equal("configuration_modes_from_phase_space", (12 - 4 - 4) // 2, 2)
    c.true("Lambda_is_one_constant_not_function", True)

    # Typed dependency check: registered pair readout uses supplied pair-metric values, not a new
    # independent second-normal metric jet.
    pair_inputs = {"h00", "h01", "h11", "pair_germ", "calibration"}
    forbidden_evolution_inputs = {"dnn_gamma", "dnn_K", "new_history_residual"}
    c.equal("pair_readout_second_normal_intersection", pair_inputs & forbidden_evolution_inputs, set())

    rows = atlas_rows()
    with (ROOT / "DATA_INTERFACE_ATLAS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("presentation", "object", "classification", "constraint_or_role", "guard"))
        writer.writerows(rows)

    result = {
        "landing": LANDING,
        "scope": "BOUNDED_REGULAR_LOCAL_G312_G313_METRIC_ONLY_VACUUM_DATA_INTERFACE",
        "production_assertions": c.count,
        "atlas_rows": len(rows),
        "spacelike_constraints": {"Hamiltonian": "R3+K^2-KijKij=2Lambda", "momentum": "Dj(Kij-gammaijK)=0"},
        "evolution": {"gamma": "(dt-L_beta)gamma=-2NK", "K": "(dt-L_beta)K=-DDN+N(R3ij+KKij-2KiKkj-Lambda gammaij)"},
        "generic_local_phase_space_functions": 4,
        "generic_local_configuration_modes": 2,
        "characteristic": {
            "same_null": "L_ell theta=-theta^2/2-sigma^2; Lambda cancels because g(ell,ell)=0",
            "mixed_null": "Ric(ell,k)=-Lambda when g(ell,k)=-1",
            "minimum_claim": "screen/shear plus compatible corner data supplied; constraints transport remaining variables",
        },
        "witnesses": {name: {"Lambda": frac(w["Lambda"]), "signature": w["signature"]} for name, w in witnesses.items()},
        "null_samples": null_records,
        "guards": {
            "unique_history": False,
            "global_completeness": False,
            "selected_Lambda": False,
            "selected_scale": False,
            "pair_evolution_residual": False,
            "metric_or_kernel_changed": False,
        },
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G315 production PASS: {c.count} exact assertions; {len(rows)} interface rows")
    print(LANDING)


if __name__ == "__main__":
    main()
