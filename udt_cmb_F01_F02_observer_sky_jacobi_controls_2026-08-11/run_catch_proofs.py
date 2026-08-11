#!/usr/bin/env python3
"""Exercise all preregistered fail-closed artifact mutations."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).resolve().parent
VERIFY = SOURCE / "verify_package.py"


def mutate_tsv(path: Path, field: str, value: str, row_index: int = 0) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
        names = list(rows[0])
    rows[row_index][field] = value
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mutate_json(path: Path, callback) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    callback(data)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    mutations = []

    def j01(p): mutate_tsv(p / "SOURCE_MANIFEST.tsv", "sha256", "0" * 64)
    mutations.append(("J01_source_hash", j01))

    def j02(p): mutate_tsv(p / "LOCAL_CONTROL_ATLAS.tsv", "query_status", "DIFFERENT_QUERY", 1)
    mutations.append(("J02_query_mismatch", j02))

    def j03(p): mutate_json(p / "DERIVATION_RESULT.json", lambda d: d["F02_tidal_matrix_equator"].__setitem__(1, ["0", "0"]))
    mutations.append(("J03_zero_F02", j03))

    def j04(p): mutate_json(p / "DERIVATION_RESULT.json", lambda d: d["F01_induced_limit"].__setitem__(0, ["1", "0"]))
    mutations.append(("J04_mutate_round_limit", j04))

    def j05(p): mutate_json(p / "DERIVATION_RESULT.json", lambda d: d.__setitem__("generator_norm", "1"))
    mutations.append(("J05_nonnull_query", j05))

    def j06(p): mutate_json(p / "DERIVATION_RESULT.json", lambda d: d["F02_tidal_matrix_equator"][0].__setitem__(1, "1"))
    mutations.append(("J06_nonsymmetric_screen", j06))

    def j07(p): mutate_json(p / "DERIVATION_RESULT.json", lambda d: d.__setitem__("maximum_conclusion", "finite map derived"))
    mutations.append(("J07_scope_promotion", j07))

    def j08(p): mutate_tsv(p / "PROJECTION_FREEDOM_LEDGER.tsv", "status_after_control", "DERIVED", 4)
    mutations.append(("J08_infer_TT_power", j08))

    def j09(p): mutate_tsv(p / "PREMISE_LEDGER.tsv", "not_owned", "NONE", 12)
    mutations.append(("J09_local_c_eff", j09))

    def j10(p): mutate_tsv(p / "LOCAL_CONTROL_ATLAS.tsv", "physical_status", "SELECTED_PHYSICAL", 1)
    mutations.append(("J10_select_F02", j10))

    def j11(p): mutate_json(p / "INDEPENDENT_VERIFICATION_RESULT.json", lambda d: d.__setitem__("method", "production curvature imported"))
    mutations.append(("J11_false_independence", j11))

    def j12(p):
        target = p / "SPECIAL_SUBLOCUS_ATLAS.tsv"
        lines = target.read_text(encoding="utf-8").splitlines()
        target.write_text("\n".join(line for line in lines if not line.startswith("NEGATIVE_CONTROL\t")) + "\n", encoding="utf-8")
    mutations.append(("J12_drop_sublocus", j12))

    caught = {}
    diagnostics = {}
    with tempfile.TemporaryDirectory(prefix="udt-jacobi-catches-") as temp:
        temp_root = Path(temp)
        for name, mutation in mutations:
            package = temp_root / name
            shutil.copytree(SOURCE, package)
            mutation(package)
            run = subprocess.run(
                ["python3", str(VERIFY), "--package", str(package), "--source-root", str(ROOT)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            caught[name] = run.returncode != 0
            if run.returncode == 0:
                diagnostics[name] = "mutation was not rejected"

    result = {"caught": caught, "diagnostics": diagnostics, "passed": sum(caught.values()), "total": len(caught)}
    (SOURCE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(caught.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
