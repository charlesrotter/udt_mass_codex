#!/usr/bin/env python3
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
BASE = "21cfeb8f25fe18afe5a5a924ea073a9cfc24238b"
PACKAGE = "udt_time_live_characteristic_flux_audit_2026-07-21"
PARENT = ROOT / "udt_pre_p06_boundary_selector_audit_2026-07-21"
PARENT_MANIFEST = "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51"
DIRTY = Path("/home/udt-admin/udt_mass_codex")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def scope(generic, inject: str | None = None) -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if inject:
        changed.add(inject)
    bad = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise generic.GateError("SCOPE", bad[0])
    return sorted(changed)


def scientific_verification() -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_time_live_flux.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=300, check=False,
    )
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run(
        [sys.executable, "-B", str(HERE / "verify_time_live_flux.py")],
        cwd=ROOT, env=env, text=True, capture_output=True, timeout=300, check=False,
    )
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    verify = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["checks"] != 80
        or result["classification"] != "TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA"
        or result["field_lane_pairs"] != 21
        or result["boundary_branches"] != 8
        or result["P06_ready_pairs"] != 0
        or result["solutions_run"] != 0
        or result["gpu_used"] is not False
        or verify["verification"] != "PASS"
        or verify["generator_imported"] is not False
        or verify["independent_algebra_checks"] != 28
        or verify["catch_proofs"] != 45
    ):
        raise AssertionError("scientific verification")
    return {
        "status": "PASS",
        "main_checks": result["checks"],
        "independent_checks": verify["independent_algebra_checks"],
        "catch_proofs": verify["catch_proofs"],
        "main_result_sha256": digest(HERE / "DERIVATION_RESULT.json"),
        "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "maximum_conclusion": result["maximum_conclusion"],
    }


def source_immutability() -> dict[str, object]:
    observed: dict[str, str] = {}
    for row in tsv(HERE / "SOURCE_LINEAGE.tsv"):
        relative = row["path"]
        expected = row["sha256"]
        if digest(ROOT / relative) != expected:
            raise AssertionError(f"source hash {relative}")
        if subprocess.run(["git", "diff", "--quiet", BASE, "--", relative], cwd=ROOT, check=False).returncode:
            raise AssertionError(f"source changed {relative}")
        observed[relative] = expected
    if len(observed) != 7:
        raise AssertionError("source count")
    return {"status": "PASS", "count": len(observed), "sources": observed}


def prior_packages() -> dict[str, str]:
    record = json.loads((PARENT / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    prior["udt_pre_p06_boundary_selector_audit_2026-07-21"] = PARENT_MANIFEST
    return prior


def validate_package_manifest(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = subprocess.run(
        ["sha256sum", "--check", manifest.name], cwd=HERE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
    )
    if corrupt or replay.returncode or "FAILED" in replay.stdout:
        raise generic.GateError("PACKAGE", "hash-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.relative_to(HERE).as_posix() for path in HERE.rglob("*")
        if path.is_file() and path.relative_to(HERE).as_posix() not in excluded
    )
    if sorted(entries) != actual or len(entries) != len(set(entries)):
        raise generic.GateError("PACKAGE", "recursive coverage")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "time_live_generic")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    changed = scope(generic)
    scientific = scientific_verification()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 59 or replay["entries"] != 1437:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = validate_package_manifest(generic)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: generic.validate_navigation(ROOT, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: validate_package_manifest(generic, True)),
    }
    output = {
        "schema": "udt-time-live-characteristic-flux-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "scientific_verifier": scientific,
        "source_immutability": sources,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "symbolic_algebra": True, "ODE_or_PDE_run": False},
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "boundary_functional_adopted": False,
            "boundary_type_selected": False,
            "time_live_seal_promoted_to_canon": False,
            "P06_launched": False,
            "numerical_evolution_launched": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"scientific={scientific['main_checks']} main/{scientific['independent_checks']} independent/{scientific['catch_proofs']} catches")
    print(f"sources={sources['count']} frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()
