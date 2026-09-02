#!/usr/bin/env python3
"""G322 production: audit the conditional maximal-Cauchy theorem interface."""

import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE_ROOTS = (REPO, REPO / "sources")
CHECKS = []
P = Fraction(3, 2)  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
AMPLITUDE = Fraction(1, 5)  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
J0 = 100.0  # CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROL
MODES = (1, 2, 3, 4)  # FREE_AND_EXPLORED_FINITE_REPLAY
SIGNS = (-1, 1)  # FREE_AND_EXPLORED_BRANCHES
SAMPLES = 2048  # CATEGORY_A_NUMERICAL_QUADRATURE

LANDING = (
    "FIXED_G321_DATA_HAVE_CONDITIONAL_UNIQUE_MAXIMAL_GLOBALLY_HYPERBOLIC_"
    "DEVELOPMENTS__MAXIMALITY_IS_PER_DATUM_AND_NOT_COMPLETENESS_OR_OCCUPANCY"
)

SOURCE_PATHS = (
    "udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md",
    "udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md",
    "udt_g320_g319_physical_initial_geometry_quotient_audit_2026-09-01/EXACT_DERIVATION.md",
    "udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXACT_DERIVATION.md",
    "udt_gr_lorentzian_relational_architecture_audit_2026-07-27/SOURCE_VERIFICATION.tsv",
)

THEOREM_INTERFACE = (
    ("H1", "smooth connected initial manifold", "SUPPORTED_BOUNDED", "analytic-domain", "marked T3"),
    ("H2", "smooth gamma and symmetric K", "SUPPORTED_BOUNDED", "analytic-regularity", "registered regular branch"),
    ("H3", "vacuum constraints", "SUPPORTED_BOUNDED", "identity-plus-backward-error", "Lambda=0"),
    ("H4", "active equation equals Ric=0", "SUPPORTED_BOUNDED", "Bianchi-and-sector-algebra", "connected Lambda=0 sector"),
    ("H5", "at least one local development", "CONDITIONAL_IMPORTED", "G321-theorem-application", "not machine-proved"),
    ("H6", "globally hyperbolic development category", "IMPORTED_DEFINITION", "theorem-interface", "Sigma is Cauchy"),
    ("H7", "data-preserving isometric embeddings", "IMPORTED_DEFINITION", "theorem-interface", "marked equivalence"),
    ("H8", "maximal extension and uniqueness", "CONDITIONAL_IMPORTED", "primary-publisher-abstract", "not a UDT derivation"),
)

SCOPE_MATRIX = (
    ("maximal_GH_exists_per_fixed_datum", "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE"),
    ("every_same_datum_GH_development_embeds", "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE"),
    ("same_datum_maximal_developments_isometric", "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE"),
    ("geodesic_completeness", "OPEN_NOT_ENTAILED"),
    ("singularity_or_curvature_control", "OPEN_NOT_ENTAILED"),
    ("arbitrary_Lorentzian_inextendibility", "OPEN_NOT_ENTAILED"),
    ("stability", "OPEN_NOT_TESTED"),
    ("unmarked_cross_datum_spacetime_identity", "OPEN_NOT_CLASSIFIED"),
    ("physical_initial_data_occupancy", "OPEN_NOT_SELECTED"),
    ("metric_kernel_angular_interface", "UNCHANGED"),
)


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_path(relative):
    matches = [root / relative for root in SOURCE_ROOTS if (root / relative).is_file()]
    if not matches:
        raise FileNotFoundError(relative)
    return matches[0]


def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                factor = work[row][column]
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
    return [[columns[column][row] for column in range(10)] for row in range(10)]


def profile_jet(x_value, mode):
    angle = mode * x_value
    p = float(P)
    amplitude = float(AMPLITUDE)
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
    scalar_3 = -8.0 * psi ** -5 * psi_2
    hamiltonian = scalar_3 + tau ** 2 - math.fsum(value * value for value in mixed_k)
    momentum_x = mixed_k_prime[0] - tau_prime + 6.0 * u_1 * mixed_k[0] - 2.0 * u_1 * tau
    return psi, z_value, scalar_3, hamiltonian, momentum_x


fingerprints = {}
for relative in SOURCE_PATHS:
    path = source_path(relative)
    check(f"source exists {relative}", path.is_file())
    fingerprints[relative] = sha256(path)

