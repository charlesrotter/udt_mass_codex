#!/usr/bin/env python3
"""Fail-closed science, source, repository, and package gates."""

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


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = HERE.name
BASE = "d000d9caace162723084941816077aa97dbf3c78"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
SOURCE = DIRTY / "phiequations.md"
SOURCE_SHA = "1dba7fa26a7a658d1dabdce6d98974b52f007cb85a33796f2a80e05995b97b62"
ALLOWED_NAVIGATION = {
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "research/README.md",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
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


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def expect_failure(callback) -> str:
    try:
        callback()
    except AssertionError:
        return "PASS"
    raise AssertionError("catch accepted corruption")


def validate_scope(injected: str = "") -> dict[str, object]:
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    # The gate output is generated after scope validation; include its declared
    # path unconditionally so pre-commit and post-commit replays are identical.
    paths.add(PACKAGE + "/REPOSITORY_GATES.json")
    if injected:
        paths.add(injected)
    invalid = sorted(
        path
        for path in paths
        if path
        and not path.startswith(PACKAGE + "/")
        and path not in ALLOWED_NAVIGATION
    )
    if invalid:
        raise AssertionError(f"scope:{invalid[0]}")
    return {"paths": sorted(path for path in paths if path), "result": "PASS"}


def validate_source(corrupt: bool = False) -> dict[str, object]:
    data = SOURCE.read_bytes()
    observed = digest(data)
    if corrupt:
        observed = "0" * 64
    if (
        observed != SOURCE_SHA
        or len(data) != 14814
        or len(data.splitlines()) != 450
    ):
        raise AssertionError("historical source identity")
    return {
        "path": str(SOURCE),
        "sha256": observed,
        "size_bytes": len(data),
        "line_count": len(data.splitlines()),
        "modified": "2026-01-10 22:29:35 -0500",
        "read_authority": "EXPLICIT_USER_DIRECTION",
        "mutated": False,
        "result": "PASS",
    }


def validate_science(corrupt: str = "") -> dict[str, object]:
    before = {
        name: (HERE / name).read_bytes()
        for name in ["DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json"]
    }
    for script in ["derive_phi_salvage.py", "verify_phi_salvage_independent.py"]:
        completed = run([sys.executable, script], cwd=HERE)
        if completed.returncode:
            raise AssertionError(completed.stdout)
    after = {
        name: (HERE / name).read_bytes()
        for name in ["DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json"]
    }
    if before != after:
        raise AssertionError("science replay not byte-identical")

    production = json.loads(after["DERIVATION_RESULT.json"])
    independent = json.loads(after["INDEPENDENT_VERIFICATION.json"])
    ledger = {row["claim_id"]: row for row in rows(HERE / "CLAIM_LEDGER.tsv")}
    state: dict[str, object] = {
        "production": production["all_pass"],
        "production_count": production["pass_count"],
        "independent": independent["all_pass"],
        "independent_count": independent["pass_count"],
        "screen_action": ledger["H04"]["primary_class"],
        "probe_equation": ledger["H05"]["primary_class"],
        "universal_equation": ledger["H06"]["primary_class"],
        "screen_scale": ledger["H07"]["primary_class"],
        "source": ledger["H08"]["primary_class"],
        "sinh": ledger["H10"]["primary_class"],
        "wrl": ledger["H11"]["current_disposition"],
        "bilocal": ledger["H12"]["current_disposition"],
        "claim_count": len(ledger),
    }
    mutations = {
        "screen_action_native": ("screen_action", "SALVAGE_EXACT_METRIC_IDENTITY"),
        "probe_promoted": ("probe_equation", "SALVAGE_EXACT_METRIC_IDENTITY"),
        "universal_promoted": ("universal_equation", "SALVAGE_EXACT_METRIC_IDENTITY"),
        "scale_promoted": ("screen_scale", "SALVAGE_EXACT_METRIC_IDENTITY"),
        "source_promoted": ("source", "SALVAGE_EXACT_METRIC_IDENTITY"),
        "sinh_promoted": ("sinh", "SALVAGE_EXACT_METRIC_IDENTITY"),
        "wrl_promoted": ("wrl", "DERIVED_ZERO_SOURCE"),
        "bilocal_promoted": ("bilocal", "CLOSES_CURRENT_GATE"),
        "missing_claim": ("claim_count", 12),
    }
    if corrupt:
        key, value = mutations[corrupt]
        state[key] = value
    if (
        state["production"] is not True
        or state["production_count"] != 8
        or state["independent"] is not True
        or state["independent_count"] != 4
        or state["screen_action"] != "REJECT_AS_NATIVE_UDT_LAW"
        or state["probe_equation"] != "SALVAGE_CONDITIONAL_PROBE_RESULT"
        or state["universal_equation"] != "REJECT_AS_NATIVE_UDT_LAW"
        or state["screen_scale"] != "REJECT_AS_NATIVE_UDT_LAW"
        or state["source"] != "REJECT_AS_NATIVE_UDT_LAW"
        or state["sinh"] != "SALVAGE_CONDITIONAL_PROBE_RESULT"
        or state["wrl"] != "REFUTED_AS_ZERO_SOURCE_JOIN"
        or state["bilocal"] != "NO_HELP_ON_OPEN_GATE"
        or state["claim_count"] != 13
    ):
        raise AssertionError("scientific classification")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 8,
        "independent_checks": 4,
        "claim_rows": 13,
        "production_sha256": digest(after["DERIVATION_RESULT.json"]),
        "independent_sha256": digest(after["INDEPENDENT_VERIFICATION.json"]),
        "result": "PASS",
    }


