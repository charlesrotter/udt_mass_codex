#!/usr/bin/env python3
"""Mutation checks for the G71 literal-citation correction layer."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path

from verify_external_review_adjudication import validate_overlay


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    original = table("SOURCE_TARGET_ATLAS.tsv")
    overlay = table("SOURCE_TARGET_LITERAL_CITATION_OVERLAY.tsv")
    assert validate_overlay(original, overlay)
    caught = {}

    def challenge(name: str, candidate: list[dict[str, str]]) -> None:
        caught[name] = not validate_overlay(original, candidate)

    candidate = deepcopy(overlay); candidate.pop(); challenge("missing_source", candidate)
    candidate = deepcopy(overlay); candidate.append(deepcopy(candidate[0])); challenge("duplicate_source", candidate)
    candidate = deepcopy(overlay); candidate[0]["literal_token"] = "NONLITERAL_PARAPHRASE"; challenge("nonliteral_token", candidate)
    candidate = deepcopy(overlay); candidate[0]["line_number"] = "1"; challenge("wrong_line_number", candidate)
    candidate = deepcopy(overlay); candidate[0]["source_path"] = overlay[1]["source_path"]; challenge("wrong_source", candidate)
    candidate = deepcopy(overlay); candidate[0]["source_shape"] = "OWNED_NATIVE"; challenge("status_promotion", candidate)
    candidate = deepcopy(overlay); candidate[4]["geometric_carry"] = "OWNED_NATIVE"; challenge("carry_promotion", candidate)
    candidate = deepcopy(overlay); candidate[5]["source_role"] = "WRONG_ROLE"; challenge("role_drift", candidate)

    assert all(caught.values()), [name for name, value in caught.items() if not value]
    result = {"schema": "udt-cmb-g71-external-catches-v1", "caught": caught,
              "passed": sum(caught.values()), "total": len(caught)}
    (HERE / "EXTERNAL_REVIEW_CATCH_PROOFS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
