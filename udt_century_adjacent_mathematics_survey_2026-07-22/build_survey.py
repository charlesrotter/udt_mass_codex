#!/usr/bin/env python3
"""Build deterministic derived tables for the century-scale adjacency survey."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "SOURCE_CENSUS.tsv"

JOIN_OBJECTS = {
    "J01": "reciprocal clock-parallel block -> complete time-live metric",
    "J02": "local tangent-space weave -> persistent global organization",
    "J03": "full tangent weave -> metric-native bivector or differential-form motif",
    "J04": "completion taxonomy -> one realized global quotient",
    "J05": "conditional reciprocal-toric quotient -> native S2 carrier",
    "J06": "carrier or quotient texture -> native deformation action",
    "J07": "complete action -> native matter source",
    "J08": "native source -> finite-cell boundary charge and mass",
    "J09": "native mass and proper volume -> bootstrap density fixed point",
    "J10": "dimensionless compactness -> absolute Xmax and total mass",
    "J11": "static conditional Hopfion -> time-live matter persistence",
    "J12": "pre-scale C2/Bach route -> post-scale EH-like route",
    "J13": "macro WR-L geometry -> particle or mass sector",
}

FAMILIES = [
    "F01_NATURAL_OPERATORS",
    "F02_HOLONOMY",
    "F03_CONFORMAL_PROJECTIVE_SCALE",
    "F04_EXTERIOR_CURVATURE_TOPOLOGY",
    "F05_BUNDLES_GLUING",
    "F06_BOUNDARY_VARIATION_CHARGE",
    "F07_SPECTRAL_SCALE",
    "F08_INVERSE_VARIATIONAL",
    "F09_FIXED_POINT_BOOTSTRAP",
    "F10_EVOLUTION_AND_CONSTRAINTS",
    "F11_HOPF_SOLITON_CONTROLS",
]

CONVERGENCE = [
    ("C01", "F01+F02", "A regular local selector is a finite-jet natural operator, while a persistent local splitting must survive the curvature-and-derivative holonomy algebra.", "Local selector search can be made finite and adversarial.", "No theorem chooses the output type or supplies a physical selector.", "J02;J03", "HIGH"),
    ("C02", "F02+F05", "Curvature transport, holonomy reduction, bundle existence, and global gluing are distinct layers.", "Test local invariant subspaces before asking for cocycles and quotient completion.", "Local projector transport cannot select a cap, seam, quotient, or carrier.", "J02;J04;J05", "HIGH"),
    ("C03", "F03+F07", "A representative or spectrum may exist without being unique, and spectral data can fail to determine geometry.", "A scale-selector claim needs a derived operator, boundary data, objective, and degeneracy audit.", "No Yamabe or spectral theorem provides UDT's physical scale.", "J10;J12", "HIGH"),
    ("C04", "F08+F06", "A differential equation need not be variational; a local Lagrangian need not globalize; a differentiable generator needs boundary data and may lack an integrable charge.", "Action, variation domain, boundary completion, and mass charge must be audited as one closure chain.", "GR boundary terms and charges are comparison controls only.", "J06;J07;J08", "HIGH"),
    ("C05", "F09+F07", "Fixed-point and eigenvalue theorems presuppose a map/operator, a domain, topology, compactness, and boundary conditions.", "Bootstrap must first be typed as an explicit whole-solution map.", "Existence theory does not invent the bootstrap operation or make it unique.", "J09;J10", "HIGH"),
    ("C06", "F10+F06", "Evolution, constraints, characteristics, gauge, and boundary flux form a coupled PDE specification.", "Time-live work is premature until a native principal symbol and incoming seal data exist.", "Ricci flow, harmonic-map flow, and Einstein evolution remain prohibited imports.", "J01;J11", "HIGH"),
    ("C07", "F04+F11", "Hopf topology certifies a supplied global map, while soliton existence and stability additionally require a supplied functional and boundary class.", "Keep quotient/map selection separate from carrier/action/stability.", "Topology alone does not derive the S2 carrier or L2+L4 dynamics.", "J05;J06;J11", "HIGH"),
    ("C08", "ALL", "Across every family, compatibility and existence are weaker than physical realization or selection.", "The smallest missing object remains an operational selector relation with typed domain and codomain.", "The survey cannot name or invent that relation from analogy.", "J01-J12", "DECISIVE"),
]

MISSING = [
    ("M01", "local selector output type", "scalar/one-form/two-form/projector/density plus weight and covariance", "Without a typed codomain invariant theory cannot enumerate candidates.", "J03", "OPEN", "Derive the codomain from the downstream join rather than preference."),
    ("M02", "finite-jet natural-selector census", "complete regular local operators from full metric/coframe/phi at bounded derivative order", "Would decide whether any local metric-only selector exists.", "J03;J12", "OPEN_HIGH_PRIORITY", "Construct invariant basis by type, CSN weight, parity, and derivative order; then test rank and branch selection."),
    ("M03", "full infinitesimal holonomy algebra", "closure of curvature and covariant derivatives on each complete branch", "Pointwise eigenplanes and open-path transport do not decide persistent reduction.", "J02", "OPEN_HIGH_PRIORITY", "Compute generated endomorphism algebra and common invariant subspaces across full-orchestra witnesses."),
    ("M04", "global cocycle and seam law", "transition functions, cap/seam compatibility, periods, orientation, and quotient map", "Needed to turn local motifs into global bundles or Hopf maps.", "J04;J05", "OPEN", "Audit only branches that survive M03; retain all compatible completions."),
    ("M05", "native variational object", "off-shell fields, functional, measure, derivative order, coefficients, and variation domain", "Needed before source, boundary term, or physical evolution can be derived.", "J06;J07", "OPEN", "If metric-led equations emerge, apply Helmholtz and global variational tests before proposing an action."),
    ("M06", "finite-cell differentiable generator", "allowed seal variations, boundary polarization, symplectic current, integrability, and normalization", "Needed before a boundary flux can be interpreted as native charge or mass.", "J08", "OPEN", "Derive from M05; do not import ADM, GHY, or Wald-Zoupas prescriptions."),
    ("M07", "typed bootstrap map", "solution space, map, topology, fixed-point equation, a priori bound, uniqueness criterion", "Fixed-point language is presently an interpretation without an operation.", "J09", "OPEN", "Define a same-solution density/mass/volume response only after native mass exists."),
    ("M08", "homothety-breaking datum or process", "independent dimensional relation beyond c_E, G_obs, and rank-one compactness", "Needed to determine absolute Xmax and total mass.", "J10", "OPEN", "Test whether M05-M07 produce an eigenvalue; otherwise retain an observational anchor explicitly."),
    ("M09", "native evolution system", "principal symbol, constraints, gauge separation, characteristics, initial data, seal data", "Needed to distinguish physical time from relaxation and test persistence.", "J01;J11", "OPEN", "No time-live solve until M05 and the global branch are defined."),
]

QUESTIONS = [
    (1, "Q01_LOCAL_NATURAL_SELECTOR_EXHAUSTION", "METRIC_LED", "J03;J12", "Enumerate every regular local diffeomorphism-covariant CSN-neutral finite-jet output of the full metric/coframe/phi data by tensor type and weight.", "No output of any admissible type distinguishes a physical representative or transverse realization.", "Closes the local-selector class only; cannot exclude global or boundary selectors.", "CPU_SYMBOLIC"),
    (2, "Q02_FULL_JET_HOLONOMY_CLOSURE", "METRIC_LED", "J02;J03", "Generate the infinitesimal holonomy algebra from curvature and successive covariant derivatives across representative complete full-orchestra branches; compute common real invariant subspaces.", "The algebra acts irreducibly on every generic branch and no registered special branch gives a globally persistent proper subbundle.", "Characterizes local parallel structure; does not select a quotient or dynamics.", "CPU_SYMBOLIC_THEN_BOUNDED_NUMERIC"),
    (3, "Q03_GLOBAL_COCYCLE_COMPLETION", "METRIC_LED", "J04;J05", "For each Q02 survivor, derive transition cocycles, monodromy, cap/seam regularity, periods, orientation, and any quotient map without privileging Hopf topology.", "No survivor globalizes under any registered finite-cell completion.", "Global compatibility atlas only; no carrier identification.", "CPU_ALGEBRAIC_TOPOLOGY"),
    (4, "Q04_NATIVE_EQUATION_TO_VARIATION_AUDIT", "METRIC_LED_IF_EQUATION_EXISTS", "J06;J07", "If Q01-Q03 expose a metric-native differential relation, test covariant Helmholtz conditions, global patching, symmetry-criticality, and full variation-domain completeness.", "No multiplier or global Lagrangian exists in the audited class.", "Conditional action classification; no source or mass until boundary completion.", "CPU_SYMBOLIC"),
    (5, "Q05_FINITE_CELL_BOUNDARY_DIFFERENTIABILITY", "METRIC_LED_IF_ACTION_EXISTS", "J08", "Derive allowed seal variations and the exact boundary term, symplectic flux, integrability, orientation, and normalization from the selected functional.", "No differentiable generator or integrable charge exists for the allowed seal data.", "Boundary-charge status only; no imported mass interpretation.", "CPU_SYMBOLIC"),
    (6, "Q06_TYPED_WHOLE_SOLUTION_BOOTSTRAP", "METRIC_LED_IF_MASS_EXISTS", "J09;J10", "Define and test a simultaneous geometry/matter/scale response map using native mass and proper volume from the same solution.", "No self-map, a priori bounded domain, or isolated fixed branch can be established.", "Bootstrap existence/selection status; not an unconditional scale theorem.", "CPU_FIRST"),
    (7, "Q07_NATIVE_TIME_SYSTEM", "METRIC_LED_IF_DYNAMICS_EXISTS", "J01;J11", "Derive the principal symbol, constraints, gauge sector, characteristics, and seal flux of the native time law before any evolution solve.", "No well-posed native initial-boundary system can be posed.", "Only then authorize bounded CPU time anchors; GPU remains downstream.", "CPU_THEN_OPTIONAL_GPU"),
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sources = read_tsv(SOURCE)
    by_family: dict[str, Counter[str]] = defaultdict(Counter)
    for row in sources:
        by_family[row["family"]][row["udt_join"]] += 1

    adjacency = []
    for family in FAMILIES:
        counts = by_family[family]
        adjacency.append({
            "family": family,
            "source_count": sum(counts.values()),
            "join_counts": ";".join(f"{join}:{counts[join]}" for join in sorted(counts)),
            "joins_touched": ";".join(sorted(counts)),
            "udt_objects": "; ".join(JOIN_OBJECTS[join] for join in sorted(counts)),
        })
    write_tsv(HERE / "UDT_ADJACENCY_MATRIX.tsv", list(adjacency[0]), adjacency)

    gates = [{
        "source_id": row["source_id"],
        "udt_join": row["udt_join"],
        "match_grade": row["match_grade"],
        "allowed_role": row["allowed_role"],
        "hypothesis_gate": row["indispensable_hypotheses"],
        "firewall_gate": row["firewall_prohibition"],
        "application_status": "GATED__NOT_APPLIED_AS_UDT_PHYSICS",
    } for row in sources]
    write_tsv(HERE / "APPLICABILITY_GATES.tsv", list(gates[0]), gates)

    convergence_rows = [dict(zip(
        ["convergence_id", "families", "convergent_lesson", "udt_use", "firewall_limit", "joins", "priority"], row
    )) for row in CONVERGENCE]
    write_tsv(HERE / "CROSS_FAMILY_CONVERGENCE.tsv", list(convergence_rows[0]), convergence_rows)

    missing_rows = [dict(zip(
        ["datum_id", "missing_datum", "required_type", "why_load_bearing", "joins", "status", "smallest_honest_next_test"], row
    )) for row in MISSING]
    write_tsv(HERE / "MISSING_DATUM_LEDGER.tsv", list(missing_rows[0]), missing_rows)

    question_rows = [dict(zip(
        ["rank", "question_id", "orientation", "joins", "bounded_question", "falsifier", "maximum_conclusion", "compute_class"], row
    )) for row in QUESTIONS]
    write_tsv(HERE / "RESEARCH_QUESTION_RANKING.tsv", list(question_rows[0]), question_rows)

    summary = {
        "status": "CENTURY_SCALE_COMPARATIVE_MATHEMATICS_ATLAS_CHARACTERIZED__NO_EXTERNAL_STRUCTURE_ADOPTED_AS_UDT",
        "source_count": len(sources),
        "family_count": len(set(row["family"] for row in sources)),
        "year_min": min(int(row["year"]) for row in sources),
        "year_max": max(int(row["year"]) for row in sources),
        "join_counts": dict(sorted(Counter(row["udt_join"] for row in sources).items())),
        "match_grade_counts": dict(sorted(Counter(row["match_grade"] for row in sources).items())),
        "role_counts": dict(sorted(Counter(row["allowed_role"] for row in sources).items())),
        "external_structures_adopted": 0,
        "physics_solves_run": 0,
        "gpu_runs": 0,
        "top_ranked_question": QUESTIONS[0][1],
    }
    (HERE / "BUILD_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
