#!/usr/bin/env python3
"""Independent fail-closed verifier for R1H effective classification and closure."""

from __future__ import annotations

import argparse
import ast
import copy
import csv
import hashlib
import io
import json
import re
import stat
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


BASE = "2058f69db3f5c3a4322c5a9404e7145a62eeef2d"
PREREG = "b7074062f0f8c196c9695e28add68950b3d9a996"
R1H_PRE_CORRECTION = "b050d2eec5050cdcacc0edada67a438656cf3307"
CORRECTION_PREREG = "cf0005afefb5684b6e38889c3f7fcdf4b9886700"
STALE_IDENTITY_SET_SHA256 = "78f9afef35b3d4b97f4fea5f1c30b0ab269f1d91becad75034f0aaff11334393"
ALLOWED_EXISTING = {
    "research/_registry/CURRENT_CLASSIFICATION.tsv",
    "research/_registry/README.md",
}
CORRECTION_ALLOWED = {
    "reorganization_r1h/R1H_POST_CORRECTION_MIGRATION_STATE_PREREGISTRATION.md",
    "reorganization_r1h/build_r1h_effective_registry.py",
    "reorganization_r1h/CURRENT_CLASSIFICATION_SCHEMA.json",
    "research/_registry/CURRENT_CLASSIFICATION.tsv",
    "reorganization_r1h/R1H_AUDIT_REPORT.md",
    "reorganization_r1h/verify_r1h_effective_registry.py",
    "reorganization_r1h/VERIFY_RESULT.json",
    "research/_registry/README.md",
}
CORRECTION_REQUIRED_BEFORE_VERIFY = CORRECTION_ALLOWED - {
    "reorganization_r1h/VERIFY_RESULT.json"
}
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
FROZEN_INPUT_HASHES = {
    "research/_registry/ROOT_OWNERSHIP.tsv": "4e8a4e82d4698f24dea7510932a919773267dfad3ad4033999e195044a056edc",
    "research/_registry/MIGRATION_READINESS.tsv": "4fbdb4e71aae4caf18df9142e7ab822bb5b348b3b364b72e97707679bd244062",
    "research/_registry/CURRENT_ARTIFACT_PATHS.tsv": "9c1f7c9a9f11dbf31706268d5dbd3c2ffd4247e3f981a603d86e2095925e729c",
    "research/_registry/CURRENT_FRONTIER_TARGETS.tsv": "5ad9408676d788063165d5b41d6e4002d81f157c2b2a22a5dd23714740d2ec61",
    "reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv": "d44c2b8b55c3e16350dec8ce55349426e57cce4d1035859e29898c9fa0736c9d",
    "reorganization_r1g/B02_B03_ADJUDICATION.tsv": "cbae13c1d79f3d16a2c6542dfe003559fd3abadffb1d56e8490fdecc3070de11",
    "reorganization_r1g/READOUT_PROVENANCE_CORRECTION_AUDIT.tsv": "16f2237db4a3188e9668fa3f57cac265e473f9bbaddabf9f767a4fef5281252c",
    "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv": "c9089c1885f2f618c12567885f1e3d416abeeaa026cd6c442cf7ae64ae70f82c",
}
REGISTRY_FIELDS = [
    "original_path", "current_path", "fixed_snapshot_owner", "fixed_snapshot_evidence",
    "effective_primary_owner", "operator_provenance", "imported_action_or_coupling",
    "comparison_readout", "role", "scientific_lifecycle", "path_migration_safety",
    "migration_review_status", "scientific_family", "adjudication_source", "review_status",
]
PRE_CORRECTION_REGISTRY_FIELDS = [
    field for field in REGISTRY_FIELDS if field != "migration_review_status"
]
CLOSURE_FIELDS = [
    "batch_id", "original_path", "current_path", "introducing_commit",
    "operator_provenance", "imported_action_or_coupling", "comparison_readout", "role",
    "scientific_lifecycle", "scientific_family", "runtime_import_modules",
    "runtime_local_imports", "runtime_file_io", "introducing_commit_family_paths",
    "result_evidence_companions", "conceptual_operator_companions",
    "frozen_or_manifest_bound_companions", "current_control_frontier_companions",
    "atomic_family_current_paths", "standalone_move_safe", "closure_ruling",
    "execution_batch_status", "adjudication_source", "review_status", "ruling_basis",
]
AXES = (
    "operator_provenance", "imported_action_or_coupling", "comparison_readout", "role",
    "scientific_lifecycle", "primary_owner",
)
R0_R1G_PREFIXES = tuple(f"reorganization_r1{suffix}/" for suffix in ("a", "b", "c", "d", "e", "f", "g")) + (
    "reorganization_r0/",
)


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(cwd: Path, command: list[str], *, binary: bool = False, check: bool = True):
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if check and completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed: {' '.join(command)}\n{error}")
    return completed


def git(repo: Path, *args: str, binary: bool = False, check: bool = True):
    result = run(repo, ["git", *args], binary=binary, check=check)
    return result.stdout if check else result


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        records = list(reader)
        return list(reader.fieldnames or []), records


def rows(path: Path) -> list[dict[str, str]]:
    return read_rows(path)[1]


def read_rows_text(payload: str) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(payload), delimiter="\t")
    return list(reader.fieldnames or []), list(reader)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def split_set(value: str) -> set[str]:
    return set() if value in {"", "NONE"} else set(value.split(";"))


