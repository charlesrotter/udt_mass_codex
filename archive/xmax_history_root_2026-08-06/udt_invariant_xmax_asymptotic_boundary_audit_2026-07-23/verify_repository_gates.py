#!/usr/bin/env python3
"""Repository gates for the invariant-Xmax asymptotic-boundary audit."""

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
BASE = "4b85bb2d4b17f146585b3f32d9f0f570f9966492"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_three_reciprocity_delta_k_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "5e96426627e86abdb27fab0399e2461358dda273e22c18034e54d86f1eaa95e8"
)
MAXIMUM = (
    "UNIVERSAL_UNATTAINABLE_XMAX_IS_A_COHERENT_UDT_WORKING_POSITIONAL_"
    "LIMIT_AND_REPLACES_THE_TWO_REGULAR_SEAL_PICTURE;THE_DECLARED_"
    "OBSERVER_ACTIONS_ARE_ALL_TRANSLATION_CONJUGATES;TANH_IS_UNIQUE_ONLY_"
    "IN_THE_ADDED_ANCHORED_FIRST_DEGREE_PROJECTIVE_CLASS;THE_METRIC_"
    "DISTINGUISHES_COORDINATE_PROPER_AND_OPTICAL_REACH_BUT_DOES_NOT_YET_"
    "SELECT_THE_POSITION_READOUT_OR_LAMBDA"
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
        for piece in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(piece)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replay_prior(generic, corrupt: bool = False) -> dict[str, object]:
    previous = load(
        ROOT / PREVIOUS / "verify_repository_gates.py",
        "invariant_xmax_previous_gate_chain",
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
    if len(details) != 99:
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
    interval = json.loads(
        (HERE / "INTERVAL_ACTION_CLASSIFICATION.json").read_text(
            encoding="utf-8"
        )
    )
    projective = json.loads(
        (HERE / "PROJECTIVE_CLASS_RESULT.json").read_text(encoding="utf-8")
    )
    wrl = json.loads(
        (HERE / "WRL_DISTANCE_RESULT.json").read_text(encoding="utf-8")
    )
    coframe = json.loads(
        (HERE / "COFRAME_REPARAMETRIZATION_RESULT.json").read_text(
            encoding="utf-8"
        )
    )
    lambdas = json.loads(
        (HERE / "ONE_BOUNDARY_LAMBDA_RESULT.json").read_text(
            encoding="utf-8"
        )
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
    readouts = read_tsv(HERE / "OPERATIONAL_READOUT_ATLAS.tsv")
    boundaries = read_tsv(HERE / "BOUNDARY_ROLE_LEDGER.tsv")
    completeness = read_tsv(HERE / "COMPLETENESS_SCOPE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")

    for row in lineage:
        source = ROOT / row["path"]
        if not source.is_file() or digest(source) != row["sha256"]:
            raise AssertionError("source lineage drift")

    route_ids = [row["route_id"] for row in routes]
    if (
        result["base_commit"] != BASE
        or result["maximum_conclusion"] != MAXIMUM
        or result["native_position_law_closed"] is not False
        or result["lambda_closed"] is not False
        or result["boundary_regrade"]["two_regular_Xmax_seals"]
        != "WITHDRAWN_IN_THIS_FRAMING"
        or result["position_phi_result"]["unique_operational_position"]
        != "NOT_DERIVED"
        or interval["endpoints_in_domain"] is not False
        or interval["physical_distance_signed"] is not False
        or interval["tanh_unique_from_invariant_bound_group_reversal_slope"]
        is not False
        or len(interval["compactifications"]) != 4
        or projective["status"]
        != "DERIVED_CONDITIONAL_ON_FIRST_DEGREE_PROJECTIVE_READOUT"
        or projective["physical_readout_premise"] != "OPEN_NOT_DERIVED"
        or wrl["coordinate_reach"] != "X"
        or wrl["proper_reach"] != "2X"
        or wrl["optical_reach"] != "INFINITE"
        or wrl["three_readouts_equal"] is not False
        or wrl["witness"] != {
            "projective_tanh": "3/5",
            "coordinate_fraction": "3/4",
            "proper_fraction": "1/2",
        }
        or coframe["exact_residual"] != "ZERO"
        or coframe["coframe_selects_H"] is not False
        or lambdas["global_nonsingular_range"] != "0<=s<=lambda"
        or lambdas["lambda_one_selected"] is not False
        or lambdas["display_H_enters_equations"] is not False
        or len(routes) != 16
        or len(universe) != 16
        or route_ids != [row["route_id"] for row in universe]
        or any(row["ruling"] == "DERIVES_UNIQUE_POSITION_LAW"
               for row in routes)
        or len(statuses) != 16
        or len(readouts) != 5
        or len(boundaries) != 7
        or len(completeness) != 11
        or len(catches) != 20
        or any(row["result"] != "PASS_REJECTED" for row in catches)
        or len(lineage) != 20
        or independent["all_checks_pass"] is not True
        or independent["catch_count"] != 20
        or independent["catch_pass_count"] != 20
        or independent["interval_action_checks"] != 13
        or independent["lambda_checks"] != 40
        or independent["source_hash_checks"] != 20
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
        or "1-exp(-2phi)" not in report
        or "Which exact metric observable is X/Xmax?" not in report
    ):
        raise AssertionError("invariant-Xmax science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "native_position_law_closed": False,
        "lambda_closed": False,
        "routes": len(routes),
        "sources": len(lineage),
        "readouts": len(readouts),
        "production_catches": len(catches),
        "independent_catches": independent["catch_pass_count"],
        "interval_action_checks": independent["interval_action_checks"],
        "lambda_checks": independent["lambda_checks"],
        "boundary_regrade": "ONE_ASYMPTOTIC_LIMIT",
        "grade": "VERIFIED-WITH-CAVEATS",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "invariant_xmax_generic_gates",
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
        "invariant_xmax_hygiene_gates",
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
        "schema": "udt-invariant-xmax-repository-gates-1.0",
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
