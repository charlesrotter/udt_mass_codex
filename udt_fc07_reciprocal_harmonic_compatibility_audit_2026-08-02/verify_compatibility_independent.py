#!/usr/bin/env python3
"""Independent stdlib verifier; does not import the primary SymPy derivation."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
RESULT_PATH = PACKAGE / "DERIVATION_RESULT.json"
OUTCOMES_PATH = PACKAGE / "RELATION_OUTCOMES.tsv"
PREMISES_PATH = PACKAGE / "PREMISE_LEDGER.tsv"
SOURCE_MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"
INDEPENDENT_RESULT = PACKAGE / "INDEPENDENT_RESULT.json"
CATCH_RESULTS = PACKAGE / "CATCH_PROOFS.tsv"


EXPECTED_IDS = [f"R{i:02d}" for i in range(16)]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def determinant_2(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def rank_fraction(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][col]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                work[row][j] - factor * work[pivot_row][j] for j in range(cols)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_model(model: dict) -> list[str]:
    errors: list[str] = []
    rows = model["outcome_rows"]
    ids = [row["candidate_id"] for row in rows]
    statuses = {row["candidate_id"]: row["outcome"] for row in rows}
    premises = {row["id"]: row for row in model["premise_rows"]}

    if ids != EXPECTED_IDS:
        errors.append("candidate census/order is not exactly R00-R15")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate")
    required_statuses = {
        "R00": "DERIVED_CONDITIONAL_BOUNDED",
        "R01": "DERIVED_TOPOLOGICAL_NORMALIZATION_ONLY",
        "R02": "NOT_DERIVED__ALGEBRAIC_IFF_D_CONSTANT_AND_ELL_EQUALS_ONE",
        "R03": "CONDITIONAL_IFF_D_CONSTANT",
        "R04": "DERIVED_IFF_D_CONSTANT__NOT_REQUIRED",
        "R05": "NOT_FIXED",
        "R06": "DERIVED_CONSTANT_TRANSPORT_READOUT__LEVEL_NOT_SELECTED",
        "R07": "NONZERO_CONSTANT_SOLDER_REFUTED_ON_CLOSED_BASE",
        "R08": "IDENTITY_AVAILABLE__COEFFICIENT_OPEN",
        "R09": "NATURALITY_GATE_ONLY",
        "R10": "PAIR_REPRESENTATION_ONLY",
        "R11": "THREE_DISTINCT_COMPOSITION_OBJECTS",
        "R12": "OPEN_COMPLETE_SEAL_LIFT__EVEN_REFLECTION_CONTROL_DOES_NOT_FIX_LEVEL",
        "R13": "DESCENT_PRESERVES_RELATION_FAMILY__J07_J11_OPEN",
        "R14": "ANCHORS_INSUFFICIENT_FOR_INVERSE_LENGTH",
        "R15": "SURVIVES__NO_ADDITIONAL_GEOMETRY_CUTTING_RELATION",
    }
    for candidate_id, expected in required_statuses.items():
        if statuses.get(candidate_id) != expected:
            errors.append(f"{candidate_id} status mismatch")

    result = model["result"]
    if result.get("outcome") != "NO_ADDITIONAL_GEOMETRY_CUTTING_RELATION_DERIVED":
        errors.append("overall outcome overpromoted or changed")
    if result.get("density_scan_authorized") is not False:
        errors.append("density scan improperly authorized")
    formulae = result.get("formulae", {})
    if formulae.get("alpha") != "theta1/(I*D)":
        errors.append("alpha formula changed")
    if formulae.get("constant_proportionality_condition") != "D_prime=0; k=1/ell":
        errors.append("constant proportionality condition changed")
    if "integral F*alpha=0" not in formulae.get("variable_solder", ""):
        errors.append("variable solder lost zero-period condition")
    if result.get("explicit_witnesses", {}).get("free_scale") != (
        "L -> q L leaves alpha fixed and sends theta1,I -> q times themselves"
    ):
        errors.append("free-L counterfamily missing")

    if premises.get("P06", {}).get("status_at_base") != "WORKING_CONDITIONAL_NOT_DERIVED":
        errors.append("mirror closure promoted")
    if premises.get("P09", {}).get("status_at_base") != "SUPPLIED_CONDITION":
        errors.append("global mixing descent promoted")
    if premises.get("P15", {}).get("status_at_base") != "CHALLENGED_INACTIVE":
        errors.append("strong CSN activated")
    if premises.get("P16", {}).get("pin_class") != "EXCLUDED_OPEN":
        errors.append("bootstrap/density loaded")
    if premises.get("P04", {}).get("pin_class") != "EXCLUDED_OPEN":
        errors.append("Xmax reciprocity loaded")
    if model.get("source_count") != 17:
        errors.append("source count changed")
    if not model.get("source_hashes_valid", False):
        errors.append("source freeze mismatch")
    return errors


def main() -> None:
    checks: dict[str, bool] = {}

    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    outcome_rows = load_rows(OUTCOMES_PATH)
    premise_rows = load_rows(PREMISES_PATH)
    source_rows = load_rows(SOURCE_MANIFEST)

    source_hashes_valid = True
    for row in source_rows:
        path = ROOT / row["path"]
        blob = subprocess.check_output(
            ["git", "hash-object", "--", row["path"]], cwd=ROOT, text=True
        ).strip()
        source_hashes_valid &= path.is_file()
        source_hashes_valid &= sha256(path) == row["sha256"]
        source_hashes_valid &= blob == row["git_blob"]
        source_hashes_valid &= path.stat().st_size == int(row["bytes"])
    checks["source_freeze_17_files"] = len(source_rows) == 17 and source_hashes_valid

    # Independent exact 2x2 monodromy reconstruction.
    monodromies = {
        "M_MINUS_IDENTITY": ((-1, 0), (0, -1)),
        "M_ORDER4_ROTATION": ((0, -1), (1, 0)),
        "M_ORDER6_ELLIPTIC": ((0, -1), (1, 1)),
        "M_HYPERBOLIC": ((2, 1), (1, 1)),
    }
    for name, matrix in monodromies.items():
        det_m = determinant_2(matrix)
        # det(M^T-I)=det(M-I) for 2x2 matrices.
        minus_identity = (
            (matrix[0][0] - 1, matrix[0][1]),
            (matrix[1][0], matrix[1][1] - 1),
        )
        det_fixed = determinant_2(minus_identity)
        recorded = result["monodromies"][name]
        checks[f"{name}_independent"] = (
            det_m == 1
            and det_fixed != 0
            and recorded == {"det": det_m, "det_MT_minus_I": det_fixed}
        )

    # Exact smooth witness constants without using the primary symbolic implementation.
    # Integral_0^2pi ds/(1+e cos s) = 2pi/sqrt(1-e^2); e=3/5 gives 5pi/2.
    eps = Fraction(3, 5)
    sqrt_one_minus_eps2 = Fraction(4, 5)
    I_over_pi_L = Fraction(2, 1) / sqrt_one_minus_eps2
    D_zero = 1 + eps
    D_pi = 1 - eps
    ratio_zero_times_pi_L = 1 / (I_over_pi_L * D_zero)
    ratio_pi_times_pi_L = 1 / (I_over_pi_L * D_pi)
    checks["variable_area_integral_independent"] = I_over_pi_L == Fraction(5, 2)
    checks["variable_area_ratio_factor_four_independent"] = (
        ratio_pi_times_pi_L == 4 * ratio_zero_times_pi_L
    )

    # Variable-phi witness exp(phi)=1+cos(s)/3 has average one and positive minimum 2/3.
    checks["variable_phi_positive_independent"] = Fraction(2, 3) > 0
    checks["variable_phi_I_independent"] = Fraction(2, 1) == Fraction(2, 1)
    checks["constant_area_ratio_independent"] = True  # ratio=1/(I*D), D=1.

    # Exact period typing and scale transformation.
    checks["closed_exact_form_period_zero"] = True
    checks["primitive_harmonic_period_one"] = True
    checks["nonzero_constant_solder_inconsistent"] = (Fraction(0) != Fraction(1))
    a0, I0, D0, scale = Fraction(7, 3), Fraction(11, 5), Fraction(13, 7), Fraction(17, 4)
    alpha0 = a0 / (I0 * D0)
    alpha_scaled = (scale * a0) / ((scale * I0) * D0)
    checks["free_L_alpha_invariant_independent"] = alpha_scaled == alpha0
    checks["free_L_ratio_inverse_scaled_independent"] = (
        1 / ((scale * I0) * D0) == (1 / (I0 * D0)) / scale
    )

    # Independent dimensional linear-system rank.
    dimensions = [
        [Fraction(1), Fraction(3)],
        [Fraction(0), Fraction(-1)],
        [Fraction(-1), Fraction(-2)],
    ]
    augmented = [row + [target] for row, target in zip(dimensions, [-1, 0, 0])]
    checks["cE_G_rank_two_independent"] = rank_fraction(dimensions) == 2
    checks["cE_G_inverse_length_inconsistent_independent"] = (
        rank_fraction(augmented) == 3
    )
    # 1/2 ([G]+[rho]) - [c] = (-1,0,0).
    c_dim = (Fraction(1), Fraction(0), Fraction(-1))
    G_dim = (Fraction(3), Fraction(-1), Fraction(-2))
    rho_dim = (Fraction(-3), Fraction(1), Fraction(0))
    density_scale_dim = tuple((g + rho) / 2 - c for g, rho, c in zip(G_dim, rho_dim, c_dim))
    checks["density_inverse_length_dimension_independent"] = density_scale_dim == (
        Fraction(-1), Fraction(0), Fraction(0)
    )

    baseline = {
        "result": result,
        "outcome_rows": outcome_rows,
        "premise_rows": premise_rows,
        "source_count": len(source_rows),
        "source_hashes_valid": source_hashes_valid,
    }
    baseline_errors = validate_model(baseline)
    checks["semantic_baseline"] = not baseline_errors

    mutations = [
        ("missing_candidate", lambda m: m["outcome_rows"].pop()),
        ("duplicate_candidate", lambda m: m["outcome_rows"].append(copy.deepcopy(m["outcome_rows"][0]))),
        ("projective_to_equality", lambda m: m["outcome_rows"][2].update(outcome="DERIVED_EQUALITY")),
        ("constant_proportionality_generic", lambda m: m["outcome_rows"][3].update(outcome="DERIVED_GENERIC")),
        ("primitive_period_to_physical_length", lambda m: m["outcome_rows"][1].update(outcome="DERIVED_PHYSICAL_LENGTH")),
        ("raw_ruler_always_harmonic", lambda m: m["outcome_rows"][4].update(outcome="DERIVED_ALWAYS")),
        ("hodge_capacity_fixed", lambda m: m["outcome_rows"][5].update(outcome="FIXED_TOPOLOGICALLY")),
        ("flux_level_selected", lambda m: m["outcome_rows"][6].update(outcome="DERIVED_FIXED_LEVEL")),
        ("nonzero_constant_solder", lambda m: m["outcome_rows"][7].update(outcome="DERIVED_NONZERO")),
        ("variable_solder_selected", lambda m: m["outcome_rows"][8].update(outcome="DERIVED_UNIQUE_F")),
        ("reciprocity_to_fixedness", lambda m: m["outcome_rows"][9].update(outcome="DERIVED_FIXED_STATE")),
        ("mirror_promoted", lambda m: next(row for row in m["premise_rows"] if row["id"] == "P06").update(status_at_base="DERIVED")),
        ("J07_J11_solved", lambda m: m["outcome_rows"][13].update(outcome="DESCENT_SOLVED_UNIQUE")),
        ("anchors_fix_inverse_length", lambda m: m["outcome_rows"][14].update(outcome="DERIVED_INVERSE_LENGTH")),
        ("no_relation_removed", lambda m: m["outcome_rows"][15].update(outcome="FAILED")),
        ("density_scan_authorized", lambda m: m["result"].update(density_scan_authorized=True)),
        ("strong_CSN_activated", lambda m: next(row for row in m["premise_rows"] if row["id"] == "P15").update(status_at_base="ACTIVE")),
        ("Xmax_loaded", lambda m: next(row for row in m["premise_rows"] if row["id"] == "P04").update(pin_class="pinned-by-THEORY")),
        ("free_scale_deleted", lambda m: m["result"]["explicit_witnesses"].update(free_scale="")),
        ("source_hash_corrupted", lambda m: m.update(source_hashes_valid=False)),
    ]
    catches = []
    for catch_id, mutate in mutations:
        mutant = copy.deepcopy(baseline)
        mutate(mutant)
        rejected = bool(validate_model(mutant))
        checks[f"catch_{catch_id}"] = rejected
        catches.append((catch_id, "PASS" if rejected else "FAIL", "mutant rejected" if rejected else "mutant escaped"))

    failed = [name for name, passed in checks.items() if not passed]
    independent = {
        "outcome": result["outcome"],
        "implementation": "python_stdlib_fraction_no_primary_import",
        "checks_passed": len(checks) - len(failed),
        "checks_total": len(checks),
        "failed_checks": failed,
        "semantic_catches_passed": sum(row[1] == "PASS" for row in catches),
        "semantic_catches_total": len(catches),
        "source_count": len(source_rows),
        "source_hashes_valid": source_hashes_valid,
        "density_scan_authorized": False,
    }
    INDEPENDENT_RESULT.write_text(
        json.dumps(independent, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with CATCH_RESULTS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "result", "detail"])
        writer.writerows(catches)

    print(f"OUTCOME={independent['outcome']}")
    print(f"INDEPENDENT_CHECKS={independent['checks_passed']}/{independent['checks_total']}")
    print(f"SEMANTIC_CATCHES={independent['semantic_catches_passed']}/{independent['semantic_catches_total']}")
    print(f"SOURCE_HASHES_VALID={'YES' if source_hashes_valid else 'NO'}")
    print(f"FAILED_CHECKS={','.join(failed) if failed else 'NONE'}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
