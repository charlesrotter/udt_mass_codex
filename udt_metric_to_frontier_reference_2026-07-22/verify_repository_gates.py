#!/usr/bin/env python3
"""Repository gates for the metric-to-frontier reference freeze."""

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
BASE = "316114a67b52db547025888df132f89eb92bb6f1"
PACKAGE = HERE.name
ATLAS = ROOT / "udt_global_metric_assembly_atlas_2026-07-22"
ATLAS_MANIFEST = "d4c7e7e16e38496343bbfbc8ef0867de45657ea2e25a724b44b653ff1b276374"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
NAVIGATION = {
    "AGENTS.md",
    "HANDOFF.md",
    "INDEX.md",
    "LIVE.md",
    "README.md",
    "research/README.md",
}


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


def validate_scope(generic, injected: str | None = None) -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    allowed = {path for path in changed if path.startswith(PACKAGE + "/")} | NAVIGATION
    invalid = sorted(path for path in changed if path and path not in allowed)
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    return sorted(path for path in changed if path)


def validate_freeze(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "REFERENCE_FREEZE_MANIFEST.tsv"
    entries = rows(manifest)
    if len(entries) != 13 or len({row["path"] for row in entries}) != 13:
        raise generic.GateError("REFERENCE_FREEZE", "coverage")
    for number, row in enumerate(entries):
        path = HERE / row["path"]
        observed = digest(path)
        if corrupt and number == 0:
            observed = "0" * 64
        if not path.is_file() or observed != row["sha256"] or path.stat().st_size != int(row["size_bytes"]):
            raise generic.GateError("REFERENCE_FREEZE", row["path"])
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def validate_internal(generic, corrupt: bool = False) -> dict[str, object]:
    result = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt:
        result["claim_rows"] -= 1
    required = (
        result["status"] == "PASS_INTERNAL_REFERENCE_CONSISTENCY"
        and result["source_rows"] == 16
        and result["claim_rows"] == 29
        and result["open_join_rows"] == 13
        and result["catch_proofs"] == 10
        and result["external_reviews"] == "PENDING_AFTER_IMMUTABLE_REFERENCE_COMMIT"
        and result["scientific_changes"] == 0
    )
    if not required:
        raise generic.GateError("INTERNAL", "result contract")
    return result


def validate_navigation(generic, corrupt: str | None = None) -> dict[str, int]:
    current = rows(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    if corrupt == "current":
        current_paths.pop()
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
    for source in sorted(HERE.glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            links.append(source.parent.joinpath(target).resolve())
    if corrupt == "link":
        links.append(ROOT / "NONEXISTENT_REFERENCE_TARGET")
    if not all(path.exists() for path in links):
        raise generic.GateError("NAVIGATION", "markdown-link")
    return {
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "frontier_targets": len(targets),
        "package_links": len(links),
    }


def prior_packages() -> dict[str, str]:
    record = json.loads((ATLAS / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {
        row["package"]: row["manifest_sha256"]
        for row in record["prior_scientific_packages"]["packages"]
    }
    prior[ATLAS.name] = ATLAS_MANIFEST
    return prior


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "metric_frontier_generic",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = validate_scope(generic)
    internal = validate_internal(generic)
    freeze = validate_freeze(generic)
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 71 or replay["entries"] != 1994:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    catches = {
        "scope": generic.expect("SCOPE", lambda: validate_scope(generic, "CANON.md")),
        "internal": generic.expect("INTERNAL", lambda: validate_internal(generic, True)),
        "reference_freeze": generic.expect("REFERENCE_FREEZE", lambda: validate_freeze(generic, True)),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "frontier")),
        "link": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "link")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
    }
    output = {
        "schema": "udt-metric-to-frontier-reference-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "internal_verifier": internal,
        "reference_freeze": freeze,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": {
            "canon_changed": False,
            "new_derivation_performed": False,
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
    print(f"reference_freeze={freeze['manifest_sha256']} entries={freeze['entries']}")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")


if __name__ == "__main__":
    main()
