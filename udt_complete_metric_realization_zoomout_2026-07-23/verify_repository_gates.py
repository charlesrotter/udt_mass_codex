#!/usr/bin/env python3
"""Repository gates for the complete-metric realization zoom-out."""

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
BASE = "196a8ef"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_coframe_hopf_bridge_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "ee35787b41fbca774031080c1c12a4c0fe01dc820abdeb444e1977d58bbb0b1b"
)
MAXIMUM = (
    "REGISTERED_COMPLETE_METRIC_REALIZATION_LAYERS_MAPPED__ANY_EXISTING_"
    "NATIVE_JOIN_IDENTIFIED_WITH_EXACT_SCOPE__MISSING_JOINS_REMAIN_OPEN"
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
    previous = load(
        ROOT / PREVIOUS / "verify_repository_gates.py",
        "realization_previous_gate_chain",
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
    replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PRIOR", PREVIOUS + ":replay")
    count = len([line for line in manifest.read_text().splitlines() if line])
    entries += count
    details.append(
        {
            "package": PREVIOUS,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": count,
            "result": "PASS",
        }
    )
    if len(details) != 89:
        raise generic.GateError("PRIOR", f"package-count:{len(details)}")
    return {"packages": details, "entries": entries, "result": "PASS"}


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text().splitlines() if line
    ]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name not in excluded
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "coverage")
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
    citations = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = re.sub(r":\d+$", "", target)
            if source.name in {
                "FRESH_ADVERSARIAL_REVIEW.md",
                "POST_CORRECTION_ADVERSARIAL_REVIEW.md",
            } and "/repo/" in target:
                destination = ROOT / target.split("/repo/", 1)[1]
                citations += 1
            else:
                destination = source.parent.joinpath(target).resolve()
                links += 1
            if not destination.exists():
                raise generic.GateError("NAVIGATION", f"{source.name}:{raw}")
    result["package_links"] = links
    result["review_path_citations"] = citations
    return result


def validate_dirty_head(generic) -> dict[str, str]:
    head = subprocess.check_output(
        ["git", "-C", str(DIRTY), "rev-parse", "HEAD"], text=True
    ).strip()
    branch = subprocess.check_output(
        ["git", "-C", str(DIRTY), "branch", "--show-current"], text=True
    ).strip()
    if head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2" or branch != "grok":
        raise generic.GateError("DIRTY", f"{head}:{branch}")
    return {"head": head, "branch": branch}


def validate_science() -> dict[str, object]:
    result = json.loads((HERE / "RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    replay = json.loads((HERE / "REPLAY_RESULT.json").read_text())
    tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(
        encoding="utf-8"
    )
    post_review = (
        HERE / "POST_CORRECTION_ADVERSARIAL_REVIEW.md"
    ).read_text(encoding="utf-8")
    if (
        result["source_count"] != 47
        or result["new_physical_premises"] != 0
        or result["counts"]["native_end_to_end_bridges"] != 0
        or independent["status"] != "PASS"
        or independent["sources_checked"] != 47
        or independent["mutation_catches"] != {"passed": 21, "total": 21}
        or independent["direct_source_semantic_replay"]["passed"] != 11
        or independent["direct_source_semantic_replay"]["total"] != 11
        or not replay["all_exit_zero"]
        or (tests["passed"], tests["failed"], tests["xfailed"]) != (70, 0, 1)
        or not any(token in review[:500] for token in ("PASS", "VERIFIED"))
        or "PASS" not in post_review[:500]
        or result["maximum_conclusion"] != MAXIMUM
    ):
        raise AssertionError("scientific contract")
    return {
        "maximum_conclusion": result["maximum_conclusion"],
        "production_stdout_sha256": replay["production"]["stdout_sha256"],
        "independent_stdout_sha256": replay["independent"]["stdout_sha256"],
        "mutation_catches": independent["mutation_catches"],
        "direct_source_semantic_replay": (
            independent["direct_source_semantic_replay"]
        ),
        "fresh_review": review.splitlines()[0],
        "post_correction_review": "PASS",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "realization_generic_gates",
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
        ROOT / "hygiene_baseline_correction_2026-07-23"
        / "verify_repository_gates.py",
        "realization_hygiene_gates",
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
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")
        ),
        "frontier": generic.expect(
            "NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")
        ),
        "dirty": generic.expect(
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)
        ),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, True)
        ),
    }
    output = {
        "schema": "udt-complete-metric-realization-repository-gates-v1",
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
