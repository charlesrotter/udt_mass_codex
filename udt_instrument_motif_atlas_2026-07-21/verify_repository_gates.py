#!/usr/bin/env python3
"""Repository gates for the UDT instrument-motif atlas."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "8e6b425b08889dd8e0b5f8d7b0ae3945dc1dcacf"
PACKAGE = "udt_instrument_motif_atlas_2026-07-21"
PARENT = ROOT / "udt_joint_invariant_subspace_atlas_2026-07-21"
PARENT_MANIFEST = "973dcc8bb297fad8358087318b24e5db9d1179e8b6a51a2535a0110e30c108c2"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
MAXIMUM = "BOUNDED_POINTWISE_INSTRUMENT_MOTIF_LATTICE_CHARACTERIZED"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run_scientific() -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["OMP_NUM_THREADS"] = "1"
    commands = [
        ("independent", [sys.executable, "-B", str(HERE / "verify_motif_atlas.py")], 900),
        ("all_margins", [sys.executable, "-B", str(HERE / "verify_motif_margins.py")], 900),
        ("contract", [sys.executable, "-B", str(HERE / "verify_package_contract.py")], 300),
    ]
    transcripts = {}
    for label, command, timeout in commands:
        completed = subprocess.run(
            command, cwd=ROOT, env=env, text=True, capture_output=True,
            timeout=timeout, check=False,
        )
        if completed.returncode or completed.stderr:
            raise AssertionError(f"{label}\n{completed.stdout}\n{completed.stderr}")
        transcripts[label] = hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest()
    atlas = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    margins = json.loads((HERE / "MARGIN_ESCALATION_RESULT.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "CONTRACT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if not (
        atlas["maximum_conclusion"] == MAXIMUM
        and atlas["configurations"] == 6144 and atlas["family_rows"] == 190464
        and atlas["edge_rows"] == 460800 and atlas["nonlinear_family_rows"] == 380928
        and atlas["nonlinear_nonuncertain_discordances"] == 0
        and atlas["nonlinear_edge_nonuncertain_discordances"] == 0
        and atlas["nonlinear_alignment_nonuncertain_discordances"] == 0
        and atlas["physical_merit_evaluated"] is False
        and independent["status"] == "PASS" and independent["total_family_classifications"] == 35712
        and independent["catch_proofs"] == 12
        and margins["status"] == "PASS" and margins["unique_target_identities"] == 124
        and margins["discordant_identities"] == 0
        and contract["status"] == "PASS" and contract["catch_proofs"] == 5
    ):
        raise AssertionError("scientific result contract")
    return {
        "status": "PASS",
        "configurations": atlas["configurations"],
        "family_rows": atlas["family_rows"],
        "edge_rows": atlas["edge_rows"],
        "nonlinear_family_rows": atlas["nonlinear_family_rows"],
        "blind_anchor_classifications": independent["total_family_classifications"],
        "all_margin_unique_identities": margins["unique_target_identities"],
        "all_margin_discordant_identities": margins["discordant_identities"],
        "production_catches": atlas["catch_proofs_passed"],
        "independent_catches": independent["catch_proofs"],
        "contract_catches": contract["catch_proofs"],
        "atlas_result_sha256": digest(HERE / "ATLAS_RESULT.json"),
        "independent_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "margin_result_sha256": digest(HERE / "MARGIN_ESCALATION_RESULT.json"),
        "contract_result_sha256": digest(HERE / "CONTRACT_VERIFICATION_RESULT.json"),
        "stdout_sha256": transcripts,
        "maximum_conclusion": MAXIMUM,
    }


def source_immutability() -> dict[str, object]:
    observed = {}
    for row in rows(HERE / "SOURCE_LINEAGE.tsv"):
        relative = row["path"]
        path = HERE / relative if row["role"] == "PREREGISTRATION" else ROOT / relative
        if digest(path) != row["sha256"]:
            raise AssertionError(f"source hash {relative}")
        observed[relative] = row["sha256"]
    if len(observed) != 8:
        raise AssertionError("source count")
    return {"status": "PASS", "count": len(observed), "sources": observed}


def prior_packages() -> dict[str, str]:
    record = json.loads((PARENT / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {row["package"]: row["manifest_sha256"]
             for row in record["prior_scientific_packages"]["packages"]}
    prior[PARENT.name] = PARENT_MANIFEST
    return prior


def main() -> None:
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "motif_generic")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    scope = generic.validate_scope(ROOT)
    scientific = run_scientific()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 68 or replay["entries"] != 1795:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = generic.validate_package_manifest(ROOT)
    catches = {
        "scope": generic.expect("SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: generic.validate_package_manifest(ROOT, True)),
    }
    output = {
        "schema": "udt-instrument-motif-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": scope,
        "scientific_verifier": scientific,
        "source_immutability": sources,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "ODE_or_PDE_run": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "action_or_equations_loaded": False,
            "physical_motif_selected": False,
            "transport_or_dynamics_claimed": False,
            "boundary_topology_or_scale_selected": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("repository_gates=PASS")
    print(f"scientific={scientific['configurations']} configurations/{scientific['family_rows']} family rows/{scientific['edge_rows']} edges")
    print(f"independent={scientific['blind_anchor_classifications']} classifications margins={scientific['all_margin_unique_identities']}")
    print(f"frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()
