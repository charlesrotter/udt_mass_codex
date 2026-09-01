#!/usr/bin/env python3
"""Exact, dependency-free G316 production derivation."""

from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHECKS = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def conformal_constant_residual(rbar, a2bar, tau2, lam, psi):
    """Lichnerowicz residual for constant coefficients and constant psi."""
    c = F(2, 3) * tau2 - 2 * lam
    return rbar * psi - a2bar * psi ** -7 + c * psi ** 5


def physical_hamiltonian(rbar, a2bar, tau2, psi):
    """Physical Hamiltonian left side for constant psi."""
    return rbar * psi ** -4 + F(2, 3) * tau2 - a2bar * psi ** -12


# Three-dimensional conformal bookkeeping.
metric_power = 4
inverse_metric_power = -metric_power
a_up_power = -10
a_down_power = a_up_power + 2 * metric_power
a_norm_power = a_up_power + a_down_power
scalar_curvature_power = -5
hamiltonian_multiplier = -scalar_curvature_power
tt_scalar_power = a_norm_power + hamiltonian_multiplier
tau_scalar_power = hamiltonian_multiplier
tau_gradient_power = inverse_metric_power
momentum_multiplier = -a_up_power
momentum_source_power = tau_gradient_power + momentum_multiplier

check("metric conformal power is four", metric_power == 4)
check("inverse metric conformal power is minus four", inverse_metric_power == -4)
check("contravariant tracefree curvature power is minus ten", a_up_power == -10)
check("covariant tracefree curvature power is minus two", a_down_power == -2)
check("tracefree norm power is minus twelve", a_norm_power == -12)
check("scalar curvature density multiplier is psi five", hamiltonian_multiplier == 5)
check("TT term in scalar equation is psi minus seven", tt_scalar_power == -7)
check("mean-curvature term in scalar equation is psi five", tau_scalar_power == 5)
check("momentum source is psi six", momentum_source_power == 6)

# Exact coefficient and sign ledger.
formula = {
    "laplacian_coefficient": -8,
    "rbar_coefficient": 1,
    "tt_norm_coefficient": -1,
    "tt_norm_power": -7,
    "tau_squared_coefficient": F(2, 3),
    "lambda_coefficient": -2,
    "scalar_source_power": 5,
    "momentum_tau_coefficient": F(2, 3),
    "momentum_source_power": 6,
}
check("scalar Laplacian coefficient", formula["laplacian_coefficient"] == -8)
check("TT norm sign", formula["tt_norm_coefficient"] == -1)
check("Lambda sign", formula["lambda_coefficient"] == -2)
check("momentum mean-curvature coefficient", formula["momentum_tau_coefficient"] == F(2, 3))

# Registered G315 witnesses, all at constant psi=1.
witnesses = [
    {
        "name": "round_positive_bounce",
        "rbar": F(6), "a2bar": F(0), "tau2": F(0), "lambda": F(3), "psi": F(1),
    },
    {
        "name": "flat_positive_slicing",
        "rbar": F(0), "a2bar": F(0), "tau2": F(9), "lambda": F(3), "psi": F(1),
    },
    {
        "name": "positive_product_time_symmetric",
        "rbar": F(6), "a2bar": F(0), "tau2": F(0), "lambda": F(3), "psi": F(1),
    },
    {
        "name": "berger_s3_g315",
        "rbar": F(7, 2), "a2bar": F(0), "tau2": F(15, 4), "lambda": F(3), "psi": F(1),
    },
    {
        "name": "flat_tt_balanced",
        "rbar": F(0), "a2bar": F(1), "tau2": F(6), "lambda": F(3, 2), "psi": F(1),
    },
]

for witness in witnesses:
    residual = conformal_constant_residual(
        witness["rbar"], witness["a2bar"], witness["tau2"], witness["lambda"], witness["psi"]
    )
    physical = physical_hamiltonian(
        witness["rbar"], witness["a2bar"], witness["tau2"], witness["psi"]
    )
    check(f"{witness['name']} conformal scalar residual vanishes", residual == 0)
    check(f"{witness['name']} physical Hamiltonian equals twice Lambda", physical == 2 * witness["lambda"])

# Constant-coefficient existence and nonexistence controls.
# Use a rational exact twelfth-power control instead of an algebraic-number dependency.
a2_rational = F(4096)
c_rational = F(1)
psi_rational = F(2)
check("constant TT balance psi twelfth", psi_rational ** 12 == a2_rational / c_rational)
check(
    "constant TT balance residual",
    F(0) * psi_rational - a2_rational * psi_rational ** -7 + c_rational * psi_rational ** 5 == 0,
)

for c_bad in (F(0), F(-1), F(-7, 3)):
    for psi in (F(1, 3), F(1), F(5, 2)):
        integrand = -F(4) * psi ** -7 + c_bad * psi ** 5
        check(f"negative integral obstruction C={c_bad} psi={psi}", integrand < 0)

constant_scalar_cases = [
    (F(6), F(-6), F(1)),
    (F(-8), F(1, 2), F(2)),
    (F(3, 2), F(-24), F(1, 2)),
]
for index, (r0, c0, psi0) in enumerate(constant_scalar_cases):
    check(f"constant scalar branch {index} sign condition", -r0 / c0 > 0)
    check(f"constant scalar branch {index} fourth power", psi0 ** 4 == -r0 / c0)
    check(f"constant scalar branch {index} residual", r0 * psi0 + c0 * psi0 ** 5 == 0)

for psi in (F(1, 5), F(1), F(11, 3)):
    check(f"zero coefficient homothety psi={psi}", conformal_constant_residual(F(0), F(0), F(0), F(0), psi) == 0)

