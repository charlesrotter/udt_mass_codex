#!/usr/bin/env python3
"""Fail-closed verification for the observer-pair startup checkpoint."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
BASE = "f1c6cb4"
DIRTY = Path("/home/udt-admin/udt_mass_codex")

CONTROLS = (
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "AGENTS.md",
    "MEMORY.md",
    "research/README.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
)
RELATIONAL = "udt_relational_pair_depth_realization_audit_2026-07-24"
OPERATOR = "udt_observer_pair_clock_operator_audit_2026-07-24"
EXPECTED_SOURCE_HASHES = {
    f"{OPERATOR}/SHA256SUMS.txt": "588f49b51101406144ea3c747ecb10cc24e80fb647feb356499e96624158f1c4",
    f"{OPERATOR}/DERIVATION_RESULT.json": "65b3ca2782781526538050015ce6f768df9e736498e39100d16e76d67702c1da",
    f"{OPERATOR}/INDEPENDENT_VERIFICATION.json": "d50786ecd05ee2af29adbbbe04fae6160f361d583830bfc7871baf42be4ed1ed",
    f"{RELATIONAL}/SHA256SUMS.txt": "3d6668d1beb524628358bcb3a372209013ed2cdb10b1f1cbdb1752598de70af6",
    f"{RELATIONAL}/DERIVATION_RESULT.json": "e736e164c9f392992207028f13f12f64987ab7520d3cb1a46447d481a8d7bd3d",
    f"{RELATIONAL}/INDEPENDENT_VERIFICATION.json": "441a6808ba1356f873745d87b4eb41a09d76c4c7f04e45fdb7bce23c13898432",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
        stderr=subprocess.PIPE,
        check=False,
    )


def git(*args: str) -> str:
    completed = run(["git", *args])
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed.stdout


def load_generic():
    path = ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py"
    spec = importlib.util.spec_from_file_location("navigation_generic_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.BASE = BASE
    module.PACKAGE = HERE.name
    return module


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    allowed = set(CONTROLS)
    bad = sorted(
        path
        for path in paths
        if path
        and path not in allowed
        and not path.startswith(HERE.name + "/")
    )
    if bad:
        raise AssertionError(f"scope:{bad[0]}")
    if not set(CONTROLS).issubset(paths):
        raise AssertionError("scope:missing-control")
    return sorted(path for path in paths if path)


def marked(text: str, begin: str, end: str) -> str:
    if text.count(begin) != 1 or text.count(end) != 1:
        raise AssertionError("startup-marker-count")
    start = text.index(begin) + len(begin)
    stop = text.index(end)
    if start >= stop:
        raise AssertionError("startup-marker-order")
    return text[start:stop]


def validate_startup(corrupt: str = "") -> dict[str, object]:
    texts = {path: (ROOT / path).read_text(encoding="utf-8") for path in CONTROLS}
    if corrupt == "missing_relational":
        texts["INDEX.md"] = texts["INDEX.md"].replace(RELATIONAL, "missing_relational")
    elif corrupt == "missing_operator":
        texts["README.md"] = texts["README.md"].replace(OPERATOR, "missing_operator")
    elif corrupt == "local_physics":
        texts["HANDOFF.md"] = texts["HANDOFF.md"].replace(
            "local physics\n  in each observer's own frame is unchanged",
            "local physics is physically slowed",
            1,
        )
    elif corrupt == "three_observer":
        texts["LIVE.md"] = texts["LIVE.md"].replace(
            "THE THREE-OBSERVER CONTROL DOES NOT REFUTE PAIR DILATION",
            "THE THREE-OBSERVER CONTROL REFUTES PAIR DILATION",
            1,
        )
    elif corrupt == "next":
        texts["MEMORY.md"] = texts["MEMORY.md"].replace(
            "transition law", "selected action", 1
        )
    elif corrupt == "duplicate_marker":
        texts["LIVE.md"] += "\n<!-- STARTUP_CURRENT_BEGIN -->\n"

    live = marked(texts["LIVE.md"], "<!-- STARTUP_CURRENT_BEGIN -->", "<!-- STARTUP_CURRENT_END -->")
    handoff = marked(
        texts["HANDOFF.md"],
        "<!-- STARTUP_CURRENT_BEGIN -->",
        "<!-- STARTUP_CURRENT_END -->",
    )
    for path, text in texts.items():
        if RELATIONAL not in text or OPERATOR not in text:
            raise AssertionError(f"startup-route:{path}")
    required_live = (
        "DILATION IS ONLY AN INTER-FRAME COMPARISON",
        "THE THREE-OBSERVER CONTROL DOES NOT REFUTE PAIR DILATION",
        "OBSERVER_INDEXED_BILOCAL_METRIC_FAMILY_GIVEN_F",
        "TRANSITION LAW BETWEEN OBSERVER-INDEXED DEPTH-AND-ANGLE CHARTS",
    )
    if any(token not in live for token in required_live):
        raise AssertionError("live-current-semantics")
    required_handoff = (
        "local physics\n  in each observer's own frame is unchanged",
        "does not invalidate pairwise dilation",
        "observer-indexed bilocal family",
        "transition law between observer-indexed depth-and-angle charts",
    )
    if any(token not in handoff for token in required_handoff):
        raise AssertionError("handoff-current-semantics")
    memory = texts["MEMORY.md"]
    if (
        "## TOP — CURRENT POINTER (2026-07-24)" not in memory
        or "transition law" not in memory
        or "neutral local identity" not in memory
    ):
        raise AssertionError("memory-current-semantics")
    frontier_lines = [
        line
        for line in texts["UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"].splitlines()
        if line.startswith("## ") and "authority" in line
    ]
    if not frontier_lines or "observer-pair" not in frontier_lines[0] or "current authority" not in frontier_lines[0]:
        raise AssertionError("frontier-overlay-order")
    return {
        "control_files": len(CONTROLS),
        "live_current_lines": len(live.splitlines()),
        "handoff_current_lines": len(handoff.splitlines()),
        "result": "PASS",
    }


def validate_links(corrupt: bool = False) -> dict[str, object]:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    checked: list[str] = []
    for relative in CONTROLS:
        source = ROOT / relative
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = source.parent.joinpath(target).resolve()
            checked.append(f"{relative}:{target}")
            if not resolved.exists():
                raise AssertionError(f"markdown-link:{relative}:{target}")
    required = [
        ROOT / RELATIONAL / name
        for name in (
            "AUDIT_REPORT.md",
            "STATUS_LEDGER.tsv",
            "OWNER_FRAME_LEDGER.tsv",
            "EXACT_DERIVATION.md",
            "DEPTH_TYPE_RULING_LEDGER.tsv",
            "COMPOSITION_DOMAIN_LEDGER.tsv",
            "LAY_REPORT.md",
            "NEXT_STEP.md",
        )
    ]
    required += [
        ROOT / OPERATOR / name
        for name in (
            "AUDIT_REPORT.md",
            "STATUS_LEDGER.tsv",
            "EXACT_DERIVATION.md",
            "TRANSPORT_TYPE_LEDGER.tsv",
            "CLOCK_READOUT_LEDGER.tsv",
            "LAY_REPORT.md",
            "NEXT_STEP.md",
        )
    ]
    if corrupt:
        required.append(ROOT / "missing-startup-target")
    if not all(path.exists() for path in required):
        raise AssertionError("required-target")
    return {"markdown_links": len(checked), "required_targets": len(required), "result": "PASS"}


def validate_source_packages(corrupt: bool = False) -> dict[str, object]:
    details = []
    for index, package in enumerate((OPERATOR, RELATIONAL)):
        manifest = ROOT / package / "SHA256SUMS.txt"
        observed_manifest = digest(manifest.read_bytes())
        expected_manifest = EXPECTED_SOURCE_HASHES[f"{package}/SHA256SUMS.txt"]
        if corrupt and index == 0:
            observed_manifest = "0" * 64
        if observed_manifest != expected_manifest:
            raise AssertionError(f"source-manifest:{package}")
        completed = run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=manifest.parent)
        if completed.returncode or "FAILED" in completed.stdout:
            raise AssertionError(f"source-replay:{package}")
        for name in ("DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json"):
            path = ROOT / package / name
            if digest(path.read_bytes()) != EXPECTED_SOURCE_HASHES[f"{package}/{name}"]:
                raise AssertionError(f"source-hash:{package}:{name}")
        details.append(
            {
                "package": package,
                "manifest_sha256": expected_manifest,
                "entries": len(manifest.read_text(encoding="utf-8").splitlines()),
                "result": "PASS",
            }
        )
    return {"packages": details, "result": "PASS"}


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status.returncode:
        raise AssertionError("dirty-metadata-unavailable")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()
    metadata_hash = digest(status.stdout)
    if corrupt:
        branch = "main"
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or len(status.stdout.splitlines()) != 54
        or metadata_hash != "4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c"
    ):
        raise AssertionError("dirty-metadata-changed")
    return {
        "head": head,
        "branch": branch,
        "paths": 54,
        "metadata_sha256": metadata_hash,
        "contents_read": False,
        "result": "PASS",
    }


def validate_tests() -> dict[str, object]:
    completed = run([sys.executable, "-m", "pytest", "-q", "tests/"])
    (HERE / "TEST_STDOUT.txt").write_text(completed.stdout, encoding="utf-8")
    (HERE / "TEST_STDERR.txt").write_text(completed.stderr, encoding="utf-8")
    match = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode
        or match is None
        or tuple(map(int, match.groups())) != (70, 1)
        or " failed" in completed.stdout
    ):
        raise AssertionError("test-baseline")
    return {
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": digest(completed.stdout.encode()),
        "stderr_sha256": digest(completed.stderr.encode()),
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
    scope = validate_scope()
    startup = validate_startup()
    links = validate_links()
    sources = validate_source_packages()
    frozen = generic.validate_frozen(ROOT)
    navigation = generic.validate_navigation(ROOT)
    dirty = validate_dirty()
    tests = validate_tests()
    catches = {
        "unexpected_scope_rejected": expect_failure(lambda: validate_scope("CANON.md")),
        "missing_relational_route_rejected": expect_failure(
            lambda: validate_startup("missing_relational")
        ),
        "missing_operator_route_rejected": expect_failure(
            lambda: validate_startup("missing_operator")
        ),
        "local_physics_mutation_rejected": expect_failure(
            lambda: validate_startup("local_physics")
        ),
        "three_observer_overstatement_rejected": expect_failure(
            lambda: validate_startup("three_observer")
        ),
        "wrong_next_seam_rejected": expect_failure(lambda: validate_startup("next")),
        "duplicate_startup_marker_rejected": expect_failure(
            lambda: validate_startup("duplicate_marker")
        ),
        "missing_link_target_rejected": expect_failure(lambda: validate_links(True)),
        "source_manifest_mutation_rejected": expect_failure(
            lambda: validate_source_packages(True)
        ),
        "frozen_manifest_mutation_rejected": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)
        ),
        "current_path_loss_rejected": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")
        ),
        "frontier_target_loss_rejected": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")
        ),
        "dirty_metadata_mutation_rejected": expect_failure(lambda: validate_dirty(True)),
    }
    output = {
        "schema": "udt-observer-pair-navigation-checkpoint-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "startup": startup,
        "links": links,
        "source_packages": sources,
        "frozen": frozen,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "catch_proofs": catches,
        "authority_boundary": {
            "navigation_only": True,
            "new_scientific_result": False,
            "canon_changed": False,
            "fixed_registry_changed": False,
            "frozen_evidence_changed": False,
            "research_artifact_changed": False,
            "action_or_carrier_selected": False,
            "density_or_Xmax_promoted": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
