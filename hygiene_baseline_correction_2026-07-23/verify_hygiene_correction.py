#!/usr/bin/env python3
"""Independent census and actual-pytest mutation checks for the hygiene correction."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BACKLOG = HERE / "HYGIENE_LEGACY_BACKLOG.tsv"
EXPECTED_BACKLOG_SHA256 = (
    "a93c4148808d78cfba3171ee1ad00ff440e0909cbdcca00c2c07e47b27776312"
)
GLOBS = [
    "simple_metric_*_results.md",
    "simple_metric_*_results_*.md",
    "lorentz_*_results.md",
    "simple_metric_session_self_audit_*.md",
    "simple_metric_legacy_*_excursion.md",
    "simple_metric_hyperbolic_refine_AGENDA.md",
    "simple_metric_Pell_mass_lock_derive.md",
    "simple_metric_distance_profile_dimensional_MAP.md",
    "simple_metric_DA_native_derive.md",
    "simple_metric_lowz_linear_native_derive.md",
    "simple_metric_cross_sector_root_check.md",
    "simple_metric_xmax_POSTULATE.md",
]
PATTERNS = [
    ("HYGIENE_HEADER", re.compile(r"##\s+HYGIENE HEADER", re.I)),
    ("BUILD_ON_GRADE_MARKER", re.compile(r"Build-on grade", re.I)),
    ("PREMISE_LEDGER", re.compile(r"Premise ledger", re.I)),
    ("OBSERVING_OR_TARGETING", re.compile(r"Observing or targeting", re.I)),
    ("VERIFIER_STATUS", re.compile(r"Verifier status", re.I)),
    ("NOT_CLAIMED", re.compile(r"NOT claimed", re.I)),
]
GRADE = re.compile(
    r"Build-on grade[^\n]*\b(DEMO|LEAD|CONDITIONAL|BANKED-FOR-STRUCTURE)\b",
    re.I,
)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def document_issues(text: str) -> list[str]:
    found = [name for name, pattern in PATTERNS if not pattern.search(text)]
    if not GRADE.search(text):
        found.append("BUILD_ON_GRADE_ALLOWED_VALUE")
    return found


def covered(root: Path) -> dict[str, Path]:
    paths: set[Path] = set()
    for pattern in GLOBS:
        paths.update(
            path.resolve()
            for path in root.glob(pattern)
            if path.is_file() and path.name != "HYGIENE_HEADER_TEMPLATE.md"
        )
    return {
        path.relative_to(root.resolve()).as_posix(): path for path in sorted(paths)
    }


def validate_independently() -> dict[str, object]:
    if digest(BACKLOG) != EXPECTED_BACKLOG_SHA256:
        raise AssertionError("backlog hash")
    with BACKLOG.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
    expected_fields = [
        "path",
        "sha256",
        "missing_requirements",
        "introducing_commit",
        "introducing_commit_time",
        "fixed_snapshot_status",
    ]
    if reader.fieldnames != expected_fields:
        raise AssertionError("backlog schema")
    names = [row["path"] for row in rows]
    if len(rows) != 37 or len(names) != len(set(names)):
        raise AssertionError("backlog identities")
    with (
        ROOT / "research" / "_registry" / "ROOT_OWNERSHIP.tsv"
    ).open(encoding="utf-8", newline="") as handle:
        ownership = {
            row["current_path"]: row
            for row in csv.DictReader(handle, delimiter="\t")
        }
    documents = covered(ROOT)
    if len(documents) != 70 or not set(names) <= set(documents):
        raise AssertionError("covered universe")
    omissions = 0
    compliant = 0
    for name, path in documents.items():
        observed = document_issues(
            path.read_text(encoding="utf-8", errors="replace")
        )
        if name not in names:
            if observed:
                raise AssertionError(f"unregistered omission: {name}")
            compliant += 1
            continue
        row = rows[names.index(name)]
        expected = row["missing_requirements"].split(";")
        if digest(path) != row["sha256"] or observed != expected:
            raise AssertionError(f"registered mismatch: {name}")
        if (
            name not in ownership
            or ownership[name]["frozen_manifest_status"]
            != row["fixed_snapshot_status"]
        ):
            raise AssertionError(f"fixed classification mismatch: {name}")
        introduction = subprocess.check_output(
            [
                "git",
                "log",
                "--follow",
                "--diff-filter=A",
                "--format=%H%x09%cI",
                "--",
                name,
            ],
            cwd=ROOT,
            text=True,
        ).strip().splitlines()[-1].split("\t")
        if introduction != [
            row["introducing_commit"],
            row["introducing_commit_time"],
        ]:
            raise AssertionError(f"introduction mismatch: {name}")
        if subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                "b5622bd847a3f37f134125a0bf734eeb57133159",
                row["introducing_commit"],
            ],
            cwd=ROOT,
            check=False,
        ).returncode:
            raise AssertionError(f"not post-test: {name}")
        omissions += len(observed)
    if compliant != 33 or omissions != 88:
        raise AssertionError(f"counts:{compliant}:{omissions}")
    return {
        "covered_documents": len(documents),
        "compliant_documents": compliant,
        "registered_backlog_documents": len(rows),
        "registered_omissions": omissions,
        "post_test_introductions": len(rows),
        "fixed_classifications_reproduced": len(rows),
        "backlog_sha256": digest(BACKLOG),
    }


def prepare_copy(destination: Path) -> None:
    sources = list(covered(ROOT).values()) + [
        ROOT / "tests" / "test_hygiene_header.py",
        ROOT / "STRUCTURE_HYGIENE.md",
        ROOT / "HYGIENE_HEADER_TEMPLATE.md",
        BACKLOG,
    ]
    for source in sources:
        relative = source.relative_to(ROOT)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def pytest_copy(mutator=None) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="udt_hygiene_catch_") as name:
        root = Path(name)
        prepare_copy(root)
        if mutator is not None:
            mutator(root)
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_hygiene_header.py",
                "-q",
            ],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=60,
            env={"PYTHONDONTWRITEBYTECODE": "1"},
        )


def mutate_unregistered(root: Path) -> None:
    (root / "simple_metric_new_regression_results.md").write_text(
        "# Deliberately incomplete\n", encoding="utf-8"
    )


def mutate_registered_bytes(root: Path) -> None:
    path = root / "simple_metric_EOS_power_window_dS_results.md"
    path.write_bytes(path.read_bytes() + b"\n")


def mutate_duplicate_row(root: Path) -> None:
    path = (
        root
        / "hygiene_baseline_correction_2026-07-23"
        / "HYGIENE_LEGACY_BACKLOG.tsv"
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(lines + [lines[1]]) + "\n", encoding="utf-8")


def mutate_enlarged_backlog(root: Path) -> None:
    document = root / "simple_metric_new_registered_gap_results.md"
    document.write_text(
        "## HYGIENE HEADER\nBuild-on grade: DEMO\nPremise ledger\n"
        "Observing or targeting: OBSERVE\nVerifier status: NONE\n",
        encoding="utf-8",
    )
    backlog = (
        root
        / "hygiene_baseline_correction_2026-07-23"
        / "HYGIENE_LEGACY_BACKLOG.tsv"
    )
    row = "\t".join(
        [
            document.name,
            digest(document),
            "NOT_CLAIMED",
            "MUTATION",
            "2026-07-23T00:00:00-04:00",
            "NOT_FROZEN_OR_MANIFEST",
        ]
    )
    backlog.write_text(
        backlog.read_text(encoding="utf-8") + row + "\n", encoding="utf-8"
    )


def main() -> None:
    census = validate_independently()
    baseline = pytest_copy()
    if baseline.returncode != 0 or "3 passed" not in baseline.stdout:
        raise AssertionError("isolated baseline did not pass")
    mutations = [
        ("UNREGISTERED_NONCOMPLIANT_DOCUMENT", mutate_unregistered),
        ("REGISTERED_DOCUMENT_BYTE_CHANGE", mutate_registered_bytes),
        ("DUPLICATE_BACKLOG_ROW", mutate_duplicate_row),
        ("SILENTLY_ENLARGED_BACKLOG", mutate_enlarged_backlog),
    ]
    catches = []
    for name, mutator in mutations:
        completed = pytest_copy(mutator)
        if completed.returncode == 0 or "1 failed" not in completed.stdout:
            raise AssertionError(f"mutation escaped: {name}")
        catches.append(
            {
                "catch_id": name,
                "pytest_exit_code": completed.returncode,
                "stdout_sha256": digest_bytes(completed.stdout.encode()),
                "stderr_sha256": digest_bytes(completed.stderr.encode()),
                "status": "PASS_REJECTED",
            }
        )
    with (HERE / "CATCH_PROOFS.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(catches[0]), delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "schema": "udt-hygiene-baseline-independent-verification-1.0",
        "result": "PASS",
        **census,
        "isolated_pytest": {
            "exit_code": baseline.returncode,
            "stdout_sha256": digest_bytes(baseline.stdout.encode()),
            "stderr_sha256": digest_bytes(baseline.stderr.encode()),
            "summary": "3 passed",
        },
        "mutation_catch_proofs": len(catches),
        "repository_files_modified_by_verifier": [
            "CATCH_PROOFS.tsv",
            "INDEPENDENT_VERIFICATION.json",
        ],
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
