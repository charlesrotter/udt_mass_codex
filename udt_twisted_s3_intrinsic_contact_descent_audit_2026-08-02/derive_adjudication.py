#!/usr/bin/env python3
"""Bind the repaired production result to the fresh cold-review verdict."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


assert digest(HERE / "PREREGISTRATION.md") == "2535d0be7eca5213afb83210adebde2820da502e35baeee6d14eac1bf007144c"
assert digest(HERE / "SOURCE_MANIFEST.tsv") == "b0ea71998dc5e0cb1c2e1aebe4f256c541863e062ceaf30625e304e80765ad4d"
assert digest(HERE / "verify_semantics.py") == "f35a8e2f58d34ebed387cc8b8483e33ad97afb8002aac58dc2ebb67424b8b8c9"
assert digest(HERE / "DERIVATION_RESULT.json") == "cc49a65de1d888b01d19f66e6ff069e8eaf3d101505ffb3b4c59dd346af5b724"
assert digest(HERE / "DESCENT_ATLAS.tsv") == "4b03f0206f5d9b9e3921e074eb67db765ab46be2b6c6fbf059a8d801da86fa8a"
assert digest(HERE / "CATCH_PROOFS.tsv") == "35047e72d558b61a179b031600062796b063d511ba8c13e52520f959015c39a5"
review = (HERE / "COLD_REVIEW_RETURN.md").read_text(encoding="utf-8")
assert "Final verdict: `VERIFIED`" in review and "All four gates pass" in review
result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
atlas = table("DESCENT_ATLAS.tsv")
subclasses = table("O13_SUBCLASSIFICATION.tsv")
catches = table("CATCH_PROOFS.tsv")
assert len(atlas) == result["objects_classified"] == 22
assert len(subclasses) == result["O13_subclassifications"] == 2
assert len(catches) == 24 and all(row["result"] == "PASS_CAUGHT" for row in catches)
assert result["realized_contact_stratum"] == "Q_POSITIVE_ONLY"
assert result["contact_two_form_on_witness"] == "IDENTICALLY_ZERO"
assert result["full_GL2_generality_claimed"] is result["on_shell_claimed"] is False
assert result["universal_claimed"] is result["physics_promoted"] is False

adjudication = {
    "schema": "udt-twisted-s3-intrinsic-contact-adjudication-1.0",
    "status": "PASS_VERIFIED_FRESH_COLD_REVIEW",
    "headline": "METRIC_DERIVED_PROJECTOR_MAKES_QT_QS_Q_INTRINSIC_ON_EXPLICIT_WITNESS__Q_POSITIVE__PHI_CONTACT_ABSOLUTE_ON_FROZEN_UNIT_WITNESS__ALTERNATING_CONTACT_TWO_FORM_ZERO__GENERAL_SCREEN_AND_SELECTION_OPEN",
    "parent_objects": 22,
    "O13_subclassifications": 2,
    "lambda_certificates": 3,
    "controls": 10,
    "catches": 24,
    "independent_coordinate_checks": 15,
    "maximum_Q_absolute_error": "3.98e-12",
    "contact_stratum": "Q_POSITIVE_ONLY_ON_WITNESS",
    "absolute_Phi_contact": "DERIVED_METRIC_SCALAR_ON_FROZEN_a_EQUALS_R_EQUALS_ONE_WITNESS",
    "absolute_sigma": "REFERENCE_DEPENDENT__DSIGMA_INTRINSIC",
    "alternating_contact_two_form": "DERIVED_IDENTICALLY_ZERO_ON_WITNESS",
    "full_GL2_neighborhood": "OPEN_NOT_TESTED",
    "on_shell_selection": "OPEN_NOT_CLAIMED",
    "universal_selection": "OPEN_NOT_CLAIMED",
    "physics_promoted": False,
    "four_gates": "PASS_ALL_FOUR",
}
(HERE / "ADJUDICATION_RESULT.json").write_text(
    json.dumps(adjudication, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(adjudication, sort_keys=True))
