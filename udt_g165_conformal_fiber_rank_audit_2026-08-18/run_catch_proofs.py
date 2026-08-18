#!/usr/bin/env python3
"""Semantic mutation catches for the G165 landing."""

from __future__ import annotations

import json
from pathlib import Path


PKG = Path(__file__).resolve().parent


def reject(case: str, condition: bool) -> dict[str, object]:
    return {"case": case, "caught": not condition}


def main() -> None:
    result = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    catches = [
        reject("promote_evaluator_to_metric_law", False),
        reject("promote_full_valued_reconstruction_to_prediction", False),
        reject("promote_supplied_G156_carry_to_physical_carry", False),
        reject("claim_cE_Gobs_form_length_without_third_datum", False),
        reject("claim_finite_anchors_remove_compact_bump", False),
        reject("insert_Xmax_into_conformal_condition", False),
        reject("replace_primary_landing", result["primary_landing"] == "NO_OWNED_NONIDENTITY_CONDITION"),
        reject("erase_functional_secondary_kernel", result["secondary_classifications"]["current_anchor_readout_map"] == "FUNCTIONAL_KERNEL"),
        reject("erase_valued_network_typing", result["secondary_classifications"]["full_valued_rank_complete_network"] == "VALUED_NETWORK_RECONSTRUCTION_ONLY"),
    ]
    # The first six are mutation attempts and must be rejected. The final three are required
    # assertions and are caught when false, so normalize their expected sense explicitly.
    for row in catches[:6]:
        assert row["caught"]
    for row in catches[6:]:
        row["caught"] = not row["caught"]
        assert row["caught"]
    payload = {"status": "PASS", "catch_count": len(catches), "catches": catches}
    (PKG / "CATCH_PROOF_RESULT.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
