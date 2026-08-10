#!/usr/bin/env python3
"""Exact controller for the three-observer overlap/calibration-carry audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

ALLOWED = {
    "ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS",
    "SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY",
    "TRIPLE_OVERLAP_OBSTRUCTION_NONTRIVIAL",
    "LOOP_HOLONOMY_NONTRIVIAL",
    "BRANCH_LABEL_REQUIRED",
    "PARTIAL_OVERLAP_ONLY",
    "DEGENERATE_OR_UNDEFINED",
    "COMMON_SCALE_PRESENTATION_ONLY",
    "COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY",
    "MIDDLE_CALIBRATION_MISMATCH_SURVIVES",
    "RECIPROCITY_COVARIANT_NOT_SELECTOR",
    "SCALAR_PROJECTION_NOT_OWNED",
    "OPEN_NOT_DECIDED_BY_SUPPLIED_DATA",
}


def R(disposition: str, basis: str) -> tuple[str, str]:
    assert disposition in ALLOWED
    return disposition, basis


# Each case declares all twelve axes in AUDIT_AXIS_ARENA.tsv order. These are semantic/type
# classifications, not merit scores.
ADJUDICATION: dict[str, list[tuple[str, str]]] = {
    "C01": [
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Objects are calibrated chart germs and arrows are genuine overlap transitions."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The metric supplies pullbacks after the common atlas/query is supplied."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "A regular open triple overlap is part of this case."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The ordinary Jacobian chain rule gives J_BC J_AB=J_AC."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "One tensor field obeys h_A=J_AB^T h_B J_AB on every overlap."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The common chart object makes the target B germ equal to the source B germ."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "Coherent endpoint presentation changes cancel in the transition cocycle."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The full Jacobian chain retains every mixing entry."),
        R("SCALAR_PROJECTION_NOT_OWNED", "Full matrix descent does not by itself select a reciprocal scalar character."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The Cech triangle product is identity on a genuine atlas."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reversal inverts transitions and preserves closure without selecting the atlas."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Carry is exact for this supplied common-atlas type."),
    ],
    "C02": [
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Objects are separate parameterizations of one supplied image with explicit transition maps."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The common image and inverse chart maps are supplied; their Jacobians are derived."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Invertible overlaps exist by the case declaration."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Differentiating chart composition gives the exact chain."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Pullbacks agree under the explicit transitions."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The transition identifies the two B presentations."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "Coherent chart/frame changes do not change identity versus obstruction."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Complete Jacobians retain off-diagonal data."),
        R("SCALAR_PROJECTION_NOT_OWNED", "A scalar projection still needs the reciprocal reduction/local system."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The triangle obstruction is identity."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reverse transitions are the supplied inverses."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The supplied common image closes the carry conditionally."),
    ],
    "C03": [
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Pair surfaces Sigma_AB Sigma_BC and Sigma_AC are maps to M, not automatically composable arrows."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "The metric derives each pullback after its query but not one common image."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "A common open overlap is not guaranteed."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "No Jacobian chain is typed until overlap transitions are supplied."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Equal or compatible pullback metrics do not identify embeddings."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "The two B germs are distinct unless an explicit transition identifies them."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "Calling a reciprocal mismatch common scale would erase physical typed data."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Each map may retain mixing but there is no common product yet."),
        R("SCALAR_PROJECTION_NOT_OWNED", "Three terminal readouts are not automatically one edge cocycle."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "A triangle obstruction is undefined without typed comparison transitions."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reciprocity reverses every supplied relation but does not identify the three surfaces."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Independent pair surfaces require an additional overlap/middle transition."),
    ],
    "C04": [
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The target state of AB is literally the source state of BC."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Ownership is conditional on the declared matched state."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The state overlap is supplied even if no global chart atlas is claimed."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Matrix/function composition is associative once domains match."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Metric compatibility is testable on the matched germ."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "No middle reset is inserted because the object is identical."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "A coherent change of the shared B basis cancels between incident arrows."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Full mixing passes through the exact product."),
        R("SCALAR_PROJECTION_NOT_OWNED", "Additive scalar depth follows only if the carried state has the owned reciprocal character."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Associativity does not force a separately supplied direct AC arrow to equal the composite."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Matched reversal is exact but does not impose path independence."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The carry operation itself is closed on matched enriched objects."),
    ],
    "C05": [
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "AB ends in B_in while BC begins in distinct B_out."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "The metric does not identify separately declared B states."),
        R("PARTIAL_OVERLAP_ONLY", "Both touch observer B but this is not yet a full calibration-state overlap."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Composition is typed only after a map M_B:B_in->B_out is supplied."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Pairwise metric calibration does not select M_B."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "Setting M_B=I without equality of objects is an unregistered premise."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "An unmatched reciprocal reset is not a common scalar rescaling."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "A supplied complete M_B must retain its mixing entries."),
        R("SCALAR_PROJECTION_NOT_OWNED", "The scalar reset is readable only after M_B and a reciprocal reduction are supplied."),
        R("TRIPLE_OVERLAP_OBSTRUCTION_NONTRIVIAL", "The typed product exposes any unclosed middle mismatch."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reversal maps the mismatch to its inverse; it need not make it identity."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "Current premises do not own the missing B transition."),
    ],
    "C06": [
        R("COMMON_SCALE_PRESENTATION_ONLY", "Objects differ by consistent positive scalar basis choices."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "No new metric structure or physics is introduced."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The underlying overlap remains unchanged."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Endpoint scale factors telescope in the chain."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "Metric components transform covariantly with the bases."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "The same B scale appears inversely on its two incident arrows."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "The complete triangle product is unchanged by scalar conjugation."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Scalar changes do not zero existing mixing entries."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "The terminal reciprocal ratio cancels common clock/ruler scale."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "No obstruction is manufactured by coherent common scale."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Frame exchange respects the cancellation."),
        R("COMMON_SCALE_PRESENTATION_ONLY", "This case is presentation, not an ownership law."),
    ],
    "C07": [
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "This case changes the declared basis of an already supplied calibration local system coherently."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "It is not a claim that physical reciprocal refactorization of a tape is gauge."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The same underlying overlap remains."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "The B reciprocal basis change cancels between adjacent arrows."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "Pullback components change covariantly while geometry is fixed."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "One B trivialization is used on both incident edges."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "Triangle identity is invariant; nonidentity obstruction changes by conjugation."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Full off-diagonal data remain in the conjugated matrices."),
        R("SCALAR_PROJECTION_NOT_OWNED", "Local scalar coordinates can shift by a coboundary; periods/closure are invariant."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "A coherent zero-cochain cannot remove genuine holonomy."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Exchange maps the conjugacy class covariantly."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "Only coherent presentation freedom is removed; physical resets remain typed."),
    ],
    "C08": [
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Arrows are full regular overlap Jacobians with nonzero mixing blocks."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The metric supplies their entries only after the complete maps are supplied/derived from queries."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Regular invertible overlaps are declared."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Matrix composition retains mixing and is associative."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Full pullback compatibility is checked without block projection."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "The complete B transition, not a diagonal quotient, identifies states."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "Coherent basis changes conjugate the complete obstruction."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Exact witnesses retain nonzero off-diagonal products."),
        R("SCALAR_PROJECTION_NOT_OWNED", "No character on arbitrary full mixing is silently selected."),
        R("TRIPLE_OVERLAP_OBSTRUCTION_NONTRIVIAL", "A nonidentity complete product can survive even when every edge is metric-compatible."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reversal gives inverse/conjugate obstruction."),
        R("SCALAR_PROJECTION_NOT_OWNED", "Complete matrix carry is stronger than and does not select scalar depth."),
    ],
    "C09": [
        R("BRANCH_LABEL_REQUIRED", "Objects include explicit path/cut-locus branch labels."),
        R("BRANCH_LABEL_REQUIRED", "The metric supplies the branch relation after the query, not a preferred member."),
        R("BRANCH_LABEL_REQUIRED", "Overlap is branchwise and may be multivalued globally."),
        R("BRANCH_LABEL_REQUIRED", "Composition is defined only for compatible concatenated labels."),
        R("BRANCH_LABEL_REQUIRED", "Each regular branch has its own pullback compatibility test."),
        R("BRANCH_LABEL_REQUIRED", "The B state includes the incoming and outgoing branch data."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "Coherent frame changes do not collapse branch labels."),
        R("BRANCH_LABEL_REQUIRED", "Mixing is retained separately on every branch."),
        R("SCALAR_PROJECTION_NOT_OWNED", "Branchwise terminal depths need not descend to one endpoint scalar."),
        R("BRANCH_LABEL_REQUIRED", "Different triangle paths can legitimately define different arrows/holonomy."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reciprocity reverses branch labels rather than selecting one."),
        R("BRANCH_LABEL_REQUIRED", "The honest output is a branch-labelled relation."),
    ],
    "C10": [
        R("LOOP_HOLONOMY_NONTRIVIAL", "A loop is a composable sequence based at one calibrated object."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "The metric does not select a loop transport without the relation family."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Every adjacent overlap is supplied on the loop."),
        R("ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS", "Rebracketing the ordered loop product changes nothing."),
        R("LOOP_HOLONOMY_NONTRIVIAL", "Metric-compatible path transports may have nonidentity isometric holonomy."),
        R("SUPPLIED_TRANSITION_CLOSES_CARRY_CONDITIONALLY", "Every intermediate state must be matched or explicitly bridged."),
        R("COHERENT_RECIPROCAL_GAUGE_PRESENTATION_ONLY", "A base-frame change conjugates loop holonomy."),
        R("LOOP_HOLONOMY_NONTRIVIAL", "Mixing can be part of the nonabelian holonomy."),
        R("SCALAR_PROJECTION_NOT_OWNED", "A scalar period exists only for an owned character/local system."),
        R("LOOP_HOLONOMY_NONTRIVIAL", "Exact witnesses show nonidentity loop products are compatible with associativity."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Loop reversal gives inverse holonomy, not forced identity."),
        R("LOOP_HOLONOMY_NONTRIVIAL", "Nontrivial holonomy is allowed on path-labelled arrows; it is not a Cech-chart cocycle."),
    ],
    "C11": [
        R("PARTIAL_OVERLAP_ONLY", "The common object is a lower-dimensional seam rather than an open pair cell."),
        R("PARTIAL_OVERLAP_ONLY", "The metric supplies induced seam data but not missing transverse calibration."),
        R("PARTIAL_OVERLAP_ONLY", "No invertible two-dimensional overlap map exists."),
        R("PARTIAL_OVERLAP_ONLY", "Only the tangent seam chain can be formed."),
        R("PARTIAL_OVERLAP_ONLY", "Induced seam metric agreement is weaker than full pair-metric descent."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "Transverse clock/ruler identification remains unowned."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "Scale/reset classification needs the missing transverse state."),
        R("PARTIAL_OVERLAP_ONLY", "Some angular/mixing components are not visible on the seam."),
        R("SCALAR_PROJECTION_NOT_OWNED", "A full reciprocal density cannot be inferred from seam data alone."),
        R("PARTIAL_OVERLAP_ONLY", "No full triple obstruction is defined."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Seam reversal does not complete the missing data."),
        R("PARTIAL_OVERLAP_ONLY", "The case remains a partial compatibility stratum."),
    ],
    "C12": [
        R("DEGENERATE_OR_UNDEFINED", "The regular calibration-arrow type fails or the required overlap is absent."),
        R("DEGENERATE_OR_UNDEFINED", "The metric identifies the degeneration but supplies no inverse Jacobian there."),
        R("DEGENERATE_OR_UNDEFINED", "No regular open triple overlap is available in at least one subcase."),
        R("DEGENERATE_OR_UNDEFINED", "The full transition chain or obstruction inverse is undefined."),
        R("DEGENERATE_OR_UNDEFINED", "Pullback metrics may be null/rank-deficient or live on disjoint domains."),
        R("MIDDLE_CALIBRATION_MISMATCH_SURVIVES", "A missing regular state cannot be identified by normalization."),
        R("OPEN_NOT_DECIDED_BY_SUPPLIED_DATA", "No gauge statement repairs rank loss or absent overlap."),
        R("DEGENERATE_OR_UNDEFINED", "Full mixing data may lose rank and cannot be projected away."),
        R("DEGENERATE_OR_UNDEFINED", "The terminal logarithmic readout diverges/fails on null or degenerate pair cells."),
        R("DEGENERATE_OR_UNDEFINED", "No full triangle/loop obstruction is defined without invertible arrows."),
        R("RECIPROCITY_COVARIANT_NOT_SELECTOR", "Reciprocity maps failure strata but does not regularize them."),
        R("DEGENERATE_OR_UNDEFINED", "Regular local branches survive separately; no global conclusion follows here."),
    ],
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def build_atlas(cases: list[dict[str, str]], axes: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for case in cases:
        entries = ADJUDICATION[case["case_id"]]
        assert len(entries) == len(axes)
        for axis, (disposition, basis) in zip(axes, entries):
            rows.append(
                {
                    "case_id": case["case_id"],
                    "case_name": case["case_name"],
                    "axis_id": axis["axis_id"],
                    "axis_name": axis["axis_name"],
                    "disposition": disposition,
                    "basis": basis,
                }
            )
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write-atlas", action="store_true")
    parser.add_argument(
        "--source-snapshot-root",
        type=Path,
        help="verify manifest hashes from an isolated authorized source snapshot instead of git show",
    )
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": str(detail)})

    cases = read_tsv(HERE / "OVERLAP_CASE_ARENA.tsv")
    axes = read_tsv(HERE / "AUDIT_AXIS_ARENA.tsv")
    atlas = build_atlas(cases, axes)
    check("case_count", len(cases) == 12, len(cases))
    check("axis_count", len(axes) == 12, len(axes))
    check("atlas_count", len(atlas) == 144, len(atlas))
    check("atlas_unique", len({(r["case_id"], r["axis_id"]) for r in atlas}) == 144)
    check("atlas_dispositions", all(r["disposition"] in ALLOWED for r in atlas))
    check("no_merit_filter", not any(word in r["basis"].lower() for r in atlas for word in ("desired universe", "best branch", "particle-like")))

    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    check("source_count", len(manifest) == 17, len(manifest))
    check("source_unique", len({r["path"] for r in manifest}) == 17)
    for index, row in enumerate(manifest, start=1):
        data = (
            (args.source_snapshot_root / row["path"]).read_bytes()
            if args.source_snapshot_root
            else subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        )
        check(f"source_{index:02d}", hashlib.sha256(data).hexdigest() == row["sha256"], row["path"])

    eta = sp.diag(-1, 1)
    J_ab = sp.Matrix([[2, 1], [1, 1]])
    J_bc = sp.Matrix([[1, 1], [2, 3]])
    J_ac = J_bc * J_ab
    check("mixing_nonzero", all(J_ac[i, j] != 0 for i in range(2) for j in range(2)), J_ac)
    check("true_atlas_chain", J_bc * J_ab == J_ac)
    omega = J_ac.inv() * J_bc * J_ab
    check("true_atlas_obstruction_identity", omega == sp.eye(2), omega)

    J_cd = sp.Matrix([[3, 1], [1, 1]])
    check("composition_associative", (J_cd * J_bc) * J_ab == J_cd * (J_bc * J_ab))

    S_a = sp.Matrix([[1, 1], [0, 1]])
    S_b = sp.diag(2, 3)
    S_c = sp.Matrix([[1, 0], [2, 1]])
    A_g = S_b * J_ab * S_a.inv()
    B_g = S_c * J_bc * S_b.inv()
    C_g = S_c * J_ac * S_a.inv()
    omega_g = C_g.inv() * B_g * A_g
    check("frame_covariant_chain", B_g * A_g == C_g)
    check("frame_covariant_obstruction", omega_g == S_a * omega * S_a.inv())

    scalar_a, scalar_b, scalar_c = map(sp.Rational, (2, 3, 5))
    SA, SB, SC = scalar_a * sp.eye(2), scalar_b * sp.eye(2), scalar_c * sp.eye(2)
    A_s = SB * J_ab * SA.inv()
    B_s = SC * J_bc * SB.inv()
    C_s = SC * J_ac * SA.inv()
    check("common_scale_telescope", B_s * A_s == C_s)

    def D(z: sp.Rational) -> sp.Matrix:
        return sp.diag(1 / z, z)

    R_a, R_b, R_c = D(sp.Rational(2)), D(sp.Rational(3)), D(sp.Rational(5))
    A_r = R_b * J_ab * R_a.inv()
    B_r = R_c * J_bc * R_b.inv()
    C_r = R_c * J_ac * R_a.inv()
    check("coherent_reciprocal_basis_telescope", B_r * A_r == C_r)
    check("coherent_reciprocal_obstruction_conjugates", C_r.inv() * B_r * A_r == R_a * omega * R_a.inv())

    S_in = sp.Matrix([[1, 1], [0, 1]])
    S_out = sp.Matrix([[1, 0], [1, 1]])
    A_in = S_in * J_ab
    B_out = J_bc * S_out.inv()
    M_b = S_out * S_in.inv()
    check("supplied_middle_transition_closes", B_out * M_b * A_in == J_ac)
    check("omitted_middle_transition_fails", B_out * A_in != J_ac)
    reset = D(sp.Rational(7))
    check("unmatched_reciprocal_reset_survives", J_ac.inv() * J_bc * reset * J_ab != sp.eye(2))

    h_a = eta
    h_b = J_ab.inv().T * h_a * J_ab.inv()
    h_c = J_bc.inv().T * h_b * J_bc.inv()
    check("pairwise_metric_AB", J_ab.T * h_b * J_ab == h_a)
    check("pairwise_metric_BC", J_bc.T * h_c * J_bc == h_b)
    check("composite_metric_AC", J_ac.T * h_c * J_ac == h_a)
    H = sp.Matrix([[sp.Rational(5, 3), sp.Rational(4, 3)], [sp.Rational(4, 3), sp.Rational(5, 3)]])
    J_ac_path = J_ac * H
    omega_path = J_ac_path.inv() * J_bc * J_ab
    check("lorentz_holonomy_preserves_metric", H.T * eta * H == eta)
    check("direct_path_pairwise_metric_compatible", J_ac_path.T * h_c * J_ac_path == h_a)
    check("pairwise_metric_not_cech_closure", omega_path == H.inv() and omega_path != sp.eye(2), omega_path)
    check("reversed_triangle_inverse", J_ab.inv() * J_bc.inv() * J_ac_path == omega_path.inv())

    J_ca = H * J_ac.inv()
    loop = J_ca * J_bc * J_ab
    check("nontrivial_loop_holonomy", loop == H and loop != sp.eye(2), loop)
    check("loop_reversal", J_ab.inv() * J_bc.inv() * J_ca.inv() == H.inv())

    z1, z2, z3 = sp.Rational(2), sp.Rational(3), sp.Rational(5)
    scalar_omega = D(z3).inv() * D(z2) * D(z1)
    check("pure_reciprocal_composition", D(z2) * D(z1) == D(z1 * z2))
    check("scalar_triangle_multiplier", scalar_omega == D(z1 * z2 / z3), scalar_omega)
    check("scalar_triangle_nonzero_control", scalar_omega != sp.eye(2))
    check("scalar_triangle_zero_control", D(z1 * z2).inv() * D(z2) * D(z1) == sp.eye(2))

    full_product = J_bc * J_ab
    diagonal_shortcut = sp.diag(J_bc[0, 0], J_bc[1, 1]) * sp.diag(J_ab[0, 0], J_ab[1, 1])
    check("mixing_not_diagonal_shortcut", full_product != diagonal_shortcut, (full_product, diagonal_shortcut))

    h_terminal = sp.Matrix([[-sp.Rational(3, 16), sp.Rational(1, 12)], [sp.Rational(1, 12), sp.Rational(37, 9)]])
    exp_four_phi = (-h_terminal.det()) / h_terminal[0, 0] ** 2
    check("terminal_orchestra_witness", h_terminal.det() == -sp.Rational(7, 9) and exp_four_phi == sp.Rational(1792, 81), exp_four_phi)

    rank_one = sp.Matrix([[1, 2], [2, 4]])
    check("degenerate_overlap_no_inverse", rank_one.det() == 0)

    overall = {
        "primary_landing": "ASSOCIATIVE_CARRY_DERIVED_FOR_COMPOSABLE_ENRICHED_QUERY_ARROWS",
        "secondary_landing": "DIRECT_EQUALS_COMPOSITE_IS_PATH_INDEPENDENCE_OR_CECH_DESCENT_NOT_ASSOCIATIVITY",
        "general_landing": "SUPPLIED_RELATION_FAMILY_RETURNS_TYPED_TRIANGLE_LOOP_BRANCH_OR_DEGENERACY_STATUS",
        "remaining_open": "PHYSICAL_OWNERSHIP_OF_ONE_COMPATIBLE_GLOBAL_RELATION_FAMILY_AND_ANY_SCALAR_RECIPROCAL_REDUCTION",
    }
    failed = [item["name"] for item in checks if not item["passed"]]
    result = {
        "schema": "udt-three-observer-overlap-calibration-carry-v1",
        "base": "ea243c7c",
        "cases": len(cases),
        "axes": len(axes),
        "atlas_rows": len(atlas),
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "checks_failed": len(failed),
        "failed": failed,
        "checks": checks,
        **overall,
    }
    if args.write_atlas:
        write_tsv(HERE / "OVERLAP_OWNERSHIP_ATLAS.tsv", atlas)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
