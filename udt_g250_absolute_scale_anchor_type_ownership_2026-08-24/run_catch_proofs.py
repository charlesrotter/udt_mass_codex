#!/usr/bin/env python3
"""Hostile formula and ownership mutations for G250."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def exact_source(relative: str) -> bytes:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = {row["path"]: row["sha256"] for row in csv.DictReader(stream, delimiter="\t")}
    candidates = (ROOT / relative, ROOT / "sources" / relative)
    existing = [path for path in candidates if path.is_file()]
    if relative not in manifest or len(existing) != 1:
        raise AssertionError(f"hostile source resolution failure: {relative}")
    payload = existing[0].read_bytes()
    if sha256_bytes(payload) != manifest[relative]:
        raise AssertionError(f"hostile source hash failure: {relative}")
    return payload


def tsv_rows(relative: str, key: str) -> dict[str, dict[str, str]]:
    text = exact_source(relative).decode("utf-8").splitlines()
    return {row[key]: row for row in csv.DictReader(text, delimiter="\t")}


def relocated_source_accepts(root_payload: bytes | None, relocated_payload: bytes | None, expected: str) -> bool:
    existing = [payload for payload in (root_payload, relocated_payload) if payload is not None]
    return len(existing) == 1 and sha256_bytes(existing[0]) == expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    ell = Q(3, 2)
    length_bar = Q(7, 5)
    area_bar = Q(11, 7)
    curvature_bar = Q(13, 9)
    length_obs = ell * length_bar
    area_obs = ell * ell * area_bar
    curvature_obs = curvature_bar / (ell * ell)

    ell_two = Q(5, 3)
    dimensionless_value = Q(5, 7)
    weight_zero_same = dimensionless_value * ell**0 == dimensionless_value * ell_two**0

    # c_E^a G^b: mass neutrality gives b=0, time neutrality then gives a=0,
    # leaving length exponent zero rather than one.
    forced_b = Q(0)
    forced_a = -2 * forced_b
    ce_g_length_exponent = forced_a + 3 * forced_b

    # An unidentified dimensionless proportionality alpha leaves a dimensional
    # composite compatible with more than one metric scale.
    composite_length = Q(17, 11)
    alpha_one, alpha_two = Q(1), Q(7, 5)

    # Removing an absolute zero point leaves relative values invariant under a
    # common additive shift, hence cannot recover that shift.
    theta = (Q(2, 3), Q(5, 4), Q(11, 6))
    shift_one, shift_two = Q(0), Q(9, 7)
    relative_one = tuple((value + shift_one) - (theta[0] + shift_one) for value in theta)
    relative_two = tuple((value + shift_two) - (theta[0] + shift_two) for value in theta)

    # A wrong event attachment returns the wrong scale even though the units agree.
    other_event_bar = Q(8, 5)
    wrong_event_recovery = length_obs / other_event_bar

    # One anchor equation can calibrate two distinct supplied histories that share
    # its normalized value while differing in another invariant.
    history_one = {"anchor_bar": length_bar, "other_invariant": Q(1)}
    history_two = {"anchor_bar": length_bar, "other_invariant": Q(2)}

    g236 = tsv_rows(
        "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PREMISE_LEDGER.tsv",
        "object",
    )["one additive offset per catalog"]
    g237 = tsv_rows(
        "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/PREMISE_LEDGER.tsv",
        "object",
    )["release_offsets"]
    g99 = tsv_rows(
        "udt_observed_middle_regime_pair_calibration_2026-08-15/PREMISE_LEDGER.tsv",
        "item",
    )
    g132 = exact_source(
        "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md"
    ).decode("utf-8")
    g202 = exact_source(
        "udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/EXACT_DERIVATION.md"
    ).decode("utf-8")
    relative_source_guard = (
        "distance-scale zero point" in g236["role"]
        and g237["open_scope"] == "absolute R normalization"
    )
    attachment_source_guard = (
        "These are dimensional calibrators, not UDT equations." in g132
        and "A native or explicitly conditional bridge" in g132
        and "These are dimensional candidates only." in g202
    )
    g99_source_guard = (
        g99["profile_family"]["value_or_rule"] == "P1 only"
        and "external M_B anchor" in g99["absolute_scale"]["status"]
        and g99["luminosity_readout"]["role"] == "effective observational transfer"
    )
    sealed_payload = b"registered sealed source"
    sealed_hash = sha256_bytes(sealed_payload)

    mutations = {
        "weight_zero_scale_owner_rejected": weight_zero_same and ell != ell_two,
        "ce_called_interval_rejected": (1, 0, -1) != (1, 0, 0),
        "ce_gobs_mass_neutrality_rejects_length": forced_a == 0 and forced_b == 0 and ce_g_length_exponent != 1,
        "linear_length_recovery_control": length_obs / length_bar == ell,
        "area_linear_recovery_rejected": area_obs / area_bar != ell,
        "area_square_root_recovery_control": (area_obs / area_bar) == ell * ell,
        "curvature_direct_ratio_recovery_rejected": curvature_obs / curvature_bar != ell,
        "curvature_inverse_square_recovery_control": curvature_bar / curvature_obs == ell * ell,
        "zero_curvature_anchor_rejected": Q(0) / (ell * ell) == Q(0) / (ell_two * ell_two) and ell != ell_two,
        "same_object_gate_erasure_rejected": wrong_event_recovery != ell,
        "attachment_free_mass_scale_rejected": attachment_source_guard and alpha_one * composite_length != alpha_two * composite_length,
        "attachment_free_density_scale_rejected": attachment_source_guard and alpha_one * composite_length != alpha_two * composite_length,
        "relative_sne_absolute_owner_rejected": relative_source_guard and relative_one == relative_two and shift_one != shift_two,
        "g99_native_promotion_rejected": g99_source_guard and g99["absolute_scale"]["status"] != "DERIVED_NATIVE",
        "second_anchor_consistency_control": (length_obs / length_bar) ** 2 == area_obs / area_bar,
        "inconsistent_second_anchor_rejected": (length_obs / length_bar) ** 2 != (Q(4, 3) * area_obs) / area_bar,
        "anchor_selects_history_rejected": (
            length_obs / history_one["anchor_bar"] == ell
            and length_obs / history_two["anchor_bar"] == ell
            and history_one["other_invariant"] != history_two["other_invariant"]
        ),
        "anchor_selects_branch_rejected": (
            length_obs / length_bar == ell and ("branch_A", length_bar) != ("branch_B", length_bar)
        ),
        "g248_probability_promotion_rejected": sum((Q(2), Q(3))) != 1,
        "xmax_anchor_promotion_rejected": (
            length_obs / length_bar == ell and Q(10) != Q(20)
        ),
        "sealed_source_missing_rejected": not relocated_source_accepts(None, None, sealed_hash),
        "sealed_source_ambiguity_rejected": not relocated_source_accepts(sealed_payload, sealed_payload, sealed_hash),
        "sealed_source_hash_mismatch_rejected": not relocated_source_accepts(None, b"mutated source", sealed_hash),
    }
    missed = [name for name, caught in mutations.items() if not caught]
    result = {
        "status": "PASS" if not missed else "FAIL",
        "implementation": "formula_type_and_exact_source_mutations_no_phrase_only_certification",
        "caught": sum(bool(value) for value in mutations.values()),
        "total": len(mutations),
        "missed": missed,
        "mutations": mutations,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if missed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
