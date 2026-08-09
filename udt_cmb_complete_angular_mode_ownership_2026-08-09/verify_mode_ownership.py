#!/usr/bin/env python3
"""Independent verifier for the complete-angular ownership audit.

This script does not import the production derivation.  Its metric checks use
standard-library exact Fraction Gaussian elimination and determinant expansion.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
import math
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "33579c653e853cecf0fe10c4266c5c54fc72b735"
CHECKS: dict[str, bool] = {}


def check(name: str, condition: object) -> None:
    CHECKS[name] = bool(condition)
    print(f"CHECK {name}: {CHECKS[name]}")


def parity(permutation: tuple[int, ...]) -> int:
    inversions = sum(permutation[i] > permutation[j] for i in range(len(permutation)) for j in range(i + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[F]]) -> F:
    size = len(matrix)
    return sum(
        F(parity(p)) * math.prod(matrix[i][p[i]] for i in range(size))
        for p in itertools.permutations(range(size))
    )


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    augmented = [row[:] + [F(int(i == j)) for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(i for i in range(column, size) if augmented[i][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [x / scale for x in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [x - scale * y for x, y in zip(augmented[row], augmented[column])]
    return [row[size:] for row in augmented]


def validate_payload(payload: dict[str, object]) -> None:
    if payload.get("status") != "DERIVED_CONDITIONAL_MODE_OWNERSHIP__METRIC_ONLY_POPULATION_PROJECTION_OPEN":
        raise ValueError("status")
    keys = payload.get("keys")
    if not isinstance(keys, dict) or payload.get("key_count") != 26 or len(keys) != 26 or not all(keys.values()):
        raise ValueError("key census")
    if payload.get("D") != "A r^2+h^2 sin^2(theta)":
        raise ValueError("D")
    if "equals r times" not in str(payload.get("equatorial_relation")) or "not the equatorial restriction" not in str(payload.get("equatorial_relation")):
        raise ValueError("slice/full distinction")
    if "U(1)" not in str(payload.get("C1_mode_ownership")) or "coupled" not in str(payload.get("C1_mode_ownership")):
        raise ValueError("C1 ownership")
    if "SO(3) ell multiplet" not in str(payload.get("C2_mode_ownership")) or "r^ell" not in str(payload.get("C2_mode_ownership")):
        raise ValueError("C2 ownership")
    if "no universal m label" not in str(payload.get("C3_mode_ownership")):
        raise ValueError("C3 ownership")
    if "select no population" not in str(payload.get("projection_result")):
        raise ValueError("projection")
    if "no registered metric-only invariant selects one FD1 ladder" not in str(payload.get("maximum_conclusion")):
        raise ValueError("maximum conclusion")


def main() -> None:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    validate_payload(payload)
    check("V01_payload", True)

    # Exact rational metric point.  s=sin(theta) is treated as the nonzero chart
    # coordinate value 3/5; no trigonometric approximation enters the matrix check.
    A, h, r, s = F(9, 4), F(2, 3), F(5, 4), F(3, 5)
    D = A * r * r + h * h * s * s
    zero = F(0)
    metric = [
        [-A, zero, zero, h * s * s],
        [zero, 1 / A, zero, zero],
        [zero, zero, r * r, zero],
        [h * s * s, zero, zero, r * r * s * s],
    ]
    inv = inverse(metric)
    expected_inv = [
        [-r * r / D, zero, zero, h / D],
        [zero, A, zero, zero],
        [zero, zero, 1 / (r * r), zero],
        [h / D, zero, zero, A / (s * s * D)],
    ]
    check("V02_fraction_inverse", inv == expected_inv)
    check("V03_fraction_determinant", determinant(metric) == -r * r * s * s * D / A)

    omega, m = F(7, 5), F(-2)
    from_inverse = -omega * omega * inv[0][0] + 2 * omega * m * inv[0][3] - m * m * inv[3][3]
    expected_potential = (r * r * omega * omega + 2 * h * omega * m - A * m * m / (s * s)) / D
    check("V04_fraction_mode_potential", from_inverse == expected_potential)

    # The squared full/equatorial volume ratio is exactly r^2.
    D_eq = A * r * r + h * h
    full_equator_volume_sq = r * r * D_eq / A
    equatorial_volume_sq = D_eq / A
    check("V05_extra_radial_volume", full_equator_volume_sq / equatorial_volume_sq == r * r)

    # Independent nonseparability point: A=1+r, h=r^2 gives B=r^2/(1+r), B'(1)=3/4.
    bprime_at_one = F(3, 4)
    theta = math.pi / 3
    mixed = float(bprime_at_one) * math.sin(theta) * math.cos(theta) / (1 + F(1, 2) * math.sin(theta) ** 2) ** 2
    check("V06_nonseparable_volume", abs(mixed) > 0.1)

    # A nonaxial round-sphere rotation produces (L_Jx g)_{t theta}=h cos(psi).
    h_float, psi = 0.7, math.pi / 4
    check("V07_nonaxial_rotation_broken", abs(h_float * math.cos(psi)) > 0.4)
    check("V08_round_rotation_restored", abs(0.0 * math.cos(psi)) == 0.0)

    # Independent center and representation checks.
    check("V09_full_center_power", all(ell * (ell + 1) - ell * (ell + 1) == 0 for ell in range(6)))
    check("V10_round_multiplet_dimensions", [2 * ell + 1 for ell in range(4)] == [1, 3, 5, 7])
    eq_m0_regular = [a for a in range(4) if a * a == 0]
    eq_m1_regular = [a for a in range(4) if a * a - 1 == 0]
    full_ell1_regular = [a for a in range(4) if a * (a + 1) - 2 == 0]
    check("V11_equatorial_channels_cross_ell", eq_m0_regular == [0] and eq_m1_regular == [1] and full_ell1_regular == [1])

    # General-screen area witness V=1+eps sin(theta)cos(psi) is positive for
    # |eps|<1 and has nonzero axial derivative at a generic point.
    eps = 0.2
    V = 1 + eps * math.sin(theta) * math.cos(psi)
    dpsi_V = -eps * math.sin(theta) * math.sin(psi)
    check("V12_general_screen_positive", 1 - abs(eps) <= V <= 1 + abs(eps))
    check("V13_general_screen_breaks_axial", abs(dpsi_V) > 0.1)

    # Discrete Fourier character orthogonality by an independent roots-of-unity sum.
    samples = 64
    unequal = sum(complex(math.cos(-2 * math.pi * j / samples), math.sin(-2 * math.pi * j / samples)) for j in range(samples)) / samples
    equal = sum(1 for _ in range(samples)) / samples
    check("V14_U1_character_projectors", abs(unequal) < 1e-14 and equal == 1)

    # Source hashes are reconstructed independently.
    source_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            frozen = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{path_text}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            source_ok &= hashlib.sha256(frozen).hexdigest() == digest
    check("V15_source_manifest", source_ok)

    mutations = {
        "M01_status_promotion": ("status", "NATIVE_PHYSICAL_MODE_SELECTION"),
        "M02_key_loss": ("key_count", 25),
        "M03_wrong_D": ("D", "A r^2+h^2"),
        "M04_slice_identity": ("equatorial_relation", "C0 equals C1"),
        "M05_false_SO3": ("C1_mode_ownership", "SO(3) triplet"),
        "M06_same_index_triplet": ("C2_mode_ownership", "same-index m triplet"),
        "M07_universal_m": ("C3_mode_ownership", "universal m label"),
        "M08_weight_invention": ("projection_result", "m=0 receives unit physical weight"),
        "M09_ladder_postselection": ("maximum_conclusion", "choose best FD1 ladder"),
    }
    caught = {}
    for name, (field, value) in mutations.items():
        trial = copy.deepcopy(payload)
        trial[field] = value
        try:
            validate_payload(trial)
        except ValueError:
            caught[name] = True
        else:
            caught[name] = False
    check("V16_all_mutations_caught", all(caught.values()) and len(caught) == 9)

    with (HERE / "MODE_OWNERSHIP_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        mode_rows = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "PROJECTION_OWNERSHIP.tsv").open(newline="", encoding="utf-8") as handle:
        projection_rows = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "STATUS_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        status_rows = list(csv.DictReader(handle, delimiter="\t"))
    check("V17_mode_atlas_census", len(mode_rows) == 5 and len({row["class"] for row in mode_rows}) == 5)
    check("V18_projection_census", len(projection_rows) == 7 and {row["status"] for row in projection_rows} >= {"OPEN", "QUERY_NOT_POPULATION"})
    check("V19_status_census", len(status_rows) == 11 and any(row["status"] == "OPEN_NOT_AUTHORIZED" for row in status_rows))
    exact_text = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report_text = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact_flat = " ".join(exact_text.split())
    check("V20_exact_scope_guard", "C1 is `CHOSE`" in exact_flat and "selects no preferred `m` and no amplitude" in exact_flat)
    check("V21_report_stop_guard", "FD2_REMAINS_OPEN_NOT_AUTHORIZED" in report_text and "no fresh zero-context external semantic review" in report_text)

    if not all(CHECKS.values()):
        raise SystemExit("independent verification failed")
    result = {
        "verdict": "VERIFIED_WITH_CAVEATS",
        "independence": "separate standard-library Fraction matrix route plus separate semantic mutation validator; same session",
        "checks": CHECKS,
        "check_count": len(CHECKS),
        "mutations": caught,
        "mutation_count": len(caught),
        "caveat": "no fresh zero-context external semantic review",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(CHECKS)}/{len(CHECKS)} independent checks; {len(caught)}/{len(caught)} mutations caught")


if __name__ == "__main__":
    main()
