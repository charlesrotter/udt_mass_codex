"""Structure hygiene — require HYGIENE HEADER on covered results docs.

Physics-blind: only checks that required section markers exist.
Does NOT judge correctness of tags or physics merit.

Coverage: paths matching HYGIENE_COVERED_GLOBS (macro/hyp trail + template).
Historical results outside the globs are not failed (gradual adoption).
Protocol: STRUCTURE_HYGIENE.md · template: HYGIENE_HEADER_TEMPLATE.md
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

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

REQUIRED_MARKERS = [
    r"##\s+HYGIENE HEADER",
    r"Build-on grade",
    r"Premise ledger",
    r"Observing or targeting",
    r"Verifier status",
    r"NOT claimed",
]

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
    missing: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(REPO)
        for pat in REQUIRED_MARKERS:
            if not re.search(pat, text, re.IGNORECASE):
                missing.append(f"{rel}: missing /{pat}/")
        if not GRADE_TOKEN.search(text):
            missing.append(f"{rel}: Build-on grade value not one of DEMO|LEAD|CONDITIONAL|BANKED-FOR-STRUCTURE")
    assert not missing, "Hygiene header gaps:\n  " + "\n  ".join(missing)


def test_hygiene_globs_documented():
    """Protocol must mention the test so drivers know the gate exists."""
    proto = (REPO / "STRUCTURE_HYGIENE.md").read_text(encoding="utf-8", errors="replace")
    assert "test_hygiene_header" in proto or "HYGIENE_HEADER" in proto