with source_path(SOURCE_PATHS[-1]).open(encoding="utf-8", newline="") as handle:
    source_rows = {row["source_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
s09 = source_rows["S09"]
check("S09 primary abstract grade", s09["access_grade"] == "PRIMARY_ABSTRACT_METADATA")
check("S09 maximal development scope", "maximal Cauchy development" in s09["exact_supported_scope"])
check("S09 comparison-only limitation", "comparison-only" in s09["limitations"])

primary_path = HERE / "S09_PRIMARY_ABSTRACT_EVIDENCE.json"
check("S09 bounded primary evidence exists", primary_path.is_file())
fingerprints[primary_path.name] = sha256(primary_path)
primary = json.loads(primary_path.read_text(encoding="utf-8"))
fragments = primary["official_abstract_fragments"]
joined_fragments = " ".join(fragments).lower()
check("S09 bounded primary schema", primary["schema"] == "udt-g322-s09-primary-abstract-bounded-evidence-v1")
check("S09 bounded primary grade", primary["source_grade"] == "PRIMARY_PUBLISHER_ABSTRACT_BOUNDED_EXCERPT")
check("S09 bounded primary DOI", primary["doi"] == "10.1007/BF01645389")
check("S09 bounded excerpt word count", sum(len(fragment.split()) for fragment in fragments) == primary["bounded_excerpt_word_count"] == 25)
check("S09 constraint antecedent", "constraint conditions" in joined_fragments)
check("S09 every-development extension", "extension of every other development" in joined_fragments)
check("S09 unique maximal embedding", "embedded in exactly one such maximal development" in joined_fragments)

raw_rank = matrix_rank(tracefree_projector())
fixed_rank = matrix_rank([[int(row == column) for column in range(10)] for row in range(10)])
check("raw tracefree rank nine", raw_rank == 9)
check("fixed Lambda principal rank ten", fixed_rank == 10)

atlas = []
q_values = {}
max_hamiltonian = 0.0
max_momentum = 0.0
for mode in MODES:
    margin = Fraction(100) - 12 * AMPLITUDE * mode ** 2 * (P + AMPLITUDE)
    check(f"regular margin mode={mode}", margin > 0)
    for sign in SIGNS:
        rows = [reconstruct(*profile_jet(2.0 * math.pi * index / SAMPLES, mode), sign)
                for index in range(SAMPLES)]
        local_h = max(abs(row[3]) for row in rows)
        local_m = max(abs(row[4]) for row in rows)
        max_hamiltonian = max(max_hamiltonian, local_h)
        max_momentum = max(max_momentum, local_m)
        check(f"positive gamma mode={mode} sign={sign}", min(row[0] for row in rows) > 0)
        check(f"regular B mode={mode} sign={sign}", min(row[1] for row in rows) > 0)
        check(f"Hamiltonian mode={mode} sign={sign}", local_h < 4e-12)
        check(f"momentum mode={mode} sign={sign}", local_m < 4e-12)
        volume = (2.0 * math.pi) ** 3 * math.fsum(row[0] ** 6 for row in rows) / SAMPLES
        total_scalar = (2.0 * math.pi) ** 3 * math.fsum(
            row[0] ** 6 * row[2] for row in rows
        ) / SAMPLES
        q_value = total_scalar / volume ** (1.0 / 3.0)
        q_values[(mode, sign)] = q_value
        atlas.append({
            "mode": mode,
            "sign": sign,
            "min_psi": min(row[0] for row in rows),
            "min_z": min(row[1] for row in rows),
            "max_hamiltonian": local_h,
            "max_momentum": local_m,
            "Q_R": q_value,
        })

base_q = q_values[(1, 1)]
for mode in MODES:
    for sign in SIGNS:
        check(f"Q_R separator mode={mode} sign={sign}", abs(q_values[(mode, sign)] / base_q - mode ** 2) < 4e-12)

with (HERE / "DATA_INTERFACE.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=tuple(atlas[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(atlas)

with (HERE / "THEOREM_INTERFACE.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("id", "hypothesis", "status", "evidence_type", "boundary"))
    writer.writerows(THEOREM_INTERFACE)

with (HERE / "SCOPE_MATRIX.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("claim", "status"))
    writer.writerows(SCOPE_MATRIX)

result = {
    "schema": "udt-g322-maximal-globally-hyperbolic-development-v1",
    "status": "PASS_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW",
    "landing": LANDING,
    "machine_assertion_count": len(CHECKS),
    "raw_tracefree_principal_rank": raw_rank,
    "fixed_lambda_principal_rank": fixed_rank,
    "constraint_sector": "Lambda=0",
    "max_hamiltonian_residual": max_hamiltonian,
    "max_momentum_residual": max_momentum,
    "theorem_interface_status": "CONDITIONAL_APPLICATION_SUPPORTED__IMPORTED_THEOREM_NOT_MACHINE_PROVED",
    "source_fingerprints": fingerprints,
    "maximal_GH_per_fixed_datum": "CONDITIONAL_IMPORTED_THEOREM_CONSEQUENCE",
    "geodesic_completeness": "OPEN_NOT_ENTAILED",
    "arbitrary_Lorentzian_inextendibility": "OPEN_NOT_ENTAILED",
    "physical_occupancy": "OPEN_NOT_SELECTED",
    "unmarked_cross_datum_classification": "OPEN_NOT_CLASSIFIED",
    "metric_kernel_angular_interface": "UNCHANGED",
}
with (HERE / "DERIVATION_RESULT.json").open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(result, indent=2, sort_keys=True))
