#!/usr/bin/env python3
"""Replay every current load-bearing A/B/C algebra check without mutating inputs."""

from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = HERE / "ALGEBRA_RERUN_OUTPUTS"


GROUPS = (
    (
        "stage1_A",
        REPO / "native_action_stage1_2026-07-18/arm_A/cold_output",
        {
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
        },
    ),
    (
        "stage1_B",
        REPO / "native_action_stage1_2026-07-18/arm_B/cold_output",
        {
            "cas_csn_decomposition.py",
            "cas_dual_reciprocity_uv.py",
            "cas_exponential_composition.py",
            "cas_metric_product_and_csn.py",
        },
    ),
    (
        "stage2_A",
        REPO / "native_action_stage2_2026-07-18/arm_A/D6_RETURN",
        {
            "cas_stage2_carrier_weight_source.py",
            "cas_stage2_mass_virial.py",
        },
    ),
    (
        "stage2_B",
        REPO / "native_action_stage2_2026-07-18/arm_B/D6_RETURN",
        {
            "cas_stage2_source_channel_identities.py",
            "cas_stage2_srel_sfol_conventions.py",
        },
    ),
    (
        "arm_C",
        REPO / "native_action_arm_c_2026-07-18/ARM_C_RETURN",
        {
            "cas_armc_boundary_charge.py",
            "cas_armc_carrier_covariance.py",
            "cas_armc_mass_virial.py",
            "cas_armc_unique_action_weights.py",
            "cas_armc_variation_domain.py",
        },
    ),
)


PACKAGE_MANIFESTS = (
    (
        "stage1_A",
        REPO / "native_action_stage1_2026-07-18/arm_A",
        "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
        29,
    ),
    (
        "stage1_B",
        REPO / "native_action_stage1_2026-07-18/arm_B",
        "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
        15,
    ),
    (
        "stage2_A",
        REPO / "native_action_stage2_2026-07-18/arm_A",
        "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
        13,
    ),
    (
        "stage2_B",
        REPO / "native_action_stage2_2026-07-18/arm_B",
        "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
        13,
    ),
    (
        "arm_C",
        REPO / "native_action_arm_c_2026-07-18",
        "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
        21,
    ),
)


