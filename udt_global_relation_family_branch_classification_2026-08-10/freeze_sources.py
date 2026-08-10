#!/usr/bin/env python3
"""Freeze the preregistered branch-package evidence before adjudication."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGES = (
    "udt_global_metric_assembly_atlas_2026-07-22",
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27",
    "udt_complete_screen_response_branch_atlas_2026-07-28",
    "udt_general_screen_complete_cell_atlas_2026-07-28",
    "udt_completion_parameterized_local_fiber_audit_2026-08-01",
    "udt_branchwise_projector_holonomy_census_2026-08-01",
    "udt_global_phi_ownership_overlap_audit_2026-08-05",
    "udt_complete_pair_phi_orchestra_audit_2026-08-05",
    "udt_reciprocal_calibration_state_solder_audit_2026-08-09",
    "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09",
    "udt_calibrated_pair_map_owner_atlas_2026-08-09",
    "udt_founding_pair_relation_functor_ownership_audit_2026-08-09",
    "udt_three_observer_overlap_calibration_carry_audit_2026-08-10",
)
PRIMARY = {"AUDIT_REPORT.md", "EXACT_DERIVATION.md", "STATUS_LEDGER.tsv", "DERIVATION_RESULT.json"}
CONTROLS = ("CURRENT_SCIENTIFIC_PREMISES.tsv", "CURRENT_RESEARCH_PROGRAM.md")


def tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    paths: list[Path] = []
    for package in PACKAGES:
        directory = ROOT / package
        assert directory.is_dir(), directory
        for path in sorted(directory.iterdir()):
            if not path.is_file() or not tracked(path):
                continue
            if path.name in PRIMARY or path.suffix == ".tsv":
                paths.append(path)
    paths.extend(ROOT / name for name in CONTROLS)
    relative = [path.relative_to(ROOT).as_posix() for path in paths]
    assert len(relative) == len(set(relative))
    assert not any(path.startswith("udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/") for path in relative)

    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        fields = ("path", "source_ref", "blob", "sha256", "size")
        writer = csv.DictWriter(stream, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for path, rel in zip(paths, relative):
            data = subprocess.check_output(["git", "show", f"{head}:{rel}"], cwd=ROOT)
            writer.writerow(
                {
                    "path": rel,
                    "source_ref": f"{head}:{rel}",
                    "blob": subprocess.check_output(
                        ["git", "rev-parse", f"{head}:{rel}"], cwd=ROOT, text=True
                    ).strip(),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                }
            )
    print(f"PASS: froze {len(paths)} source files from {head}")


if __name__ == "__main__":
    main()
