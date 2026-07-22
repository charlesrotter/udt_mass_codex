#!/usr/bin/env python3
"""Replay every post-outcome numerical-margin identity with the independent verifier."""

from __future__ import annotations

import csv
import gzip
import json
import os
from pathlib import Path

import numpy as np

from verify_motif_atlas import (
    COMPARE,
    HERE,
    PARENT,
    classify,
    digest,
    objects,
    operators,
    read_tsv,
    set_distance,
    transform_jets,
    transforms,
)


EXPECTED_HASHES = {
    "NUMERIC_MARGIN_LEDGER.tsv": "9eb973bbfcb56502c451f89464b51229b3dab4a0d55ba8e201d44b9a39007971",
    "FAMILY_MOTIF_ATLAS.tsv.gz": "af8f4f68deb95fd7136f605d0a70989cad6b6a589695117086fc617942332926",
    "NONLINEAR_FAMILY_COMPARISON.tsv.gz": "fa27912f151d06f32ed376fceb2c3df9d4fb14ddeaad2668bbce5077c5e25b17",
}


def gzip_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def write_tsv(path: Path, fields, rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    for relative, expected in EXPECTED_HASHES.items():
        if digest(HERE / relative) != expected:
            raise AssertionError(f"pinned margin source {relative}")
    margins = read_tsv(HERE / "NUMERIC_MARGIN_LEDGER.tsv")
    targets = sorted({(row["configuration_id"], row["family_id"]) for row in margins})
    target_ids = {item[0] for item in targets}
    registry = {row["family_id"]: tuple(row["operator_keys"].split(";"))
                for row in read_tsv(HERE / "INSTRUMENT_SUBSET_REGISTRY.tsv")}
    raw_by_id = {}
    for shard in read_tsv(PARENT / "RAW_SHARD_REGISTRY.tsv"):
        path = PARENT / shard["path"]
        if digest(path) != shard["sha256"]: raise AssertionError("raw shard")
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                raw = json.loads(line)
                if raw["configuration_id"] in target_ids: raw_by_id[raw["configuration_id"]] = raw
    if set(raw_by_id) != target_ids: raise AssertionError("margin raw coverage")

    saved_original = {(row["configuration_id"], row["family_id"]): row
                      for row in gzip_rows(HERE / "FAMILY_MOTIF_ATLAS.tsv.gz")
                      if (row["configuration_id"], row["family_id"]) in set(targets)}
    saved_nonlinear = {(row["configuration_id"], row["transform_id"], row["family_id"]): row
                       for row in gzip_rows(HERE / "NONLINEAR_FAMILY_COMPARISON.tsv.gz")
                       if (row["configuration_id"], row["family_id"]) in set(targets)}
    if len(saved_original) != len(targets) or len(saved_nonlinear) != 2 * len(targets):
        raise AssertionError("saved margin coverage")

    output_rows = []; mismatches = 0; uncertain_classifications = 0; maximum_projector_distance = 0.0
    for cid, family_id in targets:
        raw = raw_by_id[cid]; keys = registry[family_id]
        g = np.asarray(raw["metric"]); dg = np.asarray(raw["metric_first"]); ddg = np.asarray(raw["metric_second"])
        pf = np.asarray(raw["phi"]["first"]); ps = np.asarray(raw["phi"]["second"])
        current_objects, _ = objects(g, dg, ddg, pf, ps)
        scalar = {key: current_objects[key] for key in ("R", "H", "D")}
        original = classify(operators(current_objects, keys), current_objects["gradient"], g, scalar, keys)
        saved = saved_original[(cid, family_id)]
        original_discordant = [field for field in COMPARE if str(original[field]) != saved[field]]
        uncertain_classifications += original["numeric_status"] != "NUMERIC_CLASSIFIED"
        mismatches += bool(original_discordant)
        transform_discordant = []
        for transform_id, j, k, ell in transforms():
            transformed = transform_jets(g, dg, ddg, raw["phi"]["value"], pf, ps, j, k, ell)
            transformed_objects, _ = objects(transformed[0], transformed[1], transformed[2], transformed[4], transformed[5])
            transformed_scalar = {key: transformed_objects[key] for key in ("R", "H", "D")}
            transformed_result = classify(operators(transformed_objects, keys), transformed_objects["gradient"],
                                          transformed_objects["metric"], transformed_scalar, keys)
            saved_transform = saved_nonlinear[(cid, transform_id, family_id)]
            fields = [field for field in COMPARE if original[field] != transformed_result[field]]
            expected_uncertain = original["numeric_status"] != "NUMERIC_CLASSIFIED" or transformed_result["numeric_status"] != "NUMERIC_CLASSIFIED"
            current_discordance = []
            if saved_transform["original_numeric_status"] != original["numeric_status"]: current_discordance.append("original_numeric_status")
            if saved_transform["transformed_numeric_status"] != transformed_result["numeric_status"]: current_discordance.append("transformed_numeric_status")
            if saved_transform["classification_agreement"] != ("YES" if not fields else "NO"): current_discordance.append("classification_agreement")
            if saved_transform["numeric_status"] != ("NUMERIC_UNCERTAIN" if expected_uncertain else "NUMERIC_CLASSIFIED"): current_discordance.append("comparison_numeric_status")
            transform_discordant.extend(f"{transform_id}:{field}" for field in current_discordance)
            uncertain_classifications += transformed_result["numeric_status"] != "NUMERIC_CLASSIFIED"
        mismatches += bool(transform_discordant)
        output_rows.append({
            "configuration_id": cid, "family_id": family_id,
            "original_numeric_status": original["numeric_status"],
            "original_discordant_fields": ";".join(original_discordant),
            "transformed_accounting_discordances": ";".join(transform_discordant),
            "result": "PASS" if not original_discordant and not transform_discordant else "DISCORDANT",
        })
    write_tsv(HERE / "MARGIN_ESCALATION_COMPARISON.tsv",
              ("configuration_id", "family_id", "original_numeric_status", "original_discordant_fields",
               "transformed_accounting_discordances", "result"), output_rows)
    result = {
        "status": "PASS" if mismatches == 0 else "FAIL",
        "margin_ledger_rows": len(margins), "unique_target_identities": len(targets),
        "original_classifications": len(targets), "transformed_classifications": 2 * len(targets),
        "independent_uncertain_classifications": uncertain_classifications,
        "discordant_identities": mismatches,
        "targeting": "POST_OUTCOME_ALL_MARGIN_IDENTITIES",
    }
    (HERE / "MARGIN_ESCALATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [f"UDT_MOTIF_MARGIN_ESCALATION={result['status']}",
                  f"ledger_rows={len(margins)} identities={len(targets)} original={len(targets)} transformed={2*len(targets)}",
                  f"independent_uncertain={uncertain_classifications} discordant_identities={mismatches}",
                  "targeting=POST_OUTCOME_ALL_MARGIN_IDENTITIES"]
    (HERE / "MARGIN_ESCALATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))
    if mismatches: raise AssertionError("margin escalation discordance")


if __name__ == "__main__":
    main()
