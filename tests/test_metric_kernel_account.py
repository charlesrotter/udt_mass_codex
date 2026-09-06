import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import update_metric_kernel_account as account
from update_metric_kernel_account import BODY_ANCHORS, anchor_for, descendants, stale_after_source_changes


def fixture_rows():
    return [
        {"premise_id": "A", "upstream_ids": "", "source_sha256": "a0", "claim_polarity": "POSITIVE_OR_CONDITIONAL"},
        {"premise_id": "B", "upstream_ids": "A", "source_sha256": "b0", "claim_polarity": "POSITIVE_OR_CONDITIONAL"},
        {"premise_id": "C", "upstream_ids": "A", "source_sha256": "c0", "claim_polarity": "NEGATIVE_OR_LIMIT"},
        {"premise_id": "D", "upstream_ids": "", "source_sha256": "d0", "claim_polarity": "POSITIVE_OR_CONDITIONAL"},
    ]


def test_changed_source_flags_positive_and_negative_descendants_only():
    rows = fixture_rows()
    assert descendants(rows, {"A"}) == {"A", "B", "C"}
    stale = stale_after_source_changes(rows, {"A": "a1"})
    assert stale == {"A", "B", "C"}
    assert "D" not in stale


def test_unchanged_sources_remain_current_and_stale_cannot_be_labeled_current():
    rows = fixture_rows()
    assert stale_after_source_changes(rows, {}) == set()
    stale = stale_after_source_changes(rows, {"A": "changed"})
    status = {row["premise_id"]: ("STALE_REVIEW_REQUIRED" if row["premise_id"] in stale else "CURRENT") for row in rows}
    assert status["B"] == "STALE_REVIEW_REQUIRED"
    assert status["C"] == "STALE_REVIEW_REQUIRED"
    assert status["D"] == "CURRENT"


def test_body_anchors_are_curated_and_unsynthesized_rows_fall_back_to_appendix():
    assert BODY_ANCHORS["G315"] == "Section 5.6"
    assert BODY_ANCHORS["G324"] == "Section 5.8"
    assert BODY_ANCHORS["G337"] == "Section 5.10"
    assert anchor_for("G236") == "Section 8.5"
    assert anchor_for("G303") == "Appendix A"
    assert anchor_for("G304") == "Appendix A"
    assert anchor_for("G308") == "Appendix A"
    assert anchor_for("G309") == "Appendix A"
    assert anchor_for("G240") == "Appendix A"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _isolated_account_copy(tmp_path: Path) -> Path:
    isolated = tmp_path / "account"
    isolated.mkdir()
    for relative in (
        "update_metric_kernel_account.py",
        "verify_metric_kernel_account.py",
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "UDT_METRIC_KERNEL_COVERAGE.tsv",
        "UDT_METRIC_KERNEL_DEVELOPMENT.md",
    ):
        source = account.ROOT / relative
        destination = isolated / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    with account.SIDECAR.open(encoding="utf-8", newline="") as handle:
        sources = {row["controlling_source"] for row in csv.DictReader(handle, delimiter="\t")}
    for relative in sources:
        source = account.ROOT / relative
        destination = isolated / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return isolated


def _coverage_rows(isolated: Path) -> list[dict[str, str]]:
    with (isolated / "UDT_METRIC_KERNEL_COVERAGE.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_ordinary_updater_cannot_restore_review_after_source_change(tmp_path):
    isolated = _isolated_account_copy(tmp_path)
    before = _coverage_rows(isolated)
    changed_path = next(
        row["controlling_source"] for row in before if row["premise_id"] == "G249"
    )
    source = isolated / changed_path
    source.write_text(source.read_text(encoding="utf-8") + "\n<!-- test mutation -->\n", encoding="utf-8")

    subprocess.run(
        [sys.executable, "update_metric_kernel_account.py", "--write"],
        cwd=isolated,
        check=True,
        capture_output=True,
        text=True,
    )
    invalidated = _coverage_rows(isolated)
    changed_ids = {
        row["premise_id"] for row in invalidated if row["controlling_source"] == changed_path
    }
    affected = descendants(invalidated, changed_ids)
    by_id = {row["premise_id"]: row for row in invalidated}
    assert affected
    assert {by_id[premise_id]["claim_polarity"] for premise_id in affected} >= {
        "NEGATIVE_OR_LIMIT",
        "POSITIVE_OR_CONDITIONAL",
    }
    assert all(by_id[premise_id]["documentation_status"] != "FIDELITY_REVIEWED" for premise_id in affected)
    assert all(
        by_id[premise_id]["source_sha256"] != by_id[premise_id]["reviewed_source_sha256"]
        for premise_id in changed_ids
    )

    # An ordinary second run must accept the invalidated sidecar as current, not re-bless it.
    subprocess.run(
        [sys.executable, "update_metric_kernel_account.py"],
        cwd=isolated,
        check=True,
        capture_output=True,
        text=True,
    )
    assert _coverage_rows(isolated) == invalidated
    subprocess.run(
        [sys.executable, "verify_metric_kernel_account.py"],
        cwd=isolated,
        check=True,
        capture_output=True,
        text=True,
    )

    review_record = {
        "schema": "udt-metric-kernel-source-review-1.0",
        "review_id": "TEST_REVIEW_FOR_MUTATED_SOURCE",
        "scientific_snapshot": account.SCIENTIFIC_SNAPSHOT,
        "manuscript_sha256": _sha256(isolated / "UDT_METRIC_KERNEL_DEVELOPMENT.md"),
        "sources": {changed_path: _sha256(source)},
        "covered_premise_ids": sorted(affected),
    }
    review_path = isolated / "review_record.json"
    review_path.write_text(json.dumps(review_record), encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            "update_metric_kernel_account.py",
            "--record-review",
            str(review_path),
        ],
        cwd=isolated,
        check=True,
        capture_output=True,
        text=True,
    )
    restored = {row["premise_id"]: row for row in _coverage_rows(isolated)}
    assert all(restored[premise_id]["documentation_status"] == "FIDELITY_REVIEWED" for premise_id in affected if restored[premise_id]["manuscript_anchor"] != "Appendix A")
    assert all(restored[premise_id]["source_review_id"] == review_record["review_id"] for premise_id in affected)
