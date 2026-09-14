"""Read-only byte correspondence checks for the scoped source challenge."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "udt_positional_joint_compatibility_2026-09-14"
original = json.loads((PACKAGE / "SOURCE_PINS.json").read_text())
extra = [
    "PROVENANCE.md",
    "UDT_RESEARCH_ROADMAP.md",
    "udt_joint_observer_relation_scope_correction_2026-09-13/WORK_ORDER.md",
    "udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/PREREGISTRATION.md",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/PREREGISTRATION.md",
    "udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/EXACT_DERIVATION.md",
    "udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/EXACT_DERIVATION.md",
    "udt_g274_projective_pair_position_network_descent_2026-08-26/EXACT_DERIVATION.md",
    "udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/EXACT_DERIVATION.md",
    "udt_g255_g165_g254_lost_closure_recovery_audit_2026-08-24/AUDIT_REPORT.md",
    "udt_g231_cartan_regional_realization_bridge_2026-08-23/AUDIT_REPORT.md",
    "udt_g217_founded_depth_event_pair_first_jet_ownership_2026-08-22/AUDIT_REPORT.md",
    "udt_g273_projective_pair_distance_foundational_ownership_2026-08-26/AUDIT_REPORT.md",
    "udt_g273_projective_pair_distance_foundational_ownership_2026-08-26/SOURCE_PROPOSITION_LEDGER.tsv",
    "udt_g273_projective_pair_distance_foundational_ownership_2026-08-26/SOURCE_MANIFEST.tsv",
    "udt_g272_complete_relation_rapidity_distance_ownership_2026-08-26/EXACT_DERIVATION.md",
    "udt_g271_primary_metric_null_screen_first_jet_interlock_2026-08-26/EXACT_DERIVATION.md",
    "udt_g288_smooth_center_micro_regime_jet_interlock_2026-08-28/AUDIT_REPORT.md",
]
current = {
    name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    for name in dict.fromkeys([*original, *extra])
}
failures = [name for name, expected in original.items() if current[name] != expected]
result = {
    "kind": "byte_correspondence_and_exposure_inventory_not_scientific_verification",
    "original_pins_checked": len(original),
    "original_pin_mismatches": failures,
    "extra_sources": len(extra),
    "source_sha256": current,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(bool(failures))
