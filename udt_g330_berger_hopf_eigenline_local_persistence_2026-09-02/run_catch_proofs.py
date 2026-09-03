#!/usr/bin/env python3
"""Direct hostile mutations for the G330 exact implementations."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


MUTATIONS = (
    (
        "structure_normalization",
        "derive_berger_hopf.py",
        'A = LP({(-2, 1): 2})',
        'A = LP({(-2, 1): 1})',
    ),
    (
        "ricci_closed_form",
        "derive_berger_hopf.py",
        'lam_h = LP({(-2, 0): 4, (-4, 2): -2})',
        'lam_h = LP({(-2, 0): 4, (-4, 2): -3})',
    ),
    (
        "g313_witness",
        "derive_berger_hopf.py",
        'gap.evaluate(1, Fraction(3, 2)) == 5',
        'gap.evaluate(1, Fraction(3, 2)) == 6',
    ),
    (
        "hopf_normalization",
        "derive_berger_hopf.py",
        'normalized_hopf = Fraction(-2 * 2, 4)',
        'normalized_hopf = Fraction(-2 * 1, 4)',
    ),
    (
        "round_degeneracy",
        "derive_berger_hopf.py",
        'gap.evaluate(1, 1) == 0',
        'gap.evaluate(1, 1) != 0',
    ),
    (
        "frame_covariance",
        "verify_berger_hopf_independent.py",
        'reconstructed == mm(mm(rotation, projector), tr(rotation))',
        'reconstructed == projector',
    ),
    (
        "line_sign",
        "verify_berger_hopf_independent.py",
        '(-fibre_period_over_pi) * (-base_flux_over_pi) / 4 == -1',
        '(-fibre_period_over_pi) * (-base_flux_over_pi) / 4 == 1',
    ),
    (
        "local_gap",
        "verify_berger_hopf_independent.py",
        '>= 3 * initial / 4',
        '> initial',
    ),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    records = []
    with tempfile.TemporaryDirectory(prefix="g330_catches_") as tmp:
        tmp_path = Path(tmp)
        for name, filename, old, new in MUTATIONS:
            source = (ROOT / filename).read_text(encoding="utf-8")
            if source.count(old) != 1:
                raise AssertionError(f"mutation anchor {name} count != 1")
            mutated = source.replace(old, new)
            target = tmp_path / filename
            target.write_text(mutated, encoding="utf-8")
            result = subprocess.run(
                ["python3", "-S", str(target), "--output", str(tmp_path / f"{name}.json")],
                text=True,
                capture_output=True,
                check=False,
            )
            caught = result.returncode != 0
            if not caught:
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
    print(f"G330 hostile PASS: {len(records)}/{len(records)} caught")


if __name__ == "__main__":
    main()
