#!/usr/bin/env python3
"""Build the preregistered native stability configuration-space audit."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = "095a2a5e093f21bfd68939f5874b359868a109d3"
OUTCOME = "NATIVE_OFFSHELL_PARENT_ARENA_DERIVED__REALIZATION_VARIATION_OPEN"


def git(*args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True
    )
    return result.stdout if binary else result.stdout.decode("utf-8")


def write_tsv(name: str, header: list[str], rows: list[list[str]]) -> None:
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def source_tree() -> list[dict[str, object]]:
    raw = git("ls-tree", "-r", "-z", "--long", BASE, binary=True)
    entries: list[tuple[str, str, int]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        meta, path_raw = item.split(b"\t", 1)
        _mode, kind, blob, size = meta.decode().split()
        if kind != "blob":
            raise RuntimeError(f"non-blob tracked object is outside this audit: {path_raw!r}")
        entries.append((path_raw.decode("utf-8"), blob, int(size)))

    archive = git("archive", "--format=tar", BASE, binary=True)
    contents: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar.getmembers():
            if member.isfile():
                stream = tar.extractfile(member)
                if stream is not None:
                    contents[member.name] = stream.read()

    rows: list[dict[str, object]] = []
    for path, blob, size in entries:
        data = contents.get(path)
        if data is None:
            data = git("cat-file", "blob", blob, binary=True)
        if len(data) != size:
            raise RuntimeError(f"byte-count mismatch for {path}")
        rows.append(
            {
                "path": path,
                "blob": blob,
                "bytes": size,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return rows


AUTHORITIES = [
    ["A01", "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT", "Founded phi and reciprocal clock/ruler action are DERIVED; complete action, source, boundary, dynamics and mass remain OPEN.", "CONTROLS"],
    ["A02", "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/AUDIT_REPORT.md", "DERIVED_TYPE_CLASSIFICATION", "Complete metric plus angular/mixing content is the physical geometric arena; the final physical variation domain and boundary remain OPEN.", "SUPPORTS_OFFSHELL_PARENT"],
    ["A03", "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md", "DERIVED_WITH_OPEN_EXTENSION", "Founded phi is derived while complete four-dimensional extension selection remains OPEN.", "SUPPORTS_OFFSHELL_PARENT"],
    ["A04", "udt_complete_coframe_native_selector_audit_2026-07-26/AUDIT_REPORT.md", "OPEN_SELECTOR", "Registered premises do not select the complete coframe extension or its physical tangent domain.", "BLOCKS_REALIZED_PARENT"],
    ["A05", "udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md", "DERIVED_EXISTENCE_CLASS", "Complete regular reciprocal configurations exist off shell; no native equation selects a realized member.", "SUPPORTS_OFFSHELL_PARENT"],
    ["A06", "udt_global_functional_dof_constraint_rank_audit_2026-07-26/CORRECTION_LAYER.md", "CORRECTION", "Generic arena amplitudes are not a native field or propagating-mode count; founded phi is not an added independent field.", "CONTROLS"],
    ["A07", "udt_p4_bookkeeping_forcing_2026-07-29/AUDIT_REPORT.md", "CONDITIONAL_FORK", "Constant-moduli and field-moduli P4 domains are distinct registered conditional census choices.", "SEPARATE_CONDITIONAL_SPACE"],
    ["A08", "udt_p4_bookkeeping_forcing_2026-07-29/EXACT_DERIVATION.md", "EXACT_PULLBACK", "The constant-section pullback of the field response gives integrated constant rows; the reverse stationary implication is not derived.", "RELATION_ONLY"],
    ["A09", "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md", "CONDITIONAL", "Field-moduli response is registered as a permitted class, not selected as the native branch.", "SEPARATE_CONDITIONAL_SPACE"],
    ["A10", "udt_p4_timelive_stage_T2_2026-07-31/AUDIT_REPORT.md", "FORMAL_MODULE", "The time-live object is a formal typed module without a selected native response or common realized witness.", "NO_REALIZED_EMBEDDING"],
    ["A11", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", "FORMAL_MODULE", "The angular-live object is a formal typed module without a selected common on-shell realization.", "NO_REALIZED_EMBEDDING"],
    ["A12", "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "CONDITIONAL", "The implementation is full 3D Hopf-capable, but its round S2 carrier, L2+L4 functional and finite-box boundary do not derive from the metric arena.", "SEPARATE_CONDITIONAL_SPACE"],
    ["A13", "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md", "OPEN", "Registered modules do not supply one nonzero common live realization or its native equation and boundary.", "BLOCKS_REALIZED_PARENT"],
    ["A14", "udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md", "OPEN", "No registered native certificate closes the family relations into one owned realized space.", "BLOCKS_PERSISTENCE"],
    ["A15", "udt_bootstrap_closure_ownership_audit_2026-08-01/AUDIT_REPORT.md", "WORKING_POSIT", "Bootstrap has a coherent type schema but no derived membership, return or closure operation.", "NO_RETURN_MAP"],
    ["A16", "udt_whole_configuration_reciprocity_audit_2026-08-01/AUDIT_REPORT.md", "DERIVED_NATURALITY", "Whole-configuration Reciprocity constrains naturality/equivariance; it is not a selector, flow or bootstrap return.", "CONSTRAINT_NOT_DYNAMICS"],
    ["A17", "udt_global_local_self_consistency_premise_audit_2026-08-01/AUDIT_REPORT.md", "DISTINCT_WORKING_POSIT", "Global-local self-consistency is coherent as a new premise but is not derived by existing foundations.", "NO_RETURN_MAP"],
    ["A18", "udt_stability_derivation_closure_sweep_2026-08-01/AUDIT_REPORT.md", "BOUNDED_NEGATIVE", "Fifteen objects across five active families (F01, F02, F04, F05, F07) do not presently close every required upstream derivation.", "BLOCKS_GLOBAL_BASIN"],
    ["A19", "udt_stability_family_ontology_audit_2026-08-01/AUDIT_REPORT.md", "ONTOLOGY_CORRECTION", "F01-F07 are evidence buckets rather than a native partition of solution space or particle species.", "BLOCKS_GLOBAL_BASIN"],
    ["A20", "udt_stability_family_survivor_map_2026-08-01/AUDIT_REPORT.md", "WORKING_MAP", "F01, F02 and F04 use different objects and premise stacks, and no common metric-native stability operator is supplied.", "BLOCKS_GLOBAL_BASIN"],
    ["A21", "PONDER_MATH_ELEGANCE_2026-07-31.md", "WORKING_LEAD_ONLY", "Taxonomy times stable-basin is an interpretation to test after the native landscape is typed, never affirmative authority.", "INTERPRETATION_ONLY"],
]


CONFIG_OBJECTS = [
    ["O01", "founded_reciprocal_pair", "reciprocal clock/ruler group action with founded phi", "NATIVE_DERIVED", "yes", "no independent delta-phi field"],
    ["O02", "complete_metric_arena", "complete metric retaining angular and mixing slots modulo presentation gauge", "NATIVE_OFFSHELL_ARENA_DERIVED_AS_TYPE", "yes", "extension and realized member unselected"],
    ["O03", "complete_coframe_existence_class", "regular reciprocal R x S3 configurations for admitted phi and lambda", "DERIVED_EXISTENCE_CLASS", "yes", "example completion; not a universal selected branch"],
    ["O04", "presentation_gauge", "chart, coframe Lorentz and screen-orientation descriptions", "DERIVED_GAUGE_LAYER", "yes", "quotient directions, not physical variations"],
    ["O05", "relational_query_layer", "observer/ruler pairs, events and paths", "DERIVED_TYPED_ARGUMENTS", "yes", "queries, not missing dynamical fields"],
    ["O06", "completion_sector_layer", "topology, quotient, seam and cap labels", "DERIVED_AS_SECTOR_TYPE", "yes", "transition/gluing and realized completion open"],
    ["O07", "p4_constant_moduli", "seven constant P4 bookkeeping amplitudes", "CONDITIONAL_PERMITTED", "conditional_only", "conditional response domain on registered BASE/positive-triangular coframe arena"],
    ["O08", "p4_field_moduli", "seven field-valued P4 bookkeeping amplitudes", "CONDITIONAL_PERMITTED", "conditional_only", "conditional response domain on registered BASE/positive-triangular coframe arena"],
    ["O09", "time_live_module", "registered time-live formal module", "FORMAL_TYPED_ONLY", "no", "native response and common realization open"],
    ["O10", "angular_live_module", "registered angular-live formal module", "FORMAL_TYPED_ONLY", "no", "native response and common realization open"],
    ["O11", "hopfion_model", "round S2 carrier with conditional L2+L4 and finite box", "CONDITIONAL_CARRIER_MODEL", "no", "no derived carrier map from founded metric"],
    ["O12", "bootstrap_schema", "global-local mutual-determination type diagram", "WORKING_POSIT", "no", "membership and return operation open"],
    ["O13", "stability_evidence_families", "F01-F07 operational evidence buckets", "WORKING_CATALOGUE", "no", "not solution partition or species"],
    ["O14", "formal_family_coproduct", "disjoint union of conditional family configuration sets", "BOOKKEEPING_CONTROL_ONLY", "no", "not selected by metric"],
]


RELATIONS = [
    ["R01", "founded_reciprocal_pair", "complete_metric_arena", "INCLUDED_AS_REQUIRED_STRUCTURE", "DERIVED", "The complete arena must realize the founded pair."],
    ["R02", "complete_coframe_existence_class", "complete_metric_arena", "SUBCLASS_WITNESS", "DERIVED_AS_EXISTENCE", "Nonempty off-shell witness class, not an on-shell selector."],
    ["R03", "presentation_gauge", "complete_metric_arena", "QUOTIENT_PRESENTATION", "DERIVED", "Gauge descriptions do not add physical configurations."],
    ["R04", "relational_query_layer", "complete_metric_arena", "ARGUMENT_OVER_ARENA", "DERIVED_TYPED", "Changing a query is not an off-shell field variation."],
    ["R05", "completion_sector_layer", "complete_metric_arena", "SECTOR_INDEX_WITHOUT_GLUING", "OPEN", "Labels exist; native transitions and realized completion do not."],
    ["R06", "p4_constant_moduli", "p4_field_moduli", "CONSTANT_SECTION_EMBEDDING", "EXACT_CONDITIONAL", "A constant field embeds into the field domain."],
    ["R07", "p4_field_moduli_response", "p4_constant_moduli_response", "PULLBACK_GIVES_INTEGRATED_ROWS", "EXACT_CONDITIONAL", "Pullback is one-way and does not equate stationary sets."],
    ["R08", "p4_constant_moduli_stationary_set", "p4_field_moduli_stationary_set", "NO_EQUIVALENCE_DERIVED", "OPEN", "Integrated zero need not imply pointwise zero."],
    ["R09", "time_live_module", "p4_field_moduli", "FORMAL_EXTENSION_RELATION", "FORMAL_ONLY", "No selected response or nonzero common witness."],
    ["R10", "angular_live_module", "p4_field_moduli", "FORMAL_EXTENSION_RELATION", "FORMAL_ONLY", "No selected response or nonzero common witness."],
    ["R11", "time_live_module", "angular_live_module", "COMMON_REALIZED_INTERSECTION", "OPEN", "Typing does not prove on-shell coexistence."],
    ["R12", "hopfion_model", "complete_metric_arena", "CARRIER_EMBEDDING", "OPEN", "The conditional celestial fiber is not a selected round target section."],
    ["R13", "bootstrap_schema", "complete_metric_arena", "MEMBERSHIP_MAP", "OPEN", "No native rule maps local configurations into the bootstrap domain."],
    ["R14", "bootstrap_schema", "complete_metric_arena", "RETURN_MAP", "OPEN", "No native global-to-local closure operation is registered."],
    ["R15", "whole_configuration_reciprocity", "complete_metric_arena", "NATURALITY_CONSTRAINT", "DERIVED_IN_SCOPE", "Equivariance constrains a law but does not supply it."],
    ["R16", "stability_evidence_families", "complete_metric_arena", "NATIVE_PARTITION", "NOT_DERIVED", "F01-F07 are operational buckets."],
    ["R17", "formal_family_coproduct", "complete_metric_arena", "NATIVE_PARENT_SELECTION", "NOT_DERIVED", "Every finite family admits a formal union; this is vacuous."],
    ["R18", "hopfion_model", "stability_evidence_families", "CONDITIONAL_REALIZED_ROW", "CONDITIONAL", "Only within carrier/action/boundary premises."],
    ["R19", "p4_constant_moduli", "complete_metric_arena", "CONDITIONAL_SUBDOMAIN", "CONDITIONAL", "Registered constant census on the BASE/positive-triangular coframe arena; not natively selected."],
    ["R20", "p4_field_moduli", "complete_metric_arena", "CONDITIONAL_SUBDOMAIN", "CONDITIONAL", "Registered field census on the BASE/positive-triangular coframe arena; typed not exhausted and not natively selected."],
]


GATES = [
    ["native_geometric_arena", "PASS_TYPED", "PASS_OFFSHELL", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "PASS_NATURALITY", "OPEN", "NO"],
    ["complete_RxS3_witness_class", "PASS_CONDITIONAL_BRANCH", "PASS_OFFSHELL", "OPEN", "OPEN", "NONE", "CONDITIONAL_DOMAIN", "OPEN", "STATIONARY_WITNESS_ONLY", "CONDITIONAL_COMPLETION", "NONE", "PASS_NATURALITY", "OPEN", "NO"],
    ["p4_constant_moduli", "CONDITIONAL", "CONDITIONAL", "CONSTANTS_CHOSEN", "FINITE_R7", "CONDITIONAL_RESPONSE", "CONDITIONAL", "CONDITIONAL_ONLY", "STATIONARY_ONLY", "CONDITIONAL", "NONE", "MUST_RESPECT", "NONE", "NO_GLOBAL_BASIN"],
    ["p4_field_moduli", "CONDITIONAL", "CONDITIONAL", "FIELDS_CHOSEN", "FUNCTION_SPACE_OPEN", "CONDITIONAL_RESPONSE", "CONDITIONAL", "CONDITIONAL_ONLY", "FORMAL_LIVE_MODULES", "CONDITIONAL", "NONE", "MUST_RESPECT", "NONE", "NO_GLOBAL_BASIN"],
    ["time_angular_joint", "FORMAL_TYPED", "FORMAL_TYPED", "OPEN", "OPEN", "OPEN", "OPEN", "NO_NONZERO_WITNESS", "FORMAL_ONLY", "OPEN", "NONE", "OPEN", "NONE", "NO"],
    ["conditional_hopfion", "CONDITIONAL", "CONDITIONAL", "CARRIER_FIELDS_CHOSEN", "FINITE_BOX_FUNCTION_SPACE", "CONDITIONAL_L2_PLUS_L4_AND_CERTIFICATE", "CHOSE_FINITE_BOX", "OBSERVED_CONDITIONAL_SOLUTIONS", "SEPARATE_MODEL", "HOPF_SECTORS_CONDITIONAL", "OPEN_CARRIER_MAP", "NOT_AUDITED_AS_NATIVE", "NONE", "YES_CONDITIONAL_ONLY"],
    ["bootstrap_global_local", "WORKING_POSIT", "WORKING_POSIT", "OPEN", "OPEN", "OPEN_RETURN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "MUST_RESPECT", "MISSING", "NO"],
    ["F01_F07_catalogue", "WORKING_BUCKETS", "MULTIPLE", "MULTIPLE_CONDITIONAL", "MULTIPLE", "MULTIPLE_OR_MISSING", "MULTIPLE", "ZERO_NATIVE_REALIZED", "NO_COMMON_EMBEDDING", "MULTIPLE", "OPEN", "MUST_RESPECT", "MISSING", "NO_GLOBAL_BASIN"],
]


PREMISES = [
    ["P01", "Founded reciprocal phi and clock/ruler action", "DERIVED", "CARRIED_UNCHANGED"],
    ["P02", "Observed c_E and G_obs", "OBSERVED", "CALIBRATION_ONLY"],
    ["P03", "Four-dimensional complete extension", "OPEN", "NOT_PROMOTED"],
    ["P04", "Constants versus fields census", "OPEN", "NOT_PROMOTED"],
    ["P05", "P4 response families", "CONDITIONAL", "NOT_SELECTED"],
    ["P06", "Round S2 carrier", "POSIT", "NOT_PROMOTED"],
    ["P07", "L2+L4 Hopfion functional", "CONDITIONAL", "NOT_PROMOTED"],
    ["P08", "Computational Hopfion boundary", "CHOSE", "NOT_PROMOTED"],
    ["P09", "Finite-cell ownership split", "MIXED_PROGRAM_STAMPS", "CARRIED_EXACTLY"],
    ["P10", "Observer Reciprocity", "DERIVED_NATURALITY_IN_SCOPE", "NOT_USED_AS_DYNAMICS"],
    ["P11", "Bootstrap mutual determination", "WORKING_POSIT", "NO_OPERATION_INVENTED"],
    ["P12", "Complete response/action/source/boundary/time/mass", "OPEN", "NOT_PROMOTED"],
    ["P13", "Taxonomy times stable-basin interpretation", "WORKING_LEAD", "INTERPRETATION_ONLY"],
]


CONTROLS = [
    ["C01", "constant-section_pullback", "C1=R2; C0=R; i(a)=(a,a); alpha1=dx-dy; alpha0=i*alpha1=da-da=0", "alpha1=0 implies alpha0=0; alpha0=0 does not imply alpha1=0", "PASS"],
    ["C02", "formal_disjoint_union", "A={0}; B={0}; tagged union={(A,0),(B,0)}", "exists for arbitrary sets and therefore carries no selector content", "PASS"],
    ["C03", "same_set_different_flows", "X=R; V1=x^2; V2=(x^2-1)^2", "same X has one versus two stable minima", "PASS"],
    ["C04", "nonempty_modules_empty_live_join", "M1={0,1}; M2={0,2}", "both nonempty; common set is {0}; nonzero common live set is empty", "PASS"],
    ["C05", "fiber_labels_without_gluing", "F0={a}; F1={b}; labels={0,1}", "labels index fibers but specify no transition map between a and b", "PASS"],
]


def main() -> None:
    sources = source_tree()
    by_path = {str(row["path"]): row for row in sources}
    missing = [row[1] for row in AUTHORITIES if row[1] not in by_path]
    if missing:
        raise RuntimeError(f"authority sources absent from base: {missing}")

    write_tsv(
        "SOURCE_INVENTORY.tsv",
        ["path", "git_blob", "bytes", "sha256"],
        [[str(r["path"]), str(r["blob"]), str(r["bytes"]), str(r["sha256"])] for r in sources],
    )
    (OUT / "SOURCE_MANIFEST.sha256").write_text(
        "".join(f"{r['sha256']}  {r['path']}\n" for r in sources), encoding="utf-8"
    )
    write_tsv(
        "SOURCE_AUTHORITY_LEDGER.tsv",
        ["id", "path", "registered_status", "load_bearing_statement", "audit_effect", "git_blob", "sha256"],
        [row + [str(by_path[row[1]]["blob"]), str(by_path[row[1]]["sha256"])] for row in AUTHORITIES],
    )
    write_tsv("CONFIGURATION_OBJECT_LEDGER.tsv", ["id", "object", "definition", "status", "belongs_to_native_parent_type", "restriction"], CONFIG_OBJECTS)
    write_tsv("PARENT_RELATION_MATRIX.tsv", ["id", "source_object", "target_object", "relation", "status", "exact_scope"], RELATIONS)
    write_tsv(
        "VARIATION_AND_BASIN_GATE.tsv",
        ["arena", "configuration_object", "offshell_arena", "selected_varied_dofs", "tangent_domain", "response_flow_certificate", "boundary_domain", "onshell_nonempty", "stationary_time_angular_embedding", "completion_gluing", "hopfion_relation", "reciprocity", "bootstrap_return", "stable_basin_well_posed"],
        GATES,
    )
    write_tsv("PREMISE_LEDGER.tsv", ["id", "premise", "entry_status", "audit_treatment"], PREMISES)
    write_tsv("EXACT_CONTROL_LEDGER.tsv", ["id", "control", "construction", "result", "status"], CONTROLS)

    result = {
        "audit": "native_stability_configuration_space",
        "date": "2026-08-01",
        "base_commit": BASE,
        "primary_outcome": OUTCOME,
        "source_count": len(sources),
        "authority_count": len(AUTHORITIES),
        "configuration_object_count": len(CONFIG_OBJECTS),
        "relation_count": len(RELATIONS),
        "gate_arena_count": len(GATES),
        "premise_count": len(PREMISES),
        "control_count": len(CONTROLS),
        "native_realized_family_count": 0,
        "conditional_stability_scope_count": 1,
        "smallest_missing_owned_object": "native realized variation structure: selected varied degrees of freedom plus tangent domain and persistence/response rule on the complete metric arena",
        "maximum_conclusion": "A native typed off-shell geometric parent arena is derived. One selected realized variation space containing the registered conditional families is not derived; stable-basin language is presently global only as a working hypothesis and is well posed solely inside separately declared conditional models.",
        "gpu_used": False,
    }
    (OUT / "AUDIT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
