#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "39dda1aac9a8dab16428f7d031e1668b9bc7fde0"
PACKAGE = "udt_full_equation_variation_p05_2026-07-21"
P04 = ROOT / "udt_dynamics_branch_ruling_p04_2026-07-21"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
P04_MANIFEST = "d01d65fc5abcc35078c961d0d3fc0eec7ad26e205735a77f7d83e2b45121de3f"

SOURCES = {
    "udt_dynamics_branch_ruling_p04_2026-07-21/SHA256SUMS.txt": P04_MANIFEST,
    "udt_dynamics_branch_ruling_p04_2026-07-21/RULING_RESULT.json": "d524a993798ec8148421f5b2099358354025dae331fcef5388f6ad4c4c256039",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_variation_domain.py": "084511961b6c69270278c64ae69f58942b044f106990e7071a5003f8535aee7e",
    "native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_unique_action_weights.py": "33e804e990fad69e49b3471adc8443f8037e7d4b5f617999dd1579286c3e430c",
    "native_action_arm_c_2026-07-18/ARM_C_RETURN/cas_armc_boundary_charge.py": "e29f017a354275b62d415961365583d165bffc9637303b1a3ae9feb17510184d",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def scope(generic, inject: str | None = None) -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if inject:
        changed.add(inject)
    invalid = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if invalid:
        raise generic.GateError("SCOPE", invalid[0])
    return sorted(changed)


def operator_verification() -> dict[str, object]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_p05_operators.py")], cwd=ROOT,
        env=environment, text=True, capture_output=True, timeout=300, check=False,
    )
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run(
        [sys.executable, "-B", str(HERE / "verify_p05_operators.py")], cwd=ROOT,
        env=environment, text=True, capture_output=True, timeout=300, check=False,
    )
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "OPERATOR_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if (
        result["status"] != "PASS"
        or result["check_count"] != 32
        or result["counts"]["field_pairs"] != 21
        or result["counts"]["field_pairs_complete_actions"] != 0
        or result["counts"]["global_axes_free"] != 12
        or result["protocol_maximum_earned"] is not False
        or result["maximum_conclusion"] != "NAMED_BULK_OPERATORS_AND_VARIATION_OBSTRUCTIONS_CHARACTERIZED"
        or verification["status"] != "PASS"
        or verification["check_count"] != 9
        or verification["catch_proof_count"] != 31
    ):
        raise AssertionError("P05 operator verification")
    return {
        "status": "PASS",
        "main_checks": result["check_count"],
        "independent_checks": verification["check_count"],
        "catch_proofs": verification["catch_proof_count"],
        "main_result_sha256": digest(HERE / "OPERATOR_RESULT.json"),
        "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "maximum_conclusion": result["maximum_conclusion"],
    }


def source_immutability() -> dict[str, object]:
    observed: dict[str, str] = {}
    for relative, expected in SOURCES.items():
        value = digest(ROOT / relative)
        if value != expected:
            raise AssertionError(f"source hash: {relative}")
        completed = subprocess.run(
            ["git", "diff", "--quiet", BASE, "--", relative], cwd=ROOT, check=False,
        )
        if completed.returncode:
            raise AssertionError(f"source changed: {relative}")
        observed[relative] = value
    return {"status": "PASS", "sources": observed, "count": len(observed)}


def prior_packages() -> dict[str, str]:
    record = json.loads((P04 / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {
        row["package"]: row["manifest_sha256"]
        for row in record["prior_scientific_packages"]["packages"]
    }
    prior["udt_dynamics_branch_ruling_p04_2026-07-21"] = P04_MANIFEST
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
    generic = load(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py",
        "p05_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    changed = scope(generic)
    operator = operator_verification()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 57 or replay["entries"] != 1380:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = generic.validate_navigation(ROOT)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode("utf-8")).hexdigest()
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
        "schema": "udt-p05-conditional-operator-repository-gates-1.0",
        "base": BASE,
        "result": "PASS",
        "scope_paths": changed,
        "operator_verifier": operator,
        "source_immutability": sources,
        "frozen": frozen,
        "prior_scientific_packages": replay,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {
            "cpu_only": True,
            "gpu_work_performed": False,
            "symbolic_variation": True,
            "ODE_or_PDE_run": False,
        },
        "authority_boundary": {
            "startup_controls_changed": False,
            "canon_changed": False,
            "native_dynamics_derived": False,
            "complete_operator_earned": False,
            "P06_launched": False,
            "solve_authorized": False,
            "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    print("repository_gates=PASS")
    print(f"P05={operator['main_checks']} main/{operator['independent_checks']} independent/{operator['catch_proofs']} catches")
    print(f"sources={sources['count']} frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()
