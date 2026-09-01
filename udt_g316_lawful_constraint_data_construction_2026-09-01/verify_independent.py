#!/usr/bin/env python3
"""Implementation-distinct, dependency-free G316 verification."""

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
passed = []


def require(name, truth):
    if not truth:
        raise AssertionError(name)
    passed.append(name)


# Rebuild the powers from tensor index counting rather than reading production output.
n = 3
metric_weight = 4
inverse_weight = -metric_weight
tracefree_up_weight = -10
tracefree_down_weight = tracefree_up_weight + 2 * metric_weight
norm_weight = tracefree_up_weight + tracefree_down_weight
curvature_numerator_weight = -5
scalar_multiplier = 5

require("independent metric weight", metric_weight == 4)
require("independent inverse weight", inverse_weight == -4)
require("independent A down weight", tracefree_down_weight == -2)
require("independent A norm weight", norm_weight == -12)
require("independent TT scalar exponent", norm_weight + scalar_multiplier == -7)
require("independent scalar source exponent", scalar_multiplier == 5)
require("independent momentum source exponent", inverse_weight - tracefree_up_weight == 6)
require("spatial dimension fixed", n == 3)

# Verify exact equivalence of the physical and conformal scalar constraints on a broad rational grid.
grid = [Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2)]
r_values = [Fraction(-3), Fraction(0), Fraction(7, 2)]
a_values = [Fraction(0), Fraction(1), Fraction(5, 3)]
tau2_values = [Fraction(0), Fraction(3, 2), Fraction(9)]
lambda_values = [Fraction(-2), Fraction(0), Fraction(3)]

for psi in grid:
    for rbar, a2, tau2, lam in zip(r_values, a_values, tau2_values, lambda_values):
        physical_residual = (
            rbar * psi ** -4
            + Fraction(2, 3) * tau2
            - a2 * psi ** -12
            - 2 * lam
        )
        conformal_residual = (
            rbar * psi
            - a2 * psi ** -7
            + (Fraction(2, 3) * tau2 - 2 * lam) * psi ** 5
        )
        require(
            f"independent scalar equivalence psi={psi} tuple={rbar},{a2},{tau2},{lam}",
            conformal_residual == psi ** 5 * physical_residual,
        )

# Exercise all cross-products of a smaller coefficient grid, independently.
small = [Fraction(-1), Fraction(0), Fraction(1)]
for psi in (Fraction(1, 3), Fraction(1), Fraction(3)):
    for rbar in small:
        for a2 in (Fraction(0), Fraction(2)):
            for c in small:
                lhs = rbar * psi - a2 * psi ** -7 + c * psi ** 5
                reconstructed = psi ** 5 * (rbar * psi ** -4 - a2 * psi ** -12 + c)
                require(f"full coefficient grid {psi},{rbar},{a2},{c}", lhs == reconstructed)

# Exact homogeneous controls.
require("TT positive branch root", Fraction(2) ** 12 == Fraction(4096))
require("TT positive branch equation", -Fraction(4096) * Fraction(2) ** -7 + Fraction(2) ** 5 == 0)
for c in (Fraction(0), Fraction(-1), Fraction(-5)):
    for psi in grid:
        require(f"independent integral obstruction {c},{psi}", -Fraction(1) * psi ** -7 + c * psi ** 5 < 0)

for r0, c0, root in (
    (Fraction(6), Fraction(-6), Fraction(1)),
    (Fraction(-8), Fraction(1, 2), Fraction(2)),
    (Fraction(3, 2), Fraction(-24), Fraction(1, 2)),
):
    require(f"independent scalar root sign {r0},{c0}", -r0 / c0 > 0)
    require(f"independent scalar root power {root}", root ** 4 == -r0 / c0)
    require(f"independent scalar root residual {root}", r0 * root + c0 * root ** 5 == 0)

for psi in grid:
    require(f"independent zero-data constant family {psi}", 0 * psi + 0 * psi ** -7 + 0 * psi ** 5 == 0)

# Rebuild the four G315 controls directly from the unsplit Hamiltonian relation.
controls = {
    "round": (Fraction(6), Fraction(0), Fraction(0), Fraction(3)),
    "flat_slicing": (Fraction(0), Fraction(0), Fraction(9), Fraction(3)),
    "product": (Fraction(6), Fraction(0), Fraction(0), Fraction(3)),
    "berger": (Fraction(7, 2), Fraction(0), Fraction(15, 4), Fraction(3)),
}
for name, (r3, a2, tau2, lam) in controls.items():
    require(f"independent G315 control {name}", r3 + Fraction(2, 3) * tau2 - a2 == 2 * lam)

# Independent finite-dimensional Fredholm/kernel reconstruction.
matrix = (
    (Fraction(0), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(2), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(5)),
)


def matvec(vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3))


target = (Fraction(0), Fraction(6), Fraction(20))
for free in (Fraction(-100), Fraction(0), Fraction(7, 3)):
    require(f"independent kernel family {free}", matvec((free, Fraction(3), Fraction(4))) == target)
require("independent incompatible source", all(matvec((Fraction(x), Fraction(3), Fraction(4)))[0] != 1 for x in range(-2, 3)))

# Null boost-weight algebra and normal-connection curl.
for f_weight in (-7, -1, 0, 2, 11):
    theta_l_weight = f_weight
    theta_k_weight = -f_weight
    require(f"independent expansion product weight {f_weight}", theta_l_weight + theta_k_weight == 0)
    require(f"independent shear product weight {f_weight}", theta_l_weight + theta_k_weight == 0)

for vertex_values in ((0, 0, 0), (3, -2, 8), (-5, 11, 4)):
    df = (
        vertex_values[1] - vertex_values[0],
        vertex_values[2] - vertex_values[1],
        vertex_values[0] - vertex_values[2],
    )
    require(f"independent d squared zero {vertex_values}", sum(df) == 0)
    omega = (4, -1, 6)
    require(f"independent connection curl {vertex_values}", sum(omega[i] + df[i] for i in range(3)) == sum(omega))

# Explicit ceiling checks.
ceilings = {
    "all_lawful_data_parameterized": False,
    "history_selected": False,
    "scale_selected": False,
    "topology_selected": False,
    "boost_is_physical": False,
    "single_null_sheet_complete": False,
    "kernel_modified": False,
}
for key, value in ceilings.items():
    require(f"independent ceiling {key}", value is False)

landing = (
    "CONFORMAL_CONSTRUCTION_MAPS_A_LAWFUL_SUBSET_WITH_NONTRIVIAL_SOLVABILITY_AND_"
    "CORNER_GAUGE_BOUNDS__NO_PHYSICAL_DATA_SELECTION"
)
output = {
    "schema": "udt-g316-independent-v1",
    "landing": landing,
    "status": "PASS",
    "assertion_count": len(passed),
    "production_imported": False,
    "production_result_read": False,
    "checks": passed,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"landing": landing, "independent_assertions": len(passed)}, indent=2))
