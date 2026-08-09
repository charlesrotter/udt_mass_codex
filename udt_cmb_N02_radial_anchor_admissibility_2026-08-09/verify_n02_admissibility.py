#!/usr/bin/env python3
"""Independent N02 verifier: exact universes, algebra, and fail-closed mutations."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "c73eb657"
INV_N = (Fraction(9658, 10000), Fraction(9470, 10000), Fraction(9284, 10000))
Q_RATIOS = (
    Fraction(-2), Fraction(-1), Fraction(0), Fraction(1, 4),
    Fraction(1, 2), Fraction(3, 4), Fraction(95, 100),
)
HBAR_VALUES = ("0.001", "0.002", "0.005", "0.01", "0.02", "0.05", "0.1", "0.2", "0.5", "1")
CHECKS: dict[str, bool] = {}


def check(name: str, condition: object) -> None:
    CHECKS[name] = bool(condition)
    print(f"CHECK {name}: {CHECKS[name]}")


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fraction_text(value: Fraction | None) -> str:
    if value is None:
        return "-"
    return f"{value.numerator}/{value.denominator}"


def validate_payload(payload: dict[str, object]) -> None:
    if payload.get("status") != "VERIFIED_WITH_CAVEATS__NO_BANKED_REGULAR_CENTER_TO_WALL_C1_C2_ANCHOR__NO_EIGENSOLVE":
        raise ValueError("status")
    if payload.get("key_count") != 20 or not all(dict(payload.get("keys", {})).values()):
        raise ValueError("keys")
    if payload.get("profile_strata_count") != 45 or payload.get("endpoint_strata_count") != 24:
        raise ValueError("census")
    if payload.get("represented_R1_profiles") != 210:
        raise ValueError("profile representation")
    if payload.get("full_C1_center_curvature_residue") != "-6*a":
        raise ValueError("center residue")
    if payload.get("P1_center_result") != "A=(1-r)^n has a=-n and lim[r RicciScalar]=6n!=0; all frozen P1 full-sphere centers are curvature singular":
        raise ValueError("P1 center")
    if payload.get("mixing_center_result") != "h=hbar r^2(1-r)^q passes the necessary O(r^2) collapsing-orbit order only; full Cartesian smoothness is not claimed; RA1 literal h=h0(1-r)^q fails even that necessary order":
        raise ValueError("mixing center")
    if payload.get("wall_result") != "all registered nonzero-mixing q/qcrit<1 rows have B->infinity, finite Liouville length, sub-inverse-square matrix potentials, and a free limit-circle extension family; D/N are unselected control members":
        raise ValueError("wall ownership")
    if payload.get("round_wall_result") != "h=0 with every registered n>1 has infinite Liouville length and a limit-point continuum endpoint; D/N are not free wall data":
        raise ValueError("round wall")
    if payload.get("execution_result") != "NO_BANKED_CENTER_TO_WALL_C1_OR_C2_PROFILE_IS_ADMISSIBLE_AS_A_REGULAR_COMPLETE_CONTROL_ANCHOR":
        raise ValueError("execution")
    if payload.get("maximum_conclusion") != "admissibility map only; no eigensolve, physical profile, boundary selection, spectrum, FD2, data fit, or GPU work":
        raise ValueError("maximum conclusion")


def validate_tables(profiles: list[dict[str, str]], endpoints: list[dict[str, str]]) -> None:
    expected_profiles = set()
    expected_endpoints = set()
    for inv_n in INV_N:
        n = 1 / inv_n
        expected_profiles.add(f"R0_n{float(n):.12f}")
        expected_endpoints.add(f"E0_n{float(n):.12f}")
        for ratio in Q_RATIOS:
            expected_profiles.add(f"R1_n{float(n):.12f}_qr{float(ratio):+.2f}")
            expected_profiles.add(f"R2_n{float(n):.12f}_qr{float(ratio):+.2f}")
            expected_endpoints.add(f"E1_n{float(n):.12f}_qr{float(ratio):+.2f}")
    if len(profiles) != 45 or {row["candidate_id"] for row in profiles} != expected_profiles:
        raise ValueError("exact profile universe")
    if len(endpoints) != 24 or {row["endpoint_id"] for row in endpoints} != expected_endpoints:
        raise ValueError("exact endpoint universe")
    if sum(int(row["represented_h_magnitudes"]) for row in profiles if row["family"] == "R1_CENTER_REGULAR_MIXING_P1") != 210:
        raise ValueError("R1 representation")
    if any(row["execution_disposition"] != "BLOCKED_C1_CENTER_REGULARITY" for row in profiles):
        raise ValueError("execution promotion")
    if any(row["complete_metric_center_status"] != "FAIL_A_LINEAR_TERM" for row in profiles):
        raise ValueError("center status")
    if any(row["B_wall"] != "INFINITY" for row in endpoints if row["family"] == "R1_AND_R2_NONZERO_MIXING_WALL"):
        raise ValueError("B wall stratum")
    round_rows = [row for row in endpoints if row["family"] == "R0_ROUND_P1"]
    mixed_rows = [row for row in endpoints if row["family"] == "R1_AND_R2_NONZERO_MIXING_WALL"]
    if len(round_rows) != 3 or any(row["endpoint_character"] != "LIMIT_POINT" or row["D_N_status"] != "NOT_FREE_ENDPOINT_DATA" for row in round_rows):
        raise ValueError("round endpoint")
    if len(mixed_rows) != 21 or any(row["endpoint_character"] != "LIMIT_CIRCLE_SUB_INVERSE_SQUARE" for row in mixed_rows):
        raise ValueError("mixed endpoint")
    if any("NOT_SELECTED" not in row["D_N_status"] for row in mixed_rows):
        raise ValueError("boundary selection")

    profile_lookup = {row["candidate_id"]: row for row in profiles}
    endpoint_lookup = {row["endpoint_id"]: row for row in endpoints}
    for inv_n in INV_N:
        n = 1 / inv_n
        round_id = f"R0_n{float(n):.12f}"
        expected_round = {
            "candidate_id": round_id,
            "family": "R0_ROUND_P1",
            "inv_n": f"{float(inv_n):.4f}",
            "n_exact": fraction_text(n),
            "q_ratio": "-",
            "q_exact": "-",
            "represented_h_magnitudes": "1",
            "represented_h_values": "0",
            "B_center": "ZERO",
            "B_wall": "ZERO",
            "mixing_center_status": "PASS_H_ZERO",
            "complete_metric_center_status": "FAIL_A_LINEAR_TERM",
            "ricci_r_times_limit": fraction_text(6 * n),
            "wall_liouville_length": "INFINITE",
            "wall_domain_status": "UNIQUE_LIMIT_POINT_CONTINUUM_CONTROL",
            "boundary_ownership": "NO_FREE_D_OR_N_WALL_DATUM",
            "profile_provenance": "P1_DATA_CONDITIONED_CHOSE_NOT_NATIVE",
            "execution_disposition": "BLOCKED_C1_CENTER_REGULARITY",
        }
        if profile_lookup[round_id] != expected_round:
            raise ValueError("round profile field reconstruction")
        endpoint_id = f"E0_n{float(n):.12f}"
        expected_round_endpoint = {
            "endpoint_id": endpoint_id,
            "family": "R0_ROUND_P1",
            "n_exact": fraction_text(n),
            "q_ratio": "-",
            "B_wall": "ZERO",
            "radial_flux_exponent_u": fraction_text(n),
            "frequency_weight_exponent_u": fraction_text(-n),
            "liouville_length": "INFINITE",
            "angular_potential_exponent_x": "DECAYS_TO_ZERO",
            "rotation_potential_exponent_x": "ABSENT",
            "endpoint_character": "LIMIT_POINT",
            "extension_status": "UNIQUE_ENDPOINT_DOMAIN_DERIVED",
            "D_N_status": "NOT_FREE_ENDPOINT_DATA",
        }
        if endpoint_lookup[endpoint_id] != expected_round_endpoint:
            raise ValueError("round endpoint field reconstruction")

        for ratio in Q_RATIOS:
            qcrit = (2 - n) / 2
            q = ratio * qcrit
            B_exponent = 2 * q - n
            p = q + n / 2
            alpha_k = 2 * q / (1 - p)
            alpha_rotation = q / (1 - p)
            for prefix, family, mixing, provenance, count, h_values, B_center, residue in (
                (
                    "R1", "R1_CENTER_REGULAR_MIXING_P1",
                    "PASS_NECESSARY_H_ORDER_R2_ONLY__FULL_SMOOTHNESS_NOT_CLAIMED",
                    "FD1_BANKED_FREE_EXPLORED_CONDITIONAL_FAMILY", "10", ";".join(HBAR_VALUES),
                    "ZERO", fraction_text(6 * n),
                ),
                (
                    "R2", "R2_RA1_LITERAL_LINEAGE",
                    "FAIL_H_ORDER_R0_ON_COLLAPSING_AXIAL_ORBIT",
                    "RA1_LINEAGE_CONTROL_NOT_COMPLETE_C1_CENTER", "1", "SYMBOLIC_NONZERO_H0_LINEAGE",
                    "INFINITY", "NOT_APPLICABLE_STRONGER_COFRAME_SINGULARITY",
                ),
            ):
                candidate_id = f"{prefix}_n{float(n):.12f}_qr{float(ratio):+.2f}"
                expected_profile = {
                    "candidate_id": candidate_id,
                    "family": family,
                    "inv_n": f"{float(inv_n):.4f}",
                    "n_exact": fraction_text(n),
                    "q_ratio": fraction_text(ratio),
                    "q_exact": fraction_text(q),
                    "represented_h_magnitudes": count,
                    "represented_h_values": h_values,
                    "B_center": B_center,
                    "B_wall": "INFINITY" if B_exponent < 0 else ("FINITE_NONZERO" if B_exponent == 0 else "ZERO"),
                    "mixing_center_status": mixing,
                    "complete_metric_center_status": "FAIL_A_LINEAR_TERM",
                    "ricci_r_times_limit": residue,
                    "wall_liouville_length": "FINITE" if p < 1 else "INFINITE",
                    "wall_domain_status": "LIMIT_CIRCLE_SUB_INVERSE_SQUARE",
                    "boundary_ownership": "FREE_SELF_ADJOINT_EXTENSION_FAMILY_REQUIRED",
                    "profile_provenance": provenance,
                    "execution_disposition": "BLOCKED_C1_CENTER_REGULARITY",
                }
                if profile_lookup[candidate_id] != expected_profile:
                    raise ValueError("mixed profile field reconstruction")
            mixed_endpoint_id = f"E1_n{float(n):.12f}_qr{float(ratio):+.2f}"
            expected_mixed_endpoint = {
                "endpoint_id": mixed_endpoint_id,
                "family": "R1_AND_R2_NONZERO_MIXING_WALL",
                "n_exact": fraction_text(n),
                "q_ratio": fraction_text(ratio),
                "B_wall": "INFINITY" if B_exponent < 0 else ("FINITE_NONZERO" if B_exponent == 0 else "ZERO"),
                "radial_flux_exponent_u": fraction_text(p),
                "frequency_weight_exponent_u": fraction_text(-p),
                "liouville_length": "FINITE" if p < 1 else "INFINITE",
                "angular_potential_exponent_x": fraction_text(alpha_k),
                "rotation_potential_exponent_x": fraction_text(alpha_rotation),
                "endpoint_character": "LIMIT_CIRCLE_SUB_INVERSE_SQUARE",
                "extension_status": "REQUIRES_FREE_EXTENSION_CENSUS",
                "D_N_status": "ADMISSIBLE_CONTROL_MEMBERS_NOT_SELECTED__FULL_EXTENSION_FAMILY_OPEN",
            }
            if endpoint_lookup[mixed_endpoint_id] != expected_mixed_endpoint:
                raise ValueError("mixed endpoint field reconstruction")


def independent_center_residue() -> sp.Expr:
    """Direct tensor recomputation at general linear A and regular O(r^2) mixing."""
    r, theta = sp.symbols("r theta", positive=True)
    a, b, kappa = sp.symbols("a b kappa", real=True)
    A = 1 + a * r + b * r**2
    h = kappa * r**2
    sine = sp.sin(theta)
    metric = sp.Matrix([
        [-A, 0, 0, h * sine**2],
        [0, 1 / A, 0, 0],
        [0, 0, r**2, 0],
        [h * sine**2, 0, 0, r**2 * sine**2],
    ])
    inverse = metric.inv()
    coordinates = (sp.symbols("t"), r, theta, sp.symbols("psi"))
    size = 4
    gamma = [[[
        sp.Rational(1, 2) * sum(
            inverse[upper, index]
            * (
                sp.diff(metric[index, right], coordinates[left])
                + sp.diff(metric[index, left], coordinates[right])
                - sp.diff(metric[left, right], coordinates[index])
            )
            for index in range(size)
        )
        for right in range(size)] for left in range(size)] for upper in range(size)]
    ricci = [[sum(
        sp.diff(gamma[upper][left][right], coordinates[upper])
        - sp.diff(gamma[upper][left][upper], coordinates[right])
        + sum(
            gamma[upper][upper][index] * gamma[index][left][right]
            - gamma[upper][right][index] * gamma[index][left][upper]
            for index in range(size)
        )
        for upper in range(size)
    ) for right in range(size)] for left in range(size)]
    scalar = sum(inverse[left, right] * ricci[left][right] for left in range(size) for right in range(size))
    return sp.simplify(sp.limit(r * scalar, r, 0, dir="+"))


def main() -> None:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    profiles = read_tsv("PROFILE_STRATA.tsv")
    endpoints = read_tsv("ENDPOINT_OWNERSHIP.tsv")
    validate_payload(payload)
    validate_tables(profiles, endpoints)
    check("V01_payload", True)
    check("V02_exact_table_universes", True)

    a = sp.symbols("a", real=True)
    residue = independent_center_residue()
    check("V03_independent_full_C1_center_residue", sp.simplify(residue + 6 * a) == 0)

    algebra_ok = True
    endpoint_lookup = {row["endpoint_id"]: row for row in endpoints}
    for inv_n in INV_N:
        n = 1 / inv_n
        algebra_ok &= n > 1
        for ratio in Q_RATIOS:
            qcrit = (2 - n) / 2
            q = ratio * qcrit
            p = q + n / 2
            endpoint = endpoint_lookup[f"E1_n{float(n):.12f}_qr{float(ratio):+.2f}"]
            algebra_ok &= 2 * q - n < 0
            algebra_ok &= p < 1
            algebra_ok &= Fraction(endpoint["radial_flux_exponent_u"]) == p
            algebra_ok &= Fraction(endpoint["frequency_weight_exponent_u"]) == -p
            algebra_ok &= Fraction(endpoint["angular_potential_exponent_x"]) == 2 * q / (1 - p)
            algebra_ok &= Fraction(endpoint["rotation_potential_exponent_x"]) == q / (1 - p)
    check("V04_independent_endpoint_exponents", algebra_ok)
    check("V05_subcritical_wall", all(Fraction(row["angular_potential_exponent_x"]) > -2 for row in endpoints if row["family"] != "R0_ROUND_P1"))

    source_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            data = subprocess.run(["git", "show", f"{PREREG_COMMIT}:{path_text}"], cwd=ROOT, check=True, capture_output=True).stdout
            source_ok &= hashlib.sha256(data).hexdigest() == digest
    check("V06_source_manifest", source_ok)

    payload_mutations = {
        "M01_status_promotion": ("status", "PHYSICAL_C1_SPECTRUM_AUTHORIZED"),
        "M02_profile_loss": ("profile_strata_count", 44),
        "M03_endpoint_loss": ("endpoint_strata_count", 23),
        "M04_R1_loss": ("represented_R1_profiles", 200),
        "M05_center_erasure": ("full_C1_center_curvature_residue", "0"),
        "M06_execution_promotion": ("execution_result", "C1_ANCHOR_ADMISSIBLE"),
        "M07_wall_selection": ("wall_result", "Dirichlet is physically selected"),
        "M08_round_wall_selection": ("round_wall_result", "D is selected"),
        "M09_eigensolve": ("maximum_conclusion", "eigensolve and FD2 authorized"),
        "M10_GPU": ("maximum_conclusion", "GPU CMB fit authorized"),
        "M11_appended_eigensolve_GPU": (
            "maximum_conclusion",
            str(payload["maximum_conclusion"]) + "; eigensolve and GPU work authorized",
        ),
        "M12_appended_physical_D": (
            "wall_result",
            str(payload["wall_result"]) + "; Dirichlet is physically selected",
        ),
    }
    caught: dict[str, bool] = {}
    for name, (field, value) in payload_mutations.items():
        trial = copy.deepcopy(payload)
        trial[field] = value
        try:
            validate_payload(trial)
        except ValueError:
            caught[name] = True
        else:
            caught[name] = False
    check("V07_payload_mutations", len(caught) == 12 and all(caught.values()))

    table_trials: dict[str, tuple[list[dict[str, str]], list[dict[str, str]]]] = {
        "T01_missing_profile": (profiles[:-1], endpoints),
        "T02_duplicate_profile": (profiles + [copy.deepcopy(profiles[0])], endpoints),
        "T03_missing_endpoint": (profiles, endpoints[:-1]),
    }
    center_trial = copy.deepcopy(profiles)
    center_trial[0]["complete_metric_center_status"] = "PASS"
    table_trials["T04_center_promotion"] = (center_trial, endpoints)
    execution_trial = copy.deepcopy(profiles)
    execution_trial[0]["execution_disposition"] = "MOVE_READY"
    table_trials["T05_execution_promotion"] = (execution_trial, endpoints)
    B_trial = copy.deepcopy(endpoints)
    next(row for row in B_trial if row["family"] != "R0_ROUND_P1")["B_wall"] = "ZERO"
    table_trials["T06_B_stratum_loss"] = (profiles, B_trial)
    round_trial = copy.deepcopy(endpoints)
    next(row for row in round_trial if row["family"] == "R0_ROUND_P1")["D_N_status"] = "PHYSICAL_SELECTION"
    table_trials["T07_round_boundary_import"] = (profiles, round_trial)
    mixed_trial = copy.deepcopy(endpoints)
    next(row for row in mixed_trial if row["family"] != "R0_ROUND_P1")["D_N_status"] = "PHYSICAL_SELECTION"
    table_trials["T08_mixed_boundary_selection"] = (profiles, mixed_trial)
    q_trial = copy.deepcopy(profiles)
    next(row for row in q_trial if row["family"] == "R1_CENTER_REGULAR_MIXING_P1")["q_exact"] = "999/1"
    table_trials["T09_corrupt_q_exact"] = (q_trial, endpoints)
    count_trial = copy.deepcopy(profiles)
    r1_count_rows = [row for row in count_trial if row["family"] == "R1_CENTER_REGULAR_MIXING_P1"]
    r1_count_rows[0]["represented_h_magnitudes"] = "9"
    r1_count_rows[1]["represented_h_magnitudes"] = "11"
    table_trials["T10_redistributed_hbar_counts"] = (count_trial, endpoints)
    enum_trial = copy.deepcopy(endpoints)
    next(row for row in enum_trial if row["family"] != "R0_ROUND_P1")["D_N_status"] = "NOT_SELECTED__DIRICHLET_NATIVE"
    table_trials["T11_contradictory_D_N_enum"] = (profiles, enum_trial)
    table_caught: dict[str, bool] = {}
    for name, tables in table_trials.items():
        try:
            validate_tables(*tables)
        except ValueError:
            table_caught[name] = True
        else:
            table_caught[name] = False
    check("V08_table_mutations", len(table_caught) == 11 and all(table_caught.values()))

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    check("V09_scope", "Do not write or run an eigensolver" in prereg and "No candidate is ranked" in prereg)
    check(
        "V10_no_physical_selection",
        all(
            row["D_N_status"]
            == (
                "NOT_FREE_ENDPOINT_DATA"
                if row["family"] == "R0_ROUND_P1"
                else "ADMISSIBLE_CONTROL_MEMBERS_NOT_SELECTED__FULL_EXTENSION_FAMILY_OPEN"
            )
            for row in endpoints
        ),
    )

    if not all(CHECKS.values()):
        raise SystemExit("independent N02 admissibility verification failed")
    result = {
        "verdict": "VERIFIED_WITH_CAVEATS",
        "check_count": len(CHECKS),
        "checks": CHECKS,
        "independent_center_residue": str(residue),
        "payload_mutations": caught,
        "table_mutations": table_caught,
        "mutation_count": len(caught) + len(table_caught),
        "external_adversarial_review": "ACCEPTED_AFTER_FIVE_FAIL_CLOSED_REPAIRS__SEE_EXTERNAL_ADVERSARIAL_REVIEW.md",
        "remaining_gate": "NONE_FOR_THIS_BOUNDED_ADMISSIBILITY_RESULT",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(CHECKS)}/{len(CHECKS)} independent checks; {len(caught)+len(table_caught)}/{len(caught)+len(table_caught)} mutations caught")


if __name__ == "__main__":
    main()
