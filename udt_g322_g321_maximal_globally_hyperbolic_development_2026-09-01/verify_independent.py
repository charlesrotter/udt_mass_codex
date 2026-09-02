#!/usr/bin/env python3
"""Implementation-distinct G322 check using direct connection/Ricci loops."""

import csv
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE_ROOTS = (REPO, REPO / "sources")
CHECKS = []
P = 1.7  # CHOSE_CATEGORY_A_INDEPENDENT_CONTROL
AMPLITUDE = 0.12  # CHOSE_CATEGORY_A_INDEPENDENT_CONTROL
J0 = 300.0  # CHOSE_CATEGORY_A_INDEPENDENT_CONTROL
MODES = (1, 3, 5)  # FREE_AND_EXPLORED_INDEPENDENT_CONTROLS
SIGNS = (-1, 1)  # FREE_AND_EXPLORED_BRANCHES
SAMPLES = 1024  # CATEGORY_A_NUMERICAL_QUADRATURE


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def jet(x_value, mode):
    angle = mode * x_value
    return (
        P + AMPLITUDE * math.cos(angle),
        -AMPLITUDE * mode * math.sin(angle),
        -AMPLITUDE * mode ** 2 * math.cos(angle),
        AMPLITUDE * mode ** 3 * math.sin(angle),
    )


