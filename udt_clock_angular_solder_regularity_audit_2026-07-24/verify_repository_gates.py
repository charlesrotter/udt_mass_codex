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
BASE = "388d015"
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
        "PAIRING_CLASSIFICATION.tsv",
        "CAP_REGULARITY_LEDGER.tsv",
        "SOLDER_CLASSIFICATION.tsv",
        "OPEN_PROFILE_LEDGER.tsv",
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
    families = read_tsv(HERE / "SOLDER_CLASSIFICATION.tsv")
    by_family = {row["family_id"]: row for row in families}
    pairs = {row["case"]: row for row in read_tsv(HERE / "PAIRING_CLASSIFICATION.tsv")}
    opens = {row["quantity"]: row for row in read_tsv(HERE / "OPEN_PROFILE_LEDGER.tsv")}
    statuses = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}
    addendum = (HERE / "USER_XMAX_DIRECTIONAL_FRAMING_ADDENDUM.md").read_text(
        encoding="utf-8"
    )

    if corrupt == "pass":
        result["compact_same_scalar_pass_count"] = 1
    elif corrupt == "F02":
        by_family["F02"]["compact_two_cap_pass"] = "YES"
    elif corrupt == "F03":
        by_family["F03"]["classification"] = "REPAIRED"
    elif corrupt == "F04":
        by_family["F04"]["classification"] = "UNIQUE_PROFILE"
    elif corrupt == "F06":
        by_family["F06"]["classification"] = "GLOBALLY_OBSTRUCTED"
    elif corrupt == "Xmax":
        statuses["global_Xmax"]["status"] = "DERIVED"
    elif corrupt == "pair":
        pairs["SAME_SIGN_PROPOSED_PAIR"]["ruling"] = "ALLOWED"
    elif corrupt == "endpoint":
        opens["finite_positive_endpoint"]["selected"] = "YES"
    elif corrupt == "CMB":
        addendum = addendum.replace(
            "`OBSERVATIONAL_COMPARISON_OPEN`", "`DERIVED_CMB_ORIGIN`"
        )

    if (
        result["check_count"] != 37
        or set(result["checks"].values()) != {"PASS"}
        or result["family_count"] != 6
        or result["compact_same_scalar_pass_count"] != 0
        or len(families) != 6
        or len(by_family) != 6
        or by_family["F01"]["classification"]
        != "OBSTRUCTED_BOTH_CAPS_CURVATURE_SINGULAR"
        or by_family["F02"]["compact_two_cap_pass"] != "NO"
        or by_family["F03"]["classification"]
        != "OBSTRUCTED_FOR_SMOOTH_POSITIVE_NONZERO_COMMON_FACTOR"
        or by_family["F04"]["classification"] != "OPEN_INFINITE_PROFILE_FAMILY"
        or by_family["F06"]["classification"] != "OPEN_OUTSIDE_BOUNDED_CLASS"
        or pairs["SAME_SIGN_PROPOSED_PAIR"]["ruling"] != "FAILS_FIXED_K_INVARIANCE"
        or opens["finite_positive_endpoint"]["selected"] != "NO"
        or opens["angular_global_diameter"]["selected"] != "NO"
        or statuses["global_Xmax"]["status"] != "OPEN_NOT_EVALUABLE"
        or statuses["same_scalar_globally_impossible_in_UDT"]["status"] != "NOT_DERIVED"
        or result["F01"]["scalar_curvature"]
        != "6/b^2-2/(b^2*kappa^2*sin(2eta)^2)"
        or result["F02"]["minus_regular_kappa"] != "1"
        or result["F02"]["plus_regular_kappa"] != "NONE_FINITE_POSITIVE"
        or result["F04"]["A_over_N"] != "ell*exp(2phi)"
        or "`OBSERVATIONAL_COMPARISON_OPEN`" not in addendum
        or "X_max  = sup over allowed observer pairs (p,q) of d_h(p,q)"
        not in addendum
    ):
        raise AssertionError("science adjudication")
    if (
        independent["status"] != "PASS"
        or independent["check_count"] != 59
        or independent["catch_count"] != 11
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["family_count"] != 6
        or independent["source_count"] != 8
    ):
        raise AssertionError("independent verification")
    for row in read_tsv(HERE / "SOURCE_LINEAGE.tsv"):
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("source identity")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 37,
        "independent_checks": 59,
        "independent_catches": 11,
        "solder_families": 6,
        "compact_same_scalar_passes": 0,
        "source_identities": 8,
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
        "clock_angular_solder_generic_gates",
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
        "science_pass": expect_failure(lambda: validate_science("pass")),
        "science_F02": expect_failure(lambda: validate_science("F02")),
        "science_F03": expect_failure(lambda: validate_science("F03")),
        "science_F04": expect_failure(lambda: validate_science("F04")),
        "science_F06": expect_failure(lambda: validate_science("F06")),
        "science_Xmax": expect_failure(lambda: validate_science("Xmax")),
        "science_pair": expect_failure(lambda: validate_science("pair")),
        "science_endpoint": expect_failure(lambda: validate_science("endpoint")),
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
        "schema": "udt-clock-angular-solder-repository-gates-1.0",
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
            "mass_density_or_CMB_fit": False,
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
