#!/usr/bin/env python3
"""Exercise ten fail-closed mutations against the artifact validator.

These are catch proofs for one validator, not an independent semantic proof.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify_cmb_query_map_artifact_consistency import load_current, validate


HERE = Path(__file__).resolve().parent


def caught(payloads) -> bool:
    return not all(validate(*payloads).values())


def main() -> None:
    base = load_current()
    mutations = []

    x = copy.deepcopy(base); x[0][0]["sha256"] = "0" * 64; mutations.append(("F01_source_hash", x))
    x = copy.deepcopy(base); x[1].append(copy.deepcopy(x[1][0])); mutations.append(("F02_duplicate_family", x))
    x = copy.deepcopy(base); x[1][1]["physical_CMB_pair_query"] = "SELECTED_NATIVE"; mutations.append(("F03_premise_promotion", x))
    x = copy.deepcopy(base); x[3][0]["screen_Jacobi"] = "DIRECT_IDENTITY"; mutations.append(("F04_missing_projection", x))
    x = copy.deepcopy(base); next(row for row in x[3] if row["observable"] == "PHYSICAL_TT_PEAK_POSITIONS")["source_population"] = "NOT_REQUIRED"; mutations.append(("F05_power_without_population", x))
    x = copy.deepcopy(base); next(row for row in x[3] if row["observable"] == "PHYSICAL_TT_PEAK_POSITIONS")["normal_transport"] = "DIRECT_SCALAR_TT_MODULATOR"; mutations.append(("F06_scalar_rotation_error", x))
    x = copy.deepcopy(base); next(row for row in x[2] if row["object"] == "P1_SNE_COMPATIBILITY_ANCHOR")["what_is_banked"] = "copy_P1_into_centered_CMB_lapse"; mutations.append(("F07_P1_role_error", x))
    x = copy.deepcopy(base); next(row for row in x[2] if row["object"] == "XMAX_ASYMPTOTIC_GUARD")["what_is_banked"] = "local_wall_and_branch_selector"; mutations.append(("F08_Xmax_frame_error", x))
    x = copy.deepcopy(base); next(row for row in x[2] if row["object"] == "PAIR_CONE_READOUT")["what_is_banked"] = "local_signal_speed"; mutations.append(("F09_local_signal_error", x))
    x = copy.deepcopy(base); x[1][2]["family_rank"] = "BEST"; mutations.append(("F10_postselection", x))

    results = {name: caught(payloads) for name, payloads in mutations}
    output = {
        "evidence_role": "validator_mutation_catches_not_independent_semantic_review",
        "all_catches_fire": all(results.values()),
        "caught": sum(results.values()),
        "total": len(results),
        "results": results,
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))
    if not all(results.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
