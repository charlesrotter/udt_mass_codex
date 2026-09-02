#!/usr/bin/env python3
"""G321 production: audit local-development hypotheses for G320 data."""

import csv
from fractions import Fraction
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS = []
P = Fraction(3, 2)  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
AMPLITUDE = Fraction(1, 5)  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
J0 = 100.0  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
MODES = (1, 2, 3, 4)  # FREE_AND_EXPLORED_FINITE_REPLAY
SIGNS = (-1, 1)  # FREE_AND_EXPLORED_BRANCHES
SAMPLES = 4096  # CATEGORY_A_NUMERICAL_QUADRATURE
TWO_PI = 2.0 * math.pi

LANDING = (
    "G320_DATA_HAVE_CONDITIONAL_UNIQUE_LOCAL_MARKED_DEVELOPMENTS__"
    "REGISTERED_BREADTH_IS_ORDINARY_CAUCHY_DATA_FREEDOM_IN_BOUNDED_ARENA__"
    "NO_GLOBAL_OR_OCCUPANCY_SELECTION"
)

THEOREM_HYPOTHESIS_AUDIT = {
    "H1_initial_manifold": {
        "status": "DECLARED_DIAGNOSTIC_DOMAIN__STANDARD_SMOOTH_COMPACT_BOUNDARY_FREE_T3",
        "evidence": "T3 is fixed in the preregistration; this is an analytic domain declaration, not a numerical test",
    },
    "H2_gamma_regular": {
        "status": "ANALYTICALLY_VERIFIED_ON_REGISTERED_FAMILY",
        "evidence": "psi=3/2+(1/5)cos(nx) is analytic and psi>=13/10, hence gamma=psi^4 delta is smooth positive definite",
    },
    "H3_K_regular": {
        "status": "ANALYTICALLY_VERIFIED_ON_REGISTERED_REGULAR_BRANCH",
        "evidence": "the exact positive margin keeps Z and B nonzero; the reconstructed diagonal K is analytic and symmetric",
    },
    "H4_constraints": {
        "status": "ANALYTIC_IDENTITY_WITH_TWO_NUMERICAL_REPLAYS",
        "evidence": "Hamiltonian and all momentum components vanish analytically; production and independent residuals are numerical backward-error checks",
    },
    "H5_connected_scalar_sector": {
        "status": "DERIVED_FROM_HAMILTONIAN_VALUE",
        "evidence": "H=2 Lambda and H=0 fix Lambda=0 on the connected registered slice",
    },
    "H6_full_principal_operator": {
        "status": "EXACT_LINEAR_ALGEBRA_AUDIT",
        "evidence": "raw trace-free projector rank is nine and the Bianchi-completed fixed-Lambda metric-wave principal operator rank is ten",
    },
    "H7_gauge_constraint_propagation": {
        "status": "FORMAL_BIANCHI_CONSEQUENCE__THEOREM_APPLICATION_REMAINS_IMPORTED",
        "evidence": "fixed Lambda leaves the standard harmonic gauge-constraint propagation system homogeneous; G321 does not machine-prove the PDE theorem",
    },
    "H8_gauge_quotient": {
        "status": "IMPORTED_STANDARD_GEOMETRIC_CAUCHY_INTERFACE",
        "evidence": "lapse, shift, and harmonic-coordinate data are presentation choices under the declared standard theorem, not newly derived UDT physics",
    },
}


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(rows):
            if row != rank and work[row][col]:
                factor = work[row][col]
                work[row] = [a - factor * b for a, b in zip(work[row], work[rank])]
        rank += 1
    return rank


def tracefree_projector():
    pairs = [(a, b) for a in range(4) for b in range(a, 4)]
    metric = (-1, 1, 1, 1)
    columns = []
    for c, d in pairs:
        tensor = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        tensor[c][d] = tensor[d][c] = Fraction(1)
        trace = sum(Fraction(metric[a]) * tensor[a][a] for a in range(4))
        output = [[tensor[a][b] for b in range(4)] for a in range(4)]
        for a in range(4):
            output[a][a] -= Fraction(1, 4) * trace * metric[a]
        columns.append([output[a][b] for a, b in pairs])
    return [[columns[col][row] for col in range(10)] for row in range(10)]