def catch(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise AssertionError(f"expected {code}, got {exc.code}") from exc
    raise AssertionError(f"catch-proof accepted corruption: {code}")


def validate_prereg(repo: Path) -> None:
    parent = str(git(repo, "rev-parse", f"{PREREG}^")).strip()
    paths = str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG)).splitlines()
    if parent != BASE or paths != ["reorganization_r1h/R1H_PREREGISTRATION.md"]:
        raise GateError("PREREGISTRATION", f"{parent}:{paths}")
    correction = str(git(repo, "rev-parse", CORRECTION_PREREG)).strip()
    correction_parent = str(git(repo, "rev-parse", f"{correction}^")).strip()
    correction_paths = str(
        git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", correction)
    ).splitlines()
    if correction_parent != R1H_PRE_CORRECTION or correction_paths != [
        "reorganization_r1h/R1H_POST_CORRECTION_MIGRATION_STATE_PREREGISTRATION.md"
    ]:
        raise GateError("PREREGISTRATION", f"{correction_parent}:{correction_paths}")


def validate_scope(repo: Path, injected: str | None = None) -> list[str]:
    changed = set(str(git(repo, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(
        path for path in changed
        if path not in ALLOWED_EXISTING and not path.startswith("reorganization_r1h/")
    )
    if invalid:
        raise GateError("SCOPE", ",".join(invalid))
    required = ALLOWED_EXISTING | {
        "reorganization_r1h/B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv",
        "reorganization_r1h/CURRENT_CLASSIFICATION_SCHEMA.json",
        "reorganization_r1h/SCIENTIFIC_FAMILY_MIGRATION_RULE.md",
        "reorganization_r1h/SCIENTIFIC_FAMILY_DEFINITIONS.json",
        "reorganization_r1h/build_r1h_effective_registry.py",
        "reorganization_r1h/verify_r1h_effective_registry.py",
    }
    missing = required - changed
    if missing:
        raise GateError("SCOPE", "missing:" + ",".join(sorted(missing)))
    correction_changed = set(
        str(git(repo, "diff", "--name-only", R1H_PRE_CORRECTION)).splitlines()
    )
    correction_changed.update(
        str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines()
    )
    if injected:
        correction_changed.add(injected)
    correction_invalid = sorted(correction_changed - CORRECTION_ALLOWED)
    correction_missing = sorted(CORRECTION_REQUIRED_BEFORE_VERIFY - correction_changed)
    if correction_invalid or correction_missing:
        raise GateError(
            "SCOPE",
            f"correction_invalid={correction_invalid};correction_missing={correction_missing}",
        )
    return sorted(changed)


def validate_frozen_inputs(repo: Path, corrupt: bool = False) -> dict[str, str]:
    result = {}
    for number, (relative, expected) in enumerate(FROZEN_INPUT_HASHES.items()):
        observed = sha((repo / relative).read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if observed != expected:
            raise GateError("FROZEN_RECORD", relative)
        result[relative] = observed
    changed = str(git(repo, "diff", "--name-only", BASE, "--", *R0_R1G_PREFIXES)).strip()
    if changed:
        raise GateError("FROZEN_RECORD", changed)
    for relative in (
        "research/_registry/ROOT_OWNERSHIP.tsv",
        "research/_registry/MIGRATION_READINESS.tsv",
    ):
        if str(git(repo, "diff", "--name-only", BASE, "--", relative)).strip():
            raise GateError("FROZEN_RECORD", relative)
    return result


def source_sets(
    affected: list[dict[str, str]], candidates: list[dict[str, str]], corrupt: bool = False
) -> tuple[set[str], set[str], set[str], set[str]]:
    affected_paths = [row["current_path"] for row in affected]
    candidate_paths = [row["current_path"] for row in candidates]
    if corrupt:
        candidate_paths = candidate_paths[:-1]
    affected_set = set(affected_paths)
    candidate_set = set(candidate_paths)
    overlap = affected_set & candidate_set
    union = affected_set | candidate_set
    if (
        len(affected_paths) != 121 or len(affected_set) != 121
        or len(candidate_paths) != 32 or len(candidate_set) != 32
        or len(overlap) != 19 or len(union) != 134
    ):
        raise GateError(
            "R1G_SET_ARITHMETIC",
            f"affected={len(affected_paths)}/{len(affected_set)};"
            f"candidates={len(candidate_paths)}/{len(candidate_set)};"
            f"union={len(union)};overlap={len(overlap)}",
        )
    affected_by = {row["current_path"]: row for row in affected}
    candidate_by = {row["current_path"]: row for row in candidates}
    for path in overlap:
        if any(affected_by[path][field] != candidate_by[path][field] for field in AXES):
            raise GateError("R1G_SET_ARITHMETIC", f"overlap disagreement:{path}")
    return affected_set, candidate_set, overlap, union


def validate_override_coverage(registry: list[dict[str, str]], union: set[str]) -> None:
    overrides = [
        row["original_path"] for row in registry
        if row["review_status"] in {"R1G_ADJUDICATED", "R1H_SCIENTIFIC_FAMILY_REVIEWED"}
    ]
    if len(overrides) != 134 or len(set(overrides)) != 134 or set(overrides) != union:
        raise GateError("OVERRIDE_COVERAGE", f"{len(overrides)}/{len(set(overrides))}")


def validate_no_pre_native(registry: list[dict[str, str]], union: set[str]) -> None:
    bad = [
        row["original_path"] for row in registry
        if row["original_path"] in union and row["operator_provenance"] == "PRE_NATIVE"
    ]
    if bad:
        raise GateError("PRE_NATIVE_FALLBACK", bad[0])


def validate_readout_disclosures(registry: list[dict[str, str]], union: set[str]) -> int:
    readouts = []
    for row in registry:
        if row["original_path"] not in union:
            continue
        has_axis = row["comparison_readout"] != "NONE" or row["role"] == "REFERENCE_ONLY"
        if has_axis:
            if (
                row["operator_provenance"] != "NATIVE_2026-07-01"
                or row["imported_action_or_coupling"] != "NONE"
                or row["comparison_readout"] != "GR_EINSTEIN_TENSOR;MISNER_SHARP"
                or row["role"] != "REFERENCE_ONLY"
            ):
                raise GateError("READOUT_DISCLOSURE", row["original_path"])
            readouts.append(row["original_path"])
    if len(readouts) != 6:
        raise GateError("READOUT_DISCLOSURE", f"count={len(readouts)}")
    return len(readouts)


def validate_inherited(registry: list[dict[str, str]], union: set[str]) -> int:
    inherited = [row for row in registry if row["original_path"] not in union]
    if len(inherited) != 980:
        raise GateError("INHERITED_INFLATION", f"count={len(inherited)}")
    for row in inherited:
        if (
            row["review_status"] != "INHERITED_UNREVIEWED"
            or row["operator_provenance"] != "INHERITED_UNREVIEWED"
            or row["imported_action_or_coupling"] != "INHERITED_UNREVIEWED"
            or row["comparison_readout"] != "INHERITED_UNREVIEWED"
            or row["role"] != "INHERITED_UNREVIEWED"
            or row["scientific_lifecycle"] != "INHERITED_UNREVIEWED"
            or row["scientific_family"] != "INHERITED_UNREVIEWED"
            or row["adjudication_source"] != "R1C_FIXED_SNAPSHOT_INHERITANCE"
            or row["migration_review_status"] != "INHERITED_UNREVIEWED"
            or not row["path_migration_safety"].startswith("INHERITED_UNREVIEWED:")
        ):
            raise GateError("INHERITED_INFLATION", row["original_path"])
    return len(inherited)


def validate_migration_state_correction(
    registry: list[dict[str, str]],
    prior_registry: list[dict[str, str]],
) -> dict[str, object]:
    prior_by = {row["original_path"]: row for row in prior_registry}
    current_by = {row["original_path"]: row for row in registry}
    if len(prior_by) != 1114 or set(prior_by) != set(current_by):
        raise GateError("REPLACEMENT_SET", "pre/post identity mismatch")

    selected = [
        row["original_path"]
        for row in prior_registry
        if row["review_status"] == "R1G_ADJUDICATED"
        and row["path_migration_safety"] == "BLOCKED_PROVENANCE_CORRECTION_REQUIRED"
    ]
    selected_hash = sha("".join(f"{path}\n" for path in selected).encode("utf-8"))
    if len(selected) != 101 or selected_hash != STALE_IDENTITY_SET_SHA256:
        raise GateError("REPLACEMENT_SET", f"pre={len(selected)}:{selected_hash}")
    selected_set = set(selected)

    stale = [
        row["original_path"] for row in registry
        if row["path_migration_safety"] == "BLOCKED_PROVENANCE_CORRECTION_REQUIRED"
    ]
    if stale:
        raise GateError("STALE_PROVENANCE_BLOCK", stale[0])

    replacement_set = {
        row["original_path"] for row in registry
        if row["path_migration_safety"] == "BLOCKED_SCIENTIFIC_FAMILY_REVIEW_REQUIRED"
    }
    if replacement_set != selected_set:
        movable = [
            path for path in selected
            if current_by[path]["path_migration_safety"] in {
                "MOVE_READY", "SAFE_BYTE_IDENTICAL", "SAFE_WITH_PATH_POINTER_CHANGES"
            }
        ]
        if movable:
            raise GateError("FAMILY_REVIEW_PROMOTION", movable[0])
        raise GateError(
            "REPLACEMENT_SET",
            f"missing={sorted(selected_set - replacement_set)[:1]};"
            f"extra={sorted(replacement_set - selected_set)[:1]}",
        )

    protected_32 = 0
    immutable_1 = 0
    inherited_980 = 0
    for original, prior in prior_by.items():
        current = current_by[original]
        old_fields = PRE_CORRECTION_REGISTRY_FIELDS
        if original in selected_set:
            for field in old_fields:
                if field == "path_migration_safety":
                    continue
                if current[field] != prior[field]:
                    raise GateError("REPLACEMENT_SET", f"{original}:{field}")
            if current["migration_review_status"] != "FAMILY_REVIEW_REQUIRED":
                raise GateError("REPLACEMENT_SET", f"{original}:migration_review_status")
        elif (
            prior["review_status"] == "R1H_SCIENTIFIC_FAMILY_REVIEWED"
            and prior["path_migration_safety"] == "BLOCKED_IMMUTABLE_FAMILY_COMPANION"
        ):
            protected_32 += 1
            if any(current[field] != prior[field] for field in old_fields):
                raise GateError("PROTECTED_REVIEWED_STATE", original)
            if current["migration_review_status"] != "FAMILY_REVIEWED_BLOCKED":
                raise GateError("PROTECTED_REVIEWED_STATE", original)
        elif (
            prior["review_status"] == "R1G_ADJUDICATED"
            and prior["path_migration_safety"] == "IMMUTABLE_PATH_RETAIN"
        ):
            immutable_1 += 1
            if any(current[field] != prior[field] for field in old_fields):
                raise GateError("PROTECTED_REVIEWED_STATE", original)
            if current["migration_review_status"] != "IMMUTABLE_PATH":
                raise GateError("PROTECTED_REVIEWED_STATE", original)
        elif prior["review_status"] == "INHERITED_UNREVIEWED":
            inherited_980 += 1
            if any(current[field] != prior[field] for field in old_fields):
                raise GateError("INHERITED_BASELINE_DRIFT", original)
            if current["migration_review_status"] != "INHERITED_UNREVIEWED":
                raise GateError("INHERITED_BASELINE_DRIFT", original)
        else:
            raise GateError("REPLACEMENT_SET", f"unclassified prior row:{original}")

    if (protected_32, immutable_1, inherited_980) != (32, 1, 980):
        raise GateError(
            "PROTECTED_REVIEWED_STATE",
            f"{protected_32}/{immutable_1}/{inherited_980}",
        )
    migration_reviews = Counter(row["migration_review_status"] for row in registry)
    expected = Counter({
        "FAMILY_REVIEW_REQUIRED": 101,
        "FAMILY_REVIEWED_BLOCKED": 32,
        "IMMUTABLE_PATH": 1,
        "INHERITED_UNREVIEWED": 980,
    })
    if migration_reviews != expected:
        raise GateError("MIGRATION_REVIEW_STATUS", str(migration_reviews))
    return {
        "replacement_rows": len(selected),
        "replacement_identity_set_sha256": selected_hash,
        "protected_family_reviewed_blocked_rows": protected_32,
        "protected_immutable_rows": immutable_1,
        "inherited_old_fields_identical_rows": inherited_980,
        "stale_provenance_correction_rows": 0,
        "migration_review_status_counts": dict(sorted(migration_reviews.items())),
    }


def immutable_current_path(
    current_path: str,
    ownership: dict[str, dict[str, str]],
    readiness: dict[str, dict[str, str]],
    original_by_current: dict[str, str],
) -> bool:
    original = original_by_current.get(current_path)
    if original is None:
        return False
    frozen = ownership[original]["frozen_manifest_status"]
    frozen_bound = frozen != "NOT_FROZEN_OR_MANIFEST" and (
        "R0_FROZEN_EVIDENCE" in frozen
        or "REFERENCED_BY_SIX_FROZEN_PACKAGES" in frozen
        or "MANIFEST_EDGE_TARGET" in frozen
    )
    return readiness[original]["migration_readiness"] == "IMMUTABLE_PATH" or frozen_bound


def runtime_audit(repo: Path, path: str) -> tuple[set[str], set[str], set[str]]:
    tree = ast.parse((repo / path).read_text(encoding="utf-8"), filename=path)
    modules: set[str] = set()
    local: set[str] = set()
    file_io: set[str] = set()
    io_attributes = {
        "load", "save", "loadtxt", "savetxt", "fromfile", "tofile",
        "read_text", "write_text", "read_bytes", "write_bytes", "open",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "open":
                file_io.add("open")
            elif isinstance(node.func, ast.Attribute) and node.func.attr in io_attributes:
                file_io.add(node.func.attr)
    for module in modules:
        if (repo / f"{module}.py").exists() or (repo / module).is_dir():
            local.add(module)
    return modules, local, file_io


def validate_closure(
    repo: Path,
    closure: list[dict[str, str]],
    candidates: list[dict[str, str]],
    ownership: dict[str, dict[str, str]],
    readiness: dict[str, dict[str, str]],
    original_by_current: dict[str, str],
) -> dict[str, object]:
    candidate_by = {row["current_path"]: row for row in candidates}
    paths = [row["original_path"] for row in closure]
    if len(closure) != 32 or len(set(paths)) != 32 or set(paths) != set(candidate_by):
        raise GateError("CLOSURE_COVERAGE", f"{len(paths)}/{len(set(paths))}")
    family_commits: dict[str, set[str]] = {}
    for row in closure:
        path = row["original_path"]
        source = candidate_by[path]
        for field in (
            "operator_provenance", "imported_action_or_coupling", "comparison_readout", "role",
            "scientific_lifecycle", "introducing_commit",
        ):
            if row[field] != source[field]:
                raise GateError("CLOSURE_SOURCE", f"{path}:{field}")
        actual_commit_paths = set(
            line for line in str(git(repo, "show", "--format=", "--name-only", row["introducing_commit"])).splitlines()
            if line
        )
        recorded_commit_paths = split_set(row["introducing_commit_family_paths"])
        recorded_basenames = {Path(item).name for item in recorded_commit_paths}
        if {Path(item).name for item in actual_commit_paths} != recorded_basenames or Path(path).name not in recorded_basenames:
            raise GateError("CLOSURE_SOURCE", f"{path}:introducing commit family")
        family_commits.setdefault(row["scientific_family"], set()).add(row["introducing_commit"])

        modules, local, file_io = runtime_audit(repo, row["current_path"])
        if split_set(row["runtime_import_modules"]) != modules:
            raise GateError("CLOSURE_SOURCE", f"{path}:imports")
        if split_set(row["runtime_local_imports"]) != local or split_set(row["runtime_file_io"]) != file_io:
            raise GateError("CLOSURE_SOURCE", f"{path}:runtime closure")

        atomic = split_set(row["atomic_family_current_paths"])
        results = split_set(row["result_evidence_companions"])
        conceptual = split_set(row["conceptual_operator_companions"])
        immutable = split_set(row["frozen_or_manifest_bound_companions"])
        if row["current_path"] not in atomic or not results or not conceptual or not immutable:
            raise GateError("CLOSURE_SOURCE", f"{path}:incomplete family")
        if not results <= atomic or not conceptual <= atomic or not immutable <= atomic:
            raise GateError("CLOSURE_SOURCE", f"{path}:family subset")
        missing = [companion for companion in atomic if not (repo / companion).exists()]
        if missing:
            raise GateError("CLOSURE_SOURCE", f"{path}:missing:{missing[0]}")
        if not all(immutable_current_path(item, ownership, readiness, original_by_current) for item in immutable):
            raise GateError("CLOSURE_SOURCE", f"{path}:false immutable companion")
        if not (results & immutable):
            raise GateError("CLOSURE_SOURCE", f"{path}:no immutable result evidence")
        if (
            row["standalone_move_safe"] != "NO"
            or row["closure_ruling"] != "BLOCKED_IMMUTABLE_FAMILY_COMPANION"
            or row["execution_batch_status"] != "WITHDRAWN_NO_EXECUTION_AUTHORITY"
            or row["review_status"] != "R1H_SCIENTIFIC_FAMILY_REVIEWED"
        ):
            if immutable and row["standalone_move_safe"] != "NO":
                raise GateError("STRANDED_IMMUTABLE_COMPANION", path)
            raise GateError("CLOSURE_RULING", path)
    if len(family_commits) != 10 or any(len(commits) != 1 for commits in family_commits.values()):
        raise GateError("CLOSURE_SOURCE", f"families={family_commits}")
    return {
        "rows": len(closure),
        "batch_counts": dict(Counter(row["batch_id"] for row in closure)),
        "family_counts": dict(sorted(Counter(row["scientific_family"] for row in closure).items())),
        "closure_ruling_counts": dict(Counter(row["closure_ruling"] for row in closure)),
        "runtime_local_import_rows": sum(row["runtime_local_imports"] != "NONE" for row in closure),
        "runtime_file_io_rows": sum(row["runtime_file_io"] != "NONE" for row in closure),
    }


def validate_registry(
    registry: list[dict[str, str]],
    current: list[dict[str, str]],
    ownership: dict[str, dict[str, str]],
    readiness: dict[str, dict[str, str]],
    affected: list[dict[str, str]],
    candidates: list[dict[str, str]],
    closure: list[dict[str, str]],
) -> dict[str, object]:
    affected_set, candidate_set, overlap, union = source_sets(affected, candidates)
    originals = [row["original_path"] for row in registry]
    current_paths = [row["current_path"] for row in registry]
    expected_current = {row["original_path"]: row["current_path"] for row in current}
    if len(registry) != 1114 or len(set(originals)) != 1114 or len(set(current_paths)) != 1114:
        raise GateError("REGISTRY_IDENTITY", f"{len(registry)}/{len(set(originals))}/{len(set(current_paths))}")
    if {row["original_path"]: row["current_path"] for row in registry} != expected_current:
        raise GateError("REGISTRY_IDENTITY", "current map mismatch")
    validate_override_coverage(registry, union)
    validate_no_pre_native(registry, union)
    readout_count = validate_readout_disclosures(registry, union)
    inherited_count = validate_inherited(registry, union)

    affected_by = {row["current_path"]: row for row in affected}
    candidate_by = {row["current_path"]: row for row in candidates}
    closure_by = {row["original_path"]: row for row in closure}
    for row in registry:
        original = row["original_path"]
        if row["fixed_snapshot_owner"] != ownership[original]["primary_owner"]:
            raise GateError("REGISTRY_SOURCE", f"{original}:fixed owner")
        if row["fixed_snapshot_evidence"] != ownership[original]["ownership_evidence"]:
            raise GateError("REGISTRY_SOURCE", f"{original}:fixed evidence")
        if original not in union:
            if row["effective_primary_owner"] != ownership[original]["primary_owner"]:
                raise GateError("REGISTRY_SOURCE", f"{original}:inherited owner")
            suffix = row["path_migration_safety"].split(":", 1)[-1]
            if suffix != readiness[original]["migration_readiness"]:
                raise GateError("REGISTRY_SOURCE", f"{original}:inherited readiness")
            continue
        source = candidate_by.get(original, affected_by.get(original))
        assert source is not None
        for field in AXES:
            target = "effective_primary_owner" if field == "primary_owner" else field
            if row[target] != source[field]:
                raise GateError("REGISTRY_SOURCE", f"{original}:{target}")
        if original in candidate_set:
            close = closure_by[original]
            if (
                row["path_migration_safety"] != close["closure_ruling"]
                or row["migration_review_status"] != "FAMILY_REVIEWED_BLOCKED"
                or row["scientific_family"] != close["scientific_family"]
                or row["review_status"] != "R1H_SCIENTIFIC_FAMILY_REVIEWED"
            ):
                raise GateError("REGISTRY_SOURCE", f"{original}:R1H closure")
        else:
            expected_migration = source["migration_safety"]
            expected_migration_review = "IMMUTABLE_PATH"
            if expected_migration == "BLOCKED_PROVENANCE_CORRECTION_REQUIRED":
                expected_migration = "BLOCKED_SCIENTIFIC_FAMILY_REVIEW_REQUIRED"
                expected_migration_review = "FAMILY_REVIEW_REQUIRED"
            elif expected_migration != "IMMUTABLE_PATH_RETAIN":
                raise GateError("REGISTRY_SOURCE", f"{original}:unexpected source migration")
            if (
                row["path_migration_safety"] != expected_migration
                or row["migration_review_status"] != expected_migration_review
                or row["scientific_family"] != source["family_id"]
                or row["review_status"] != "R1G_ADJUDICATED"
            ):
                raise GateError("REGISTRY_SOURCE", f"{original}:R1G overlay")

    reviews = Counter(row["review_status"] for row in registry)
    provenance = Counter(row["operator_provenance"] for row in registry)
    migration_reviews = Counter(row["migration_review_status"] for row in registry)
    expected_reviews = Counter({
        "INHERITED_UNREVIEWED": 980,
        "R1G_ADJUDICATED": 102,
        "R1H_SCIENTIFIC_FAMILY_REVIEWED": 32,
    })
    expected_provenance = Counter({
        "INHERITED_UNREVIEWED": 980,
        "NATIVE_2026-07-01": 131,
        "MIXED": 2,
        "OPEN": 1,
    })
    expected_migration_reviews = Counter({
        "FAMILY_REVIEW_REQUIRED": 101,
        "FAMILY_REVIEWED_BLOCKED": 32,
        "IMMUTABLE_PATH": 1,
        "INHERITED_UNREVIEWED": 980,
    })
    if (
        reviews != expected_reviews
        or provenance != expected_provenance
        or migration_reviews != expected_migration_reviews
    ):
        raise GateError("REGISTRY_SOURCE", f"{reviews}:{provenance}:{migration_reviews}")
    return {
        "rows": len(registry),
        "unique_original_paths": len(set(originals)),
        "unique_current_paths": len(set(current_paths)),
        "r1g_affected_rows": len(affected_set),
        "r1g_b02_b03_rows": len(candidate_set),
        "r1g_overlap_rows": len(overlap),
        "r1g_union_rows": len(union),
        "inherited_rows": inherited_count,
        "reference_only_readout_rows": readout_count,
        "review_status_counts": dict(sorted(reviews.items())),
        "operator_provenance_counts": dict(sorted(provenance.items())),
        "migration_review_status_counts": dict(sorted(migration_reviews.items())),
        "effective_primary_owner_counts": dict(sorted(Counter(row["effective_primary_owner"] for row in registry).items())),
        "scientific_lifecycle_counts": dict(sorted(Counter(row["scientific_lifecycle"] for row in registry).items())),
    }


def validate_current_paths(repo: Path, current: list[dict[str, str]], corrupt: bool = False) -> dict[str, object]:
    working = copy.deepcopy(current)
    if corrupt:
        working[-1]["current_path"] = working[0]["current_path"]
    originals = [row["original_path"] for row in working]
    paths = [row["current_path"] for row in working]
    missing = [path for path in paths if not (repo / path).exists()]
    if len(working) != 1114 or len(set(originals)) != 1114 or len(set(paths)) != 1114 or missing:
        raise GateError("CURRENT_PATH", f"{len(working)}/{len(set(originals))}/{len(set(paths))}/{missing[:1]}")
    return {
        "rows": len(working),
        "unique_original_paths": len(set(originals)),
        "unique_current_paths": len(set(paths)),
        "status_counts": dict(Counter(row["path_status"] for row in working)),
    }


def validate_links(repo: Path, injected_missing: bool = False) -> int:
    sources = [repo / "research/_registry/README.md"]
    sources += sorted((repo / "reorganization_r1h").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    targets: list[Path] = []
    for source in sources:
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            targets.append(source.parent.joinpath(target).resolve())
    if injected_missing:
        targets.append(repo / "missing-r1h-catchproof-target")
    missing = [target for target in targets if not target.exists()]
    if missing:
        raise GateError("BROKEN_LINK", str(missing[0]))
    return len(targets)


def validate_manifests(repo: Path, corrupt: bool = False) -> list[dict[str, object]]:
    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {
        line.split(None, 3)[3]: line.split()[1]
        for line in str(git(repo, "ls-files", "-s")).splitlines()
    }
    result = []
    for number, (package, digest) in enumerate(PACKAGES.items()):
        expected = "0" * 64 if corrupt and number == 0 else digest
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != expected:
            raise GateError("MANIFEST", package)
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        before = sorted(path for path in base_paths if path.startswith(package + "/"))
        after = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not before or before != after:
            raise GateError("MANIFEST", f"{package}:path state")
        for path in before:
            if index_oids[path] != str(git(repo, "rev-parse", f"{BASE}:{path}")).strip():
                raise GateError("MANIFEST", path)
        result.append({
            "package": package,
            "manifest_sha256": digest,
            "manifest_entries_passed": len(replay.stdout.splitlines()),
            "tracked_paths_byte_identical_to_base": len(before),
            "result": "PASS",
        })
    return result


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
        kind = (
            "regular_file" if stat.S_ISREG(info.st_mode)
            else "directory" if stat.S_ISDIR(info.st_mode)
            else "symlink" if stat.S_ISLNK(info.st_mode)
            else "other"
        )
        result[path] = (code, info.st_size, kind)
    return result


def validate_dirty(repo: Path, dirty_checkout: Path, corrupt: bool = False) -> int:
    inventory = repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv"
    recorded = {row["path"]: row for row in rows(inventory)}
    observed = dirty_metadata(dirty_checkout)
    if corrupt:
        observed = dict(observed); observed.pop(next(iter(observed)))
    if len(recorded) != 54 or len(observed) != 54 or set(recorded) != set(observed):
        raise GateError("DIRTY_METADATA", f"{len(recorded)}/{len(observed)}")
    for path, value in observed.items():
        row = recorded[path]
        expected = (row["status"], int(row["size_bytes_lstat"]), row["object_type"])
        if value != expected or row["content_sha256"] != "NOT_READ":
            raise GateError("DIRTY_METADATA", path)
    return len(observed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    validate_prereg(repo)
    changed = validate_scope(repo)
    frozen_hashes = validate_frozen_inputs(repo)
    schema = json.loads((repo / "reorganization_r1h/CURRENT_CLASSIFICATION_SCHEMA.json").read_text(encoding="utf-8"))
    registry_fields, registry = read_rows(repo / "research/_registry/CURRENT_CLASSIFICATION.tsv")
    prior_fields, prior_registry = read_rows_text(
        str(git(repo, "show", f"{R1H_PRE_CORRECTION}:research/_registry/CURRENT_CLASSIFICATION.tsv"))
    )
    closure_fields, closure = read_rows(repo / "reorganization_r1h/B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv")
    if registry_fields != REGISTRY_FIELDS or schema["columns"] != REGISTRY_FIELDS:
        raise GateError("SCHEMA", str(registry_fields))
    if (
        schema.get("schema_version") != "R1H_CURRENT_CLASSIFICATION_V2_MIGRATION_REVIEW_AXIS"
        or schema.get("migration_review_status_counts") != {
            "FAMILY_REVIEW_REQUIRED": 101,
            "FAMILY_REVIEWED_BLOCKED": 32,
            "IMMUTABLE_PATH": 1,
            "INHERITED_UNREVIEWED": 980,
        }
    ):
        raise GateError("SCHEMA", "migration-review contract")
    if prior_fields != PRE_CORRECTION_REGISTRY_FIELDS:
        raise GateError("SCHEMA", f"pre-correction:{prior_fields}")
    if closure_fields != CLOSURE_FIELDS:
        raise GateError("SCHEMA", str(closure_fields))

    current = rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    ownership = {row["current_path"]: row for row in rows(repo / "research/_registry/ROOT_OWNERSHIP.tsv")}
    readiness = {row["current_path"]: row for row in rows(repo / "research/_registry/MIGRATION_READINESS.tsv")}
    original_by_current = {row["current_path"]: row["original_path"] for row in current}
    affected = rows(repo / "reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv")
    candidates = rows(repo / "reorganization_r1g/B02_B03_ADJUDICATION.tsv")
    current_result = validate_current_paths(repo, current)
    closure_result = validate_closure(repo, closure, candidates, ownership, readiness, original_by_current)
    registry_result = validate_registry(registry, current, ownership, readiness, affected, candidates, closure)
    correction_result = validate_migration_state_correction(registry, prior_registry)

    generator = run(repo, ["python3", "-B", "reorganization_r1h/build_r1h_effective_registry.py", "--repo", ".", "--check"])
    generator_result = json.loads(generator.stdout)
    if generator_result["registry_sha256"] != sha((repo / "research/_registry/CURRENT_CLASSIFICATION.tsv").read_bytes()):
        raise GateError("GENERATOR", "registry hash")
    if generator_result["closure_sha256"] != sha((repo / "reorganization_r1h/B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv").read_bytes()):
        raise GateError("GENERATOR", "closure hash")

    links = validate_links(repo)
    frontier = rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    frontier_targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(frontier_targets) != 101 or not all((repo / target).exists() for target in frontier_targets):
        raise GateError("FRONTIER", f"{len(frontier)}/{len(frontier_targets)}")
    manifests = validate_manifests(repo)
    dirty_count = validate_dirty(repo, args.dirty_checkout.resolve())
    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (test.get("passed"), test.get("failed"), test.get("xfailed"), test.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(test))

    _, _, _, union = source_sets(affected, candidates)
    native_row = next(row for row in registry if row["original_path"] in union and row["operator_provenance"] == "NATIVE_2026-07-01")
    pre_native = copy.deepcopy(registry)
    next(row for row in pre_native if row["original_path"] == native_row["original_path"])["operator_provenance"] = "PRE_NATIVE"
    missing_override = copy.deepcopy(registry)
    next(row for row in missing_override if row["review_status"] == "R1G_ADJUDICATED")["review_status"] = "INHERITED_UNREVIEWED"
    duplicate_override = copy.deepcopy(registry)
    duplicate_override.append(copy.deepcopy(next(row for row in registry if row["review_status"] == "R1G_ADJUDICATED")))
    readout_drift = copy.deepcopy(registry)
    next(row for row in readout_drift if row["role"] == "REFERENCE_ONLY")["comparison_readout"] = "NONE"
    inherited_inflation = copy.deepcopy(registry)
    next(row for row in inherited_inflation if row["review_status"] == "INHERITED_UNREVIEWED")["review_status"] = "R1G_ADJUDICATED"
    stranded = copy.deepcopy(closure)
    stranded[0]["standalone_move_safe"] = "YES"
    replacement_row = next(
        row for row in registry
        if row["migration_review_status"] == "FAMILY_REVIEW_REQUIRED"
    )
    stale_state = copy.deepcopy(registry)
    next(
        row for row in stale_state if row["original_path"] == replacement_row["original_path"]
    )["path_migration_safety"] = "BLOCKED_PROVENANCE_CORRECTION_REQUIRED"
    wrong_replacement = copy.deepcopy(registry)
    next(
        row for row in wrong_replacement if row["original_path"] == replacement_row["original_path"]
    )["path_migration_safety"] = "BLOCKED_UNREVIEWED"
    promoted = copy.deepcopy(registry)
    next(
        row for row in promoted if row["original_path"] == replacement_row["original_path"]
    )["path_migration_safety"] = "MOVE_READY"
    protected_family = copy.deepcopy(registry)
    next(
        row for row in protected_family
        if row["migration_review_status"] == "FAMILY_REVIEWED_BLOCKED"
    )["scientific_family"] = "CORRUPTED_FAMILY"
    protected_immutable = copy.deepcopy(registry)
    next(
        row for row in protected_immutable
        if row["migration_review_status"] == "IMMUTABLE_PATH"
    )["path_migration_safety"] = "MOVE_READY"
    inherited_drift = copy.deepcopy(registry)
    next(
        row for row in inherited_drift
        if row["migration_review_status"] == "INHERITED_UNREVIEWED"
    )["effective_primary_owner"] = "CORRUPTED_OWNER"

    catchproof = {
        "pre_native_fallback_rejected": catch("PRE_NATIVE_FALLBACK", lambda: validate_no_pre_native(pre_native, union)),
        "missing_override_rejected": catch("OVERRIDE_COVERAGE", lambda: validate_override_coverage(missing_override, union)),
        "duplicate_override_rejected": catch("OVERRIDE_COVERAGE", lambda: validate_override_coverage(duplicate_override, union)),
        "reference_only_readout_loss_rejected": catch("READOUT_DISCLOSURE", lambda: validate_readout_disclosures(readout_drift, union)),
        "standalone_move_stranding_immutable_companion_rejected": catch(
            "STRANDED_IMMUTABLE_COMPANION",
            lambda: validate_closure(repo, stranded, candidates, ownership, readiness, original_by_current),
        ),
        "inherited_unreviewed_inflation_rejected": catch("INHERITED_INFLATION", lambda: validate_inherited(inherited_inflation, union)),
        "incorrect_union_or_overlap_rejected": catch("R1G_SET_ARITHMETIC", lambda: source_sets(affected, candidates, True)),
        "unauthorized_edit_rejected": catch("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_record_mutation_rejected": catch("FROZEN_RECORD", lambda: validate_frozen_inputs(repo, True)),
        "duplicate_current_path_rejected": catch("CURRENT_PATH", lambda: validate_current_paths(repo, current, True)),
        "manifest_mutation_rejected": catch("MANIFEST", lambda: validate_manifests(repo, True)),
        "broken_link_rejected": catch("BROKEN_LINK", lambda: validate_links(repo, True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), True)),
        "stale_provenance_correction_state_rejected": catch(
            "STALE_PROVENANCE_BLOCK",
            lambda: validate_migration_state_correction(stale_state, prior_registry),
        ),
        "incorrect_101_identity_replacement_set_rejected": catch(
            "REPLACEMENT_SET",
            lambda: validate_migration_state_correction(wrong_replacement, prior_registry),
        ),
        "family_review_required_promotion_rejected": catch(
            "FAMILY_REVIEW_PROMOTION",
            lambda: validate_migration_state_correction(promoted, prior_registry),
        ),
        "family_reviewed_blocked_drift_rejected": catch(
            "PROTECTED_REVIEWED_STATE",
            lambda: validate_migration_state_correction(protected_family, prior_registry),
        ),
        "immutable_path_drift_rejected": catch(
            "PROTECTED_REVIEWED_STATE",
            lambda: validate_migration_state_correction(protected_immutable, prior_registry),
        ),
        "inherited_old_field_drift_rejected": catch(
            "INHERITED_BASELINE_DRIFT",
            lambda: validate_migration_state_correction(inherited_drift, prior_registry),
        ),
    }

    result = {
        "result": "PASS",
        "mode": "R1H_POST_CORRECTION_MIGRATION_STATE_FAIL_CLOSED_VERIFY",
        "base": BASE,
        "preregistration_commit": PREREG,
        "pre_correction_tip": R1H_PRE_CORRECTION,
        "correction_preregistration_commit": str(git(repo, "rev-parse", CORRECTION_PREREG)).strip(),
        "changed_paths": changed,
        "correction_changed_paths": sorted(
            str(git(repo, "diff", "--name-only", R1H_PRE_CORRECTION)).splitlines()
        ),
        "fixed_input_hashes": frozen_hashes,
        "current_paths": current_result,
        "effective_registry": registry_result,
        "migration_state_correction": correction_result,
        "pre_correction_registry_sha256": sha(
            str(git(repo, "show", f"{R1H_PRE_CORRECTION}:research/_registry/CURRENT_CLASSIFICATION.tsv")).encode("utf-8")
        ),
        "effective_registry_sha256": sha((repo / "research/_registry/CURRENT_CLASSIFICATION.tsv").read_bytes()),
        "closure": closure_result,
        "closure_sha256": sha((repo / "reorganization_r1h/B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv").read_bytes()),
        "schema_sha256": sha((repo / "reorganization_r1h/CURRENT_CLASSIFICATION_SCHEMA.json").read_bytes()),
        "generator_check": "PASS",
        "generator_summary": generator_result,
        "markdown_links_verified": links,
        "frontier_rows": len(frontier),
        "frontier_unique_targets": len(frontier_targets),
        "frozen_manifest_replays": manifests,
        "test_baseline": test,
        "dirty_checkout_metadata_rows": dirty_count,
        "dirty_content_policy": "NOT_READ",
        "catchproof": catchproof,
        "b02_b03_execution_batches_withdrawn": True,
        "artifact_moves_or_content_edits": 0,
        "integration_authorized": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
