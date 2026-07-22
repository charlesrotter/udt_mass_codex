#!/usr/bin/env python3
"""Repository gates for the century-scale mathematics survey."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import unquote
import re


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "0f4d75b47d82d13fdfac50f56439fc580fc67645"
PACKAGE = HERE.name
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prior_packages() -> dict[str, str]:
    record = json.loads(
        (ROOT / "udt_metric_to_frontier_reference_2026-07-22/FINAL_REPOSITORY_GATES.json").read_text(encoding="utf-8")
    )
    packages = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    packages["udt_metric_to_frontier_reference_2026-07-22"] = record["package_manifest"]["manifest_sha256"]
    return packages


def validate_manifest(generic, corrupt: bool = False) -> dict[str, object]:
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


def validate_navigation(generic, corrupt: str | None = None) -> dict[str, int]:
    generic.PACKAGE = PACKAGE
    navigation = generic.validate_navigation(ROOT, corrupt=corrupt)
    # Also accept the survey's external Markdown citations without fetching them here.
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    external = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if target.startswith(("http://", "https://", "mailto:", "#")):
                external += 1
    navigation["external_citations"] = external
    return navigation


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "survey_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    packages = prior_packages()
    prior = generic.replay_packages(ROOT, packages, "PRIOR")
    assert len(packages) == 72 and prior["entries"] == 2029
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    package = validate_manifest(generic)
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    assert verification["status"] == "PASS" and verification["catch_pass_count"] == 15

    catches = {
        "scope_rejects_live_edit": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen_corruption_rejected": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior_corruption_rejected": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, packages, "PRIOR", True)),
        "current_path_loss_rejected": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "current")),
        "frontier_loss_rejected": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "frontier")),
        "dirty_metadata_loss_rejected": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package_corruption_rejected": generic.expect("PACKAGE", lambda: validate_manifest(generic, True)),
    }

    result = {
        "schema": "udt-century-adjacent-mathematics-survey-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "survey_verification": verification,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"physics_solves": 0, "gpu_runs": 0},
        "authority_boundary": "SURVEY_ONLY__NO_EXTERNAL_STRUCTURE_ADOPTED__NO_DERIVATION_OR_GPU_AUTHORIZED",
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
