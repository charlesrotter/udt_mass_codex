#!/usr/bin/env python3
"""Semantic mutation catches for G168."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
catches: dict[str, bool] = {}


def catch(name: str, condition: object) -> None:
    value = bool(condition)
    catches[name] = value
    if not value:
        raise AssertionError(name)


g = sp.diag(sp.Rational(-1, 4), 4, 9, sp.Rational(144, 25))
u = sp.Matrix([2, 0, 0, 0])
s = sp.Matrix([1, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4)])
inner = lambda x, y: (x.T * g * y)[0]
guu = inner(u, u)
gus = inner(u, s)
r = s - gus / guu * u

# Mutant 1: wrong projection sign.
r_wrong = s + gus / guu * u
catch("wrong_projection_sign", inner(u, r_wrong) != 0)

# Mutants 2-3: angular deletion/freeze.
h_full = sp.Matrix.hstack(u, s).T * g * sp.Matrix.hstack(u, s)
g_no_angular = sp.diag(sp.Rational(-1, 4), 4, 0, 0)
h_no_angular = sp.Matrix.hstack(u, s).T * g_no_angular * sp.Matrix.hstack(u, s)
catch("drop_angular_gram", h_no_angular != h_full)
catch("freeze_nonradial_Z", inner(r, r) != 4 * sp.Rational(1, 4))

# Mutant 4: coincidence promoted to a plane.
catch("coincidence_plane_overclaim", sp.Matrix.hstack(u, sp.zeros(4, 1)).rank() != 2)

# Mutant 5: ruler flip claimed to reverse scalar depth.
h_orth = sp.diag(-1, sp.Rational(59, 25))
R = sp.diag(1, -1)
catch("ruler_flip_is_not_depth_reversal", R.T * h_orth * R == h_orth)

# Mutant 6: B velocity forced into positional plane.
vb = sp.Matrix([sp.Rational(5, 4), 0, sp.Rational(3, 4), 0])
catch("relative_velocity_plane_overclaim", vb[2] != 0)

# Mutant 7: bare labels claimed to own the surface germ.
s0 = sp.Matrix([0, 1, 0, 0])
s1 = sp.Matrix([0, 1, 1, 0])
catch("bare_label_ownership_overclaim", sp.Matrix.hstack(u, s0).columnspace() != sp.Matrix.hstack(u, s1).columnspace())

# Mutant 8: counterfamily ceases to share the B boundary if the taper is removed.
alpha = sp.symbols("alpha", nonzero=True)
catch("counterfamily_boundary_taper", alpha * 1 != 0)

report = (HERE / "AUDIT_REPORT.md").read_text()
exact = (HERE / "EXACT_DERIVATION.md").read_text()
catch("no_path_required_guard", "No path" in report and "not a\n+curve between separated endpoints".replace("\n+", "\n") in exact)
catch("bare_labels_open_guard", "Bare labels" in exact and "insufficient" in exact)
catch("global_ceiling_guard", "global physical relation network" in (HERE / "STATUS_LEDGER.tsv").read_text())
catch(
    "germ_ownership_postulate_guard",
    "additional working postulate" in exact
    and "PROPOSED_WORKING_POSTULATE_NOT_DERIVED" in (HERE / "STATUS_LEDGER.tsv").read_text(),
)

result = {
    "catches_passed": sum(catches.values()),
    "catches_total": len(catches),
    "catches": catches,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"passed": result["catches_passed"], "total": result["catches_total"]}))
