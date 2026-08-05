#!/usr/bin/env python3
"""Fail closed on the current Xmax asymptotic-limit meaning and workflow."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "VERIFICATION_RESULT.json"
SOURCE = f"{HERE.name}/STATUS_AND_WORKFLOW.md"
BASE = "81d39e369e1bc6de59199d7a357168f6067e858d"
CURRENT_CONTROLS = (
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "research/README.md",
)


def table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_g14(row: dict[str, str]) -> None:
    assert row["current_status"] == "WORKING_FOUNDATIONAL_POSITIONAL_DILATION_ASYMPTOTE"
    assert row["epistemic_label"] == "WORKING"
    assert row["active_use"] == "OWNER_RATIFIED_LIMIT_FRAME_AND_REQUIRED_DEPTH_LAW_GATE"
    assert row["controlling_source"] == SOURCE
    for token in (
        "exact observer/event/path separation-depth realization",
        "signed-magnitude join",
        "all-frame theorem",
        "numerical value",
        "WR-L/global join",
        "mass-density modulation",
    ):
        assert token in row["open_scope"]
    for token in (
        "optional analogy",
        "material wall",
        "center",
        "seal",
        "boundary functional",
        "selected tanh",
        "derived numerical constant",
    ):
        assert token in row["forbidden_regression"]


def validate_premises(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 10
    by_id = {row["id"]: row for row in rows}
    assert len(by_id) == 10
    assert by_id["P01"]["status"] == "WORKING_FOUNDATIONAL_FRAME"
    assert by_id["P03"]["status"] == "OPEN_REALIZATION"
    assert by_id["P04"]["status"] == "OWNER_REQUIRED_CANDIDATE_GATE"
    assert by_id["P05"]["status"] == "WORKING_INTENT__THEOREM_OPEN"
    assert by_id["P08"]["status"] == "OPEN"
    assert by_id["P09"]["status"] == "OPEN"
    assert by_id["P10"]["status"] == "OPEN_UNCHANGED"


def expect_failure(name: str, operation, caught: list[str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        caught.append(name)
        return
    raise AssertionError(f"mutation escaped: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    registry = {row["premise_id"]: row for row in table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")}
    validate_g14(registry["G14"])
    premises = table(HERE / "PREMISE_LEDGER.tsv")
    validate_premises(premises)
    reconciliation = table(HERE / "SOURCE_RECONCILIATION.tsv")
    assert len(reconciliation) == 6 and len({row["source"] for row in reconciliation}) == 6
    mutations = table(HERE / "CONTROL_MUTATION_LEDGER.tsv")
    assert len(mutations) == 10 and len({row["path"] for row in mutations}) == 10
    for row in mutations:
        prior = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        current = (ROOT / row["path"]).read_bytes()
        assert hashlib.sha256(prior).hexdigest() == row["base_sha256"]
        assert hashlib.sha256(current).hexdigest() == row["current_sha256"]
        assert row["mutation_class"] == "EXACT_STATUS_OR_WORKFLOW_POINTER_SUBSTITUTION"

    status_text = (HERE / "STATUS_AND_WORKFLOW.md").read_text(encoding="utf-8")
    for token in (
        "0 <= s(p,q) < X_max",
        "s(p,q) -> X_max from below  => |delta| -> infinity",
        "not a material wall",
        "Passing the asymptote",
        "necessary but not sufficient",
        "local WR-L `X` distinct from global `X_max`",
    ):
        assert token in status_text

    for control in CURRENT_CONTROLS:
        text = (ROOT / control).read_text(encoding="utf-8")
        assert SOURCE in text, control
        assert "positional-dilation asymptote" in text, control
    for control in ("LIVE.md", "HANDOFF.md"):
        text = (ROOT / control).read_text(encoding="utf-8")
        current = text.split("<!-- STARTUP_CURRENT_BEGIN -->", 1)[1].split(
            "<!-- STARTUP_CURRENT_END -->", 1
        )[0]
        assert SOURCE in current
        assert "numerical `X_max`" in current
        assert "wall" in current and "preferred center" in current

    caught: list[str] = []
    bad = dict(registry["G14"])
    bad["current_status"] = "OPTIONAL_ANALOGY"
    expect_failure("limit_role_reopened", lambda: validate_g14(bad), caught)
    bad = dict(registry["G14"])
    bad["open_scope"] = bad["open_scope"].replace("numerical value; ", "")
    expect_failure("numerical_value_promoted", lambda: validate_g14(bad), caught)
    bad = dict(registry["G14"])
    bad["open_scope"] = bad["open_scope"].replace("all-frame theorem; ", "")
    expect_failure("frame_theorem_promoted", lambda: validate_g14(bad), caught)
    bad = dict(registry["G14"])
    bad["forbidden_regression"] = bad["forbidden_regression"].replace("material wall ", "")
    expect_failure("wall_guard_removed", lambda: validate_g14(bad), caught)
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["id"] == "P03")["status"] = "IDENTICAL_TO_SIGNED_DEPTH"
    expect_failure("signed_magnitude_merged", lambda: validate_premises(bad), caught)
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["id"] == "P08")["status"] = "DERIVED_EQUAL"
    expect_failure("wrl_global_join_promoted", lambda: validate_premises(bad), caught)
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["id"] == "P10")["status"] = "DERIVED_BOUNDARY_TERM"
    expect_failure("boundary_completion_inferred", lambda: validate_premises(bad), caught)
    bad = [dict(row) for row in premises]
    next(row for row in bad if row["id"] == "P04")["status"] = "SELECTED_TANH_PROFILE"
    expect_failure("profile_selected_from_asymptote", lambda: validate_premises(bad), caught)
    assert len(caught) == 8

    result = {
        "schema": "udt.xmax_asymptotic_limit_frame.verification.v1",
        "status": "PASS",
        "premise_rows": len(premises),
        "source_reconciliation_rows": len(reconciliation),
        "control_mutation_rows": len(mutations),
        "current_controls": len(CURRENT_CONTROLS),
        "catch_proofs": caught,
        "maximum_conclusion": "STATUS_AND_WORKFLOW_CORRECTION_ONLY",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUTPUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
