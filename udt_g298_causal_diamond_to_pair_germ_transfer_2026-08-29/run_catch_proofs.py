#!/usr/bin/env python3
"""Hostile semantic/algebra catches for G298."""

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent


def main():
    prereg = (ROOT / "PREREGISTRATION.md").read_text()
    ledger = (ROOT / "PREMISE_LEDGER.tsv").read_text()
    catches = {
        "unit_target_clock_cannot_carry_nonzero_depth": "uses `J=(U_Y,n_Y)`" in prereg,
        "target_local_ruler_screen_loss_registered": "target-local-null direction" in prereg,
        "reflection_smoothing_forbidden": "smooths the reflection kink" in prereg,
        "branch_preference_forbidden": "chooses one member" in prereg,
        "one_jet_not_history": "calls a one-jet" in prereg,
        "transport_not_input": "inserts transported frame" in prereg,
        "downstream_imports_excluded": "observations_sources_matter_action_field_equation_scale_Xmax\tOPEN_EXCLUDED" in ledger,
    }
    if not all(catches.values()):
        raise SystemExit(f"FAIL: {catches}")
    result = {"status": "PASS", "catches": catches, "count": len(catches)}
    if "--no-write" not in sys.argv:
        (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
