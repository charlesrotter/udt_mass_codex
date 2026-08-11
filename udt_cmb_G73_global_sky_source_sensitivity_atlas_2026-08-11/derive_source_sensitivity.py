#!/usr/bin/env python3
"""Derive the bounded G73 global-sky source-sensitivity classification."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G72_ATLAS = ROOT / "udt_cmb_G72_metric_screen_response_join_2026-08-11/G68_RESPONSE_ATLAS.tsv"
LANDING = (
    "REGULAR_SKY_RESPONSE_SOURCE_INVERTIBLE__"
    "ROBUST_KALEIDOSCOPE_REQUIRES_GLOBAL_BRANCHING_SINGULARITY_OR_SOURCE_RESTRICTION"
)
ANGLES_DEG = (5.0, 15.0, 30.0)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_sources() -> int:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    for row in manifest:
        target = ROOT / row["path"]
        assert target.is_file() and digest(target) == row["sha256"], target
    return len(manifest)


def alignment_fraction(chi: float, cone_degrees: float) -> float:
    epsilon = math.radians(cone_degrees)
    return (2.0 / math.pi) * math.atan(math.exp(2.0 * chi) * math.tan(epsilon))


def exact_checks() -> dict[str, bool | str]:
    a, b, c, d = sp.symbols("a b c d", real=True)
    determinant = a * d - b * c
    M = sp.Matrix([[a, b], [c, d]])
    Minv = sp.Matrix([[d, -b], [-c, a]]) / determinant
    invertible_reconstruction = sp.simplify(M * Minv - sp.eye(2)) == sp.zeros(2)

    ell, q, t = sp.symbols("ell q t", positive=True)
    canonical = ell * sp.diag(q, 1 / q)
    canonical_determinant = sp.simplify(canonical.det() - ell**2) == 0
    tangent_compression = sp.simplify((canonical[1, 1] * t) / canonical[0, 0] - t / q**2) == 0

    # A finite regular global response: three source pixels, invertible local blocks, and a
    # permutation of observer pixels. It retains all six source degrees of freedom exactly.
    B0 = sp.Matrix([[2, 0], [0, 1]])
    B1 = sp.Matrix([[1, 1], [0, 1]])
    B2 = sp.Matrix([[3, 0], [0, 2]])
    block = sp.diag(B0, B1, B2)
    pixel_permutation = sp.zeros(6)
    order = (2, 0, 1)
    for target_pixel, source_pixel in enumerate(order):
        for channel in range(2):
            pixel_permutation[2 * target_pixel + channel, 2 * source_pixel + channel] = 1
    global_map = pixel_permutation * block
    global_regular_full_rank = global_map.rank() == 6 and global_map.det() != 0
    global_inverse_exact = sp.simplify(global_map.inv() * global_map - sp.eye(6)) == sp.zeros(6)

    rank_loss = sp.diag(1, 0)
    rank_loss_collapses_direction = rank_loss.rank() == 1 and rank_loss.det() == 0

    # Two source samples duplicated into four observed samples. The source remains recoverable,
    # but exact repeated-image constraints are imposed by the map.
    duplicate = sp.Matrix([[1, 0], [0, 1], [1, 0], [0, 1]])
    duplication_creates_equal_pairs = (
        duplicate.rank() == 2
        and duplicate[0, :] == duplicate[2, :]
        and duplicate[1, :] == duplicate[3, :]
    )

    return {
        "pointwise_inverse_exact": invertible_reconstruction,
        "canonical_common_area_is_ell_squared": canonical_determinant,
        "direction_tangent_compresses_by_q_squared": tangent_compression,
        "finite_global_regular_map_full_rank": global_regular_full_rank,
        "finite_global_regular_inverse_exact": global_inverse_exact,
        "rank_loss_collapses_one_direction": rank_loss_collapses_direction,
        "noninjective_duplication_imposes_repeated_images": duplication_creates_equal_pairs,
        "global_sphere_note": (
            "a smooth everywhere-local-diffeomorphism S2-to-S2 is a covering; connected S2 is "
            "simply connected, so nontrivial self-multiplicity requires critical/branch points"
        ),
    }


def build_g68_atlas() -> dict[str, float | int]:
    source = table(G72_ATLAS)
    output: list[dict[str, str]] = []
    max_condition = 0.0
    max_chi = 0.0
    max_anisotropy_percent = 0.0
    for row in source:
        chi = float(row["shear_magnitude"])
        condition = math.exp(2.0 * chi)
        anisotropy_percent = 100.0 * (condition - 1.0)
        max_condition = max(max_condition, condition)
        max_chi = max(max_chi, chi)
        max_anisotropy_percent = max(max_anisotropy_percent, anisotropy_percent)
        probabilities = {angle: alignment_fraction(chi, angle) for angle in ANGLES_DEG}
        output.append(
            {
                "profile_id": row["profile_id"],
                "family": row["family"],
                "status": row["status"],
                "length_scale_dimensionful": row["length_scale"],
                "shear_chi": f"{chi:.17g}",
                "singular_value_ratio_exp_2chi": f"{condition:.17g}",
                "anisotropy_gain_percent": f"{anisotropy_percent:.17g}",
                "fraction_within_5deg_unoriented_axis": f"{probabilities[5.0]:.17g}",
                "fraction_within_15deg_unoriented_axis": f"{probabilities[15.0]:.17g}",
                "fraction_within_30deg_unoriented_axis": f"{probabilities[30.0]:.17g}",
                "relative_polar_angle": row["relative_polar_angle"],
                "endpoint_azimuthal_carry_psi": row["endpoint_azimuthal_carry_psi"],
                "scope": "REGISTERED_G68_CONTROL_ONLY",
            }
        )
    with (HERE / "G68_SOURCE_SENSITIVITY_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    return {
        "rows": len(output),
        "max_shear_chi": max_chi,
        "max_singular_value_ratio": max_condition,
        "max_anisotropy_gain_percent": max_anisotropy_percent,
        "baseline_alignment_fraction_5deg": alignment_fraction(0.0, 5.0),
        "max_alignment_fraction_5deg": alignment_fraction(max_chi, 5.0),
        "baseline_alignment_fraction_15deg": alignment_fraction(0.0, 15.0),
        "max_alignment_fraction_15deg": alignment_fraction(max_chi, 15.0),
        "baseline_alignment_fraction_30deg": alignment_fraction(0.0, 30.0),
        "max_alignment_fraction_30deg": alignment_fraction(max_chi, 30.0),
    }


def write_regime_atlas() -> None:
    rows = [
        {
            "regime": "R1_REGULAR_SINGLE_BRANCH",
            "mathematical_map": "one-to-one sky map plus pointwise M in GL+(2)",
            "current_owner": "DERIVED_CONDITIONAL_ON_SUPPLIED_QUERY",
            "source_status": "EXACTLY_RECOVERABLE",
            "geometry_signature": "scale shear rotation and remapping",
            "missing_joint": "physical global query and source",
            "maximum_conclusion": "no universal source erasure or forced motif",
        },
        {
            "regime": "R2_REGULAR_STRONG_SHEAR",
            "mathematical_map": "invertible M with singular-value ratio tending to infinity",
            "current_owner": "MATHEMATICAL_LIMIT_NOT_SELECTED",
            "source_status": "AMPLITUDE_RETAINED_DIRECTION_COMPRESSED",
            "geometry_signature": "almost all unoriented vectors align to dominant axis",
            "missing_joint": "branch or profile reaching the limit",
            "maximum_conclusion": "conditional geometry-dominated direction only",
        },
        {
            "regime": "R3_CAUSTIC_OR_FOLD",
            "mathematical_map": "det(D)=0 or critical sky map",
            "current_owner": "OPEN_DOMAIN_BOUNDARY",
            "source_status": "NONINVERTIBLE_OR_BRANCHING",
            "geometry_signature": "rank collapse folding magnification or repeated image",
            "missing_joint": "continuation regularization branch and detector rules",
            "maximum_conclusion": "candidate kaleidoscope mechanism not derived",
        },
        {
            "regime": "R4_MULTIBRANCH",
            "mathematical_map": "branch-labelled response family",
            "current_owner": "CONDITIONAL_SET_VALUED_GEOMETRY",
            "source_status": "ONE_RESPONSE_PER_BRANCH",
            "geometry_signature": "path-dependent repeated or rotated images possible",
            "missing_joint": "selection sum averaging phase population and weights",
            "maximum_conclusion": "do not collapse branch set into observable",
        },
        {
            "regime": "R5_G68_CONTROL_TILE",
            "mathematical_map": "21 regular stationary equatorial endpoint maps",
            "current_owner": "OBSERVED_BOUNDED_CONTROL",
            "source_status": "INVERTIBLE_AND_WEAKLY_ANISOTROPIC",
            "geometry_signature": "nonzero area and shear no resolved polar rotation",
            "missing_joint": "full sky endpoint profile scale and source",
            "maximum_conclusion": "not a strong kaleidoscope on this tile",
        },
    ]
    with (HERE / "RESPONSE_REGIME_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_count = verify_sources()
    exact = exact_checks()
    assert all(value is True for value in exact.values() if isinstance(value, bool))
    g68 = build_g68_atlas()
    assert g68["rows"] == 21
    write_regime_atlas()
    payload = {
        "schema": "udt-cmb-g73-source-sensitivity-v1",
        "landing": LANDING,
        "source_manifest_rows": source_count,
        "exact_checks": exact,
        "g68_control": g68,
        "status": {
            "regular_single_branch_source_recovery": "DERIVED_EXACT",
            "strong_shear_directional_alignment": "DERIVED_ASYMPTOTIC_CONDITIONAL",
            "rank_loss_or_fold_kaleidoscope": "POTENTIAL_MECHANISM_OPEN_NO_BRANCH_OWNER",
            "multibranch_observable_combination": "OPEN_NO_OWNER",
            "g68_kaleidoscope_strength": "OBSERVED_WEAK_ON_BOUNDED_TILE",
            "physical_cmb_source_and_observable": "OPEN_NO_OWNER",
        },
        "maximum_conclusion": (
            "regular one-to-one G72 response preserves arbitrary source information exactly; "
            "geometry can dominate direction in a strong-shear limit, while robust repeated-image "
            "kaleidoscope behavior requires a global non-bijective or singular branch structure, "
            "or a restricted source family, none of which is selected by the current controls"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