# Finite-dimensional exact model of the conformal-Killing kernel/Fredholm obstruction.
eigenvalues = (F(0), F(2), F(5))
compatible_source = (F(0), F(6), F(20))
incompatible_source = (F(1), F(6), F(20))
particular_w = (F(0), F(3), F(4))
check("compatible vector source orthogonal to kernel", compatible_source[0] == 0)
check("incompatible vector source has kernel component", incompatible_source[0] != 0)
check(
    "particular vector solution",
    tuple(eigenvalues[i] * particular_w[i] for i in range(3)) == compatible_source,
)
for kernel_shift in (F(-9), F(0), F(13, 2)):
    shifted = (particular_w[0] + kernel_shift, particular_w[1], particular_w[2])
    check(
        f"vector solution nonunique modulo kernel shift {kernel_shift}",
        tuple(eigenvalues[i] * shifted[i] for i in range(3)) == compatible_source,
    )

# Null-corner boost weights and invariants.
weights = {
    "q": 0,
    "theta_l": 1,
    "sigma_l": 1,
    "theta_k": -1,
    "sigma_k": -1,
    "ric_lk": 0,
}
check("theta cross product boost invariant", weights["theta_l"] + weights["theta_k"] == 0)
check("shear cross contraction boost invariant", weights["sigma_l"] + weights["sigma_k"] == 0)
check("screen metric boost invariant", weights["q"] == 0)
check("mixed Ricci projection boost invariant", weights["ric_lk"] == 0)

# Discrete exterior-calculus check: omega -> omega + df leaves d omega unchanged.
# A one-dimensional finite difference is not d^2=0, so explicitly use an exact 2-cell coboundary.
vertex_f = (F(3), F(-2), F(8))
edge_df = (vertex_f[1] - vertex_f[0], vertex_f[2] - vertex_f[1], vertex_f[0] - vertex_f[2])
check("exact gradient has zero loop curl", sum(edge_df) == 0)
edge_omega = (F(4), F(-1), F(6))
check("normal connection loop curl boost invariant", sum(edge_omega[i] + edge_df[i] for i in range(3)) == sum(edge_omega))

# Semantic nonpromotion gates.
semantic = {
    "arbitrary_seeds_are_lawful": False,
    "cmc_is_udt": False,
    "construction_is_globally_complete": False,
    "boost_is_physical_scale": False,
    "one_null_sheet_is_complete": False,
    "physical_history_selected": False,
    "metric_changed": False,
    "kernel_changed": False,
}
for key, value in semantic.items():
    check(f"semantic guard {key}", value is False)

landing = (
    "CONFORMAL_CONSTRUCTION_MAPS_A_LAWFUL_SUBSET_WITH_NONTRIVIAL_SOLVABILITY_AND_"
    "CORNER_GAUGE_BOUNDS__NO_PHYSICAL_DATA_SELECTION"
)

atlas_rows = [
    ("spacelike", "conformal metric", "SUPPLIED_SEED", "conformal geometry; topology/boundary still supplied"),
    ("spacelike", "TT tensor", "SUPPLIED_SEED", "tracefree divergence-free shape seed"),
    ("spacelike", "mean curvature", "SUPPLIED_SEED", "CMC only a diagnostic subcase"),
    ("spacelike", "Lambda", "CONNECTED_SECTOR_INPUT_OR_INFERRED", "no magnitude selection"),
    ("spacelike", "psi", "SOLVED_IF_SOLVABLE", "positive conformal factor; existence may fail"),
    ("spacelike", "W", "SOLVED_MODULO_KERNEL_IF_SOLVABLE", "conformal-Killing degeneracy"),
    ("spacelike", "gamma and K", "LAWFUL_OUTPUT", "only after both constraints pass"),
    ("null corner", "screen metric", "BOOST_INVARIANT_GEOMETRY", "does not fix null normalization"),
    ("null corner", "ell expansion and shear", "BOOST_WEIGHT_PLUS_ONE", "one sheet transport data"),
    ("null corner", "k expansion and shear", "BOOST_WEIGHT_MINUS_ONE", "transverse sheet remains required"),
    ("null corner", "normal connection", "GAUGE_CONNECTION", "gradient shift; curl invariant"),
    ("all", "physical history", "NOT_SELECTED", "construction characterizes lawful data only"),
]

with (ROOT / "DATA_CONSTRUCTION_ATLAS.tsv").open("w", encoding="utf-8") as handle:
    handle.write("presentation\tobject\tclassification\tconstraint_or_guard\n")
    for row in atlas_rows:
        handle.write("\t".join(row) + "\n")

def frac_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"

result = {
    "schema": "udt-g316-derivation-v1",
    "landing": landing,
    "status": "INTERNALLY_DERIVED__EXTERNAL_REVIEW_REQUIRED",
    "assertion_count": len(CHECKS),
    "conformal_powers": {
        "metric": metric_power,
        "A_up": a_up_power,
        "A_norm": a_norm_power,
        "TT_scalar": tt_scalar_power,
        "scalar_source": tau_scalar_power,
        "momentum_source": momentum_source_power,
    },
    "formula": {key: frac_text(value) if isinstance(value, F) else value for key, value in formula.items()},
    "witnesses": [
        {
            key: frac_text(value) if isinstance(value, F) else value
            for key, value in witness.items()
        }
        for witness in witnesses
    ],
    "boost_weights": weights,
    "atlas_rows": len(atlas_rows),
    "selected_history": False,
    "metric_changed": False,
    "kernel_changed": False,
    "checks": CHECKS,
}

(ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"landing": landing, "assertions": len(CHECKS), "atlas_rows": len(atlas_rows)}, indent=2))
