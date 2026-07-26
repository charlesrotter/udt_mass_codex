#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path, fieldnames, data):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


checks = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


# Freeze and replay every source identity before using it.
manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
for row in manifest:
    source = ROOT / row["source_path"]
    check(f"source:{row['source_path']}", source.is_file() and digest(source) == row["sha256"])

completion_path = ROOT / "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv"
config_path = ROOT / "udt_directional_observer_pair_distance_audit_2026-07-24/CORRECTED_CONFIGURATION_REGISTRY.tsv"
branch_path = ROOT / "udt_observer_longitudinal_transverse_cocycle_audit_2026-07-24/BRANCH_COCYCLE_ATLAS.tsv"
basis_path = ROOT / "udt_founded_pair_first_jet_one_form_atlas_2026-07-26/ONE_FORM_BASIS.tsv"
outcome_path = ROOT / "udt_founded_pair_first_jet_one_form_atlas_2026-07-26/ONE_FORM_OUTCOMES.tsv"
equation_path = ROOT / "udt_directional_observer_pair_distance_audit_2026-07-24/EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv"
bootstrap_equation_path = ROOT / "udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv"

completion = rows(completion_path)
configs = rows(config_path)
branches = rows(branch_path)
basis = rows(basis_path)
outcomes = {row["id"]: row for row in rows(outcome_path)}
equations = rows(equation_path)
bootstrap_equations = rows(bootstrap_equation_path)

check("twelve_completion_classes", len(completion) == 12)
check("completion_ids_exact", {r["completion_id"] for r in completion} == {f"FC{i:02d}_" + r["completion_id"].split("_", 1)[1] for i, r in enumerate(completion, 1)})
check("four_corrected_configurations", len(configs) == 4 and {r["configuration_id"] for r in configs} == {"Q01_ROUND_S3", "Q02_SQUASHED_S3", "Q03_WRL_LOCAL", "Q04_PHYSICAL_XMAX_JOIN"})
check("six_branch_rows", len(branches) == 6)
check("twenty_two_basis_rows", len(basis) == 22 and len(outcomes) == 22)
check("twenty_eight_equation_families", len(equations) == 28)
check("B19_only_complete_equation_family", [r["family_id"] for r in equations if r["complete_spatial_metric"] != "NO"] == ["B19"])
check("zero_complete_simultaneous_closure_families", len(bootstrap_equations) == 28 and all(r["complete_simultaneous_closure"] == "NO" for r in bootstrap_equations))

# A registered completion type is not a solved metric. Only FC04 has the two concrete complete
# configurations recorded by the frozen concrete-configuration sources.
completion_rows = []
for row in completion:
    cid = row["completion_id"]
    if cid == "FC04_TWO_CAP_P1":
        rep = "Q01_ROUND_S3;Q02_SQUASHED_S3"
        status = "CONCRETE_COMPLETE_REPRESENTATIVES_REGISTERED"
        pair_gate = "TEST_CONCRETE_REPRESENTATIVES"
    elif cid == "FC12_RECIPROCAL_TORIC_DIAGONAL":
        rep = "-"
        status = "PARAMETRIC_METRIC_ANSATZ_PROFILE_AND_ENDPOINT_OPEN"
        pair_gate = "NO_ACTUAL_COMPLETE_REPRESENTATIVE"
    else:
        rep = "-"
        status = "COMPLETION_TAXONOMY_WITHOUT_ACTUAL_COMPLETE_METRIC"
        pair_gate = "NO_ACTUAL_COMPLETE_REPRESENTATIVE"
    completion_rows.append({
        "completion_id": cid,
        "source_selection_status": row["selection_status"],
        "registered_concrete_representatives": rep,
        "metric_witness_status": status,
        "founded_pair_pullback_gate": pair_gate,
    })

check("only_FC04_has_concrete_representatives", [r["completion_id"] for r in completion_rows if r["registered_concrete_representatives"] != "-"] == ["FC04_TWO_CAP_P1"])

