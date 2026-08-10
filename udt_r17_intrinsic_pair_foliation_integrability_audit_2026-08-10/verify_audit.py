#!/usr/bin/env python3
"""Fail-closed package verifier and exercised mutation catches."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = "GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def source_rows(rows: list[dict[str, str]]) -> bool:
    require(len(rows) == 15, "source count")
    require(len({r["source_id"] for r in rows}) == 15, "source ids")
    require(len({r["path"] for r in rows}) == 15, "source paths")
    for row in rows:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(hashlib.sha256(data).hexdigest() == row["sha256"], "source sha")
        require(str(len(data)) == row["size"], "source size")
    return True


def scientific_state(state: dict) -> bool:
    require(state["landing"] == LANDING, "landing")
    require(state["leaf_metric_determinant"] == "-1", "leaf determinant")
    require(state["terminal_ratio"] == "u**4", "terminal ratio")
    require(state["terminal_depth"] == "log(u)", "terminal depth")
    require(all(state["checks"].values()), "production checks")
    require(not any(state["scope_guards"].values()), "scope promotion")
    return True


def independent_state(state: dict) -> bool:
    require(state["mode"] == "independent_standard_library_exact_rationals", "independent mode")
    require(state["imports_production_controller"] is False, "false independence")
    require(state["witness_count"] == 6, "witness count")
    require(state["passed_checks"] == 36, "independent checks")
    require(all(all(w["checks"].values()) for w in state["witnesses"]), "witness failure")
    return True


def rejected(callable_) -> bool:
    try:
        callable_()
    except (ValueError, KeyError):
        return True
    return False


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = list(csv.DictReader(stream, delimiter="\t"))
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")
    )
    source_rows(manifest)
    scientific_state(production)
    independent_state(independent)

    catches: list[tuple[str, str, bool]] = []

    def add(cid: str, target: str, mutant) -> None:
        catches.append((cid, target, rejected(mutant)))

    add("C01", "missing source", lambda: source_rows(manifest[:-1]))
    add("C02", "duplicate source", lambda: source_rows(manifest[:-1] + [manifest[0]]))

    def mutate_prod(key, value):
        altered = json.loads(json.dumps(production))
        altered[key] = value
        return lambda: scientific_state(altered)

    add("C03", "wrong determinant", mutate_prod("leaf_metric_determinant", "0"))
    add("C04", "wrong terminal ratio", mutate_prod("terminal_ratio", "u**2"))
    add("C05", "wrong terminal depth", mutate_prod("terminal_depth", "0"))
    add("C06", "wrong landing", mutate_prod("landing", "COMPLETE_PHYSICAL_PAIR_SURFACE_FAMILY_DERIVED"))

    def promote(name):
        altered = json.loads(json.dumps(production))
        altered["scope_guards"][name] = True
        return lambda: scientific_state(altered)

    add("C07", "select one leaf", promote("one_leaf_selected"))
    add("C08", "select one winding", promote("one_winding_selected"))
    add("C09", "promote cross-leaf map", promote("cross_leaf_pair_map_derived"))
    add("C10", "erase path-labelled screen carry", promote("screen_transport_path_independent"))
    add("C11", "promote physical complete arrow", promote("physical_complete_arrow_derived"))
    add("C12", "select lambda", promote("lambda_selected"))

    altered_independent = json.loads(json.dumps(independent))
    altered_independent["imports_production_controller"] = True
    add("C13", "false independent verifier", lambda: independent_state(altered_independent))

    if not all(item[2] for item in catches):
        raise SystemExit(f"FAIL catches: {catches}")

    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "mutant", "expected", "observed"])
        for cid, target, passed in catches:
            writer.writerow([cid, target, "REJECT", "REJECT" if passed else "ACCEPT"])

    output = {
        "status": "PASS",
        "source_manifest_rows": 15,
        "production_checks": sum(production["checks"].values()),
        "independent_checks": independent["passed_checks"],
        "catch_proofs": len(catches),
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: 15 sources; 10 production; 36 independent; 13/13 catches")


if __name__ == "__main__":
    main()
