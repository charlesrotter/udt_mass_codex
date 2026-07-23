#!/usr/bin/env python3
"""Repository gates for the reciprocal-angular intertwiner audit."""

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
BASE = "0d7b06d3e175cfd0a39cce79ebf5f1eef06c50ca"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_reciprocal_seam_descent_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "edb261f17ba31ecbd53cc75bdf78092ff120c18e864694f41af0167a942bbc2d"
)
MAXIMUM = (
    "NONBLOCK_RECIPROCAL_ANGULAR_INTERTWINERS_EXIST_EXACTLY_FOR_MATCHED_"
    "REPRESENTATIONS_BUT_THE_COMPLETE_METRIC_RECIPROCITY_CSN_C_ANCHOR_"
    "SEAL_AND_FINITE_CELL_DO_NOT_SELECT_THE_MATCH__C_FIXES_CLOCK_RULER_"
    "CONVERSION_NOT_ANGULAR_NORMALIZATION"
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
        "intertwiner_previous_gate_chain",
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
    if len(details) != 94:
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
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text()
    )
    tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(
        encoding="utf-8"
    )
    generators = read_tsv(HERE / "GENERATOR_INTERTWINER_ATLAS.tsv")
    bilinears = read_tsv(HERE / "BILINEAR_CROSS_INVARIANT_ATLAS.tsv")
    seals = read_tsv(HERE / "SEAL_INTERTWINER_ATLAS.tsv")
    combined = read_tsv(HERE / "COMBINED_DIHEDRAL_INTERTWINER_ATLAS.tsv")
    combined_bilinear = read_tsv(
        HERE / "COMBINED_DIHEDRAL_BILINEAR_ATLAS.tsv"
    )
    witnesses = read_tsv(HERE / "CONDITIONAL_NONBLOCK_WITNESSES.tsv")
    completions = read_tsv(HERE / "COMPLETION_SOLDERING_ATLAS.tsv")
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
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or counts["continuous_generator_cases"] != 10
        or counts["bilinear_cross_cases"] != 10
        or counts["seal_cases"] != 5
        or counts["combined_pair_cases"] != 5
        or counts["combined_bilinear_pair_cases"] != 5
        or counts["conditional_complete_metric_witnesses"] != 3
        or counts["completion_rows"] != 12
        or counts["complete_g_phi_witnesses"] != 0
        or counts["selected_completions"] != 0
        or counts["joins"] != 8
        or counts["sources"] != 25
        or independent["status"] != "PASS"
        or independent["mutation_catches_passed"] != 29
        or len(generators) != 10
        or len(bilinears) != 10
        or len(seals) != 5
        or len(combined) != 5
        or len(combined_bilinear) != 5
        or len(witnesses) != 3
        or len(completions) != 12
        or len(joins) != 8
        or len(catches) != 29
        or len(lineage) != 25
        or any(row["status"] != "CAUGHT" for row in catches)
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or not review.startswith(
            "**Verdict**\n\n`VERIFIED-WITH-CAVEATS`."
        )
    ):
        raise AssertionError("reciprocal-angular science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "continuous_generator_cases": len(generators),
        "bilinear_cross_cases": len(bilinears),
        "seal_cases": len(seals),
        "combined_map_cases": len(combined),
        "combined_bilinear_cases": len(combined_bilinear),
        "local_full_metric_witnesses": len(witnesses),
        "completion_rows": len(completions),
        "complete_g_phi_witnesses": 0,
        "selected_completions": 0,
        "source_files": len(lineage),
        "mutation_catches": len(catches),
        "fresh_review": "VERIFIED-WITH-CAVEATS",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "intertwiner_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic)
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = load(
        ROOT
        / "hygiene_baseline_correction_2026-07-23"
        / "verify_repository_gates.py",
        "intertwiner_hygiene_gates",
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
        "schema": "udt-reciprocal-angular-intertwiner-repository-gates-1.0",
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