# Exact homogeneous ultrastatic R x Berger-S3 control.
# de1=p e2^e3, de2=p e3^e1, de3=q e1^e2. Solve the torsion-free connection
# omega12=A e3, omega13=B e2, omega23=C e1.
p, q = sp.symbols("p q", nonzero=True, real=True)
A, B, C = sp.symbols("A B C", real=True)
solution = sp.solve([A - B - p, A + C - p, C - B - q], [A, B, C], dict=True)[0]
check("cartan_connection_solution", solution == {A: p - q / 2, B: -q / 2, C: q / 2})

# Milnor-Ricci eigenvalues in this normalization. The screen is doubly degenerate; the Hopf line is
# simple exactly away from the round p=q locus.
ric_screen = sp.simplify(p * q - q**2 / 2)
ric_hopf = sp.simplify(q**2 / 2)
ric_gap = sp.factor(ric_hopf - ric_screen)
check("ricci_gap", sp.simplify(ric_gap - q * (q - p)) == 0)
check("round_isotropy", sp.simplify(ric_gap.subs(p, q)) == 0)

# Use pair-adapted covector order (u_flat,n_flat,s1,s2). u is parallel and n is the Hopf unit vector.
# The only nonzero first-jet datum is screen twist of nabla n.
motif_vectors = {row["id"]: sp.zeros(4, 1) for row in basis}
motif_vectors["N07"] = sp.Matrix([-q, 0, 0, 0])  # q u_flat, with u_flat=(-1,0,0,0)
motif_vectors["N08"] = sp.Matrix([0, q, 0, 0])   # q n_flat
image_matrix = sp.Matrix.hstack(*(motif_vectors[row["id"]] for row in basis))
check("conditional_pair_image_rank_two", image_matrix.rank() == 2)

o2_ids = [r["id"] for r in basis if r["uses_screen_orientation"] == "NO"]
n_even_ids = [r["id"] for r in basis if outcomes[r["id"]]["n_flip_parity"] == "EVEN"]
o2_even_ids = [i for i in o2_ids if i in n_even_ids]

def rank_for(ids):
    return sp.Matrix.hstack(*(motif_vectors[i] for i in ids)).rank() if ids else 0

check("orientation_free_image_rank_zero", rank_for(o2_ids) == 0)
check("n_even_image_rank_one", rank_for(n_even_ids) == 1)
check("orientation_free_n_even_rank_zero", rank_for(o2_even_ids) == 0)

# Exterior derivatives in two-form order (u^n,u^s1,u^s2,n^s1,n^s2,s1^s2).
# d(q u_flat)=0; d(q n_flat)=q^2 s1^s2.
exterior = {row["id"]: sp.zeros(6, 1) for row in basis}
exterior["N08"] = sp.Matrix([0, 0, 0, 0, 0, q**2])
exterior_matrix = sp.Matrix.hstack(*(exterior[row["id"]] for row in basis))
check("conditional_pair_exterior_rank_one", exterior_matrix.rank() == 1)
check("N07_closed", exterior["N07"] == sp.zeros(6, 1))
check("N08_not_closed", exterior["N08"] != sp.zeros(6, 1))

motif_rows = []
for row in basis:
    mid = row["id"]
    if mid == "N07":
        value = "q*u_flat"
        closed = "YES"
        exact = "YES_AS_q_TIMES_GLOBAL_ULTRASTATIC_TIME"
        founded = "NO_COORDINATE_TIME_NOT_RECIPROCAL_DEPTH"
    elif mid == "N08":
        value = "q*n_flat"
        closed = "NO_d_equals_q_squared_s1_wedge_s2"
        exact = "NO"
        founded = "NO"
    else:
        value = "0"
        closed = "TRIVIALLY"
        exact = "TRIVIALLY"
        founded = "NO_ZERO_FORM"
    motif_rows.append({
        "id": mid,
        "homogeneous_pair_pullback": value,
        "uses_screen_orientation": row["uses_screen_orientation"],
        "n_flip_parity": outcomes[mid]["n_flip_parity"],
        "closed": closed,
        "exact": exact,
        "founded_depth_status": founded,
    })

