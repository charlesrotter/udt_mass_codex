#!/usr/bin/env python3
"""Independent, fail-closed verifier for the R1G provenance audit.

This implementation does not import the R1G freezer or builder.  It rebuilds
candidate sets and Git history directly from the fixed origin/grok base and
checks the resulting audit overlay, frozen packages, navigation, test record,
and dirty-checkout metadata.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import re
import stat
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


BASE = "8015342a81b2d27cc310dde95ab7f386c6441a77"
PREREG = "7078b4bed9c7e42f3de343874e3b667e3facac10"
CORRECTION_PREREG = "5c2cd3c"
BOUNDARY = "f7664786d1e2340262ea5aa22336cf0c2f8b0dfc"
BOUNDARY_PARENT = "78939836326cb822e22b2a72bfd8097365185aa6"
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
EXPECTED_FAMILIES = {
    "876ea84a656b5428305b7ca5957184b32dd7fc3a": 1,
    "5177aea9252af40278bcdea65569039de5309893": 11,
    "20579ee944802b337195b43d55d1872a3e5a2e4e": 14,
    "24671fabfc1e2e21a1d08c1b24ae4639c9e83263": 8,
    "95f2d73efadfef2569189ac2e1c25547817866fb": 2,
    "2836cc8694db1967ba0d03ee43184ab87238ae05": 11,
    "add2f22217576fa96308c68bc459e8e271affddf": 14,
    "48b50d402960f92aaa345daee26ae7dd14dca0c0": 14,
    "4ee798243b0911bdd8360710aa84ca75aefae039": 14,
    "883a484b7385e8bd21d305f237236c6a66e0c340": 11,
    "7a09b800a2f3f5a375c21cb66fdc8f173a23dcb7": 6,
    "1c7ff8f0455bbf8502bb5572d06e6ba44c58f4d3": 7,
    "5a82fbbd657402126c8f74af6b70bab92d02e274": 5,
    "34d1b6b1c4469f1fccf77eb6a212fc90cc766ee2": 1,
    "6cb6e306c0549f14f775ac956ffde7cc119267c9": 2,
}
MIXED_CANDIDATES = {"phi_source_derivation.py", "homog_alpha_test.py"}
READOUT_ONLY_CANDIDATES = {
    "cascade_bv16_cas.py",
    "cascade_or_energy_cas.py",
    "verify_universe_bv2_f_einstein.py",
}
C12_READOUT_FILES = {
    "cascade_bv16_cas.py",
    "cascade_bv16_rungs.py",
    "cascade_or_energy_cas.py",
    "cascade_or_energy_numeric.py",
    "cascade_or_energy_rung1_and_alignment.py",
}
OPEN_CANDIDATES = {"verify_redshift_profile_derivation.py"}
ALLOWED_PROVENANCE = {"PRE_NATIVE", "NATIVE_2026-07-01", "MIXED", "OPEN"}
ALLOWED_LIFECYCLE = {"ACTIVE", "SUPERSEDED", "HISTORICAL", "FROZEN"}
ALLOWED_OWNERS = {"FOUNDATIONS", "NATIVE_ACTION", "PARTICLE_MASS", "MACRO"}


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(repo: Path, command: list[str], *, binary: bool = False, check: bool = True):
    result = subprocess.run(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if check and result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{error}")
    return result


def git(repo: Path, *args: str, binary: bool = False, check: bool = True):
    result = run(repo, ["git", *args], binary=binary, check=check)
    return result.stdout if check else result


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def expect(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise AssertionError(f"expected {code}, got {exc.code}") from exc
    raise AssertionError(f"catch-proof accepted corruption; expected {code}")


def path_history(repo: Path, path: str) -> list[str]:
    return [line for line in str(git(repo, "log", "--format=%H", "--", path)).splitlines() if line]


def history_record(repo: Path, path: str) -> dict[str, str]:
    lines = [
        line.split("\t", 2)
        for line in str(git(repo, "log", "--format=%H%x09%aI%x09%cI", "--", path)).splitlines()
        if line
    ]
    if not lines:
        raise GateError("MISSING_HISTORY", path)
    latest = lines[0]
    introducing = lines[-1]
    return {
        "introducing_commit": introducing[0],
        "introducing_author_date": introducing[1],
        "introducing_commit_date": introducing[2],
        "first_commit": introducing[0],
        "first_commit_date": introducing[2],
        "last_commit": latest[0],
        "last_commit_date": latest[2],
    }


def validate_provenance_row(repo: Path, row: dict[str, str]) -> None:
    provenance = row.get("operator_provenance", "")
    lifecycle = row.get("scientific_lifecycle", "")
    destination = row.get("corrected_destination_proposal", "")
    evidence = row.get("operator_lineage_evidence", "")
    pre_commit = row.get("pre_native_lineage_commit", "")
    path = row.get("current_path", "")
    imported = row.get("imported_action_or_coupling", "")
    readout = row.get("comparison_readout", "")
    role = row.get("role", "")
    if provenance not in ALLOWED_PROVENANCE:
        raise GateError("INVALID_PROVENANCE_LABEL", path)
    if lifecycle not in ALLOWED_LIFECYCLE:
        raise GateError("INVALID_LIFECYCLE_LABEL", path)
    if row.get("primary_owner", "") not in ALLOWED_OWNERS:
        raise GateError("INVALID_OWNER", path)
    if not row.get("migration_safety", ""):
        raise GateError("MISSING_MIGRATION_SAFETY", path)
    if not imported or not readout or not role:
        raise GateError("MISSING_SEPARATE_PROVENANCE_AXIS", path)
    if role == "REFERENCE_ONLY":
        if imported != "NONE":
            raise GateError("IMPORTED_COUPLING_MISLABELED_REFERENCE_ONLY", path)
        if readout == "NONE" or "COMPARISON_READOUT:" not in evidence or "ROLE:REFERENCE_ONLY" not in evidence:
            raise GateError("READOUT_DISCLOSURE_MISSING", path)
        if provenance != "NATIVE_2026-07-01":
            raise GateError("REFERENCE_ONLY_READOUT_DEMOTED_NATIVE", path)
    elif readout != "NONE":
        raise GateError("READOUT_ROLE_MISSING", path)
    if role == "ENTERS_TESTED_ACTION_AND_PHI_EOM":
        if imported == "NONE":
            raise GateError("IMPORTED_COUPLING_DISCLOSURE_MISSING", path)
        if provenance != "MIXED":
            raise GateError("IMPORTED_COUPLING_NOT_MIXED", path)
    elif imported != "NONE":
        raise GateError("IMPORTED_COUPLING_ROLE_MISSING", path)
    if provenance == "PRE_NATIVE":
        if not pre_commit or not evidence:
            raise GateError("PRE_NATIVE_EVIDENCE_MISSING", path)
        if pre_commit not in path_history(repo, path):
            raise GateError("PRE_NATIVE_LINEAGE_NOT_IN_PATH_HISTORY", path)
        ancestor = git(repo, "merge-base", "--is-ancestor", pre_commit, BOUNDARY_PARENT, check=False)
        if ancestor.returncode:
            raise GateError("PRE_NATIVE_LINEAGE_NOT_ANCESTRAL", path)
    elif pre_commit:
        raise GateError("SPURIOUS_PRE_NATIVE_LINEAGE", path)
    if destination.startswith("archive/pre_2026-07-01/") and provenance != "PRE_NATIVE":
        raise GateError("INVALID_PRE_ARCHIVE_DESTINATION", path)
    if provenance in {"NATIVE_2026-07-01", "MIXED"} and BOUNDARY[:7] not in evidence and BOUNDARY not in evidence:
        raise GateError("NATIVE_LINEAGE_EVIDENCE_MISSING", path)


def validate_candidate_table(repo: Path, table: list[dict[str, str]], expected: list[dict[str, str]]) -> None:
    expected_paths = [row["current_path"] for row in expected]
    actual_paths = [row["current_path"] for row in table]
    if len(table) != 32 or len(set(actual_paths)) != 32 or set(actual_paths) != set(expected_paths):
        raise GateError("CANDIDATE_COVERAGE", f"rows={len(table)} unique={len(set(actual_paths))}")
    expected_by_path = {row["current_path"]: row for row in expected}
    for row in table:
        path = row["current_path"]
        source = expected_by_path[path]
        record = history_record(repo, path)
        for field in ("introducing_commit", "first_commit", "first_commit_date", "last_commit", "last_commit_date"):
            if row[field] != record[field] or row[field] != source[field]:
                raise GateError("HISTORY_MISMATCH", f"{path}:{field}")
        blob = str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        if row["git_blob_oid"] != blob or row["sha256"] != sha(payload):
            raise GateError("CONTENT_IDENTITY_MISMATCH", path)
        expected_provenance = "MIXED" if path in MIXED_CANDIDATES else "OPEN" if path in OPEN_CANDIDATES else "NATIVE_2026-07-01"
        if row["operator_provenance"] != expected_provenance:
            raise GateError("PROVENANCE_ADJUDICATION_MISMATCH", path)
        if row["scientific_lifecycle"] != "HISTORICAL":
            raise GateError("LIFECYCLE_ADJUDICATION_MISMATCH", path)
        if row["r1e_destination"] != source["destination"]:
            raise GateError("R1E_DESTINATION_MISMATCH", path)
        if path in READOUT_ONLY_CANDIDATES:
            expected_axes = ("NONE", "GR_EINSTEIN_TENSOR;MISNER_SHARP", "REFERENCE_ONLY")
        elif path in MIXED_CANDIDATES:
            expected_axes = ("ALPHA_MINUS_2_GR_PHYSICAL_METRIC;NONZERO_ALPHA_FREE", "NONE", "ENTERS_TESTED_ACTION_AND_PHI_EOM")
        else:
            expected_axes = ("NONE", "NONE", "NONE")
        actual_axes = (row["imported_action_or_coupling"], row["comparison_readout"], row["role"])
        if actual_axes != expected_axes:
            raise GateError("SEPARATE_PROVENANCE_AXIS_MISMATCH", path)
        validate_provenance_row(repo, row)


def validate_affected(repo: Path, table: list[dict[str, str]], expected_paths: set[str]) -> None:
    actual = [row["current_path"] for row in table]
    if len(table) != 121 or len(set(actual)) != 121 or set(actual) != expected_paths:
        raise GateError("AFFECTED_CASCADE_COVERAGE", f"rows={len(table)} unique={len(set(actual))}")
    family_counts = Counter(row["introducing_commit"] for row in table)
    if dict(family_counts) != EXPECTED_FAMILIES:
        raise GateError("FAMILY_CENSUS_MISMATCH", str(dict(family_counts)))
    for row in table:
        path = row["current_path"]
        record = history_record(repo, path)
        for field in ("introducing_commit", "introducing_commit_date", "last_commit", "last_commit_date"):
            if row[field] != record[field]:
                raise GateError("HISTORY_MISMATCH", f"{path}:{field}")
        if row["operator_provenance"] != "NATIVE_2026-07-01":
            raise GateError("PROVENANCE_ADJUDICATION_MISMATCH", path)
        expected_axes = (("NONE", "GR_EINSTEIN_TENSOR;MISNER_SHARP", "REFERENCE_ONLY")
                         if path in C12_READOUT_FILES else ("NONE", "NONE", "NONE"))
        actual_axes = (row["imported_action_or_coupling"], row["comparison_readout"], row["role"])
        if actual_axes != expected_axes:
            raise GateError("SEPARATE_PROVENANCE_AXIS_MISMATCH", path)
        expected_lifecycle = "FROZEN" if row["introducing_commit"] == "34d1b6b1c4469f1fccf77eb6a212fc90cc766ee2" else "HISTORICAL"
        if row["scientific_lifecycle"] != expected_lifecycle:
            raise GateError("LIFECYCLE_ADJUDICATION_MISMATCH", path)
        validate_provenance_row(repo, row)


def validate_readout_audit(repo: Path, table: list[dict[str, str]]) -> None:
    expected = C12_READOUT_FILES | {"verify_universe_bv2_f_einstein.py"} | MIXED_CANDIDATES
    paths = [row["current_path"] for row in table]
    if len(table) != 8 or len(set(paths)) != 8 or set(paths) != expected:
        raise GateError("READOUT_AUDIT_COVERAGE", f"rows={len(table)} unique={len(set(paths))}")
    by_path = {row["current_path"]: row for row in table}
    for path in C12_READOUT_FILES | {"verify_universe_bv2_f_einstein.py"}:
        row = by_path[path]
        if (row["imported_action_or_coupling"], row["comparison_readout"], row["role"], row["operator_provenance"]) != (
            "NONE", "GR_EINSTEIN_TENSOR;MISNER_SHARP", "REFERENCE_ONLY", "NATIVE_2026-07-01"
        ):
            raise GateError("READOUT_AUDIT_RULING", path)
    for path in MIXED_CANDIDATES:
        row = by_path[path]
        if row["comparison_readout"] != "NONE" or row["role"] != "ENTERS_TESTED_ACTION_AND_PHI_EOM" or row["operator_provenance"] != "MIXED":
            raise GateError("ALPHA_COUPLING_AUDIT_RULING", path)

    bv16 = (repo / "cascade_bv16_cas.py").read_text(encoding="utf-8")
    bv16_native, bv16_readout = bv16.split("# ================= Y3(i): Einstein tensor from scratch, OFF-SHELL", 1)
    if "L = L_geo - U" not in bv16_native or "EL_phi" not in bv16_native or "EL_rho" not in bv16_native:
        raise GateError("NATIVE_ACTION_CHAIN_MISSING", "cascade_bv16_cas.py")
    if "Gtt_mixed" in bv16_native or "Ric4" in bv16_native or "Gtt_mixed" not in bv16_readout:
        raise GateError("GR_READOUT_FEEDBACK", "cascade_bv16_cas.py")

    energy = (repo / "cascade_or_energy_cas.py").read_text(encoding="utf-8")
    energy_native, energy_readout = energy.split("# ---------------------------------------------------------------- C10: OFF-SHELL Misner-Sharp identity via G^t_t", 1)
    if "L = L_banked" not in energy_native or "EL_phi" not in energy_native or "EL_rho" not in energy_native:
        raise GateError("NATIVE_ACTION_CHAIN_MISSING", "cascade_or_energy_cas.py")
    if "Gtt_mix" in energy_native or "Ric4" in energy_native or "Gtt_mix" not in energy_readout:
        raise GateError("GR_READOUT_FEEDBACK", "cascade_or_energy_cas.py")

    verify = (repo / "verify_universe_bv2_f_einstein.py").read_text(encoding="utf-8")
    if "# on-shell substitutions (native EOMs with source sigma)" not in verify:
        raise GateError("NATIVE_ACTION_CHAIN_MISSING", "verify_universe_bv2_f_einstein.py")
    native_block = verify.split("# on-shell substitutions (native EOMs with source sigma)", 1)[1].split("# (ii)", 1)[0]
    if "phipp =" not in native_block or "rhopp =" not in native_block or "Gmix" in native_block:
        raise GateError("GR_READOUT_FEEDBACK", "verify_universe_bv2_f_einstein.py")

    for path, readout_marker in {
        "cascade_bv16_rungs.py": "# MS mass",
        "cascade_or_energy_numeric.py": "# Misner-Sharp route",
        "cascade_or_energy_rung1_and_alignment.py": "m = 0.5 * rho",
    }.items():
        source = (repo / path).read_text(encoding="utf-8")
        if "shoot(" not in source or readout_marker not in source or source.index("shoot(") > source.index(readout_marker):
            raise GateError("GR_READOUT_FEEDBACK", path)

    phi_source = (repo / "phi_source_derivation.py").read_text(encoding="utf-8")
    required_phi = ["grr = sp.exp(alpha*phi)", "L2 =", "grr*Grr", "sp.diff(integrand, phi)", "alpha * xi * e^{alpha φ}"]
    if not all(token in phi_source for token in required_phi):
        raise GateError("IMPORTED_COUPLING_NOT_IN_ACTION", "phi_source_derivation.py")
    homog = (repo / "homog_alpha_test.py").read_text(encoding="utf-8")
    if "weight = alpha * sp.exp(alpha*phi) * rho**2" not in homog or "I_req = sp.simplify(R / weight)" not in homog:
        raise GateError("IMPORTED_COUPLING_NOT_IN_ACTION", "homog_alpha_test.py")


def validate_links(repo: Path) -> int:
    sources = [repo / "README.md"]
    sources += sorted((repo / "research").rglob("*.md"))
    sources += sorted((repo / "reorganization_r1g").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    count = 0
    for source in sources:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not source.parent.joinpath(target).resolve().exists():
                raise AssertionError(f"broken link: {source.relative_to(repo)}:{raw}")
            count += 1
    return count


def dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all", binary=True))
    records = raw.split(b"\0")
    result: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8); code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9); code, raw_path = fields[1].decode(), fields[9]; index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10); code, raw_path = fields[1].decode(), fields[10]
        elif marker in {b"?", b"!"}:
            code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise AssertionError(f"unknown status record: {record[:40]!r}")
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (repo / path).lstat()
        kind = "regular_file" if stat.S_ISREG(info.st_mode) else "directory" if stat.S_ISDIR(info.st_mode) else "symlink" if stat.S_ISLNK(info.st_mode) else "other"
        result[path] = (code, info.st_size, kind)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    audit = repo / "reorganization_r1g"

    correction_paths = [line for line in str(git(repo, "show", "--format=", "--name-only", CORRECTION_PREREG)).splitlines() if line]
    if correction_paths != ["reorganization_r1g/R1G_READOUT_PROVENANCE_CORRECTION_PREREGISTRATION.md"]:
        raise AssertionError("correction preregistration commit scope mismatch")
    if git(repo, "merge-base", "--is-ancestor", CORRECTION_PREREG, "HEAD", check=False).returncode:
        raise AssertionError("correction preregistration is not an ancestor of HEAD")

    if str(git(repo, "rev-parse", f"{BOUNDARY}^" )).strip() != BOUNDARY_PARENT:
        raise AssertionError("native-field-equation boundary parent mismatch")
    if git(repo, "merge-base", "--is-ancestor", BOUNDARY, BASE, check=False).returncode:
        raise AssertionError("boundary is not an ancestor of the audit base")
    boundary_subject = str(git(repo, "show", "-s", "--format=%s", BOUNDARY)).strip()
    boundary_date = str(git(repo, "show", "-s", "--format=%cI", BOUNDARY)).strip()
    boundary_names = set(str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", BOUNDARY)).splitlines())
    if boundary_date[:10] != "2026-07-01" or "Native UDT field equations derived" not in boundary_subject:
        raise AssertionError("boundary subject/date mismatch")
    if not {"native_field_equations_constrained_two_player_results.md", "verify_native_fieldeq.py"} <= boundary_names:
        raise AssertionError("boundary payload mismatch")
    semantic = (repo / "native_field_equations_constrained_two_player_results.md").read_text(encoding="utf-8")
    ledger_text = (repo / "branch_operator_contamination_ledger.md").read_text(encoding="utf-8")
    charter_text = (repo / "PURSUIT_CHARTER_2026-07-04.md").read_text(encoding="utf-8")
    semantic_flat = " ".join(semantic.split())
    if "supersedes the live two-player scalar-tensor frame" not in semantic_flat or "as the NATIVE frame" not in semantic_flat:
        raise AssertionError("native boundary semantic evidence missing")
    if "CERTIFIED native operator" not in ledger_text or "geometric-source" not in ledger_text or "native field equations" not in charter_text.lower():
        raise AssertionError("boundary corroboration missing")

    classifier = bytes(git(repo, "show", f"{BASE}:reorganization_r1c/build_r1c_lane_overlay.py", binary=True)).decode()
    bug = 'if lower.startswith(("cascade_", "p1_", "p2_", "p3_", "p4_", "p5_", "weld_", "angular_")):'
    if bug not in classifier or 'return "LEGACY_FROZEN", "PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE"' not in classifier:
        raise AssertionError("R1C prefix bug was not independently reproduced")

    plan = rows(repo / "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv")
    expected_candidates = [row for row in plan if row["batch_id"] in {"B02_LEGACY_STANDALONE_ALGEBRA_A", "B03_LEGACY_STANDALONE_ALGEBRA_B"}]
    if Counter(row["batch_id"] for row in expected_candidates) != Counter({"B02_LEGACY_STANDALONE_ALGEBRA_A": 18, "B03_LEGACY_STANDALONE_ALGEBRA_B": 14}):
        raise AssertionError("B02/B03 plan count mismatch")
    for row in expected_candidates:
        row.update(history_record(repo, row["current_path"]))
    b02_dates = [row["first_commit_date"][:10] for row in expected_candidates if row["batch_id"].startswith("B02")]
    b03_dates = [row["first_commit_date"][:10] for row in expected_candidates if row["batch_id"].startswith("B03")]
    if (min(b02_dates), max(b02_dates), min(b03_dates), max(b03_dates)) != ("2026-07-02", "2026-07-07", "2026-07-02", "2026-07-08"):
        raise AssertionError("B02/B03 introducing-date range mismatch")

    ownership = rows(repo / "research/_registry/ROOT_OWNERSHIP.tsv")
    all_cascade = [row for row in ownership if Path(row["current_path"]).name.lower().startswith("cascade_")]
    affected_source = [
        row for row in all_cascade
        if row["primary_owner"] == "LEGACY_FROZEN"
        and row["ownership_evidence"] == "PRE_NATIVE_FAMILY+R0_HISTORICAL_EVIDENCE"
    ]
    if len(all_cascade) != 138 or len(affected_source) != 121:
        raise AssertionError(f"cascade census mismatch: all={len(all_cascade)} affected={len(affected_source)}")
    expected_affected = {row["current_path"] for row in affected_source}
    affected_history = [history_record(repo, path) for path in sorted(expected_affected)]
    intro_dates = Counter(row["introducing_commit_date"][:10] for row in affected_history)
    if intro_dates != Counter({"2026-07-02": 61, "2026-07-03": 60}):
        raise AssertionError(f"affected introducing dates mismatch: {intro_dates}")

    candidate_table = rows(audit / "B02_B03_ADJUDICATION.tsv")
    affected_table = rows(audit / "AFFECTED_CASCADE_FILE_CENSUS.tsv")
    readout_audit = rows(audit / "READOUT_PROVENANCE_CORRECTION_AUDIT.tsv")
    validate_candidate_table(repo, candidate_table, expected_candidates)
    validate_affected(repo, affected_table, expected_affected)
    validate_readout_audit(repo, readout_audit)
    candidate_provenance = Counter(row["operator_provenance"] for row in candidate_table)
    affected_provenance = Counter(row["operator_provenance"] for row in affected_table)
    if candidate_provenance != Counter({"NATIVE_2026-07-01": 29, "MIXED": 2, "OPEN": 1}):
        raise AssertionError(f"candidate provenance totals mismatch: {candidate_provenance}")
    if affected_provenance != Counter({"NATIVE_2026-07-01": 121}):
        raise AssertionError(f"affected provenance totals mismatch: {affected_provenance}")

    summary = rows(audit / "AFFECTED_CASCADE_FAMILY_SUMMARY.tsv")
    if len(summary) != 15 or {row["introducing_commit"]: int(row["file_count"]) for row in summary} != EXPECTED_FAMILIES:
        raise AssertionError("family summary mismatch")
    if any(row["destination_root_proposal"].startswith("archive/pre_2026-07-01/") for row in summary):
        raise AssertionError("family summary retained invalid pre-native destination")
    c12 = next(row for row in summary if row["family_id"] == "C12_ENERGY_ORIENTATION")
    if (c12["operator_provenance"], c12["imported_action_or_coupling"], c12["comparison_readout"], c12["role"]) != (
        "NATIVE_2026-07-01", "NONE", "GR_EINSTEIN_TENSOR;MISNER_SHARP", "REFERENCE_ONLY"
    ):
        raise AssertionError("C12 family readout/provenance separation mismatch")

    rules = json.loads((audit / "CORRECTED_CLASSIFIER_RULES.json").read_text(encoding="utf-8"))
    required_axes = {"operator_provenance", "imported_action_or_coupling", "comparison_readout", "scientific_lifecycle", "path_migration_safety"}
    if set(rules["separate_axes"]) != required_axes:
        raise AssertionError("corrected classifier axes mismatch")
    rule_effects = {row["rule"]: row["effect"] for row in rules["rules_in_precedence_order"]}
    if "MIXED only" not in rule_effects.get("mixed_lineage", "") or "REFERENCE_ONLY" not in rule_effects.get("reference_only_readout", ""):
        raise AssertionError("corrected classifier readout rule mismatch")

    bad_post_july = copy.deepcopy(candidate_table[0])
    bad_post_july["operator_provenance"] = "PRE_NATIVE"
    bad_post_july["pre_native_lineage_commit"] = ""
    bad_post_july["corrected_destination_proposal"] = "archive/pre_2026-07-01/" + bad_post_july["current_path"]
    valid_fixture = copy.deepcopy(candidate_table[0])
    valid_fixture.update({
        "current_path": "LIVE.md",
        "operator_provenance": "PRE_NATIVE",
        "operator_lineage_evidence": "explicit path-specific operator record",
        "pre_native_lineage_commit": BOUNDARY_PARENT,
        "corrected_destination_proposal": "archive/pre_2026-07-01/LIVE.md",
        "primary_owner": "FOUNDATIONS",
        "scientific_lifecycle": "HISTORICAL",
    })
    validate_provenance_row(repo, valid_fixture)
    removed_evidence = copy.deepcopy(valid_fixture)
    removed_evidence["pre_native_lineage_commit"] = ""
    native_pre_destination = copy.deepcopy(candidate_table[0])
    native_pre_destination["corrected_destination_proposal"] = "archive/pre_2026-07-01/" + native_pre_destination["current_path"]
    missing_candidate = candidate_table[:-1]
    duplicate_candidate = copy.deepcopy(candidate_table)
    duplicate_candidate[-1]["current_path"] = duplicate_candidate[0]["current_path"]
    readout_row = copy.deepcopy(next(row for row in candidate_table if row["current_path"] == "cascade_bv16_cas.py"))
    demoted_readout = copy.deepcopy(readout_row)
    demoted_readout["operator_provenance"] = "MIXED"
    deleted_readout_disclosure = copy.deepcopy(readout_row)
    deleted_readout_disclosure["comparison_readout"] = "NONE"
    imported_as_reference = copy.deepcopy(next(row for row in candidate_table if row["current_path"] == "phi_source_derivation.py"))
    imported_as_reference.update({
        "operator_provenance": "NATIVE_2026-07-01",
        "comparison_readout": "GR_EINSTEIN_TENSOR;MISNER_SHARP",
        "role": "REFERENCE_ONLY",
    })
    catchproof = {
        "post_july_cascade_without_lineage_rejected": expect("PRE_NATIVE_EVIDENCE_MISSING", lambda: validate_provenance_row(repo, bad_post_july)),
        "removing_pre_native_lineage_evidence_rejected": expect("PRE_NATIVE_EVIDENCE_MISSING", lambda: validate_provenance_row(repo, removed_evidence)),
        "pre_native_destination_without_pre_native_provenance_rejected": expect("INVALID_PRE_ARCHIVE_DESTINATION", lambda: validate_provenance_row(repo, native_pre_destination)),
        "missing_candidate_rejected": expect("CANDIDATE_COVERAGE", lambda: validate_candidate_table(repo, missing_candidate, expected_candidates)),
        "duplicate_candidate_rejected": expect("CANDIDATE_COVERAGE", lambda: validate_candidate_table(repo, duplicate_candidate, expected_candidates)),
        "reference_only_gr_readout_demotion_rejected": expect("REFERENCE_ONLY_READOUT_DEMOTED_NATIVE", lambda: validate_provenance_row(repo, demoted_readout)),
        "deleted_readout_disclosure_rejected": expect("READOUT_DISCLOSURE_MISSING", lambda: validate_provenance_row(repo, deleted_readout_disclosure)),
        "imported_action_coupling_as_reference_only_rejected": expect("IMPORTED_COUPLING_MISLABELED_REFERENCE_ONLY", lambda: validate_provenance_row(repo, imported_as_reference)),
    }

    outside_diff = str(git(repo, "diff", "--name-only", BASE, "--", ".", ":(exclude)reorganization_r1g"))
    if outside_diff.strip():
        raise AssertionError(f"non-R1G tracked mutation: {outside_diff}")
    status = str(git(repo, "status", "--porcelain=v1", "--untracked-files=all"))
    for line in status.splitlines():
        path = line[3:]
        if path != "reorganization_r1g" and not path.startswith("reorganization_r1g/"):
            raise AssertionError(f"out-of-scope worktree path: {line}")

    links = validate_links(repo)
    frontier = rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(targets) != 101 or not all((repo / target).exists() for target in targets):
        raise AssertionError("frontier verification failed")

    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1] for line in str(git(repo, "ls-files", "-s")).splitlines()}
    manifests = []
    for package, digest in PACKAGES.items():
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != digest:
            raise AssertionError(f"manifest drift: {package}")
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        package_base = sorted(path for path in base_paths if path.startswith(package + "/"))
        package_current = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not package_base or package_current != package_base:
            raise AssertionError(f"package path drift: {package}")
        for path in package_base:
            if index_oids[path] != str(git(repo, "rev-parse", f"{BASE}:{path}")).strip():
                raise AssertionError(f"package byte drift: {path}")
        manifests.append({
            "package": package,
            "manifest_sha256": digest,
            "tracked_paths_byte_identical_to_base": len(package_base),
            "sha256sum_check_lines": len(replay.stdout.splitlines()),
            "result": "PASS",
        })

    recorded = {row["path"]: row for row in rows(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    dirty = dirty_metadata(args.dirty_checkout.resolve())
    if len(recorded) != len(dirty) or len(dirty) != 54 or set(recorded) != set(dirty):
        raise AssertionError("dirty checkout path metadata drift")
    for path, value in dirty.items():
        row = recorded[path]
        if (row["status"], int(row["size_bytes_lstat"]), row["object_type"], row["content_sha256"]) != (*value, "NOT_READ"):
            raise AssertionError(f"dirty checkout metadata drift: {path}")

    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if not test.get("baseline_match") or (test["passed"], test["failed"], test["xfailed"]) != (69, 1, 1):
        raise AssertionError("test baseline drift")

    result = {
        "result": "PASS",
        "mode": "R1G_INDEPENDENT_FAIL_CLOSED_PROVENANCE_VERIFY",
        "base": BASE,
        "preregistration_commit": PREREG,
        "readout_correction_preregistration_commit": str(git(repo, "rev-parse", CORRECTION_PREREG)).strip(),
        "native_field_equation_boundary": BOUNDARY,
        "boundary_parent": BOUNDARY_PARENT,
        "r1c_prefix_bug_reproduced": True,
        "all_cascade_prefix_rows": len(all_cascade),
        "affected_cascade_rows": len(affected_table),
        "affected_introduction_dates": dict(intro_dates),
        "affected_family_rows": len(summary),
        "affected_operator_provenance": dict(affected_provenance),
        "b02_b03_rows": len(candidate_table),
        "batch_counts": dict(Counter(row["batch_id"] for row in candidate_table)),
        "batch_introduction_ranges": {"B02": [min(b02_dates), max(b02_dates)], "B03": [min(b03_dates), max(b03_dates)]},
        "candidate_operator_provenance": dict(candidate_provenance),
        "candidate_reference_only_readout_rows": sum(row["role"] == "REFERENCE_ONLY" for row in candidate_table),
        "candidate_imported_action_or_coupling_rows": sum(row["imported_action_or_coupling"] != "NONE" for row in candidate_table),
        "candidate_lifecycle": dict(Counter(row["scientific_lifecycle"] for row in candidate_table)),
        "affected_reference_only_readout_rows": sum(row["role"] == "REFERENCE_ONLY" for row in affected_table),
        "affected_imported_action_or_coupling_rows": sum(row["imported_action_or_coupling"] != "NONE" for row in affected_table),
        "readout_correction_audit_rows": len(readout_audit),
        "corrected_pre_2026_07_01_destinations": sum(row["corrected_destination_proposal"].startswith("archive/pre_2026-07-01/") for row in candidate_table),
        "catchproof": catchproof,
        "markdown_links_verified": links,
        "frontier_rows": len(frontier),
        "frontier_unique_targets": len(targets),
        "frozen_manifest_replays": manifests,
        "test_baseline": test,
        "dirty_workstation_rows_metadata_only": len(dirty),
        "dirty_content_policy": "NOT_READ",
        "artifact_moves_or_edits": 0,
        "current_registry_edits": 0,
        "b02_b03_authorized": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
