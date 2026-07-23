#!/usr/bin/env python3
"""Repository gates for the three-reciprocity Delta-K audit."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "51a355a746fab82baa9760ceaf564f20ab2e1099"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_angular_bulk_jacobi_selector_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "b348e768e4c11b2cef951d8ded26f770391a06178a12b9d0d75386d71214b9ff"
)
MAXIMUM = (
    "CURRENT_RECIPROCITIES_SUPPLY_A_REFERENCE_SOURCE_AND_COVARIANT_"
    "OBSTRUCTION;UNDER_ADDED_HOMOGENEITY_CENTRALITY_AND_TWO_SEAL_"
    "PREMISES_THE_OPEN_TENSOR_SEAM_REDUCES_TO_ONE_DIMENSIONLESS_SCALAR_"
    "LAMBDA_BUT_LAMBDA_EQUALS_ONE_REMAINS_OPEN"
)


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replay_prior(generic, corrupt: bool = False) -> dict[str, object]:
    previous = load(
        ROOT / PREVIOUS / "verify_repository_gates.py",
        "three_reciprocity_previous_gate_chain",
    )
    result = previous.replay_prior(generic, corrupt)
    details = list(result["packages"])
    entries = int(result["entries"])
    manifest = ROOT / PREVIOUS / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PREVIOUS_MANIFEST:
        raise generic.GateError("PRIOR", PREVIOUS + ":manifest")
    replay = generic.run(
        manifest.parent, ["sha256sum", "--check", manifest.name]
    )
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PRIOR", PREVIOUS + ":replay")
    count = len(
        [line for line in manifest.read_text(encoding="utf-8").splitlines()
         if line]
    )
    details.append(
        {
            "package": PREVIOUS,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": count,
            "result": "PASS",
        }
    )
    entries += count
    if len(details) != 98:
        raise generic.GateError("PRIOR", f"package-count:{len(details)}")
    return {"packages": details, "entries": entries, "result": "PASS"}


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
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name not in excluded
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def validate_dirty_head(generic) -> dict[str, str]:
    head = subprocess.check_output(
        ["git", "-C", str(DIRTY), "rev-parse", "HEAD"], text=True
    ).strip()
    branch = subprocess.check_output(
        ["git", "-C", str(DIRTY), "branch", "--show-current"], text=True
    ).strip()
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
    ):
        raise generic.GateError("DIRTY", f"{head}:{branch}")
    return {"head": head, "branch": branch}


def validate_science() -> dict[str, object]:
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    covariance = json.loads(
        (HERE / "RECIPROCITY_COVARIANCE.json").read_text(encoding="utf-8")
    )
    xmax = json.loads(
        (HERE / "XMAX_GROUP_ENDPOINTS.json").read_text(encoding="utf-8")
    )
    flow = json.loads(
        (HERE / "CONSTANT_LAMBDA_RICCATI.json").read_text(encoding="utf-8")
    )
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    tests = json.loads(
        (HERE / "FULL_TEST_RESULT.json").read_text(encoding="utf-8")
    )
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    routes = read_tsv(HERE / "ROUTE_RULING_MATRIX.tsv")
    universe = read_tsv(HERE / "ROUTE_UNIVERSE.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    counters = read_tsv(HERE / "COUNTERFAMILY_ATLAS.tsv")
    joins = read_tsv(HERE / "JOIN_LEDGER.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    roles = read_tsv(HERE / "THREE_RECIPROCITY_ROLE_MAP.tsv")

    for row in lineage:
        source = ROOT / row["path"]
        if not source.is_file() or digest(source) != row["sha256"]:
            raise AssertionError("source lineage drift")

    lambda_witnesses = {
        row["lambda"]: row["S_shape"] for row in flow["witnesses"]
    }
    route_ids = [row["route_id"] for row in routes]
    if (
        result["base_commit"] != BASE
        or result["maximum_conclusion"] != MAXIMUM
        or result["native_closure"] is not False
        or result["current_registered_composition"]["Delta_K_zero"]
        != "NOT_DERIVED"
        or result["current_registered_composition"][
            "two_regular_mirror_seals"
        ] != "NOT_DERIVED"
        or result["strongest_charitable_composition"]["remaining_seam"]
        != "lambda=1"
        or covariance["reference_source"] != "K_rec=-L^2=-I"
        or covariance["zero_is_forced_by_covariance"] is not False
        or covariance["central_survivor"] != "Delta_K=mu*I"
        or xmax["status"] != "CHOSE_CONDITIONAL_NOT_UNIQUE"
        or xmax["position_field_join"] != "OPEN_NOT_CERTIFIED"
        or xmax["opposite_endpoints_composable"] is not False
        or xmax["endpoints_are_regular_mirror_seals"] is not False
        or flow["riccati_residual"] != "EXACT_ZERO"
        or flow["second_nontrivial_area_seal_condition"]
        != "s^2=lambda^2"
        or flow["matched_flow_shape"] != "lambda^2"
        or flow["two_seals_force_lambda_one"] is not False
        or lambda_witnesses.get("2") != "4"
        or lambda_witnesses.get("3") != "9"
        or len(routes) != 14
        or len(universe) != 14
        or route_ids != [row["route_id"] for row in universe]
        or any(row["ruling"] == "DERIVES_MISSING_PREMISE"
               for row in routes)
        or len(statuses) != 14
        or len(counters) != 4
        or len(joins) != 15
        or len(catches) != 18
        or any(row["result"] != "PASS_REJECTED" for row in catches)
        or len(lineage) != 20
        or len(roles) != 3
        or independent["all_checks_pass"] is not True
        or independent["catch_count"] != 18
        or independent["catch_pass_count"] != 18
        or independent["lambda_flow_checks"] != 32
        or independent["source_hash_checks"] != 20
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
        or "lambda=1" not in report
        or "two regular reciprocal mirror seals" not in report
    ):
        raise AssertionError("three-reciprocity science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "native_closure": False,
        "routes": len(routes),
        "sources": len(lineage),
        "counterfamilies": len(counters),
        "joins": len(joins),
        "production_catches": len(catches),
        "independent_catches": independent["catch_pass_count"],
        "lambda_flow_checks": independent["lambda_flow_checks"],
        "smallest_conditional_seam": "lambda=1",
        "grade": "VERIFIED-WITH-CAVEATS",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "three_reciprocity_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = [
        path
        for path in generic.validate_scope(ROOT)
        if path != f"{PACKAGE}/REPOSITORY_GATES.json"
    ]
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = load(
        ROOT
        / "hygiene_baseline_correction_2026-07-23"
        / "verify_repository_gates.py",
        "three_reciprocity_hygiene_gates",
    ).validate_tests(generic)
    science = validate_science()
    package = validate_package(generic)
    catches = {
        "scope": generic.expect(
            "SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")
        ),
        "frozen": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, True)
        ),
        "prior": generic.expect(
            "PRIOR", lambda: replay_prior(generic, True)
        ),
        "current_paths": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "current"),
        ),
        "frontier": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "frontier"),
        ),
        "dirty": generic.expect(
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)
        ),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, True)
        ),
    }
    output = {
        "schema": "udt-three-reciprocity-repository-gates-1.0",
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
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": MAXIMUM,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
