#!/usr/bin/env python3
"""Repository gates for the dual-systole global transport audit."""

from __future__ import annotations

import csv
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
BASE = "7feec2b301de9c9626aaac4b513268e7c8ec165a"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def validate_scope(generic, injected: str = "") -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(
        str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines()
    )
    if injected:
        changed.add(injected)
    invalid = sorted(
        path for path in changed if path and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    return sorted(changed)


def validate_dirty_head(generic, corrupt: bool = False) -> dict[str, str]:
    head = str(generic.git(DIRTY, "rev-parse", "HEAD")).strip()
    branch = str(generic.git(DIRTY, "branch", "--show-current")).strip()
    if corrupt:
        head = "0" * 40
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
    ):
        raise generic.GateError("DIRTY", "head-or-branch")
    return {"head": head, "branch": branch}


def validate_tests() -> dict[str, object]:
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode != 0
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError(
            f"repository test baseline changed: {completed.returncode}\n"
            f"{completed.stdout}"
        )
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 "
        "python3 -m pytest -q tests/",
        "returncode": completed.returncode,
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "result": "PASS",
    }


def validate_science(corrupt: bool = False) -> dict[str, object]:
    generated = [
        "SOURCE_VERIFICATION.tsv",
        "CONTINUOUS_WALL_ATLAS.tsv",
        "STANDARD_WALL_CONTROLS.tsv",
        "GL2Z_COVARIANCE.tsv",
        "DIAGONAL_PATH_ATLAS.tsv",
        "GLOBAL_TRANSPORT_ATLAS.tsv",
        "COMPLETION_COVERAGE.tsv",
        "RESULTS.json",
        "CATCH_PROOF_RESULTS.tsv",
        "INDEPENDENT_RESULTS.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    commands = [
        [sys.executable, "derive_dual_systole_global_transport.py"],
        [sys.executable, "verify_dual_systole_global_transport.py"],
    ]
    stdout = []
    for command in commands:
        completed = run(command, cwd=HERE)
        stdout.append(completed.stdout)
        if completed.returncode:
            raise AssertionError(f"science replay failed: {command}\n{completed.stdout}")
    for name in generated:
        if (HERE / name).read_bytes() != before[name]:
            raise AssertionError(f"science replay not byte-identical: {name}")

    production = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_RESULTS.json").read_text(encoding="utf-8")
    )
    catches = read_tsv(HERE / "CATCH_PROOF_RESULTS.tsv")
    status = read_tsv(HERE / "STATUS_LEDGER.tsv")
    premises = read_tsv(HERE / "PREMISE_AUDIT.tsv")
    if corrupt:
        production["phase_section"] = "DERIVED"
    if (
        production["wall_theorem"]["independent_co_shortest_pair"] != "UNIMODULAR"
        or production["wall_theorem"]["maximum_unoriented_tie_multiplicity"] != 3
        or production["diagonal_path_ruling"]
        != "RECIPROCAL_CHARACTER_SWAP_REQUIRES_TIE_CROSSING"
        or production["completion_count"] != 12
        or production["physical_ruling"]
        != "CANONICAL_GEOMETRIC_CHARACTER_NOT_PHYSICALLY_SELECTED"
        or production["phase_section"] != "OPEN"
        or production["matter_solve_launched"]
        or production["gpu_used"]
        or independent["overall"] != "PASS"
        or independent["catch_proof_pass_count"] != 16
        or len(catches) != 16
        or len(status) != 18
        or len(premises) != 23
    ):
        raise AssertionError("science/status/authority contract")
    return {
        "production_stdout_sha256": hashlib.sha256(
            stdout[0].encode()
        ).hexdigest(),
        "independent_stdout_sha256": hashlib.sha256(
            stdout[1].encode()
        ).hexdigest(),
        "deterministic_replay": "BYTE_IDENTICAL",
        "continuous_objects": production["continuous_object_count"],
        "wall_controls": production["wall_control_count"],
        "GL2Z_controls": production["GL2Z_control_count"],
        "completions": production["completion_count"],
        "maximum_tie": production["wall_theorem"][
            "maximum_unoriented_tie_multiplicity"
        ],
        "independent_catches": independent["catch_proof_pass_count"],
        "external_model_review": "NOT_PERFORMED_CAVEAT",
        "result": "PASS",
    }


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    completed = run(["sha256sum", "--check", manifest.name], cwd=HERE)
    if corrupt or completed.returncode or "FAILED" in completed.stdout:
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    ]
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file()
        and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def expect_assertion(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch-proof accepted science corruption")


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "dual_systole_generic",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = validate_scope(generic)
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = validate_tests()
    science = validate_science()
    package = validate_package(generic)
    catches = {
        "scope": generic.expect(
            "SCOPE", lambda: validate_scope(generic, "CANON.md")
        ),
        "frozen": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)
        ),
        "current_paths": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, corrupt="current"),
        ),
        "frontier": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, corrupt="frontier"),
        ),
        "dirty": generic.expect(
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, corrupt=True)
        ),
        "dirty_head": generic.expect(
            "DIRTY", lambda: validate_dirty_head(generic, corrupt=True)
        ),
        "science_authority": expect_assertion(
            lambda: validate_science(corrupt=True)
        ),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, corrupt=True)
        ),
    }
    if any(value != "PASS" for value in catches.values()):
        raise AssertionError(f"repository catches failed: {catches}")

    result = {
        "schema": "udt-dual-systole-global-transport-repository-gates-v1",
        "date": "2026-07-24",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "science": science,
        "package_manifest": package,
        "catch_proofs": catches,
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "carrier_or_action_adopted": False,
            "physical_character_adopted": False,
            "phase_section_adopted": False,
            "density_scan_performed": False,
            "density_geometry_law_adopted": False,
            "matter_solve_performed": False,
            "gpu_work_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("repository_gates=PASS")
    print(
        f"frozen_packages={len(frozen['packages'])} "
        f"frozen_entries={frozen['entries']} tracked_paths={frozen['tracked_paths']}"
    )
    print(
        f"tests={tests['passed']} passed/{tests['xfailed']} xfailed "
        f"dirty_paths={dirty['paths']}"
    )
    print(
        f"wall_controls={science['wall_controls']} "
        f"maximum_tie={science['maximum_tie']} "
        f"catch_proofs={science['independent_catches']}"
    )


if __name__ == "__main__":
    main()
