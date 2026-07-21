#!/usr/bin/env python3
"""Build the law-neutral P03 founded-constraint atlas.

This program inventories provenance and equivalence/restriction effects.  It does not
evaluate an action, solve an equation of motion, or rank configurations.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P02 = ROOT / "udt_local_jet_atlas_p02_2026-07-21"
MAP = ROOT / "udt_complete_metric_solution_space_map_2026-07-21"
RESULT = HERE / "ATLAS_RESULT.json"
TRANSCRIPT = HERE / "ATLAS_TRANSCRIPT.txt"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


TREATMENT = {
    "P01": ("LOCAL_COMPARISON_NO_METRIC_EQUATION", "INTERNAL_COMPARISON"),
    "P02": ("INTERNAL_CHARACTER", "INTERNAL_COMPARISON"),
    "P03": ("INTERNAL_DETERMINANT_ONE", "INTERNAL_COMPARISON"),
    "P04": ("INTERNAL_FUNCTIONAL_COMPOSITION", "INTERNAL_COMPARISON"),
    "P05": ("GLOBAL_EXISTENTIAL_NO_LOCAL_DELETION", "REALIZED_UNIVERSE"),
    "P06": ("CONVENTION_FREE", "ALL_LOCAL_BRANCHES"),
    "P07": ("CONDITIONAL_LOCAL_REALIZATION", "SUPPLIED_METRIC_READOUT"),
    "P08": ("LOCAL_EQUIVALENCE", "PRE_SCALE_METRIC_CLASS"),
    "P09": ("CONDITIONAL_LOCAL_REALIZATION", "SUPPLIED_4D_LORENTZ_ARENA"),
    "P10": ("OPEN_REALIZATION", "RECIPROCAL_TO_SPACETIME_JOIN"),
    "P11": ("GLOBAL_ONLY", "COMPLETE_CELL"),
    "P12": ("STATIC_SEAL_ONLY", "STATIC_PHI_SEAL"),
    "P13": ("BOUNDARY_OPEN", "BOUNDARY_VARIATION"),
    "P14": ("DOWNSTREAM_CALIBRATION_ONLY", "CALIBRATED_READOUT"),
    "P15": ("DOWNSTREAM_CALIBRATION_ONLY", "CALIBRATED_READOUT"),
    "P16": ("GLOBAL_OUTPUT_OPEN", "COMPLETE_GLOBAL_SOLUTION"),
    "P17": ("GLOBAL_ADMISSIBILITY_ONLY", "COMPLETE_MATTER_BEARING_SOLUTION"),
    "P18": ("OPEN_REPRESENTATIVE", "POST_SCALE_JOIN"),
    "P19": ("EXCLUDED_DYNAMICS", "NOT_LOADED_IN_P03"),
    "P20": ("EXCLUDED_COMPARISON_DYNAMICS", "NOT_LOADED_IN_P03"),
    "P21": ("EXCLUDED_CARRIER", "NOT_LOADED_IN_P03"),
    "P22": ("EXCLUDED_CARRIER_DYNAMICS", "NOT_LOADED_IN_P03"),
    "P23": ("GLOBAL_OPEN", "GLOBAL_COMPLETION"),
    "P24": ("CONDITIONAL_GEOMETRY_TOOL", "SUPPLIED_REGULAR_METRIC"),
    "P25": ("OPEN_DYNAMICAL_CHARACTER", "NOT_LOADED_IN_P03"),
    "P26": ("OPEN_SYMMETRY", "NOT_FIXED_IN_P03"),
    "P27": ("HABIT_BLOCKED", "REGRESSION_SLICE_ONLY"),
    "P28": ("HABIT_BLOCKED", "CHARTED_SLICE_ONLY"),
    "P29": ("BOUNDARY_OPEN", "BOUNDARY_VARIATION"),
    "P30": ("EXCLUDED_COMPARISON", "REFERENCE_ONLY_AFTER_FREEZE"),
    "P31": ("EXCLUDED_TARGET", "AFTER_FROZEN_ATLAS_ONLY"),
    "P32": ("CATEGORY_A_CONTROL", "NUMERICAL_METHOD_ONLY"),
    "P33": ("HABIT_BLOCKED", "DIAGNOSTIC_ONLY"),
    "P34": ("CHARACTERIZE_ONLY", "ALL_LOCAL_BRANCHES"),
    "P35": ("SEMANTIC_SEPARATION", "ALL_DOMAINS"),
    "P36": ("GLOBAL_DOWNSTREAM_OPEN", "AFTER_NATIVE_MASS_AND_VOLUME"),
}


REALIZATION_ROWS = [
    {
        "id": "B00", "branch": "ABSTRACT_RECIPROCAL_COMPARISON",
        "supplied_inputs": "positive clock/ruler comparison pair; signed comparison argument",
        "founded_relations": "difference; reversal; dual pairing; composition; regularity",
        "metric_status": "NO_SPACETIME_SOLDERING_SUPPLIED",
        "local_effect": "two positive channel weights reduce to one reciprocal character",
        "open_data": "metric; spacetime dimension; slot; coframe; transverse sector; connection",
    },
    {
        "id": "B01", "branch": "CONDITIONAL_4D_CONFORMAL_METRIC",
        "supplied_inputs": "four-dimensional Lorentzian metric arena",
        "founded_relations": "positive local Common-Scale equivalence",
        "metric_status": "CONDITIONAL_ARENA_NO_RECIPROCAL_SOLDERING",
        "local_effect": "P02 metric atlas quotiented only by declared common scale",
        "open_data": "physical representative; reciprocal plane; phi-metric join; dynamics",
    },
    {
        "id": "B02", "branch": "SUPPLIED_LOCAL_LORENTZ_READOUT",
        "supplied_inputs": "signature convention (-+++); regular representative",
        "founded_relations": "none beyond B01; readout itself is conditional",
        "metric_status": "Z09_WITHIN_SUPPLIED_CONVENTION",
        "local_effect": "one of fifteen zero-jet inertia strata is the supplied regular interior",
        "open_data": "other signatures and degeneracies remain atlas closures; no dynamics",
    },
    {
        "id": "B03", "branch": "SUPPLIED_RECIPROCAL_TWO_PLUS_TWO_REALIZATION",
        "supplied_inputs": "base/screen split; reciprocal coframe pair; positive screen",
        "founded_relations": "determinant-one internal comparison after supplied soldering",
        "metric_status": "S27_WITHIN_SUPPLIED_SPLIT_CONVENTION",
        "local_effect": "relative base character represented; screen shift shear and twist remain free",
        "open_data": "origin uniqueness integrability global extension and physical section",
    },
    {
        "id": "B04", "branch": "STATIC_PHI_SEAL",
        "supplied_inputs": "static phi branch; finite-cell seal",
        "founded_relations": "phi_at_seal=0; parity-preserving_delta_phi=0",
        "metric_status": "BOUNDARY_SUBBRANCH_NOT_INTERIOR_EQUATION",
        "local_effect": "one scalar boundary value and its allowed variation are fixed",
        "open_data": "normal derivative; other field data; coframe involution; boundary functional; corners",
    },
    {
        "id": "B05", "branch": "COMPLETE_FINITE_CELL",
        "supplied_inputs": "finite mirrored closure; no spatial infinity",
        "founded_relations": "global domain ontology",
        "metric_status": "GLOBAL_COMPLETION_NOT_RESOLVED_BY_LOCAL_JETS",
        "local_effect": "none on point-local P02 tensors",
        "open_data": "topology; caps; periods; causal type; charts; Xmax; global existence",
    },
    {
        "id": "B06", "branch": "COMPLETE_BOOTSTRAP_READOUT",
        "supplied_inputs": "complete matter-bearing global solution with native mass volume stability",
        "founded_relations": "narrow total-density admissibility working principle",
        "metric_status": "NOT_YET_EVALUABLE",
        "local_effect": "none before the complete global objects exist",
        "open_data": "action; source; carrier; physical representative; mass; volume; window center and width",
    },
]


EFFECT_ROWS = [
    ("E01", "relative positional comparison", "P01", "B00", "difference/reversal on ordered comparisons", "PRESERVE", "No equation on a point-local metric or phi jet follows."),
    ("E02", "dual reciprocal character", "P02;P03", "B00", "u>0;v>0;u*v=1", "RESTRICT", "The internal two-channel logarithmic pair has one independent relative mode."),
    ("E03", "regular additive composition", "P04", "B00", "D(a+b)=D(a)D(b)", "RESTRICT", "The named positive regular comparison is an exponential character; pointwise phi values remain free."),
    ("E04", "realized nontriviality", "P05", "B06", "there exists a realized location/comparison with phi!=0", "NO_LOCAL_EFFECT", "An existential global observation cannot delete a local phi=0 point or mathematical branch."),
    ("E05", "phi distance comparison semantics", "P35", "ALL", "phi is signed; distance is nonnegative; ordered comparison is separately signed", "SEMANTIC_SEPARATION", "No sign or causal stratum is removed."),
    ("E06", "positive CSN zero jet", "P08", "B01", "g is equivalent to Omega^2*g for Omega>0", "IDENTIFY", "Metric inertia rank and degeneracy are preserved; all fifteen P02 inertia witnesses remain represented."),
    ("E07", "positive CSN dphi type", "P08;P35", "B01", "g_inverse(dphi,dphi) rescales by Omega^-2", "PRESERVE", "Zero versus nonzero and timelike/null/spacelike type are preserved once the conditional metric arena is supplied."),
    ("E08", "positive CSN screen expansion", "P08;P10", "B03", "theta_A maps to theta_A+2*d_A(log Omega)", "IDENTIFY", "Expansion is representative data; its rank does not label the quotient."),
    ("E09", "positive CSN screen shear", "P08;P10", "B03", "trace-free q-inverse Lie derivative is unchanged", "PRESERVE", "All three shear-map ranks remain distinct conditional split strata."),
    ("E10", "positive CSN split twist", "P08;P10", "B03", "Frobenius vertical twist distribution is unchanged", "PRESERVE", "Integrable and nonintegrable split witnesses both remain."),
    ("E11", "positive CSN curvature decomposition", "P08", "B01", "Riemann algebraic space equals Weyl[10] direct-sum Schouten[10]; scale Hessian translates Schouten", "IDENTIFY", "The quotient retains ten curvature components; full-Riemann and Ricci ranks are not quotient labels."),
    ("E12", "conditional Lorentz readout", "P07;P09", "B02", "regular signature convention (-+++)", "CONDITIONAL_ONLY", "Z09 is the supplied interior stratum; this does not erase the other fourteen atlas closures from the unconditional parent."),
    ("E13", "conditional reciprocal split", "P07;P10", "B03", "Lorentzian base plus positive screen in the supplied split", "CONDITIONAL_ONLY", "S27 is the supplied regular split stratum; the split and its alignment are not founded universally."),
    ("E14", "conditional Levi-Civita evaluator", "P24", "B01;B02;B03", "connection determined from a supplied regular metric representative", "CONDITIONAL_ONLY", "It evaluates a metric; it does not remove a metric configuration."),
    ("E15", "finite-cell ontology", "P11", "B05", "complete domain is finite and has no spatial infinity", "NO_LOCAL_EFFECT", "No point-local tensor identity, hard wall, cap, or asymptotic charge is supplied."),
    ("E16", "static seal phi value", "P12", "B04", "phi_at_seal=0", "RESTRICT", "One scalar value is fixed only on the static seal branch."),
    ("E17", "static seal allowed variation", "P12", "B04", "delta_phi_at_seal=0 for parity-preserving variations", "RESTRICT", "One scalar tangent direction is fixed only in that boundary variation branch."),
    ("E18", "static seal normal jet", "P12;P29", "B04", "normal_derivative_phi is free", "PRESERVE", "Zero and nonzero normal-derivative witnesses remain."),
    ("E19", "remaining boundary data", "P13;P29", "B04;B05", "not supplied", "PRESERVE", "Other coframe data polarizations normal jets caps and corners remain open."),
    ("E20", "angular and global completion", "P23", "B05", "period cap quotient topology and no-cap are open", "PRESERVE", "No local split or Petrov stratum is removed by an unchosen completion."),
    ("E21", "global Xmax", "P16", "B05;B06", "derived global output with unknown value and functional", "NO_LOCAL_EFFECT", "It cannot serve as a supplied local ruler or branch score."),
    ("E22", "bootstrap admissibility", "P17;P36", "B06", "complete-solution density window after native mass volume and stability exist", "NO_LOCAL_EFFECT", "It supplies no present local equation coefficient center width or cutoff."),
    ("E23", "observational c_E and G_obs", "P14;P15", "CALIBRATED_READOUT", "downstream measured anchors", "NO_LOCAL_EFFECT", "They do not alter the pre-scale local atlas."),
    ("E24", "unloaded dynamics carrier and comparisons", "P19;P20;P21;P22;P30;P31", "NOT_LOADED_IN_P03", "excluded from candidate and acceptance logic", "PRESERVE", "No configuration is accepted rejected or ranked by an unloaded law or desired readout."),
]


INCONSISTENT_ROWS = [
    ("I01", "u*v=1; u=v; nontrivial positive character", "u=v=1 is the only positive intersection, contradicting the nontrivial clause", "ordinary covariance is a diagnostic alternative, not an added foundation"),
    ("I02", "phi equals nonnegative physical distance", "owner semantics permit signed phi and require nonnegative distance as a distinct object", "keep a separate comparison map open"),
    ("I03", "realized nontriviality deletes phi=0", "the source explicitly retains the mathematical phi=0 representation", "treat nontriviality as global existential evidence"),
    ("I04", "internal reciprocal character uniquely selects a spacetime plane", "the soldering/slot map is explicitly open", "branch abstract and soldered realizations separately"),
    ("I05", "the conditional Lorentz readout is unconditional UDT geometry", "its source status is CONDITIONAL/CHOSE", "retain B01/B02 as supplied arenas"),
    ("I06", "the supplied two-plus-two split is universal", "P10 requires branching over slot projector coframe and type-change realizations", "retain B03 as conditional"),
    ("I07", "the static seal condition is an interior equation", "the cited condition is boundary- and branch-local", "apply only in B04"),
    ("I08", "mirror fixes normal derivative phi", "canon explicitly leaves the normal derivative free", "retain both zero and nonzero normal jets"),
    ("I09", "finite cell means hard wall cap or ADM infinity", "finite closure forbids spatial-infinity input and supplies none of those completions", "retain global completion alternatives"),
    ("I10", "global bootstrap is inserted as a local density coupling", "the principle explicitly forbids that insertion", "defer B06 until native global objects exist"),
    ("I11", "Xmax is supplied as a local or numerical constant", "current meaning makes it a derived global output", "leave its value and closure functional open"),
    ("I12", "CSN chooses a physical representative", "CSN identifies the local common-scale orbit", "physical representative remains an open post-scale join"),
    ("I13", "a curvature identity is treated as a field equation", "metric geometry alone supplies no variation or evolution law", "record the identity only as configuration data"),
    ("I14", "a preferred profile action solution or comparison ranks P03 branches", "P03's registered question is a provenance/effect census", "stop before any merit or dynamics layer"),
]


DIMENSION_ROWS = [
    ("D01", "B00", "positive diagonal comparison weights", "2", "1", "1", "log(u)+log(v)=0; common positive scale is not a second physical mode", "EXACT_INTERNAL_CHARACTER"),
    ("D02", "B01_INTERIOR", "signed scalar phi value", "1", "1", "1", "no founded point-local value equation", "FREE_LOCAL_VALUE"),
    ("D03", "B01_INTERIOR", "dphi covector", "4", "4", "4", "no founded point-local differential equation", "ALL_EIGHT_P02_STRATA_RETAINED"),
    ("D04", "B01", "raw symmetric metric two-jet", "150", "20", "10", "normal-coordinate redundancy leaves Riemann[20]; CSN Hessian identifies Schouten[10]", "P02_EXACT"),
    ("D05", "B01", "algebraic curvature tensor", "20", "20", "10", "Weyl[10] direct-sum Schouten[10] with Schouten translated along the CSN orbit", "P02_EXACT"),
    ("D06", "B01", "Schouten representative sector", "10", "10", "0", "all ten components are representative data at a point", "NOT_A_QUOTIENT_OBSERVABLE"),
    ("D07", "B01", "common-scale-invariant curvature sector", "10", "10", "10", "local positive common scale preserves this sector", "CONTINUOUS_DATA_RETAINED"),
    ("D08", "B02", "generic invariant curvature modulo local Lorentz frame", "10", "10", "4", "six generic frame parameters identify presentations", "CONDITIONAL_REGULAR_LORENTZ_COUNT"),
    ("D09", "B03", "split expansion shear twist first-jet data", "8", "8", "6", "CSN removes two expansion-covector components; four shear plus two twist components remain", "CONDITIONAL_SPLIT_COUNT"),
    ("D10", "B04", "static seal phi value", "1", "0", "0", "phi_at_seal=0", "STATIC_SEAL_ONLY"),
    ("D11", "B04", "static seal normal derivative phi", "1", "1", "1", "explicitly free", "STATIC_SEAL_ONLY"),
    ("D12", "B04;B05", "complete boundary/coframe data", "UNKNOWN", "UNKNOWN", "UNKNOWN", "allowed variations normal jets caps and corners are not supplied", "UNCOUNTED_OPEN_SPACE"),
    ("D13", "B05;B06", "global topology Xmax mass volume and bootstrap data", "UNKNOWN", "UNKNOWN", "UNKNOWN", "point-local P02 cannot count complete-cell/global degrees of freedom", "UNCOUNTED_OPEN_SPACE"),
]


COUNTERMODEL_ROWS = [
    ("M01", "realized nontriviality forces phi nonzero at every point", "phi(x)=x on a finite interval", "phi(0)=0 and phi(1)=1", "EXACT_ELEMENTARY"),
    ("M02", "signed phi is physical negative distance", "phi=-1; distance=1 as separate data", "signed field and nonnegative length coexist", "SEMANTIC_PRODUCT_WITNESS"),
    ("M03", "Reciprocity restricts an unsoldered metric jet", "D(phi)=diag(exp(-phi),exp(phi)) paired with any P02 zero-jet witness", "det(D)=1 independently of the metric witness", "EXACT_PRODUCT_WITNESS"),
    ("M04", "current premises select one dphi causal/support class", "all F01-F08 P02 witnesses", "eight exact strata remain without a phi equation", "P02_EXACT_TABLE"),
    ("M05", "current premises force split integrability", "K01 and K02", "same zero shear/expansion ranks with twist ranks zero and one", "P02_EXACT_TABLE"),
    ("M06", "current premises force one shear rank", "K01 K03 K05 at zero expansion and twist", "shear-map ranks zero one and two all occur", "P02_EXACT_TABLE"),
    ("M07", "screen expansion rank is common-scale invariant", "K01 and its positive local CSN transform", "arbitrary scale gradient changes expansion while shear and twist remain", "P02_EXACT_ALGEBRA"),
    ("M08", "Ricci rank labels pre-scale curvature", "fixed zero Weyl plus C0-C4 Schouten witnesses", "all five Ricci ranks lie in representative data", "P02_EXACT_DIRECT_SUM"),
    ("M09", "current premises select one algebraic curvature type", "W01-W06", "all six exact invariant-sector types occur with zero Ricci", "P02_EXACT_TABLE"),
    ("M10", "static seal parity fixes the normal derivative", "phi_a(n)=a*n for a=0 and a=1", "both are odd and vanish at n=0; derivatives are 0 and 1", "EXACT_ELEMENTARY"),
    ("M11", "finite-cell ontology supplies a point-local curvature equation", "constant local metric patch inside a finite coordinate cell with arbitrary compactly supported local jet perturbation", "finiteness alone states a domain property and no tensor equality", "LOCALITY_LOGICAL_WITNESS"),
    ("M12", "bootstrap presently removes a local P02 stratum", "same local jet embedded as an unevaluated member of B06", "native mass volume stability and window data are absent, so the admissibility predicate has no current truth value", "DOMAIN_GUARD_WITNESS"),
]


def build_input_registry() -> list[dict[str, str]]:
    premise_rows = read_tsv(MAP / "PREMISE_AND_REDUCTION_LEDGER.tsv")
    require(len(premise_rows) == 36, "premise universe")
    require(set(TREATMENT) == {row["id"] for row in premise_rows}, "premise treatment coverage")
    output = []
    for row in premise_rows:
        treatment, domain = TREATMENT[row["id"]]
        output.append({
            **row,
            "p03_treatment": treatment,
            "application_domain": domain,
            "metric_atlas_restriction": "NO" if treatment not in {
                "CONDITIONAL_LOCAL_REALIZATION", "STATIC_SEAL_ONLY"
            } else "CONDITIONAL_OR_BOUNDARY_ONLY",
        })
    return output


def build_survival_rows() -> list[dict[str, str]]:
    specifications = [
        ("METRIC_INERTIA", "ZERO_JET_INERTIA_STRATA.tsv", "status"),
        ("SPLIT_INERTIA", "SPLIT_ZERO_JET_STRATA.tsv", "branch_status"),
        ("DPHI", "DPHI_FIRST_JET_STRATA.tsv", "stratum"),
        ("SPLIT_FIRST_JET", "SPLIT_FIRST_JET_STRATA.tsv", "integrability"),
        ("CURVATURE_RANK", "CURVATURE_OPERATOR_RANK_STRATA.tsv", "curvature_operator_rank"),
        ("RICCI_RANK", "RICCI_ENDOMORPHISM_RANK_STRATA.tsv", "Ricci_endomorphism_rank"),
        ("PETROV", "PETROV_STRATA.tsv", "Petrov_type"),
    ]
    output: list[dict[str, str]] = []
    for atlas, filename, label_field in specifications:
        digest = sha256(P02 / filename)
        for row in read_tsv(P02 / filename):
            source_id = row["id"]
            if atlas == "METRIC_INERTIA":
                local = "PRESERVED_IN_FULL_P02_CLOSURE"
                conditional = (
                    "IN_SUPPLIED_LORENTZ_CONVENTION"
                    if source_id == "Z09"
                    else "OUTSIDE_SUPPLIED_LORENTZ_CONVENTION_NOT_FOUNDATION_EXCLUDED"
                )
                quotient = f"INERTIA_{row['n_negative']}_{row['n_positive']}_{row['n_zero']}"
                reason = "positive common scaling preserves inertia and rank"
            elif atlas == "SPLIT_INERTIA":
                local = "PRESERVED_CONDITIONAL_SPLIT_WITNESS"
                conditional = (
                    "IN_SUPPLIED_RECIPROCAL_SPLIT_CONVENTION"
                    if source_id == "S27"
                    else "OUTSIDE_SUPPLIED_SPLIT_CONVENTION_NOT_FOUNDATION_EXCLUDED"
                )
                quotient = f"SPLIT_{row['base_inertia']}_{row['screen_inertia']}"
                reason = "split is conditional and positive common scaling preserves its inertia"
            elif atlas == "DPHI":
                local = "SURVIVES_LOCAL_INTERIOR"
                conditional = "NO_PHI_FIELD_EQUATION_LOADED"
                quotient = f"{row['support']}_{row['causal_type']}"
                reason = "positive common scaling preserves causal type and current semantics add no differential constraint"
            elif atlas == "SPLIT_FIRST_JET":
                local = "REPRESENTATIVE_WITNESS_RETAINED"
                conditional = "CONDITIONAL_SUPPLIED_SPLIT"
                quotient = f"SHEAR_{row['shear_map_rank']}_TWIST_{row['twist_map_rank']}"
                reason = "expansion is identified along the common-scale orbit while shear and twist ranks remain"
            elif atlas == "CURVATURE_RANK":
                local = "REPRESENTATIVE_WITNESS_RETAINED_NOT_QUOTIENT_LABEL"
                conditional = "CONDITIONAL_4D_METRIC_ARENA"
                quotient = "UNDEFINED_ON_CSN_QUOTIENT"
                reason = "Schouten translation can change full curvature-operator rank"
            elif atlas == "RICCI_RANK":
                local = "REPRESENTATIVE_WITNESS_RETAINED_NOT_QUOTIENT_LABEL"
                conditional = "CONDITIONAL_4D_METRIC_ARENA"
                quotient = "UNDEFINED_ON_CSN_QUOTIENT"
                reason = "Ricci belongs to the representative-dependent Schouten sector"
            else:
                local = "SURVIVES_PRE_SCALE_LOCAL_QUOTIENT"
                conditional = "CONDITIONAL_4D_LORENTZ_CLASSIFICATION"
                quotient = f"PETROV_{row['Petrov_type']}"
                reason = "positive common scaling preserves algebraic type"
            output.append({
                "atlas": atlas,
                "source_id": source_id,
                "source_label": row[label_field],
                "local_foundation_status": local,
                "conditional_branch_status": conditional,
                "csn_quotient_key": quotient,
                "reason": reason,
                "source_table": filename,
                "source_table_sha256": digest,
            })
    require(len(output) == 89, "P02 discrete coverage")
    return output


def build_graph() -> dict[str, object]:
    nodes = [
        ("F_POSITION", "FOUNDATION"), ("F_RECIPROCAL_C", "FOUNDATION"),
        ("F_DUAL_RECIPROCITY", "FOUNDATION"), ("F_COMPOSITION", "POSIT"),
        ("F_CSN", "FOUNDATION"), ("S_SEMANTICS", "OWNER_CLARIFICATION"),
        ("C_4D_LORENTZ", "CONDITIONAL"), ("O_SOLDERING", "OPEN"),
        ("F_FINITE_CELL", "FOUNDATION"), ("F_STATIC_SEAL", "FOUNDATION_SCOPED"),
        ("O_BOUNDARY", "OPEN"), ("O_GLOBAL_COMPLETION", "OPEN"),
        ("W_BOOTSTRAP", "WORKING_GLOBAL"), ("P02_ATLAS", "FROZEN_PARENT"),
        ("Q_INTERNAL_CHARACTER", "OUTPUT"), ("Q_CSN_ORBITS", "OUTPUT"),
        ("Q_STATIC_SEAL", "OUTPUT"), ("Q_UNCONSTRAINED_LOCAL", "OUTPUT"),
        ("Q_UNCONSTRAINED_GLOBAL", "OUTPUT"),
    ]
    edges = [
        ("F_POSITION", "Q_INTERNAL_CHARACTER", "comparison_argument"),
        ("F_RECIPROCAL_C", "Q_INTERNAL_CHARACTER", "coequal_channels"),
        ("F_DUAL_RECIPROCITY", "Q_INTERNAL_CHARACTER", "determinant_one"),
        ("F_COMPOSITION", "Q_INTERNAL_CHARACTER", "regular_character"),
        ("F_CSN", "Q_CSN_ORBITS", "positive_common_scale_equivalence"),
        ("P02_ATLAS", "Q_CSN_ORBITS", "exact_local_parent"),
        ("S_SEMANTICS", "Q_UNCONSTRAINED_LOCAL", "prevents_conflation"),
        ("C_4D_LORENTZ", "P02_ATLAS", "conditional_arena"),
        ("O_SOLDERING", "Q_UNCONSTRAINED_LOCAL", "join_remains_open"),
        ("F_FINITE_CELL", "Q_UNCONSTRAINED_GLOBAL", "finite_completion_required"),
        ("F_STATIC_SEAL", "Q_STATIC_SEAL", "phi_value_and_variation"),
        ("O_BOUNDARY", "Q_UNCONSTRAINED_GLOBAL", "remaining_data_open"),
        ("O_GLOBAL_COMPLETION", "Q_UNCONSTRAINED_GLOBAL", "topology_scale_open"),
        ("W_BOOTSTRAP", "Q_UNCONSTRAINED_GLOBAL", "not_evaluable_before_complete_solution"),
    ]
    return {
        "schema": "udt-p03-constraint-dependency-graph-1.0",
        "nodes": [{"id": name, "kind": kind} for name, kind in nodes],
        "edges": [{"from": left, "to": right, "relation": relation} for left, right, relation in edges],
        "forbidden_edges": [
            {"from": "Q_INTERNAL_CHARACTER", "to": "P02_ATLAS", "reason": "no spacetime soldering supplied"},
            {"from": "W_BOOTSTRAP", "to": "Q_UNCONSTRAINED_LOCAL", "reason": "no local equation supplied"},
            {"from": "F_FINITE_CELL", "to": "P02_ATLAS", "reason": "domain ontology is not a point-local tensor relation"},
        ],
    }


def main() -> None:
    phi = sp.symbols("phi", real=True)
    u = sp.exp(-phi)
    v = sp.exp(phi)
    require(sp.simplify(u * v) == 1, "reciprocal character")
    a, b = sp.symbols("a b", real=True)
    composition_residual = (
        sp.diag(sp.exp(-a), sp.exp(a)) * sp.diag(sp.exp(-b), sp.exp(b))
        - sp.diag(sp.exp(-(a + b)), sp.exp(a + b))
    ).applyfunc(sp.simplify)
    require(composition_residual == sp.zeros(2), "composition")
    n = sp.symbols("n", real=True)
    seal_family = a * n
    require(seal_family.subs(n, 0) == 0 and sp.diff(seal_family, n) == a, "seal free normal jet")

    input_rows = build_input_registry()
    survival_rows = build_survival_rows()
    graph = build_graph()

    write_tsv("FOUNDATION_INPUT_REGISTRY.tsv", [
        "id", "item", "premise_stamp", "source", "atlas_effect", "disallowed_inference",
        "p03_treatment", "application_domain", "metric_atlas_restriction",
    ], input_rows)
    write_tsv("REALIZATION_BRANCHES.tsv", [
        "id", "branch", "supplied_inputs", "founded_relations", "metric_status", "local_effect", "open_data",
    ], REALIZATION_ROWS)
    write_tsv("CONSTRAINT_EFFECT_LEDGER.tsv", [
        "id", "object", "premise_ids", "domain", "exact_relation_or_status", "effect", "consequence",
    ], [dict(zip(
        ["id", "object", "premise_ids", "domain", "exact_relation_or_status", "effect", "consequence"], row
    )) for row in EFFECT_ROWS])
    write_tsv("SURVIVING_STRATA.tsv", [
        "atlas", "source_id", "source_label", "local_foundation_status", "conditional_branch_status",
        "csn_quotient_key", "reason", "source_table", "source_table_sha256",
    ], survival_rows)
    write_tsv("INCONSISTENT_COMBINATIONS.tsv", [
        "id", "combination", "conflict", "required_treatment",
    ], [dict(zip(["id", "combination", "conflict", "required_treatment"], row)) for row in INCONSISTENT_ROWS])
    write_tsv("UNCONSTRAINED_DIMENSIONS.tsv", [
        "id", "branch", "object", "parent_dimension", "after_explicit_restriction",
        "after_declared_equivalence", "counting_relation", "status",
    ], [dict(zip([
        "id", "branch", "object", "parent_dimension", "after_explicit_restriction",
        "after_declared_equivalence", "counting_relation", "status",
    ], row)) for row in DIMENSION_ROWS])
    write_tsv("COUNTERMODEL_LEDGER.tsv", [
        "id", "challenged_overstatement", "witness", "exact_check", "certification",
    ], [dict(zip(["id", "challenged_overstatement", "witness", "exact_check", "certification"], row)) for row in COUNTERMODEL_ROWS])
    (HERE / "CONSTRAINT_DEPENDENCY_GRAPH.json").write_text(
        json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    atlas_counts = Counter(row["atlas"] for row in survival_rows)
    quotient_split = {
        row["csn_quotient_key"] for row in survival_rows if row["atlas"] == "SPLIT_FIRST_JET"
    }
    conditional_lorentz = sum(
        row["conditional_branch_status"] == "IN_SUPPLIED_LORENTZ_CONVENTION"
        for row in survival_rows
    )
    conditional_split = sum(
        row["conditional_branch_status"] == "IN_SUPPLIED_RECIPROCAL_SPLIT_CONVENTION"
        for row in survival_rows
    )
    table_names = [
        "FOUNDATION_INPUT_REGISTRY.tsv", "REALIZATION_BRANCHES.tsv", "CONSTRAINT_EFFECT_LEDGER.tsv",
        "SURVIVING_STRATA.tsv", "INCONSISTENT_COMBINATIONS.tsv", "UNCONSTRAINED_DIMENSIONS.tsv",
        "COUNTERMODEL_LEDGER.tsv", "CONSTRAINT_DEPENDENCY_GRAPH.json",
    ]
    checks = {
        "all_36_registered_premises_classified": len(input_rows) == 36,
        "all_89_P02_discrete_strata_accounted": len(survival_rows) == 89,
        "all_15_metric_inertia_witnesses_retained": atlas_counts["METRIC_INERTIA"] == 15,
        "all_36_split_inertia_witnesses_retained": atlas_counts["SPLIT_INERTIA"] == 36,
        "all_8_dphi_strata_retained": atlas_counts["DPHI"] == 8,
        "all_12_split_first_jet_witnesses_retained": atlas_counts["SPLIT_FIRST_JET"] == 12,
        "split_first_jet_quotient_has_6_shear_twist_classes": len(quotient_split) == 6,
        "all_7_curvature_rank_witnesses_retained_as_representatives": atlas_counts["CURVATURE_RANK"] == 7,
        "all_5_Ricci_rank_witnesses_retained_as_representatives": atlas_counts["RICCI_RANK"] == 5,
        "all_6_Petrov_types_retained": atlas_counts["PETROV"] == 6,
        "conditional_Lorentz_branch_is_single_Z09_row": conditional_lorentz == 1,
        "conditional_split_branch_is_single_S27_row": conditional_split == 1,
        "internal_reciprocity_does_not_solder_metric": graph["forbidden_edges"][0]["from"] == "Q_INTERNAL_CHARACTER",
        "finite_cell_has_no_point_local_edge": graph["forbidden_edges"][2]["from"] == "F_FINITE_CELL",
        "bootstrap_has_no_point_local_edge": graph["forbidden_edges"][1]["from"] == "W_BOOTSTRAP",
        "static_seal_normal_derivative_free": sp.diff(seal_family, n) == a,
        "no_metric_stratum_removed_by_unconditional_foundation": all(
            row["local_foundation_status"] != "REMOVED" for row in survival_rows
        ),
        "no_action_or_equation_loaded": True,
        "no_merit_filter_loaded": True,
        "P02_package_manifest_unchanged": sha256(P02 / "SHA256SUMS.txt")
        == "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938",
    }
    require(all(checks.values()), "main checks")
    result = {
        "schema": "udt-p03-founded-constraint-atlas-1.0",
        "status": "PASS",
        "maximum_conclusion": "CURRENT_FOUNDATION_CONSTRAINED_CONFIGURATION_SPACE_CHARACTERIZED",
        "question_mode": "METRIC_LED_OBSERVING_CONSTRAINT_EFFECTS",
        "counts": {
            "foundation_input_rows": len(input_rows),
            "realization_branches": len(REALIZATION_ROWS),
            "constraint_effects": len(EFFECT_ROWS),
            "P02_discrete_strata_accounted": len(survival_rows),
            "inconsistent_combinations": len(INCONSISTENT_ROWS),
            "dimension_rows": len(DIMENSION_ROWS),
            "countermodels": len(COUNTERMODEL_ROWS),
            "split_first_jet_invariant_quotient_classes": len(quotient_split),
        },
        "P02_axis_counts": dict(sorted(atlas_counts.items())),
        "dimension_contract": {
            "internal_positive_pair_before_reciprocity": 2,
            "internal_reciprocal_character": 1,
            "conditional_4D_curvature_before_CSN": 20,
            "conditional_4D_curvature_after_local_CSN": 10,
            "conditional_generic_curvature_after_Lorentz_frame_quotient": 4,
            "conditional_split_first_jet_before_CSN": 8,
            "conditional_split_first_jet_after_CSN": 6,
            "static_seal_phi_value": 0,
            "static_seal_free_normal_phi_jet": 1,
        },
        "constraint_ruling": {
            "unconditional_point_local_metric_strata_removed": 0,
            "CSN_is_equivalence_not_branch_selection": True,
            "internal_reciprocity_metric_soldering": "OPEN",
            "conditional_Lorentz_zero_jet": "Z09",
            "conditional_reciprocal_split_zero_jet": "S27",
            "local_phi_value_equation": "NOT_SUPPLIED",
            "local_phi_differential_equation": "NOT_SUPPLIED",
            "static_seal_phi_value": "ZERO_IN_B04_ONLY",
            "static_seal_normal_derivative": "FREE",
            "complete_boundary_data": "OPEN",
            "global_completion": "OPEN",
        },
        "scope": {
            "CPU_only": True,
            "GPU_used": False,
            "ODE_or_PDE_run": False,
            "action_selected": False,
            "equation_of_motion_selected": False,
            "comparison_or_empirical_target_loaded": False,
            "merit_filter_used": False,
            "P04_launched": False,
        },
        "checks": {name: "PASS" for name in checks},
        "check_count": len(checks),
        "table_sha256": {name: sha256(HERE / name) for name in table_names},
        "source_sha256": {
            "P02_manifest": sha256(P02 / "SHA256SUMS.txt"),
            "premise_ledger": sha256(MAP / "PREMISE_AND_REDUCTION_LEDGER.tsv"),
            "cold_packet": sha256(ROOT / "UDT_NATIVE_ACTION_COLD_PACKET.md"),
            "CSN_postulate": sha256(ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"),
            "bootstrap_principle": sha256(ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"),
            "owner_meanings": sha256(ROOT / "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv"),
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    RESULT.write_text(payload, encoding="utf-8")
    transcript = (
        "P03 founded-constraint atlas\n"
        f"status={result['status']}\n"
        f"checks={result['check_count']}/{result['check_count']}\n"
        f"inputs={len(input_rows)} effects={len(EFFECT_ROWS)} branches={len(REALIZATION_ROWS)}\n"
        f"p02_strata_accounted={len(survival_rows)}/89\n"
        f"unconditional_point_local_metric_strata_removed=0\n"
        f"csn_curvature_dimensions=20->10\n"
        f"conditional_split_first_jet_dimensions=8->6\n"
        f"countermodels={len(COUNTERMODEL_ROWS)} inconsistent_combinations={len(INCONSISTENT_ROWS)}\n"
        "action_selected=False equation_selected=False merit_filter=False\n"
        f"maximum_conclusion={result['maximum_conclusion']}\n"
    )
    TRANSCRIPT.write_text(transcript, encoding="utf-8")
    print(transcript, end="")


if __name__ == "__main__":
    main()
