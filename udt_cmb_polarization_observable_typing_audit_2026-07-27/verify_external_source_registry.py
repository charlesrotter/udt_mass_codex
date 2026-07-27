#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse


HERE = Path(__file__).resolve().parent
ALLOWED_HOSTS = {"arxiv.org", "lambda.gsfc.nasa.gov"}
EXPECTED = {
    "X01": ("https://arxiv.org/abs/1907.12875", "2020_AA_641_A5"),
    "X02": ("https://arxiv.org/abs/1807.06208", "2020_AA_641_A4"),
    "X03": ("https://lambda.gsfc.nasa.gov/product/planck/curr/planck_prod_irsa.html", "PR4_NPIPE_current_2026-07-27"),
    "X04": ("https://arxiv.org/abs/2503.14452", "2025_DR6"),
    "X05": ("https://arxiv.org/abs/2506.06274", "2025_DR6_foregrounds"),
    "X06": ("https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/index.html", "DR6.02_current_2026-07-27"),
    "X07": ("https://arxiv.org/abs/astro-ph/9609170", "PhysRevD_55_1830_1997"),
    "X08": ("https://arxiv.org/abs/1906.02552", "2020_AA_641_A7"),
    "X09": ("https://arxiv.org/abs/2509.13654", "arXiv_v2_2026-04-14"),
    "X10": ("https://arxiv.org/abs/2110.00483", "PhysRevLett_127_151301_2021"),
}


def main() -> int:
    with (HERE / "EXTERNAL_SOURCE_REGISTRY.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 10
    assert [row["external_id"] for row in rows] == [f"X{i:02d}" for i in range(1, 11)]
    assert {row["source_class"] for row in rows} <= {"S11", "S12", "S13", "S14"}
    assert all(urlparse(row["url"]).scheme == "https" for row in rows)
    assert all(urlparse(row["url"]).hostname in ALLOWED_HOSTS for row in rows)
    assert all(row["admissible_use"] and row["prohibited_promotion"] for row in rows)
    assert {row["external_id"]: (row["url"], row["version_or_date"]) for row in rows} == EXPECTED
    print(json.dumps({"result": "PASS", "primary_or_official_sources": 10}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
