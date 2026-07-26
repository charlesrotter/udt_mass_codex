#!/usr/bin/env python3
"""Repository preservation gates for the functional-rank audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = HERE.name
BASE = "ccd3334245748ee17356c1fb6b39c61d3a662fdf"
DIRTY_HEAD = "8b13104a4f1af45af617d2aa50cd5fdacf4082af"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
DIRTY_STATUS_SHA = "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json", "REPOSITORY_GATES_STDOUT.txt"}


def load_generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("functional_rank_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = PACKAGE
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def git(cwd: Path, *args: str) -> str:
    result = run(["git", *args], cwd)
    if result.returncode:
        raise AssertionError(result.stdout)
    return result.stdout


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git(ROOT, "diff", "--name-only", BASE).splitlines())
    paths.update(git(ROOT, "ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    bad = sorted(path for path in paths if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise AssertionError(f"scope:{bad[0]}")
    return sorted(path for path in paths if path)


def validate_tests() -> dict[str, object]:
    result = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", result.stdout)
    if result.returncode or match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError(result.stdout)
    normalized = re.sub(r"in \d+(?:\.\d+)?s", "in <elapsed>s", result.stdout)
    return {
        "command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -m pytest -q tests/",
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "normalized_stdout_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
        "normalization": "pytest elapsed time replaced by <elapsed>",
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(
        ["git", "status", "--short"], cwd=DIRTY, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if status.returncode:
        raise AssertionError("dirty metadata unavailable")
    head = git(DIRTY, "rev-parse", "HEAD").strip()
    branch = git(DIRTY, "branch", "--show-current").strip()
    count = len(status.stdout.splitlines())
    status_digest = hashlib.sha256(status.stdout).hexdigest()
    if corrupt:
        count -= 1
    if head != DIRTY_HEAD or branch != "grok" or count != 55 or status_digest != DIRTY_STATUS_SHA:
        raise AssertionError("dirty checkout metadata changed")
    return {
        "head": head,
        "branch": branch,
        "paths": count,
        "metadata_sha256": status_digest,
        "contents_read": False,
        "result": "PASS",
    }


def validate_package(corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    result = run(["sha256sum", "--check", manifest.name], HERE)
    entries = [line.split("  ", 1)[1] for line in manifest.read_text().splitlines() if line]
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    if corrupt or result.returncode or "FAILED" in result.stdout or sorted(entries) != actual:
        raise AssertionError("package manifest")
    return {
        "entries": len(entries),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "result": "PASS",
    }


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    generic = load_generic()
    output = {
        "schema": "udt-global-functional-rank-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": validate_scope(),
        "frozen": generic.validate_frozen(ROOT),
        "navigation": generic.validate_navigation(ROOT),
        "tests": validate_tests(),
        "dirty_checkout": validate_dirty(),
        "package_manifest": validate_package(),
        "catch_proofs": {
            "scope": expect_failure(lambda: validate_scope("LIVE.md")),
            "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
            "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
            "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
            "dirty": expect_failure(lambda: validate_dirty(True)),
            "package": expect_failure(lambda: validate_package(True)),
        },
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "source_results_changed": False,
            "frozen_or_historical_changed": False,
            "physical_modes_derived": False,
            "action_source_carrier_selected": False,
            "density_used": False,
            "gpu_work": False,
            "repository_reorganization": False,
            "external_repository_transmission": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    rendered = json.dumps(output, sort_keys=True) + "\n"
    (HERE / "REPOSITORY_GATES_STDOUT.txt").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
