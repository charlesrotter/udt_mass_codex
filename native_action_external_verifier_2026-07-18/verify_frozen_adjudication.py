#!/usr/bin/env python3
"""Externally replay and hash-check the frozen native-action adjudication.

All executable inputs are copied into a caller-supplied work tree before they
are run. The frozen packages are read only. The JSON report is emitted outside
those packages.
"""

from __future__ import annotations

import argparse
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import shutil
import site
import stat
import subprocess
import sys
from typing import Any

import sympy


EXPECTED_SYMPY = "1.13.1"
EXPECTED_MPMATH = "1.3.0"

PACKAGES = (
    (
        "stage1_A",
        "native_action_stage1_2026-07-18/arm_A",
        "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
        29,
    ),
    (
        "stage1_B",
        "native_action_stage1_2026-07-18/arm_B",
        "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
        15,
    ),
    (
        "stage2_A",
        "native_action_stage2_2026-07-18/arm_A",
        "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
        13,
    ),
    (
        "stage2_B",
        "native_action_stage2_2026-07-18/arm_B",
        "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
        13,
    ),
    (
        "arm_C",
        "native_action_arm_c_2026-07-18",
        "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
        21,
    ),
    (
        "final_adjudication",
        "native_action_final_adjudication_2026-07-18",
        "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
        36,
    ),
)

