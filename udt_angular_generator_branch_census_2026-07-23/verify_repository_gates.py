#!/usr/bin/env python3
"""Repository gates for the angular-generator complete-branch census."""

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
BASE = "863c2c879e7d1aad351ffc0e456dafcb93a97e98"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_reciprocal_angular_intertwiner_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "604f382c42324b05e31c555c35bf57ab7f22b45bbc654ae6552f9f85844028cb"
)
MAXIMUM = (
    "THE_FULL_METRIC_ANGULAR_STRAIN_MATCHES_THE_RECIPROCAL_MINUS1_PLUS1_"
    "SPECTRUM_IFF_ITS_RELATIVE_MEAN_SCALE_RATE_VANISHES_AND_ITS_CSN_SHAPE_"
    "SPEED_HAS_UNIT_MAGNITUDE__THE_REGISTERED_FC12_PROFILE_SUPPLIES_AN_"
    "EXACT_CONSTANT_RELATIVE_SCALE_SUBFAMILY_BUT_ARBITRARY_OMEGA_TOPOLOGY_"
    "SEAL_MONODROMY_AND_CURRENT_BOOTSTRAP_DO_NOT_FORCE_OR_SELECT_IT"
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
        "angular_generator_previous_gate_chain",
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
    if len(details) != 95:
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
    formula = json.loads((HERE / "ANGULAR_GENERATOR_FORMULA.json").read_text())
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text()
    )
    tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    branches = read_tsv(HERE / "BRANCH_GENERATOR_ATLAS.tsv")
    universe = read_tsv(HERE / "BRANCH_UNIVERSE.tsv")
    points = read_tsv(HERE / "POINTWISE_GENERATOR_CONTROLS.tsv")
    mirrors = read_tsv(HERE / "MIRROR_LIFT_GENERATOR_ATLAS.tsv")
    monodromy = read_tsv(HERE / "MONODROMY_GENERATOR_ATLAS.tsv")
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
    rulings = result["branch_ruling_counts"]
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or formula["reciprocal_predicate"]
        != "w_p=0 AND sigma_squared=1"
        or formula["complete_metric_determinant"] != "-c**2*exp(4*w)"
        or counts["completion_families"] != 12
        or counts["pointwise_controls"] != 10
        or counts["mirror_lifts"] != 5
        or counts["monodromy_controls"] != 9
        or counts["joins"] != 9
        or counts["sources"] != 15
        or counts["catch_proofs"] != 20
        or counts["forced_persistent_unconditional_families"] != 0
        or counts["conditional_persistent_regular_families"] != 0
        or counts["complete_on_shell_g_phi_branches"] != 0
        or rulings
        != {
            "ALLOWED_NOT_FORCED": 4,
            "INSUFFICIENT_METRIC_DATA": 1,
            "UNDEFINED_AT_REQUIRED_STRATUM": 7,
        }
        or independent["status"] != "PASS"
        or independent["mutation_catches"] != 20
        or len(branches) != 12
        or len(universe) != 12
        or [row["completion_id"] for row in branches]
        != [row["completion_id"] for row in universe]
        or any(row["pattern_forced"] != "NO" for row in branches)
        or len(points) != 10
        or len(mirrors) != 5
        or len(monodromy) != 9
        or len(joins) != 9
        or len(catches) != 20
        or len(lineage) != 15
        or any(row["status"] != "CAUGHT" for row in catches)
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
        or "Correction made before banking" not in report
    ):
        raise AssertionError("angular-generator science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "completion_families": len(branches),
        "branch_ruling_counts": rulings,
        "forced_persistent_unconditional_families": 0,
        "complete_on_shell_g_phi_branches": 0,
        "relative_mean_gate": "w_p=0",
        "shape_gate": "sigma_squared=1",
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
        "angular_generator_generic_gates",
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
        "angular_generator_hygiene_gates",
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
        "schema": "udt-angular-generator-branch-census-repository-gates-1.0",
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