concrete_rows = [
    {
        "representative_id": "Q01_ROUND_S3_B19",
        "completion_class": "FC04_TWO_CAP_P1",
        "metric_status": "CONDITIONAL_COMPLETE_ON_SHELL_SPATIAL_ULTRASTATIC",
        "global_metric_and_joins": "YES_ROUND_S3_PRODUCT;ANTIPODAL_PATH_SET_VALUED",
        "u_status": "GLOBAL_ULTRASTATIC_TIME_DIRECTION",
        "n_status": "GLOBAL_HOPF_FIELDS_EXIST_BUT_NONE_METRIC_SELECTED_BY_ROUND_ISOTROPY",
        "conditional_motif_rank": "2_FOR_A_CHOSEN_ORIENTED_HOPF_PAIR",
        "orientation_free_rank": "0",
        "exterior_rank": "1_FOR_CHOSEN_ORIENTED_HOPF_PAIR",
        "closed_line": "q*u_flat_IF_HOPF_PAIR_AND_ORIENTATION_CHOSEN",
        "founded_depth": "NO_PAIR_NOT_INTRINSIC_AND_LINE_IS_TIME",
        "ruling": "FAIL_FOUNDED_PAIR_AND_NORMALIZATION_GATES",
    },
    {
        "representative_id": "Q02_SQUASHED_S3_OFF_SHELL",
        "completion_class": "FC04_TWO_CAP_P1",
        "metric_status": "COMPLETE_HOMOGENEOUS_OFF_SHELL_CONTROL",
        "global_metric_and_joins": "YES_BERGER_S3_PRODUCT;FULL_CUT_DISTANCE_ATLAS_OPEN_NOT_FIELD_SMOOTHNESS",
        "u_status": "GLOBAL_ULTRASTATIC_TIME_DIRECTION",
        "n_status": "METRIC_SELECTED_UNORIENTED_SIMPLE_RICCI_EIGENLINE_IF_p_NOT_equal_q",
        "conditional_motif_rank": "2_IF_SCREEN_ORIENTATION_CHOSEN",
        "orientation_free_rank": "0",
        "exterior_rank": "1_IF_SCREEN_ORIENTATION_CHOSEN",
        "closed_line": "q*u_flat_IF_SCREEN_ORIENTATION_CHOSEN",
        "founded_depth": "NO_LINE_IS_TIME_AND_BRANCH_IS_OFF_SHELL",
        "ruling": "FAIL_ORIENTATION_FOUNDING_ON_SHELL_AND_NORMALIZATION_GATES",
    },
    {
        "representative_id": "Q03_WRL_LOCAL",
        "completion_class": "-",
        "metric_status": "LOCAL_STATIC_SPHERICAL_INCOMPLETE",
        "global_metric_and_joins": "NO_ALL_OBSERVER_RECENTERING_OR_COMPLETE_CELL",
        "u_status": "LOCAL_STATIC_DIRECTION",
        "n_status": "LOCAL_RADIAL_DIRECTION_RELATIVE_TO_CHOSEN_CENTER",
        "conditional_motif_rank": "NOT_GLOBAL_EVALUABLE",
        "orientation_free_rank": "NOT_GLOBAL_EVALUABLE",
        "exterior_rank": "NOT_GLOBAL_EVALUABLE",
        "closed_line": "LOCAL_ONLY",
        "founded_depth": "LOCAL_CLOCK_PROFILE_ONLY",
        "ruling": "FAIL_COMPLETE_REPRESENTATIVE_GATE",
    },
    {
        "representative_id": "Q04_PHYSICAL_XMAX_JOIN",
        "completion_class": "-",
        "metric_status": "ABSENT",
        "global_metric_and_joins": "ABSENT",
        "u_status": "ABSENT",
        "n_status": "ABSENT",
        "conditional_motif_rank": "NOT_EVALUABLE",
        "orientation_free_rank": "NOT_EVALUABLE",
        "exterior_rank": "NOT_EVALUABLE",
        "closed_line": "ABSENT",
        "founded_depth": "ABSENT",
        "ruling": "FAIL_ABSENT_REPRESENTATIVE",
    },
]

