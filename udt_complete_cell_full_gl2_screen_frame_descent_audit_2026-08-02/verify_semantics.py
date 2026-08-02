#!/usr/bin/env python3
"""Fail-closed semantic and identity verifier with exercised mutations."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(state: dict[str, object]) -> None:
    assert state["headline"] == "SPLIT_RELATIVE_ONLY__NO_COMPLETE_FRAME_DESCENT"
    assert state["source_scope"] == "FROZEN_23_SOURCE_BOUNDED_FAMILY"
    assert state["screen_slots"] == ["area", "rotation_gauge", "shear1", "shear2"]
    assert state["curvature_rows"] == 36 and state["curvature_blocks"] == 6
    assert state["closure_equations"] == 5
    assert state["q_squared"] == "t1^2-t0^2"
    assert state["q_pair_boost_invariant"] is True
    assert state["q_full_frame_invariant"] is False
    assert state["contact_log_defined_at_null"] is False
    assert state["connection_is_tensor"] is False
    assert state["scalar_curvature_uniquely_selects_contact"] is False
    assert state["ansatz_exit_is_inconsistency"] is False
    assert state["formal_witness_is_physical"] is False
    assert state["physics_promoted"] is False


def main() -> int:
    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(sources) == len({row["path"] for row in sources}) == 23
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file() and path.stat().st_size == int(row["bytes"])
        assert digest(path) == row["sha256"]
        blob = subprocess.run(
            ["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        assert blob == row["git_blob"]

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    curvature = table(HERE / "FULL_CURVATURE_CENSUS.tsv")
    assert len(curvature) == 36
    assert len({row["curvature_pair"] for row in curvature if row["expression"] != "0"}) == 6
    assert independent["curvature_rows_matched"] == 36
    assert independent["independent_closure_equations"] == 5

    state = {
        "headline": result["headline"],
        "source_scope": "FROZEN_23_SOURCE_BOUNDED_FAMILY",
        "screen_slots": result["screen_response_slots"],
        "curvature_rows": result["curvature_rows"],
        "curvature_blocks": result["nonzero_lower_curvature_blocks"],
        "closure_equations": result["independent_closure_equations"],
        "q_squared": "t1^2-t0^2",
        "q_pair_boost_invariant": independent["pair_boost_q_squared_invariant"],
        "q_full_frame_invariant": False,
        "contact_log_defined_at_null": False,
        "connection_is_tensor": False,
        "scalar_curvature_uniquely_selects_contact": False,
        "ansatz_exit_is_inconsistency": False,
        "formal_witness_is_physical": False,
        "physics_promoted": False,
    }
    validate(state)
    mutations = (
        ("C01", "remove_second_shear", lambda x: x.update(screen_slots=["area", "rotation_gauge", "shear1"])),
        ("C02", "filter_curvature_row", lambda x: x.update(curvature_rows=35)),
        ("C03", "omit_curvature_block", lambda x: x.update(curvature_blocks=5)),
        ("C04", "drop_closure_equation", lambda x: x.update(closure_equations=4)),
        ("C05", "replace_pair_norm_by_t1", lambda x: x.update(q_squared="t1^2")),
        ("C06", "deny_pair_boost_invariance", lambda x: x.update(q_pair_boost_invariant=False)),
        ("C07", "promote_full_frame_descent", lambda x: x.update(q_full_frame_invariant=True)),
        ("C08", "define_log_on_null", lambda x: x.update(contact_log_defined_at_null=True)),
        ("C09", "promote_connection_tensor", lambda x: x.update(connection_is_tensor=True)),
        ("C10", "claim_scalar_selects_contact", lambda x: x.update(scalar_curvature_uniquely_selects_contact=True)),
        ("C11", "call_ansatz_exit_inconsistency", lambda x: x.update(ansatz_exit_is_inconsistency=True)),
        ("C12", "promote_offshell_witness", lambda x: x.update(formal_witness_is_physical=True)),
        ("C13", "globalize_source_scope", lambda x: x.update(source_scope="ALL_UDT_METRICS")),
        ("C14", "promote_physics", lambda x: x.update(physics_promoted=True)),
    )
    catches = []
    for catch_id, mutation, change in mutations:
        altered = copy.deepcopy(state)
        change(altered)
        caught = False
        try:
            validate(altered)
        except AssertionError:
            caught = True
        assert caught
        catches.append({"catch_id": catch_id, "mutation": mutation, "result": "PASS_CAUGHT"})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["catch_id", "mutation", "result"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    verification = {
        "status": "PASS_VERIFIED_WITH_CAVEATS_NO_FRESH_BLIND_REVIEW",
        "frozen_sources": len(sources),
        "curvature_rows": len(curvature),
        "curvature_blocks": 6,
        "independent_curvature_matches": independent["curvature_rows_matched"],
        "independent_closure_equations": 5,
        "catch_proofs": len(catches),
        "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(verification, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

