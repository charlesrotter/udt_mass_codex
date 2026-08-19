#!/usr/bin/env python3
"""Semantic mutation catches for the bounded G166 landing."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    report = " ".join((HERE / "AUDIT_REPORT.md").read_text().split())
    report_lower = report.lower()
    catches = {
        "no_fixed_path_input": "does not begin with a path or pre-existing distance" in report_lower,
        "orchestra_precedes_readout": "enters the pair metric before the scalar readout" in report_lower,
        "no_independent_kernel_profile": "no second response profile" in report_lower,
        "no_xmax_in_kernel": "`x_max`, which remains downstream" in report_lower,
        "general_envelope_not_solution_space": "does not establish that this envelope is the derived udt solution space" in report_lower,
        "general_assembly_still_conditional": "general nonspherical, mixing, and time-live assembly remains conditional" in report_lower,
        "network_carry_not_erased": "arbitrary observer-network calibration carry remains open" in report_lower,
        "ceff_not_signal_speed": "not a local material signal speed" in report_lower,
        "g165_retained_as_control": "G165 remains a valid control" in report,
    }
    result = {
        "status": "PASS" if all(catches.values()) else "FAIL",
        "catches": catches,
        "passed": sum(catches.values()),
        "total": len(catches),
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if not all(catches.values()):
        raise SystemExit(f"FAIL: {[k for k, v in catches.items() if not v]}")
    print(f"PASS: {len(catches)} semantic mutation catches")


if __name__ == "__main__":
    main()
