#!/usr/bin/env python3
"""Fail-closed relational-depth and repository verification."""

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
BASE = "bc5a0a9"
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
        "DEPTH_TYPE_RULING_LEDGER.tsv",
        "COMPOSITION_DOMAIN_LEDGER.tsv",
        "ROUND_PAIR_CONTROL_LEDGER.tsv",
        "SCALE_GATE.tsv",
        "STATUS_LEDGER.tsv",
        "OWNER_FRAME_LEDGER.tsv",
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
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    depth = {row["id"]: row for row in read_tsv(HERE / "DEPTH_TYPE_RULING_LEDGER.tsv")}
    composition = {row["domain"]: row for row in read_tsv(HERE / "COMPOSITION_DOMAIN_LEDGER.tsv")}
    round_rows = {row["quantity"]: row for row in read_tsv(HERE / "ROUND_PAIR_CONTROL_LEDGER.tsv")}
    scales = {row["object"]: row for row in read_tsv(HERE / "SCALE_GATE.tsv")}
    statuses = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}
    owner = {row["claim"]: row for row in read_tsv(HERE / "OWNER_FRAME_LEDGER.tsv")}

    if corrupt == "scalar":
        depth["D03"]["status"] = "DERIVED_UNIVERSAL"
    elif corrupt == "observer":
        depth["D02"]["status"] = "OPEN"
    elif corrupt == "linear":
        composition["universal continuous F of proper distance"]["result"] = "NONLINEAR_ALLOWED"
    elif corrupt == "angular":
        composition["noncollinear round triples"]["result"] = "SCALAR_DEPTHS_SUFFICIENT"
    elif corrupt == "cut":
        result["cut_locus"]["scalar_distance"] = "PATH_FAMILY"
    elif corrupt == "transport":
        result["cut_locus"]["full_transport"] = "UNIQUE"
    elif corrupt == "scale":
        scales["c and inverse-c"]["status"] = "DEPTH_NORMALIZATION_DERIVED"
    elif corrupt == "Xmax":
        statuses["physical Xmax mass density CMB"]["status"] = "DERIVED"
    elif corrupt == "local":
        result["owner_frame"]["local_physics_modified_by_pair_dilation"] = True
    elif corrupt == "three":
        result["owner_frame"]["three_observer_result"] = "DILATION_REFUTED"

    if (
        result["check_count"] != 76
        or set(result["checks"].values()) != {"PASS"}
        or result["source_count"] != 10
        or result["owner_frame"]["classification"] != "OWNER_CLARIFIED_RELATIONAL_ONLY"
        or result["owner_frame"]["rho_p_p"] != "0_FOR_EVERY_OBSERVER"
        or result["owner_frame"]["local_physics_modified_by_pair_dilation"] is not False
        or result["owner_frame"]["three_observer_result"] != "PAIRWISE_DILATIONS_COMPATIBLE"
        or result["global_scalar_theorem"]["status"]
        != "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH"
        or result["smallest_surviving_type"]["type"]
        != "OBSERVER_INDEXED_BILOCAL_METRIC_FAMILY"
        or result["composition"]["ordinary_geodesic_universal_F"] != "LINEAR_ONLY"
        or result["composition"]["noncollinear_composition"] != "REQUIRES_ANGULAR_DATUM"
        or result["cut_locus"]["scalar_distance"] != "SINGLE_VALUED"
        or result["cut_locus"]["full_transport"] != "PATH_FAMILY"
        or result["scale"]["dimensionless_depth_normalization_from_c_alone"] != "NOT_DERIVED"
        or len(depth) != 8
        or depth["D02"]["status"] != "SMALLEST_SURVIVING_METRIC_NATIVE_TYPE_GIVEN_F"
        or depth["D03"]["status"] != "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH"
        or depth["D06"]["status"] != "EXACT_CONDITIONAL_DISPLAY_NOT_METRIC_DISTANCE_IDENTITY"
        or len(composition) != 6
        or composition["universal continuous F of proper distance"]["result"] != "FORCES_F_EQUAL_KAPPA_D"
        or composition["noncollinear round triples"]["result"] != "ANGULAR_DATUM_REQUIRED"
        or len(round_rows) != 7
        or round_rows["antipodal distance"]["consequence"] != "scalar distance unique at cut"
        or len(scales) != 4
        or scales["c and inverse-c"]["status"]
        != "FOUNDING_SCALE_CONVERSION_NOT_DEPTH_NORMALIZATION_ALONE"
        or len(statuses) != 12
        or statuses["pair dilation modifies local physics"]["status"]
        != "REFUTED_BY_OWNER_FRAME_MEANING"
        or statuses["three observers invalidate pair dilation"]["status"] != "REFUTED"
        or statuses["physical Xmax mass density CMB"]["status"] != "OPEN_NOT_PROMOTED"
        or len(owner) != 5
        or owner["observer self-depth"]["owner_meaning"] != "rho_p(p)=0"
        or owner["dilation ontology"]["classification"] != "OWNER_CLARIFIED_RELATIONAL_ONLY"
    ):
        raise AssertionError("science adjudication")
    if (
        independent["result"] != "PASS"
        or independent["check_count"] != 68
        or independent["catch_count"] != 14
        or set(independent["checks"].values()) != {"PASS"}
        or set(independent["catches"].values()) != {"PASS"}
        or independent["ruling"]["global_scalar"]
        != "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH"
        or independent["ruling"]["angular_composition"] != "REQUIRED"
        or independent["ruling"]["physical_Xmax"] != "OPEN"
        or independent["ruling"]["owner_frame"] != "RELATIONAL_ONLY_LOCAL_NEUTRAL"
    ):
        raise AssertionError("independent verification")
    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv") + read_tsv(HERE / "SOURCE_ADDENDUM.tsv")
    if len(sources) != 10 or len({row["id"] for row in sources}) != 10:
        raise AssertionError("source census")
    for row in sources:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError("source identity")
    return {
        "deterministic_replay": "BYTE_IDENTICAL",
        "production_checks": 76,
        "independent_checks": 68,
        "independent_catches": 14,
        "source_identities": 10,
        "owner_frame": "RELATIONAL_ONLY_LOCAL_NEUTRAL",
        "global_scalar": "REFUTED_SCOPED",
        "smallest_surviving_type": "OBSERVER_INDEXED_BILOCAL_METRIC_FAMILY_GIVEN_F",
        "ordinary_additive_F": "LINEAR_ONLY",
        "angular_composition": "REQUIRED",
        "physical_Xmax": "OPEN",
        "result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "independent_sha256": hashlib.sha256((HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()).hexdigest(),
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
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=DIRTY, stdout=subprocess.PIPE, check=True).stdout.decode().strip()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=DIRTY, stdout=subprocess.PIPE, check=True).stdout.decode().strip()
    if corrupt:
        branch = "main"
    metadata_sha = hashlib.sha256(status.stdout).hexdigest()
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
        or len(status.stdout.splitlines()) != 54
        or metadata_sha != "4bc96070c841a14c497b642ee7b93dcf9061372f770aee065d6b495ee4996f4c"
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
        if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    )
    if sorted(entries) != actual:
        raise AssertionError("package coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": hashlib.sha256((HERE / "SHA256SUMS.txt").read_bytes()).hexdigest(),
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
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19" / "verify_repository_gates.py",
        "relational_pair_depth_generic_gates",
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
        "science_scalar": expect_failure(lambda: validate_science("scalar")),
        "science_observer": expect_failure(lambda: validate_science("observer")),
        "science_linear": expect_failure(lambda: validate_science("linear")),
        "science_angular": expect_failure(lambda: validate_science("angular")),
        "science_cut": expect_failure(lambda: validate_science("cut")),
        "science_transport": expect_failure(lambda: validate_science("transport")),
        "science_scale": expect_failure(lambda: validate_science("scale")),
        "science_Xmax": expect_failure(lambda: validate_science("Xmax")),
        "science_local": expect_failure(lambda: validate_science("local")),
        "science_three": expect_failure(lambda: validate_science("three")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, corrupt=True)),
        "current_paths": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, corrupt="frontier")),
        "dirty": expect_failure(lambda: validate_dirty(True)),
        "package": expect_failure(lambda: validate_package(True)),
    }
    output = {
        "schema": "udt-relational-pair-depth-repository-gates-1.0",
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
            "F_profile_selected": False,
            "observer_chart_transition_selected": False,
            "local_physics_modified_by_pair_dilation": False,
            "three_observer_dilation_refuted": False,
            "physical_Xmax_promoted": False,
            "mass_density_or_CMB_promoted": False,
            "action_source_carrier_selected": False,
            "gpu_work": False,
            "repository_reorganization": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
