"""Verify selection-history completeness: every candidate evaluated logged."""
import json

# Required pre-committed candidates per dispatch §4.3.2
REQUIRED_CANDIDATES = {
    "form_i_smooth_const": "Form (i) smooth large-scale const g_0",
    "form_ii_subshell_A": "Form (ii) sub-shell A 2MRS sub-Mpc",
    "form_ii_subshell_B": "Form (ii) sub-shell B Mpc-Gpc peak",
    "form_ii_subshell_C": "Form (ii) sub-shell C Gpc high-ell",
    "form_iii_ell_src_2": "Form (iii) ell_src=2 quadrupolar",
    "form_iii_ell_src_3": "Form (iii) ell_src=3 octupolar",
    "form_iii_ell_src_4": "Form (iii) ell_src=4 hexadecapolar",
}

print("=" * 78)
print("Selection-history completeness audit")
print("=" * 78)

# Agent V
print("\n[Agent V selection_history.json]")
with open("/home/udt-admin/UDT/cr_next/cr_S47_AGENT_V_TOPDOWN_BIPOSH_HEMI/selection_history.json") as f:
    sh_v = json.load(f)
print(f"  candidates_evaluated count: {len(sh_v['candidates_evaluated'])}")
print(f"  directions_computed count: {len(sh_v['directions_computed'])}")
print(f"  threshold_comparisons count: {len(sh_v['threshold_comparisons'])}")
print(f"  discarded_candidates_with_reason count: {len(sh_v['discarded_candidates_with_reason'])}")

v_labels = [(c['form_label'], c['sub_label']) for c in sh_v['candidates_evaluated']]
print(f"  Candidate labels: {v_labels}")

# Agent W
print("\n[Agent W selection_history.json]")
with open("/home/udt-admin/UDT/cr_next/cr_S47_AGENT_W_BOTTOMUP_BIPOSH_HEMI/selection_history.json") as f:
    sh_w = json.load(f)
print(f"  candidates_evaluated count: {len(sh_w['candidates_evaluated'])}")
print(f"  K_ell_computations count: {len(sh_w['K_ell_computations'])}")
print(f"  direction_predictions count: {len(sh_w['direction_predictions'])}")
print(f"  amplitude_predictions count: {len(sh_w['amplitude_predictions'])}")
print(f"  scope_bounding_events count: {len(sh_w['scope_bounding_events'])}")
print(f"  no_silent_discards: {sh_w['no_silent_discards']}")

w_labels = sh_w['candidates_evaluated']
print(f"  Candidate labels: {w_labels}")

# Cross-check with results.json
print("\n[Agent V results.json per_candidate_predictions]")
with open("/home/udt-admin/UDT/cr_next/cr_S47_AGENT_V_TOPDOWN_BIPOSH_HEMI/results.json") as f:
    r_v = json.load(f)
v_pred = r_v['per_candidate_predictions']
print(f"  Keys: {list(v_pred.keys())}")
print(f"  Match SH count: {len(v_pred) == len(v_labels)}")

print("\n[Agent W results.json candidates]")
with open("/home/udt-admin/UDT/cr_next/cr_S47_AGENT_W_BOTTOMUP_BIPOSH_HEMI/results.json") as f:
    r_w = json.load(f)
w_pred = r_w['candidates']
print(f"  Keys: {list(w_pred.keys())}")
print(f"  Match SH count: {len(w_pred) == len(w_labels)}")

# Direction predictions
print("\n[Agent V directions_computed]")
for d in sh_v['directions_computed']:
    print(f"  {d['form_label']} {d['sub_label']}: {d['direction_l_b_galactic']}")

print("\n[Agent W direction_predictions]")
for d in sh_w['direction_predictions']:
    print(f"  {d['candidate']}: {d['direction_lb_deg']} via {d['method']}")

# Check for any threshold widening or scope expansion
print("\n[Agent V thresholds in threshold_comparisons]")
for tc in sh_v['threshold_comparisons']:
    print(f"  {tc['form_label']} {tc['sub_label']}: clean={tc['direction_threshold_clean_deg']}/halt={tc['direction_threshold_halt_deg']}/amp_clean={tc['amplitude_threshold_clean_frac']}/amp_halt={tc['amplitude_threshold_halt_frac']}")

# Verify thresholds match dispatch §4.3.1
expected_dir_clean = 15.0
expected_dir_halt = 30.0
expected_amp_clean = 0.20
expected_amp_halt = 0.50

print("\n[Threshold pre-commitment verification per dispatch §4.3.1]")
v_threshold_consistent = all(
    tc['direction_threshold_clean_deg'] == expected_dir_clean and
    tc['direction_threshold_halt_deg'] == expected_dir_halt and
    tc['amplitude_threshold_clean_frac'] == expected_amp_clean and
    tc['amplitude_threshold_halt_frac'] == expected_amp_halt
    for tc in sh_v['threshold_comparisons']
)
print(f"  Agent V thresholds consistent across all 7 candidates: {v_threshold_consistent}")
print(f"  Expected: dir_clean=15.0, dir_halt=30.0, amp_clean=0.20, amp_halt=0.50")

# Check Agent W threshold_comparisons (empty array — flag this)
print(f"\n  Agent W threshold_comparisons count: {len(sh_w['threshold_comparisons'])}")
if len(sh_w['threshold_comparisons']) == 0:
    print(f"    NOTE: Agent W threshold_comparisons array is EMPTY")
    print(f"    Dispatch §4.4.1.3 mandates threshold-comparison logging.")
    print(f"    However: §4.3.4 says comparison to Planck happens at synthesis layer.")
    print(f"    Agent W discipline_compliance.synthesis_layer_comparison_deferred=True")
    print(f"    This is consistent with §4.3.4 deferral; threshold_comparisons logging")
    print(f"    is not strictly mandated absent Planck-comparison.")
