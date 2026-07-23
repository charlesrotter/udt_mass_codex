#!/usr/bin/env python3
"""Repository gates for the scientific consolidation checkpoint."""

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
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "7995470"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PARENT = "udt_finite_cell_cartan_transport_atlas_2026-07-23"
PARENT_MANIFEST_SHA256 = "f70ec5f8bad2fc648ff4d9d983628bd7a450374db2fd3fc766a88c6ae67e7c5e"
CONTROLS = {
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "AGENTS.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "research/README.md",
    "MEMORY.md",
}
MAXIMUM = (
    "CURRENT_EVIDENCE_LINKED_NAVIGATION_AND_STATUS_CHECKPOINT_"
    "VERIFIED_WITHOUT_NEW_PHYSICS_OR_ARTIFACT_REORGANIZATION"
)


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_scope(generic, injected: str = "") -> list[str]:
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
    # This generated report is an output, not an input to its own scope.
    # Excluding it makes the first run and every clean committed replay
    # byte-identical.
    changed.discard(f"{PACKAGE}/REPOSITORY_GATES.json")
    if injected:
        changed.add(injected)
    invalid = sorted(
        path
        for path in changed
        if path
        and path not in CONTROLS
        and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    if not CONTROLS.issubset(changed):
        raise generic.GateError("SCOPE", "missing-control")
    return sorted(changed)


def replay_parent(generic, corrupt: bool = False) -> dict[str, object]:
    parent_gate = load(
        ROOT / PARENT / "verify_repository_gates.py",
        "consolidation_parent_gate",
    )
    prior = parent_gate.replay_parent(generic)
    manifest = ROOT / PARENT / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PARENT_MANIFEST_SHA256:
        raise generic.GateError("PARENT", "finite-cell-manifest")
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PARENT", "finite-cell-replay")
    entries = len([line for line in manifest.read_text().splitlines() if line])
    packages = list(prior["packages"])
    packages.append(
        {
            "package": PARENT,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": entries,
            "result": "PASS",
        }
    )
    if len(packages) != 106 or entries != 25:
        raise generic.GateError("PARENT", f"totals:{len(packages)}:{entries}")
    return {
        "packages": packages,
        "entries": int(prior["entries"]) + entries,
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/"],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode != 0
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError("repository test baseline changed")
    recorded = json.loads(HERE.joinpath("FULL_TEST_RESULT.json").read_text())
    if (
        (recorded["passed"], recorded["failed"], recorded["xfailed"])
        != (70, 0, 1)
        or digest(HERE / "FULL_TEST_STDOUT.txt")
        != recorded["stdout_sha256"]
    ):
        raise AssertionError("recorded test result")
    return {**recorded, "result": "PASS"}


def validate_links() -> dict[str, int]:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    paths = [ROOT / path for path in CONTROLS if path.endswith(".md")]
    paths.extend(sorted(HERE.glob("*.md")))
    checked = 0
    for source in paths:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = source.parent.joinpath(
                unquote(target.split("#", 1)[0])
            ).resolve()
            checked += 1
            if not resolved.exists():
                raise AssertionError(f"broken link {source}:{target}")
    return {"markdown_links": checked}


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
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
        and path.name not in {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def validate_science(mutation: str = "") -> dict[str, object]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for command in (
        [sys.executable, "build_checkpoint_evidence.py"],
        [sys.executable, "-s", "verify_checkpoint_independent.py"],
    ):
        completed = subprocess.run(
            command,
            cwd=HERE,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode:
            raise AssertionError(f"checkpoint replay: {command}")
    result = json.loads(HERE.joinpath("CHECKPOINT_RESULT.json").read_text())
    independent = json.loads(
        HERE.joinpath("INDEPENDENT_VERIFICATION.json").read_text()
    )
    rehearsal = json.loads(
        HERE.joinpath("ZERO_STATE_REHEARSAL_RESULT.json").read_text()
    )
    statuses = read_tsv(HERE / "CURRENT_STATUS_LEDGER.tsv")
    if mutation:
        statuses[10]["status"] = "DERIVED"
    status_map = {row["id"]: row["status"] for row in statuses}
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    maps = read_tsv(HERE / "METRIC_TO_FRONTIER_MAP.tsv")
    guards = read_tsv(HERE / "REGRESSION_GUARD_LEDGER.tsv")
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["source_count"] != 26
        or result["source_addition_count"] != 1
        or result["status_count"] != 24
        or result["post_commit_status_correction_count"] != 2
        or result["frontier_map_count"] != 13
        or result["regression_guard_count"] != 15
        or result["physics_derivation_performed"] is not False
        or result["artifact_move_performed"] is not False
        or independent["all_checks_pass"] is not True
        or independent["check_count"] != 16
        or independent["all_catches_pass"] is not True
        or independent["catch_count"] != 24
        or rehearsal["all_checks_pass"] is not True
        or len(rehearsal["checks"]) != 17
        or "head" in rehearsal
        or "worktree_status" in rehearsal
        or rehearsal["method"]
        != "deterministic_parser_no_conversational_context_no_external_model"
        or len(statuses) != 24
        or status_map.get("C11") != "OPEN"
        or status_map.get("C14") != "OPEN"
        or status_map.get("C23") != "OPEN"
        or status_map.get("C10")
        != "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
        or status_map.get("C22") != "OPEN_NOT_JOINED"
        or len(lineage) != 26
        or len(maps) != 13
        or len(guards) != 15
    ):
        raise AssertionError("checkpoint science contract")
    return {
        "grade": "NAVIGATION-VERIFIED",
        "sources": 26,
        "statuses": 24,
        "frontier_map_rows": 13,
        "regression_guards": 15,
        "independent_checks": 16,
        "independent_catches": 24,
        "zero_state_checks": 17,
        "external_model_review": "NOT_PERFORMED_NO_DISCLOSURE_GRANT",
        "result": "PASS",
    }


def reject_science_mutation(generic) -> None:
    try:
        validate_science("promote-action")
    except AssertionError as exc:
        raise generic.GateError("SCIENCE", "open-action-promotion") from exc


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "consolidation_generic_gate",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = validate_scope(generic)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_parent(generic)
    navigation = generic.validate_navigation(ROOT)
    links = validate_links()
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty_head = load(
        ROOT
        / "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23"
        / "verify_repository_gates.py",
        "consolidation_dirty_head",
    )
    dirty.update(dirty_head.validate_dirty_head(generic))
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
        "parent": generic.expect(
            "PARENT", lambda: replay_parent(generic, corrupt=True)
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
        "science": generic.expect(
            "SCIENCE", lambda: reject_science_mutation(generic)
        ),
    }
    output = {
        "schema": "udt-scientific-consolidation-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "authority_boundary": MAXIMUM,
        "scope_paths": scope,
        "science": science,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "links": links,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {
            "physics_derivation_performed": False,
            "gpu_work_performed": False,
        },
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    HERE.joinpath("REPOSITORY_GATES.json").write_text(
        rendered, encoding="utf-8"
    )
    print(rendered, end="")


if __name__ == "__main__":
    main()
