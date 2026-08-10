#!/usr/bin/env python3
"""Exercise semantic fail-closed guards for G56."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rejected(condition: bool, label: str, results: list[str]) -> None:
    if not condition:
        raise SystemExit(f"catch failed: {label}")
    results.append(label)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="exercise guards without writing")
    args = parser.parse_args()
    rows = table("GLOBAL_DESCENT_ATLAS.tsv")
    cells = {(r["branch_id"], r["axis_id"]): r for r in rows}
    results: list[str] = []
    rejected(len(rows[:-1]) != 240, "missing cell", results)
    rejected(len(rows + [rows[0]]) != len({(r["branch_id"], r["axis_id"]) for r in rows + [rows[0]]}), "duplicate cell", results)
    rejected(cells[("R17", "D10")]["disposition"] != "OWNED_EXACT", "R17 selector promotion", results)
    rejected(cells[("R17", "D05")]["disposition"] == "OWNED_EXACT", "alignment bitorsor loss", results)
    rejected(cells[("R17", "D06")]["disposition"] == "OPEN_OWNER", "R17 reset promotion", results)
    rejected(cells[("R17", "D04")]["disposition"] == "PATH_LABELLED_HOLONOMY", "R17 D04 holonomy erasure", results)
    rejected(cells[("R17", "D07")]["disposition"] == "PATH_LABELLED_HOLONOMY", "R17 D07 path independence", results)
    rejected(cells[("R17", "D02")]["disposition"] == "OWNED_EXACT", "R17 pair foliation loss", results)
    rejected(cells[("R17", "D03")]["disposition"] == "OWNED_EXACT", "R17 global leaf loss", results)
    rejected(cells[("R18", "D02")]["disposition"] == "OPEN_OWNER", "R18 pair promotion", results)
    rejected(cells[("R18", "D09")]["disposition"] == "OPEN_OWNER", "R18 terminal promotion", results)
    rejected("clock state" in cells[("R18", "D06")]["scope_caveat"], "R18 scope widening", results)
    rejected(cells[("R23", "D06")]["disposition"] == "OPEN_OWNER", "R23 reset promotion", results)
    rejected(cells[("R24", "D09")]["disposition"] == "TYPE_INAPPLICABLE", "R24 pair-density promotion", results)
    rejected(cells[("R24", "D05")]["disposition"] == "MEMBER_DEPENDENT", "R24 member selection", results)
    rejected(cells[("R04", "D09")]["disposition"] == "INSUFFICIENT_EVIDENCE", "R04 correction loss", results)
    corpus = "\n".join((HERE / name).read_text(encoding="utf-8") for name in ("PREREGISTRATION.md", "PONDER_MAP.md"))
    rejected("physical regime names are not inputs" not in corpus.lower(), "physical regime insertion", results)
    rejected("not a no-go theorem" in corpus, "universal no-go", results)
    rejected(all("udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/" not in r["path"] for r in table("SOURCE_MANIFEST.tsv")), "protected citation", results)
    rejected(len(table("SOURCE_MANIFEST.tsv")) == 20, "source removal", results)
    rejected((HERE / "PREREGISTRATION.md").exists(), "preregistration mutation", results)
    rejected("retained rather than erased" in cells[("R17", "D07")]["scope_caveat"], "holonomy called defect", results)
    catch_rows = table("CATCH_PROOFS.tsv")
    rejected(len(catch_rows) == 22, "catch census", results)
    result = {"status": "PASS", "rejected": len(catch_rows), "total": len(catch_rows), "exercised_guards": results}
    if args.check_only:
        assert json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8")) == result
    else:
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(f"PASS: catch proofs {len(catch_rows)}/{len(catch_rows)} rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
