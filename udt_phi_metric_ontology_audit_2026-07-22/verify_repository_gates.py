#!/usr/bin/env python3
"""Repository gates for the phi–metric ontology audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "e06fb57b3e13a398289ec687a89cfd46b3728635"
PACKAGE = HERE.name
DIRTY = Path("/home/udt-admin/udt_mass_codex")
LOCAL_SELECTOR = "udt_local_selector_holonomy_closure_2026-07-22"
LOCAL_SELECTOR_MANIFEST = "948f96ddffae51ed4811cc96dd6dd9abdc81bdabc1b2f9e27bec70b14afbee71"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def prior_manifest_records() -> list[dict[str, str]]:
    latest = json.loads((ROOT / LOCAL_SELECTOR / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    records = [
        {"package": row["package"], "expected": row["manifest_sha256"]}
        for row in latest["prior_scientific_packages"]["packages"]
    ]
    records.append({"package": LOCAL_SELECTOR, "expected": LOCAL_SELECTOR_MANIFEST})
    return records


def replay_prior(generic, corrupt: bool = False) -> dict[str, object]:
    details = []
    entries = 0
    records = prior_manifest_records()
    for index, record in enumerate(records):
        package = record["package"]
        expected = record["expected"]
        candidates = [ROOT / package / "SHA256SUMS.txt", ROOT / package / "MANIFEST.sha256"]
        matching = [path for path in candidates if path.exists() and digest(path) == expected]
        if corrupt and index == 0:
            matching = []
        if len(matching) != 1:
            raise generic.GateError("PRIOR", package + ":manifest")
        manifest = matching[0]
        replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
        if replay.returncode or "FAILED" in str(replay.stdout):
            raise generic.GateError("PRIOR", package + ":replay")
        count = len([line for line in manifest.read_text(encoding="utf-8").splitlines() if line])
        entries += count
        details.append(
            {
                "package": package,
                "manifest": manifest.name,
                "manifest_sha256": expected,
                "entries": count,
                "result": "PASS",
            }
        )
    if len(details) != 74 or entries != 2077:
        raise generic.GateError("PRIOR", f"totals:{len(details)}:{entries}")
    return {"packages": details, "entries": entries, "result": "PASS"}


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json", "REPOSITORY_GATES_TRANSCRIPT.txt"}
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in excluded)
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "phi_ontology_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = validate_package(generic)
    scientific = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if scientific["status"] != "PASS" or scientific["catch_proofs"] != {"passed": 17, "total": 17}:
        raise AssertionError("scientific verification contract")

    catches = {
        "scope_rejects_live_edit": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen_corruption_rejected": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior_corruption_rejected": generic.expect("PRIOR", lambda: replay_prior(generic, True)),
        "current_path_loss_rejected": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier_loss_rejected": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package_corruption_rejected": generic.expect("PACKAGE", lambda: validate_package(generic, True)),
    }

    result = {
        "schema": "udt-phi-metric-ontology-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "scientific_verification": scientific,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"physics_solves": 0, "gpu_runs": 0, "cpu_source_audits": 1},
        "authority_boundary": "ONTOLOGY_AUDIT_ONLY__NO_ACTION_REALIZATION_DYNAMICS_OR_SCALE",
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
