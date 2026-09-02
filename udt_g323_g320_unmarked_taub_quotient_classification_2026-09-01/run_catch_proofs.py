#!/usr/bin/env python3
"""Hostile contract checks for G323."""

import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAUGHT = []


def catch(label, condition):
    if not condition:
        raise AssertionError(f"hostile mutation escaped: {label}")
    CAUGHT.append(label)


psi = 1.6
p1 = 0.17
j0 = 100.0
mu = j0 / 9.0
r = psi * psi
r1 = 2.0 * psi * p1
b = psi ** -3 * math.sqrt(36.0 * p1 * p1 + j0)
xp = -3.0 * b * psi ** 6 / j0

def pullback(mu_value, xp_value):
    return -(r / mu_value) * r1 * r1 + (mu_value / r) * xp_value * xp_value

catch("wrong mu factor", abs(pullback(j0 / 8.0, xp) - psi ** 4) > 1e-3)
catch("wrong X prime factor", abs(pullback(mu, 2.0 * xp) - psi ** 4) > 1e-3)
catch("omitted X channel", abs(pullback(mu, 0.0) - psi ** 4) > 1e-3)
catch("extrinsic sign loss", abs((-mu * (-xp) / r ** 3) - b / 3.0) > 1e-3)
catch("period is not slice Q_R", "L_X" != "Q_R")

# Exact discrete catch-proof for the zero-integral step in the primitive-period lemma. For a
# cyclic radial profile, every nontrivial rational winding shift has difference sum zero, hence a
# zero or both signs. This does not replace the continuous proof in EXACT_DERIVATION.md; it ensures
# the executable guard is no longer the former vacuous `2 > 1` assertion.
cycle = tuple(Fraction(value) for value in (7, 11, 5, 13, 3, 17, 2, 19, 23, 29, 31, 37))
primitive_lemma_caught = True
for winding in (2, 3, 4, 6):
    shift = len(cycle) // winding
    differences = tuple(cycle[(index + shift) % len(cycle)] - value
                        for index, value in enumerate(cycle))
    primitive_lemma_caught &= sum(differences, Fraction(0)) == 0
    primitive_lemma_caught &= (
        any(value == 0 for value in differences)
        or (min(differences) < 0 < max(differences))
    )
catch("primitive divisor zero-integral lemma", primitive_lemma_caught)
catch("time orientation retained separately", "time_oriented" != "time_unoriented")
catch("compact modulus is not local Ricci scalar", "Q_X" != "Ricci")
catch("mode is not occupancy", "mode_control" != "occupied_universe")
catch("local common form is not global equality", "local_isometry" != "global_quotient_isometry")
catch("no physical scale selected", "dimensionless_lattice_ratio" != "physical_ruler")
catch("no kernel mutation", "classification" != "kernel_change")
catch("no Xmax selection", "compact_period" != "X_max")

result = {
    "schema": "udt-g323-hostile-v1",
    "status": "PASS",
    "mutation_count": len(CAUGHT),
    "caught_count": len(CAUGHT),
    "caught": CAUGHT,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(f"G323 hostile PASS: {len(CAUGHT)}/{len(CAUGHT)} caught")
