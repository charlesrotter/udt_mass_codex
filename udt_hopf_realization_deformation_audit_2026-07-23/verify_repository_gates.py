#!/usr/bin/env python3
"""Repository gates for the Hopf realization deformation audit."""

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
BASE = "7bb7d13"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
DIRTY_HEAD = "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
DIRTY_BRANCH = "grok"
PARENT = "udt_hopf_transport_bootstrap_dependency_audit_2026-07-23"
PARENT_MANIFEST_SHA256 = (
    "95b69c6400aa60923126b1be4e84511876475791b49ba47a08d57db115078360"
)


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
    with path.open(newline="", encoding="utf-8") as handle:
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


def replay_prior(
    generic,
    consolidation,
    parent_gate,
    transport_gate,
    csn_gate,
    corrupt: bool = False,
):
    prior = parent_gate.replay_prior(
        generic, consolidation, transport_gate, csn_gate
    )
    parent_dir = ROOT / PARENT
    manifest = parent_dir / "SHA256SUMS.txt"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PARENT_MANIFEST_SHA256:
        raise generic.GateError("PRIOR", "parent-manifest")
    completed = run(["sha256sum", "--check", manifest.name], cwd=parent_dir)
    if completed.returncode or "FAILED" in completed.stdout:
        raise generic.GateError("PRIOR", "parent-replay")
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
    total_entries = int(prior["entries"]) + entries
    if len(packages) != 110 or entries != 20 or total_entries != 3149:
        raise generic.GateError(
            "PRIOR", f"totals:{len(packages)}:{entries}:{total_entries}"
        )
    return {"packages": packages, "entries": total_entries, "result": "PASS"}


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
        raise AssertionError(
            f"repository test baseline changed: {completed.returncode}\n"
            f"{completed.stdout}\n{completed.stderr}"
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


def validate_science() -> dict[str, object]:
    production = HERE / "DERIVATION_RESULT.json"
    candidate = HERE / "DEFORMATION_OUTCOMES.tsv"
    global_result = HERE / "GLOBAL_COMPLETION_OUTCOMES.tsv"
    independent = HERE / "INDEPENDENT_VERIFICATION_RESULT.json"
    with tempfile.TemporaryDirectory(prefix="udt_hopf_deformation_") as tmp:
        tmpdir = Path(tmp)
        prod_tmp = tmpdir / "production.json"
        candidate_tmp = tmpdir / "candidate.tsv"
        global_tmp = tmpdir / "global.tsv"
        independent_tmp = tmpdir / "independent.json"
        commands = [
            [
                sys.executable,
                "derive_hopf_realization_deformations.py",
                "--output",
                str(prod_tmp),
                "--candidate-output",
                str(candidate_tmp),
                "--global-output",
                str(global_tmp),
            ],
            [
                sys.executable,
                "-s",
                "verify_hopf_realization_deformations_independent.py",
                "--production-result",
                str(prod_tmp),
                "--candidate-result",
                str(candidate_tmp),
                "--global-result",
                str(global_tmp),
                "--output",
                str(independent_tmp),
            ],
        ]
        for command in commands:
            completed = run(command, cwd=HERE)
            if completed.returncode:
                raise AssertionError(
                    f"science replay failed: {command}\n"
                    f"{completed.stdout}\n{completed.stderr}"
                )
        for expected, replay in (
            (production, prod_tmp),
            (candidate, candidate_tmp),
            (global_result, global_tmp),
            (independent, independent_tmp),
        ):
            if replay.read_bytes() != expected.read_bytes():
                raise AssertionError(f"science replay not byte-identical: {expected.name}")

    prod = json.loads(production.read_text())
    indep = json.loads(independent.read_text())
    candidates = read_tsv(candidate)
    completions = read_tsv(global_result)
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    authority = read_tsv(HERE / "SOURCE_AUTHORITY.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    status_map = {row["id"]: row["status"] for row in statuses}
    artifacts = {
        row["artifact"]: row["sha256"]
        for row in read_tsv(HERE / "ARTIFACT_HASHES.tsv")
    }
    for artifact, expected in artifacts.items():
        if digest(HERE / artifact) != expected:
            raise AssertionError(f"artifact hash mismatch: {artifact}")
    if (
        not prod["all_checks_pass"]
        or len(prod["checks"]) != 15
        or not indep["all_checks_pass"]
        or indep["counts"]["exact_passed"] != 11
        or indep["counts"]["catches_passed"] != 15
        or indep["counts"]["agreement_passed"] != 6
        or len(candidates) != 20
        or len(completions) != 12
        or len(statuses) != 23
        or len(authority) != 15
        or len(catches) != 15
        or status_map.get("S03") != "RANK_ONE_LATITUDE_IMAGE"
        or status_map.get("S09") != "PHASE_CONNECTION_DERIVED_IN_CHART"
        or status_map.get("S21")
        != "RESTRICTED_CONDITIONAL_SEED_DEFORMATION_ONLY"
        or prod["global_counts"]["native_full_deformation"] != 0
    ):
        raise AssertionError("science/status contract")
    return {
        "production_checks": 15,
        "independent_exact_checks": 11,
        "independent_catches": 15,
        "independent_agreement_checks": 6,
        "candidate_rows": 20,
        "completion_rows": 12,
        "status_rows": 23,
        "source_authority_rows": 15,
        "production_sha256": digest(production),
        "candidate_sha256": digest(candidate),
        "completion_sha256": digest(global_result),
        "independent_sha256": digest(independent),
        "deterministic_replay": "BYTE_IDENTICAL",
        "fresh_zero_context_model_review": "NOT_PERFORMED_CAVEAT",
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


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "hopf_deformation_generic_gates",
    )
    consolidation = load(
        ROOT
        / "udt_scientific_consolidation_checkpoint_2026-07-23"
        / "verify_repository_gates.py",
        "hopf_deformation_consolidation_gates",
    )
    parent_gate = load(
        ROOT / PARENT / "verify_repository_gates.py",
        "hopf_deformation_parent_gates",
    )
    transport_gate = load(
        ROOT
        / "udt_reciprocal_transport_naturality_selector_audit_2026-07-23"
        / "verify_repository_gates.py",
        "hopf_deformation_transport_gates",
    )
    csn_gate = load(
        ROOT
        / "udt_csn_dphi_transport_selector_audit_2026-07-23"
        / "verify_repository_gates.py",
        "hopf_deformation_csn_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = validate_scope(generic)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(
        generic,
        consolidation,
        parent_gate,
        transport_gate,
        csn_gate,
    )
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
            "PRIOR",
            lambda: replay_prior(
                generic,
                consolidation,
                parent_gate,
                transport_gate,
                csn_gate,
                corrupt=True,
            ),
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
        "schema": "udt-hopf-realization-deformation-repository-gates-v1",
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
            "native_carrier_adopted": False,
            "full_metric_to_carrier_map_claimed": False,
            "phase_section_adopted": False,
            "flat_shift_connection_assumed": False,
            "physical_connection_adopted": False,
            "action_or_source_constructed": False,
            "bootstrap_local_selector_adopted": False,
            "density_scan_performed": False,
            "time_live_solve_performed": False,
            "gpu_work_performed": False,
            "canon_changed": False,
            "startup_controls_changed": False,
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