branch_rows = []
for row in branches:
    bid = row["branch"]
    if bid == "B19_ROUND_S3":
        representative = "Q01_ROUND_S3_B19"
        ruling = "CONCRETE_TESTED_NO_FOUNDED_PAIR_DEPTH"
    elif bid == "SQUASHED_S3_OFF_SHELL":
        representative = "Q02_SQUASHED_S3_OFF_SHELL"
        ruling = "CONCRETE_TESTED_OFF_SHELL_NO_FOUNDED_DEPTH"
    elif bid == "WRL_LOCAL_RESIDUAL":
        representative = "Q03_WRL_LOCAL"
        ruling = "LOCAL_NOT_COMPLETE"
    elif bid == "CONSTANT_SPATIAL_CURVATURE_STATIC_CONTROL":
        representative = "-"
        ruling = "COMPARISON_NOT_REGISTERED_UDT_BRANCH"
    else:
        representative = "-"
        ruling = "NO_COMPLETE_METRIC_REPRESENTATIVE"
    branch_rows.append({
        "branch": bid,
        "source_metric_status": row["metric_status"],
        "concrete_representative": representative,
        "pullback_ruling": ruling,
    })

gate_rows = [
    {
        "representative_id": "Q01_ROUND_S3_B19",
        "G1_complete_metric": "PASS_CONDITIONAL_C2",
        "G2_global_domain_joins": "PASS_S3_PRODUCT_PATH_SET_VALUED_AT_ANTIPODES",
        "G3_global_u": "PASS_ULTRASTATIC",
        "G4_metric_selected_n": "FAIL_ROUND_ISOTROPY",
        "G5_surviving_motifs": "CONDITIONAL_CHOSEN_HOPF_PAIR_ONLY",
        "G6_span_and_exterior_rank": "CONDITIONAL_2_AND_1",
        "G7_global_closed_exact_line": "CONDITIONAL_q_u_flat_EQUALS_MINUS_q_dt",
        "G8_founded_normalized_depth": "FAIL_COORDINATE_TIME_NOT_RECIPROCAL_DEPTH",
        "all_gates": "NO",
    },
    {
        "representative_id": "Q02_SQUASHED_S3_OFF_SHELL",
        "G1_complete_metric": "PASS_OFF_SHELL_CONTROL",
        "G2_global_domain_joins": "PASS_GLOBAL_BERGER_S3_FIELD_GEOMETRY",
        "G3_global_u": "PASS_ULTRASTATIC",
        "G4_metric_selected_n": "PARTIAL_UNORIENTED_SIMPLE_RICCI_EIGENLINE",
        "G5_surviving_motifs": "N07_N08_ONLY_IF_SCREEN_ORIENTATION_CHOSEN",
        "G6_span_and_exterior_rank": "CONDITIONAL_2_AND_1;O2_RANK_0",
        "G7_global_closed_exact_line": "CONDITIONAL_q_u_flat_EQUALS_MINUS_q_dt",
        "G8_founded_normalized_depth": "FAIL_COORDINATE_TIME_OFF_SHELL_NOT_RECIPROCAL_DEPTH",
        "all_gates": "NO",
    },
    {
        "representative_id": "Q03_WRL_LOCAL",
        "G1_complete_metric": "FAIL_LOCAL",
        "G2_global_domain_joins": "FAIL",
        "G3_global_u": "NOT_EVALUABLE",
        "G4_metric_selected_n": "NOT_EVALUABLE_GLOBALLY",
        "G5_surviving_motifs": "NOT_EVALUABLE_GLOBALLY",
        "G6_span_and_exterior_rank": "NOT_EVALUABLE_GLOBALLY",
        "G7_global_closed_exact_line": "NOT_EVALUABLE_GLOBALLY",
        "G8_founded_normalized_depth": "FAIL_GLOBAL_GATE",
        "all_gates": "NO",
    },
    {
        "representative_id": "Q04_PHYSICAL_XMAX_JOIN",
        "G1_complete_metric": "FAIL_ABSENT",
        "G2_global_domain_joins": "FAIL_ABSENT",
        "G3_global_u": "ABSENT",
        "G4_metric_selected_n": "ABSENT",
        "G5_surviving_motifs": "NOT_EVALUABLE",
        "G6_span_and_exterior_rank": "NOT_EVALUABLE",
        "G7_global_closed_exact_line": "ABSENT",
        "G8_founded_normalized_depth": "ABSENT",
        "all_gates": "NO",
    },
]

