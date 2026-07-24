#!/usr/bin/env python3
"""Repository gates for the bootstrap substrate-to-micro closure audit."""

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
BASE = "3e3237b"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_hopf_realization_deformation_audit_2026-07-23"
PREVIOUS_MANIFEST_SHA256 = (
    "b1b69eb7a1aa1bfbc747f85d51c59cb835d1206c77a5be81d3eac993ee910e2b"
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
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
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
        str(
            generic.git(ROOT, "ls-files", "--others", "--exclude-standard")
        ).splitlines()
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
    previous_gate,
    consolidation,
    transport_parent,
    transport_gate,
    csn_gate,
    corrupt: bool = False,
) -> dict[str, object]:
    prior = previous_gate.replay_prior(
        generic,
        consolidation,
        transport_parent,
        transport_gate,
        csn_gate,
    )
    manifest = ROOT / PREVIOUS / "SHA256SUMS.txt"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PREVIOUS_MANIFEST_SHA256:
        raise generic.GateError("PRIOR", "previous-manifest")
    completed = run(["sha256sum", "--check", manifest.name], cwd=manifest.parent)
    if completed.returncode or "FAILED" in completed.stdout:
        raise generic.GateError("PRIOR", "previous-replay")
    entries = len([line for line in manifest.read_text().splitlines() if line])
    packages = list(prior["packages"])
    packages.append(
        {
            "package": PREVIOUS,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": entries,
            "result": "PASS",
        }
    )
    total_entries = int(prior["entries"]) + entries
    if len(packages) != 111 or entries != 23 or total_entries != 3172:
        raise generic.GateError(
            "PRIOR", f"totals:{len(packages)}:{entries}:{total_entries}"
        )
    return {"packages": packages, "entries": total_entries, "result": "PASS"}


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


