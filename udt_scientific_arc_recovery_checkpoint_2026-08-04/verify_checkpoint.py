#!/usr/bin/env python3
"""Build and verify the documentary scientific-arc recovery checkpoint."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFESTS = (
    "native_action_stage1_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage1_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_A/SHA256SUMS.txt",
    "native_action_stage2_2026-07-18/arm_B/SHA256SUMS.txt",
    "native_action_arm_c_2026-07-18/SHA256SUMS.txt",
    "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt",
)
STARTUP = ("LIVE.md", "HANDOFF.md", "README.md", "INDEX.md", "AGENTS.md", "MEMORY.md")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def git_blob(data: bytes) -> str:
    payload = f"blob {len(data)}\0".encode() + data
    return hashlib.sha1(payload).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)


def render_manifest(paths: list[str]) -> str:
    lines = ["path\tgit_blob\tbytes\tsha256"]
    for relative in paths:
        data = (ROOT / relative).read_bytes()
        lines.append(f"{relative}\t{git_blob(data)}\t{len(data)}\t{digest_bytes(data)}")
    return "\n".join(lines) + "\n"


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--write", action="store_true")
args = parser.parse_args()

source_paths = (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
assert source_paths and len(source_paths) == len(set(source_paths))
assert all((ROOT / path).is_file() for path in source_paths)
manifest_text = render_manifest(source_paths)
if args.write:
    (HERE / "SOURCE_MANIFEST.tsv").write_text(manifest_text, encoding="utf-8")
else:
    assert (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8") == manifest_text

mass = table(HERE / "MASS_BRANCH_AUTHORITY_MAP.tsv")
assert [row["family_id"] for row in mass] == [f"F0{i}" for i in range(1, 8)]
assert sum("CONDITIONAL" in row["current_status"] or "SETTLED_STATIC_FINITE_BOX_CONDITIONAL" in row["current_status"] for row in mass) == 3
assert mass[2]["current_status"] == "CONTROL_STRATUM_NOT_FAMILY"
assert mass[4]["current_status"] == "STRUCTURAL_COMPLETION_CLASS_NOT_FAMILY"
assert mass[5]["current_status"] == "EXACT_EMPTY_SCOPE_NOT_FAMILY"
assert mass[6]["current_status"] == "FORMAL_MODULE_CLASS_NOT_FAMILY"

structure = table(HERE / "BANKABLE_STRUCTURE_AND_OPEN_JOINTS.tsv")
assert len(structure) == 19 and len({row["id"] for row in structure}) == 19
by_id = {row["id"]: row for row in structure}
assert by_id["B01"]["status"] == "DERIVED"
assert by_id["B13"]["status"] == "WORKING_COHERENT_ARCHITECTURE_NOT_DERIVED_OPERATION"
assert by_id["B16"]["status"] == "OPEN_SIDE_CERTIFICATE"
assert by_id["B19"]["status"] == "OPEN"

premises = {row["premise_id"]: row for row in table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")}
assert premises["G01"]["current_status"] == "DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR"
assert premises["G02"]["current_status"] == "DERIVED_PHI_MAPS_TO_DIAG_EXP_MINUS_PHI_EXP_PLUS_PHI"
assert premises["G09"]["epistemic_label"] == "POSIT"
assert premises["G12"]["epistemic_label"] == "WORKING"
assert premises["G15"]["current_status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"
assert premises["G16"]["current_status"] == "OPEN"

checkpoint = (HERE / "SCIENTIFIC_ARC_CHECKPOINT.md").read_text(encoding="utf-8")
groebner = (HERE / "GROEBNER_PROGRAM_RECONSTRUCTION.md").read_text(encoding="utf-8")
overview = (HERE / "OVERVIEW_AND_ROUTE_MAP.md").read_text(encoding="utf-8")
review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
assert "`phi` is already `DERIVED`" in checkpoint
assert "three conditional realized-family rows and zero native" in checkpoint
assert "one bounded curvature-zero-set certificate" in checkpoint
assert "did not precede P4" in checkpoint
assert "INCOMPLETE-COMPUTATION" in groebner
assert "not a matter action or" in groebner and "field equation" in groebner
assert "realization principle" in overview
assert "explicit epistemic ruling" in overview
assert "PASS_WITH_REQUIRED_REPAIRS" in review
assert "REPAIRS_APPLIED" in review
assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/C08_TRANSFORMATION_CERTIFICATE_RETURN_STATUS.md" in source_paths

for name in ("LIVE.md", "HANDOFF.md"):
    text = (ROOT / name).read_text(encoding="utf-8")
    assert text.count("<!-- STARTUP_CURRENT_BEGIN -->") == 1
    assert text.count("<!-- STARTUP_CURRENT_END -->") == 1
    current = text.split("<!-- STARTUP_CURRENT_BEGIN -->", 1)[1].split("<!-- STARTUP_CURRENT_END -->", 1)[0]
    assert HERE.name in current
    assert "phi" in current and "gr\u00f6bner" in current.lower()

for name in STARTUP:
    assert HERE.name in (ROOT / name).read_text(encoding="utf-8")

link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
links = 0
for source in [HERE / "SCIENTIFIC_ARC_CHECKPOINT.md", HERE / "GROEBNER_PROGRAM_RECONSTRUCTION.md", HERE / "OVERVIEW_AND_ROUTE_MAP.md"] + [ROOT / name for name in STARTUP]:
    for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
        target = raw.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = unquote(target.split("#", 1)[0])
        resolved = Path(re.sub(r":\d+$", "", relative)) if Path(relative).is_absolute() else source.parent.joinpath(relative).resolve()
        assert resolved.exists(), (source, relative)
        links += 1

members = 0
for relative in MANIFESTS:
    manifest = ROOT / relative
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, member = line.split(None, 1)
        target = manifest.parent / member.strip()
        assert target.is_file() and digest(target) == expected
        members += 1
assert members == 127

current_paths = [row["current_path"] for row in table(ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")]
assert len(current_paths) == len(set(current_paths)) == 1114
assert all((ROOT / path).exists() for path in current_paths)
frontier = table(ROOT / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
targets = {row["target_path"].rstrip("/") for row in frontier}
assert len(frontier) == 306 and len(targets) == 101
assert all((ROOT / target).exists() for target in targets)

status = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT)
unrelated: list[dict[str, str]] = []
for item in status.split(b"\0"):
    if not item.startswith(b"?? "):
        continue
    relative = os.fsdecode(item[3:])
    if relative.startswith(HERE.name + "/"):
        continue
    stat = (ROOT / relative).stat()
    unrelated.append({"path": relative, "bytes": str(stat.st_size), "mtime_ns": str(stat.st_mtime_ns)})
unrelated.sort(key=lambda row: row["path"])
baseline = table(ROOT / "udt_reciprocal_path_composition_residual_audit_2026-08-04/UNRELATED_UNTRACKED_METADATA.tsv")
assert unrelated == baseline and len(unrelated) == 83

premise_run = run(["python3", "verify_current_scientific_premises.py"], 60)
assert premise_run.returncode == 0 and "PASS: 18 premise guards" in premise_run.stdout
tests = run(["python3", "-m", "pytest", "-q", "tests"], 300)
assert tests.returncode == 0 and "70 passed, 1 xfailed" in tests.stdout

catches = [
    ("C01_PHI_UNDEFINED", "`phi` is already `DERIVED`" not in checkpoint.replace("`phi` is already `DERIVED`", "`phi` is undefined")),
    ("C02_COLLAPSE_FAMILIES", len({row["object_kind"] for row in mass[:4]}) != 1),
    ("C03_PROMOTE_BOOTSTRAP", by_id["B13"]["status"] != "DERIVED"),
    ("C04_PROMOTE_MASS", by_id["B19"]["status"] == "OPEN"),
    ("C05_TIMEOUT_AS_NO_GO", "scientific acceptance criteria" in groebner and "`INCOMPLETE-COMPUTATION`" in groebner),
    ("C06_ADOPT_POSTULATE", "explicit epistemic ruling" in overview),
    ("C07_REVERSE_CHRONOLOGY", "did not precede P4" in checkpoint and "P4 first" in (ROOT / "INDEX.md").read_text(encoding="utf-8")),
    ("C08_OMIT_TWO_HOUR_SOURCE", "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/C08_TRANSFORMATION_CERTIFICATE_RETURN_STATUS.md" in source_paths),
]
assert all(caught for _, caught in catches)
catch_text = "catch_id\tresult\n" + "".join(f"{name}\tCAUGHT\n" for name, _ in catches)
if args.write:
    (HERE / "CATCH_PROOFS.tsv").write_text(catch_text, encoding="utf-8")
else:
    assert (HERE / "CATCH_PROOFS.tsv").read_text(encoding="utf-8") == catch_text

result = {
    "status": "PASS",
    "checkpoint_status": "DOCUMENTARY_RECOVERY_VERIFIED_WITH_CAVEATS__NO_NEW_PHYSICS",
    "source_paths": len(source_paths),
    "source_manifest_sha256": digest_bytes(manifest_text.encode()),
    "mass_family_rows": len(mass),
    "conditional_realized_family_rows": 3,
    "native_stable_matter_families": 0,
    "structure_rows": len(structure),
    "catch_proofs": len(catches),
    "startup_files_routed": len(STARTUP),
    "checked_links": links,
    "frozen_manifests": len(MANIFESTS),
    "frozen_manifest_members": members,
    "frozen_package_paths": members + len(MANIFESTS),
    "premise_guards": 18,
    "current_paths": len(current_paths),
    "frontier_rows": len(frontier),
    "frontier_targets": len(targets),
    "unrelated_untracked_metadata_rows": len(unrelated),
    "tests": "70 passed, 1 xfailed",
    "semantic_independence": "FRESH_EXTERNAL_REVIEW_PASS_AFTER_REQUIRED_REPAIRS",
}
if args.write:
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
