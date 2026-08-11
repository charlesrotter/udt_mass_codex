#!/usr/bin/env python3
"""Artifact-consistency verifier for the complete CMB observation-query map.

This implementation does not import the deterministic renderer. It verifies the
frozen source hashes and the saved source/family/layer/channel artifacts against
their registered universes. It does not independently derive semantic ownership
from the natural-language source texts; that role belongs to the sealed external
semantic review preserved with this package.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

EXPECTED_SOURCES = {
    "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/EXACT_DERIVATION.md": "b41d49db51888523b99c14a83c632fd5c45ea7592eb0e4fbc4ab1016be69e93f",
    "udt_common_query_pair_immersion_reconstruction_2026-08-11/EXACT_DERIVATION.md": "bc96d6889075ede38271a4d63d3c021f7df0952b27f7e831c0d7161b97f737da",
    "udt_sne_native_observer_query_replay_2026-08-11/AUDIT_REPORT.md": "30a1cd9887e04cffc86b3646083c7fe890ca030f3430bf86365cfbe4a87a5c0b",
    "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/AUDIT_REPORT.md": "32fadafc5b336a35aae10bc7c24e98c27bbd64e03d43d42bbd9f1a6a8f3d932c",
    "udt_roadA_RA1_muon_modes_2026-08-08/DERIVATION_NOTES.md": "5bc678191a489bf2a7f34416eafb32eed5671a560737630b124b6e88ab724235",
    "udt_roadA_RA2_projection_2026-08-08/PHASE1_NOTES.md": "9346f0823a8b2f7855ce6d180c50b7f1a21e2ac56656650def3fec4b7eb2a733",
    "udt_roadA_RA2_projection_2026-08-08/PHASE2_COMPARISON.md": "cc493cc32eeb161be501a1575433028f8aa4dde3909f28894b839751e576dfd7",
    "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md": "4d6017b2639be41acdcdaa65ee97c7ce5fbf35ac91e7aa0de4f3eac5dd37927e",
    "udt_fd1_corrected_full_spectral_atlas_2026-08-09/ATTRIBUTED_READOUT_PROTOCOL.md": "f090e86dd74473570329f47c36831efcd6ff64da1189ad2dc54720f2c66ce803",
    "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md": "e8baaa58bf006beed6b5c708fc2e475485c25660c1b3b35977aef213c03082ba",
    "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md": "553799701372ebcfdbdd006892724778f01a66d9425280cd71afd238e6cfdfae",
    "udt_cmb_complete_angular_family_atlas_map_2026-08-09/FAMILY_UNIVERSE.tsv": "b14fe464d3256fb7fbe3f07ca6d0934d29d31f5bc58f2edd1d91baf90d6361e9",
    "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md": "a81155f315c174b17968f10060148bacb03ccbbca3d6b7badfc5093f0074fc97",
    "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/EXACT_DERIVATION.md": "39ad31b1cc8c7a18851ec4190a0e22d2f3b192162ac89f54af50fe0fce4589eb",
    "udt_freedata_inventory_MAP_2026-08-09.md": "9050e0f5a803dae0a456c2d6fc38dd87d9016dff919e77036ea2800f6c3a097c",
    "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md": "664ac79ebe0e64eb4854ca067913084d7a6396e21a768a5fb9e92fdf8151d982",
}


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(131072)
            if not block:
                return h.hexdigest()
            h.update(block)


def table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate(
    sources: list[dict[str, str]],
    families: list[dict[str, str]],
    layers: list[dict[str, str]],
    observables: list[dict[str, str]],
    result: dict,
) -> dict[str, bool]:
    source_map = {row["path"]: row["sha256"] for row in sources}
    checks = {
        "source_manifest_exact": source_map == EXPECTED_SOURCES and len(source_map) == len(sources) == 16,
        "source_files_exact": all(hash_file(ROOT / path) == digest for path, digest in EXPECTED_SOURCES.items()),
        "family_universe_exact": [row["family_id"] for row in families] == [f"F{i:02d}" for i in range(18)],
        "family_universe_unique": len({row["family_id"] for row in families}) == 18,
        "no_native_or_selected_promotions": all(
            row["physical_CMB_pair_query"] == "OPEN_NOT_SUPPLIED"
            and row["family_rank"] == "UNRANKED"
            for row in families
        ),
        "no_power_or_polarization_claim": all(
            row["TT_power_prediction"] == "OPEN" and row["polarization_prediction"] == "OPEN"
            for row in families
        ),
        "only_F00_has_historical_position_readout": [
            row["family_id"] for row in families if row["TT_position_readout"] != "NOT_PERFORMED"
        ] == ["F00"],
        "degenerate_control_retained": next(row for row in families if row["family_id"] == "F15")[
            "ambient_regular_geometry"
        ] == "NOT_REGULAR_DEGENERATE",
        "F00_projection_caveat": next(
            row for row in observables if row["observable"] == "FD1_RA2_AFFINE_TT_POSITION_DIAGNOSTIC"
        )["screen_Jacobi"] == "REPLACED_BY_TWO_FITTED_AFFINE_FREEDOMS",
        "physical_TT_requires_population": next(
            row for row in observables if row["observable"] == "PHYSICAL_TT_PEAK_POSITIONS"
        )["source_population"] == "REQUIRED_TO_DECIDE_WHICH_MODES_FORM_PEAKS",
        "scalar_TT_does_not_read_pure_normal_rotation": next(
            row for row in observables if row["observable"] == "PHYSICAL_TT_PEAK_POSITIONS"
        )["normal_transport"] == "PURE_SO2_ROTATION_NOT_DIRECTLY_READ_BY_SCALAR_TT",
        "polarization_requires_orientation_carry": next(
            row for row in observables if row["observable"] == "PHYSICAL_TE_EE_BB_POLARIZATION"
        )["normal_transport"] == "REQUIRED_OR_EQUIVALENT_SCREEN_CONNECTION",
        "P1_role_guard": next(
            row for row in layers if row["object"] == "P1_SNE_COMPATIBILITY_ANCHOR"
        )["what_is_banked"] == "must_not_be_copied_into_centered_CMB_lapse",
        "Xmax_guard_only": next(
            row for row in layers if row["object"] == "XMAX_ASYMPTOTIC_GUARD"
        )["what_is_banked"] == "not_local_wall_not_selector_not_value",
        "pair_speed_type_guard": next(
            row for row in layers if row["object"] == "PAIR_CONE_READOUT"
        )["what_is_banked"] == "conditional_pair_readout_not_local_speed",
        "query_layers_exact": [row["layer_id"] for row in layers] == [f"Q{i:02d}" for i in range(14)],
        "observables_exact": len(observables) == 4 and len({row["observable"] for row in observables}) == 4,
        "summary_counts_exact": result["source_count"] == 16
        and result["family_count"] == 18
        and result["query_layer_count"] == 14
        and result["observable_class_count"] == 4,
        "summary_no_selection": result["complete_physical_CMB_query_count"] == 0
        and result["families_ranked"] == 0
        and result["families_with_TT_power_prediction"] == 0
        and result["families_with_polarization_prediction"] == 0,
        "known_bank_counts": result["c0_root_count_banked"] == 10080
        and result["c1_matrix_element_count_banked"] == 15420,
        "status_exact": result["status"]
        == "COMPLETE_CMB_QUERY_ARCHITECTURE_MAPPED__NO_COMPLETE_PHYSICAL_REALIZATION_OWNED",
    }
    return checks


def load_current() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict]:
    return (
        table(HERE / "SOURCE_MANIFEST.tsv"),
        table(HERE / "FAMILY_REALIZATION_ATLAS.tsv"),
        table(HERE / "QUERY_LAYER_ATLAS.tsv"),
        table(HERE / "OBSERVABLE_CHANNEL_REQUIREMENTS.tsv"),
        json.loads((HERE / "DERIVATION_RESULT.json").read_text()),
    )


def main() -> None:
    checks = validate(*load_current())
    payload = {
        "verdict": "ARTIFACTS_CONSISTENT" if all(checks.values()) else "FAILED",
        "implementation": "standard_library_artifact_consistency_no_renderer_import",
        "semantic_independence": False,
        "semantic_review": "EXTERNAL_REVIEW_RAW.md",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
    }
    (HERE / "ARTIFACT_CONSISTENCY.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
