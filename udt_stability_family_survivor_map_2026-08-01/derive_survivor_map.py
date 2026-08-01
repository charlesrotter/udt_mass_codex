#!/usr/bin/env python3
"""Deterministic seven-family survivor and computation-readiness map."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
PARENT = ROOT / "udt_stability_hypothesis_cross_family_atlas_2026-08-01"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def anchor(anchor_id: str, path: str, role: str, ruling: str) -> dict[str, str]:
    source = ROOT / path
    if not source.is_file():
        raise RuntimeError(f"missing anchor: {path}")
    return {"anchor_id": anchor_id, "path": path, "sha256": sha256(source), "role": role, "ruling": ruling}


def main() -> None:
    source = read_tsv(PKG / "SOURCE_INVENTORY.tsv")
    families = read_tsv(PKG / "FAMILY_UNIVERSE.tsv")
    cells = read_tsv(PKG / "CELL_UNIVERSE.tsv")
    if (len(source), len(families), len(cells)) != (1513, 7, 12):
        raise RuntimeError("preregistered census mismatch")
    source_by_path = {row["path"]: row for row in source}
    if len(source_by_path) != 1513:
        raise RuntimeError("duplicate source path")
    for row in source:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise RuntimeError(f"source changed: {row['path']}")

    anchors = [
        anchor("A01", "udt_stability_hypothesis_cross_family_atlas_2026-08-01/FAMILY_ATLAS.tsv", "parent family rulings", "seven corrected noninterchangeable families"),
        anchor("A02", "udt_stability_hypothesis_cross_family_atlas_2026-08-01/COMMON_GRAMMAR_MATRIX.tsv", "parent closure cells", "static, time, and bootstrap states remain separate"),
        anchor("A03", "udt_stability_hypothesis_cross_family_atlas_2026-08-01/INDEPENDENT_REVIEW.md", "parent cold ceiling", "weak architecture only; no species spectrum or shared operator"),
        anchor("A04", "udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md", "P4 S-i/S-ii stability scope", "one separately preregistered lambda-Schur next-tile option; full certificate remains open"),
        anchor("A05", "udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv", "P4 branch ledger", "controls, empty postures, S-i and S-ii outcomes typed separately"),
        anchor("A06", "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md", "P4 exact operators", "lambda-Schur and free germ curvature are distinct F01 obstructions"),
        anchor("A07", "udt_p4_stability_slice_2026-07-30/CORRECTION_LAYER.md", "P4 numeric lead ceiling", "Galerkin index is corroboration and not a banked lambda-Schur sign"),
        anchor("A08", "udt_p4_cold_adversarial_review_2026-08-01/AUDIT_REPORT.md", "P4 cold regrade", "formal response/census evidence; fixed realized solution remains open"),
        anchor("A09", "udt_p4_cold_review_repair_2026-08-01/CLOSURE_REPORT.md", "P4 review closure", "presentation/provenance closed without physics promotion"),
        anchor("A10", "udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md", "native stability gate", "record is not sufficient for a native stability solve"),
        anchor("A11", "udt_stability_foundations_audit_2026-08-01/FIXED_REALIZATION_GATE.tsv", "joint realization prerequisites", "realized field, native equation, boundary, and tangent-space test remain open"),
        anchor("A12", "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "Hopfion scope", "static finite-box conditional; carrier, physical boundary, and time persistence open"),
        anchor("A13", "CURRENT_SCIENTIFIC_PREMISES.tsv", "premise controller", "carrier, action, boundary, mass, time, and bootstrap ceilings retained"),
        anchor("A14", "udt_global_local_self_consistency_premise_audit_2026-08-01/AUDIT_REPORT.md", "bootstrap ceiling", "bootstrap is a distinct unadopted posit with no membership rule"),
        anchor("A15", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "action/source ceiling", "complete native action, source, boundary charge, and mass remain open"),
    ]
    if any(item["path"] not in source_by_path or source_by_path[item["path"]]["sha256"] != item["sha256"] for item in anchors):
        raise RuntimeError("authority anchor outside frozen source universe")
    write_tsv("SOURCE_AUTHORITY_LEDGER.tsv", anchors)

    premises = [
        {"premise_id": "P01", "object": "seven-family partition", "status": "DERIVED_AUDIT_PARTITION", "role": "bounded census", "source_basis": "A01-A03", "limit": "not all possible UDT families"},
        {"premise_id": "P02", "object": "P4 response/Hessian", "status": "CONDITIONAL", "role": "F01-F03 stability evidence", "source_basis": "A04-A09", "limit": "not a native whole response law"},
        {"premise_id": "P03", "object": "P4 ell=1 normalization", "status": "CHOSE", "role": "certified F01 branch", "source_basis": "A04-A07", "limit": "travels with candidate"},
        {"premise_id": "P04", "object": "germ-Hessian-flat wall response", "status": "CONDITIONAL_WITNESS", "role": "F01 lambda-Schur candidate domain", "source_basis": "A04-A07", "limit": "free second-germ curvature remains open"},
        {"premise_id": "P05", "object": "angular parity", "status": "SUPPLIED", "role": "F01 branch split", "source_basis": "A04-A07", "limit": "not selected by metric/bootstrap"},
        {"premise_id": "P06", "object": "round S2 carrier", "status": "POSIT", "role": "F04 configuration", "source_basis": "A12-A13", "limit": "emergence open"},
        {"premise_id": "P07", "object": "L2+L4 carrier functional", "status": "CONDITIONAL_CHOSEN", "role": "F04 static stability", "source_basis": "A12-A13", "limit": "not common with P4"},
        {"premise_id": "P08", "object": "Hopfion finite computational box/mask", "status": "CHOSE_SOLVER_BOUNDARY", "role": "F04 static certificate", "source_basis": "A12", "limit": "not physical finite-cell completion"},
        {"premise_id": "P09", "object": "native physical time equation", "status": "OPEN", "role": "time persistence gate", "source_basis": "A10-A15", "limit": "zero families promoted"},
        {"premise_id": "P10", "object": "physical finite-cell boundary", "status": "OPEN", "role": "global stability gate", "source_basis": "A10-A15", "limit": "computational boundaries do not substitute"},
        {"premise_id": "P11", "object": "bootstrap membership rule", "status": "WORKING_POSIT_OPERATION_OPEN", "role": "family selection gate", "source_basis": "A13-A15", "limit": "zero families selected"},
        {"premise_id": "P12", "object": "complete native action/response/source", "status": "OPEN", "role": "cross-family operator gate", "source_basis": "A10-A15", "limit": "no operator transfer"},
        {"premise_id": "P13", "object": "native unconditional mass", "status": "OPEN", "role": "particle interpretation gate", "source_basis": "A13-A15", "limit": "conditional readouts only"},
        {"premise_id": "P14", "object": "F05 stability response/domain", "status": "ABSENT", "role": "ring readiness blocker", "source_basis": "A01-A03", "limit": "period law is not stability"},
        {"premise_id": "P15", "object": "F07 common realized live field", "status": "OPEN", "role": "joint-realization blocker", "source_basis": "A08-A11", "limit": "formal embeddings are not a solution"},
        {"premise_id": "P16", "object": "F06 massive closed scope", "status": "EXACT_SCOPED_EMPTY", "role": "nonexistence control", "source_basis": "A01-A09", "limit": "regrade if premise scope changes"},
    ]
    write_tsv("PREMISE_LEDGER.tsv", premises)

    survivor = [
        {"family_id": "F01", "present_state": "CONDITIONAL_PARTIAL_SURVIVOR", "surviving_branch": "odd-pinned zero-trace core positive under registered crease/witness premises", "excluded_or_negative": "free angular-wall branch unstable; empty closed postures belong to F06", "open_certificate": "lambda-Schur sign plus unpinned free wall-germ curvature", "time_status": "OPEN_NO_NATIVE_TIME_EQUATION", "bootstrap_status": "NOT_SELECTED", "readiness": "CPU_EXACT_CHECK_READY", "later_test": "rigorous lambda-Schur sign certification at every isolated F(s)=integral log(w_s)=0 root in s in (1,3), separately for free f/h traces and SUPPLIED ODD zero f/h traces", "maximum_test_conclusion": "local single-cell Schur sign and conditional joint index in the named germ-Hessian-flat branch only; never whole-chain or full physical stability", "source_basis": "A01-A11"},
        {"family_id": "F02", "present_state": "CONDITIONAL_SECTOR_SURVIVOR_CONTINUOUS", "surviving_branch": "jet-quadratic sector satisfying 64 E0^2 ell^4 <= g_p c_m pi^4", "excluded_or_negative": "no-m-jet class unstable for nonzero E0", "open_certificate": "fixed joint realization, complete boundary/perturbation domain, and full certificate", "time_status": "OPEN_NO_NATIVE_TIME_EQUATION", "bootstrap_status": "NOT_SELECTED", "readiness": "BLOCKED_MISSING_FIXED_REALIZATION", "later_test": "none until a common realized background and owned full domain exist", "maximum_test_conclusion": "current exact continuous sector dichotomy only", "source_basis": "A01-A11"},
        {"family_id": "F03", "present_state": "CONTROL_NONISOLATED", "surviving_branch": "massless PSD-degenerate controls reproduce registered flat directions", "excluded_or_negative": "not an isolated stable basin", "open_certificate": "not a survivor-certificate target", "time_status": "OPEN_NOT_PROMOTED", "bootstrap_status": "NOT_SELECTED", "readiness": "CONTROL_ONLY", "later_test": "retain as regression and nonisolation control", "maximum_test_conclusion": "calculation control only", "source_basis": "A01-A10"},
        {"family_id": "F04", "present_state": "CONDITIONAL_STATIC_FINITE_BOX_SURVIVOR", "surviving_branch": "full-3D Q approximately 1 Hopfion under round-S2 POSIT and L2+L4 finite-box premises", "excluded_or_negative": "no carrier emergence, physical finite-cell boundary, infinite-volume, or time theorem", "open_certificate": "physical completion and time-live persistence", "time_status": "OPEN_NO_NATIVE_TIME_EQUATION", "bootstrap_status": "NOT_SELECTED", "readiness": "BLOCKED_MISSING_TIME_EQUATION", "later_test": "none until native time law and physical boundary are owned", "maximum_test_conclusion": "settled static finite-box conditional remains unchanged", "source_basis": "A01-A03;A10-A15"},
        {"family_id": "F05", "present_state": "STRUCTURAL_EXISTENCE_FAMILY_NOT_STABILITY_TESTED", "surviving_branch": "massless constant rings; conditional mixed-sign multicell completion", "excluded_or_negative": "uniform all-definite massive cyclic rings excluded", "open_certificate": "no owned stability response or perturbation domain", "time_status": "OPEN_NOT_TESTABLE", "bootstrap_status": "NOT_SELECTED", "readiness": "BLOCKED_MISSING_NATIVE_RESPONSE", "later_test": "none until a family-native response and variation domain are derived", "maximum_test_conclusion": "closure and mass classification only", "source_basis": "A01-A03;A13-A15"},
        {"family_id": "F06", "present_state": "EXACT_SCOPED_EMPTY", "surviving_branch": "none in the registered massive cyclic-N1/double-crease scope", "excluded_or_negative": "massive candidate locus eliminated by completion/wall-trace constraints", "open_certificate": "stability is not applicable on an empty domain", "time_status": "NOT_APPLICABLE", "bootstrap_status": "NOT_SELECTED", "readiness": "NOT_APPLICABLE_EMPTY", "later_test": "none unless the premise scope changes and the negative is regraded", "maximum_test_conclusion": "exact scoped nonexistence, not instability", "source_basis": "A01-A09"},
        {"family_id": "F07", "present_state": "FORMAL_MODULES_NO_REALIZED_SURVIVOR", "surviving_branch": "formal static/time/angular module embeddings only", "excluded_or_negative": "no common nonzero live on-shell field has been exhibited", "open_certificate": "fixed realization, native whole equation, boundary, tangent space, and stability law", "time_status": "FORMAL_TIME_LABEL_NOT_PHYSICAL_PERSISTENCE", "bootstrap_status": "NOT_SELECTED", "readiness": "BLOCKED_MISSING_FIXED_REALIZATION", "later_test": "joint-realization closure audit before any stability computation", "maximum_test_conclusion": "formal compatibility and missing-join localization only", "source_basis": "A01-A03;A08-A15"},
    ]
    write_tsv("SURVIVOR_LEDGER.tsv", survivor)

    cell_status = {
        "F01": ["CONDITIONAL_NONEMPTY_SCOPED", "CONDITIONAL_STATIONARY_WITNESS", "CONDITIONAL_REDUCED_JOINT_HESSIAN_OWNED", "PARTIAL_CREASE_PARITY_OWNED_HIGHER_GERMS_OPEN", "PARTIAL_ZERO_TRACE_CORE_FULL_GERMS_OPEN", "EMPTY_CLOSED_POSTURES_ROUTED_TO_F06", "FREE_BRANCH_UNSTABLE_ODD_PIN_CORE_POSITIVE", "OPEN_LAMBDA_SCHUR_AND_FREE_GERM_CURVATURE", "OPEN_NO_NATIVE_TIME_EQUATION", "OPEN_PHYSICAL_COMPLETION", "ABSENT", "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY"],
        "F02": ["CONDITIONAL_NONEMPTY_CLASS", "CONDITIONAL_LANDING_NOT_JOINT_REALIZATION", "CONDITIONAL_SECTOR_HESSIAN_OWNED", "PARTIAL_CLASS_BOUNDARY", "SECTOR_DOMAIN_ONLY", "NO_EXISTENCE_EXCLUSION_WITHIN_RETAINED_JET_CLASS", "EXACT_CONTINUOUS_SECTOR_DICHOTOMY", "SECTOR_ONLY_NOT_FULL_CERTIFICATE", "OPEN_NO_NATIVE_TIME_EQUATION", "OPEN_PHYSICAL_COMPLETION", "ABSENT", "BLOCKED_MISSING_FIXED_REALIZATION"],
        "F03": ["PRESENT_CONTROL", "PRESENT_CONTROL_BACKGROUND", "CONDITIONAL_CONTROL_HESSIAN_OWNED", "PRESENT_CONTROL_DOMAIN", "PRESENT_CONTROL_DOMAIN", "NONE", "PSD_DEGENERATE_CONTROL", "NOT_ISOLATED", "OPEN_NOT_PROMOTED", "NOT_EVALUATED_PHYSICALLY", "ABSENT", "CONTROL_ONLY"],
        "F04": ["OBSERVED_CARRIER_CONDITIONAL", "OBSERVED_STATIC_FINITE_BOX", "CHOSEN_CONDITIONAL_L2_PLUS_L4", "COMPUTATIONAL_BOUNDARY_OWNED_PHYSICAL_OPEN", "STATIC_FINITE_BOX_DOMAIN_OWNED_TIME_DOMAIN_MISSING", "CONDITIONAL_TOPOLOGICAL_SECTOR_AVAILABLE", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL", "STATIC_CERTIFICATE_ONLY", "OPEN_NO_NATIVE_TIME_EQUATION", "OPEN_PHYSICAL_BOUNDARY", "ABSENT", "BLOCKED_MISSING_TIME_EQUATION"],
        "F05": ["MASSLESS_RING_EXISTS_MIXED_MULTICELL_CONDITIONAL", "CLOSURE_CONFIGURATION_ONLY", "PERIOD_LAW_NOT_STABILITY_RESPONSE", "SCOPED_CYCLIC_COMPLETION_OWNED", "NO_STABILITY_PERTURBATION_DOMAIN", "ALL_DEFINITE_MASSIVE_RING_EXCLUDED", "NOT_TESTED", "ABSENT", "OPEN_NOT_TESTABLE", "CLASSIFICATION_SCOPE_ONLY", "ABSENT", "BLOCKED_MISSING_NATIVE_RESPONSE"],
        "F06": ["EMPTY_MASSIVE_SCOPE", "NONE_EMPTY", "COMPLETION_LAW_NOT_STABILITY_RESPONSE", "SCOPED_COMPLETION_OWNED", "NOT_APPLICABLE", "EXACT_NONEXISTENCE", "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE", "SCOPED_CLOSURE_ONLY", "ABSENT", "NOT_APPLICABLE_EMPTY"],
        "F07": ["FORMAL_MODULES_ONLY", "OPEN_COMMON_REALIZED_BACKGROUND", "ABSENT_COMPLETE_NATIVE_RESPONSE", "OPEN_DIFFERENTIABLE_FINITE_CELL_BOUNDARY", "ABSENT_TANGENT_SPACE_TO_REALIZED_SET", "BLOCKED_BY_REALIZATION_JOIN", "BLOCKED", "BLOCKED", "FORMAL_LABEL_ONLY_PHYSICAL_PERSISTENCE_OPEN", "OPEN", "ABSENT", "BLOCKED_MISSING_FIXED_REALIZATION"],
    }
    cell_rows = [
        {"family_id": family_id, "cell_id": cell["cell_id"], "cell": cell["cell"], "status": cell_status[family_id][index], "source_basis": next(row["source_basis"] for row in survivor if row["family_id"] == family_id)}
        for family_id in [f"F{i:02d}" for i in range(1, 8)]
        for index, cell in enumerate(cells)
    ]
    write_tsv("SURVIVOR_CELL_MATRIX.tsv", cell_rows)

    readiness = [
        {"family_id": "F01", "fixed_object": "YES_CONDITIONAL", "response": "YES_CONDITIONAL", "boundary": "YES_FOR_REGISTERED_CREASE_WITNESS", "perturbation_domain": "YES_FOR_LAMBDA_SCHUR_BLOCK_ONLY", "bounded_range": "YES_REGISTERED_ROOT_AND_PARITIES", "cpu_anchor": "YES_GALERKIN_CORROBORATION_NOT_CERTIFICATE", "physical_time_equation": "NO", "physical_boundary": "NO", "primary_blocker_or_target": "LAMBDA_SCHUR_SIGN_IS_BOUNDED_TARGET__FREE_GERM_REMAINS_SEPARATE", "readiness": "CPU_EXACT_CHECK_READY"},
        {"family_id": "F02", "fixed_object": "CONDITIONAL_CLASS_ONLY", "response": "YES_SECTOR_ONLY", "boundary": "PARTIAL", "perturbation_domain": "SECTOR_ONLY", "bounded_range": "YES_FOR_EXISTING_THRESHOLD", "cpu_anchor": "YES_EXISTING_EXACT_DICHOTOMY", "physical_time_equation": "NO", "physical_boundary": "NO", "primary_blocker_or_target": "NO_COMMON_FIXED_REALIZATION_FOR_STRONGER_TEST", "readiness": "BLOCKED_MISSING_FIXED_REALIZATION"},
        {"family_id": "F03", "fixed_object": "YES_CONTROL", "response": "YES_CONTROL", "boundary": "YES_CONTROL", "perturbation_domain": "YES_CONTROL", "bounded_range": "NOT_APPLICABLE", "cpu_anchor": "YES", "physical_time_equation": "NO", "physical_boundary": "NO", "primary_blocker_or_target": "CONTROL_NOT_SURVIVOR_TARGET", "readiness": "CONTROL_ONLY"},
        {"family_id": "F04", "fixed_object": "YES_CARRIER_CONDITIONAL_STATIC", "response": "YES_CHOSEN_STATIC_FUNCTIONAL", "boundary": "COMPUTATIONAL_ONLY", "perturbation_domain": "STATIC_FINITE_BOX_ONLY", "bounded_range": "YES_STATIC_HISTORY", "cpu_anchor": "YES_STATIC_OPERATOR", "physical_time_equation": "NO", "physical_boundary": "NO", "primary_blocker_or_target": "NATIVE_TIME_EQUATION_AND_PHYSICAL_BOUNDARY_MISSING", "readiness": "BLOCKED_MISSING_TIME_EQUATION"},
        {"family_id": "F05", "fixed_object": "YES_CLOSURE_CLASS", "response": "NO_STABILITY_RESPONSE", "boundary": "YES_CLOSURE_SCOPE", "perturbation_domain": "NO", "bounded_range": "NO", "cpu_anchor": "YES_PERIOD_IDENTITIES_ONLY", "physical_time_equation": "NO", "physical_boundary": "NO", "primary_blocker_or_target": "NATIVE_STABILITY_RESPONSE_MISSING", "readiness": "BLOCKED_MISSING_NATIVE_RESPONSE"},
        {"family_id": "F06", "fixed_object": "NO_EMPTY", "response": "NOT_APPLICABLE", "boundary": "YES_SCOPED_CLOSURE", "perturbation_domain": "NOT_APPLICABLE", "bounded_range": "NOT_APPLICABLE", "cpu_anchor": "YES_NONEXISTENCE", "physical_time_equation": "NOT_APPLICABLE", "physical_boundary": "NOT_APPLICABLE", "primary_blocker_or_target": "EMPTY_DOMAIN", "readiness": "NOT_APPLICABLE_EMPTY"},
        {"family_id": "F07", "fixed_object": "NO_FORMAL_ONLY", "response": "NO_COMPLETE_NATIVE_RESPONSE", "boundary": "NO", "perturbation_domain": "NO_REALIZED_TANGENT_SPACE", "bounded_range": "NO", "cpu_anchor": "YES_FORMAL_COMPATIBILITY_ONLY", "physical_time_equation": "NO", "physical_boundary": "NO", "primary_blocker_or_target": "COMMON_FIXED_REALIZATION_MISSING_FIRST", "readiness": "BLOCKED_MISSING_FIXED_REALIZATION"},
    ]
    write_tsv("READINESS_LEDGER.tsv", readiness)

    dependency = [
        {"family_id": "F01", "owned_closure": "conditional branch, Hessian, free-trace/odd-zero-trace domains, and F(s)=integral log(w_s)=0 root equation on s in (1,3)", "missing_closure": "root isolation and lambda-Schur sign; separately free second-germ curvature", "readiness_effect": "lambda-Schur cell alone is CPU exact-check ready without assuming root uniqueness", "source_basis": "A04-A09;P02-P05"},
        {"family_id": "F02", "owned_closure": "conditional sector Hessian and exact continuous threshold", "missing_closure": "common fixed realization, full boundary and perturbation domain", "readiness_effect": "stronger computation blocked", "source_basis": "A01-A11;P02;P09-P12"},
        {"family_id": "F03", "owned_closure": "control background/domain/Hessian", "missing_closure": "not applicable as survivor target", "readiness_effect": "control only", "source_basis": "A01-A10;P02"},
        {"family_id": "F04", "owned_closure": "conditional static field, chosen functional, computational finite-box operator", "missing_closure": "native time equation, carrier emergence, physical boundary", "readiness_effect": "time/GPU work blocked", "source_basis": "A10-A15;P06-P12"},
        {"family_id": "F05", "owned_closure": "period/completion and mass-exclusion identities", "missing_closure": "stability response and perturbation domain", "readiness_effect": "stability computation blocked", "source_basis": "A01-A03;P12;P14"},
        {"family_id": "F06", "owned_closure": "exact scoped nonexistence", "missing_closure": "none within empty domain", "readiness_effect": "not applicable", "source_basis": "A01-A09;P16"},
        {"family_id": "F07", "owned_closure": "formal module embeddings", "missing_closure": "common realized field, native equation, boundary, tangent space", "readiness_effect": "joint-realization audit first", "source_basis": "A08-A15;P09-P12;P15"},
    ]
    write_tsv("FAMILY_DEPENDENCY_CLOSURE.tsv", dependency)

    development_queue = [
        {"family_id": "F01", "computation_readiness": "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY", "development_disposition": "ACTIVE_DERIVATION_QUEUE", "queue_group": "Q02_F01_FREE_GERM_COMPLETION", "queue_rank": 2, "priority_grade": "WORKING_OPERATIONAL_NOT_PHYSICS", "derivation_object": "determine whether deeper finite-cell N4/period/holonomy structure owns the second wall germ", "dependency": "separate from the ready lambda-Schur sign check", "stop_condition": "no invented germ pin or boundary response"},
        {"family_id": "F02", "computation_readiness": "BLOCKED_MISSING_FIXED_REALIZATION", "development_disposition": "ACTIVE_DERIVATION_QUEUE", "queue_group": "Q01_JOINT_REALIZATION", "queue_rank": 1, "priority_grade": "WORKING_OPERATIONAL_NOT_PHYSICS", "derivation_object": "derive one common fixed/on-shell field and complete domain before extending the sector result", "dependency": "shared with F07 realization join", "stop_condition": "do not promote the conditional landing class to a realized universe"},
        {"family_id": "F03", "computation_readiness": "CONTROL_ONLY", "development_disposition": "RETAIN_AS_CONTROL", "queue_group": "NONE", "queue_rank": "-", "priority_grade": "NOT_RANKED", "derivation_object": "none; replay when a related operator changes", "dependency": "validation/nonisolation control", "stop_condition": "do not turn flat controls into survivor basins"},
        {"family_id": "F04", "computation_readiness": "BLOCKED_MISSING_TIME_EQUATION", "development_disposition": "ACTIVE_DERIVATION_QUEUE_DOWNSTREAM", "queue_group": "Q04_NATIVE_TIME_AND_PHYSICAL_BOUNDARY", "queue_rank": 4, "priority_grade": "WORKING_OPERATIONAL_NOT_PHYSICS", "derivation_object": "derive native time response and physical finite-cell carrier boundary", "dependency": "also depends on carrier ownership and complete native response", "stop_condition": "no imported dynamics or computational-boundary substitution"},
        {"family_id": "F05", "computation_readiness": "BLOCKED_MISSING_NATIVE_RESPONSE", "development_disposition": "ACTIVE_DERIVATION_QUEUE", "queue_group": "Q03_RING_RESPONSE_AND_VARIATION_DOMAIN", "queue_rank": 3, "priority_grade": "WORKING_OPERATIONAL_NOT_PHYSICS", "derivation_object": "ask whether the metric supplies a response and perturbation domain for the completion family", "dependency": "period identity alone is insufficient", "stop_condition": "do not import P4/Hopfion stability operators"},
        {"family_id": "F06", "computation_readiness": "NOT_APPLICABLE_EMPTY", "development_disposition": "RETAIN_NEGATIVE_CONTROL_REOPEN_ON_PREMISE_CHANGE", "queue_group": "NONE", "queue_rank": "-", "priority_grade": "NOT_RANKED", "derivation_object": "none in current exact massive closed scope", "dependency": "regrade only if a controlling premise changes", "stop_condition": "nonexistence is not instability or abandonment"},
        {"family_id": "F07", "computation_readiness": "BLOCKED_MISSING_FIXED_REALIZATION", "development_disposition": "ACTIVE_DERIVATION_QUEUE", "queue_group": "Q01_JOINT_REALIZATION", "queue_rank": 1, "priority_grade": "WORKING_OPERATIONAL_NOT_PHYSICS", "derivation_object": "derive or rule out one common nonzero static/time/angular live on-shell realization", "dependency": "native whole equation, compatible boundary, and premise stack", "stop_condition": "formal embeddings cannot substitute for a realized solution"},
    ]
    write_tsv("DEVELOPMENT_QUEUE.tsv", development_queue)

    candidate_contract = [
        {"item": "family", "value": "F01 only", "status": "FROZEN", "limit": "no transfer to F02-F07"},
        {"item": "branch", "value": "R05 free f/h traces and R06 SUPPLIED ODD zero f/h traces on the conditional germ-Hessian-flat crease witness", "status": "FROZEN", "limit": "branch domains remain separate; empty closed postures excluded"},
        {"item": "target", "value": "sign of the local lambda/mu Schur block at every isolated root of F(s)=integral_-1^1 log(w_s(x)) dx=0, s in (1,3), with w_s(x)=(s^2/2)x^2+(s^2-s)x+1+s^2/2-s", "status": "OPEN_BOUNDED", "limit": "sources prove existence but not root uniqueness; not the free wall-germ curvature"},
        {"item": "normalization", "value": "ell=1", "status": "CHOSE", "limit": "must travel"},
        {"item": "wall_response", "value": "banked germ-Hessian-flat witnesses", "status": "CONDITIONAL", "limit": "unrestricted second germ remains open"},
        {"item": "existing_anchor", "value": "joint Galerkin n-=1 at s approximately 1.68102 and dimensions 13/17/21", "status": "CORROBORATION_ONLY", "limit": "free f/h trace branch only; not a sign certificate and not evidence for the odd-zero-trace branch"},
        {"item": "primary_method", "value": "rigorous root and integral enclosure of the exact Schur scalar", "status": "PROPOSED_NOT_RUN", "limit": "method must be preregistered"},
        {"item": "independent_method", "value": "independent spectral/index enclosure without importing primary sign result", "status": "PROPOSED_NOT_RUN", "limit": "same-code replay is insufficient"},
        {"item": "certification", "value": "raw interval/error bounds exclude zero at every isolated root on each named free-trace and supplied-odd-zero-trace branch", "status": "REQUIRED", "limit": "no tolerance retuning"},
        {"item": "maximum_conclusion", "value": "local single-cell conditional lambda-Schur sign and branch-local joint index only", "status": "FIXED", "limit": "no whole mixed-chain/full stability, time persistence, matter, or bootstrap selection"},
    ]
    write_tsv("F01_CPU_CANDIDATE_CONTRACT.tsv", candidate_contract)

    next_steps = [
        {"rank": 1, "family_id": "F01", "status": "SEPARATELY_PREREGISTRABLE_CPU_EXACT_CHECK", "test": "isolate every F(s)=integral log(w_s)=0 root in s in (1,3), then certify the local lambda-Schur sign separately on the free-f/h-trace and SUPPLIED-ODD-zero-f/h-trace branches", "why_ranked": "only bounded open cell with owned conditional object, response, branch, and domain", "required_before_execution": "new preregistration; exact Schur formulas and all-root enclosure frozen; raw interval/error contract; no retuning", "ceiling": "local single-cell Schur sign and conditional branch index only; free wall-germ curvature and physical stability remain open"},
        {"rank": 2, "family_id": "F07", "status": "EVIDENCE_DERIVATION_BLOCKED_NOT_COMPUTATION_READY", "test": "joint-realization closure audit", "why_ranked": "upstream blocker shared by stronger F02/F07 stability questions", "required_before_execution": "derive or rule out one common on-shell field, native whole equation, compatible boundary, and premise stack", "ceiling": "realization join only"},
        {"rank": 3, "family_id": "F04", "status": "BLOCKED_NOT_COMPUTATION_READY", "test": "physical time-live Hopfion persistence", "why_ranked": "scientifically important but downstream of missing time law and physical boundary", "required_before_execution": "native time equation, carrier ownership, physical finite-cell completion, perturbation domain, CPU anchors", "ceiling": "none until prerequisites are owned"},
    ]
    write_tsv("RANKED_NEXT_TESTS.tsv", next_steps)

    status = [
        {"claim": "family_map", "status": "SEVEN_OF_SEVEN_COMPLETE", "basis": "SURVIVOR_LEDGER.tsv;SURVIVOR_CELL_MATRIX.tsv", "limit": "registered families only"},
        {"claim": "conditional_survivor_streams", "status": "F01_F02_F04_WITH_INCOMPATIBLE_PREMISES", "basis": "A01-A12", "limit": "not three particle species and not one common operator"},
        {"claim": "controls_structural_empty_formal", "status": "F03_CONTROL_F05_STRUCTURAL_F06_EMPTY_F07_FORMAL", "basis": "A01-A11", "limit": "not survivor inflation"},
        {"claim": "cpu_exact_candidates", "status": "ONE_F01_LAMBDA_SCHUR", "basis": "A04-A08", "limit": "separate preregistration required; free germ curvature remains"},
        {"claim": "cpu_bounded_solve_candidates", "status": "ZERO", "basis": "READINESS_LEDGER.tsv", "limit": "missing realization/response/boundary/time prerequisites"},
        {"claim": "gpu_candidates", "status": "ZERO", "basis": "READINESS_LEDGER.tsv", "limit": "no family owns the full GPU contract"},
        {"claim": "active_derivation_queue", "status": "FIVE_FAMILIES_IN_FOUR_DEVELOPMENT_GROUPS", "basis": "DEVELOPMENT_QUEUE.tsv", "limit": "blocked from computation does not mean abandoned; Q04 is downstream"},
        {"claim": "time_persistence", "status": "ZERO_OF_SEVEN_DERIVED", "basis": "C09", "limit": "formal/static/sector labels do not promote"},
        {"claim": "bootstrap_selection", "status": "ZERO_OF_SEVEN_SELECTED", "basis": "C11;A13-A15", "limit": "no membership rule"},
        {"claim": "overall", "status": "SURVIVOR_MAP_COMPLETE_WITH_CPU_CANDIDATE", "basis": "all ledgers", "limit": "readiness map only; no computation authorized"},
    ]
    write_tsv("STATUS_LEDGER.tsv", status)

    result = {
        "outcome": "SURVIVOR_MAP_COMPLETE_WITH_CPU_CANDIDATE",
        "source_paths_verified": 1513,
        "source_anchors": 15,
        "premises": 16,
        "families": 7,
        "cells_per_family": 12,
        "cell_rows": 84,
        "family_overlap": 0,
        "conditional_survivor_families": 3,
        "control_families": 1,
        "structural_only_families": 1,
        "empty_families": 1,
        "formal_only_families": 1,
        "dependency_rows": 7,
        "candidate_contract_rows": 10,
        "active_derivation_queue_families": 5,
        "derivation_queue_groups": 4,
        "families_discarded": 0,
        "cpu_exact_check_ready": 1,
        "cpu_bounded_solve_ready": 0,
        "gpu_ready": 0,
        "time_persistence_derived": 0,
        "bootstrap_selected": 0,
        "new_computation_run": False,
        "gpu_used": False,
        "carrier_adopted": False,
        "action_adopted": False,
        "bootstrap_law_adopted": False,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS survivor map: families=7 cells=84 cpu_exact=1 cpu_solve=0 gpu=0")


if __name__ == "__main__":
    main()
