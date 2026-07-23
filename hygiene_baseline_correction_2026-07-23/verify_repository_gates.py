#!/usr/bin/env python3
"""Repository gates for the hygiene-baseline correction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "1b455fbb9326c7813bedaf1d220c29f7901ab512"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
BANK_PACKAGE = "udt_bank_simplex_interior_atlas_2026-07-23"
BANK_MANIFEST = "75ac459c9eb978c88272b7115da2a723f4d7a009b4f72f7d7972dc525437a1f1"
ALLOWED_CURRENT = {
    "CLAUDE.md",
    "LIVE.md",
    "STRUCTURE_HYGIENE.md",
    "tests/test_hygiene_header.py",
}
EXPECTED_CURRENT_HASHES = {
    "CLAUDE.md": "b199c327a2892317fb691ce82992ac02852ca4213f14ba194e52c745e6a12c70",
    "LIVE.md": "5212f12687732ccbf28eb3079e6aa5e6d980764eaf068e17167440ddde3e73c2",
    "STRUCTURE_HYGIENE.md": "b5eec1a27a3cc73eae911942e31feb522260484a5f0c477383cee2f86e0d1f5d",
    "tests/test_hygiene_header.py": "755987b47bf5818ab0474b0fab77e0a259c78b5f3c342c1b8374684f910b57a8",
}


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def validate_scope(generic, injected: str | None = None) -> list[str]:
    changed = set(
        str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines()
    )
    changed.update(
        str(
            generic.git(
                ROOT, "ls-files", "--others", "--exclude-standard"
            )
        ).splitlines()
    )
    if injected:
        changed.add(injected)
    invalid = sorted(
        path
        for path in changed
        if path
        and path not in ALLOWED_CURRENT
        and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    return sorted(path for path in changed if path)


def validate_current_hashes(generic, corrupt: bool = False) -> dict[str, str]:
    observed = {
        path: digest(ROOT / path)
        for path in sorted(EXPECTED_CURRENT_HASHES)
    }
    if corrupt:
        observed["tests/test_hygiene_header.py"] = "0" * 64
    if observed != EXPECTED_CURRENT_HASHES:
        raise generic.GateError("CURRENT_HASH", "current-control-mismatch")
    return observed


def validate_bank_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = ROOT / BANK_PACKAGE / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != BANK_MANIFEST:
        raise generic.GateError("BANK_PACKAGE", "manifest-hash")
    replay = generic.run(
        manifest.parent, ["sha256sum", "--check", manifest.name]
    )
    entries = [line for line in manifest.read_text().splitlines() if line]
    if replay.returncode or "FAILED" in replay.stdout or len(entries) != 41:
        raise generic.GateError("BANK_PACKAGE", "manifest-replay")
    return {
        "package": BANK_PACKAGE,
        "manifest_sha256": observed,
        "entries": len(entries),
        "result": "PASS",
    }


def validate_tests(generic) -> dict[str, object]:
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = ""
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = generic.run(
        ROOT, ["python3", "-m", "pytest", "tests/"], env=env
    )
    summary = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode != 0
        or summary is None
        or tuple(map(int, summary.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise generic.GateError("TESTS", f"return:{completed.returncode}")
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/",
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "result": "PASS",
    }


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in replay.stdout:
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text().splitlines()
        if line
    ]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name not in excluded
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "hygiene_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    bank = load(
        ROOT / BANK_PACKAGE / "verify_repository_gates.py",
        "hygiene_bank_gate_chain",
    )
    scope = validate_scope(generic)
    current_hashes = validate_current_hashes(generic)
    frozen = generic.validate_frozen(ROOT)
    prior = bank.replay_prior(generic)
    bank_package = validate_bank_package(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = validate_tests(generic)
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text()
    )
    saved_tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    if (
        independent["result"] != "PASS"
        or independent["covered_documents"] != 70
        or independent["registered_backlog_documents"] != 37
        or independent["registered_omissions"] != 88
        or independent["mutation_catch_proofs"] != 4
        or saved_tests["result"] != "PASS"
        or (saved_tests["passed"], saved_tests["failed"], saved_tests["xfailed"])
        != (70, 0, 1)
    ):
        raise AssertionError("hygiene correction contract")
    package = validate_package(generic)
    catches = {
        "scope_rejects_unrelated_edit": generic.expect(
            "SCOPE", lambda: validate_scope(generic, "CANON.md")
        ),
        "current_control_corruption_rejected": generic.expect(
            "CURRENT_HASH", lambda: validate_current_hashes(generic, True)
        ),
        "frozen_corruption_rejected": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, True)
        ),
        "prior_corruption_rejected": generic.expect(
            "PRIOR", lambda: bank.replay_prior(generic, True)
        ),
        "bank_package_corruption_rejected": generic.expect(
            "BANK_PACKAGE", lambda: validate_bank_package(generic, True)
        ),
        "current_path_loss_rejected": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "current"),
        ),
        "frontier_loss_rejected": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "frontier"),
        ),
        "dirty_metadata_loss_rejected": generic.expect(
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)
        ),
        "package_corruption_rejected": generic.expect(
            "PACKAGE", lambda: validate_package(generic, True)
        ),
    }
    result = {
        "schema": "udt-hygiene-baseline-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "current_control_hashes": current_hashes,
        "independent_verification": independent,
        "saved_full_tests": saved_tests,
        "rerun_full_tests": tests,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "bank_simplex_package": bank_package,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "package_manifest": package,
        "catch_proofs": catches,
        "authority_boundary": (
            "TEST_BASELINE_AND_EXACT_LEGACY_BACKLOG_ONLY__"
            "NO_SCIENTIFIC_ARTIFACT_OR_VERDICT_CHANGE"
        ),
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