CAS_GROUPS = (
    (
        "stage1_A",
        "native_action_stage1_2026-07-18/arm_A/cold_output",
        (
            "cas_common_scale.py",
            "cas_completion_fork.py",
            "cas_conformal_weights.py",
            "cas_metric_block.py",
            "cas_p4_stress.py",
            "cas_p4_variation.py",
            "cas_radial_flux.py",
            "cas_reciprocity.py",
            "cas_s2_static_completion.py",
            "cas_s2_stress.py",
            "cas_weak_metric_expansion.py",
        ),
    ),
    (
        "stage1_B",
        "native_action_stage1_2026-07-18/arm_B/cold_output",
        (
            "cas_csn_decomposition.py",
            "cas_dual_reciprocity_uv.py",
            "cas_exponential_composition.py",
            "cas_metric_product_and_csn.py",
        ),
    ),
    (
        "stage2_A",
        "native_action_stage2_2026-07-18/arm_A/D6_RETURN",
        (
            "cas_stage2_carrier_weight_source.py",
            "cas_stage2_mass_virial.py",
        ),
    ),
    (
        "stage2_B",
        "native_action_stage2_2026-07-18/arm_B/D6_RETURN",
        (
            "cas_stage2_source_channel_identities.py",
            "cas_stage2_srel_sfol_conventions.py",
        ),
    ),
    (
        "arm_C",
        "native_action_arm_c_2026-07-18/ARM_C_RETURN",
        (
            "cas_armc_boundary_charge.py",
            "cas_armc_carrier_covariance.py",
            "cas_armc_mass_virial.py",
            "cas_armc_unique_action_weights.py",
            "cas_armc_variation_domain.py",
        ),
    ),
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def manifest_hash_gate(actual: str, expected: str) -> bool:
    return actual == expected


def package_snapshot(package: Path) -> dict[str, Any]:
    if package.is_symlink() or not package.is_dir():
        raise RuntimeError(f"package is not a real directory: {package}")
    rows: list[dict[str, Any]] = []
    for path in sorted(package.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"symlink forbidden in frozen package: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise RuntimeError(f"non-regular package entry: {path}")
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & 0o222:
            raise RuntimeError(f"writable file in frozen package: {path}")
        rows.append(
            {
                "path": path.relative_to(package).as_posix(),
                "sha256": sha256_file(path),
                "size": path.stat().st_size,
                "mode": f"{mode:04o}",
            }
        )
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {
        "state_sha256": sha256_bytes(canonical),
        "file_count_including_manifest": len(rows),
        "files": rows,
    }


def parse_and_verify_manifest(
    package: Path, expected_manifest_hash: str, expected_entries: int
) -> dict[str, Any]:
    manifest = package / "SHA256SUMS.txt"
    actual_manifest_hash = sha256_file(manifest)
    if not manifest_hash_gate(actual_manifest_hash, expected_manifest_hash):
        raise RuntimeError(
            f"manifest hash mismatch for {package}: "
            f"{actual_manifest_hash} != {expected_manifest_hash}"
        )
    listed: dict[str, str] = {}
    for line_number, row in enumerate(
        manifest.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            expected, relative = row.split("  ", 1)
        except ValueError as exc:
            raise RuntimeError(
                f"malformed manifest row {manifest}:{line_number}"
            ) from exc
        if relative.startswith("./"):
            relative = relative[2:]
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts or relative in listed:
            raise RuntimeError(f"unsafe or duplicate manifest path: {relative}")
        listed[relative] = expected
    if len(listed) != expected_entries:
        raise RuntimeError(
            f"manifest entry count mismatch for {package}: "
            f"{len(listed)} != {expected_entries}"
        )
    actual_files = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS.txt"
    }
    if set(listed) != actual_files:
        raise RuntimeError(
            f"manifest inventory mismatch for {package}: "
            f"missing={sorted(set(listed) - actual_files)} "
            f"unlisted={sorted(actual_files - set(listed))}"
        )
    for relative, expected in listed.items():
        actual = sha256_file(package / relative)
        if actual != expected:
            raise RuntimeError(
                f"manifest content mismatch for {package / relative}: "
                f"{actual} != {expected}"
            )
    return {
        "manifest_sha256": actual_manifest_hash,
        "manifest_entries": len(listed),
        "internal_manifest": "PASS",
    }


def exact_process_gate(
    returncode: int, stderr: bytes, actual_stdout: bytes, expected_stdout: bytes
) -> bool:
    return returncode == 0 and stderr == b"" and actual_stdout == expected_stdout


def dependency_gate(sympy_version: str, mpmath_version: str) -> bool:
    return sympy_version == EXPECTED_SYMPY and mpmath_version == EXPECTED_MPMATH


def catchproof() -> dict[str, str]:
    probes = {
        "altered_manifest_hash_rejected": not manifest_hash_gate("0" * 64, "1" * 64),
        "altered_stdout_rejected": not exact_process_gate(0, b"", b"changed", b"frozen"),
        "nonzero_exit_rejected": not exact_process_gate(1, b"", b"frozen", b"frozen"),
        "stderr_rejected": not exact_process_gate(0, b"diagnostic", b"frozen", b"frozen"),
        "dependency_mismatch_rejected": not dependency_gate("0.0.0", EXPECTED_MPMATH),
    }
    failed = [name for name, passed in probes.items() if not passed]
    if failed:
        raise RuntimeError(f"catch-proof failure: {failed}")
    return {name: "PASS" for name in probes}


def replay_cas(repo: Path, work_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    environment = {
        "CUDA_VISIBLE_DEVICES": "",
        "HOME": str(work_root / "home"),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": str(Path(sys.executable).parent),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    (work_root / "home").mkdir()
    run_root = work_root / "cas_runs"
    run_root.mkdir()
    sequence = 0
    for group, relative_directory, expected_names in CAS_GROUPS:
        source_directory = repo / relative_directory
        actual_names = tuple(sorted(path.name for path in source_directory.glob("cas_*.py")))
        if actual_names != tuple(sorted(expected_names)):
            raise RuntimeError(
                f"{group} script inventory mismatch: "
                f"expected={sorted(expected_names)} actual={list(actual_names)}"
            )
        for name in expected_names:
            sequence += 1
            source = source_directory / name
            expected_output = source_directory / f"{source.stem}_out.txt"
            if not expected_output.is_file():
                raise RuntimeError(f"missing frozen output: {expected_output}")
            run_directory = run_root / f"{sequence:02d}_{group}_{source.stem}"
            run_directory.mkdir()
            copied_script = run_directory / source.name
            shutil.copyfile(source, copied_script)
            completed = subprocess.run(
                [sys.executable, "-I", "-B", str(copied_script)],
                cwd=run_directory,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=120,
            )
            expected_bytes = expected_output.read_bytes()
            passed = exact_process_gate(
                completed.returncode,
                completed.stderr,
                completed.stdout,
                expected_bytes,
            )
            result = {
                "sequence": sequence,
                "group": group,
                "script": source.relative_to(repo).as_posix(),
                "copied_script": copied_script.relative_to(work_root).as_posix(),
                "source_sha256": sha256_file(source),
                "expected_stdout_sha256": sha256_bytes(expected_bytes),
                "actual_stdout_sha256": sha256_bytes(completed.stdout),
                "returncode": completed.returncode,
                "stderr_bytes": len(completed.stderr),
                "stdout_exact": completed.stdout == expected_bytes,
                "result": "PASS" if passed else "FAIL",
            }
            results.append(result)
            if not passed:
                raise RuntimeError(f"CAS replay failed: {result}")
    if len(results) != 24:
        raise RuntimeError(f"CAS replay count mismatch: {len(results)} != 24")
    return results


def verify(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    work_root = args.work_root.resolve()
    report_path = args.report.resolve() if args.report else None
    if not (repo / ".git").exists():
        raise RuntimeError(f"not a repository root: {repo}")
    if work_root == repo or repo in work_root.parents:
        raise RuntimeError("work root must be outside the repository")
    if not work_root.is_dir() or any(work_root.iterdir()):
        raise RuntimeError("work root must be an existing empty directory")
    if report_path is not None:
        for _, relative, _, _ in PACKAGES:
            package = (repo / relative).resolve()
            if report_path == package or package in report_path.parents:
                raise RuntimeError("report path must be outside frozen packages")

    sympy_version = sympy.__version__
    mpmath_version = metadata.version("mpmath")
    venv_configuration = (Path(sys.prefix) / "pyvenv.cfg").read_text(
        encoding="utf-8"
    )
    system_site_disabled = "include-system-site-packages = false" in venv_configuration
    import_paths = [str(Path(entry).resolve()) for entry in sys.path if entry]
    clean_environment = {
        "virtual_environment": sys.prefix != sys.base_prefix,
        "parent_isolated_interpreter": sys.flags.isolated == 1,
        "user_site_disabled": not site.ENABLE_USER_SITE,
        "system_site_disabled": system_site_disabled,
        "repository_absent_from_import_path": str(repo) not in import_paths,
        "isolated_child_interpreter": True,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "import_paths": import_paths,
    }
    if not dependency_gate(sympy_version, mpmath_version):
        raise RuntimeError(
            f"dependency mismatch: sympy={sympy_version}, mpmath={mpmath_version}"
        )
    if not clean_environment["virtual_environment"]:
        raise RuntimeError("verifier is not running inside a virtual environment")
    if not clean_environment["parent_isolated_interpreter"]:
        raise RuntimeError("verifier parent interpreter is not isolated")
    if not clean_environment["user_site_disabled"]:
        raise RuntimeError("user-site packages are enabled")
    if not clean_environment["system_site_disabled"]:
        raise RuntimeError("system site-packages are enabled")
    if not clean_environment["repository_absent_from_import_path"]:
        raise RuntimeError("repository is present on the verifier import path")
    if clean_environment["cuda_visible_devices"] != "":
        raise RuntimeError("CUDA visibility must be empty")

    before: dict[str, Any] = {}
    manifests: dict[str, Any] = {}
    for label, relative, expected_hash, expected_entries in PACKAGES:
        package = repo / relative
        manifests[label] = parse_and_verify_manifest(
            package, expected_hash, expected_entries
        )
        before[label] = package_snapshot(package)

    catchproof_results = catchproof()
    cas_results = replay_cas(repo, work_root)

    after: dict[str, Any] = {}
    post_manifests: dict[str, Any] = {}
    for label, relative, expected_hash, expected_entries in PACKAGES:
        package = repo / relative
        post_manifests[label] = parse_and_verify_manifest(
            package, expected_hash, expected_entries
        )
        after[label] = package_snapshot(package)

    unchanged: dict[str, bool] = {}
    for label, _, _, _ in PACKAGES:
        unchanged[label] = before[label] == after[label]
        if not unchanged[label]:
            raise RuntimeError(f"package changed during verification: {label}")
        if manifests[label] != post_manifests[label]:
            raise RuntimeError(f"manifest state changed during verification: {label}")

    report: dict[str, Any] = {
        "result": "PASS",
        "mode": "CPU_ONLY_EXTERNAL_NON_MUTATING",
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "sympy": sympy_version,
        "mpmath": mpmath_version,
        "clean_environment": clean_environment,
        "work_root": str(work_root),
        "package_manifests": manifests,
        "package_state_before": {
            label: {
                "state_sha256": snapshot["state_sha256"],
                "file_count_including_manifest": snapshot[
                    "file_count_including_manifest"
                ],
            }
            for label, snapshot in before.items()
        },
        "package_state_after": {
            label: {
                "state_sha256": snapshot["state_sha256"],
                "file_count_including_manifest": snapshot[
                    "file_count_including_manifest"
                ],
            }
            for label, snapshot in after.items()
        },
        "package_unchanged": unchanged,
        "catchproof": catchproof_results,
        "cas_replays_passed": sum(row["result"] == "PASS" for row in cas_results),
        "cas_replays_expected": 24,
        "cas_results": cas_results,
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = verify(args)
        exit_code = 0
    except Exception as exc:  # fail closed while preserving a machine-readable record
        report = {
            "result": "FAIL",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        exit_code = 1
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.resolve().write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
