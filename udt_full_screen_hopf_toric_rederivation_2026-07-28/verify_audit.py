#!/usr/bin/env python3
"""Fail-closed package verifier for the full-screen N22/T18 rederivation."""

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
BASE = "ace0699fc145c935c16cd283f393c18e654d5b74"
DIRTY_COUNT = 57
DIRTY_SHA = "bf85b6db00083cfa0d19e4ba9cc09766423cc2d5e224954f12ceda74aeab9c96"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_tsv(name: str):
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    errors: list[str] = []
    try:
        production_run = run([sys.executable, str(HERE / "derive_full_screen_hopf_toric.py")])
        independent_run = run([sys.executable, str(HERE / "verify_full_screen_hopf_toric_independent.py")])
        require(production_run.returncode == 0, production_run.stdout)
        require(independent_run.returncode == 0, independent_run.stdout)

        production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
        independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
        require(production["check_count"] == 34, "production check count")
        require(all(row["status"] == "PASS" for row in production["checks"]), "production checks")
        require(independent["status"] == "PASS" and independent["catch_proofs"] == 32, "independent result")

        manifest = read_tsv("SOURCE_MANIFEST.tsv")
        require(len(manifest) == 38 and len({row["path"] for row in manifest}) == 38, "source count")
        source_identity = hashlib.sha256(
            "\n".join(row["path"] + "\t" + row["blob"] for row in manifest).encode()
        ).hexdigest()
        require(source_identity == "5c9b9d0e6ca284513ab85afacda01c948f087f979fee5f5362fd1300961ba11f",
                "source identity")
        for row in manifest:
            blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
            data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
            require(blob == row["blob"], "blob " + row["path"])
            require(hashlib.sha256(data).hexdigest() == row["sha256"], "sha " + row["path"])
            require(len(data) == int(row["bytes"]), "size " + row["path"])

        routes = {row["id"]: row for row in read_tsv("ROUTE_CLASSIFICATION.tsv")}
        regrades = {row["claim_id"]: row for row in read_tsv("N22_T18_REGRADING.tsv")}
        status = {row["id"]: row for row in read_tsv("STATUS_LEDGER.tsv")}
        require(set(regrades) == {"N22", "T18"}, "exact two-row regrade")
        require(routes["N22"]["classification"] == "SUPERSEDED_OR_REFINED", "N22 route")
        require(routes["T18"]["classification"] == "SUPERSEDED_OR_REFINED", "T18 route")
        require(regrades["N22"]["full_screen_status"].startswith("STRONGER_CONDITIONAL"), "N22 status")
        require(regrades["T18"]["full_screen_status"].endswith("NO_SELECTION"), "T18 status")
        require(status["S05"]["status"] == "REFUTED_EXACT", "contact periodicity countermodel")
        require(status["S16"]["status"] == "ALLOWED_EXACT_COUNTERFAMILY", "lens counterfamily")
        require(status["S19"]["status"] == "BLOCKED_TYPE_GAP", "carrier boundary")
        require(status["S23"]["status"] == "OPEN_UNCHANGED", "physics boundary")

        review = (HERE / "ADVERSARIAL_REVIEW.md").read_text()
        require("Verdict: `PASS`" in review or "Verdict: `VERIFIED-WITH-CAVEATS`" in review,
                "fresh adversarial verdict")
        require("fresh zero-context" in review.lower(), "fresh-review provenance")

        catches = read_tsv("CATCH_PROOFS.tsv")
        require(len(catches) == 32 and all(row["status"] == "PASS" for row in catches), "catch proofs")
        require([row["id"] for row in catches] == [f"F{i:02d}" for i in range(1, 33)], "catch IDs")

        current = run([sys.executable, "verify_current_scientific_premises.py"])
        require(current.returncode == 0, current.stdout)

        lines = run(["git", "status", "--short"]).stdout.splitlines()
        unrelated = [line for line in lines if not line[3:].startswith(HERE.name + "/")
                     and line[3:] not in {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}]
        payload = ("\n".join(unrelated) + ("\n" if unrelated else "")).encode()
        require(len(unrelated) == DIRTY_COUNT, "dirty count")
        require(hashlib.sha256(payload).hexdigest() == DIRTY_SHA, "dirty metadata")

        report = (HERE / "AUDIT_REPORT.md").read_text()
        exact = (HERE / "EXACT_DERIVATION.md").read_text()
        for required in [
            "exp(-phi) theta1=sigma3",
            "strong local CSN",
            "3-2sqrt(2)",
            "L(p,1)",
            "carrier emergence",
            "fiber-equivariant",
        ]:
            require(required in report + exact, "missing disclosure " + required)
    except Exception as exc:  # collect one exact failure in a machine-readable record
        errors.append(str(exc))

    result = {
        "schema": "udt-full-screen-hopf-toric-verification-1.0",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "production_checks": 34,
        "independent_checks": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text()).get("checks_passed", 0)
        if (HERE / "INDEPENDENT_RESULT.json").exists() else 0,
        "catch_proofs": 32,
        "source_count": 38,
        "source_identity_sha256": "5c9b9d0e6ca284513ab85afacda01c948f087f979fee5f5362fd1300961ba11f",
        "regraded_claims": ["N22", "T18"],
        "dirty_paths": DIRTY_COUNT,
        "dirty_status_sha256": DIRTY_SHA,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