def validate_science(mutate: str = "") -> dict[str, object]:
    names = {
        "production": "DERIVATION_RESULT.json",
        "channels": "CHANNEL_OUTCOMES.tsv",
        "regrades": "PRIOR_RESULT_REGRADE.tsv",
        "fixed": "FIXED_POINT_OUTCOMES.tsv",
        "completions": "COMPLETION_CHANNEL_MATRIX.tsv",
        "independent": "INDEPENDENT_VERIFICATION_RESULT.json",
    }
    with tempfile.TemporaryDirectory(prefix="udt_bootstrap_micro_") as temporary:
        temp = Path(temporary)
        commands = [
            [
                sys.executable,
                "derive_bootstrap_substrate_micro.py",
                "--result",
                str(temp / names["production"]),
                "--channels",
                str(temp / names["channels"]),
                "--regrades",
                str(temp / names["regrades"]),
                "--fixed-point",
                str(temp / names["fixed"]),
                "--completions",
                str(temp / names["completions"]),
            ],
            [
                sys.executable,
                "-s",
                "verify_bootstrap_substrate_micro_independent.py",
                "--production",
                str(temp / names["production"]),
                "--channels",
                str(temp / names["channels"]),
                "--regrades",
                str(temp / names["regrades"]),
                "--fixed-point",
                str(temp / names["fixed"]),
                "--completions",
                str(temp / names["completions"]),
                "--output",
                str(temp / names["independent"]),
            ],
        ]
        for command in commands:
            completed = run(command, cwd=HERE)
            if completed.returncode:
                raise AssertionError(
                    f"science replay failed: {command}\n"
                    f"{completed.stdout}\n{completed.stderr}"
                )
        for name in names.values():
            if (temp / name).read_bytes() != (HERE / name).read_bytes():
                raise AssertionError(f"science replay not byte-identical: {name}")

    production = json.loads((HERE / names["production"]).read_text())
    independent = json.loads((HERE / names["independent"]).read_text())
    channels = read_tsv(HERE / names["channels"])
    regrades = read_tsv(HERE / names["regrades"])
    fixed = read_tsv(HERE / names["fixed"])
    completions = read_tsv(HERE / names["completions"])
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    authority = read_tsv(HERE / "SOURCE_AUTHORITY.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    artifacts = {
        row["artifact"]: row["sha256"]
        for row in read_tsv(HERE / "ARTIFACT_HASHES.tsv")
    }
    for artifact, expected in artifacts.items():
        if digest(HERE / artifact) != expected:
            raise AssertionError(f"artifact hash mismatch: {artifact}")

    if mutate == "density":
        production["authority_boundary"]["density_curvature_law_derived"] = True
    if (
        not production["all_checks_pass"]
        or production["algebra"]["passed"] != 12
        or len(production["source_checks"]) != 17
        or not all(row["passed"] for row in production["source_checks"])
        or not independent["all_checks_pass"]
        or independent["counts"]["exact_passed"] != 11
        or independent["counts"]["agreement_passed"] != 13
        or independent["counts"]["catches_passed"] != 11
        or len(channels) != 24
        or len(regrades) != 15
        or len(fixed) != 14
        or len(completions) != 12
        or len(statuses) != 23
        or len(authority) != 15
        or len(catches) != 11
        or any(production["authority_boundary"].values())
    ):
        raise AssertionError("science/status/authority contract")

    return {
        "production_algebra": "12/12",
        "source_checks": "17/17",
        "independent_exact": "11/11",
        "independent_agreement": "13/13",
        "independent_catches": "11/11",
        "channels": len(channels),
        "regrades": len(regrades),
        "fixed_point_arrows": len(fixed),
        "completions": len(completions),
        "statuses": len(statuses),
        "authority_rows": len(authority),
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
    if len(entries) != 25:
        raise generic.GateError("PACKAGE", f"entries:{len(entries)}")
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
        "bootstrap_micro_generic",
    )
    previous_gate = load(
        ROOT / PREVIOUS / "verify_repository_gates.py",
        "bootstrap_micro_previous",
    )
    consolidation = load(
        ROOT
        / "udt_scientific_consolidation_checkpoint_2026-07-23"
        / "verify_repository_gates.py",
        "bootstrap_micro_consolidation",
    )
    transport_parent = load(
        ROOT
        / "udt_hopf_transport_bootstrap_dependency_audit_2026-07-23"
        / "verify_repository_gates.py",
        "bootstrap_micro_transport_parent",
    )
    transport_gate = load(
        ROOT
        / "udt_reciprocal_transport_naturality_selector_audit_2026-07-23"
        / "verify_repository_gates.py",
        "bootstrap_micro_transport",
    )
    csn_gate = load(
        ROOT
        / "udt_csn_dphi_transport_selector_audit_2026-07-23"
        / "verify_repository_gates.py",
        "bootstrap_micro_csn",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = validate_scope(generic)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(
        generic,
        previous_gate,
        consolidation,
        transport_parent,
        transport_gate,
        csn_gate,
    )
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(previous_gate.validate_dirty_head(generic))
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
                previous_gate,
                consolidation,
                transport_parent,
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
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, corrupt=True)
        ),
        "science_authority": "PASS"
        if _expect_assertion(lambda: validate_science("density"))
        else "FAIL",
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, corrupt=True)
        ),
    }
    if any(value != "PASS" for value in catches.values()):
        raise AssertionError(f"repository catches failed: {catches}")

    output = {
        "schema": "udt-bootstrap-substrate-micro-repository-gates-v1",
        "date": "2026-07-23",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "frozen": frozen,
        "prior_scientific_packages": prior,
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
            "density_scan_performed": False,
            "density_curvature_law_adopted": False,
            "gpu_work_performed": False,
            "time_live_solve_performed": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("repository_gates=PASS")
    print(
        f"prior_packages={len(prior['packages'])} "
        f"prior_entries={prior['entries']}"
    )
    print(
        f"tests={tests['passed']} passed/{tests['xfailed']} xfailed "
        f"dirty_paths={dirty['paths']}"
    )


def _expect_assertion(function) -> bool:
    try:
        function()
    except AssertionError:
        return True
    return False


if __name__ == "__main__":
    main()