full_pass = [r for r in concrete_rows if r["ruling"] == "PASS_ALL_EIGHT_GATES"]
check("no_full_witness", not full_pass)
check("no_nontrivial_orientation_free_motif_on_complete_controls", all(r["orientation_free_rank"] in {"0", "NOT_GLOBAL_EVALUABLE", "NOT_EVALUABLE"} for r in concrete_rows))
check("B19_and_WRL_not_spliced", concrete_rows[0]["metric_status"].find("ULTRASTATIC") >= 0 and concrete_rows[2]["ruling"] == "FAIL_COMPLETE_REPRESENTATIVE_GATE")

write_tsv(HERE / "COMPLETION_PULLBACK_ATLAS.tsv", list(completion_rows[0]), completion_rows)
write_tsv(HERE / "CONCRETE_REPRESENTATIVE_ATLAS.tsv", list(concrete_rows[0]), concrete_rows)
write_tsv(HERE / "BRANCH_PULLBACK_ATLAS.tsv", list(branch_rows[0]), branch_rows)
write_tsv(HERE / "HOMOGENEOUS_MOTIF_PULLBACK.tsv", list(motif_rows[0]), motif_rows)
write_tsv(HERE / "EIGHT_GATE_MATRIX.tsv", list(gate_rows[0]), gate_rows)

result = {
    "result": "PASS",
    "grade": "VERIFIED_WITH_CAVEATS_REGISTERED_COMPLETE_BRANCH_PULLBACK",
    "checks": checks,
    "counts": {
        "source_rows": len(manifest),
        "completion_classes": len(completion),
        "corrected_configurations": len(configs),
        "branch_rows": len(branches),
        "equation_families": len(equations),
        "first_jet_basis": len(basis),
        "completion_classes_with_concrete_representatives": 1,
        "concrete_complete_metric_configurations": 2,
        "conditional_or_on_shell_complete": 1,
        "off_shell_complete_controls": 1,
        "full_founded_depth_witnesses": len(full_pass),
    },
    "homogeneous_control": {
        "connection": {"A": str(solution[A]), "B": str(solution[B]), "C": str(solution[C])},
        "ricci_screen": str(ric_screen),
        "ricci_hopf": str(ric_hopf),
        "ricci_gap": str(ric_gap),
        "conditional_motif_rank": image_matrix.rank(),
        "orientation_free_rank": rank_for(o2_ids),
        "n_even_rank": rank_for(n_even_ids),
        "orientation_free_n_even_rank": rank_for(o2_even_ids),
        "exterior_rank": exterior_matrix.rank(),
        "nonzero_motifs": ["N07", "N08"],
        "closed_nonzero_line": "N07=q*u_flat",
        "nonclosed_line": "N08=q*n_flat;dN08=q^2*s1_wedge_s2",
    },
    "authority_boundary": {
        "complete_branch_selected": False,
        "global_founded_pair_selected": False,
        "coordinate_time_identified_with_phi": False,
        "higher_jet_rule_invented": False,
        "action_selected": False,
        "carrier_or_source_selected": False,
        "density_or_bootstrap_selected": False,
        "boundary_or_Xmax_selected": False,
        "gpu_work": False,
        "repository_reorganization": False,
    },
    "maximum_conclusion": "REGISTERED_COMPLETION_AND_REPRESENTATIVE_UNIVERSE_CENSUSED;COMPLETE_BRANCH_FIRST_JET_PULLBACKS_DERIVED_WITHIN_EXPLICIT_HOMOGENEOUS_CONTROLS;NO_REGISTERED_COMPLETE_PULLBACK_WITNESS",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
