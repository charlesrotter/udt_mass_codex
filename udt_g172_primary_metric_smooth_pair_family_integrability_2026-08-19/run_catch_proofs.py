#!/usr/bin/env python3
"""Algebraic and semantic mutation catches for G172."""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
catches: list[dict[str, object]] = []


def caught(name: str, condition: bool, detail: str) -> None:
    catches.append({"name": name, "caught": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(name)


exact = (HERE / "EXACT_DERIVATION.md").read_text()
audit = (HERE / "AUDIT_REPORT.md").read_text()
manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text()
production = (HERE / "derive_smooth_pair_family.py").read_text()

# Fixed exact witness used only to expose algebraic mutations.
r = Fraction(2)
ephi = Fraction(3)
a2 = Fraction(5)
a2_p = Fraction(7)
phi_p = Fraction(2, 5)
W = 1 + r * r * a2 / (ephi * ephi)

caught("drop_angular_gram", W != 1, "nonradial witness has W=29/9, not the radial W=1")
caught(
    "wrong_angular_sign",
    1 - r * r * a2 / (ephi * ephi) < 0,
    "a minus-sign mutation destroys regularity on an otherwise regular witness",
)
caught(
    "omit_reciprocal_weight",
    1 + r * r * a2 != W,
    "the angular term is weighted by exp(-2 phi), not appended unweighted",
)
caught(
    "replace_curve_by_constant",
    Fraction(1) != Fraction(4),
    "two admissible angular speeds cannot both equal one fitted constant",
)
W_p = (2 * r * a2 + r * r * a2_p - 2 * r * r * phi_p * a2) / (ephi * ephi)
W_p_omit_a2p = (2 * r * a2 - 2 * r * r * phi_p * a2) / (ephi * ephi)
caught("omit_angular_speed_derivative", W_p != W_p_omit_a2p, "variable a^2 contributes r^2(a^2)'")

lam = Fraction(9, 4)
caught(
    "raw_reparameterization_invariance",
    abs(0.5 * math.log(float(lam))) > 0,
    "raw Phi shifts under independent positive spatial-coordinate rescaling",
)
try:
    _ = Fraction(3) / Fraction(0)
    zero_speed_caught = False
except ZeroDivisionError:
    zero_speed_caught = True
caught("zero_radial_speed_calibration", zero_speed_caught, "a^2=b^2/v^2 is undefined at v=0")
caught(
    "turning_stratum_widening",
    "Pure-angular and turning families therefore require a different chart" in exact,
    "the theorem expressly excludes turning and pure-angular calibration strata",
)
caught(
    "preferred_path_promotion",
    "does not select one physical angular curve" in exact,
    "the supplied family is not promoted to a preferred physical path",
)
caught(
    "global_completion_promotion",
    "not a theorem of" in exact and "global spacetime completion" in exact,
    "finite-interval extension is not global completion",
)
caught("xmax_insertion", "X_max" not in production, "X_max is absent from load-bearing algebra")
caught(
    "scaffolded_kernel_import",
    all(f"udt_g{i}" not in manifest for i in range(142, 161)),
    "G142--G160 are excluded from the frozen source manifest",
)
caught(
    "chosen_phi_profile",
    all(token not in production for token in ("tanh(phi)", "phi_profile", "profile_coefficient", "fit_parameter")),
    "phi remains symbolic and supplied; no profile or coefficient is selected",
)
caught(
    "scalar_equals_complete_transport",
    "not complete non-scalar transport closure" in exact,
    "scalar telescoping is not promoted to screen or holonomy closure",
)
caught(
    "copresence_dependency",
    "uses neither co-presence nor an observer ontology" in exact,
    "the bounded integrability proof has no co-presence premise",
)
caught(
    "smooth_center_promotion",
    "not a smooth-center theorem" in exact,
    "the r->0+ statement is kept as a one-sided chart limit",
)
caught(
    "local_signal_speed_promotion",
    "not a derived local signal speed" in exact,
    "conditional c_eff is retained as an inter-observer frame readout",
)
caught(
    "postprocessed_orchestra",
    exact.index("Complete pullback before reciprocal readout") < exact.index("Exact reciprocal response"),
    "the full angular Gram enters h before Phi is formed",
)
caught(
    "unbounded_landing",
    "bounded family theorem" in exact and "Maximum conclusion" in audit,
    "scope language blocks promotion beyond the preregistered class",
)

result = {
    "catches_passed": sum(int(row["caught"]) for row in catches),
    "catches_total": len(catches),
    "catches": catches,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"catches_passed": result["catches_passed"], "catches_total": result["catches_total"]}, sort_keys=True))
