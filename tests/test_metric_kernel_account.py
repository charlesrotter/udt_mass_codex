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
