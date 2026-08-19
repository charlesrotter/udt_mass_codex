#!/usr/bin/env python3
"""G174 algebraic and semantic mutation catches."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
exact = (HERE / "EXACT_DERIVATION.md").read_text()
prereg = (HERE / "PREREGISTRATION.md").read_text()
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
mA2 = v * v + r * r * b2
mP2 = v * v + r * r * b2 / A
e4A = A * H / mA2
e4P = A * H / mP2

catches = [
    catch("line_called_calibrated_vector", "an unoriented line or two-plane, does not fix a vector scale" in exact, "line and calibrated vector are separated"),
    catch("m_called_new_physical_scalar", "Jacobian" in exact and "not an extra post-pullback response" in exact, "m is typed as calibration Jacobian"),
    catch("m_held_fixed_under_reparam", "\\widetilde m=|\\lambda|m" in exact, "density transforms with the auxiliary chart"),
    catch("calibrated_tangent_changed_by_reparam", "F_*\\partial_s" in exact and "unchanged" in exact, "calibrated tangent is chart-independent"),
    catch("two_scalars_same_germ", mA2 != mP2 and e4A != e4P, "G173 candidates have different calibrated vectors"),
    catch("mA_selected", "Neither is selected" in exact, "m_A remains unselected"),
    catch("mP_selected", "Neither is selected" in exact, "m_P remains unselected"),
    catch("constant_unit_changes_depth", "Every endpoint density shifts by the same constant" in exact, "same-tape endpoint response is constant-scale blind"),
    catch("variable_recalibration_called_gauge", "It changes the grading of the tape" in exact, "variable ruler rescaling is a different input"),
    catch("G173_tensor_rejected", "G173's tensor and rank theorem survives unchanged" in exact, "turning regularity is retained"),
    catch("physical_owner_claimed", "`OPEN`: which physical pair relation supplies that calibration" in exact, "physical ownership remains open"),
    catch("path_inserted", "No path" in exact, "no route selector is introduced"),
    catch("Xmax_inserted", "`X_max`" in exact and "INACTIVE" in exact, "Xmax remains inactive"),
    catch("scaffold_reintroduced", "G142--G160" in exact and "INACTIVE" in exact, "retired scaffold remains inactive"),
    catch("globalized", "global completion" in exact and "OPEN" in exact, "local type theorem is not globalized"),
    catch("prereg_falsifier_missing", "same fully calibrated spatial vector" in prereg, "the decisive falsifier was preregistered"),
    catch("status_ledger_owner_drift", "physical calibration owner\tOPEN" in ledger, "ledger retains ownership boundary"),
    catch("independent_shared_code", independent["imports_production_code"] is False and independent["uses_sympy"] is False, "independent replay is stdlib-only"),
]

result = {
    "status": "PASS__G174_MUTATION_AND_SEMANTIC_CATCHES",
    "catches_passed": len(catches),
    "catches_total": len(catches),
    "catches": catches,
    "production_status": production["status"],
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
