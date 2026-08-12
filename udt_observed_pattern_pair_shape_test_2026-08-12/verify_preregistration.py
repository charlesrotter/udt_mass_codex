#!/usr/bin/env python3
"""Verify the frozen pattern-shape preregistration before residual evaluation."""

from __future__ import annotations

import csv
import io
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def rows(name: str):
    with (ROOT / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    premises = rows("PREMISE_LEDGER.tsv")
    gates = rows("FALSIFICATION_CONTRACT.tsv")
    sources = rows("SOURCE_MANIFEST.tsv")
    frozen_status_text = subprocess.check_output(
        [
            "git",
            "show",
            "efdecd35:udt_observed_pattern_pair_shape_test_2026-08-12/STATUS_LEDGER.tsv",
        ],
        cwd=ROOT.parent,
        text=True,
    )
    status = list(csv.DictReader(io.StringIO(frozen_status_text), delimiter="\t"))
    prereg = (ROOT / "PREREGISTRATION.md").read_text()

    assert len(premises) == 15
    assert len(gates) == 10
    assert len(sources) == 9
    assert len(status) == 7
    assert "F_pair" in prereg and "d_A (dz/dlambda)/L_pair" in prereg
    assert "F_C0(z)=z+z^2/2" in prereg
    assert "n=1.0559332414320268" in prereg
    assert "12.592" in prereg and "22.458" in prereg
    assert "No outcome may select the physical complete history" in prereg
    assert all(row["status"] == "ABSENT" for row in status if "outcome" in row["item"] or "residual" in row["item"])
    assert any(row["status"] == "INACTIVE_FORBIDDEN" for row in premises)
    print("Pattern-shape preregistration: 15 premises, 10 gates, 9 sources; PASS")


if __name__ == "__main__":
    main()
