#!/usr/bin/env python3
"""Exact bounded architecture and ownership atlas for the UDT native-law question."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def write_tsv(name: str, fields: tuple[str, ...], rows: list[tuple[str, ...]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)


def exact_algebra() -> dict[str, object]:
    phi, psi, z = sp.symbols("phi psi z", real=True)
    D = lambda x: sp.diag(sp.exp(-x), sp.exp(x))
    K = sp.Matrix([[0, 1], [1, 0]])
    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    eta = sp.diag(1, -1)
    checks: list[bool] = []
    checks += [sp.simplify(D(phi) * D(psi) - D(phi + psi)) == sp.zeros(2)]
    checks += [sp.simplify(D(phi).det()) == 1]
    checks += [sp.simplify(D(phi).T * K * D(phi) - K) == sp.zeros(2)]
    checks += [sp.simplify(D(-phi) * D(phi)) == sp.eye(2)]
    boost = sp.simplify(H.T * D(phi) * H)
    checks += [sp.simplify(boost - sp.Matrix([[sp.cosh(phi), -sp.sinh(phi)], [-sp.sinh(phi), sp.cosh(phi)]])) == sp.zeros(2)]
    checks += [sp.simplify(boost.T * eta * boost - eta) == sp.zeros(2)]

    P01 = sp.diag(1, 1, 0, 0)
    P02 = sp.diag(1, 0, 1, 0)
    R = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    A = sp.diag(2, 3, 5, 7)
    checks += [R * P01 * R.inv() == P02]
    checks += [P01 != P02]
    query_values = [sp.trace(P01 * A), sp.trace(P02 * A)]
    checks += [query_values == [5, 7]]
    checks += [sp.trace((R * P01 * R.inv()) * (R * A * R.inv())) == sp.trace(P01 * A)]
    checks += [sp.trace(A) == sp.trace(R * A * R.inv()) == 17]
    checks += [sp.trace(P01) == sp.trace(P02) == 2]

    # Regular branch-derived spectral projector: its derivative is owned by the parent matrix.
    W = sp.zeros(4)
    W[1, 2] = W[2, 1] = 1
    Pprime = sp.zeros(4)
    Pprime[1, 2] = Pprime[2, 1] = sp.Rational(-1, 2)
    B = W
    branch_chain = sp.trace(Pprime * B)
    checks += [P01 * P01 == P01]
    checks += [P01.T == P01]
    checks += [branch_chain == -1]
    checks += [sp.trace(Pprime) == 0]
    checks += [(A[1, 1] - A[2, 2]) * Pprime[1, 2] == 1]

    # At a repeated spatial eigenvalue, two isometry-related regular limits disagree.
    A_collision = sp.diag(2, 4, 4, 7)
    checks += [R * A_collision * R.inv() == A_collision]
    checks += [R * P01 * R.inv() == P02 and P01 != P02]

    # Registered conditional WR-L SNe readout join; no data fitting occurs here.
    u = 1 + z
    r_over_X = 1 - u ** -2
    dl_over_X = sp.factor(sp.simplify(u**2 * r_over_X))
    checks += [sp.simplify(dl_over_X - z * (z + 2)) == 0]
    checks += [sp.simplify(dl_over_X.subs(z, 0)) == 0]
    checks += [sp.simplify(dl_over_X.subs(z, 1)) == 3]
    checks += [sp.simplify(sp.diff(dl_over_X, z) - (2 * z + 2)) == 0]

    # Type-level controls are exact finite assertions, not physical equations.
    checks += [len({"clock", "areal", "optical", "proper_pair"}) == 4]
    checks += [query_values[0] != query_values[1]]
    checks += [branch_chain != 0]
    failed = [index for index, check in enumerate(checks, start=1) if check is not True and check != sp.true]
    assert not failed, failed
    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "reciprocal_pair_query_values": [str(v) for v in query_values],
        "basic_trace": "17",
        "branch_selector_chain_term": str(branch_chain),
        "collision_limits_distinct": True,
        "sne_conditional_shape": str(dl_over_X),
        "sne_readout_slots": ["clock", "areal", "optical", "proper_pair"],
    }


LAW_CLASSES = [
    ("K01", "FOUNDED_RECIPROCAL_COMPARISON", "ordered pair/path query plus signed depth", "morphism of reciprocal pair fibers / O(1,1) character"),
    ("K02", "AMBIENT_METRIC_GEOMETRY", "metric/coframe on M", "metric connection curvature causal and identity objects on M"),
    ("K03", "PAIR_RESOLVED_RESPONSE", "ambient geometry plus ordered reciprocal query", "associated screen mixing projected-response objects over query space"),
    ("K04", "NATIVE_DYNAMICAL_CLOSURE", "admissible complete configuration and jets or disclosed nonlocal data", "covariant residual constraint evolution or variational dual object"),
    ("K05", "GLOBAL_BOOTSTRAP_ADMISSIBILITY", "one complete on-shell solution and native global/local observables", "relation subset or compatibility value on global-local observable space"),
    ("K06", "BOUNDARY_COMPLETION", "bulk/query/reduction data restricted to boundary seal corner or defect", "boundary response polarization gluing flux or admissibility object"),
]


def architecture_atlas() -> list[tuple[str, ...]]:
    home = {
        "H01": ("M", "base tensor/density or equation bundle", "ambient metric/coframe or declared base fields"),
        "H02": ("P or observer/path groupoid", "equivariant associated-bundle section or typed morphism", "base fields only; queries are arguments"),
        "H03": ("configuration of (g,s)", "base plus section-field response", "independent delta_g and delta_s after ownership is supplied"),
        "H04": ("regular branch with s=S[g]", "composite base response", "delta_g with delta_s=DS_g[delta_g]"),
        "H05": ("stratified union of regular and singular homes", "stratum response plus open interface/gluing object", "stratum tangent or tangent-cone/interface owner"),
        "H06": ("M after query-fiber aggregation", "averaged or quotiented base object", "metric plus measure/weight data if derived"),
        "H07": ("typed diagram of M P reductions and strata", "tuple/diagram preserving each codomain", "owner attached to each component"),
        "H08": ("outside current universe", "unclassified", "unclassified"),
    }
    availability = {
        "H01": {"K01": "DOWNSTREAM_READOUT_ONLY", "K02": "DERIVED_NATURAL_HOME", "K03": "GENERICALLY_INSUFFICIENT_ALONE", "K04": "ADMISSIBLE_NOT_SELECTED", "K05": "ADMISSIBLE_GLOBAL_OUTPUT_NOT_DERIVED", "K06": "BASE_BOUNDARY_ONLY"},
        "H02": {"K01": "DERIVED_NATURAL_HOME", "K02": "BASIC_PULLBACK_AVAILABLE", "K03": "DERIVED_TYPE_HOME_LAW_ABSENT", "K04": "ADMISSIBLE_NOT_SELECTED", "K05": "QUERY_FAMILY_AVAILABLE_GLOBAL_JOIN_OPEN", "K06": "QUERY_BOUNDARY_AVAILABLE_POLARIZATION_OPEN"},
        "H03": {"K01": "CONDITIONAL_SECTION_EVALUATION", "K02": "BASIC_COMPONENT_AVAILABLE", "K03": "CONDITIONAL_PHYSICAL_FIELD_HOME", "K04": "ADMISSIBLE_ONLY_IF_SECTION_OWNERSHIP_SELECTED", "K05": "CONDITIONAL_SECTION_EVALUATED_RETURN", "K06": "CONDITIONAL_SECTION_BOUNDARY"},
        "H04": {"K01": "CONDITIONAL_REGULAR_BRANCH", "K02": "BASIC_PARENT_AVAILABLE", "K03": "CONDITIONAL_REGULAR_BRANCH", "K04": "ADMISSIBLE_WITH_CHAIN_RULE_NOT_SELECTED", "K05": "CONDITIONAL_REGULAR_BRANCH_RETURN", "K06": "CONDITIONAL_REGULAR_BRANCH_BOUNDARY"},
        "H05": {"K01": "TILEWISE_OR_SET_VALUED", "K02": "BASIC_PARENT_PLUS_STRATA", "K03": "STRATIFIED_RULE_OPEN", "K04": "STRATIFIED_RULE_OPEN", "K05": "STRATIFIED_GLOBAL_JOIN_OPEN", "K06": "STRATIFIED_BOUNDARY_RULE_OPEN"},
        "H06": {key: "UNAVAILABLE_MISSING_NATIVE_AGGREGATION_DATA" for key, *_ in LAW_CLASSES},
        "H07": {"K01": "DERIVED_QUERY_COMPONENT", "K02": "DERIVED_BASIC_COMPONENT", "K03": "QUERY_OR_REDUCTION_COMPONENT", "K04": "ADMISSIBLE_TYPED_ENVELOPE_NOT_SELECTED", "K05": "GLOBAL_COMPONENT_OPEN", "K06": "MULTITYPE_BOUNDARY_COMPONENT_OPEN"},
        "H08": {key: "UNCLASSIFIED_ESCAPE_RETAINED" for key, *_ in LAW_CLASSES},
    }
    rows = []
    for architecture_id in [f"H{i:02d}" for i in range(1, 9)]:
        h, c, v = home[architecture_id]
        for law_id, law_class, input_type, output_type in LAW_CLASSES:
            rows.append((architecture_id, law_id, law_class, h, input_type, c + " :: " + output_type, v, availability[architecture_id][law_id]))
    return rows


def main() -> None:
    result = exact_algebra()
    write_tsv("LAW_CLASS_UNIVERSE.tsv", ("law_id", "law_class", "input_type", "native_codomain_type"), LAW_CLASSES)
    atlas = architecture_atlas()
    write_tsv("HOME_CODOMAIN_ATLAS.tsv", ("architecture_id", "law_id", "law_class", "home", "input_type", "codomain", "variation_owner", "ruling"), atlas)
    variation = [
        ("V01", "ambient metric/coframe", "M configuration", "INDEPENDENT_ONLY_AFTER_NATIVE_DOMAIN", "delta_g modulo declared presentation gauge", "OPEN_NATIVE_VARIATION_DOMAIN"),
        ("V02", "observer pair/path query", "P/groupoid argument", "NO", "changes the question/arrow, not the universe", "DERIVED_QUERY_NOT_FIELD_VARIATION"),
        ("V03", "realized reciprocal section s", "section of P over M", "YES_ONLY_IF_H03_SELECTED", "independent delta_s", "OPEN_PHYSICAL_OWNERSHIP"),
        ("V04", "branch-derived section S[g]", "regular branch", "NO_INDEPENDENT_VARIATION", "delta_s=DS_g[delta_g]", "CONDITIONAL_CHAIN_RULE"),
        ("V05", "regular projector/screen response", "regular selector stratum", "NO_INDEPENDENT_VARIATION_IF_DERIVED", "parent metric/form chain rule", "CONDITIONAL_REGULAR"),
        ("V06", "collision zero tie causal or rank-change data", "singular stratum", "NO_UNIQUE_SMOOTH_OWNER", "ambient path or future stratified rule", "OPEN_STRATIFIED_OWNERSHIP"),
        ("V07", "transition/completion modulus", "global configuration", "POTENTIALLY", "cocycle-compatible modulus modulo coboundary", "OPEN_GLOBAL_OWNER"),
        ("V08", "discrete topology/monodromy sector", "component label", "NO_CONTINUOUS_TANGENT", "enumerate sector", "DERIVED_TYPE_DISTINCTION"),
        ("V09", "base boundary/seal data", "boundary of M", "POTENTIALLY_AFTER_DOMAIN", "declared boundary tangent", "OPEN_BOUNDARY_OWNER"),
        ("V10", "pair polarization/section boundary data", "query or reduction boundary", "ONLY_AFTER_HOME_DECLARED", "query argument or section tangent as typed", "OPEN_MULTIPLE_CLASSES"),
        ("V11", "fiber measure weight normalization", "query fiber", "UNAVAILABLE", "no variation until native aggregation exists", "OPEN_NOT_SUPPLIED"),
        ("V12", "bootstrap/global-local return", "complete on-shell solution space", "NOT_YET_TYPED_AS_VARIATION", "relation/admissibility owner open", "WORKING_NOT_DERIVED"),
    ]
    write_tsv("VARIATION_OWNERSHIP_ATLAS.tsv", ("variation_id", "object", "home", "independent_physical_variation", "rule", "status"), variation)
    sne = [
        ("H01", "COMPATIBLE_ONLY_WITH_DOWNSTREAM_TYPED_QUERY_READOUT_LAYER", "NO", "does not choose basic dynamics"),
        ("H02", "COMPATIBLE_CAPABILITY_NOT_SELECTOR", "NO", "four readouts can be query morphisms"),
        ("H03", "COMPATIBLE_CAPABILITY_NOT_SELECTOR", "NO", "four readouts can evaluate a realized reduction"),
        ("H04", "COMPATIBLE_CAPABILITY_NOT_SELECTOR", "NO", "four readouts can evaluate a regular derived reduction"),
        ("H05", "COMPATIBLE_TILEWISE_NOT_SELECTOR", "NO", "registered static branch can be one regular tile"),
        ("H06", "BLOCKED_MISSING_NATIVE_AGGREGATION_DATA", "NO", "anchor cannot invent a fiber measure"),
        ("H07", "COMPATIBLE_TYPED_ENVELOPE_NOT_SELECTOR", "NO", "distinct readout codomains are retained explicitly"),
        ("H08", "UNCLASSIFIED", "NO", "escape cannot be rejected from this anchor"),
    ]
    write_tsv("SNE_COMPATIBILITY_ATLAS.tsv", ("architecture_id", "compatibility", "selects_home", "reason"), sne)
    quantifiers = [
        ("Q01", "SUPPLIED_QUERY_READOUT", "evaluate L(g,q) for the asked q", "q is an argument not varied", "DERIVED_AVAILABLE_FOR_KINEMATICS_AND_READOUT", "does not define on-shell dynamics"),
        ("Q02", "UNIVERSAL_ALL_QUERIES", "require L(g,q)=0 for every q in each query fiber", "vary g; do not vary q", "ADMISSIBLE_NOT_SELECTED", "nonbasic residual can define observer-independent solution subset"),
        ("Q03", "EXISTENTIAL_QUERY", "require existence of q with L(g,q)=0", "q is a witness unless promoted", "ADMISSIBLE_NOT_SELECTED", "does not identify a physical observer/reduction"),
        ("Q04", "REALIZED_SECTION", "evaluate L(g,s(x)) on physical s", "vary g and independently vary s only after ownership", "OPEN_PHYSICAL_OWNERSHIP", "section existence is insufficient"),
        ("Q05", "BRANCH_DERIVED_SECTION", "evaluate L(g,S[g]) on regular branch", "vary g with DS_g chain term", "CONDITIONAL_REGULAR", "parent selector and collision rule open"),
        ("Q06", "SET_VALUED_STRATIFIED", "retain orbit/tile/set at singular strata", "stratum tangent or open interface owner", "OPEN_STRATIFIED", "all-versus-exists quantifier at orbit remains open"),
        ("Q07", "FIBER_AGGREGATED", "integrate or quotient over q", "vary g and every derived aggregation datum", "OPEN_UNAVAILABLE", "measure weight normalization convergence meaning absent"),
    ]
    write_tsv("QUERY_QUANTIFIER_LEDGER.tsv", ("quantifier_id", "quantifier", "law_condition", "variation_owner", "status", "consequence"), quantifiers)
    native_compatibility = [
        ("H01", "COMPATIBLE", "law acts on metric/configuration data on M", "still not selected by founding kinematics"),
        ("H02", "COMPATIBLE_IF_QUERY_IS_DERIVED_ARGUMENT", "query bundle is metric-derived and adds no physical field", "dynamical quantifier and codomain remain open"),
        ("H03", "CONDITIONAL_EXTRA_STRUCTURE", "independent physical section adds data beyond the metric unless proved metric-owned", "not adoptable as native merely by declaring ownership"),
        ("H04", "COMPATIBLE_ON_REGULAR_METRIC_DERIVED_BRANCH", "section is output of parent metric", "selector and singular continuation open"),
        ("H05", "COMPATIBLE_IF_ALL_STRATA_AND_GLUE_ARE_METRIC_DERIVED", "no independent carrier or section required", "stratified law absent"),
        ("H06", "COMPATIBLE_IN_PRINCIPLE_ONLY_IF_AGGREGATION_IS_METRIC_DERIVED", "could remain metric-only", "all aggregation data absent"),
        ("H07", "REQUIRED_AS_TYPED_BOOKKEEPING_NOT_SELECTED_AS_ONE_PHYSICAL_LAW", "preserves already-derived homes without extra physics", "dynamical component remains open"),
        ("H08", "OPEN", "nonexhaustiveness escape", "must be audited if discovered"),
    ]
    write_tsv("NATIVE_COMPATIBILITY_LEDGER.tsv", ("architecture_id", "metric_is_theory_compatibility", "reason", "remaining_gate"), native_compatibility)
    entailment = [
        ("E01", "founded reciprocal comparison", "EQUIVARIANT_TYPED_QUERY_MORPHISM", "DERIVED", "abstract depth assignment still open physically"),
        ("E02", "ambient metric connection curvature", "BASIC_SPACETIME_GEOMETRY", "DEFINED_FROM_METRIC", "not a native equation"),
        ("E03", "pair-resolved response", "QUERY_OR_REALIZED_BRANCH_REDUCTION", "TYPE_DERIVED_LAW_OPEN", "no generic basic descent"),
        ("E04", "one homogeneous home for all law classes", "REJECTED_BY_EXISTING_TYPE_DISTINCTIONS", "DERIVED_BOUNDED", "typed layering is required for faithful bookkeeping"),
        ("E05", "basic native dynamics", "ADMISSIBLE", "OPEN_NOT_SELECTED", "founding postulates do not mention a residual codomain"),
        ("E06", "nonbasic equivariant native dynamics", "ADMISSIBLE", "OPEN_NOT_SELECTED", "covariance does not force basicness"),
        ("E07", "realized-section dynamics", "ADMISSIBLE_WITH_NEW_OWNERSHIP", "OPEN_NOT_SELECTED", "section existence is not physical ownership"),
        ("E08", "branch-derived dynamics", "ADMISSIBLE_REGULARLY", "OPEN_NOT_SELECTED", "parent law and chain rule required"),
        ("E09", "stratified completion", "REQUIRED_IF_SELECTED_BRANCH_CROSSES_REGISTERED_STRATA", "OPEN", "no gluing/interface law derived"),
        ("E10", "fiber aggregation", "FORMALLY_CONCEIVABLE", "OPEN_UNAVAILABLE", "measure weight normalization convergence meaning missing"),
        ("E11", "SNe conditional readout", "FOUR_DISTINCT_DOWNSTREAM_CODOMAIN_SLOTS", "CONDITIONAL_ANCHOR", "cannot invert readout to law home"),
        ("E12", "complete native law home/codomain/ownership", "MULTIPLE_ADMISSIBLE_EXTENSIONS", "OPEN_FOUNDATIONS_DO_NOT_DECIDE", "no action source or boundary premise added"),
    ]
    write_tsv("FOUNDATIONAL_ENTAILMENT_MATRIX.tsv", ("entailment_id", "object", "required_or_allowed_type", "status", "scope"), entailment)
    stratified = [
        ("S01", "simple spectrum/nonzero intrinsic form", "H04", "parent chain rule", "CONDITIONAL_REGULAR"),
        ("S02", "round spectral collision", "H05", "set-valued orbit; no unique derivative", "OPEN_STRATIFIED"),
        ("S03", "intrinsic-form zero/rank jump", "H05", "ambient crossing only", "OPEN_STRATIFIED"),
        ("S04", "null or zero dphi", "H05", "normalized selector unavailable", "OPEN_STRATIFIED"),
        ("S05", "causal-type transition", "H05", "tilewise data plus open interface", "OPEN_STRATIFIED"),
        ("S06", "tie/Jordan/complex spectral locus", "H05", "set-valued or no real plane", "OPEN_STRATIFIED"),
        ("S07", "boundary-selector defect intersection", "H05", "boundary tangent/polarization open", "OPEN_STRATIFIED_BOUNDARY"),
    ]
    write_tsv("STRATIFIED_OWNERSHIP_LEDGER.tsv", ("stratum_id", "stratum", "home", "variation_rule", "status"), stratified)
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