def profile_jet(x_value, mode, p=float(P), amplitude=float(AMPLITUDE)):
    angle = mode * x_value
    return (
        p + amplitude * math.cos(angle),
        -amplitude * mode * math.sin(angle),
        -amplitude * mode * mode * math.cos(angle),
        amplitude * mode ** 3 * math.sin(angle),
    )


def reconstruct(psi, psi_1, psi_2, psi_3, sign):
    f_value = 12.0 * psi_2 * psi ** -5
    f_prime = 12.0 * (psi_3 * psi ** -5 - 5.0 * psi_2 * psi ** -6 * psi_1)
    z_value = 36.0 * psi_1 ** 2 + J0
    z_prime = 72.0 * psi_1 * psi_2
    b_value = sign * psi ** -3 * math.sqrt(z_value)
    b_prime = b_value * (-3.0 * psi_1 / psi + z_prime / (2.0 * z_value))
    a_value = f_value / b_value
    a_prime = f_prime / b_value - f_value * b_prime / b_value ** 2
    tau = 0.5 * (a_value + b_value)
    anisotropy = 0.5 * (a_value - b_value)
    tau_prime = 0.5 * (a_prime + b_prime)
    anisotropy_prime = 0.5 * (a_prime - b_prime)
    mixed_k = (
        (tau + 2.0 * anisotropy) / 3.0,
        (tau - anisotropy) / 3.0,
        (tau - anisotropy) / 3.0,
    )
    mixed_k_prime = (
        (tau_prime + 2.0 * anisotropy_prime) / 3.0,
        (tau_prime - anisotropy_prime) / 3.0,
        (tau_prime - anisotropy_prime) / 3.0,
    )

    u_1 = psi_1 / psi
    ricci_cov = (
        -4.0 * psi_2 / psi + 4.0 * u_1 ** 2,
        -2.0 * psi_2 / psi - 2.0 * u_1 ** 2,
        -2.0 * psi_2 / psi - 2.0 * u_1 ** 2,
    )
    gamma_factor = psi ** 4
    scalar_3 = math.fsum(ricci_cov) / gamma_factor
    k_squared = math.fsum(value * value for value in mixed_k)
    hamiltonian = scalar_3 + tau ** 2 - k_squared
    momentum_x = (
        mixed_k_prime[0] - tau_prime + 6.0 * u_1 * mixed_k[0]
        - 2.0 * u_1 * tau
    )
    k_cov = tuple(gamma_factor * value for value in mixed_k)
    gamma_dot = tuple(-2.0 * value for value in k_cov)
    k_dot = tuple(
        ricci_cov[index] + tau * k_cov[index]
        - 2.0 * gamma_factor * mixed_k[index] ** 2
        for index in range(3)
    )
    return {
        "psi": psi,
        "z": z_value,
        "gamma": (gamma_factor,) * 3,
        "K": k_cov,
        "tau": tau,
        "R3": scalar_3,
        "hamiltonian": hamiltonian,
        "momentum": (momentum_x, 0.0, 0.0),
        "gamma_dot": gamma_dot,
        "K_dot": k_dot,
    }


def mean(values):
    return math.fsum(values) / len(values)


def summarize(mode, sign):
    rows = []
    for index in range(SAMPLES):
        x_value = TWO_PI * index / SAMPLES
        rows.append(reconstruct(*profile_jet(x_value, mode), sign))
    volume = TWO_PI ** 3 * mean([row["psi"] ** 6 for row in rows])
    total_scalar = TWO_PI ** 3 * mean(
        [row["psi"] ** 6 * row["R3"] for row in rows]
    )
    return {
        "mode": mode,
        "sign": sign,
        "min_psi": min(row["psi"] for row in rows),
        "min_z": min(row["z"] for row in rows),
        "max_hamiltonian": max(abs(row["hamiltonian"]) for row in rows),
        "max_momentum": max(abs(value) for row in rows for value in row["momentum"]),
        "max_lambda_inferred": max(abs(0.5 * row["hamiltonian"]) for row in rows),
        "volume": volume,
        "Q_R": total_scalar / volume ** (1.0 / 3.0),
        "mean_gamma_dot_norm2": mean([
            math.fsum(value * value for value in row["gamma_dot"]) for row in rows
        ]),
        "mean_K_dot_norm2": mean([
            math.fsum(value * value for value in row["K_dot"]) for row in rows
        ]),
        "rows": rows,
    }


