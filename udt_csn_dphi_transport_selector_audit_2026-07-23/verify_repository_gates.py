#!/usr/bin/env python3
"""Repository and evidence gates for the CSN--dphi transport audit."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "42edf80"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
CONSOLIDATION = "udt_scientific_consolidation_checkpoint_2026-07-23"
CONSOLIDATION_MANIFEST_SHA256 = (
    "37b80dedf0f1d3574f4c477e70f4121e6738dfa0ae3c250fdb97731188e66231"
)
DIRTY_HEAD = "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
DIRTY_BRANCH = "grok"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        stderr=subprocess.PIPE,
        check=False,
    )


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_scope(generic, injected: str = "") -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(
        str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines()
    )
    changed.discard(f"{PACKAGE}/REPOSITORY_GATES.json")
    if injected:
        changed.add(injected)
    invalid = sorted(
        path for path in changed if path and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    return sorted(changed)


def replay_prior(generic, consolidation, corrupt: bool = False) -> dict[str, object]:
    prior = consolidation.replay_parent(generic)
    manifest = ROOT / CONSOLIDATION / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != CONSOLIDATION_MANIFEST_SHA256:
        raise generic.GateError("PRIOR", "consolidation-manifest")
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PRIOR", "consolidation-replay")
    entries = len([line for line in manifest.read_text().splitlines() if line])
    packages = list(prior["packages"])
    packages.append(
        {
            "package": CONSOLIDATION,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": entries,
            "result": "PASS",
        }
    )
    if len(packages) != 107 or entries != 32:
        raise generic.GateError("PRIOR", f"totals:{len(packages)}:{entries}")
    return {
        "packages": packages,
        "entries": int(prior["entries"]) + entries,
        "result": "PASS",
    }


def validate_dirty_head(generic) -> dict[str, object]:
    head = str(generic.git(DIRTY, "rev-parse", "HEAD")).strip()
    branch = str(generic.git(DIRTY, "branch", "--show-current")).strip()
    if head != DIRTY_HEAD or branch != DIRTY_BRANCH:
        raise generic.GateError("DIRTY", f"head-or-branch:{head}:{branch}")
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
        raise AssertionError("repository test baseline changed")
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/",
        "returncode": completed.returncode,
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "result": "PASS",
    }


def validate_science() -> dict[str, object]:
    production = HERE / "DERIVATION_RESULT.json"
    independent = HERE / "INDEPENDENT_VERIFICATION_RESULT.json"
    with tempfile.TemporaryDirectory(prefix="udt_csn_dphi_verify_") as tmp:
        tmpdir = Path(tmp)
        prod_tmp = tmpdir / "production.json"
        indep_tmp = tmpdir / "independent.json"
        commands = [
            [
                sys.executable,
                "derive_csn_dphi_transport.py",
                "--output",
                str(prod_tmp),
            ],
            [
                sys.executable,
                "-s",
                "verify_csn_dphi_transport_independent.py",
                "--production-result",
                str(prod_tmp),
                "--output",
                str(indep_tmp),
            ],
        ]
        for command in commands:
            completed = run(command, cwd=HERE)
            if completed.returncode:
                raise AssertionError(f"science replay failed: {command}")
        if prod_tmp.read_bytes() != production.read_bytes():
            raise AssertionError("production replay is not byte-identical")
        if indep_tmp.read_bytes() != independent.read_bytes():
            raise AssertionError("independent replay is not byte-identical")

    prod = json.loads(production.read_text())
    indep = json.loads(independent.read_text())
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    status_map = {row["id"]: row["status"] for row in statuses}
    if (
        prod["checks_total"] != prod["checks_passed"]
        or prod["checks_total"] != 38
        or indep["checks_total"] != indep["checks_passed"]
        or indep["checks_total"] != 25
        or indep["catch_proofs_total"] != indep["catch_proofs_passed"]
        or indep["catch_proofs_total"] != 12
        or len(statuses) != 23
        or status_map.get("S04") != "DERIVED_GEOMETRIC_CANDIDATE"
        or status_map.get("S09") != "UNIQUE_CONDITIONAL"
        or status_map.get("S16") != "OBSTRUCTED_FOR_THIS_CONSTRUCTION"
        or status_map.get("S21") != "OPEN"
        or status_map.get("S23") != "OPEN_NOT_ACTIVATED"
    ):
        raise AssertionError("science/status contract")
    return {
        "production_checks": 38,
        "independent_checks": 25,
        "independent_catches": 12,
        "status_rows": 23,
        "production_sha256": digest(production),
        "independent_sha256": digest(independent),
        "deterministic_replay": "BYTE_IDENTICAL",
        "result": "PASS",
    }


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
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


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "csn_dphi_generic_gates",
    )
    consolidation = load(
        ROOT / CONSOLIDATION / "verify_repository_gates.py",
        "csn_dphi_consolidation_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = validate_scope(generic)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic, consolidation)
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
        "prior": generic.expect(
            "PRIOR", lambda: replay_prior(generic, consolidation, corrupt=True)
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
            "DIRTY",
            lambda: generic.validate_dirty(ROOT, DIRTY, corrupt=True),
        ),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, corrupt=True)
        ),
    }
    result = {
        "schema": "udt-csn-dphi-transport-repository-gates-v1",
        "date": "2026-07-23",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "science": science,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "authority_boundary": {
            "physical_connection_adopted": False,
            "action_or_source_constructed": False,
            "carrier_adopted": False,
            "gpu_work_performed": False,
            "canon_changed": False,
            "repository_reorganization_performed": False,
        },
    }
    HERE.joinpath("REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
