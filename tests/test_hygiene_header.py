"""Structure hygiene — require HYGIENE HEADER on covered results docs.

Physics-blind: only checks that required section markers exist.
Does NOT judge correctness of tags or physics merit.

Coverage: paths matching HYGIENE_COVERED_GLOBS (macro/hyp trail + template).
Historical results outside the globs are not failed (gradual adoption). The exact hashed legacy
backlog is accepted but cannot grow or change silently.
Protocol: STRUCTURE_HYGIENE.md · template: HYGIENE_HEADER_TEMPLATE.md
"""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
BACKLOG = (
    REPO
    / "hygiene_baseline_correction_2026-07-23"
    / "HYGIENE_LEGACY_BACKLOG.tsv"
)
EXPECTED_BACKLOG_SHA256 = (
    "a93c4148808d78cfba3171ee1ad00ff440e0909cbdcca00c2c07e47b27776312"
)
EXPECTED_BACKLOG_ROWS = 37
EXPECTED_BACKLOG_OMISSIONS = 88

# Gradual adoption: enforce on this arc's results trail + any new simple_metric results.
HYGIENE_COVERED_GLOBS = [
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

REQUIREMENT_PATTERNS = {
    "HYGIENE_HEADER": r"##\s+HYGIENE HEADER",
    "BUILD_ON_GRADE_MARKER": r"Build-on grade",
    "PREMISE_LEDGER": r"Premise ledger",
    "OBSERVING_OR_TARGETING": r"Observing or targeting",
    "VERIFIER_STATUS": r"Verifier status",
    "NOT_CLAIMED": r"NOT claimed",
}
REQUIRED_MARKERS = list(REQUIREMENT_PATTERNS.values())

# At least one build-on grade token must appear (value filled)
GRADE_TOKEN = re.compile(
    r"Build-on grade[^\n]*\b(DEMO|LEAD|CONDITIONAL|BANKED-FOR-STRUCTURE)\b",
    re.IGNORECASE,
)


def _covered_files() -> list[Path]:
    found: set[Path] = set()
    for pattern in HYGIENE_COVERED_GLOBS:
        for p in REPO.glob(pattern):
            if p.is_file() and p.name != "HYGIENE_HEADER_TEMPLATE.md":
                found.add(p.resolve())
    return sorted(found)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _issues(text: str) -> list[str]:
    missing = [
        name
        for name, pattern in REQUIREMENT_PATTERNS.items()
        if not re.search(pattern, text, re.IGNORECASE)
    ]
    if not GRADE_TOKEN.search(text):
        missing.append("BUILD_ON_GRADE_ALLOWED_VALUE")
    return missing


def _registered_backlog() -> dict[str, dict[str, str]]:
    assert BACKLOG.is_file(), f"legacy backlog missing: {BACKLOG.relative_to(REPO)}"
    assert _sha256(BACKLOG) == EXPECTED_BACKLOG_SHA256, (
        "legacy backlog changed; preregister and independently review any correction"
    )
    with BACKLOG.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        expected_fields = [
            "path",
            "sha256",
            "missing_requirements",
            "introducing_commit",
            "introducing_commit_time",
            "fixed_snapshot_status",
        ]
        assert reader.fieldnames == expected_fields, "legacy backlog schema changed"
        rows = list(reader)
    paths = [row["path"] for row in rows]
    assert len(rows) == EXPECTED_BACKLOG_ROWS, "legacy backlog row count changed"
    assert len(paths) == len(set(paths)), "duplicate legacy backlog path"
    omissions = sum(
        len(row["missing_requirements"].split(";")) for row in rows
    )
    assert omissions == EXPECTED_BACKLOG_OMISSIONS, (
        "legacy backlog omission count changed"
    )
    return {row["path"]: row for row in rows}


def test_hygiene_template_exists_and_complete():
    tmpl = REPO / "HYGIENE_HEADER_TEMPLATE.md"
    assert tmpl.is_file(), "HYGIENE_HEADER_TEMPLATE.md missing"
    text = tmpl.read_text(encoding="utf-8", errors="replace")
    for pat in REQUIRED_MARKERS:
        assert re.search(pat, text, re.IGNORECASE), f"template missing marker: {pat}"
    assert (REPO / "STRUCTURE_HYGIENE.md").is_file(), "STRUCTURE_HYGIENE.md missing"


def test_covered_results_have_hygiene_header():
    files = _covered_files()
    assert files, "no covered results files found — check globs"
    covered = {path.relative_to(REPO).as_posix(): path for path in files}
    backlog = _registered_backlog()
    failures: list[str] = []
    for rel in sorted(set(backlog) - set(covered)):
        failures.append(f"{rel}: registered backlog path is not covered")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(REPO).as_posix()
        actual_issues = _issues(text)
        if rel not in backlog:
            for issue in actual_issues:
                failures.append(f"{rel}: unregistered missing requirement {issue}")
            continue
        row = backlog[rel]
        if _sha256(path) != row["sha256"]:
            failures.append(f"{rel}: registered bytes changed")
        expected_issues = row["missing_requirements"].split(";")
        if actual_issues != expected_issues:
            failures.append(
                f"{rel}: registered omissions changed "
                f"{expected_issues!r} -> {actual_issues!r}"
            )
    assert not failures, "Hygiene contract violations:\n  " + "\n  ".join(failures)


def test_hygiene_globs_documented():
    """Protocol must mention the test so drivers know the gate exists."""
    proto = (REPO / "STRUCTURE_HYGIENE.md").read_text(encoding="utf-8", errors="replace")
    assert "test_hygiene_header" in proto or "HYGIENE_HEADER" in proto
