#!/usr/bin/env python3
"""Fail-closed package verifier for the intrinsic-ruler/descent audit."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "97d85edb7da351e6a96bb8c55b4e969ea8e3a749"
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"
SOURCE_ID = "340944872577f6c885ac2bd7aeedd05618ea39b0c04d0a774f5d943d4599a440"


def run(command):
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_tsv(name):
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    errors = []
    try:
        prod = run([sys.executable, str(HERE / "derive_intrinsic_ruler_descent.py")])
        independent = run([sys.executable, str(HERE / "verify_intrinsic_ruler_descent_independent.py")])
        require(prod.returncode == 0, prod.stdout)
        require(independent.returncode == 0, independent.stdout)
        p = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
        i = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
        require(p["check_count"] == 23 and all(x["status"] == "PASS" for x in p["checks"]), "production")
        require(i["status"] == "PASS" and i["checks_passed"] == 139 and i["catch_proofs"] == 28, "independent")

        manifest = read_tsv("SOURCE_MANIFEST.tsv")
        require(len(manifest) == 23 and len({row["path"] for row in manifest}) == 23, "sources")
        identity = hashlib.sha256("\n".join(row["path"]+"\t"+row["blob"] for row in manifest).encode()).hexdigest()
        require(identity == SOURCE_ID, "source identity")
        for row in manifest:
            data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
            blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
            require(blob == row["blob"] and hashlib.sha256(data).hexdigest() == row["sha256"] and len(data) == int(row["bytes"]), "source "+row["path"])

        branches = {row["id"]: row for row in read_tsv("BRANCH_COMPATIBILITY_ATLAS.tsv")}
        status = {row["id"]: row for row in read_tsv("STATUS_LEDGER.tsv")}
        refinements = {row["claim_id"]: row for row in read_tsv("PARENT_STATUS_REFINEMENT.tsv")}
        require(set(refinements) == {"N22", "T18"}, "parent refinements")
        require(branches["B03"]["full_descent"].startswith("FAIL_VPHI"), "old witness descent")
        require(branches["B05"]["full_descent"] == "PASS", "anisotropic descent")
        require(branches["B10"]["classification"] == "SMALLEST_REMAINING_SELECTOR_SEAM", "next seam")
        require(status["S14"]["status"] == "INCOMPATIBLE_EXACT", "rank/descent incompatibility")
        require(status["S16"]["status"] == "OPEN_NOT_RULED_OUT", "no global selector no-go")
        require(status["S18"]["status"] == "POSIT_UNCHANGED", "carrier")
        require(status["S19"]["status"] == "OPEN_UNCHANGED", "physics")

        catches = read_tsv("CATCH_PROOFS.tsv")
        require(len(catches) == 28 and [r["id"] for r in catches] == [f"F{x:02d}" for x in range(1, 29)], "catch IDs")
        require(all(row["status"] == "PASS" and row["expected"] == row["actual"] for row in catches), "catch results")

        review = (HERE / "ADVERSARIAL_REVIEW.md").read_text()
        require("Verdict: `PASS`" in review or "Verdict: `VERIFIED-WITH-CAVEATS`" in review, "review verdict")
        require("fresh" in review.lower(), "review context")

        premises = run([sys.executable, "verify_current_scientific_premises.py"])
        require(premises.returncode == 0, premises.stdout)
        lines = run(["git", "status", "--short"]).stdout.splitlines()
        unrelated = [line for line in lines if not line[3:].startswith(HERE.name + "/")]
        payload = ("\n".join(unrelated) + ("\n" if unrelated else "")).encode()
        require(len(unrelated) == DIRTY_COUNT and hashlib.sha256(payload).hexdigest() == DIRTY_SHA, "dirty identity")

        text = (HERE / "AUDIT_REPORT.md").read_text() + (HERE / "EXACT_DERIVATION.md").read_text()
        for disclosure in ["V(phi)=0", "V(h)+kappa(hR-Rh)=0", "E1=exp(-phi)(V-alpha/c_E K)",
                           "C3", "second continuous Killing", "not a proof that no other"]:
            require(disclosure in text, "missing disclosure "+disclosure)
    except Exception as exc:
        errors.append(str(exc))

    result = {
        "schema": "udt-intrinsic-ruler-full-screen-descent-verification-1.0",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "production_checks": 23,
        "independent_checks": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text()).get("checks_passed", 0),
        "catch_proofs": 28,
        "source_count": 23,
        "source_identity_sha256": SOURCE_ID,
        "dirty_paths": DIRTY_COUNT,
        "dirty_status_sha256": DIRTY_SHA,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
