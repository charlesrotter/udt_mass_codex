#!/usr/bin/env python3
import csv
import json
from pathlib import Path

here = Path(__file__).resolve().parent

def rows(name):
    with (here/name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))

production = json.loads((here/"TRANSPORT_RESULT.json").read_text())
independent = json.loads((here/"INDEPENDENT_VERIFICATION.json").read_text())
semantic = json.loads((here/"SEMANTIC_VERIFICATION.json").read_text())
cold = json.loads((here/"COLD_REVIEW_RESULT.json").read_text())
repo = json.loads((here/"REPOSITORY_GATES.json").read_text())
object_universe = rows("OBJECT_UNIVERSE.tsv")
object_status = rows("OBJECT_STATUS.tsv")
premises = rows("PREMISE_LEDGER.tsv")
premise_audit = rows("PREMISE_AUDIT.tsv")

assert production["status"] == "PASS_EXACT_PRODUCTION"
assert independent["status"] == "PASS_INDEPENDENT_HIGH_PRECISION"
assert semantic["status"] == "PASS_FAIL_CLOSED" and semantic["mutation_catches"] == 36
assert cold["final_grade"] == "PASS_WITH_CAVEATS"
assert repo["status"] == "PASS"
assert [(r["object_id"],r["object"]) for r in object_status] == [(r["object_id"],r["object"]) for r in object_universe]
assert [(r["premise_id"],r["choice_or_object"]) for r in premise_audit] == [(r["premise_id"],r["choice_or_object"]) for r in premises]

result = {
    "schema": "udt-defect-transport-adjudication-1.0",
    "status": "VERIFIED_WITH_CAVEATS",
    "scope": "frozen_stationary_off_shell_18_candidate_ensemble",
    "full_transport_candidates": 6,
    "controls": {"intrinsic_zero": 9, "projector_blocked": 2, "metric_degenerate": 1},
    "derived": [
        "defect_graph_H1_Z5",
        "global_lift_and_w1_zero",
        "trivial_real_line_connection_and_holonomy",
        "regular_edge_turning_magnitude_one",
        "two_six_puncture_pole_links",
        "metric_anchored_kernel_plane_connection_formula",
        "exact_twist_scaling"
    ],
    "observed_exact_bounded": [
        "12_nonzero_curvature_point_certificates",
        "four_registered_screen_lambda_coordinate_triples_distinct_at_p1_p2"
    ],
    "open": cold["scope_caveats"],
    "charge_carrier_substrate_or_physics_selected": False,
    "four_gates": {"preregistered": True, "bounded_scope": True, "independently_verified": True, "premises_audited": True},
}
(here/"ADJUDICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
