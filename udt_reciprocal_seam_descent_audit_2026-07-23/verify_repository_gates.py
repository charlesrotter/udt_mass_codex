#!/usr/bin/env python3
"""Repository gates for the reciprocal value-character seam audit."""

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
BASE = "67ac641e3bf764c2d4b43ddf79df7ef24a1ff429"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_global_reciprocal_persistence_selector_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "4d1e70a28191a4cc25f39b3d24d41bb48b2c0de1b6151c15e354a4a2dfc82624"
)
MAXIMUM = (
    "RECIPROCAL_VALUE_CHARACTER_HAS_EXACT_Z2_GRADED_SEAM_DESCENT_AND_"
    "CAN_SURVIVE_DPHI_DEGENERATION__COMPLETE_PHYSICAL_GLUE_STILL_"
    "REQUIRES_UNSUPPLIED_COVER_EQUIVARIANCE_ANGULAR_SOLDERING_METRIC_"
    "JETS_AND_CONNECTION_DATA__NO_REALIZATION_RELATION_OR_COMPLETION_"
    "SELECTOR_DERIVED"
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
        "seam_descent_previous_gate_chain",
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
    if len(details) != 93:
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
    review_citations = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = re.sub(r":\d+$", "", target)
            if source.name == "FRESH_ADVERSARIAL_REVIEW.md" and "/repo/" in target:
                destination = ROOT / target.split("/repo/", 1)[1]
                review_citations += 1
            else:
                destination = source.parent.joinpath(target).resolve()
                links += 1
            if not destination.exists():
                raise generic.GateError(
                    "NAVIGATION", f"{source.name}:{raw}"
                )
    result["package_links"] = links
    result["review_path_citations"] = review_citations
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
    completions = read_tsv(HERE / "COMPLETION_DESCENT_ATLAS.tsv")
    profiles = read_tsv(HERE / "MIRROR_JET_CONTROLS.tsv")
    theorems = read_tsv(HERE / "GLOBAL_DESCENT_THEOREMS.tsv")
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
        or counts["completion_rows"] != 12
        or counts["parametric_type_rows"] != 11
        or counts["conditional_control_rows"] != 1
        or counts["complete_g_phi_witnesses"] != 0
        or counts["selected_completions"] != 0
        or counts["mirror_profiles"] != 3
        or counts["mirror_profiles_value_first_second_jet_pass"] != 3
        or counts["critical_dphi_mirror_profiles"] != 1
        or counts["global_theorems"] != 12
        or counts["joins"] != 7
        or counts["sources"] != 22
        or independent["status"] != "PASS"
        or independent["catch_proofs_passed"] != 25
        or len(completions) != 12
        or any(
            row["selection_ruling"]
            != "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_DESCENT"
            for row in completions
        )
        or len(profiles) != 3
        or any(
            row["value_pullback_match"] != "True"
            or row["first_jet_pullback_match"] != "True"
            or row["second_jet_pullback_match"] != "True"
            for row in profiles
        )
        or len(theorems) != 12
        or len(joins) != 7
        or len(catches) != 25
        or len(lineage) != 22
        or any(row["status"] != "CAUGHT" for row in catches)
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or not review.startswith("**Verdict**\n\n`VERIFIED`.")
    ):
        raise AssertionError("reciprocal seam-descent science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "completion_rows": len(completions),
        "complete_g_phi_witnesses": 0,
        "selected_completions": 0,
        "mirror_profiles": len(profiles),
        "global_theorems": len(theorems),
        "joins": len(joins),
        "source_files": len(lineage),
        "mutation_catches": len(catches),
        "fresh_review": "VERIFIED",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "seam_descent_generic_gates",
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
        "seam_descent_hygiene_gates",
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
        "schema": "udt-reciprocal-seam-descent-repository-gates-1.0",
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
