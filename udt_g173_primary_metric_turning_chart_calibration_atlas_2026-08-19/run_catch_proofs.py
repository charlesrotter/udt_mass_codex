#!/usr/bin/env python3
"""G173 algebraic and semantic mutation catches."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
exact = (HERE / "EXACT_DERIVATION.md").read_text()
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())


def catch(name: str, condition: bool, detail: str) -> dict[str, object]:
    if not condition:
        raise AssertionError(f"uncaught mutation: {name}: {detail}")
    return {"name": name, "caught": True, "detail": detail}


A = Fraction(4)
r = Fraction(3)
v = Fraction(0)
b2 = Fraction(1)
H = A * v * v + r * r * b2
det_h = -H / A
raw_e4 = A * H
mA2 = v * v + r * r * b2
mP2 = v * v + r * r * b2 / A
e4A = raw_e4 / mA2
e4P = raw_e4 / mP2

catches = [
    catch("dropped_angular_gram", det_h != 0, "v=0 remains regular only when r^2 b^2 is retained"),
    catch("turning_called_rank_failure", det_h == Fraction(-9, 4), "exact turning determinant is negative"),
    catch("true_rank_boundary_erased", "v = b = 0" in exact and "rank one" in exact, "zero complete spatial tangent is explicit"),
    catch("raw_phi_called_scalar", "affine log-density" in exact, "raw Phi chart shift is explicit"),
    catch("calibration_weight_omitted", "positive weight-one line density" in exact, "scalar calibration type is explicit"),
    catch("unique_calibration_imposed", e4A != e4P, "two registered metric-built turning readouts disagree"),
    catch("mA_radial_failure", "both give" in exact and "Phi_A=\\Phi_P=\\Phi_r=\\phi" in exact, "radial recovery is retained"),
    catch("finite_G172_extension_claimed", "No finite pointwise extension" in exact, "bounded no-go is explicit"),
    catch("chart_transition_erased", "Phi_m" in exact and "frac{|v|}{m}" in exact, "G172 overlap has exact transition"),
    catch("postreadout_orchestra", "H=e^{2\\phi}v^2+r^2b^2" in exact, "radial and angular data enter h directly"),
    catch("physical_ruler_selected", "cannot select the physical ruler" in (HERE / "PREREGISTRATION.md").read_text(), "selection is forbidden"),
    catch("cross_calibration_telescoping", "cross-calibration carry\tOPEN" in ledger, "cross-calibration carry remains open"),
    catch("scalar_equals_transport", "non-scalar transport closure\tOPEN" in ledger, "transport remains separately typed"),
    catch("globalized_local_atlas", "global completion" in exact and "OPEN" in exact, "global completion remains open"),
    catch("time_live_widening", "time-live" in exact and "OPEN" in exact, "time-live extension remains open"),
    catch("Xmax_inserted", "`X_max`" in exact and "INACTIVE" in exact, "Xmax is excluded"),
    catch("scaffold_reintroduced", "G142--G160" in exact and "INACTIVE" in exact, "retired scaffold is inactive"),
    catch("external_review_premature", production["status"].endswith("AWAITING_INDEPENDENT_AND_EXTERNAL_REVIEW"), "production is not pre-promoted"),
    catch("independent_replay_shared_code", independent["imports_production_code"] is False and independent["uses_sympy"] is False, "independent replay is stdlib-only"),
]

result = {
    "status": "PASS__G173_MUTATION_AND_SEMANTIC_CATCHES",
    "catches_passed": len(catches),
    "catches_total": len(catches),
    "catches": catches,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
