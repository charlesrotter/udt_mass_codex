#!/usr/bin/env python3
"""Exercised semantic catches for the G72 external-review layer."""

from __future__ import annotations

import json
from pathlib import Path

from verify_external_review_adjudication import validate_review_text


HERE = Path(__file__).resolve().parent


def main() -> None:
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    assert validate_review_text(raw)
    mutations = {
        "wrong_landing": raw.replace("VERIFIED_AS_CONDITIONAL_RESPONSE", "PHYSICAL_CMB_DERIVED", 1),
        "common_query_removed": raw.replace("same supplied calibrated query", "untyped path", 1),
        "physical_observables_promoted": raw.replace("physical TT/TE/EE/BB open", "physical TT/TE/EE/BB derived", 1),
        "psi_identified_with_rotation": raw.replace("`psi` is decisively not the relative polar rotation", "`psi` is the relative polar rotation", 1),
        "local_scope_erased": raw.replace("zero/constant-source argument is valid only as a local order-zero response statement", "zero/constant-source argument is a global theorem", 1),
        "sne_promoted_to_selector": raw.replace("SNe P1 remains only a future low-redshift compatibility anchor", "SNe P1 selects the CMB profile", 1),
    }
    caught = {name: not validate_review_text(candidate) for name, candidate in mutations.items()}
    assert all(caught.values()), [name for name, value in caught.items() if not value]
    payload = {
        "schema": "udt-cmb-g72-external-catches-v1",
        "caught": caught,
        "passed": sum(caught.values()),
        "total": len(caught),
    }
    (HERE / "EXTERNAL_REVIEW_CATCH_PROOFS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
