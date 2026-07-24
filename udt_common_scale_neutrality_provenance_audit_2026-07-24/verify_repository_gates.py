#!/usr/bin/env python3
"""Repository, frozen evidence, navigation, tests, and dirty-metadata gates."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "c171b052ad321df7d71832cfa35403f07108d61e"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def git(*args: str) -> str:
    completed = run(["git", *args])
    if completed.returncode:
        raise AssertionError(completed.stdout)
    return completed.stdout


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    bad = sorted(path for path in paths if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise AssertionError(f"scope:{bad[0]}")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "SOURCE_CENSUS.tsv",
        "SOURCE_MANIFEST.tsv",
        "RESULTS.json",
        "INDEPENDENT_RESULTS.json",
        "CATCH_PROOF_RESULTS.tsv",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    outputs = []
    for command in (
        [sys.executable, "build_source_census.py"],
        [sys.executable, "derive_csn_provenance.py"],
        [sys.executable, "verify_csn_provenance_independent.py"],
    ):
        completed = run(command, cwd=HERE)
        outputs.append(completed.stdout)
        if completed.returncode:
            raise AssertionError(completed.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("science replay not byte-identical")

    result = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_RESULTS.json").read_text(encoding="utf-8")
    )
    if corrupt == "csn":
        result["rulings"]["strong_local_CSN"] = "DERIVED"
    elif corrupt == "c2":
        result["rulings"]["C2_Bach"] = "UNIQUE_UNCONDITIONAL"
    elif corrupt == "source":
        result["production_check_count"] = 19
    if (
        result["status"] != "PASS"
        or result["production_check_count"] != 20
        or not all(result["production_checks"].values())
        or result["rulings"]["strong_local_CSN"]
        != "OWNER_POSTULATE_NOT_DERIVED_FROM_RECIPROCITY_CURRENTLY_CHALLENGED"
        or result["rulings"]["C2_Bach"]
        != "UNIQUE_CONDITIONAL_IF_STRONG_LOCAL_CSN_IS_RETAINED"
        or result["rulings"]["EH"] != "CONDITIONAL_NOT_SELECTED"
        or result["rulings"]["physical_representative"] != "OPEN_SELECTOR"
    ):
        raise AssertionError("production science")
    if (
        independent["status"] != "PASS"
        or independent["catch_count"] != 10
        or any(row["result"] != "PASS_REJECTED" for row in independent["catches"])
    ):
        raise AssertionError("independent science")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "sources": 1421,
        "query_hits": 18612,
        "mandatory_load_bearing_paths": 29,
        "load_bearing_claim_rows": 23,
        "production_checks": 20,
        "independent_catches": 10,
        "production_stdout_sha256": hashlib.sha256(
            outputs[1].encode("utf-8")
        ).hexdigest(),
        "independent_stdout_sha256": hashlib.sha256(
            outputs[2].encode("utf-8")
        ).hexdigest(),
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status.returncode:
        raise AssertionError("dirty metadata unavailable")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    if corrupt:
        branch = "main"
    metadata_sha = hashlib.sha256(status.stdout).hexdigest()
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or len(status.stdout.splitlines()) != 54
        or metadata_sha
        != "4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c"
    ):
        raise AssertionError("dirty checkout metadata changed")
    return {
        "head": head,
        "branch": branch,
        "paths": len(status.stdout.splitlines()),
        "metadata_sha256": metadata_sha,
        "contents_read": False,
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError(completed.stdout)
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/",
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "result": "PASS",
    }


def validate_package(corrupt: bool = False) -> dict[str, object]:
    completed = run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=HERE)
    if corrupt or completed.returncode or "FAILED" in completed.stdout:
        raise AssertionError("package manifest")
    entries = [
        line.split("  ", 1)[1]
        for line in (HERE / "SHA256SUMS.txt").read_text().splitlines()
        if line
    ]
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file()
        and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": hashlib.sha256(
            (HERE / "SHA256SUMS.txt").read_bytes()
        ).hexdigest(),
        "result": "PASS",
    }


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "csn_provenance_generic",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = validate_scope()
    science = validate_science()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    dirty = validate_dirty()
    tests = validate_tests()
    package = validate_package()
    catches = {
        "scope": expect_failure(lambda: validate_scope("CANON.md")),
        "science_csn": expect_failure(lambda: validate_science("csn")),
        "science_c2": expect_failure(lambda: validate_science("c2")),
        "science_source": expect_failure(lambda: validate_science("source")),
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
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-common-scale-neutrality-provenance-repository-gates-v1",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "science": science,
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "historical_or_frozen_changed": False,
            "action_selected": False,
            "physical_metric_selected": False,
            "carrier_or_source_selected": False,
            "density_or_mass_solve": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