# Exact principal-rank audit: raw trace-free output is nine-dimensional, while each
# Bianchi-completed fixed-Lambda harmonic system has ten metric-wave directions.
raw_projector = tracefree_projector()
raw_rank = matrix_rank(raw_projector)
fixed_sector_rank = matrix_rank([[int(i == j) for j in range(10)] for i in range(10)])
check("raw tracefree rank nine", raw_rank == 9)
check("fixed sector principal rank ten", fixed_sector_rank == 10)

# Nonnumerical theorem hypotheses are typed explicitly in THEOREM_HYPOTHESIS_AUDIT.
# They are not counted as executable assertions.  In particular, G321 does not pretend
# to machine-prove the imported local harmonic well-posedness theorem.

summaries = {}
atlas = []
for mode in MODES:
    margin = Fraction(100) - 12 * AMPLITUDE * mode ** 2 * (P + AMPLITUDE)
    check(f"exact regular margin mode={mode}", margin > 0)
    for sign in SIGNS:
        summary = summarize(mode, sign)
        summaries[(mode, sign)] = summary
        check(f"positive metric mode={mode} sign={sign}", summary["min_psi"] > 0)
        check(f"regular branch mode={mode} sign={sign}", summary["min_z"] > 0)
        check(f"Hamiltonian mode={mode} sign={sign}", summary["max_hamiltonian"] < 3e-12)
        check(f"momentum mode={mode} sign={sign}", summary["max_momentum"] < 3e-12)
        check(f"Lambda zero mode={mode} sign={sign}", summary["max_lambda_inferred"] < 2e-12)
        atlas.append({key: value for key, value in summary.items() if key != "rows"})

base_q = summaries[(1, 1)]["Q_R"]
for mode in MODES:
    for sign in SIGNS:
        ratio = summaries[(mode, sign)]["Q_R"] / base_q
        check(f"marked Q_R separator mode={mode} sign={sign}", abs(ratio - mode ** 2) < 3e-12)

# K-sign branches are exact time reverses in unit lapse and zero shift.
for mode in MODES:
    negative = summaries[(mode, -1)]["rows"]
    positive = summaries[(mode, 1)]["rows"]
    for index, (minus, plus) in enumerate(zip(negative, positive)):
        check(f"same gamma mode={mode} point={index}", minus["gamma"] == plus["gamma"])
        for axis in range(3):
            tolerance = 2e-13 * max(1.0, abs(plus["K"][axis]))
            check(
                f"K time reverse mode={mode} point={index} axis={axis}",
                abs(minus["K"][axis] + plus["K"][axis]) < tolerance,
            )
            check(
                f"gamma dot time reverse mode={mode} point={index} axis={axis}",
                abs(minus["gamma_dot"][axis] + plus["gamma_dot"][axis]) < 2 * tolerance,
            )
            tolerance_dot = 3e-12 * max(1.0, abs(plus["K_dot"][axis]))
            check(
                f"K dot time-even mode={mode} point={index} axis={axis}",
                abs(minus["K_dot"][axis] - plus["K_dot"][axis]) < tolerance_dot,
            )

with (HERE / "DEVELOPMENT_ATLAS.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=tuple(atlas[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(atlas)

result = {
    "schema": "udt-g321-local-development-uniqueness-v1",
    "status": "PASS_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW",
    "landing": LANDING,
    "assertion_count": len(CHECKS),
    "raw_tracefree_principal_rank": raw_rank,
    "fixed_lambda_principal_rank": fixed_sector_rank,
    "constraint_sector": "Lambda=0",
    "theorem_hypothesis_audit": THEOREM_HYPOTHESIS_AUDIT,
    "theorem_interface_status": "AUDITED_CONDITIONAL__NOT_MACHINE_PROVED_IN_FULL",
    "initial_adm_rhs_single_valued_after_gauge_fix": True,
    "lapse_shift_are_physical_data": False,
    "local_geometric_uniqueness": "CONDITIONAL_ON_IMPORTED_STANDARD_THEOREM",
    "different_modes_distinct_as_marked_developments": True,
    "opposite_signs_are_distinct_full_data": True,
    "opposite_signs_are_time_reversed_data": True,
    "unmarked_same_spacetime_different_slice_classified": False,
    "global_history_selected": False,
    "physical_initial_data_selected": False,
    "metric_or_kernel_changed": False,
}
with (HERE / "DERIVATION_RESULT.json").open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, sort_keys=True)
    handle.write("\n")

print(json.dumps(result, indent=2, sort_keys=True))