SOURCE_ANCHORS = (
    (
        "controller",
        REPO / "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
        "9b7c172a395084bf9a7fede33a261de7a61ca7704c3650e9b7828f9ec814b668",
    ),
    (
        "C0",
        REPO / "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md",
        "6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192",
    ),
    (
        "C1",
        REPO / "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    ),
    (
        "arm_C_input_manifest",
        REPO / "UDT_NATIVE_ACTION_ARM_C_INPUT_SHA256SUMS_2026-07-18.txt",
        "010e7922423ab724467d94f6408425905fb872c5ccaebc5fa5941fc66080f2dc",
    ),
    (
        "A1_A6_manifest",
        REPO / "UDT_NATIVE_ACTION_STAGE2_A1_A6_SHA256SUMS_2026-07-18.txt",
        "85776969410e6dc8bee6b1aa901331dcc139e718dbdfd28c593df3f2054408b7",
    ),
    (
        "preregistration",
        REPO / "UDT_NATIVE_ACTION_FINAL_ADJUDICATION_PREREG_2026-07-18.md",
        "b8d4bd4bb48cfcfb51bc85fb82d6fdd816b6e6585dd1600fdea3093e39dba457",
    ),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def verify_package_manifest(package: Path) -> tuple[str, int, list[str]]:
    manifest = package / "SHA256SUMS.txt"
    failures: list[str] = []
    rows = manifest.read_text(encoding="utf-8").splitlines()
    for row in rows:
        expected, relative = row.split("  ", 1)
        relative = relative[2:] if relative.startswith("./") else relative
        target = package / relative
        if not target.is_file():
            failures.append(f"missing:{relative}")
        elif sha256_file(target) != expected:
            failures.append(f"hash:{relative}")
    return sha256_file(manifest), len(rows), failures


def write_integrity_record() -> None:
    rows: list[dict[str, object]] = []
    for label, package, expected_manifest_hash, expected_count in PACKAGE_MANIFESTS:
        actual_hash, actual_count, failures = verify_package_manifest(package)
        passed = (
            actual_hash == expected_manifest_hash
            and actual_count == expected_count
            and not failures
        )
        rows.append(
            {
                "kind": "package_manifest",
                "label": label,
                "path": package.relative_to(REPO).as_posix() + "/SHA256SUMS.txt",
                "expected_sha256": expected_manifest_hash,
                "actual_sha256": actual_hash,
                "expected_entries": expected_count,
                "actual_entries": actual_count,
                "internal_failures": ";".join(failures),
                "result": "PASS" if passed else "FAIL",
            }
        )
    for label, path, expected_hash in SOURCE_ANCHORS:
        actual_hash = sha256_file(path)
        rows.append(
            {
                "kind": "source_anchor",
                "label": label,
                "path": path.relative_to(REPO).as_posix(),
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "expected_entries": "",
                "actual_entries": "",
                "internal_failures": "",
                "result": "PASS" if actual_hash == expected_hash else "FAIL",
            }
        )
    with (HERE / "INPUT_INTEGRITY.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=tuple(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    failed = [row for row in rows if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"input integrity failure: {failed}")


def replay_algebra() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    replay_rows: list[dict[str, object]] = []
    sequence = 0
    for group, directory, expected_names in GROUPS:
        actual_names = {path.name for path in directory.glob("cas_*.py")}
        if actual_names != expected_names:
            raise SystemExit(
                f"{group} script inventory mismatch: "
                f"missing={sorted(expected_names - actual_names)} "
                f"extra={sorted(actual_names - expected_names)}"
            )
        for name in sorted(expected_names):
            sequence += 1
            script = directory / name
            expected_output = directory / f"{script.stem}_out.txt"
            if not expected_output.is_file():
                raise SystemExit(f"missing frozen output for {script}")

            source = script.read_text(encoding="utf-8")
            compile(source, str(script), "exec")
            environment = os.environ.copy()
            environment["CUDA_VISIBLE_DEVICES"] = ""
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment["PYTHONHASHSEED"] = "0"
            result = subprocess.run(
                [sys.executable, script.name],
                cwd=directory,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                check=False,
            )
            replay_name = f"{sequence:02d}_{group}_{script.stem}_out.txt"
            replay_path = OUTPUTS / replay_name
            replay_path.write_bytes(result.stdout)
            expected_bytes = expected_output.read_bytes()
            passed = (
                result.returncode == 0
                and result.stderr == b""
                and result.stdout == expected_bytes
            )
            replay_rows.append(
                {
                    "sequence": sequence,
                    "group": group,
                    "script": script.relative_to(REPO).as_posix(),
                    "frozen_output": expected_output.relative_to(REPO).as_posix(),
                    "replay_output": replay_path.relative_to(HERE).as_posix(),
                    "compile": "PASS",
                    "exit_code": result.returncode,
                    "stderr_bytes": len(result.stderr),
                    "stdout_exact_match": "PASS" if result.stdout == expected_bytes else "FAIL",
                    "script_sha256": sha256_file(script),
                    "frozen_output_sha256": sha256_bytes(expected_bytes),
                    "replay_output_sha256": sha256_bytes(result.stdout),
                    "result": "PASS" if passed else "FAIL",
                }
            )
    if sequence != 24:
        raise SystemExit(f"expected 24 scripts, found {sequence}")
    with (HERE / "ALGEBRA_RERUN.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=tuple(replay_rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(replay_rows)
    failed = [row for row in replay_rows if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"algebra replay failure: {failed}")


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    write_integrity_record()
    replay_algebra()
    completed = datetime.now(timezone.utc).isoformat()
    (HERE / "RERUN_METADATA.txt").write_text(
        "\n".join(
            (
                f"started_utc={started}",
                f"completed_utc={completed}",
                f"python={sys.version.split()[0]}",
                "execution=CPU_ONLY",
                "gpu_exposed_to_child_scripts=NO",
                "package_manifests=PASS_5_OF_5",
                "source_anchors=PASS_6_OF_6",
                "algebra_scripts=PASS_24_OF_24",
                "stdout_reproduction=BYTE_EXACT_24_OF_24",
                "certification_limit=ENCODED_ALGEBRA_ONLY",
                "",
            )
        ),
        encoding="utf-8",
    )
    print("PASS package manifests 5/5")
    print("PASS source anchors 6/6")
    print("PASS algebra scripts 24/24")
    print("PASS byte-exact stdout 24/24")
    print("CPU_ONLY true")


if __name__ == "__main__":
    main()
