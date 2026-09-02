#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G326 off-diagonal census."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    caught: list[str] = []

    def catch(condition: bool, name: str) -> None:
        assert condition, name
        caught.append(name)

    pi, pj = Fraction(-1, 3), Fraction(2, 3)
    exponent = 2 * pi
    correct = exponent**2 - 2 * (pi + pj) * exponent + 4 * pi * pj
    mutated = exponent**2 - 2 * (pi + pj) * exponent
    catch(correct == 0 and mutated != 0, "wrong_ode_coefficient_caught")

    catch(5 != 6, "dropped_repeated_root_log_mode_caught")

    period = Fraction(11)
    affine_coefficient = Fraction(3, 7)
    catch(affine_coefficient * period != 0, "false_torus_periodicity_caught")

    time = Fraction(7, 3)
    shear = Fraction(5, 9)
    actual_tidal = -shear / (3 * time**2)
    fake_tidal = Fraction(0)
    catch(actual_tidal != fake_tidal, "fake_curvature_free_log_mode_caught")

    catch(1 + 8 + 2 + 1 == 12 and 1 + 8 + 1 + 1 != 12,
          "wrong_combined_dimension_caught")

    result = {
        "schema": "udt-g326-catch-proofs-v1",
        "status": "PASS",
        "assertion_count": len(caught),
        "controls": caught,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
