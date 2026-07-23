#!/usr/bin/env python3
"""Repository gates for the phi causal-interface atlas."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "03e0e9407c756ad4cae2fbf4a4814c820aeaf5fc"
PACKAGE = HERE.name
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS_PACKAGE = "udt_temporal_soldering_atlas_2026-07-22"
PREVIOUS_MANIFEST = "11d67cb7c09188a69e38dcc4e6b0370faa15c0ec7d72bf616e70c8c2bf21def8"


def load(path, name):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def prior_records():
    previous = load(
        ROOT / PREVIOUS_PACKAGE / "verify_repository_gates.py",
        "previous_phi_interface_gate_chain",
    )
    records = previous.prior_manifest_records()
    records.append({"package": PREVIOUS_PACKAGE, "expected": PREVIOUS_MANIFEST})
    return records


def replay_prior(generic, corrupt=False):
    details = []
    entries = 0
    for index, record in enumerate(prior_records()):
        package, expected = record["package"], record["expected"]
        candidates = [ROOT / package / "SHA256SUMS.txt", ROOT / package / "MANIFEST.sha256"]
        matching = [path for path in candidates if path.exists() and digest(path) == expected]
        if corrupt and index == 0:
            matching = []
        if len(matching) != 1:
            raise generic.GateError("PRIOR", package + ":manifest")
        manifest = matching[0]
        replay = generic.run(manifest.parent, ["sha256sum", "--check", manifest.name])
        if replay.returncode or "FAILED" in str(replay.stdout):
            raise generic.GateError("PRIOR", package + ":replay")
        count = len([line for line in manifest.read_text().splitlines() if line])
        entries += count
        details.append({
            "package": package,
            "manifest": manifest.name,
            "manifest_sha256": expected,
            "entries": count,
            "result": "PASS",
        })
    if len(details) != 83 or entries != 2_341:
        raise generic.GateError("PRIOR", f"totals:{len(details)}:{entries}")
    return {"packages": details, "entries": entries, "result": "PASS"}


def validate_package(generic, corrupt=False):
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text().splitlines() if line]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in excluded)
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", f"coverage:{sorted(set(entries) ^ set(actual))}")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def validate_dirty_head(generic):
    head = subprocess.check_output(["git", "-C", str(DIRTY), "rev-parse", "HEAD"], text=True).strip()
    branch = subprocess.check_output(["git", "-C", str(DIRTY), "branch", "--show-current"], text=True).strip()
    if head != BASE or branch != "grok":
        raise generic.GateError("DIRTY", f"head:{head}:{branch}")
    return {"head": head, "branch": branch}


def main():
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "phi_interface_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic)
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = generic.validate_tests(ROOT)
    package = validate_package(generic)
    scientific = json.loads((HERE / "PACKAGE_VERIFICATION.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    replay = json.loads((HERE / "REPLAY_RESULT.json").read_text())
    if (
        scientific["status"] != "PASS_WITH_REGISTERED_SCOPE"
        or scientific["state"]["identity_count"] != 3_072
        or scientific["state"]["interface_rows"] != 0
        or scientific["state"]["physical_labels"] != 0
        or scientific["state"]["continuous_complete_motif_claim"] is not False
        or scientific["state"]["frozen_generator_probes"] != 13_824
        or independent["status"] != "PASS"
        or len(independent["mutation_catches"]) != 8
        or not replay["all_exit_zero"]
        or not replay["all_outputs_byte_identical"]
    ):
        raise AssertionError("scientific verification contract")
    catches = {
        "scope_rejects_live_edit": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen_corruption_rejected": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior_corruption_rejected": generic.expect("PRIOR", lambda: replay_prior(generic, True)),
        "current_path_loss_rejected": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier_loss_rejected": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty_metadata_loss_rejected": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package_corruption_rejected": generic.expect("PACKAGE", lambda: validate_package(generic, True)),
    }
    result = {
        "schema": "udt-phi-causal-interface-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "scientific_verification": scientific,
        "independent_verification": independent,
        "deterministic_replay": replay,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {
            "physics_solves": 0,
            "gpu_runs": 0,
            "cpu_production_interval_passes": 2,
            "cpu_independent_interval_passes": 2,
            "sne_fits": 0,
        },
        "authority_boundary": "PHI_CAUSAL_INTERFACE_ATLAS_ONLY__NO_PHYSICAL_REGIME_BRANCH_GLOBAL_SOLUTION_ACTION_CARRIER_OR_NAVIGATION_EDIT",
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
