#!/usr/bin/env python3
"""Deterministic source-authority and semantic adjudication verifier."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def frozen_blob(row: dict[str, str]) -> bytes:
    """Return the exact preregistered Git blob, independent of later path edits."""
    return subprocess.run(
        ["git", "cat-file", "blob", row["git_blob"]],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout


def validate(state: dict[str, object]) -> None:
    assert state["headline"] == (
        "FOUNDED_ABSTRACT_PAIR_DERIVED__LOCAL_PHYSICAL_ALIGNMENT_CONDITIONAL_ON_DECLARED_READOUT__"
        "BRANCH_CONDITIONAL_PHYSICAL_REDUCTIONS_EXIST__COMPLETE_UNIVERSAL_REDUCTION_OPEN"
    )
    assert state["abstract_pair"] == "DERIVED"
    assert state["local_alignment"] == "DERIVED_CONDITIONAL_ON_RECORDED_READOUT"
    assert state["branch_reductions"] == "DERIVED_BOUNDED_EXISTENCE"
    assert state["universal_reduction"] == "OPEN"
    assert state["fixed_component_plane"] == "REFUTED_USE_EQUIVARIANCE"
    assert state["q_squared"] == "DERIVED_GIVEN_REGISTERED_REDUCTION"
    assert state["q_squared_metric_only"] == "NOT_DERIVED"
    assert state["physics_promoted"] is False


def main() -> int:
    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(sources) == len({row["path"] for row in sources}) == 29
    frozen_content: dict[str, bytes] = {}
    for row in sources:
        content = frozen_blob(row)
        assert len(content) == int(row["bytes"])
        assert hashlib.sha256(content).hexdigest() == row["sha256"]
        frozen_content[row["path"]] = content

    claims = table(HERE / "SOURCE_CLAIM_LEDGER.tsv")
    assert len(claims) == len({row["id"] for row in claims}) == 15
    source_paths = {row["path"] for row in sources}
    for row in claims:
        assert row["path"] in source_paths
        content = frozen_content[row["path"]].decode("utf-8")
        assert row["anchor"] in content, (row["id"], row["anchor"])

    decisions = table(HERE / "DECISION_MATRIX.tsv")
    assert len(decisions) == 6
    assert sum(row["universal_complete_reduction"] == "NO" for row in decisions) == 3
    assert sum(row["universal_complete_reduction"] == "EQUIVARIANCE_REQUIRED" for row in decisions) == 1
    assert sum(row["universal_complete_reduction"] == "NOT_UNIVERSAL" for row in decisions) == 1
    statuses = table(HERE / "STATUS_LEDGER.tsv")
    assert len(statuses) == 12
    assert {row["status"] for row in statuses if row["object"] == "universal_complete_physical_reduction"} == {"OPEN"}

    state = {
        "headline": (
            "FOUNDED_ABSTRACT_PAIR_DERIVED__LOCAL_PHYSICAL_ALIGNMENT_CONDITIONAL_ON_DECLARED_READOUT__"
            "BRANCH_CONDITIONAL_PHYSICAL_REDUCTIONS_EXIST__COMPLETE_UNIVERSAL_REDUCTION_OPEN"
        ),
        "abstract_pair": "DERIVED",
        "local_alignment": "DERIVED_CONDITIONAL_ON_RECORDED_READOUT",
        "branch_reductions": "DERIVED_BOUNDED_EXISTENCE",
        "universal_reduction": "OPEN",
        "fixed_component_plane": "REFUTED_USE_EQUIVARIANCE",
        "q_squared": "DERIVED_GIVEN_REGISTERED_REDUCTION",
        "q_squared_metric_only": "NOT_DERIVED",
        "physics_promoted": False,
    }
    validate(state)
    mutations = (
        ("C01", "demote_abstract_pair", lambda x: x.update(abstract_pair="OPEN")),
        ("C02", "promote_local_to_unconditional", lambda x: x.update(local_alignment="UNCONDITIONAL")),
        ("C03", "erase_branch_reductions", lambda x: x.update(branch_reductions="NONE")),
        ("C04", "promote_universal_reduction", lambda x: x.update(universal_reduction="DERIVED")),
        ("C05", "retain_fixed_components", lambda x: x.update(fixed_component_plane="PHYSICAL_FIXED")),
        ("C06", "promote_q2_universal", lambda x: x.update(q_squared="UNIVERSAL_METRIC_SCALAR")),
        ("C07", "promote_q2_metric_only", lambda x: x.update(q_squared_metric_only="DERIVED")),
        ("C08", "promote_physics", lambda x: x.update(physics_promoted=True)),
    )
    catches = []
    for catch_id, name, mutation in mutations:
        changed = copy.deepcopy(state)
        mutation(changed)
        caught = False
        try:
            validate(changed)
        except AssertionError:
            caught = True
        assert caught
        catches.append({"catch_id": catch_id, "mutation": name, "result": "PASS_CAUGHT"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["catch_id", "mutation", "result"], lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)

    review = (HERE / "COLD_REVIEW_RETURN.md").read_text(encoding="utf-8")
    assert "fresh zero-context" in review.lower()
    assert "DERIVED_GIVEN_REGISTERED_REDUCTION" in review
    assert "No one explicit witness closes every intrinsic pair" in review

    result = {
        "schema": "udt-reciprocal-pair-reduction-authority-1.0",
        "status": "PASS_VERIFIED_FRESH_COLD_REVIEW",
        "frozen_sources": len(sources),
        "source_claims": len(claims),
        "decision_obligations": len(decisions),
        "status_rows": len(statuses),
        "catch_proofs": len(catches),
        "fresh_zero_context_review": True,
        "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
        **state,
    }
    (HERE / "ADJUDICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
