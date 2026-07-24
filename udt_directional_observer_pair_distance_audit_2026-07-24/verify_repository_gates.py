#!/usr/bin/env python3
"""Repository, science, frozen-package, navigation, and dirt gates."""

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
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "f566f44"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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
        "DERIVATION_RESULT.json",
        "FC_PAIR_DISTANCE_SCREEN.tsv",
        "EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv",
        "SOLDER_FAMILY_PAIR_DISTANCE_SCREEN.tsv",
        "COMPLETE_WITNESS_LEDGER.tsv",
        "ROUND_DIRECTIONAL_DISTANCE_LEDGER.tsv",
        "SQUASHED_CONTROL_LEDGER.tsv",
        "SHAPE_SENSITIVITY_LEDGER.tsv",
        "PHYSICAL_XMAX_GATE_MATRIX.tsv",
        "STATUS_LEDGER.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
        "RUN_ENVIRONMENT.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    completed = run([sys.executable, "replay_and_capture.py"], cwd=HERE)
    if completed.returncode:
        raise AssertionError(completed.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("science replay not byte-identical")

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    fc_rows = read_tsv(HERE / "FC_PAIR_DISTANCE_SCREEN.tsv")
    families = read_tsv(HERE / "EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv")
    solder = read_tsv(HERE / "SOLDER_FAMILY_PAIR_DISTANCE_SCREEN.tsv")
    witnesses = {row["witness_id"]: row for row in read_tsv(HERE / "COMPLETE_WITNESS_LEDGER.tsv")}
    round_rows = {row["quantity"]: row for row in read_tsv(HERE / "ROUND_DIRECTIONAL_DISTANCE_LEDGER.tsv")}
    squashed = {row["quantity"]: row for row in read_tsv(HERE / "SQUASHED_CONTROL_LEDGER.tsv")}
    gates = read_tsv(HERE / "PHYSICAL_XMAX_GATE_MATRIX.tsv")
    statuses = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}

    if corrupt == "center":
        result["round_control"]["privileged_center"] = True
    elif corrupt == "round_variance":
        result["round_control"]["directional_spread"] = "small"
    elif corrupt == "depth":
        round_rows["neutral_torus_to_cap_depth"]["status"] = "DERIVED_XMAX"
    elif corrupt == "squashed_on_shell":
        witnesses["W03_SQUASHED_S3_OFF_SHELL"]["metric_status"] = "ON_SHELL_PHYSICAL"
    elif corrupt == "squashed_band":
        squashed["directional_cut_band"]["status"] = "DERIVED"
    elif corrupt == "physical":
        gates[0]["full_physical_pass"] = "YES"
    elif corrupt == "CMB":
        statuses["CMB_relation_to_directional_band"]["status"] = "DERIVED_CMB_ORIGIN"

    complete = [row for row in families if row["complete_spatial_metric"] == "YES_CONDITIONAL"]
    if (
        result["check_count"] != 50
        or set(result["checks"].values()) != {"PASS"}
        or result["FC_rows"] != 12
        or result["equation_family_rows"] != 28
        or result["solder_family_rows"] != 6
        or result["complete_metric_configuration_classes"] != 2
        or result["complete_on_shell_spatial_metric_witnesses"] != 1
        or result["complete_nonround_off_shell_control_families"] != 1
        or result["complete_nonround_clock_soldered_witnesses"] != 0
        or result["physical_Xmax_pass_count"] != 0
        or len(fc_rows) != 12
        or len({row["completion_id"] for row in fc_rows}) != 12
        or any(row["complete_metric_witness"] != "NO" for row in fc_rows)
        or len(families) != 28
        or len({row["family_id"] for row in families}) != 28
        or len(complete) != 1
        or complete[0]["family_id"] != "B19"
        or len(solder) != 6
        or any(row["physical_Xmax_gate"] != "NO" for row in solder)
        or result["round_control"]["privileged_center"] is not False
        or result["round_control"]["directional_spread"] != "0"
        or result["round_control"]["diameter"] != "pi*b"
        or round_rows["neutral_torus_to_cap_depth"]["status"]
        != "DERIVED_CONDITIONAL_NOT_XMAX"
        or witnesses["W03_SQUASHED_S3_OFF_SHELL"]["metric_status"]
        != "COMPLETE_NONROUND_OFF_SHELL_CONFIGURATION"
        or witnesses["W03_SQUASHED_S3_OFF_SHELL"]["clock_solder"]
        != "NO_CONSTANT_LAPSE_CONTROL"
        or squashed["Hopf_fiber_closed_geodesic"]["exact_result"]
        != "length=2*pi*b*sigma"
        or squashed["horizontal_great_circle"]["exact_result"] != "length=2*pi*b"
        or squashed["directional_cut_band"]["status"] != "OPEN"
        or any(row["full_physical_pass"] != "NO" for row in gates)
        or statuses["complete_nonround_metric_configuration"]["status"]
        != "PRESENT_OFF_SHELL_CONTROL"
        or statuses["current_nonround_directional_band"]["status"]
        != "OPEN_NOT_EVALUABLE"
        or statuses["CMB_relation_to_directional_band"]["status"]
        != "OBSERVATIONAL_COMPARISON_OPEN"
        or statuses["physical_UDT_Xmax"]["status"] != "OPEN_NOT_EVALUABLE"
    ):
        raise AssertionError("science adjudication")
    if (
        independent["status"] != "PASS"
        or independent["check_count"] != 172
        or independent["catch_count"] != 14
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["FC_rows"] != 12
        or independent["equation_family_rows"] != 28
        or independent["solder_family_rows"] != 6
        or independent["source_count"] != 13
    ):
        raise AssertionError("independent verification")
    source_rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv") + read_tsv(
        HERE / "SOURCE_ADDENDUM.tsv"
    )
    for row in source_rows:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("source identity")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 50,
        "independent_checks": 172,
        "independent_catches": 14,
        "FC_rows": 12,
        "equation_family_rows": 28,
        "solder_family_rows": 6,
        "complete_nonround_off_shell_controls": 1,
        "complete_nonround_clock_soldered_witnesses": 0,
        "physical_Xmax_passes": 0,
        "source_identities": 13,
        "result_sha256": hashlib.sha256(
            (HERE / "DERIVATION_RESULT.json").read_bytes()
        ).hexdigest(),
        "independent_sha256": hashlib.sha256(
            (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
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
        "paths": 54,
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
        "command": (
            "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 "
            "python3 -m pytest -q tests/"
        ),
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
        "directional_pair_distance_generic_gates",
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
        "science_center": expect_failure(lambda: validate_science("center")),
        "science_round_variance": expect_failure(lambda: validate_science("round_variance")),
        "science_depth": expect_failure(lambda: validate_science("depth")),
        "science_squashed_on_shell": expect_failure(lambda: validate_science("squashed_on_shell")),
        "science_squashed_band": expect_failure(lambda: validate_science("squashed_band")),
        "science_physical": expect_failure(lambda: validate_science("physical")),
        "science_CMB": expect_failure(lambda: validate_science("CMB")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "current_paths": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")
        ),
        "frontier": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")
        ),
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-directional-pair-distance-repository-gates-1.0",
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
            "squashed_control_promoted_on_shell": False,
            "physical_Xmax_promoted": False,
            "CMB_or_density_fit": False,
            "action_source_carrier_mass_selected": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
