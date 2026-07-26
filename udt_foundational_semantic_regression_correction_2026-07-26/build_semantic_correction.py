#!/usr/bin/env python3
"""Build the preregistered semantic-precedence registry and candidate adjudication."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


CONTROL_PATHS = {
    row["path"] for row in read_tsv(HERE / "CONTROL_TARGETS.tsv")
}

DOF_PREFIX = "udt_global_functional_dof_constraint_rank_audit_2026-07-26/"

DOF_MUTABLE_CURRENT = {
    "AUDIT_REPORT.md",
    "AUDIT_RESULT.json",
    "CATCH_PROOF_RESULTS.tsv",
    "COMPLETION_DOF_ATLAS.tsv",
    "CONSTRAINT_RANK_LEDGER.tsv",
    "DERIVED_OBJECT_NO_DOUBLE_COUNT.tsv",
    "EXACT_DERIVATION.md",
    "INDEPENDENT_VERIFICATION_RESULT.json",
    "LAY_REPORT.md",
    "LOCAL_PRESENTATION_RANK.tsv",
    "NEXT_STEP.md",
    "REALIZATION_BRANCH_RANK.tsv",
    "RESPONSE_COVERAGE_TARGET.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "build_dof_audit.py",
    "verify_dof_audit.py",
    "verify_dof_audit_independent.py",
}

CENTRAL_SUPERSESSIONS = {
    "udt_coframe_hopf_bridge_audit_2026-07-23/AUDIT_REPORT.md": "S01",
    "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv": "S02",
    "udt_global_local_relational_closure_audit_2026-07-25/DEPENDENCY_ARCHITECTURE.tsv": "S03",
    "udt_native_coframe_composition_law_audit_2026-07-23/AUDIT_REPORT.md": "S04",
    "udt_native_coframe_composition_law_audit_2026-07-23/LAY_REPORT.md": "S05",
    "udt_native_coframe_composition_law_audit_2026-07-23/STATUS_LEDGER.tsv": "S06",
}

PATTERNS = {
    "FOUNDED_PHI": ("founded phi", "founded_phi", "reciprocal depth"),
    "INDEPENDENT_PHI": ("independent phi", "independent_phi", "independent signed phi"),
    "PHI_OPENNESS": ("phi relation", "phi profile", "phi assignment", "phi extension", "phi solder"),
    "STRONG_LOCAL_CSN": ("strong local csn", "strong_local_csn"),
    "SCALE_FREE": ("scale-free", "scale free"),
    "GENERIC_DOF": ("f4[6]", "propagating mode", "degree of freedom"),
    "CARRIER": ("s2 carrier", "s^2 carrier", "carrier emergence"),
    "ACTION": ("c2/bach", "c^2", "eh action", "native action"),
    "BOOTSTRAP": ("bootstrap",),
    "MAXWELL": ("maxwell", "f=ds", "d f=0", "df=0"),
    "XMAX": ("x_max", "xmax"),
    "MASS_SOURCE_BOUNDARY": ("native source", "boundary charge", "unconditional mass"),
}

TERM_GUARDS = {
    "FOUNDED_PHI": "G01;G02",
    "INDEPENDENT_PHI": "G03",
    "PHI_OPENNESS": "G01;G03;G08",
    "STRONG_LOCAL_CSN": "G04;G05",
    "SCALE_FREE": "G04;G05;G06",
    "GENERIC_DOF": "G07;G08",
    "CARRIER": "G09;G15",
    "ACTION": "G10;G11;G16",
    "BOOTSTRAP": "G12",
    "MAXWELL": "G13",
    "XMAX": "G14",
    "MASS_SOURCE_BOUNDARY": "G15;G16",
}


def matched_terms(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return []
    return [name for name, needles in PATTERNS.items() if any(needle in text for needle in needles)]


def premise_use(guard_id: str) -> tuple[str, str]:
    mapping = {
        "G01": ("DERIVED", "ACTIVE_FOUNDATION"),
        "G02": ("DERIVED", "ACTIVE_FOUNDATION"),
        "G03": ("CHOSE", "COMPARISON_ONLY_NOT_NATIVE"),
        "G04": ("OPEN", "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES"),
        "G05": ("DERIVED", "ALGEBRA_ONLY"),
        "G06": ("OBSERVED", "ACTIVE_CALIBRATION"),
        "G07": ("DERIVED", "GENERIC_ARENA_BASELINE_ONLY"),
        "G08": ("OPEN", "ACTIVE_OPEN_GATE"),
        "G09": ("POSIT", "CONDITIONAL_CARRIER_BRANCH_ONLY"),
        "G10": ("CONDITIONAL", "INACTIVE_WITHOUT_STRONG_CSN_PREMISE"),
        "G11": ("CONDITIONAL", "NOT_SELECTED"),
        "G12": ("WORKING", "ON_SHELL_ADMISSIBILITY_ONLY"),
        "G13": ("CONDITIONAL", "TORIC_GEOMETRY_ONLY"),
        "G14": ("WORKING", "GLOBAL_OBSERVER_PAIR_SCHEMA"),
        "G15": ("SETTLED", "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL"),
        "G16": ("OPEN", "NO_COMPLETE_PHYSICS_CLAIM"),
    }
    return mapping[guard_id]


def build_registry() -> None:
    rows = []
    for guard in read_tsv(HERE / "SEMANTIC_GUARD_UNIVERSE.tsv"):
        label, active_use = premise_use(guard["guard_id"])
        rows.append(
            {
                "premise_id": guard["guard_id"],
                "term": guard["term"],
                "current_status": guard["controlling_status"],
                "epistemic_label": label,
                "active_use": active_use,
                "open_scope": guard["open_scope"],
                "forbidden_regression": guard["forbidden_regression"],
                "controlling_source": guard["controlling_source"],
                "precedence_rule": "LIVE_THEN_THIS_REGISTRY_THEN_CITED_SOURCE__CONFLICT_MEANS_STOP",
            }
        )
    write_tsv(
        ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv",
        [
            "premise_id",
            "term",
            "current_status",
            "epistemic_label",
            "active_use",
            "open_scope",
            "forbidden_regression",
            "controlling_source",
            "precedence_rule",
        ],
        rows,
    )


def classify_candidate(
    row: dict[str, str], prior: dict[str, dict[str, str]]
) -> tuple[str, str, str]:
    path = row["path"]
    terms = matched_terms(ROOT / path)
    hit_text = ";".join(terms) if terms else "NONE"

    if path == "CANON.md":
        return "OWNER_LOCKED_CANON_UNCHANGED", hit_text, "CANON is not current semantic navigation and Charles did not authorize canonization"
    if path in CONTROL_PATHS:
        return "CONTROL_UPDATED_TO_PRECEDENCE_REGISTRY", hit_text, "current startup/navigation control must route through the correction"
    if path.startswith(DOF_PREFIX):
        name = path[len(DOF_PREFIX):]
        if name in DOF_MUTABLE_CURRENT:
            return "FAULTY_CURRENT_OUTPUT_CORRECTED", hit_text, "current generated result or executable verifier carried the regressed ontology"
        return "FAULTY_PACKAGE_HISTORY_PRESERVED_WITH_CORRECTION_LAYER", hit_text, "preregistration, frozen inputs, and historical records remain evidence of the error"
    if path in CENTRAL_SUPERSESSIONS:
        return "CENTRAL_SUPERSESSION_OVERLAY_REQUIRED", hit_text, "known July-25 wording ambiguity; algebra survives and the correction is path-specific"

    old = prior.get(path)
    if old:
        ruling = old["primary_ruling"]
        if ruling == "HISTORICAL_OR_FROZEN_PRESERVE_ONLY":
            return "HISTORICAL_OR_FROZEN_NONCONTROLLING", hit_text, "immutable or historical evidence preserved; current registry controls reuse"
        if ruling == "CONDITIONAL_SLOT_SCOPE_REQUIRES_RETENTION":
            return "CHOSE_COMPARISON_SCOPE_RETAINED", hit_text, "independent-scalar or supplied-slot atlas remains valid only in its explicit chosen comparison scope"
        if ruling == "OVERBROAD_ALL_SOLDER_OPEN":
            return "CENTRAL_SUPERSESSION_OVERLAY_REQUIRED", hit_text, "known ambiguity between founded pair depth and still-open physical assignment or extension"
        return "PRIOR_FOUNDED_PHI_AUDIT_RETAINED", hit_text, f"July-25 impact ruling retained: {ruling}"

    if terms:
        return "POST_CORRECTION_RESULT_REGISTRY_GOVERNS_REUSE", hit_text, "post-July result contains high-risk vocabulary; its scoped mathematics is retained but current premise meanings come from the registry"
    return "NO_HIGH_RISK_SEMANTIC_HIT", hit_text, "candidate contains none of the preregistered high-risk semantic tokens"


def build_candidate_adjudication() -> None:
    candidates = read_tsv(HERE / "ACTIVE_SEMANTIC_CANDIDATES.tsv")
    prior_rows = read_tsv(
        ROOT / "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/ACTIVE_RESULT_IMPACT_LEDGER.tsv"
    )
    prior = {row["path"]: row for row in prior_rows}
    output = []
    for candidate in candidates:
        disposition, hits, reason = classify_candidate(candidate, prior)
        output.append(
            {
                **candidate,
                "semantic_terms": hits,
                "prior_phi_ruling": prior.get(candidate["path"], {}).get("primary_ruling", "NOT_IN_PRIOR_399"),
                "controlling_disposition": disposition,
                "reason": reason,
            }
        )
    write_tsv(
        HERE / "ACTIVE_SEMANTIC_ADJUDICATION.tsv",
        [
            "candidate_id",
            "path",
            "selection_sources",
            "base_blob",
            "semantic_terms",
            "prior_phi_ruling",
            "controlling_disposition",
            "reason",
        ],
        output,
    )

    census = []
    for term in PATTERNS:
        selected = [row for row in output if term in row["semantic_terms"].split(";")]
        census.append(
            {
                "semantic_term": term,
                "candidate_paths": str(len(selected)),
                "controlling_rule": TERM_GUARDS[term],
                "audit_method": "literal_casefolded_token_family_plus_path_disposition",
            }
        )
    write_tsv(
        HERE / "SEMANTIC_HIT_CENSUS.tsv",
        ["semantic_term", "candidate_paths", "controlling_rule", "audit_method"],
        census,
    )


def main() -> None:
    build_registry()
    build_candidate_adjudication()
    print("built current premise registry and 754-row semantic adjudication")


if __name__ == "__main__":
    main()
