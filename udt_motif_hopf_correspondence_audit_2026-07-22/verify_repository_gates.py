#!/usr/bin/env python3
"""Repository gates for the corrected motif-to-Hopf correspondence audit."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "50756174718908e1aa5fd0a721f5ae6c527c4c8e"
PACKAGE = "udt_motif_hopf_correspondence_audit_2026-07-22"
PARENT = ROOT / "udt_instrument_motif_atlas_2026-07-21"
PARENT_MANIFEST = "97dac2c32317deb603a054cffd3d2162f537d8bc7806d2276fa7e8544dd22ed5"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
MAXIMUM = (
    "OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS"
    "+EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS"
)


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def scientific_results() -> dict[str, object]:
    atlas = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")
    )
    correction = json.loads(
        (HERE / "REVIEW_CORRECTION_RESULT.json").read_text(encoding="utf-8")
    )
    package = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    summary = json.loads((HERE / "SCIENTIFIC_SUMMARY.json").read_text(encoding="utf-8"))
    required = (
        atlas["coherent_identities"] == 3072
        and atlas["metric_phi_twojets"] == 52224
        and atlas["path_family_rows"] == 1618944
        and atlas["path_summary_rows"] == 95232
        and atlas["distribution_rows"] == 143487
        and atlas["global_hopf_eligible_local_identities"] == 0
        and independent["status"] == "PASS_WITH_REGISTERED_SCOPE"
        and independent["classification_mismatches"] == 0
        and independent["adverse_family_paths"] == 1312
        and correction["status"] == "PASS_WITH_REGISTERED_SCOPE"
        and correction["maximum_conclusion"] == MAXIMUM
        and correction["covariance"]["all_family_node_comparisons"] == 67456
        and correction["covariance"]["nonuncertain_classification_discordances"] == 0
        and correction["covariance"]["matched_edge_transport_discordances"] == 0
        and correction["exercised_mutation_catches"] == 29
        and correction["covariance"]["point_status_census"] == {
            "BOTH_CLASSIFIED": 67396,
            "ONE_SIDED_UNCERTAIN": 33,
            "BOTH_UNCERTAIN": 27,
        }
        and correction["covariance"]["skipped_edge_reason_census"] == {
            "ORIGINAL_EDGE_UNMATCHED+TRANSFORMED_EDGE_UNMATCHED": 50,
        }
        and correction["covariance"]["coordinate_map_interpretation"]
            == "ZERO_CONSTANT_CUBIC_GLOBAL_POLYNOMIAL_FROM_REGISTERED_JETS"
        and correction["covariance"]["possible_edge_transport_comparisons"] == 63488
        and correction["covariance"]["matched_edge_transport_comparisons"] == 63438
        and correction["covariance"]["skipped_edge_transport_comparisons"] == 50
        and correction["covariance"]["uncertainty_bearing_point_comparisons"] == 60
        and correction["frobenius_certification_scope"] == "REGISTERED_CHART_ONLY"
        and correction["overall_correspondence_status"] == "LEAD"
        and package["status"] == "PASS_WITH_REGISTERED_SCOPE"
        and package["maximum_conclusion"] == MAXIMUM
        and summary["maximum_conclusion"] == MAXIMUM
        and summary["overall_correspondence_status"] == "LEAD"
    )
    if not required:
        raise AssertionError("scientific result contract")
    return {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "coherent_identities": atlas["coherent_identities"],
        "twojets": atlas["metric_phi_twojets"],
        "family_rows": atlas["path_family_rows"],
        "distribution_rows": atlas["distribution_rows"],
        "blind_path_comparisons": independent["blind_path_family_comparisons"],
        "adverse_path_comparisons": independent["adverse_path_family_comparisons"],
        "covariance_comparisons": correction["covariance"]["all_family_node_comparisons"],
        "edge_transport_comparisons": correction["covariance"]["matched_edge_transport_comparisons"],
        "edge_transport_skipped": correction["covariance"]["skipped_edge_transport_comparisons"],
        "uncertainty_bearing_covariance_points": correction["covariance"]["uncertainty_bearing_point_comparisons"],
        "correction_mutation_catches": correction["exercised_mutation_catches"],
        "frobenius_certification_scope": correction["frobenius_certification_scope"],
        "overall_correspondence_status": "LEAD",
        "maximum_conclusion": MAXIMUM,
        "hashes": {
            name: digest(HERE / name)
            for name in (
                "ATLAS_RESULT.json", "INDEPENDENT_VERIFICATION_RESULT.json",
                "REVIEW_CORRECTION_RESULT.json", "VERIFICATION_RESULT.json",
                "SCIENTIFIC_SUMMARY.json", "TORIC_CONTROL_RESULT.json",
                "PATH_FAMILY_ATLAS.tsv.gz", "DISTRIBUTION_ATLAS.tsv.gz",
            )
        },
    }


def source_immutability() -> dict[str, object]:
    observed = {}
    for row in rows(HERE / "SOURCE_LINEAGE.tsv"):
        path = ROOT / row["path"]
        if digest(path) != row["sha256"]:
            raise AssertionError(f"source hash {row['path']}")
        observed[row["path"]] = row["sha256"]
    if len(observed) != 10:
        raise AssertionError("source count")
    return {"status": "PASS", "count": len(observed), "sources": observed}


def prior_packages() -> dict[str, str]:
    record = json.loads((PARENT / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {
        row["package"]: row["manifest_sha256"]
        for row in record["prior_scientific_packages"]["packages"]
    }
    prior[PARENT.name] = PARENT_MANIFEST
    return prior


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "motif_hopf_generic",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    scientific = scientific_results()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 69 or replay["entries"] != 1864:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect(
            "PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)
        ),
        "current": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")
        ),
        "frontier": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")
        ),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect(
            "PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)
        ),
    }
    output = {
        "schema": "udt-motif-hopf-correspondence-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "scientific_verifier": scientific,
        "source_immutability": sources,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "action_or_equations_selected": False,
            "physical_motif_selected": False,
            "continuous_transport_or_dynamics_claimed": False,
            "boundary_topology_or_scale_selected": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("repository_gates=PASS")
    print(
        f"scientific={scientific['coherent_identities']} identities/"
        f"{scientific['family_rows']} family rows/{scientific['distribution_rows']} distributions"
    )
    print(
        f"covariance={scientific['covariance_comparisons']} edge_transport="
        f"{scientific['edge_transport_comparisons']}"
    )
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(
        f"tests={tests['passed']} passed/{tests['failed']} known failed/"
        f"{tests['xfailed']} xfailed"
    )
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()