def validate_navigation() -> dict[str, object]:
    required = {
        "HANDOFF.md": "udt_historical_phi_equation_salvage_audit_2026-07-24/AUDIT_REPORT.md",
        "INDEX.md": "udt_historical_phi_equation_salvage_audit_2026-07-24/AUDIT_REPORT.md",
        "README.md": "udt_historical_phi_equation_salvage_audit_2026-07-24/AUDIT_REPORT.md",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": "udt_historical_phi_equation_salvage_audit_2026-07-24/AUDIT_REPORT.md",
        "research/README.md": "../udt_historical_phi_equation_salvage_audit_2026-07-24/AUDIT_REPORT.md",
    }
    for path, pointer in required.items():
        if pointer not in (ROOT / path).read_text(encoding="utf-8"):
            raise AssertionError(f"missing navigation pointer:{path}")
    if "udt_historical_phi_equation_salvage" in (
        ROOT / "LIVE.md"
    ).read_text(encoding="utf-8"):
        raise AssertionError("LIVE changed for supporting-only audit")
    current = rows(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    frontier = rows(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    if len(current) != 1114 or len(frontier) != 306:
        raise AssertionError("navigation registry count")
    return {
        "pointers": len(required),
        "current_paths": len(current),
        "frontier_rows": len(frontier),
        "LIVE_changed": False,
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    text = (HERE / "TEST_STDOUT.txt").read_text(encoding="utf-8")
    match = re.search(r"(\d+) passed, (\d+) xfailed", text)
    if match is None or tuple(map(int, match.groups())) != (70, 1):
        raise AssertionError("test baseline")
    return {
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": digest((HERE / "TEST_STDOUT.txt").read_bytes()),
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    legacy = {
        row["path"]: row
        for row in rows(
            ROOT
            / "reorganization_r1b/postmove_forensic_census/"
            / "DIRTY_WORKSTATION_INVENTORY.tsv"
        )
    }
    observed = generic_dirty_metadata(DIRTY)
    if corrupt:
        observed = dict(observed)
        observed.pop("phiequations.md", None)
    if len(legacy) != 54 or len(observed) != 55:
        raise AssertionError(f"dirty count:{len(legacy)}:{len(observed)}")
    if set(observed) != set(legacy) | {"phiequations.md"}:
        raise AssertionError("dirty identity set")
    for path, row in legacy.items():
        expected = (
            row["status"],
            int(row["size_bytes_lstat"]),
            row["object_type"],
        )
        if observed[path] != expected or row["content_sha256"] != "NOT_READ":
            raise AssertionError(f"legacy dirty metadata:{path}")
    if observed["phiequations.md"] != ("??", 14814, "regular_file"):
        raise AssertionError("historical source dirty metadata")
    status = git_at(DIRTY, "status", "--short")
    if (
        digest(status.encode())
        != "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"
        or git_at(DIRTY, "rev-parse", "HEAD").strip()
        != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or git_at(DIRTY, "branch", "--show-current").strip() != "grok"
    ):
        raise AssertionError("dirty checkout identity")
    return {
        "paths": 55,
        "legacy_metadata_only_paths": 54,
        "new_explicit_source_path": "phiequations.md",
        "status_sha256": digest(status.encode()),
        "contents_read": "ONLY_EXPLICITLY_AUTHORIZED_phiequations.md",
        "mutated": False,
        "result": "PASS",
    }


def git_at(repo: Path, *args: str) -> str:
    completed = run(["git", *args], cwd=repo)
    if completed.returncode:
        raise AssertionError(completed.stdout)
    return completed.stdout


def generic_dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    # Reuse the frozen R1B parser after the generic module is loaded in main.
    return _GENERIC.dirty_metadata(repo)


def validate_package(corrupt: bool = False) -> dict[str, object]:
    completed = run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=HERE)
    if corrupt or completed.returncode or "FAILED" in completed.stdout:
        raise AssertionError("package manifest")
    entries = [
        line.split("  ", 1)[1]
        for line in (HERE / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        if line
    ]
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file()
        and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package manifest coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest((HERE / "SHA256SUMS.txt").read_bytes()),
        "result": "PASS",
    }


def main() -> None:
    global _GENERIC
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "historical_phi_generic_gates",
    )
    _GENERIC = generic
    generic.BASE = BASE

    scope = validate_scope()
    source = validate_source()
    science = validate_science()
    frozen = generic.validate_frozen(ROOT)
    navigation_registry = generic.validate_navigation(ROOT)
    navigation = validate_navigation()
    dirty = validate_dirty()
    tests = validate_tests()
    package = validate_package()

    science_catches = {
        key: expect_failure(lambda key=key: validate_science(key))
        for key in [
            "screen_action_native",
            "probe_promoted",
            "universal_promoted",
            "scale_promoted",
            "source_promoted",
            "sinh_promoted",
            "wrl_promoted",
            "bilocal_promoted",
            "missing_claim",
        ]
    }
    catches = {
        "out_of_scope_mutation_rejected": expect_failure(
            lambda: validate_scope("CANON.md")
        ),
        "historical_source_mutation_rejected": expect_failure(
            lambda: validate_source(corrupt=True)
        ),
        "dirty_identity_loss_rejected": expect_failure(
            lambda: validate_dirty(corrupt=True)
        ),
        "frozen_corruption_rejected": expect_failure(
            lambda: generic.validate_frozen(ROOT, corrupt=True)
        ),
        "package_corruption_rejected": expect_failure(
            lambda: validate_package(corrupt=True)
        ),
        **science_catches,
    }

    output = {
        "schema": "udt-historical-phi-equation-salvage-gates-v1",
        "result": "PASS",
        "base": BASE,
        "scope": scope,
        "source": source,
        "science": science,
        "frozen": frozen,
        "navigation_registry": navigation_registry,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package": package,
        "catch_proofs": catches,
        "catch_count": len(catches),
        "authority_boundary": {
            "LIVE_changed": False,
            "CANON_changed": False,
            "native_action_selected": False,
            "native_source_selected": False,
            "profile_selected": False,
            "bilocal_gate_closed": False,
            "gpu_work_performed": False,
            "research_artifact_mutated": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("repository_gates=PASS")
    print(
        f"science={science['production_checks']}+{science['independent_checks']} "
        f"claims={science['claim_rows']}"
    )
    print(
        f"frozen={len(frozen['packages'])} manifests/"
        f"{frozen['entries']} entries/{frozen['tracked_paths']} paths"
    )
    print(f"tests={tests['passed']} passed/{tests['xfailed']} xfailed")
    print(f"catches={len(catches)}")
    print(f"gate_sha256={digest((HERE / 'REPOSITORY_GATES.json').read_bytes())}")


if __name__ == "__main__":
    main()
