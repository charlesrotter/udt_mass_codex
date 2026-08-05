#!/usr/bin/env python3
"""Independent standard-library replay of the Xmax status/control correction."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "udt_xmax_asymptotic_limit_frame_correction_2026-08-05"
CONTROLS = (
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "AGENTS.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "research/README.md",
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    registry_rows = read_tsv(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    assert len(registry_rows) == 18
    g14 = next(row for row in registry_rows if row["premise_id"] == "G14")
    assert g14 == {
        "premise_id": "G14",
        "term": "Xmax",
        "current_status": "WORKING_FOUNDATIONAL_POSITIONAL_DILATION_ASYMPTOTE",
        "epistemic_label": "WORKING",
        "active_use": "OWNER_RATIFIED_LIMIT_FRAME_AND_REQUIRED_DEPTH_LAW_GATE",
        "open_scope": (
            "exact observer/event/path separation-depth realization; signed-magnitude join; "
            "all-frame theorem; numerical value; WR-L/global join; angular/bootstrap and "
            "mass-density modulation"
        ),
        "forbidden_regression": (
            "optional analogy; material wall edge radius center seal or boundary functional; "
            "selected tanh fractional-linear or WR-L profile; derived numerical constant"
        ),
        "controlling_source": (
            "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md"
        ),
        "precedence_rule": "LIVE_THEN_THIS_REGISTRY_THEN_CITED_SOURCE__CONFLICT_MEANS_STOP",
    }

    premise_rows = read_tsv(PACKAGE / "PREMISE_LEDGER.tsv")
    assert [row["id"] for row in premise_rows] == [f"P{i:02d}" for i in range(1, 11)]
    status_by_id = {row["id"]: row["status"] for row in premise_rows}
    assert status_by_id == {
        "P01": "WORKING_FOUNDATIONAL_FRAME",
        "P02": "DERIVED_ON_SUPPLIED_DEPTH",
        "P03": "OPEN_REALIZATION",
        "P04": "OWNER_REQUIRED_CANDIDATE_GATE",
        "P05": "WORKING_INTENT__THEOREM_OPEN",
        "P06": "RETAINED_FRAME_PRINCIPLE",
        "P07": "OBSERVED_CALIBRATION_ANCHOR",
        "P08": "OPEN",
        "P09": "OPEN",
        "P10": "OPEN_UNCHANGED",
    }

    status = (PACKAGE / "STATUS_AND_WORKFLOW.md").read_text(encoding="utf-8")
    assert status.count("0 <= s(p,q) < X_max") == 1
    assert status.count("s(p,q) -> X_max from below  => |delta| -> infinity") == 1
    assert "It is not a derivation of `s`, `delta(s)`" in status
    assert "No two of these may be identified by name alone." in status
    assert "many functions can share the same limiting behavior" in status

    payload = []
    source = f"{PACKAGE.name}/STATUS_AND_WORKFLOW.md"
    for name in CONTROLS:
        text = (ROOT / name).read_text(encoding="utf-8")
        if name in {"LIVE.md", "HANDOFF.md"}:
            text = text.split("<!-- STARTUP_CURRENT_BEGIN -->", 1)[1].split(
                "<!-- STARTUP_CURRENT_END -->", 1
            )[0]
        assert source in text
        assert "positional-dilation asymptote" in text
        payload.append(name + "\n" + text)
    control_sha = hashlib.sha256("\n".join(payload).encode()).hexdigest()

    reconciliation = read_tsv(PACKAGE / "SOURCE_RECONCILIATION.tsv")
    assert len(reconciliation) == 6
    assert all(row["retained_open_scope"] for row in reconciliation)
    assert not any("PROMOTE" in row["correction_effect"] for row in reconciliation)

    print(
        "PASS independent: G14 exact; 10 premise rows; 6 reconciled sources; "
        f"7 current controls; control_sha256={control_sha}"
    )


if __name__ == "__main__":
    main()
