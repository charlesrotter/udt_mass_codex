#!/usr/bin/env python3
"""Exercise the G73 topology-scope correction catches."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path

from verify_external_review_adjudication import validate_scope


HERE = Path(__file__).resolve().parent


def rows() -> list[dict[str, str]]:
    with (HERE / "TOPOLOGY_SCOPE_LEDGER.tsv").open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    base = rows()
    assert validate_scope(base)
    keyed = {row["case"]: index for index, row in enumerate(base)}
    mutations = {}

    def challenge(name: str, case: str, field: str, value: str) -> None:
        candidate = deepcopy(base)
        candidate[keyed[case]][field] = value
        mutations[name] = not validate_scope(candidate)

    challenge("whole_s2_singularity_erased", "WHOLE_S2_SELF_MAP", "singularity_requirement", "NOT_REQUIRED")
    challenge("different_topology_forced_singular", "DIFFERENT_TOPOLOGY", "singularity_requirement", "ALWAYS_REQUIRED")
    challenge("partial_sky_forced_singular", "PARTIAL_OR_NONCOMPACT_SKY", "singularity_requirement", "ALWAYS_REQUIRED")
    challenge("branch_set_denied", "BRANCH_LABELLED_RELATION", "regular_multiplicity_status", "IMPOSSIBLE")
    challenge("branch_combination_promoted", "BRANCH_LABELLED_RELATION", "udt_owner_status", "DERIVED_SUM")
    challenge("strong_shear_called_repetition", "STRONG_SHEAR_SINGLE_BRANCH", "regular_multiplicity_status", "REPEATED_IMAGE")
    missing = deepcopy(base); missing.pop(); mutations["missing_case"] = not validate_scope(missing)
    duplicate = deepcopy(base); duplicate.append(deepcopy(base[0])); mutations["duplicate_case"] = not validate_scope(duplicate)
    assert all(mutations.values()), [name for name, value in mutations.items() if not value]
    payload = {
        "schema": "udt-cmb-g73-external-catches-v1",
        "caught": mutations,
        "passed": sum(mutations.values()),
        "total": len(mutations),
    }
    (HERE / "EXTERNAL_REVIEW_CATCH_PROOFS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
