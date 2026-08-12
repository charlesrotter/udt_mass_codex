#!/usr/bin/env python3
"""Verify the complete-pair observed-pattern shape-test package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DATA = Path("/media/udt-admin/ScratchDisk/Data/BAO/CobayaSampler_bao_data/desi_bao_dr2")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    result = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())

    mean = DATA / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
    cov = DATA / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
    assert sha256(mean) == result["mean_sha256"]
    assert sha256(cov) == result["cov_sha256"]
    assert result["status"] == independent["status"] == catches["status"] == "PASS"
    assert result["preregistration_commit"] == "efdecd35"
    assert result["symbolic"]["orientation_preserving_reparameterization_invariant"] is True
    assert result["symbolic"]["missing_L_pair_reparameterization_invariant"] is False
    assert result["symbolic"]["general_scalar_exact"] is True
    assert result["symbolic"]["missing_exp_phi_fails_scalar_reduction"] is True
    assert result["symbolic"]["c0_exact"] is True

    expected = {"C0": 114.72114835807093, "C1": 31.274892627884704}
    for name, target in expected.items():
        observed = result["totals"][name]
        assert abs(observed["chi2"] - target) < 1e-12
        assert observed["constraints"] == 6
        assert observed["classification"] == "INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY"
        assert float(independent["total_abs_deltas"][name]) < 1e-12
    assert result["delta_chi2_C1_minus_C0"] < -83.0
    assert result["direct_profile_verification"]["maximum_amplitude_abs_delta"] < 1e-6
    assert result["direct_profile_verification"]["maximum_chi2_abs_delta"] < 1e-10
    assert float(independent["maximum_row_abs_delta"]) < 1e-12
    assert catches["caught"] == catches["total"] == 9
    assert all(catches["checks"].values())

    with (ROOT / "SHAPE_RESIDUAL_ATLAS.tsv").open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 12
    assert {row["control"] for row in rows} == {"C0", "C1"}
    assert sorted({float(row["z"]) for row in rows}) == [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]

    prereg = "efdecd35"
    assert subprocess.check_output(
        ["git", "cat-file", "-t", prereg], cwd=REPO, text=True
    ).strip() == "commit"
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", prereg, "origin/grok"],
        cwd=REPO,
        check=True,
    )

    exact = (ROOT / "EXACT_DERIVATION.md").read_text()
    audit = (ROOT / "AUDIT_REPORT.md").read_text()
    evidence = (ROOT / "EVIDENCE_GATES.md").read_text()
    assert "= d_A (dz/dlambda) / L_pair" in exact
    assert "COMPLETE_PAIR_SHAPE_OPERATOR_DERIVED" in audit
    assert "complete pair history" in audit
    assert "LEAD__INTERNALLY_VERIFIED_WITH_CAVEATS" in evidence

    print("complete-pair pattern-shape package: PASS (operator, 2 controls, 6 bins, 9 catches)")


if __name__ == "__main__":
    main()
