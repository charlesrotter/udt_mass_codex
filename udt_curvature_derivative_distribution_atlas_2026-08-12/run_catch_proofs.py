#!/usr/bin/env python3
"""Baseline-first hostile mutations for the derivative-atlas package."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

from verify_package import rows, validate


HERE = Path(__file__).resolve().parent


def state() -> dict:
    return {
        "p": rows("DERIVATIVE_DISTRIBUTION_ATLAS.tsv"),
        "a": rows("ADJUDICATED_DERIVATIVE_ATLAS.tsv"),
        "c": rows("INDEPENDENT_COMPARISON.tsv"),
        "d": json.loads((HERE / "DERIVATION_RESULT.json").read_text()),
        "i": json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text()),
        "j": json.loads((HERE / "ADJUDICATION_RESULT.json").read_text()),
        "t": json.loads((HERE / "TENSOR_IDENTITY_VERIFICATION.json").read_text()),
        "m": rows("SOURCE_MANIFEST.tsv"),
        "r": rows("RAW_ARTIFACT_MANIFEST.tsv"),
        "gp": rows("GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv"),
        "gi": rows("INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv"),
        "gc": rows("GRAM_INTRINSIC_SUBSPACE_COMPARISON.tsv"),
        "ga": rows("ADJUDICATED_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv"),
        "gpr": json.loads((HERE / "GRAM_INTRINSIC_SUBSPACE_RESULT.json").read_text()),
        "gir": json.loads((HERE / "INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_RESULT.json").read_text()),
        "gar": json.loads((HERE / "GRAM_INTRINSIC_SUBSPACE_ADJUDICATION.json").read_text()),
        "s": rows("STATUS_LEDGER.tsv"),
    }


def check(s: dict) -> dict:
    return validate(s["p"], s["a"], s["c"], s["d"], s["i"], s["j"], s["t"], s["m"], s["r"], s["gp"], s["gi"], s["gc"], s["ga"], s["gpr"], s["gir"], s["gar"], s["s"])


def expect(name, mutation, baseline):
    changed = copy.deepcopy(baseline)
    mutation(changed)
    try:
        check(changed)
    except Exception:
        return {"catch": name, "status": "CAUGHT"}
    raise RuntimeError(f"mutation escaped: {name}")


def main() -> None:
    baseline = state()
    check(baseline)
    mutations = [
        ("drop_jet", lambda s: s["p"].pop()),
        ("duplicate_key", lambda s: s["p"][1].update(scope=s["p"][0]["scope"], identity=s["p"][0]["identity"], point=s["p"][0]["point"])),
        ("drop_G63", lambda s: s["p"].__setitem__(slice(None), [r for r in s["p"] if r["scope"] != "G63"])),
        ("invent_registered_SPI", lambda s: s["p"][0].update(spi_class="SPI_RANK2_REGISTERED_PAIR")),
        ("hide_unresolved", lambda s: s["a"][0].update(cross_route_status="VERIFIED") if s["a"][0]["cross_route_status"] != "VERIFIED" else next(r for r in s["a"] if r["cross_route_status"] != "VERIFIED").update(cross_route_status="VERIFIED")),
        ("promote_misaligned_owner", lambda s: next(r for r in s["a"] if r["parent_owner_class"] == "SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS").update(tested_derivative_owner="TRUE", ownership_adjudication="POSITIVE_OWNER")),
        ("drop_independent_row", lambda s: s["c"].pop()),
        ("false_independent_pass", lambda s: next(r for r in s["c"] if r["pass"] == "FALSE").update({"pass": "TRUE"})),
        ("Gram_route_disagreement", lambda s: s["c"][0].update(independent_gram_classes="CORRUPTED")),
        ("loosen_tensor_gate", lambda s: s["i"].update(max_tensor_relative_error=6e-3)),
        ("loosen_ladder_gate", lambda s: s["i"].update(max_outer_ladder_difference=6e-3)),
        ("wrong_primary_landing", lambda s: s["j"].update(primary_landing="FIRST_DERIVATIVE_CONCOMITANTS_OWN_REGISTERED_SPLIT_ON_ALL_PRIOR_MISALIGNED_JETS")),
        ("promote_history", lambda s: s["j"].update(no_physical_history_selected=False)),
        ("promote_query", lambda s: s["j"].update(no_query_or_realization_selected=False)),
        ("identity_gate_broken", lambda s: s["t"]["maximum_defects"].update(riemann_differential_bianchi=3e-8)),
        ("source_hash_corrupt", lambda s: s["m"][0].update(sha256="0" * 64)),
        ("raw_artifact_hash_corrupt", lambda s: s["r"][0].update(sha256="0" * 64)),
        ("drop_Gram_spectral_row", lambda s: s["gp"].pop()),
        ("erase_Gram_spectral_blocks", lambda s: s["gp"][0].update(spectral_blocks_json="")),
        ("promote_spectral_unresolved", lambda s: next(r for r in s["ga"] if r["cross_route_status"] == "SPECTRALLY_UNRESOLVED").update(cross_route_status="VERIFIED", adjudicated_structure="FOUR_REAL_SIMPLE_LINES")),
        ("corrupt_spectral_comparison", lambda s: next(r for r in s["gc"] if r["pass"] == "TRUE" and any(a["key"] == r["key"] and a["tensor"] == r["tensor"] and a["cross_route_status"] == "VERIFIED" for a in s["ga"])).update({"pass": "FALSE"})),
        ("inflate_derivative_owners", lambda s: s["j"].update(derivative_owner_count=7)),
        ("erase_misaligned_ownership_uncertainty", lambda s: s["j"].update(prior_misaligned_ownership_unresolved_count=0, prior_misaligned_resolved_no_owner_count=1194)),
        ("erase_package_caveat", lambda s: next(r for r in s["s"] if r["object"] == "package").update(result="SETTLED")),
    ]
    output = [expect(name, mutation, baseline) for name, mutation in mutations]
    result = {"status": "PASS", "catch_count": len(output), "caught": sum(row["status"] == "CAUGHT" for row in output)}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("catch", "status"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
