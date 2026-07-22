#!/usr/bin/env python3
"""Repository gates for the bounded global metric-assembly atlas."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "9f313b5b665acdb81802f59001052cf895ff5a47"
PACKAGE = "udt_global_metric_assembly_atlas_2026-07-22"
PARENT = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
PARENT_MANIFEST = "b9dca9e1baca68b82118e1a008829196d9bb834dae69cfa5d82f0ae771902164"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
MAXIMUM = (
    "BOUNDED_REGISTERED_GLOBAL_METRIC_ASSEMBLY_ATLAS_CHARACTERIZED"
    "__GLOBAL_QUOTIENT_SELECTION_OPEN"
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


def validate_navigation(generic, corrupt: str | None = None) -> dict[str, int]:
    current = rows(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    if corrupt == "current":
        current_paths = current_paths[:-1]
    if len(current) != 1114 or len(current_paths) != 1114 or len(set(current_paths)) != 1114:
        raise generic.GateError("NAVIGATION", "current-count")
    if not all((ROOT / path).exists() for path in current_paths):
        raise generic.GateError("NAVIGATION", "current-target")

    frontier = rows(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if corrupt == "frontier":
        targets.pop()
    if len(frontier) != 306 or len(targets) != 101:
        raise generic.GateError("NAVIGATION", "frontier-count")
    if not all((ROOT / path).exists() for path in targets):
        raise generic.GateError("NAVIGATION", "frontier-target")

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links: list[Path] = []
    archival_citations = 0
    for source in sorted((ROOT / PACKAGE).glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target.startswith("/tmp/"):
                archived = Path(re.sub(r":\d+$", "", target))
                relative_parts = list(archived.parts[3:])
                if relative_parts and relative_parts[0] == "repo":
                    relative_parts = relative_parts[1:]
                if not relative_parts:
                    raise generic.GateError("NAVIGATION", "empty-archival-citation")
                links.append(ROOT.joinpath(*relative_parts).resolve())
                archival_citations += 1
            else:
                links.append(source.parent.joinpath(target).resolve())
    if corrupt == "archival":
        links.append(ROOT / "NONEXISTENT_ARCHIVAL_CITATION_TARGET")
    if not all(path.exists() for path in links):
        raise generic.GateError("NAVIGATION", "markdown-link")
    return {
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "package_links": len(links),
        "archival_tmp_citations_mapped": archival_citations,
    }


def scientific_results() -> dict[str, object]:
    atlas = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    required = (
        atlas["schema"] == "udt-global-metric-assembly-atlas-1.0"
        and atlas["frozen_path_identities"] == 95232
        and atlas["unique_frozen_path_identities"] == 95232
        and atlas["stable_path_count"] == 93920
        and atlas["transition_or_unstable_path_count"] == 1312
        and atlas["dense_transport_anchor_count"] == 83
        and atlas["dense_transport_status_census"] == {
            "DENSE_TRANSPORT_NUMERIC_MARGIN_RETAINED": 7,
            "DENSE_TRANSPORT_PASS": 76,
        }
        and atlas["midpoint_integrable_candidate_identities"] == 1536
        and atlas["midpoint_integrable_unique_analytic_identities"] == 192
        and atlas["midpoint_integrable_structural_mask_census"] == {"M8": 1536}
        and atlas["finite_cell_follow_status_census"]
        == {"SAMPLED_ALL_9_NODES_INTEGRABLE_CANDIDATE": 1536}
        and atlas["completion_class_count"] == 12
        and atlas["motif_completion_cross_rows"] == 84
        and atlas["holonomy_registry_rows"] == 20
        and atlas["monodromy_class_census"]
        == {
            "FINITE_ELLIPTIC": 3,
            "HYPERBOLIC": 1,
            "IDENTITY": 1,
            "ORIENTATION_REVERSING": 2,
            "PARABOLIC_OR_MINUS_PARABOLIC": 1,
        }
        and atlas["selector_matrix_rows"] == 84
        and atlas["selected_global_quotient_classes"] == []
        and atlas["density_bootstrap_routes"] == 5
        and atlas["stage_6_status"] == "NOT_ACTIVATED__GLOBAL_QUOTIENT_NOT_SELECTED"
        and atlas["stage_7_status"] == "NOT_ACTIVATED__NATIVE_DYNAMICS_UNDEFINED"
        and atlas["cpu_time_live_runs"] == 0
        and atlas["gpu_runs"] == 0
        and atlas["maximum_conclusion"] == MAXIMUM
        and verification["status"] == "PASS_WITH_REGISTERED_NUMERIC_MARGINS"
        and verification["path_identities"] == 95232
        and verification["candidate_paths"] == 1536
        and verification["candidate_nodes"] == 13824
        and verification["candidate_unique_analytic_identities"] == 192
        and verification["candidate_structural_masks"] == ["M8"]
        and verification["completion_classes"] == 12
        and verification["selector_rows"] == 84
        and verification["density_bootstrap_routes"] == 5
        and verification["catch_proofs"] == 20
        and verification["maximum_conclusion"] == MAXIMUM
    )
    if not required:
        raise AssertionError("scientific result contract")
    return {
        "status": verification["status"],
        "path_identities": 95232,
        "stable_paths": 93920,
        "transition_paths": 1312,
        "transport_anchors": 83,
        "transport_passes": 76,
        "transport_numeric_margins": 7,
        "finite_cell_candidate_rows": 1536,
        "finite_cell_candidate_nodes": 13824,
        "analytic_candidate_identities": 192,
        "candidate_structural_mask": "M8_PHI_FIELD_ONLY",
        "completion_classes": 12,
        "selector_rows": 84,
        "selected_quotients": 0,
        "stage_6_status": atlas["stage_6_status"],
        "stage_7_status": atlas["stage_7_status"],
        "cpu_time_live_runs": 0,
        "gpu_runs": 0,
        "maximum_conclusion": MAXIMUM,
        "hashes": {
            name: digest(HERE / name)
            for name in (
                "ATLAS_RESULT.json",
                "VERIFICATION_RESULT.json",
                "PATH_ASSEMBLY_CENSUS.tsv.gz",
                "FINITE_CELL_DISTRIBUTION_FOLLOW.tsv.gz",
                "DENSE_TRANSPORT_ATLAS.tsv",
                "DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv",
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
    if len(observed) != 8:
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


def validate_package_manifest(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "hash-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    ]
    excluded = {
        "SHA256SUMS.txt",
        "REPOSITORY_GATES.json",
        "REPOSITORY_GATES_TRANSCRIPT.txt",
    }
    actual = sorted(
        path.name for path in HERE.iterdir() if path.is_file() and path.name not in excluded
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "global_assembly_generic",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    scientific = scientific_results()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 70 or replay["entries"] != 1941:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = validate_package_manifest(generic)
    catches = {
        "scope": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect(
            "PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)
        ),
        "current": generic.expect(
            "NAVIGATION", lambda: validate_navigation(generic, "current")
        ),
        "frontier": generic.expect(
            "NAVIGATION", lambda: validate_navigation(generic, "frontier")
        ),
        "archival_link": generic.expect(
            "NAVIGATION", lambda: validate_navigation(generic, "archival")
        ),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package_manifest(generic, True)
        ),
    }
    output = {
        "schema": "udt-global-metric-assembly-repository-gates-1.0",
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
            "global_quotient_selected": False,
            "carrier_or_action_selected": False,
            "time_live_solve_performed": False,
            "physical_mass_or_density_derived": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("repository_gates=PASS")
    print(
        f"scientific={scientific['path_identities']} paths/"
        f"{scientific['transport_anchors']} transport anchors/"
        f"{scientific['finite_cell_candidate_nodes']} candidate nodes"
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
