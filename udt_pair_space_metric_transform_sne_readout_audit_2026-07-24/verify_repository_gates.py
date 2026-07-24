#!/usr/bin/env python3
"""Fail-closed science, scope, frozen, navigation, test, and package gates."""

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
BASE = "148f84ea467d9716f8706c161efd45d0a381ecaa"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_scope(injected: str = "") -> list[str]:
    paths = set(git("diff", "--name-only", BASE).splitlines())
    paths.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    if injected:
        paths.add(injected)
    invalid = sorted(
        path for path in paths if path and not path.startswith(PACKAGE + "/")
    )
    if invalid:
        raise AssertionError(f"scope:{invalid[0]}")
    return sorted(path for path in paths if path)


def validate_science(corrupt: str = "") -> dict[str, object]:
    generated = [
        "DERIVATION_RESULT.json",
        "PAIR_METRIC_LEDGER.tsv",
        "COMPOSITION_LEDGER.tsv",
        "READOUT_DISPOSITION.tsv",
        "STATUS_LEDGER.tsv",
        "SNE_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
        "SNE_STDOUT.txt",
        "SNE_STDERR.txt",
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
        "RUN_ENVIRONMENT.json",
    ]
    before = {name: (HERE / name).read_bytes() for name in generated}
    completed = run([sys.executable, "replay_and_capture.py"], cwd=HERE)
    if completed.returncode:
        raise AssertionError(completed.stdout)
    if any((HERE / name).read_bytes() != before[name] for name in generated):
        raise AssertionError("scientific replay not byte-identical")

    derivation = json.loads(
        (HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")
    )
    sne = json.loads((HERE / "SNE_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    pairs = {
        row["candidate"]: row for row in read_tsv(HERE / "PAIR_METRIC_LEDGER.tsv")
    }
    readouts = {
        row["candidate"]: row
        for row in read_tsv(HERE / "READOUT_DISPOSITION.tsv")
    }

    state: dict[str, object] = {
        "selected_profile": independent["ruling"]["selected_profile"],
        "global_Xmax": independent["ruling"]["global_Xmax"],
        "valid_pair_transforms": independent["ruling"]["valid_pair_transforms"],
        "SNe_pair_selection": independent["ruling"]["SNe_pair_profile_selection"],
        "proper_SNe_status": readouts["WRL_PROPER_PAIR_TRANSFORM"]["SNe_status"],
        "B19_SNe_status": readouts["B19_ROUND_PAIR_TRANSFORM"]["SNe_status"],
        "FC12_SNe_status": readouts["FC12_OPEN"]["SNe_status"],
        "Pell_status": readouts["RETIRED_P_ELL"]["SNe_status"],
        "WRL_chi2_dof": sne["scores"]["WRL_AREAL_OPTICAL"]["chi2_dof"],
        "J1_chi2_dof": sne["scores"]["PROJECTIVE_AREAL_J1"]["chi2_dof"],
    }
    mutations = {
        "select": ("selected_profile", "WRL"),
        "xmax": ("global_Xmax", "DERIVED"),
        "count": ("valid_pair_transforms", 2),
        "sne_select": ("SNe_pair_selection", True),
        "proper": ("proper_SNe_status", "EVALUABLE"),
        "b19": ("B19_SNe_status", "EVALUABLE"),
        "fc12": ("FC12_SNe_status", "EVALUABLE"),
        "pell": ("Pell_status", "EVALUABLE"),
        "wrl_score": ("WRL_chi2_dof", 1.0),
        "j1_score": ("J1_chi2_dof", 1.0),
    }
    if corrupt:
        key, value = mutations[corrupt]
        state[key] = value

    if (
        derivation["result"] != "PASS"
        or derivation["check_count"] != 84
        or set(derivation["checks"].values()) != {"PASS"}
        or derivation["source_count"] != 23
        or len(pairs) != 3
        or not all(
            row["pair_metric_status"] == "CONDITIONAL_VALID_METRIC_TRANSFORM"
            for row in pairs.values()
        )
        or state["selected_profile"] != "NONE"
        or state["global_Xmax"] != "OPEN"
        or state["valid_pair_transforms"] != 3
        or state["SNe_pair_selection"] is not False
        or state["proper_SNe_status"] != "NOT_EVALUABLE_AS_PAIR_PROFILE"
        or state["B19_SNe_status"] != "NOT_EVALUABLE"
        or state["FC12_SNe_status"] != "NOT_EVALUABLE"
        or state["Pell_status"] != "PROHIBITED"
        or abs(float(state["WRL_chi2_dof"]) - 0.9098574003059215) > 2e-12
        or abs(float(state["J1_chi2_dof"]) - 2.166501637078457) > 2e-12
        or independent["result"] != "PASS"
        or independent["check_count"] != 107
        or independent["catch_count"] != 9
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS_REJECTED"}
        or sum(
            row["SNe_status"].startswith("EVALUABLE")
            for row in readouts.values()
        )
        != 2
    ):
        raise AssertionError("science adjudication")

    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 84,
        "independent_checks": 107,
        "independent_catches": 9,
        "source_identities": 23,
        "valid_pair_transforms": 3,
        "selected_profile": "NONE",
        "SNe_evaluable_readouts": 2,
        "SNe_pair_profile_selection": False,
        "global_Xmax": "OPEN",
        "derivation_sha256": digest((HERE / "DERIVATION_RESULT.json").read_bytes()),
        "SNe_sha256": digest((HERE / "SNE_RESULT.json").read_bytes()),
        "independent_sha256": digest(
            (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
        ),
        "result": "PASS",
    }


def validate_dirty(corrupt: bool = False) -> dict[str, object]:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=DIRTY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
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
    metadata_sha = digest(completed.stdout)
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or len(completed.stdout.splitlines()) != 54
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
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": digest(completed.stdout.encode()),
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
        "manifest_sha256": digest((HERE / "SHA256SUMS.txt").read_bytes()),
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
        "pair_space_generic_gates",
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
    science_catches = {
        key: expect_failure(lambda key=key: validate_science(key))
        for key in [
            "select",
            "xmax",
            "count",
            "sne_select",
            "proper",
            "b19",
            "fc12",
            "pell",
            "wrl_score",
            "j1_score",
        ]
    }
    catches = {
        "scope": expect_failure(lambda: validate_scope("CANON.md")),
        **{f"science_{key}": value for key, value in science_catches.items()},
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
        "schema": "udt-pair-space-sne-repository-gates-1.0",
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
            "profile_selected": False,
            "pair_metric_identified_with_optical_distance": False,
            "physical_Xmax_promoted": False,
            "BAO_CMB_black_hole_claimed": False,
            "action_source_carrier_selected": False,
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
