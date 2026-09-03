#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G331 implementations."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

MUTATIONS = (
    (
        "base_gap_normalization",
        "derive_nonsymmetric_eigenline.py",
        "return 4 * (c * c - a * a) / a**4",
        "return 5 * (c * c - a * a) / a**4",
    ),
    (
        "weighted_metric_horizontal_form",
        "derive_nonsymmetric_eigenline.py",
        "zeta = (Jet2(weight_2) / f, Jet2(-weight_1) / f)",
        "zeta = (Jet2(weight_1) / f, Jet2(-weight_1) / f)",
    ),
    (
        "weighted_ricci_projector",
        "derive_nonsymmetric_eigenline.py",
        "matscale(outer(xi, eta), 2 - lam_h)",
        "matscale(outer(xi, eta), 1 - lam_h)",
    ),
    (
        "irrational_orbit_certificate",
        "derive_nonsymmetric_eigenline.py",
        "require(irrational_coefficient != 0, f\"irrational_{n}_nonzero_sqrt2_part\")",
        "require(irrational_coefficient == 0, f\"irrational_{n}_nonzero_sqrt2_part\")",
    ),
    (
        "conformal_ricci_sign",
        "derive_nonsymmetric_eigenline.py",
        "conformal_ricci_13 = -epsilon",
        "conformal_ricci_13 = epsilon",
    ),
    (
        "s3_line_bundle_class",
        "derive_nonsymmetric_eigenline.py",
        "h1_mod2_dimension = 0",
        "h1_mod2_dimension = 1",
    ),
    (
        "constraint_compatibility_promotion",
        "derive_nonsymmetric_eigenline.py",
        "explicit_bump_constraint_compatible = False",
        "explicit_bump_constraint_compatible = True",
    ),
    (
        "common_fibre_period_promotion",
        "derive_nonsymmetric_eigenline.py",
        "common_closed_fibre_period = False",
        "common_closed_fibre_period = True",
    ),
    (
        "independent_weighted_metric",
        "verify_nonsymmetric_eigenline_independent.py",
        "zeta = (w2 / f, -w1 / f)",
        "zeta = (w1 / f, -w1 / f)",
    ),
    (
        "independent_half_gap",
        "verify_nonsymmetric_eigenline_independent.py",
        "require(error < separation / 2, f\"spectral_{index}_strict_half_gap\")",
        "require(error > separation / 2, f\"spectral_{index}_strict_half_gap\")",
    ),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    records = []
    with tempfile.TemporaryDirectory(prefix="g331_catches_") as tmp:
        tmp_path = Path(tmp)
        for name, filename, old, new in MUTATIONS:
            source = (ROOT / filename).read_text(encoding="utf-8")
            if source.count(old) != 1:
                raise AssertionError(f"mutation anchor {name} count != 1")
            target = tmp_path / filename
            target.write_text(source.replace(old, new), encoding="utf-8")
            result = subprocess.run(
                ["python3", "-S", str(target), "--output", str(tmp_path / f"{name}.json")],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                raise AssertionError(f"hostile mutation escaped: {name}")
            records.append({
                "name": name,
                "caught": True,
                "returncode": result.returncode,
                "last_line": (result.stderr or result.stdout).strip().splitlines()[-1],
            })
    payload = {
        "all_caught": True,
        "catch_count": len(records),
        "production_output_read": False,
        "records": records,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G331 hostile PASS: {len(records)}/{len(records)} caught")


if __name__ == "__main__":
    main()
