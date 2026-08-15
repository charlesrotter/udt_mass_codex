#!/usr/bin/env python3
"""Prove selected consistency guards fail under targeted record mutations."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile

from verify_package import build_checks


ROOT = Path(__file__).resolve().parent


def copy_package(destination: Path) -> None:
    for path in ROOT.iterdir():
        if path.is_file():
            shutil.copy2(path, destination / path.name)


def main() -> None:
    catches: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="udt_null_carrier_catches_") as tmp:
        work = Path(tmp)
        copy_package(work)

        primary_path = work / "DERIVATION_RESULT.json"
        primary = json.loads(primary_path.read_text(encoding="utf-8"))
        primary["physical_eta_selected"] = True
        primary_path.write_text(json.dumps(primary, indent=2) + "\n", encoding="utf-8")
        catches["physical_eta_promotion"] = not build_checks(work)["physical_eta_open"]

    with tempfile.TemporaryDirectory(prefix="udt_null_carrier_catches_") as tmp:
        work = Path(tmp)
        copy_package(work)
        atlas = work / "CANDIDATE_MEASURE_ATLAS.tsv"
        atlas.write_text(
            atlas.read_text(encoding="utf-8").replace(
                "VALID_QUERY_LABEL_BOOKKEEPING__TAUTOLOGICAL_PUSHFORWARD",
                "PHYSICAL_CARRIER_DERIVED",
                1,
            ),
            encoding="utf-8",
        )
        catches["label_current_type_promotion"] = not build_checks(work)["label_current_typed_bookkeeping"]

    with tempfile.TemporaryDirectory(prefix="udt_null_carrier_catches_") as tmp:
        work = Path(tmp)
        copy_package(work)
        exact = work / "EXACT_DERIVATION.md"
        exact.write_text(
            exact.read_text(encoding="utf-8").replace(
                "closure itself is already encoded in query typing",
                "closure is new metric dynamics",
                1,
            ),
            encoding="utf-8",
        )
        catches["metric_overcredit"] = not build_checks(work)["metric_not_overcredited"]

    with tempfile.TemporaryDirectory(prefix="udt_null_carrier_catches_") as tmp:
        work = Path(tmp)
        copy_package(work)
        (work / "PREREGISTRATION.md").unlink()
        catches["missing_preregistration"] = not build_checks(work)["exists:PREREGISTRATION.md"]

    result = {"catches": catches, "all_pass": all(catches.values())}
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
