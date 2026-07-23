#!/usr/bin/env python3
"""Repository gates for the native complete-coframe composition-law audit."""

from __future__ import annotations

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
BASE = "3f0e3332a681e32253c9700b0e96babd315067f8"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
ADDITIONAL_PRIOR = (
    (
        "udt_bank_simplex_interior_atlas_2026-07-23",
        "75ac459c9eb978c88272b7115da2a723f4d7a009b4f72f7d7972dc525437a1f1",
    ),
    (
        "hygiene_baseline_correction_2026-07-23",
        "1660a94a039194c8143691a50862f07ec51bcc17126fa95880b4da0b4e41a4e7",
    ),
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
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def replay_prior(generic, corrupt: bool = False) -> dict[str, object]:
    bank = load(
        ROOT
        / "udt_bank_simplex_interior_atlas_2026-07-23"
        / "verify_repository_gates.py",
        "composition_bank_gate_chain",
    )
    chained = bank.replay_prior(generic, corrupt)
    details = list(chained["packages"])
    entries = int(chained["entries"])
    for index, (package, expected) in enumerate(ADDITIONAL_PRIOR):
        manifest = ROOT / package / "MANIFEST.sha256"
        observed = digest(manifest)
        if corrupt and index == 0:
            observed = "0" * 64
        if observed != expected:
            raise generic.GateError("PRIOR", package + ":manifest")
        replay = generic.run(
            manifest.parent, ["sha256sum", "--check", manifest.name]
        )
        if replay.returncode or "FAILED" in str(replay.stdout):
            raise generic.GateError("PRIOR", package + ":replay")
        count = len([line for line in manifest.read_text().splitlines() if line])
        entries += count
        details.append(
            {
                "package": package,
                "manifest": manifest.name,
                "manifest_sha256": expected,
                "entries": count,
                "result": "PASS",
            }
        )
    if len(details) != 87:
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
        raise generic.GateError(
            "PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}"
        )
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
    if head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2" or branch != "grok":
        raise generic.GateError("DIRTY", f"head:{head}:{branch}")
    return {"head": head, "branch": branch}


def validate_navigation(generic) -> dict[str, int]:
    """Validate operational links while preserving raw review path citations."""

    saved_package = generic.PACKAGE
    generic.PACKAGE = "__NO_PACKAGE_MARKDOWN__"
    try:
        navigation = generic.validate_navigation(ROOT)
    finally:
        generic.PACKAGE = saved_package

    evidence_records = {
        "FRESH_ADVERSARIAL_REVIEW.md",
        "POST_CORRECTION_REVIEW.md",
    }
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    operational_links = 0
    evidence_path_citations = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            target = re.sub(r":\d+$", "", target)
            if source.name in evidence_records and "/repo/" in target:
                relative = target.split("/repo/", 1)[1]
                destination = ROOT / relative
                evidence_path_citations += 1
            else:
                destination = source.parent.joinpath(target).resolve()
                operational_links += 1
            if not destination.exists():
                raise generic.GateError(
                    "NAVIGATION", f"markdown-link:{source.name}:{raw}"
                )
    navigation["package_links"] = operational_links
    navigation["review_path_citations"] = evidence_path_citations
    return navigation


def validate_science() -> dict[str, object]:
    result = json.loads((HERE / "RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    replay = json.loads((HERE / "REPLAY_RESULT.json").read_text())
    tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    expected_conclusion = (
        "CURRENT_UDT_PREMISES_SUPPLY_CONDITIONAL_RECIPROCAL_ONE_PARAMETER_"
        "COMPOSITION_BUT_NOT_A_WEIGHTED_MULTI_CONFIGURATION_MEAN_OR_NATIVE_"
        "COMPLETE_COFRAME_COMPOSITION"
    )
    if (
        result["maximum_conclusion"] != expected_conclusion
        or result["source_count"] != 18
        or result["counts"]["candidate_complete_native_laws"] != 0
        or result["counts"]["partial_native_reciprocal_laws"] != 1
        or result["source_behavioral_reconstruction"]["chart_checks"] != 6
        or result["source_behavioral_reconstruction"]["coframe_checks"] != 6
        or independent["status"] != "PASS"
        or independent["sources_checked"] != 18
        or independent["catch_proofs"] != {"passed": 16, "total": 16}
        or independent["independent_source_behavior"]["chart_checks"] != 4
        or independent["independent_source_behavior"]["matrix_checks"] != 4
        or not replay["all_exit_zero"]
        or replay["derivation"]["stdout_sha256"]
        != "c0ac1742e375b711bf7330dc8072e9188a320bb1411245fe611d1bc79d48d150"
        or replay["independent"]["stdout_sha256"]
        != "8775a4d94b02597834355c2a00aded03aba27929dd63e9daa26874a323f14848"
        or (tests["passed"], tests["failed"], tests["xfailed"]) != (70, 0, 1)
    ):
        raise AssertionError("composition audit scientific contract")
    reviews = {
        name: (HERE / name).read_text(encoding="utf-8")
        for name in (
            "FRESH_ADVERSARIAL_REVIEW.md",
            "POST_CORRECTION_REVIEW.md",
        )
    }
    if any(
        "PASS_WITH_CAVEATS" not in text[:100]
        for text in reviews.values()
    ):
        raise AssertionError("fresh-review verdict contract")
    correction = (HERE / "POST_REVIEW_CORRECTION_APPLICATION.md").read_text()
    for required in (
        "type-correct relative",
        "genuinely local-Lorentz-equivariant quotient operation",
        "selected weighted multi-input rule",
        "compatible `phi/dphi` rule",
    ):
        if required not in correction:
            raise AssertionError("post-review correction propagation")
    return {
        "maximum_conclusion": result["maximum_conclusion"],
        "sources_checked": independent["sources_checked"],
        "candidate_complete_native_laws": 0,
        "partial_native_reciprocal_laws": 1,
        "production_behavioral_checks": {
            "scalar": result["source_behavioral_reconstruction"]["chart_checks"],
            "coframe": result["source_behavioral_reconstruction"]["coframe_checks"],
        },
        "independent_behavioral_checks": {
            "scalar": independent["independent_source_behavior"]["chart_checks"],
            "coframe": independent["independent_source_behavior"]["matrix_checks"],
        },
        "mutation_catches": independent["catch_proofs"],
        "fresh_reviews": {
            name: "PASS_WITH_CAVEATS__EXACT_CORRECTIONS_APPLIED"
            for name in reviews
        },
        "test_baseline": tests,
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "composition_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic)
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = validate_science()["test_baseline"]
    rerun_tests = load(
        ROOT
        / "hygiene_baseline_correction_2026-07-23"
        / "verify_repository_gates.py",
        "composition_hygiene_gates",
    ).validate_tests(generic)
    scientific = validate_science()
    package = validate_package(generic)
    catches = {
        "scope_rejects_live_edit": generic.expect(
            "SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")
        ),
        "frozen_corruption_rejected": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, True)
        ),
        "prior_corruption_rejected": generic.expect(
            "PRIOR", lambda: replay_prior(generic, True)
        ),
        "current_path_loss_rejected": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "current"),
        ),
        "frontier_loss_rejected": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "frontier"),
        ),
        "dirty_metadata_loss_rejected": generic.expect(
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)
        ),
        "package_corruption_rejected": generic.expect(
            "PACKAGE", lambda: validate_package(generic, True)
        ),
    }
    output = {
        "schema": "udt-native-coframe-composition-repository-gates-v1",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "scientific_verification": scientific,
        "saved_full_tests": tests,
        "rerun_full_tests": rerun_tests,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {
            "cpu_only": True,
            "gpu_work_performed": False,
            "physics_solve_performed": False,
        },
        "authority_boundary": (
            "COMPLETE_TRIANGULAR_CHART_GROUP_CLOSURE_AND_COMPOSITION_"
            "OBSTRUCTIONS_ONLY__NO_NATIVE_PHYSICAL_COMPOSITION_ACTION_"
            "CARRIER_SOURCE_BOUNDARY_SCALE_OR_CANON"
        ),
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