def geometry(psi, psi_1, psi_2):
    scale = psi ** 4
    scale_1 = 4.0 * psi ** 3 * psi_1
    scale_2 = 12.0 * psi ** 2 * psi_1 ** 2 + 4.0 * psi ** 3 * psi_2
    g = [[scale * float(i == j) for j in range(3)] for i in range(3)]
    g_inv = [[float(i == j) / scale for j in range(3)] for i in range(3)]
    dg = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    ddg = [[[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(3):
        dg[0][i][i] = scale_1
        ddg[0][0][i][i] = scale_2
    dg_inv = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(3):
        dg_inv[0][i][i] = -scale_1 / scale ** 2

    connection = [[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dconnection = [[[[0.0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for lower in range(3):
                    bracket = dg[i][j][lower] + dg[j][i][lower] - dg[lower][i][j]
                    connection[upper][i][j] += 0.5 * g_inv[upper][lower] * bracket
                    for derivative in range(3):
                        dbracket = (
                            ddg[derivative][i][j][lower]
                            + ddg[derivative][j][i][lower]
                            - ddg[derivative][lower][i][j]
                        )
                        dconnection[derivative][upper][i][j] += 0.5 * (
                            dg_inv[derivative][upper][lower] * bracket
                            + g_inv[upper][lower] * dbracket
                        )

    ricci = [[0.0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                ricci[i][j] += dconnection[k][k][i][j] - dconnection[j][k][i][k]
                for lower in range(3):
                    ricci[i][j] += (
                        connection[k][i][j] * connection[lower][k][lower]
                        - connection[lower][i][k] * connection[k][j][lower]
                    )
    scalar = sum(g_inv[i][j] * ricci[i][j] for i in range(3) for j in range(3))
    return g, connection, scalar


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
    mixed_k = [
        (tau + 2.0 * anisotropy) / 3.0,
        (tau - anisotropy) / 3.0,
        (tau - anisotropy) / 3.0,
    ]
    mixed_k_prime = [
        (tau_prime + 2.0 * anisotropy_prime) / 3.0,
        (tau_prime - anisotropy_prime) / 3.0,
        (tau_prime - anisotropy_prime) / 3.0,
    ]
    g, connection, scalar = geometry(psi, psi_1, psi_2)
    hamiltonian = scalar + tau ** 2 - sum(value ** 2 for value in mixed_k)
    tensor = [mixed_k[index] - tau for index in range(3)]
    momentum = []
    for i in range(3):
        value = mixed_k_prime[0] - tau_prime if i == 0 else 0.0
        for j in range(3):
            value += connection[j][j][i] * tensor[i]
            value -= connection[j][j][i] * tensor[j]
        momentum.append(value)
    return {
        "psi": psi,
        "scalar": scalar,
        "hamiltonian": hamiltonian,
        "momentum": tuple(momentum),
        "K": tuple(g[index][index] * mixed_k[index] for index in range(3)),
    }


source_relative = "udt_gr_lorentzian_relational_architecture_audit_2026-07-27/SOURCE_VERIFICATION.tsv"
source_path = next((root / source_relative for root in SOURCE_ROOTS if (root / source_relative).is_file()), None)
check("independent source resolved", source_path is not None)
with source_path.open(encoding="utf-8", newline="") as handle:
    sources = {row["source_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
s09 = sources["S09"]
check("independent primary source grade", s09["access_grade"] == "PRIMARY_ABSTRACT_METADATA")
check("independent maximal theorem scope", "maximal Cauchy development" in s09["exact_supported_scope"])
check("independent theorem limitation", "Einstein dynamics" in s09["limitations"])

primary_path = HERE / "S09_PRIMARY_ABSTRACT_EVIDENCE.json"
check("independent bounded primary evidence exists", primary_path.is_file())
primary = json.loads(primary_path.read_text(encoding="utf-8"))
fragments = primary["official_abstract_fragments"]
joined_fragments = " ".join(fragments).lower()
check("independent bounded primary schema", primary["schema"] == "udt-g322-s09-primary-abstract-bounded-evidence-v1")
check("independent bounded primary grade", primary["source_grade"] == "PRIMARY_PUBLISHER_ABSTRACT_BOUNDED_EXCERPT")
check("independent bounded primary DOI", primary["doi"] == "10.1007/BF01645389")
check("independent bounded excerpt word count", sum(len(fragment.split()) for fragment in fragments) == primary["bounded_excerpt_word_count"] == 25)
check("independent constraint antecedent", "constraint conditions" in joined_fragments)
check("independent every-development extension", "extension of every other development" in joined_fragments)
check("independent unique maximal embedding", "embedded in exactly one such maximal development" in joined_fragments)

max_hamiltonian = 0.0
max_momentum = 0.0
max_ricci_formula_error = 0.0
max_time_reverse_error = 0.0
q_values = {}
for mode in MODES:
    branch_rows = {}
    for sign in SIGNS:
        rows = []
        for index in range(SAMPLES):
            x_value = 2.0 * math.pi * index / SAMPLES
            values = jet(x_value, mode)
            row = reconstruct(*values, sign)
            rows.append(row)
            expected_scalar = -8.0 * values[0] ** -5 * values[2]
            max_ricci_formula_error = max(max_ricci_formula_error, abs(row["scalar"] - expected_scalar))
            max_hamiltonian = max(max_hamiltonian, abs(row["hamiltonian"]))
            max_momentum = max(max_momentum, *(abs(value) for value in row["momentum"]))
        branch_rows[sign] = rows
    weights = [row["psi"] ** 6 for row in branch_rows[1]]
    volume = (2.0 * math.pi) ** 3 * math.fsum(weights) / SAMPLES
    total_scalar = (2.0 * math.pi) ** 3 * math.fsum(
        row["psi"] ** 6 * row["scalar"] for row in branch_rows[1]
    ) / SAMPLES
    q_values[mode] = total_scalar / volume ** (1.0 / 3.0)
    for minus, plus in zip(branch_rows[-1], branch_rows[1]):
        max_time_reverse_error = max(
            max_time_reverse_error,
            *(abs(a + b) for a, b in zip(minus["K"], plus["K"])),
        )

check("independent direct Ricci loop", max_ricci_formula_error < 3e-13)
check("independent Hamiltonian", max_hamiltonian < 6e-12)
check("independent momentum", max_momentum < 6e-12)
check("independent time reversal", max_time_reverse_error < 6e-12)
for mode in MODES:
    check(f"independent Q_R n={mode}", abs(q_values[mode] / q_values[1] - mode ** 2) < 6e-12)

result = {
    "schema": "udt-g322-independent-maximal-development-v1",
    "status": "PASS_INDEPENDENT",
    "assertion_count": len(CHECKS),
    "production_imported": False,
    "production_output_read": False,
    "direct_connection_ricci_loop": True,
    "modes_checked": list(MODES),
    "branches_checked": list(SIGNS),
    "max_ricci_formula_error": max_ricci_formula_error,
    "max_hamiltonian_residual": max_hamiltonian,
    "max_momentum_residual": max_momentum,
    "max_time_reversal_error": max_time_reverse_error,
    "theorem_source_scope": "INDEPENDENTLY_AUTHENTICATED_PRIMARY_PUBLISHER_BOUNDED_EXCERPT",
    "maximal_development_conclusion": "UPHELD_CONDITIONAL_ON_IMPORTED_THEOREM",
    "completeness_or_occupancy_claim": "NONE",
}
with (HERE / "INDEPENDENT_VERIFICATION.json").open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(result, indent=2, sort_keys=True))
