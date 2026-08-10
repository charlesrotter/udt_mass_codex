#!/usr/bin/env python3
"""Exact CPU controller for the founding pair-relation ownership audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent

AXES = [
    ("A01", "object_and_arrow_type"),
    ("A02", "direct_founding_words_or_equations"),
    ("A03", "observer_worldline_and_frame"),
    ("A04", "event_pairing"),
    ("A05", "ruler_direction_and_evolution"),
    ("A06", "local_pair_map"),
    ("A07", "branch_or_path_at_cut_locus"),
    ("A08", "cE_calibration_normalization"),
    ("A09", "middle_observer_transition"),
    ("A10", "reversal_and_frame_reciprocity"),
    ("A11", "terminal_phi_pair_ceff_compatibility"),
    ("A12", "maximum_justified_interpretation"),
]

ALLOWED = {
    "FOUNDING_DERIVED",
    "QUERY_SUPPLIED_NOT_FOUNDING_DERIVED",
    "METRIC_DERIVED_AFTER_DECLARED_QUERY",
    "CONSTRAINT_NOT_SELECTOR",
    "CONDITIONAL_LOCAL",
    "BRANCH_RELATION_NOT_SINGLE_MAP",
    "OUTPUT_COMPATIBLE_NOT_SELECTOR",
    "OPEN_NOT_OWNED",
    "FAILS_REQUIRED_TYPE",
}


def R(disposition: str, basis: str) -> tuple[str, str]:
    assert disposition in ALLOWED
    return disposition, basis


# Every one of the 9 x 12 cells is separately declared. This is the adjudication,
# not an output-dependent merit ranking.
ADJUDICATION: dict[str, list[tuple[str, str]]] = {
    "I01": [
        R("FOUNDING_DERIVED", "An ordered abstract comparison with supplied signed depth is the domain of D(delta)."),
        R("FOUNDING_DERIVED", "The source explicitly begins from relative depth Delta, then derives reciprocal scaling."),
        R("OPEN_NOT_OWNED", "No physical observer worldline or tetrad is defined by the founding equations."),
        R("OPEN_NOT_OWNED", "Source and target roles do not pair spacetime events."),
        R("OPEN_NOT_OWNED", "No ruler direction or evolution law appears in the founding source."),
        R("OPEN_NOT_OWNED", "D(delta) acts after delta is supplied; it does not construct a pair surface."),
        R("OPEN_NOT_OWNED", "The abstract character contains no cut-locus or branch rule."),
        R("FOUNDING_DERIVED", "c_E dimension-matches clock and ruler channels, but only at the algebraic calibration level."),
        R("OPEN_NOT_OWNED", "Composition assumes matched abstract depths; no physical middle calibration identification is defined."),
        R("FOUNDING_DERIVED", "D(b)D(a)=D(a+b), D(a)^-1=D(-a), and abstract source-target reversal are exact."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "The terminal evaluator reduces to this character once a calibrated pair metric is supplied."),
        R("FOUNDING_DERIVED", "The foundation owns the ordered-depth character, not the observer-to-depth realization."),
    ],
    "I02": [
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Two framed observer worldlines define objects but still only a hom-set of possible comparisons."),
        R("OPEN_NOT_OWNED", "The founding source does not explicitly define observer as worldline plus proper clock plus tetrad."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "This is a standard legitimate observer-query enrichment, not a consequence of D(delta)."),
        R("OPEN_NOT_OWNED", "Two worldlines alone admit many event-pairing maps."),
        R("OPEN_NOT_OWNED", "Endpoint frames do not specify how a ruler is evolved between events."),
        R("OPEN_NOT_OWNED", "Worldlines and frames do not single out one connecting surface."),
        R("OPEN_NOT_OWNED", "Multiple paths and intersections remain possible."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Proper clocks and c_E normalize local clock length; unit rulers normalize local spatial length."),
        R("OPEN_NOT_OWNED", "Separate local frames do not identify an A-carried tape with B's local tape."),
        R("CONSTRAINT_NOT_SELECTOR", "Frame Reciprocity requires equal law and covariant reversal but does not choose an event pairing."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "Any resulting regular pair metric can be read terminally, but the readout does not construct it."),
        R("CONDITIONAL_LOCAL", "Framed worldlines are useful declared data but insufficient for a unique pair relation."),
    ],
    "I03": [
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "A paired-event relation chooses endpoint events but not a unique comparison germ between them."),
        R("OPEN_NOT_OWNED", "No simultaneity or event-pairing convention is stated in the two founding postulates."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Worldlines and frames remain declared query data."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "The event-pairing map is explicit input by definition of this interpretation."),
        R("OPEN_NOT_OWNED", "Paired events do not select ruler direction or its evolution."),
        R("OPEN_NOT_OWNED", "Several pair surfaces can share the same paired boundary events."),
        R("OPEN_NOT_OWNED", "Path and cut-locus branch remain unselected."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "c_E fixes the dimensions and local origin normalization of each declared frame."),
        R("OPEN_NOT_OWNED", "Pairing endpoints does not own associative calibration carry through a third observer."),
        R("CONSTRAINT_NOT_SELECTOR", "Reciprocity constrains the reversed paired relation but does not create it."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "A supplied regular connecting geometry is still required before terminal evaluation."),
        R("CONDITIONAL_LOCAL", "Explicit event pairing closes one semantic gap but not the pair-map or carry gaps."),
    ],
    "I04": [
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "The object is a complete local observer germ plus an intersection/branch query."),
        R("OPEN_NOT_OWNED", "The founding source does not enumerate this enriched query."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "A's worldline, proper clock, and local frame are explicit query inputs."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "B is paired by the declared regular intersection rule."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "The initial unit ruler and its evolution are supplied, not inferred from c_E."),
        R("METRIC_DERIVED_AFTER_DECLARED_QUERY", "F(y,s)=Exp_zA(y)[s n(y)] is metric-natural on the declared regular branch."),
        R("CONDITIONAL_LOCAL", "Normal-neighborhood uniqueness ends at conjugate points and cut loci."),
        R("FOUNDING_DERIVED", "y=c_E tau and unit affine s make h=eta at the A-origin."),
        R("OPEN_NOT_OWNED", "One local germ does not provide the transition law between separately built germs."),
        R("CONSTRAINT_NOT_SELECTOR", "Reversal must be constructed from the same relation; Reciprocity tests covariance rather than selecting n or the branch."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "The pullback h gives the exact terminal phi_pair on its regular domain."),
        R("CONDITIONAL_LOCAL", "This is the strongest local positive construction: query-supplied data plus metric-derived geometry."),
    ],
    "I05": [
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "The calibrated pair surface or branch-labelled relation is itself the supplied arrow data."),
        R("OPEN_NOT_OWNED", "Calling a supplied relation an ordered comparison does not make its construction founded."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Observer data are included by this enlarged query definition."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Event pairing is encoded by the supplied relation."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Ruler evolution is encoded by the supplied comparison Jacobian."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "The map is input, not derived merely because its pullback is metric-covariant."),
        R("BRANCH_RELATION_NOT_SINGLE_MAP", "A branch-labelled family is honest; no preferred branch follows from the label set."),
        R("FOUNDING_DERIVED", "A-calibration fixes h=eta at the declared origin and makes the terminal ratio dimensionless."),
        R("OPEN_NOT_OWNED", "A family of supplied pair surfaces still needs a matched intermediate calibration rule."),
        R("CONSTRAINT_NOT_SELECTOR", "A supplied inverse and matched composition can satisfy Reciprocity; the axiom does not generate them."),
        R("FOUNDING_DERIVED", "On every supplied regular calibrated h, phi_pair=(1/4)log[(-det h)/h00^2] is exact."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "The construction is sufficient by definition but is not a derivation of the physical functor."),
    ],
    "I06": [
        R("CONSTRAINT_NOT_SELECTOR", "Equivariance is a condition on arrows already in the comparison groupoid."),
        R("FOUNDING_DERIVED", "Composition, reversal, neutral comparison, and equal law for exchanged frames are founding constraints."),
        R("OPEN_NOT_OWNED", "Equivariance does not create observer worldlines or frames."),
        R("CONSTRAINT_NOT_SELECTOR", "A symmetry maps admissible event pairings to reversed pairings; it need not select one."),
        R("CONSTRAINT_NOT_SELECTOR", "Ruler evolution must transform covariantly but is not chosen by covariance."),
        R("CONSTRAINT_NOT_SELECTOR", "Many distinct pair maps can all be natural under frame changes."),
        R("CONSTRAINT_NOT_SELECTOR", "Reciprocity may exchange branch labels without collapsing a branch family."),
        R("CONSTRAINT_NOT_SELECTOR", "The fixed calibration must be respected, but covariance does not supply it beyond c_E."),
        R("CONSTRAINT_NOT_SELECTOR", "Associativity can reject unmatched resets but cannot identify the middle state without transition data."),
        R("FOUNDING_DERIVED", "On matched abstract comparisons, reversal and additive depth are exact."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "The terminal evaluator is frame-covariant but covariance alone does not choose its h."),
        R("CONSTRAINT_NOT_SELECTOR", "Observer-frame Reciprocity is a powerful regression gate, not an existence/uniqueness theorem."),
    ],
    "I07": [
        R("FOUNDING_DERIVED", "c_E is the fixed conversion joining clock duration and ruler length in the founding pair."),
        R("FOUNDING_DERIVED", "The founding source explicitly dimension-matches c_E dt and dr."),
        R("OPEN_NOT_OWNED", "A conversion constant does not specify observer histories."),
        R("FAILS_REQUIRED_TYPE", "c_E has units of speed and cannot by itself be an event-pairing map."),
        R("FAILS_REQUIRED_TYPE", "c_E supplies no spatial direction or transport law."),
        R("FAILS_REQUIRED_TYPE", "Local scale calibration is not a map from a two-parameter query into spacetime."),
        R("FAILS_REQUIRED_TYPE", "A scalar calibration cannot select a cut-locus branch."),
        R("FOUNDING_DERIVED", "Proper clock plus c_E and a unit ruler give h00=-1,h01=0,h11=1 at a declared A-origin."),
        R("OPEN_NOT_OWNED", "The same local unit convention at B does not identify it with the A-carried relational state."),
        R("CONSTRAINT_NOT_SELECTOR", "Both directions use the same c_E, satisfying frame equality without selecting the relation."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "c_eff/c_E=exp(-2 phi_pair) is calibrated only after h is supplied."),
        R("FOUNDING_DERIVED", "c_E fixes local units and the terminal reference value, not position, simultaneity, branch, or carry."),
    ],
    "I08": [
        R("BRANCH_RELATION_NOT_SINGLE_MAP", "The metric exponential defines a relation of regular initial data and endpoints."),
        R("OPEN_NOT_OWNED", "The founding reciprocal equations do not mention exponential or Jacobi maps."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "A base observer curve and initial frame are required inputs."),
        R("CONDITIONAL_LOCAL", "A unique transverse intersection can induce pairing only on a declared regular branch."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "Initial direction and its observer-history evolution remain query data."),
        R("METRIC_DERIVED_AFTER_DECLARED_QUERY", "The complete metric determines each regular exponential/Jacobi branch."),
        R("BRANCH_RELATION_NOT_SINGLE_MAP", "At cut loci the natural metric output is the full branch relation."),
        R("QUERY_SUPPLIED_NOT_FOUNDING_DERIVED", "c_E calibrates the base clock coordinate but not the branch relation."),
        R("OPEN_NOT_OWNED", "dExp position blocks do not compose; full Jacobi phase needs enlarged carried data and a reduction."),
        R("CONSTRAINT_NOT_SELECTOR", "Metric naturality and reversal organize branches without choosing one physical member."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "Each regular branch pullback is terminally readable; equal readouts need not identify equal maps."),
        R("BRANCH_RELATION_NOT_SINGLE_MAP", "Geometry supplies a local multirelation, not a universal single-valued physical functor."),
    ],
    "I09": [
        R("CONSTRAINT_NOT_SELECTOR", "X_max is a condition on realized observer-pair separations and depths."),
        R("OPEN_NOT_OWNED", "The founding reciprocal derivation does not construct the numerical or global X_max realization."),
        R("OPEN_NOT_OWNED", "An asymptotic bound does not supply observer histories."),
        R("FAILS_REQUIRED_TYPE", "A limiting value cannot pair events by itself."),
        R("FAILS_REQUIRED_TYPE", "A scalar asymptote supplies no ruler direction or evolution."),
        R("FAILS_REQUIRED_TYPE", "Endpoint behavior does not generate a local pair map."),
        R("CONSTRAINT_NOT_SELECTOR", "Every admitted branch must meet the limit gate where applicable, but the gate does not choose the branch."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "c_E fixes ordinary-regime calibration while X_max constrains the far asymptote."),
        R("OPEN_NOT_OWNED", "The asymptotic gate gives no middle-observer transition."),
        R("CONSTRAINT_NOT_SELECTOR", "A frame-shared limit must respect exchange, but that requirement is not yet an all-frame theorem."),
        R("OUTPUT_COMPATIBLE_NOT_SELECTOR", "Many terminal profiles can diverge at the same finite separation."),
        R("CONSTRAINT_NOT_SELECTOR", "X_max is a necessary global gate after relation realization, not the relation owner."),
    ],
}


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, object]] = []

    def truth(self, name: str, value: object, detail: object = "") -> None:
        passed = bool(value)
        self.rows.append({"name": name, "passed": passed, "detail": str(detail if detail != "" else value)})

    def exact(self, name: str, actual: object, expected: object) -> None:
        passed = bool(sp.simplify(sp.sympify(actual) - sp.sympify(expected)) == 0)
        self.rows.append({"name": name, "passed": passed, "detail": f"actual={sp.simplify(actual)} expected={sp.simplify(expected)}"})


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_atlas() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for interpretation_id in sorted(ADJUDICATION):
        decisions = ADJUDICATION[interpretation_id]
        if len(decisions) != len(AXES):
            raise RuntimeError(f"{interpretation_id}: expected {len(AXES)} decisions, got {len(decisions)}")
        for (axis_id, axis), (disposition, basis) in zip(AXES, decisions, strict=True):
            rows.append(
                {
                    "interpretation_id": interpretation_id,
                    "axis_id": axis_id,
                    "axis": axis,
                    "disposition": disposition,
                    "basis": basis,
                    "merit_filter": "NONE_CHARACTERIZE_ONLY",
                }
            )
    return rows


def write_atlas(rows: list[dict[str, str]]) -> None:
    fields = ["interpretation_id", "axis_id", "axis", "disposition", "basis", "merit_filter"]
    with (PACKAGE / "SEMANTIC_OWNERSHIP_ATLAS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def replay_sources(checks: Checks) -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks.exact("source_count", len(sources), 15)
    checks.truth("source_paths_unique", len({row["path"] for row in sources}) == 15)
    for index, row in enumerate(sources, start=1):
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        checks.truth(f"source_{index:02d}", sha256(data) == row["sha256"], row["path"])


def derive(write_outputs: bool) -> dict[str, object]:
    checks = Checks()
    replay_sources(checks)

    with (PACKAGE / "SEMANTIC_INTERPRETATION_ARENA.tsv").open(newline="", encoding="utf-8") as handle:
        arena = list(csv.DictReader(handle, delimiter="\t"))
    checks.exact("arena_count", len(arena), 9)
    checks.truth("arena_ids", {row["interpretation_id"] for row in arena} == set(ADJUDICATION))
    checks.truth("arena_no_merit_filter", all(row["merit_filter"] == "NONE_CHARACTERIZE_ONLY" for row in arena))

    atlas = make_atlas()
    if write_outputs:
        write_atlas(atlas)
    checks.exact("atlas_rows", len(atlas), 108)
    checks.exact("atlas_unique_identities", len({(row["interpretation_id"], row["axis_id"]) for row in atlas}), 108)
    checks.truth("atlas_dispositions_registered", all(row["disposition"] in ALLOWED for row in atlas))
    checks.truth("atlas_no_merit_filter", all(row["merit_filter"] == "NONE_CHARACTERIZE_ONLY" for row in atlas))

    source_text = (ROOT / "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md").read_text(encoding="utf-8")
    checks.truth("founding_source_supplies_relative_depth_first", "at relative depth $\\Delta$" in source_text)
    checks.truth("founding_source_marks_composition_as_posit", "**POSIT / positional relativity**" in source_text)
    checks.truth("founding_source_does_not_define_event_pairing", "event pairing" not in source_text.lower())

    # Exact founded character: supplied depth -> reciprocal action, composition, reversal, and K exchange.
    a, b = sp.symbols("a b", real=True)
    D = lambda x: sp.diag(sp.exp(-x), sp.exp(x))
    K = sp.Matrix([[0, 1], [1, 0]])
    checks.truth("founded_composition", sp.simplify(D(b) * D(a) - D(a + b)) == sp.zeros(2))
    checks.truth("founded_reversal", sp.simplify(D(a).inv() - D(-a)) == sp.zeros(2))
    checks.truth("founded_exchange", sp.simplify(K * D(a) * K - D(-a)) == sp.zeros(2))
    checks.truth("founded_pairing_preserved", sp.simplify(D(a).T * K * D(a) - K) == sp.zeros(2))

    # Category/type control: ordered objects identify Hom(A,B), not one arrow, unless thinness is added.
    hom_ab = {"f", "g"}
    inverse = {"f": "f_inv", "g": "g_inv"}
    checks.exact("same_ordered_pair_two_arrows", len(hom_ab), 2)
    checks.truth("each_arrow_has_reversal", set(inverse) == hom_ab and len(set(inverse.values())) == 2)
    checks.truth("order_does_not_select_arrow", hom_ab != {"f"} and hom_ab != {"g"})

    # Flat exact event-pairing family. y and s are c_E-calibrated length coordinates.
    y, s, L, k = sp.symbols("y s L k", real=True, nonzero=True)
    Fk = sp.Matrix([y + k * s / L, s])
    Jk = Fk.jacobian([y, s])
    eta2 = sp.diag(-1, 1)
    hk = sp.simplify(Jk.T * eta2 * Jk)
    checks.exact("pairing_family_h00", hk[0, 0], -1)
    checks.exact("pairing_family_h01", hk[0, 1], -k / L)
    checks.exact("pairing_family_h11", hk[1, 1], 1 - k**2 / L**2)
    checks.exact("pairing_family_det", hk.det(), -1)
    ruler2 = sp.simplify(hk[1, 1] - hk[0, 1] ** 2 / hk[0, 0])
    checks.exact("pairing_family_orthogonal_ruler", ruler2, 1)
    phi_k = sp.Rational(1, 4) * sp.log((-hk.det()) / hk[0, 0] ** 2)
    checks.exact("pairing_family_terminal_depth", phi_k, 0)
    checks.truth("different_k_pairs_different_B_events", sp.simplify(Fk.subs(s, L) - Fk.subs({s: L, k: 0})) != sp.zeros(2, 1))

    # Same central observer and pair metric, different ruler evolution: map identity remains open.
    omega = sp.symbols("omega", real=True, nonzero=True)
    F_plus = sp.Matrix([y, s * sp.cos(omega * y), s * sp.sin(omega * y), 0])
    F_minus = sp.Matrix([y, s * sp.cos(omega * y), -s * sp.sin(omega * y), 0])
    eta4 = sp.diag(-1, 1, 1, 1)
    h_plus = sp.simplify(F_plus.jacobian([y, s]).T * eta4 * F_plus.jacobian([y, s]))
    h_minus = sp.simplify(F_minus.jacobian([y, s]).T * eta4 * F_minus.jacobian([y, s]))
    checks.truth("distinct_ruler_evolutions", sp.simplify(F_plus - F_minus) != sp.zeros(4, 1))
    checks.truth("same_pair_metric_does_not_identify_map", sp.simplify(h_plus - h_minus) == sp.zeros(2))

    # c_E/proper-clock/unit-ruler calibration fixes a declared origin, not pairing or branch.
    checks.truth("cE_origin_normalization", hk.subs(k, 0) == eta2)
    checks.truth("cE_does_not_remove_pairing_parameter", hk.diff(k) != sp.zeros(2))

    # Middle carry: matched channels compose, but a rebuilt reciprocal reset is an extra transition.
    r = sp.symbols("r", real=True)
    composite = sp.simplify(D(b) * D(r) * D(a))
    checks.truth("middle_reset_composite", sp.simplify(composite - D(a + b + r)) == sp.zeros(2))
    checks.truth("matched_middle_is_special_case", sp.simplify(composite.subs(r, 0) - D(a + b)) == sp.zeros(2))
    common = sp.symbols("common", positive=True)
    checks.truth("common_scale_not_reciprocal_reset", sp.simplify(common * sp.eye(2) - D(r)) != sp.zeros(2))

    # X_max is a necessary asymptotic gate but cannot select among profiles.
    d = sp.symbols("d", positive=True)
    profile_1 = sp.tanh(d)
    profile_2 = 1 - sp.exp(-d)
    checks.exact("xmax_profile_1_limit", sp.limit(profile_1, d, sp.oo), 1)
    checks.exact("xmax_profile_2_limit", sp.limit(profile_2, d, sp.oo), 1)
    checks.truth("xmax_gate_nonunique", sp.simplify(profile_1 - profile_2) != 0)

    failed = [row for row in checks.rows if not row["passed"]]
    dispositions = {name: sum(row["disposition"] == name for row in atlas) for name in sorted(ALLOWED)}
    result = {
        "schema": "udt-founding-pair-relation-ownership-v1",
        "base": "3c8a4a2dce3f31a15c58949efc8eaf2b9a39a977",
        "preregistration_commit": "1ab46192",
        "source_freeze_commit": "09c3d5d6",
        "primary_landing": "CONDITIONAL_QUERY_ENRICHMENT",
        "secondary_landing": "ASSOCIATIVE_CALIBRATION_CARRY_NOT_OWNED",
        "atlas_rows": len(atlas),
        "disposition_counts": dispositions,
        "checks_total": len(checks.rows),
        "checks_passed": len(checks.rows) - len(failed),
        "checks_failed": len(failed),
        "failed": failed,
        "checks": checks.rows,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write-atlas", action="store_true")
    args = parser.parse_args()
    result = derive(args.write_atlas)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["checks_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
