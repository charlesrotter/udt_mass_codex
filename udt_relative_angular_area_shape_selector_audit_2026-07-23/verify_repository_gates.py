#!/usr/bin/env python3
"""Repository gates for the relative angular-area/shape selector audit."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "cabb61a1f943b667fe2c2898531e365265588f05"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_angular_generator_branch_census_2026-07-23"
PREVIOUS_MANIFEST = (
    "8fbdc3cff3cc347a76466721311c5a4be6ad10ee2767127a4a850c06a78c7ccc"
)
MAXIMUM = (
    "THE_COMPLETE_NONBLOCK_METRIC_DEFINES_EXACT_FULL_CSN_INVARIANT_"
    "RELATIVE_ANGULAR_AREA_AND_SHAPE_SPEED_DIAGNOSTICS_BUT_CURRENT_"
    "METRIC_ALGEBRA_RECIPROCITY_CSN_FINITE_CELL_TOPOLOGY_CARTAN_"
    "IDENTITIES_BOOTSTRAP_AND_C_DO_NOT_FIX_THEIR_GLOBAL_TARGET_VALUES__"
    "A_REGULAR_MIRROR_SEAL_FORCES_ZERO_RELATIVE_AREA_RATE_AT_ITS_FIXED_"
    "POINT_BUT_LEAVES_SHAPE_SPEED_AMPLITUDE_AND_BULK_PERSISTENCE_"
    "UNSELECTED"
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
        "relative_angular_previous_gate_chain",
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
    count = len([line for line in manifest.read_text().splitlines() if line])
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
    if len(details) != 96:
        raise generic.GateError("PRIOR", f"package-count:{len(details)}")
    return {"packages": details, "entries": entries, "result": "PASS"}


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text().splitlines()
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


def validate_navigation(generic) -> dict[str, int]:
    saved = generic.PACKAGE
    generic.PACKAGE = "__NO_PACKAGE_MARKDOWN__"
    try:
        result = generic.validate_navigation(ROOT)
    finally:
        generic.PACKAGE = saved

    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = re.sub(r":\d+$", "", target)
            destination = source.parent.joinpath(target).resolve()
            links += 1
            if not destination.exists():
                raise generic.GateError(
                    "NAVIGATION", f"{source.name}:{raw}"
                )
    result["package_links"] = links
    return result


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
    result = json.loads((HERE / "RESULT.json").read_text())
    nonblock = json.loads(
        (HERE / "NONBLOCK_INVARIANT_FORMULA.json").read_text()
    )
    diagnostics = json.loads(
        (HERE / "DIAGNOSTIC_FORMULA.json").read_text()
    )
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text()
    )
    tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    selectors = read_tsv(HERE / "SELECTOR_RULING_MATRIX.tsv")
    universe = read_tsv(HERE / "SELECTOR_UNIVERSE.tsv")
    endpoints = read_tsv(HERE / "ENDPOINT_FLAT_COUNTERFAMILY.tsv")
    seals = read_tsv(HERE / "SEAL_DIAGNOSTIC_ATLAS.tsv")
    joins = read_tsv(HERE / "JOIN_LEDGER.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")

    for row in lineage:
        source = ROOT / row["path"]
        if (
            not source.is_file()
            or digest(source) != row["sha256"]
            or source.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source lineage changed")

    counts = result["counts"]
    selector_ids = [row["selector_id"] for row in selectors]
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or nonblock["orthogonal_angular_metric"] != "q=Q-C^T*h^-1*C"
        or not nonblock["cross_terms_retained"]
        or nonblock["raw_Q_is_invariant_angular_metric"]
        or diagnostics["joint_target"] != "w_p=0 AND S_shape=1"
        or diagnostics["relative_area_rate"] != "A_rel=w_p"
        or diagnostics["shape_speed_squared"]
        != "S_shape=u_p**2+theta_p**2*sinh(2*u)**2"
        or not diagnostics["c_in_complete_reciprocal_metric"]
        or counts["selectors"] != 11
        or counts["area_global_derivations"] != 0
        or counts["shape_global_derivations"] != 0
        or counts["joint_global_derivations"] != 0
        or counts["seal_local_area_derivations"] != 1
        or counts["endpoint_flat_controls"] != 7
        or counts["seal_lift_rows"] != 5
        or counts["sources"] != 17
        or counts["joins"] != 8
        or counts["catch_proofs"] != 24
        or counts["complete_on_shell_g_phi_branches"] != 0
        or len(selectors) != 11
        or len(universe) != 11
        or selector_ids != [row["selector_id"] for row in universe]
        or any(row["joint_ruling"] == "DERIVES_GLOBAL" for row in selectors)
        or selectors[4]["area_ruling"] != "DERIVES_AT_FIXED_SEAL_ONLY"
        or selectors[4]["shape_ruling"] != "CONSTRAINS_NOT_FIXES"
        or selectors[8]["joint_ruling"] != "NOT_AN_EQUATION"
        or len(endpoints) != 7
        or len(seals) != 5
        or {row["relative_area_at_fixed_seal"] for row in seals[:4]}
        != {"ZERO"}
        or len(joins) != 8
        or len(catches) != 24
        or len(lineage) != 17
        or any(row["status"] != "CAUGHT" for row in catches)
        or independent["status"] != "PASS"
        or independent["mutation_catches"] != 24
        or independent["rational_nonblock_controls"] != 3
        or not independent["three_independent_bulk_knobs"]
        or independent["mirror_dimensions"]
        != {
            "ANGULAR_MINUS_I": 0,
            "ANGULAR_PLUS_I": 0,
            "AXIS_EXCHANGE": 1,
            "AXIS_REFLECTION": 1,
        }
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
        or "forces the relative angular-area rate to vanish" not in report
    ):
        raise AssertionError("relative-angular science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "selectors": len(selectors),
        "area_global_derivations": 0,
        "shape_global_derivations": 0,
        "joint_global_derivations": 0,
        "seal_local_area_derivations": 1,
        "complete_on_shell_g_phi_branches": 0,
        "source_files": len(lineage),
        "production_mutation_catches": len(catches),
        "independent_mutation_catches": independent["mutation_catches"],
        "grade": "VERIFIED-WITH-CAVEATS",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "relative_angular_generic_gates",
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
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = load(
        ROOT
        / "hygiene_baseline_correction_2026-07-23"
        / "verify_repository_gates.py",
        "relative_angular_hygiene_gates",
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
        "schema": (
            "udt-relative-angular-area-shape-selector-repository-gates-1.0"
        ),
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
