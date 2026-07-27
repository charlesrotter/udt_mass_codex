#!/usr/bin/env python3
"""Deterministic founding-object entailment classification and exact countermodel."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def write_tsv(name: str, rows: list[dict]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_propositions() -> list[dict]:
    # The expected SHA and marker make every cited proposition line-addressed and fail closed.
    specs = [
        ("P01", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", 46, 50,
         "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
         "Use the dimension-matched temporal/radial coframe pair", "founding pair is (c dt,dr)"),
        ("P02", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", 62, 89,
         "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
         "Preserving the reciprocal pairing gives", "dual inverse action forces uv=1"),
        ("P03", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", 91, 115,
         "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
         "Positional composition fixes the exponential", "continuous additive composition yields the exponential character"),
        ("P04", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", 117, 123,
         "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
         "Using the local metric readout", "declared local readout yields the displayed metric"),
        ("P05", "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", 42, 42,
         "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
         "does not yet derive a unique action", "action, profile, and global scale are not derived"),
        ("P06", "udt_observer_pair_clock_operator_audit_2026-07-24/AUDIT_REPORT.md", 17, 41,
         "a7ae3805927d7d8efe1a2daabfd07c0612c0f52375b60e727a6d0d0fabe66c87",
         "abstract ordered observer-pair operator", "abstract pair operator precedes path transport"),
        ("P07", "udt_observer_pair_clock_operator_audit_2026-07-24/AUDIT_REPORT.md", 45, 59,
         "a7ae3805927d7d8efe1a2daabfd07c0612c0f52375b60e727a6d0d0fabe66c87",
         "Three objects must not be conflated", "founded matrix, coordinate transport, and physical-frame comparison differ"),
        ("P08", "udt_observer_pair_clock_operator_audit_2026-07-24/AUDIT_REPORT.md", 105, 132,
         "a7ae3805927d7d8efe1a2daabfd07c0612c0f52375b60e727a6d0d0fabe66c87",
         "What remains open", "physical pair-depth, event pairing, coframe completion, and holonomy remain open"),
        ("P09", "udt_relational_pair_depth_realization_audit_2026-07-24/AUDIT_REPORT.md", 84, 105,
         "de149d583e63dfd3977a477b4147e24c5bb388421a54cb8e66ff758436a35e5f",
         "scalar distance is uniquely", "scalar depth can be endpoint single-valued while full transport is path-multiple"),
        ("P10", "udt_three_reciprocity_delta_k_audit_2026-07-23/AUDIT_REPORT.md", 42, 50,
         "a7e00f3cdc5b7ee3e26afdd0426ca27b5b663f0b5477977650f9a995f04fa214",
         "Observer-frame reciprocity", "frame covariance is conjugation and does not force a unique invariant value"),
        ("P11", "udt_covariant_reciprocal_coframe_lift_atlas_2026-07-26/AUDIT_REPORT.md", 9, 34,
         "b338fa5538e54951d3bcea8325b7c3a00940a45b2287805f766bf772ab2713ef",
         "metric and scalar anchors alone cannot solder", "complete local solder needs extra observer/direction data and lambda remains"),
        ("P12", "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/AUDIT_REPORT.md", 11, 13,
         "d97ea230affe133e40dcac6374f126b51f5741b5af79749de634a1a41d8aee88",
         "No global observer/ruler section is needed", "typed path-frame bundle assembles without a global section"),
        ("P13", "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/AUDIT_REPORT.md", 25, 38,
         "d97ea230affe133e40dcac6374f126b51f5741b5af79749de634a1a41d8aee88",
         "foundations permit typed path-labelled", "parallel endpoint-only meaning is conditional, not selected"),
        ("P14", "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md", 12, 30,
         "7296d4fc3e9a44510f05c0a61a5dce498f894e0d9bf6b9bb6f8e947ef1983398",
         "The obstruction is exact and local", "complete twisted witness has nonparallel X and nonclosing full loops but exact scalar clock join"),
        ("P15", "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md", 108, 118,
         "7296d4fc3e9a44510f05c0a61a5dce498f894e0d9bf6b9bb6f8e947ef1983398",
         "No registered current premise", "ordinary closure, reciprocal seam, and quotient remain open"),
        ("P16", "udt_reduced_holonomy_condition_audit_2026-07-27/AUDIT_REPORT.md", 75, 96,
         "e6d9d41974c540e00ba8f1787576eccd4046b208ff15545cf0604bcfce6f7eab",
         "stronger than the founding scalar", "global parallelism erases nonconstant depth/twist and has no registered premise"),
        ("P17", "udt_founding_observer_comparison_semantics_audit_2026-07-27/AUDIT_REPORT.md", 11, 37,
         "f5b048e1e3055e91933293037f9f3755068d4400ac01bd61ae19e008ebf9a730",
         "SEMANTICS_OPEN", "founding operator is abstract relational; complete endpoint/path semantics are not selected"),
        ("P18", "udt_founding_observer_comparison_semantics_audit_2026-07-27/AUDIT_REPORT.md", 53, 79,
         "f5b048e1e3055e91933293037f9f3755068d4400ac01bd61ae19e008ebf9a730",
         "ADMISSIBLE_CONDITIONAL", "both endpoint and path routes are conditional realizations"),
        ("P19", "udt_founding_observer_comparison_semantics_audit_2026-07-27/AUDIT_REPORT.md", 91, 93,
         "f5b048e1e3055e91933293037f9f3755068d4400ac01bd61ae19e008ebf9a730",
         "remain untouched", "action, carrier, source, boundary, density, mass, Xmax, and dynamics are unaffected"),
    ]
    rows = []
    for pid, path, start, end, expected_sha, marker, proposition in specs:
        raw = (ROOT / path).read_bytes()
        actual_sha = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8")
        lines = text.splitlines()
        cited = "\n".join(lines[start - 1:end])
        assert actual_sha == expected_sha, (path, actual_sha)
        assert marker in cited, (pid, marker)
        rows.append({
            "proposition_id": pid, "source_path": path, "line_start": start, "line_end": end,
            "source_sha256": actual_sha, "proposition": proposition, "marker": marker,
        })
    return rows


def classify_objects() -> list[dict]:
    return [
        {"object_id":"O01","classification":"FOUNDING_DERIVED","founding_packet_alone":"YES","minimum_added_premise":"NONE","transport_type":"LOCAL_CHARACTER","current_selection":"EXACT","reason":"dual pairing plus continuous composition fixes D(phi)","stronger_not_implied":"spacetime solder or connection"},
        {"object_id":"O02","classification":"FOUNDING_DERIVED_ABSTRACT","founding_packet_alone":"YES_ONCE_ORDERED_DEPTH_IS_SUPPLIED","minimum_added_premise":"ordered additive depth value","transport_type":"ABSTRACT_ENDPOINT_LABELS_NOT_PHYSICAL_EVENTS","current_selection":"EXACT_ABSTRACT","reason":"D(phi_q)D(phi_p)^-1 composes and reverses without a metric path","stronger_not_implied":"physical depth assignment, path rule, or endpoint event rule"},
        {"object_id":"O03","classification":"METRIC_DERIVED_CONDITIONAL","founding_packet_alone":"NO","minimum_added_premise":"stationary metric plus common exact scalar section and endpoint event/frame identification","transport_type":"SCALAR_ENDPOINT_EXACT","current_selection":"CONDITIONAL","reason":"log Q=phi(q)-phi(p) is exact on the registered stationary realization","stronger_not_implied":"full-frame endpoint closure"},
        {"object_id":"O04","classification":"CONDITIONAL_SUPPLIED_STRUCTURE","founding_packet_alone":"NO","minimum_added_premise":"complete metric plus ordered observer and ruler or equivalent selector","transport_type":"LOCAL_COMPLETE_COFRAME","current_selection":"NOT_UNIQUE","reason":"metric and scalars alone have no nontrivial Lorentz-equivariant solder","stronger_not_implied":"unique global section or transport"},
        {"object_id":"O05","classification":"METRIC_DERIVED_CONDITIONAL","founding_packet_alone":"NO","minimum_added_premise":"O04 plus supplied complete metric, Levi-Civita connection, and specified path","transport_type":"PATH_LABELLED","current_selection":"MATHEMATICALLY_EXACT_NOT_PHYSICAL_ONTOLOGY","reason":"conjugated path transport is canonical after those inputs are supplied","stronger_not_implied":"path-independent endpoint lift"},
        {"object_id":"O06","classification":"NOT_DERIVED","founding_packet_alone":"NO","minimum_added_premise":"all-path holonomy centralization or a separately selected endpoint trivialization","transport_type":"ENDPOINT_ONLY_FULL_FRAME","current_selection":"OPEN","reason":"actual complete witness has path-dependent full transport while preserving founding kinematics","stronger_not_implied":"UDT selection of a global parallel grading"},
        {"object_id":"O07","classification":"NOT_DERIVED_EXTRA_RESTRICTION","founding_packet_alone":"NO","minimum_added_premise":"impose nabla X=0 and require compatible reduced holonomy","transport_type":"GLOBAL_PARALLEL_FIELD","current_selection":"NOT_REQUIRED","reason":"local founding countermodel has nabla X nonzero; complete witness independently repeats the obstruction","stronger_not_implied":"physical branch, lambda, or holonomy reduction selected by UDT"},
        {"object_id":"O08","classification":"ALGEBRAICALLY_AVAILABLE_NOT_PHYSICALLY_SELECTED","founding_packet_alone":"ALGEBRAIC_NORMALIZER_ONLY","minimum_added_premise":"swap normalizer F; physical seam additionally needs quotient/boundary law","transport_type":"INVOLUTION_NOT_ORDINARY_TRANSPORT","current_selection":"OPEN","reason":"F D(phi) F^-1=D(-phi) is algebraic but actual ordinary holonomy is not reciprocal inversion","stronger_not_implied":"ordinary Levi-Civita holonomy or physical quotient"},
    ]


def implication_graph() -> list[dict]:
    return [
        {"edge_id":"E01","source":"FOUNDING_PACKET","target":"O01","added_premise":"NONE","status":"DERIVED"},
        {"edge_id":"E02","source":"O01","target":"O02","added_premise":"ordered additive depth supplied","status":"DERIVED_ABSTRACT"},
        {"edge_id":"E03","source":"O02","target":"O03","added_premise":"stationary common exact scalar section plus endpoint identification","status":"CONDITIONAL"},
        {"edge_id":"E04","source":"O01","target":"O04","added_premise":"complete metric plus ordered observer/ruler selector","status":"CONDITIONAL_NONUNIQUE"},
        {"edge_id":"E05","source":"O04","target":"O05","added_premise":"Levi-Civita connection plus specified path","status":"CONDITIONAL_EXACT"},
        {"edge_id":"E06","source":"O05","target":"O06","added_premise":"all relevant holonomy centralizes X or endpoint trivialization selected","status":"NOT_CURRENTLY_DERIVED"},
        {"edge_id":"E07","source":"O04","target":"O07","added_premise":"nabla X=0 imposed and global compatibility proved","status":"EXTRA_RESTRICTION"},
        {"edge_id":"E08","source":"O06","target":"O07","added_premise":"smooth connected all-path transport construction","status":"MATHEMATICAL_IF_GLOBAL_HYPOTHESES_HOLD_NOT_PHYSICAL_SELECTION"},
        {"edge_id":"E09","source":"O01","target":"O08","added_premise":"external swap normalizer F","status":"ALGEBRAIC_ONLY"},
        {"edge_id":"N01","source":"OBSERVER_FRAME_COVARIANCE","target":"O06","added_premise":"NONE","status":"NON_EDGE_COUNTERMODEL"},
        {"edge_id":"N02","source":"FOUNDING_PACKET","target":"O07","added_premise":"NONE","status":"NON_EDGE_COUNTERMODEL"},
        {"edge_id":"N03","source":"O08","target":"ORDINARY_HOLONOMY","added_premise":"NONE","status":"NON_EDGE_ACTUAL_WITNESS"},
    ]


def exact_countermodels() -> tuple[list[dict], dict]:
    x = sp.symbols("x", real=True)
    phi = x
    g = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi))
    gi = sp.simplify(g.inv())
    coords = (sp.symbols("t", real=True), x)
    gamma = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            gi[a, d] * (sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c]) - sp.diff(g[b, c], coords[d]))
            for d in range(2)
        )) for c in range(2)] for b in range(2)] for a in range(2)]
    X = sp.diag(-1, 1)
    nabla = [[[sp.simplify(
        sp.diff(X[a, c], coords[b])
        + sum(gamma[a][b][d] * X[d, c] - gamma[d][b][c] * X[a, d] for d in range(2))
    ) for c in range(2)] for a in range(2)] for b in range(2)]
    anchor = sp.simplify(nabla[0][0][1].subs(x, 0))
    assert anchor == -2

    a, b = sp.symbols("a b", real=True)
    D = lambda z: sp.diag(sp.exp(-z), sp.exp(z))
    assert sp.simplify(D(a) * D(b) - D(a + b)) == sp.zeros(2)
    assert D(1) != sp.eye(2)
    K = sp.Matrix([[0, 1], [1, 0]])
    assert sp.simplify(D(a).T * K * D(a) - K) == sp.zeros(2)

    complete = json.loads((ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/DERIVATION_RESULT.json").read_text())
    assert complete["exact_P00_nabla_E0_X_0_1"] == "-3/25"
    assert complete["curvature_span_ranks"] == [6] and complete["lie_closure_ranks"] == [6]
    assert complete["loop_transports"] == complete["loops_with_nonzero_ordinary_closure_residual"] == 36
    assert complete["ordinary_holonomy_is_not_reciprocal_inversion"] is True

    rows = [
        {"countermodel_id":"C01","level":"FOUNDING_LOCAL","founded_character":"PASS","nonidentity":"PASS","composition":"PASS","complete_metric":"LOCAL_4D_WITH_DECLARED_SPHERICAL_SECTOR","on_shell":"NO","nabla_X":"NONZERO_EXACT_-2_AT_r1","holonomy":"NOT_NEEDED","logical_use":"FOUNDING_PACKET_DOES_NOT_ENTAIL_GLOBAL_PARALLELISM"},
        {"countermodel_id":"C02","level":"COMPLETE_COFRAME_WITNESS","founded_character":"PASS","nonidentity":"PASS","composition":"PASS","complete_metric":"YES_REGISTERED_TWISTED_S3","on_shell":"NO_OFF_SHELL","nabla_X":"NONZERO_EXACT_-3/25_AT_P00_ALL_LAMBDA","holonomy":"SO(1,3)_RANK_6_AND_36_OF_36_LOOPS_NONCLOSING","logical_use":"REINFORCES_PATH_DEPENDENCE_WITHOUT_REPLACING_C01"},
    ]
    algebra = {
        "local_metric": "diag(-exp(-2(r-1)),exp(2(r-1)),r^2,r^2 sin(theta)^2)_near_r=1",
        "local_phi": "r-1",
        "local_X": "diag(-1,1)",
        "local_Gamma_t_t_x_at_x0": str(sp.simplify(gamma[0][0][1].subs(x, 0))),
        "local_nabla_dt_X_t_r_at_r1": str(anchor),
        "complete_exact_anchor": complete["exact_P00_nabla_E0_X_0_1"],
        "complete_holonomy_rank": complete["lie_closure_ranks"][0],
        "complete_nonclosing_loops": complete["loops_with_nonzero_ordinary_closure_residual"],
    }
    return rows, algebra


def downstream_regrade() -> list[dict]:
    return [
        {"regrade_id":"R01","prior_statement_class":"abstract reciprocal operator missing","effective_ruling":"SUPERSEDED_CLOSED","required_object":"O02","reason":"founded character already supplies the abstract ordered comparison"},
        {"regrade_id":"R02","prior_statement_class":"shortest path must create scalar clock operator","effective_ruling":"SUPERSEDED_TOO_STRONG","required_object":"O02","reason":"paths enter only after abstract depth is supplied"},
        {"regrade_id":"R03","prior_statement_class":"complete coframe solder missing","effective_ruling":"REMAINS_OPEN_CONDITIONAL","required_object":"O04","reason":"metric/scalars alone do not uniquely select observer/ruler embedding"},
        {"regrade_id":"R04","prior_statement_class":"global reciprocal closure missing","effective_ruling":"SPLIT_REQUIRED","required_object":"O05_O06_O07","reason":"typed path transport exists conditionally; endpoint independence and parallelism are separate extra questions"},
        {"regrade_id":"R05","prior_statement_class":"global parallel reciprocal frame required by Reciprocity","effective_ruling":"REJECTED_AS_FOUNDING_REQUIREMENT","required_object":"O07","reason":"explicit local countermodel satisfies founding packet with nonzero nabla X"},
        {"regrade_id":"R06","prior_statement_class":"path groupoid is UDT physical ontology","effective_ruling":"NOT_AUTHORIZED","required_object":"O05","reason":"mathematical consistency given inputs does not select physical semantics"},
        {"regrade_id":"R07","prior_statement_class":"endpoint-only complete semantics is derived","effective_ruling":"NOT_DERIVED","required_object":"O06","reason":"requires depth/event/global trivialization and holonomy conditions"},
        {"regrade_id":"R08","prior_statement_class":"lambda one selected by observer Reciprocity","effective_ruling":"NOT_DERIVED","required_object":"O07","reason":"lambda one follows only after the unrequired endpoint-parallel restriction on bounded controls"},
        {"regrade_id":"R09","prior_statement_class":"physical observer-pair depth/event/readout open","effective_ruling":"UNCHANGED_OPEN","required_object":"O03_O04","reason":"abstract kinematics does not supply complete physical comparison data"},
        {"regrade_id":"R10","prior_statement_class":"action source carrier boundary density mass Xmax dynamics open","effective_ruling":"UNCHANGED_OPEN","required_object":"DOWNSTREAM","reason":"object semantics audit supplies none of these"},
    ]


def main() -> int:
    propositions = source_propositions()
    objects = classify_objects()
    graph = implication_graph()
    countermodels, algebra = exact_countermodels()
    regrade = downstream_regrade()
    write_tsv("SOURCE_PROPOSITIONS.tsv", propositions)
    write_tsv("OBJECT_CLASSIFICATION.tsv", objects)
    write_tsv("IMPLICATION_GRAPH.tsv", graph)
    write_tsv("COUNTERMODEL_LEDGER.tsv", countermodels)
    write_tsv("DOWNSTREAM_REGRADE.tsv", regrade)
    result = {
        "schema": "udt-founding-reciprocity-object-entailment-1.0",
        "status": "COMPUTED",
        "source_propositions": len(propositions),
        "objects": len(objects),
        "founding_derived_objects": ["O01", "O02"],
        "metric_conditional_objects": ["O03", "O04", "O05"],
        "not_founding_derived_objects": ["O06", "O07"],
        "algebraic_not_selected_objects": ["O08"],
        "founding_requires_global_parallelism": False,
        "complete_physical_semantics": "OPEN",
        "path_groupoid_selected_as_physics": False,
        "endpoint_only_selected_as_physics": False,
        "lambda_selected": False,
        "local_countermodel": algebra,
        "downstream_regrades": len(regrade),
        "authority_boundary": "NO_ACTION_SOURCE_CARRIER_BOUNDARY_DENSITY_BOOTSTRAP_MASS_XMAX_DYNAMICS_OR_SIGNALLING_INFERENCE",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
