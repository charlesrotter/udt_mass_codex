#!/usr/bin/env python3
"""Build the preregistered P03G law-neutral global kinematic assembly atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = "CURRENT_GLOBAL_KINEMATIC_ASSEMBLY_CONDITIONS_AND_OPEN_BRANCHES_CHARACTERIZED"

PARENT_MANIFESTS = {
    "P01": ("udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt", "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad"),
    "P02": ("udt_local_jet_atlas_p02_2026-07-21/SHA256SUMS.txt", "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938"),
    "P03": ("udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt", "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be"),
    "COMPLETE_MAP": ("udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt", "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38"),
    "GLOBAL_COCYCLE": ("udt_global_coframe_cocycle_audit_2026-07-20/SHA256SUMS.txt", "1297e8f6773f863f426d66f6c4915741a742c1ee13230abf2b066421de49b04b"),
    "STATIC_SEAL": ("finite_cell_seal_boundary_phase_join_2026-07-20/SHA256SUMS.txt", "704b084548a212eabcfb1ac051e89234a7fd91bbeaf7f70abcc28bf63edc7a3b"),
    "COMPLETE_SEAL": ("udt_complete_seal_fixed_set_selector_audit_2026-07-21/SHA256SUMS.txt", "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def rows() -> dict[str, list[dict[str, object]]]:
    inputs = [
        {"id": "I01", "object": "P02_P03_local_configuration_atlas", "domain": "POINT_LOCAL", "authority": "FROZEN_PARENT", "status": "EXACT_INPUT", "source": "udt_founded_constraint_atlas_p03_2026-07-21/STATUS_LEDGER.tsv:S18", "open_or_limit": "On-shell and global occurrence unevaluated"},
        {"id": "I02", "object": "local_field_realizations_C01_C07", "domain": "POINT_LOCAL_TO_GLOBAL", "authority": "FROZEN_PARENT", "status": "SEVEN_BRANCH_INPUT", "source": "udt_complete_metric_solution_space_map_2026-07-21/OFFSHELL_CONFIGURATION_BRANCHES.tsv", "open_or_limit": "No branch has global existence proved"},
        {"id": "I03", "object": "reciprocal_transition_group_G_F", "domain": "OVERLAPS", "authority": "DERIVED_EXACT", "status": "COMPATIBILITY_INPUT", "source": "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv:C01-C07", "open_or_limit": "Two-channel constant real class only"},
        {"id": "I04", "object": "cover_nerve_overlap_incidence", "domain": "GLOBAL_CELL", "authority": "NOT_SUPPLIED", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_global_coframe_cocycle_audit_2026-07-20/STATUS_LEDGER.tsv:S08", "open_or_limit": "Algebra does not generate a cover"},
        {"id": "I05", "object": "actual_transition_cocycle_and_global_Z2_class", "domain": "GLOBAL_CELL", "authority": "NOT_SUPPLIED", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv:C15", "open_or_limit": "Even local cocycle parity does not select its global class"},
        {"id": "I06", "object": "CSN_local_representative_changes", "domain": "OVERLAPS", "authority": "FOUNDING_EQUIVALENCE", "status": "IDENTIFICATION_ONLY", "source": "udt_founded_constraint_atlas_p03_2026-07-21/CONSTRAINT_EFFECT_LEDGER.tsv:E06-E11", "open_or_limit": "No physical or global representative selected"},
        {"id": "I07", "object": "global_signed_phi", "domain": "GLOBAL_CELL", "authority": "NOT_SUPPLIED", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_founded_constraint_atlas_p03_2026-07-21/REALIZATION_BRANCHES.tsv:B05", "open_or_limit": "Existence zero set and sign holonomy unproved"},
        {"id": "I08", "object": "full_four_dimensional_coframe_soldering", "domain": "OVERLAPS_AND_CELL", "authority": "CONDITIONAL", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_founded_constraint_atlas_p03_2026-07-21/STATUS_LEDGER.tsv:S05", "open_or_limit": "Two-channel character does not select a full coframe map"},
        {"id": "I09", "object": "static_phi_seal_wire", "domain": "STATIC_SEAL", "authority": "PINNED_SCOPED", "status": "PHI_ZERO_DELTA_PHI_ZERO_NORMAL_JET_FREE", "source": "finite_cell_seal_boundary_phase_join_2026-07-20/STATUS_LEDGER.tsv:S02-S04", "open_or_limit": "One scalar wire only"},
        {"id": "I10", "object": "complete_seal_lift_and_boundary_polarization", "domain": "SEAL_AND_CORNERS", "authority": "NOT_SUPPLIED", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_complete_seal_fixed_set_selector_audit_2026-07-21/STATUS_LEDGER.tsv:F16-F17", "open_or_limit": "Four local lift classes and multiple variations survive"},
        {"id": "I11", "object": "topology_caps_periods_quotient_no_cap", "domain": "GLOBAL_CELL", "authority": "NOT_SUPPLIED", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv:C14-C15", "open_or_limit": "Bounded witnesses are nonexhaustive"},
        {"id": "I12", "object": "regular_degenerate_type_changing_completion", "domain": "GLOBAL_CELL", "authority": "PRESERVED_PARENT_BRANCHES", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_founded_constraint_atlas_p03_2026-07-21/COMPLETENESS_SCOPE.tsv:1_FIELDS;4_DOMAIN_COORDINATES", "open_or_limit": "Inverse-metric diagnostics do not cover degeneracies"},
        {"id": "I13", "object": "connection_and_torsion", "domain": "GLOBAL_CELL", "authority": "CONDITIONAL_BRANCH", "status": "OPEN_ASSEMBLY_DATA", "source": "udt_complete_metric_solution_space_map_2026-07-21/OFFSHELL_CONFIGURATION_BRANCHES.tsv:C07", "open_or_limit": "Levi-Civita and independent-connection branches remain separate"},
        {"id": "I14", "object": "physical_representative_scale_Xmax", "domain": "COMPLETE_CELL", "authority": "OPEN_GLOBAL_OUTPUT", "status": "NOT_EVALUABLE", "source": "udt_founded_constraint_atlas_p03_2026-07-21/CONSTRAINT_EFFECT_LEDGER.tsv:E21", "open_or_limit": "No supplied local ruler or physical section"},
        {"id": "I15", "object": "mass_volume_density_bootstrap", "domain": "COMPLETE_MATTER_BEARING_SOLUTION", "authority": "WORKING_GLOBAL_ADMISSIBILITY", "status": "NOT_EVALUABLE", "source": "udt_founded_constraint_atlas_p03_2026-07-21/CONSTRAINT_EFFECT_LEDGER.tsv:E22", "open_or_limit": "Native mass volume stability and solution do not exist yet"},
        {"id": "I16", "object": "action_equation_source_carrier_merit", "domain": "DYNAMICS", "authority": "EXCLUDED", "status": "NOT_LOADED", "source": "udt_founded_constraint_atlas_p03_2026-07-21/CONSTRAINT_EFFECT_LEDGER.tsv:E24", "open_or_limit": "P04 not launched"},
    ]

    schema = [
        {"axis_id": "A01", "object": "local_field_realization", "local_input": "C01-C07", "required_global_data": "field bundle and transition law for every independent field", "founded_compatibility": "retain all seven branches", "status": "OPEN_EXTENSION", "bounded_exhaustiveness": "EXACT_FOR_REGISTERED_LOCAL_BRANCHES"},
        {"axis_id": "A02", "object": "cover_and_nerve", "local_input": "charts are local only", "required_global_data": "cover overlap triple-overlap corner and boundary incidence", "founded_compatibility": "finite cell requires completion", "status": "OPEN_DATA", "bounded_exhaustiveness": "SCHEMA_ONLY"},
        {"axis_id": "A03", "object": "reciprocal_transition_component", "local_input": "G_a and F_b", "required_global_data": "component and nonzero modulus on each overlap", "founded_compatibility": "exact G/F multiplication laws", "status": "PARTLY_DERIVED", "bounded_exhaustiveness": "COMPLETE_CONSTANT_REAL_TWO_CHANNEL_CLASS"},
        {"axis_id": "A04", "object": "closed_path_cocycle_and_reversal_class", "local_input": "Z2 grading", "required_global_data": "cocycle satisfying triple relations plus global class", "founded_compatibility": "closed identity products have even F parity", "status": "OPEN_GLOBAL_CLASS", "bounded_exhaustiveness": "LOCAL_ALGEBRA_EXACT_GLOBAL_BUNDLE_OPEN"},
        {"axis_id": "A05", "object": "CSN_representative_patching", "local_input": "positive local common scale", "required_global_data": "positive overlap factors and existence of any global representative", "founded_compatibility": "representatives identified not ranked", "status": "OPEN_GLOBAL_SECTION", "bounded_exhaustiveness": "SCHEMA_ONLY"},
        {"axis_id": "A06", "object": "signed_phi_patching", "local_input": "signed local phi", "required_global_data": "scalar or line-bundle law zero set and sign holonomy", "founded_compatibility": "do not identify sign with nonnegative distance", "status": "OPEN_GLOBAL_FIELD", "bounded_exhaustiveness": "SCHEMA_ONLY"},
        {"axis_id": "A07", "object": "full_coframe_soldering_and_angular_lift", "local_input": "conditional reciprocal two-plane", "required_global_data": "complete four-dimensional lift and angular transition", "founded_compatibility": "do not promote two-channel group to full coframe", "status": "OPEN_FULL_LIFT", "bounded_exhaustiveness": "FOUR_CONSTANT_SEAL_LIFTS_ONLY"},
        {"axis_id": "A08", "object": "seal_and_boundary_tangent", "local_input": "phi=0 delta_phi=0 normal_phi_jet_free", "required_global_data": "full involution boundary polarization corner and normal-jet rules", "founded_compatibility": "one scalar tangent removed only", "status": "OPEN_COMPLETION", "bounded_exhaustiveness": "SCALAR_RULE_EXACT_OTHER_FIELDS_OPEN"},
        {"axis_id": "A09", "object": "topology_caps_periods_quotient_no_cap", "local_input": "finite mirrored ontology", "required_global_data": "global topology cap cycles periods quotient and boundary count", "founded_compatibility": "p=0,1,3,5 and general alternatives survive", "status": "OPEN_TOPOLOGY", "bounded_exhaustiveness": "WITNESS_LIST_PLUS_OTHER_UNENUMERATED"},
        {"axis_id": "A10", "object": "regular_degenerate_type_changing_singular_completion", "local_input": "all P02 inertia closures", "required_global_data": "degeneracy locus chart transitions and admissibility rule", "founded_compatibility": "no local stratum removed", "status": "OPEN_COMPLETION", "bounded_exhaustiveness": "SCHEMA_ONLY"},
        {"axis_id": "A11", "object": "connection_and_torsion", "local_input": "metric or independent connection branch", "required_global_data": "global connection bundle holonomy torsion and boundary data", "founded_compatibility": "Levi-Civita only after regular representative supplied", "status": "OPEN_BRANCH", "bounded_exhaustiveness": "REGISTERED_BRANCH_SPLIT_ONLY"},
        {"axis_id": "A12", "object": "scale_Xmax_mass_volume_bootstrap", "local_input": "none point-locally", "required_global_data": "complete physical representative native matter mass volume stability and density", "founded_compatibility": "evaluate only after complete matter-bearing solution", "status": "NOT_EVALUABLE", "bounded_exhaustiveness": "DOWNSTREAM_OUTPUT_SCHEMA"},
    ]

    cocycles = [
        {"id": "C01", "branch": "all_preserving_G", "exact_condition": "G_a G_d=G_ad", "assembly_status": "SURVIVES_CONDITIONALLY", "selected": "NO", "open_data": "cover and overlap values"},
        {"id": "C02", "branch": "two_inverting_maps", "exact_condition": "F_b F_c=G_(b/c)", "assembly_status": "SURVIVES_CONDITIONALLY", "selected": "NO", "open_data": "actual overlap labels"},
        {"id": "C03", "branch": "mixed_preserving_inverting", "exact_condition": "G_a F_b=F_(ab); F_b G_a=F_(b/a)", "assembly_status": "SURVIVES_CONDITIONALLY", "selected": "NO", "open_data": "actual overlap labels"},
        {"id": "C04", "branch": "three_inverting_triple_overlap", "exact_condition": "F_b F_c F_d=F_(bd/c)!=I", "assembly_status": "EXCLUDED_BY_EXACT_COCYCLE", "selected": "NO", "open_data": "none within declared constant two-channel class"},
        {"id": "C05", "branch": "two_inverting_one_preserving_triple", "exact_condition": "F_b F_c G_(c/b)=I", "assembly_status": "EXACT_LOCAL_COCYCLE_WITNESS", "selected": "NO", "open_data": "global cover and bundle"},
        {"id": "C06", "branch": "closed_identity_product_odd_reversal_parity", "exact_condition": "Z2_sum=1 cannot equal identity component", "assembly_status": "EXCLUDED_BY_EXACT_COCYCLE", "selected": "NO", "open_data": "none within declared group"},
        {"id": "C07", "branch": "closed_identity_product_even_reversal_parity", "exact_condition": "Z2_sum=0 is necessary", "assembly_status": "NECESSARY_NOT_SUFFICIENT", "selected": "NO", "open_data": "continuous product cover and global class"},
        {"id": "C08", "branch": "global_Z2_class", "exact_condition": "transition grading is local cocycle data", "assembly_status": "OPEN_GLOBAL_CLASS", "selected": "NO", "open_data": "cover gauge and cohomology class"},
        {"id": "C09", "branch": "continuous_transition_modulus", "exact_condition": "G_a F_b G_a^-1=F_(a^2 b)", "assembly_status": "IDENTIFIED_UP_TO_CONJUGACY_ONLY", "selected": "NO", "open_data": "sign class physical readout and field-dependent extension"},
        {"id": "C10", "branch": "mixed_readout_modulus", "exact_condition": "mu=B^2/(A^2 b^2)>1 is CSN and diagonal-gauge invariant", "assembly_status": "MULTIPLE_VALUES_SURVIVE_CONDITIONALLY", "selected": "NO", "open_data": "physical soldering and observer slicing"},
        {"id": "C11", "branch": "supplied_corner_incidence", "exact_condition": "commuting F_b,F_c gives c=+/-b; angular axes same or perpendicular", "assembly_status": "REDUCES_AFTER_INCIDENCE_SUPPLIED", "selected": "NO", "open_data": "number order angle and incidence of corners"},
        {"id": "C12", "branch": "field_dependent_full_4x4_transition", "exact_condition": "not classified by constant two-channel audit", "assembly_status": "OPEN_UNENUMERATED", "selected": "NO", "open_data": "complete coframe transition law"},
    ]

    lifts = [
        {"id": "L01", "object": "angular_plus_identity", "full_determinant": "-1", "coframe_fixed_dim": "3", "coframe_antifixed_dim": "1", "metric_even_dim": "7", "metric_odd_dim": "3", "compatibility": "compatible with scalar odd phi rule", "status": "CONDITIONAL_UNSELECTED", "limit": "ordinary codimension-one fixed mirror is extra premise"},
        {"id": "L02", "object": "angular_minus_identity", "full_determinant": "-1", "coframe_fixed_dim": "1", "coframe_antifixed_dim": "3", "metric_even_dim": "7", "metric_odd_dim": "3", "compatibility": "compatible with scalar odd phi rule", "status": "CONDITIONAL_UNSELECTED", "limit": "codimension-three fixed-set interpretation unforced"},
        {"id": "L03", "object": "angular_axis_reflection", "full_determinant": "+1", "coframe_fixed_dim": "2", "coframe_antifixed_dim": "2", "metric_even_dim": "6", "metric_odd_dim": "4", "compatibility": "compatible with scalar odd phi rule", "status": "CONDITIONAL_UNSELECTED", "limit": "axis and global period data unselected"},
        {"id": "L04", "object": "local_Hopf_exchange", "full_determinant": "+1", "coframe_fixed_dim": "2", "coframe_antifixed_dim": "2", "metric_even_dim": "6", "metric_odd_dim": "4", "compatibility": "locally conjugate to axis reflection", "status": "CONDITIONAL_UNSELECTED", "limit": "global distinction requires integral basis periods cover or quotient"},
        {"id": "L05", "object": "static_phi_rule_only", "full_determinant": "NA", "coframe_fixed_dim": "NA", "coframe_antifixed_dim": "NA", "metric_even_dim": "9", "metric_odd_dim": "1", "compatibility": "phi=0 delta_phi=0 and free normal derivative", "status": "PINNED_SCOPED_NOT_COMPLETE_LIFT", "limit": "does not select L01-L04"},
        {"id": "L06", "object": "boundary_Dirichlet_witness", "full_determinant": "NA", "coframe_fixed_dim": "NA", "coframe_antifixed_dim": "NA", "metric_even_dim": "NA", "metric_odd_dim": "NA", "compatibility": "preserves scalar seal wire", "status": "CONDITIONAL_VARIATION_WITNESS", "limit": "not selected by kinematics"},
        {"id": "L07", "object": "boundary_Neumann_or_mixed_witness", "full_determinant": "NA", "coframe_fixed_dim": "NA", "coframe_antifixed_dim": "NA", "metric_even_dim": "NA", "metric_odd_dim": "NA", "compatibility": "preserves scalar seal wire with different transverse choices", "status": "CONDITIONAL_VARIATION_WITNESS", "limit": "not selected by kinematics"},
    ]

    topology = [
        {"id": "T01", "branch": "finite_cell_with_uncapped_boundary", "kind": "NO_CAP_OR_BOUNDARY_RETAINED", "witness_parameter": "NA", "status": "OPEN", "selected": "NO", "limit": "finite ontology does not require a particular cap"},
        {"id": "T02", "branch": "primitive_toric_cap_p0", "kind": "TORIC_WITNESS", "witness_parameter": "p=0", "status": "CONDITIONAL_SURVIVOR", "selected": "NO", "limit": "cover and periods supplied only in witness"},
        {"id": "T03", "branch": "primitive_toric_cap_p1", "kind": "S3_WITNESS", "witness_parameter": "p=1", "status": "CONDITIONAL_SURVIVOR", "selected": "NO", "limit": "not selected without globally diagonal opposing-eigen-circle premises"},
        {"id": "T04", "branch": "primitive_toric_cap_p3", "kind": "LENS_WITNESS", "witness_parameter": "p=3", "status": "CONDITIONAL_SURVIVOR", "selected": "NO", "limit": "inequivalent to p1 and not excluded"},
        {"id": "T05", "branch": "primitive_toric_cap_p5", "kind": "LENS_WITNESS", "witness_parameter": "p=5", "status": "CONDITIONAL_SURVIVOR", "selected": "NO", "limit": "inequivalent to p1/p3 and not excluded"},
        {"id": "T06", "branch": "general_toric_or_lens_family", "kind": "UNBOUNDED_PARAMETER_FAMILY", "witness_parameter": "general_p", "status": "OPEN", "selected": "NO", "limit": "bounded examples do not exhaust family"},
        {"id": "T07", "branch": "other_non_toric_or_unenumerated_topology", "kind": "OTHER_UNENUMERATED", "witness_parameter": "NA", "status": "OPEN_REQUIRED_REMAINDER", "selected": "NO", "limit": "prevents false exhaustive claim"},
        {"id": "T08", "branch": "regular_non_degenerate_completion", "kind": "REGULAR", "witness_parameter": "NA", "status": "OPEN_GLOBAL_EXISTENCE", "selected": "NO", "limit": "local regularity is not global existence"},
        {"id": "T09", "branch": "degenerate_or_type_changing_completion", "kind": "DEGENERATE_CLOSURE", "witness_parameter": "NA", "status": "OPEN_PRESERVED", "selected": "NO", "limit": "inverse-metric diagnostics do not classify this closure"},
        {"id": "T10", "branch": "singular_or_stratified_completion", "kind": "OTHER_UNENUMERATED", "witness_parameter": "NA", "status": "OPEN_REQUIRED_REMAINDER", "selected": "NO", "limit": "admissibility rule absent"},
        {"id": "T11", "branch": "global_phi_scalar", "kind": "TRIVIAL_SIGN_BUNDLE", "witness_parameter": "NA", "status": "OPEN", "selected": "NO", "limit": "global existence and zero-set incidence unproved"},
        {"id": "T12", "branch": "phi_with_sign_holonomy_or_local_sections", "kind": "NONTRIVIAL_SIGN_PATCHING", "witness_parameter": "NA", "status": "OPEN", "selected": "NO", "limit": "must be reconciled with physical phi semantics"},
    ]

    gates = []
    gate_specs = [
        ("C01", "CONFORMAL_METRIC_ONLY", "metric atlas; CSN factors; topology; boundary", "global conformal metric and representative existence"),
        ("C02", "CONFORMAL_METRIC_PLUS_INDEPENDENT_PHI", "C01 data plus phi patching", "global relation between phi and metric"),
        ("C03", "COFRAME_PLUS_RECIPROCAL_CHARACTER", "full coframe soldering; G/F cocycle; angular lifts", "global coframe bundle and section"),
        ("C04", "METRIC_PLUS_SUPPLIED_PROJECTOR", "global rank-two subbundle and transition preservation", "projector holonomy and seal action"),
        ("C05", "METRIC_PLUS_RECIPROCAL_CONSTRAINT", "globally defined constraint and boundary compatibility", "off-shell enforcement belongs to unselected dynamics"),
        ("C06", "TWO_STAGE_PRE_POST_SCALE_BRIDGE", "pre-scale object; global section; post-scale map", "bridge and scale selection"),
        ("C07", "INDEPENDENT_CONNECTION_OR_TORSION", "connection bundle; transition law; torsion and boundary data", "global connection dynamics and relation to metric"),
    ]
    for index, (branch, name, closure, missing) in enumerate(gate_specs, 1):
        gates.append({"id": f"G{index:02d}", "local_branch": branch, "branch_name": name, "required_closure": closure, "currently_derived": "NO", "current_ruling": "LOCAL_BRANCH_RETAINED_GLOBAL_EXISTENCE_UNEVALUATED", "missing_data": missing})

    countermodels = [
        {"id": "M01", "challenged_inference": "transition algebra supplies a cover", "witness": "same G/F multiplication table can be assigned to different declared covers", "preserved_inputs": "local reciprocal group", "varied_output": "cover nerve and overlap incidence", "ruling": "INFERENCE_FAILS"},
        {"id": "M02", "challenged_inference": "local cocycle witness selects a global bundle", "witness": "F_b F_c G_(c/b)=I is valid before any global cover is specified", "preserved_inputs": "exact triple product", "varied_output": "global cocycle class", "ruling": "INFERENCE_FAILS"},
        {"id": "M03", "challenged_inference": "seal closure selects mixed readout", "witness": "mu=4 and mu=9 full Lorentzian mirror witnesses", "preserved_inputs": "reciprocity CSN phi visibility and seal isometry", "varied_output": "dimensionless mixing modulus", "ruling": "INFERENCE_FAILS"},
        {"id": "M04", "challenged_inference": "scalar seal selects complete lift", "witness": "L01-L04 all preserve the scalar odd phi rule", "preserved_inputs": "phi=0 delta_phi=0 free normal derivative", "varied_output": "full coframe fixed/antifixed multiplicities", "ruling": "INFERENCE_FAILS"},
        {"id": "M05", "challenged_inference": "mirror selects boundary polarization", "witness": "Dirichlet and Neumann/mixed full variation witnesses preserve the scalar seal", "preserved_inputs": "static phi seal wire", "varied_output": "transverse and momentum variations", "ruling": "INFERENCE_FAILS"},
        {"id": "M06", "challenged_inference": "regular primitive caps select p=1", "witness": "p=1 p=3 and p=5 primitive mirror-compatible cap witnesses", "preserved_inputs": "declared toric regularity and mirror compatibility", "varied_output": "global topology", "ruling": "INFERENCE_FAILS"},
        {"id": "M07", "challenged_inference": "finite cell excludes no-cap or other topology", "witness": "finite-domain statement supplies no cap period quotient or boundary count", "preserved_inputs": "finite mirrored ontology", "varied_output": "cap and topology", "ruling": "INFERENCE_FAILS"},
        {"id": "M08", "challenged_inference": "static phi zero fixes normal jet", "witness": "phi(n)=a*n for arbitrary a", "preserved_inputs": "odd phi and phi(0)=0", "varied_output": "normal derivative a", "ruling": "INFERENCE_FAILS"},
        {"id": "M09", "challenged_inference": "regular local metric erases degenerate closures", "witness": "P02 retains all fifteen zero-jet inertia strata", "preserved_inputs": "unconditional local parent atlas", "varied_output": "rank and signature closure", "ruling": "INFERENCE_FAILS"},
        {"id": "M10", "challenged_inference": "CSN selects physical scale or representative", "witness": "positive local rescalings remain an equivalence orbit", "preserved_inputs": "common-scale neutrality", "varied_output": "representative scale and curvature representative data", "ruling": "INFERENCE_FAILS"},
        {"id": "M11", "challenged_inference": "one local field branch is globally forced", "witness": "C01-C07 have different field content and all remain registered", "preserved_inputs": "current foundation census", "varied_output": "metric coframe projector constraint bridge or connection realization", "ruling": "INFERENCE_FAILS"},
        {"id": "M12", "challenged_inference": "global kinematics determine Xmax mass volume or bootstrap", "witness": "those quantities are undefined before physical representative and native matter-bearing solution", "preserved_inputs": "finite-cell ontology and local metric atlas", "varied_output": "downstream global outputs", "ruling": "NOT_YET_EVALUABLE"},
    ]

    moduli = [
        {"id": "U01", "object": "cover_chart_count_and_nerve", "kind": "DISCRETE_COMBINATORIAL", "status": "UNCOUNTED", "why_not_removed": "no cover supplied"},
        {"id": "U02", "object": "overlap_transition_labels", "kind": "DISCRETE_PLUS_CONTINUOUS", "status": "UNCOUNTED", "why_not_removed": "group known but assignment absent"},
        {"id": "U03", "object": "global_Z2_cocycle_class", "kind": "DISCRETE_TOPOLOGICAL", "status": "UNCOUNTED", "why_not_removed": "local parity is not global class"},
        {"id": "U04", "object": "transition_moduli_and_sign_classes", "kind": "CONTINUOUS_AND_DISCRETE", "status": "UNCOUNTED", "why_not_removed": "conjugacy only partly identifies them"},
        {"id": "U05", "object": "mixed_readout_mu", "kind": "CONTINUOUS_DIMENSIONLESS", "status": "UNCOUNTED", "why_not_removed": "mu=4 and mu=9 survive"},
        {"id": "U06", "object": "full_4x4_soldering", "kind": "FUNCTIONAL", "status": "UNCOUNTED", "why_not_removed": "constant 2x2 audit is bounded"},
        {"id": "U07", "object": "signed_phi_global_patching_and_zero_set", "kind": "FUNCTIONAL_TOPOLOGICAL", "status": "UNCOUNTED", "why_not_removed": "local signed field only"},
        {"id": "U08", "object": "angular_lift_periods_and_integral_basis", "kind": "DISCRETE_PLUS_CONTINUOUS", "status": "UNCOUNTED", "why_not_removed": "local lifts unselected"},
        {"id": "U09", "object": "caps_quotients_topology_and_no_cap", "kind": "TOPOLOGICAL", "status": "UNCOUNTED", "why_not_removed": "multiple witnesses and remainder survive"},
        {"id": "U10", "object": "boundary_polarization_and_corner_data", "kind": "FUNCTIONAL", "status": "UNCOUNTED", "why_not_removed": "scalar seal wire is incomplete"},
        {"id": "U11", "object": "normal_jets_and_degeneracy_loci", "kind": "FUNCTIONAL_STRATIFIED", "status": "UNCOUNTED", "why_not_removed": "normal phi jet free and other jets open"},
        {"id": "U12", "object": "connection_torsion_and_holonomy", "kind": "FUNCTIONAL_GEOMETRIC", "status": "UNCOUNTED", "why_not_removed": "C07 remains independent branch"},
        {"id": "U13", "object": "global_physical_representative_and_scale", "kind": "GLOBAL_CONTINUOUS", "status": "UNCOUNTED", "why_not_removed": "CSN does not choose a section"},
        {"id": "U14", "object": "Xmax", "kind": "GLOBAL_OUTPUT", "status": "NOT_EVALUABLE", "why_not_removed": "functional and complete cell absent"},
        {"id": "U15", "object": "mass_volume_density_bootstrap", "kind": "MATTER_BEARING_GLOBAL_OUTPUT", "status": "NOT_EVALUABLE", "why_not_removed": "native matter source and complete solution absent"},
    ]

    status = [
        {"id": "S01", "claim": "P02_P03_point_local_atlas", "status": "IMMUTABLE_INPUT", "scope_or_limit": "all 89 discrete strata remain accounted"},
        {"id": "S02", "claim": "assembly_axis_coverage", "status": "EXACT_PREREGISTERED_SCHEMA", "scope_or_limit": "12 of 12 axes represented"},
        {"id": "S03", "claim": "reciprocal_G_F_transition_algebra", "status": "DERIVED_EXACT_CONDITIONAL_CLASS", "scope_or_limit": "constant real two-channel representation"},
        {"id": "S04", "claim": "closed_identity_cocycle_reversal_parity", "status": "DERIVED_NECESSARY", "scope_or_limit": "odd F parity excluded; even parity not sufficient"},
        {"id": "S05", "claim": "actual_cover_and_global_cocycle", "status": "OPEN", "scope_or_limit": "local group does not create cover incidence or class"},
        {"id": "S06", "claim": "mixed_readout_family", "status": "DERIVED_CONDITIONAL_NONUNIQUE", "scope_or_limit": "mu=4 and mu=9 survive; full soldering unselected"},
        {"id": "S07", "claim": "full_four_dimensional_transition_law", "status": "OPEN_UNENUMERATED", "scope_or_limit": "constant 2x2 results cannot be promoted"},
        {"id": "S08", "claim": "static_phi_seal", "status": "PINNED_SCOPED", "scope_or_limit": "phi=0 delta_phi=0 normal derivative free"},
        {"id": "S09", "claim": "complete_seal_lift", "status": "OPEN", "scope_or_limit": "four registered local lifts remain unselected"},
        {"id": "S10", "claim": "boundary_variation_and_corner_polarization", "status": "OPEN", "scope_or_limit": "at least two inequivalent witnesses survive"},
        {"id": "S11", "claim": "global_topology", "status": "OPEN_NONUNIQUE", "scope_or_limit": "p=0,1,3,5 general no-cap and other remainder retained"},
        {"id": "S12", "claim": "topology_census_exhaustiveness", "status": "EXPLICITLY_NOT_CLAIMED", "scope_or_limit": "other unenumerated branch is mandatory"},
        {"id": "S13", "claim": "global_signed_phi", "status": "OPEN", "scope_or_limit": "existence zero set and sign holonomy unproved"},
        {"id": "S14", "claim": "degenerate_type_changing_or_singular_completion", "status": "OPEN_PRESERVED", "scope_or_limit": "regular inverse-metric tools do not erase it"},
        {"id": "S15", "claim": "global_connection_torsion_holonomy", "status": "OPEN_BRANCH", "scope_or_limit": "Levi-Civita and independent connection branches separate"},
        {"id": "S16", "claim": "global_physical_representative_scale_Xmax", "status": "OPEN_NOT_EVALUABLE", "scope_or_limit": "CSN and finite ontology do not select them"},
        {"id": "S17", "claim": "mass_volume_density_bootstrap", "status": "OPEN_NOT_EVALUABLE", "scope_or_limit": "complete native matter-bearing solution absent"},
        {"id": "S18", "claim": "local_C01_C07_global_extension", "status": "ALL_RETAINED_EXISTENCE_UNEVALUATED", "scope_or_limit": "zero branches globally proved or excluded"},
        {"id": "S19", "claim": "dynamics_action_equation_and_merit", "status": "NOT_LOADED", "scope_or_limit": "P04 was not launched"},
        {"id": "S20", "claim": "P03G_grade", "status": "LEAD_INDEPENDENT_REPLAY_FRESH_ADVERSARIAL_OPEN", "scope_or_limit": "bounded global assembly schema and exact existing compatibility; fresh-model review did not return"},
        {"id": "S21", "claim": "maximum_conclusion", "status": MAXIMUM, "scope_or_limit": "no existence uniqueness selection topology dynamics or bootstrap closure"},
    ]
    return {
        "ASSEMBLY_INPUT_REGISTRY.tsv": inputs,
        "GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv": schema,
        "COVER_AND_COCYCLE_BRANCHES.tsv": cocycles,
        "SEAL_LIFT_AND_TANGENT_BRANCHES.tsv": lifts,
        "TOPOLOGY_AND_COMPLETION_BRANCHES.tsv": topology,
        "LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv": gates,
        "GLOBAL_COUNTERMODEL_LEDGER.tsv": countermodels,
        "UNCOUNTED_GLOBAL_MODULI.tsv": moduli,
        "STATUS_LEDGER.tsv": status,
    }


FIELDS = {
    "ASSEMBLY_INPUT_REGISTRY.tsv": ["id", "object", "domain", "authority", "status", "source", "open_or_limit"],
    "GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv": ["axis_id", "object", "local_input", "required_global_data", "founded_compatibility", "status", "bounded_exhaustiveness"],
    "COVER_AND_COCYCLE_BRANCHES.tsv": ["id", "branch", "exact_condition", "assembly_status", "selected", "open_data"],
    "SEAL_LIFT_AND_TANGENT_BRANCHES.tsv": ["id", "object", "full_determinant", "coframe_fixed_dim", "coframe_antifixed_dim", "metric_even_dim", "metric_odd_dim", "compatibility", "status", "limit"],
    "TOPOLOGY_AND_COMPLETION_BRANCHES.tsv": ["id", "branch", "kind", "witness_parameter", "status", "selected", "limit"],
    "LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv": ["id", "local_branch", "branch_name", "required_closure", "currently_derived", "current_ruling", "missing_data"],
    "GLOBAL_COUNTERMODEL_LEDGER.tsv": ["id", "challenged_inference", "witness", "preserved_inputs", "varied_output", "ruling"],
    "UNCOUNTED_GLOBAL_MODULI.tsv": ["id", "object", "kind", "status", "why_not_removed"],
    "STATUS_LEDGER.tsv": ["id", "claim", "status", "scope_or_limit"],
}


def build_graph() -> dict[str, object]:
    nodes = [
        {"id": "LOCAL_ATLAS", "kind": "frozen_input"},
        {"id": "FIELD_REALIZATION", "kind": "branch_axis"},
        {"id": "COVER_NERVE", "kind": "open_global_data"},
        {"id": "GF_GROUP", "kind": "derived_local_algebra"},
        {"id": "TRANSITION_COCYCLE", "kind": "open_global_data"},
        {"id": "CSN_PATCHING", "kind": "equivalence_data"},
        {"id": "SIGNED_PHI", "kind": "open_global_data"},
        {"id": "FULL_COFRAME", "kind": "open_global_data"},
        {"id": "STATIC_SEAL_WIRE", "kind": "scoped_input"},
        {"id": "SEAL_LIFT", "kind": "open_global_data"},
        {"id": "BOUNDARY_TANGENT", "kind": "open_global_data"},
        {"id": "TOPOLOGY_CAPS", "kind": "open_global_data"},
        {"id": "DEGENERACY_COMPLETION", "kind": "open_global_data"},
        {"id": "CONNECTION_TORSION", "kind": "open_global_data"},
        {"id": "GLOBAL_KINEMATIC_OBJECT", "kind": "not_constructed"},
        {"id": "PHYSICAL_SCALE_XMAX", "kind": "downstream_open"},
        {"id": "MASS_BOOTSTRAP", "kind": "downstream_open"},
        {"id": "DYNAMICS", "kind": "excluded"},
    ]
    edges = [
        {"from": "LOCAL_ATLAS", "to": "FIELD_REALIZATION", "relation": "supplies_local_branches"},
        {"from": "GF_GROUP", "to": "TRANSITION_COCYCLE", "relation": "constrains_overlap_products"},
        {"from": "COVER_NERVE", "to": "TRANSITION_COCYCLE", "relation": "supplies_domain_and_incidence"},
        {"from": "FIELD_REALIZATION", "to": "FULL_COFRAME", "relation": "determines_required_field_join"},
        {"from": "CSN_PATCHING", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_representative_equivalence"},
        {"from": "SIGNED_PHI", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_field_patching"},
        {"from": "FULL_COFRAME", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_soldering"},
        {"from": "TRANSITION_COCYCLE", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_bundle_compatibility"},
        {"from": "STATIC_SEAL_WIRE", "to": "SEAL_LIFT", "relation": "constrains_but_does_not_select"},
        {"from": "SEAL_LIFT", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_boundary_identification"},
        {"from": "BOUNDARY_TANGENT", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_if_variation_is_later_loaded"},
        {"from": "TOPOLOGY_CAPS", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_global_completion"},
        {"from": "DEGENERACY_COMPLETION", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_closure_choice"},
        {"from": "CONNECTION_TORSION", "to": "GLOBAL_KINEMATIC_OBJECT", "relation": "required_on_C07_branch"},
        {"from": "GLOBAL_KINEMATIC_OBJECT", "to": "PHYSICAL_SCALE_XMAX", "relation": "necessary_not_sufficient"},
        {"from": "PHYSICAL_SCALE_XMAX", "to": "MASS_BOOTSTRAP", "relation": "downstream_join_still_requires_matter"},
    ]
    forbidden = [
        {"from": "GF_GROUP", "to": "COVER_NERVE", "reason": "transition algebra does not create cover"},
        {"from": "STATIC_SEAL_WIRE", "to": "BOUNDARY_TANGENT", "reason": "scalar wire does not select a complete polarization"},
        {"from": "CSN_PATCHING", "to": "PHYSICAL_SCALE_XMAX", "reason": "equivalence does not choose a section"},
        {"from": "LOCAL_ATLAS", "to": "DYNAMICS", "reason": "configuration census does not select dynamics"},
        {"from": "GLOBAL_KINEMATIC_OBJECT", "to": "MASS_BOOTSTRAP", "reason": "geometry alone does not yet define native matter"},
    ]
    return {"schema": "udt-p03g-global-assembly-dependency-graph-1.0", "nodes": nodes, "edges": edges, "forbidden_edges": forbidden}


def exact_algebra(checks: dict[str, str]) -> dict[str, object]:
    a, b, c, d = sp.symbols("a b c d", real=True, nonzero=True)

    def G(x):
        return sp.diag(x, 1 / x)

    def F(x):
        return sp.Matrix([[0, x], [1 / x, 0]])

    require("G_group_law", sp.simplify(G(a) * G(d) - G(a * d)) == sp.zeros(2), checks)
    require("F_involution", sp.simplify(F(b) ** 2 - sp.eye(2)) == sp.zeros(2), checks)
    require("F_F_preserving", sp.simplify(F(b) * F(c) - G(b / c)) == sp.zeros(2), checks)
    require("G_F_inverting", sp.simplify(G(a) * F(b) - F(a * b)) == sp.zeros(2), checks)
    require("F_G_inverting", sp.simplify(F(b) * G(a) - F(b / a)) == sp.zeros(2), checks)
    require("three_F_not_identity", (F(b) * F(c) * F(d))[0, 0] == 0 and (F(b) * F(c) * F(d))[0, 1] != 0, checks)
    require("FFG_cocycle_witness", sp.simplify(F(b) * F(c) * G(c / b) - sp.eye(2)) == sp.zeros(2), checks)
    require("F_conjugacy", sp.simplify(G(a) * F(b) * G(a).inv() - F(a**2 * b)) == sp.zeros(2), checks)
    tangent = {}
    for label, (fixed, anti) in {"plus_identity": (3, 1), "minus_identity": (1, 3), "reflection": (2, 2)}.items():
        tangent[label] = {"fixed": fixed, "anti": anti, "metric_even": fixed * (fixed + 1) // 2 + anti * (anti + 1) // 2, "metric_odd": fixed * anti}
    require("tangent_dimensions", tangent == {"plus_identity": {"fixed": 3, "anti": 1, "metric_even": 7, "metric_odd": 3}, "minus_identity": {"fixed": 1, "anti": 3, "metric_even": 7, "metric_odd": 3}, "reflection": {"fixed": 2, "anti": 2, "metric_even": 6, "metric_odd": 4}}, checks)
    n, slope = sp.symbols("n slope", real=True)
    phi = slope * n
    require("free_seal_normal_jet", phi.subs(n, 0) == 0 and sp.diff(phi, n) == slope, checks)
    return {"group": "Z2_GRADED_G_F", "tangent_dimensions": tangent, "seal_family": "phi(n)=slope*n"}


def main() -> None:
    checks: dict[str, str] = {}
    for label, (relative, expected) in PARENT_MANIFESTS.items():
        require(f"parent_{label}_hash", digest(ROOT / relative) == expected, checks)

    data = rows()
    for filename, table in data.items():
        write_tsv(filename, FIELDS[filename], table)

    require("axis_count", len(data["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"]) == 12, checks)
    require("axis_identity", {row["axis_id"] for row in data["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"]} == {f"A{i:02d}" for i in range(1, 13)}, checks)
    require("all_local_branches_retained", {row["local_branch"] for row in data["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"]} == {f"C{i:02d}" for i in range(1, 8)} and all(row["currently_derived"] == "NO" for row in data["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"]), checks)
    require("topology_remainder", sum(row["kind"] == "OTHER_UNENUMERATED" for row in data["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"]) >= 2, checks)
    require("zero_selected_branches", not any(row.get("selected") == "YES" for table in data.values() for row in table), checks)
    require("dynamics_not_loaded", next(row for row in data["STATUS_LEDGER.tsv"] if row["id"] == "S19")["status"] == "NOT_LOADED", checks)
    algebra = exact_algebra(checks)

    graph = build_graph()
    node_ids = {node["id"] for node in graph["nodes"]}
    require("graph_endpoints", all(edge["from"] in node_ids and edge["to"] in node_ids for edge in graph["edges"]), checks)
    require("forbidden_not_realized", not ({(edge["from"], edge["to"]) for edge in graph["edges"]} & {(edge["from"], edge["to"]) for edge in graph["forbidden_edges"]}), checks)
    (HERE / "ASSEMBLY_DEPENDENCY_GRAPH.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lineage = []
    for index, (label, (relative, expected)) in enumerate(PARENT_MANIFESTS.items(), 1):
        lineage.append({"id": f"SRC{index:02d}", "role": label, "path": relative, "sha256": expected, "use": "immutable parent evidence"})
    write_tsv("SOURCE_LINEAGE.tsv", ["id", "role", "path", "sha256", "use"], lineage)

    counts = {
        "assembly_inputs": len(data["ASSEMBLY_INPUT_REGISTRY.tsv"]),
        "preregistered_axes": len(data["GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"]),
        "cocycle_branches": len(data["COVER_AND_COCYCLE_BRANCHES.tsv"]),
        "seal_lift_and_tangent_branches": len(data["SEAL_LIFT_AND_TANGENT_BRANCHES.tsv"]),
        "topology_and_completion_branches": len(data["TOPOLOGY_AND_COMPLETION_BRANCHES.tsv"]),
        "local_realization_branches_retained": len(data["LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv"]),
        "countermodels": len(data["GLOBAL_COUNTERMODEL_LEDGER.tsv"]),
        "uncounted_global_moduli": len(data["UNCOUNTED_GLOBAL_MODULI.tsv"]),
        "globally_proved_local_branches": 0,
        "globally_excluded_local_branches": 0,
        "selected_global_branches": 0,
    }
    table_hashes = {name: digest(HERE / name) for name in data}
    result = {
        "schema": "udt-p03g-global-kinematic-assembly-atlas-1.0",
        "status": "PASS",
        "evidence_grade": "LEAD_INDEPENDENT_REPLAY_FRESH_ADVERSARIAL_OPEN",
        "maximum_conclusion": MAXIMUM,
        "question_mode": "METRIC_LED_OBSERVING_GLOBAL_ASSEMBLY",
        "counts": counts,
        "exact_algebra": algebra,
        "compatibility_ruling": {
            "reciprocal_transition_algebra": "DERIVED_EXACT_IN_BOUNDED_TWO_CHANNEL_CLASS",
            "actual_cover_and_global_cocycle": "OPEN",
            "complete_seal_lift": "OPEN",
            "global_topology": "OPEN_NONUNIQUE_AND_NONEXHAUSTIVE",
            "global_signed_phi": "OPEN",
            "all_C01_C07_local_branches": "RETAINED_GLOBAL_EXISTENCE_UNEVALUATED",
            "P04_dynamics_lane": "NOT_SELECTED_OR_LAUNCHED",
        },
        "parent_manifest_sha256": {label: expected for label, (_, expected) in PARENT_MANIFESTS.items()},
        "table_sha256": table_hashes,
        "check_count": len(checks),
        "checks": checks,
        "scope": {"CPU_only": True, "GPU_used": False, "ODE_or_PDE_run": False, "action_selected": False, "equation_selected": False, "topology_selected": False, "global_solution_claimed": False, "P04_launched": False, "P11_launched": False},
    }
    (HERE / "ASSEMBLY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    transcript = [
        "P03G_GLOBAL_KINEMATIC_ASSEMBLY=PASS",
        f"checks={len(checks)}",
        "axes=12/12",
        "local_branches_retained=7/7",
        "global_branches_selected=0",
        "globally_proved_local_branches=0",
        "globally_excluded_local_branches=0",
        "reciprocal_group=Z2_GRADED_G_F",
        "odd_reversal_identity_cocycles=EXCLUDED",
        "cover_global_cocycle_seal_lift_topology=OPEN",
        "dynamics=NOT_LOADED",
        f"maximum_conclusion={MAXIMUM}",
    ]
    text = "\n".join(transcript) + "\n"
    (HERE / "ASSEMBLY_TRANSCRIPT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
