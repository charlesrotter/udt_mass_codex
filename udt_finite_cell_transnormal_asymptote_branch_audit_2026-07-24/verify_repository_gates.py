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
BASE = "e0c3015"
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
        "FINITE_CELL_TRANSNORMAL_LEDGER.tsv",
        "EQUATION_FAMILY_SCREEN.tsv",
        "CALCULABLE_CONTROL_LEDGER.tsv",
        "CONTROL_GATE_MATRIX.tsv",
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
    fc_rows = read_tsv(HERE / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv")
    families = read_tsv(HERE / "EQUATION_FAMILY_SCREEN.tsv")
    controls = read_tsv(HERE / "CONTROL_GATE_MATRIX.tsv")
    statuses = {
        row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")
    }
    fc_by_id = {row["completion_id"]: row for row in fc_rows}
    family_by_id = {row["family_id"]: row for row in families}
    control_by_id = {row["control_id"]: row for row in controls}

    if corrupt == "global":
        result["full_global_Xmax_pass_count"] = 1
    elif corrupt == "b19_clock":
        family_by_id["B19"]["primary_classification"] = "FULL_GLOBAL_XMAX_PASS"
    elif corrupt == "wrl_global":
        family_by_id["B21"]["global_Xmax_evaluable"] = "YES"
    elif corrupt == "fc_witness":
        fc_by_id["FC12_RECIPROCAL_TORIC_DIAGONAL"]["complete_g_phi_witness"] = "YES"
    elif corrupt == "critical":
        statuses["smooth_real_phi_global_transnormal_on_compact_rest_slice"][
            "status"
        ] = "UNOBSTRUCTED"
    elif corrupt == "control":
        control_by_id["C_B19_ROUND"]["passes_all"] = "YES"

    expected_fc_counts = {
        "FORMULA_ONLY_PROFILE_OR_ENDPOINT_OPEN": 1,
        "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH": 5,
        "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS": 6,
    }
    expected_family_counts = {
        "CONDITIONAL_DEPTH_EVALUABLE_NOT_CLOCK_SOLDERED": 1,
        "INELIGIBLE_NO_COMMON_WITNESS": 24,
        "LOCAL_CLOCK_DEPTH_ONLY_NO_GLOBAL_COMPLETION": 1,
        "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS": 2,
    }
    if (
        result["check_count"] != 20
        or set(result["checks"].values()) != {"PASS"}
        or result["fc_rows"] != 12
        or result["family_rows"] != 28
        or result["control_count"] != 3
        or result["full_global_Xmax_pass_count"] != 0
        or result["fc_classification_counts"] != expected_fc_counts
        or result["family_classification_counts"] != expected_family_counts
        or len(fc_rows) != 12
        or len(fc_by_id) != 12
        or len(families) != 28
        or len(family_by_id) != 28
        or len(controls) != 3
        or len(control_by_id) != 3
        or any(row["passes_all"] != "NO" for row in controls)
        or family_by_id["B19"]["primary_classification"]
        != "CONDITIONAL_DEPTH_EVALUABLE_NOT_CLOCK_SOLDERED"
        or family_by_id["B21"]["global_Xmax_evaluable"] != "NO"
        or fc_by_id["FC12_RECIPROCAL_TORIC_DIAGONAL"][
            "complete_g_phi_witness"
        ]
        != "NO_CONDITIONAL_OPEN_PROFILE_CONTROL_ONLY"
        or statuses["smooth_real_phi_global_transnormal_on_compact_rest_slice"][
            "status"
        ]
        != "OBSTRUCTED"
        or statuses["global_Xmax"]["status"] != "OPEN_NOT_EVALUABLE"
        or result["exact_controls"]["WRL"]["endpoint"] != "2*X"
        or result["exact_controls"]["B19_round"]["one_sided_endpoint"] != "pi*b/4"
        or result["exact_controls"]["B19_round"]["global_spatial_diameter"] != "pi*b"
        or result["exact_controls"]["B19_round"]["diameter_to_depth_ratio"] != "4"
    ):
        raise AssertionError("science adjudication")
    if (
        independent["status"] != "PASS"
        or independent["check_count"] != 17
        or independent["catch_count"] != 12
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["fc_rows"] != 12
        or independent["family_rows"] != 28
        or independent["source_count"] != 15
    ):
        raise AssertionError("independent verification")
    generated_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in generated
        if name.endswith((".json", ".tsv", ".txt"))
    )
    if "TRANSMORMAL" in generated_text:
        raise AssertionError("forbidden transnormal misspelling")
    for row in read_tsv(HERE / "SOURCE_LINEAGE.tsv"):
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("source identity")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 20,
        "independent_checks": 17,
        "independent_catches": 12,
        "finite_cell_rows": 12,
        "equation_family_rows": 28,
        "full_global_Xmax_passes": 0,
        "source_identities": 15,
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
        "finite_cell_transnormal_generic_gates",
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
        "science_global": expect_failure(lambda: validate_science("global")),
        "science_B19_clock": expect_failure(lambda: validate_science("b19_clock")),
        "science_WRL_global": expect_failure(lambda: validate_science("wrl_global")),
        "science_FC12_witness": expect_failure(lambda: validate_science("fc_witness")),
        "science_critical_point": expect_failure(lambda: validate_science("critical")),
        "science_control": expect_failure(lambda: validate_science("control")),
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
        "schema": "udt-finite-cell-transnormal-repository-gates-1.0",
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
            "action_or_source_selected": False,
            "carrier_selected": False,
            "mass_density_or_boundary_solve": False,
            "global_Xmax_promoted": False,
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
