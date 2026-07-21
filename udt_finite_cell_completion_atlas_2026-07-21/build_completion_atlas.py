#!/usr/bin/env python3
"""Build the law-neutral finite-cell completion type-space atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLASSIFICATION = "CURRENT_FINITE_CELL_COMPLETION_TYPE_SPACE_MAPPED_WITH_UNBOUNDED_REMAINDERS"
MAXIMUM = "UDT_FINITE_CELL_COMPLETION_CONFIGURATION_ATLAS_CHARACTERIZED_WITHOUT_DYNAMICS"

SOURCES = [
    ("S01", "UDT_NATIVE_ACTION_COLD_PACKET.md", "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0", "founding and finite-cell authority"),
    ("S02", "udt_premise_reset_audit_2026-07-19/SHA256SUMS.txt", "6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7", "corrected phi distance scale and boundary meanings"),
    ("S03", "udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt", "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38", "P00 whole-space protocol"),
    ("S04", "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt", "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad", "P01 law-neutral geometry interface"),
    ("S05", "udt_local_jet_atlas_p02_2026-07-21/SHA256SUMS.txt", "c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938", "P02 complete registered local marginal strata"),
    ("S06", "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt", "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be", "P03 founded constraint effects"),
    ("S07", "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt", "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9", "P03G global assembly axes and uncounted moduli"),
    ("S08", "udt_dynamics_branch_ruling_p04_2026-07-21/SHA256SUMS.txt", "d01d65fc5abcc35078c961d0d3fc0eec7ad26e205735a77f7d83e2b45121de3f", "conditional dynamics status only"),
    ("S09", "udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt", "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e", "conditional bulk and boundary-current status"),
    ("S10", "udt_pre_p06_boundary_selector_audit_2026-07-21/SHA256SUMS.txt", "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51", "boundary-family nonselection evidence"),
    ("S11", "udt_time_live_characteristic_flux_audit_2026-07-21/SHA256SUMS.txt", "3089e66d65f85753d45e9e78596dba9ae2b962a015857c969ff6a0492d442f12", "time-live causal and flux families"),
    ("S12", "udt_free_global_seal_transversality_audit_2026-07-21/SHA256SUMS.txt", "5198a69a1b8a3026af529bccd4d47639d718a21fc1153947b3ebfab8720502d8", "free-embedding and transversality families"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for source_id, rel, expected, role in SOURCES:
        check(f"source_{source_id}", sha256(ROOT / rel) == expected)
    write_tsv("SOURCE_LINEAGE.tsv", ["id", "path", "sha256", "role"], [
        {"id": sid, "path": path, "sha256": digest, "role": role}
        for sid, path, digest, role in SOURCES
    ])

    parent_tables = [
        ("METRIC_INERTIA", "udt_local_jet_atlas_p02_2026-07-21/ZERO_JET_INERTIA_STRATA.tsv", 15),
        ("SPLIT_INERTIA", "udt_local_jet_atlas_p02_2026-07-21/SPLIT_ZERO_JET_STRATA.tsv", 36),
        ("DPHI", "udt_local_jet_atlas_p02_2026-07-21/DPHI_FIRST_JET_STRATA.tsv", 8),
        ("SPLIT_FIRST_JET", "udt_local_jet_atlas_p02_2026-07-21/SPLIT_FIRST_JET_STRATA.tsv", 12),
        ("CURVATURE_RANK", "udt_local_jet_atlas_p02_2026-07-21/CURVATURE_OPERATOR_RANK_STRATA.tsv", 7),
        ("RICCI_RANK", "udt_local_jet_atlas_p02_2026-07-21/RICCI_ENDOMORPHISM_RANK_STRATA.tsv", 5),
        ("PETROV", "udt_local_jet_atlas_p02_2026-07-21/PETROV_STRATA.tsv", 6),
    ]
    carry_rows: list[dict[str, object]] = []
    for atlas, rel, expected_count in parent_tables:
        rows = read_tsv(ROOT / rel)
        check(f"parent_{atlas}_count", len(rows) == expected_count)
        for row in rows:
            canonical = json.dumps(row, sort_keys=True, separators=(",", ":"))
            carry_rows.append({
                "atlas": atlas,
                "source_id": row["id"],
                "source_path": rel,
                "parent_row_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
                "treatment": "CARRIED_WITHOUT_RANKING",
            })
    check("p02_marginal_total", len(carry_rows) == 89)
    check("p02_identity_unique", len({(r["atlas"], r["source_id"]) for r in carry_rows}) == 89)
    p03_rows = read_tsv(ROOT / "udt_founded_constraint_atlas_p03_2026-07-21/SURVIVING_STRATA.tsv")
    check("p03_all_89_accounted", len(p03_rows) == 89 and len({(r["atlas"], r["source_id"]) for r in p03_rows}) == 89)
    p03g_axes = read_tsv(ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv")
    p03g_uncounted = read_tsv(ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21/UNCOUNTED_GLOBAL_MODULI.tsv")
    check("p03g_axis_count", len(p03g_axes) == 12)
    check("p03g_uncounted_count", len(p03g_uncounted) == 15)
    p00_dofs = read_tsv(ROOT / "udt_complete_metric_solution_space_map_2026-07-21/COMPLETE_METRIC_DOF_LEDGER.tsv")
    check("p00_dof_count", len(p00_dofs) == 24)
    check("ten_conditional_metric_slots", sum(int(r["metric_slot_count"]) for r in p00_dofs) == 10)
    write_tsv("P02_MARGINAL_CARRYFORWARD.tsv", ["atlas", "source_id", "source_path", "parent_row_sha256", "treatment"], carry_rows)
    write_tsv("PARENT_ATLAS_CENSUS.tsv", ["parent", "object", "count", "treatment"], [
        {"parent": "P00", "object": "complete_dof_rows", "count": 24, "treatment": "all retained"},
        {"parent": "P00", "object": "conditional_metric_slots", "count": 10, "treatment": "all-coordinate and unranked"},
        {"parent": "P02", "object": "marginal_registered_strata", "count": 89, "treatment": "identity carryforward"},
        {"parent": "P03", "object": "founded-constraint-accounted_strata", "count": 89, "treatment": "no local deletion"},
        {"parent": "P03G", "object": "global_assembly_axes", "count": 12, "treatment": "all open/partial statuses retained"},
        {"parent": "P03G", "object": "uncounted_global_moduli", "count": 15, "treatment": "not discretized away"},
    ])

    axes = [
        ("X01", "METRIC_ZERO_JET", "finite_marginals_plus_continuous", "15 inertia rows plus continuous congruence data", "degenerate and other-signature closure"),
        ("X02", "METRIC_HIGHER_JETS", "functional_unbounded", "P02 complete second-jet point atlas", "all orders nonsmooth and singular remainder"),
        ("X03", "PHI_ZERO_SET", "functional_topological_unbounded", "regular and finite-order germ witnesses", "arbitrary closed and stratified zero-set remainder"),
        ("X04", "CAUSAL_TIME_LIVE", "functional_unbounded", "all local causal dphi classes", "moving branching type-changing histories"),
        ("X05", "FIELD_COFRAME_BUNDLE", "functional_topological_unbounded", "seven registered local realizations", "field-dependent transitions and unenumerated bundles"),
        ("X06", "ANGULAR_MIXED_GEOMETRY", "functional_topological_unbounded", "all screen shear/twist ranks and ten slots", "off-toric collapse and arbitrary screen topology"),
        ("X07", "GLOBAL_INCIDENCE", "combinatorial_topological_unbounded", "cover and bounded witness families", "arbitrary covers gluings corners and networks"),
        ("X08", "TRANSITION_COCYCLE", "functional_groupoid_unbounded", "constant two-channel group law", "full field-dependent 4D cocycles"),
        ("X09", "VARIATION_CHANNEL", "functional_unbounded", "conditional raw L01/L02 currents", "boundary interface cap quotient and corner functionals"),
        ("X10", "GLOBAL_OUTPUT", "not_evaluable", "status-only placeholders", "representative scale Xmax mass volume density bootstrap"),
    ]
    axis_rows = [{"id": i, "axis": a, "cardinality_kind": k, "registered_coverage": c, "required_remainder": r, "ranking_allowed": "NO"} for i, a, k, c, r in axes]
    check("ten_completion_axes", len(axis_rows) == 10)
    check("no_axis_ranking", all(r["ranking_allowed"] == "NO" for r in axis_rows))
    write_tsv("COMPLETION_AXIS_SCHEMA.tsv", ["id", "axis", "cardinality_kind", "registered_coverage", "required_remainder", "ranking_allowed"], axis_rows)

    phi_rows = [
        ("Z01", "EMPTY_ZERO_SET", "phi has fixed nonzero sign", "OPEN_FAMILY"),
        ("Z02", "IDENTICALLY_ZERO", "phi zero on complete connected region", "TRIVIAL_FIELD_FAMILY"),
        ("Z03", "REGULAR_LEVEL_HYPERSURFACE", "dphi nonzero on zero set", "IMPLICIT_FUNCTION_STRATUM"),
        ("Z04", "FINITE_ODD_ORDER_CONTACT", "first nonzero normal order odd and at least three", "CRITICAL_SIGN_CROSSING"),
        ("Z05", "FINITE_EVEN_ORDER_CONTACT", "first nonzero normal order even", "CRITICAL_TOUCHING"),
        ("Z06", "MORSE_OR_QUADRATIC_CRITICAL_ZERO", "nondegenerate Hessian with arbitrary inertia", "CONE_ISOLATED_OR_BRANCHING_BY_SIGNATURE"),
        ("Z07", "POSITIVE_DIMENSIONAL_CRITICAL_ZERO", "dphi zero along part or all of zero set", "CRITICAL_SUBMANIFOLD_OR_STRATUM"),
        ("Z08", "MULTIPLE_COMPONENT_ZERO_SET", "two or more disjoint or intersecting components", "GLOBAL_INCIDENCE_OPEN"),
        ("Z09", "ZERO_ON_OPEN_REGION", "phi vanishes on a nonempty open set but not necessarily globally", "SMOOTH_NONANALYTIC_ALLOWED"),
        ("Z10", "INFINITE_ORDER_FLAT_ZERO", "all finite jets vanish at some zero", "NOT_CLASSIFIED_BY_FINITE_JET_ATLAS"),
        ("Z11", "NONSMOOTH_OR_DISTRIBUTIONAL_ZERO", "phi regularity below smooth", "REGULARITY_BRANCH_OPEN"),
        ("Z12", "ARBITRARY_CLOSED_OR_OTHER_STRATIFIED_ZERO_SET", "unrestricted smooth-category remainder without EOM or analyticity", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("PHI_ZERO_SET_ATLAS.tsv", ["id", "family", "defining_property", "status"], [
        {"id": i, "family": f, "defining_property": d, "status": s} for i, f, d, s in phi_rows
    ])
    check("phi_remainder_present", phi_rows[-1][1].startswith("ARBITRARY_CLOSED"))

    germ_rows = []
    for order in range(1, 7):
        germ_rows.append({
            "id": f"G{order:02d}",
            "germ": f"n^{order}",
            "first_nonzero_order": order,
            "first_nonzero_derivative": math.factorial(order),
            "gradient_regular": "YES" if order == 1 else "NO",
            "sign_behavior": "CROSSING" if order % 2 else "TOUCHING",
            "zero_geometry": "LOCAL_HYPERSURFACE_SET_n_zero",
        })
    germ_rows.extend([
        {"id": "G07", "germ": "n^2-y^2", "first_nonzero_order": 2, "first_nonzero_derivative": "HESSIAN_INDEFINITE", "gradient_regular": "NO_AT_ORIGIN", "sign_behavior": "BRANCHING", "zero_geometry": "TWO_INTERSECTING_BRANCHES"},
        {"id": "G08", "germ": "n^2+y^2", "first_nonzero_order": 2, "first_nonzero_derivative": "HESSIAN_POSITIVE", "gradient_regular": "NO_AT_ORIGIN", "sign_behavior": "NO_SIGN_CHANGE", "zero_geometry": "CODIMENSION_TWO_IN_n_y_SLICE"},
        {"id": "G09", "germ": "n*(n^2-1)", "first_nonzero_order": 1, "first_nonzero_derivative": -1, "gradient_regular": "YES_AT_ALL_THREE_ROOTS", "sign_behavior": "MULTIPLE_CROSSINGS", "zero_geometry": "THREE_COMPONENTS_IN_ONE_DIMENSION"},
    ])
    check("finite_germ_count", len(germ_rows) == 9)
    check("odd_even_germ_coverage", {r["sign_behavior"] for r in germ_rows[:6]} == {"CROSSING", "TOUCHING"})
    write_tsv("FINITE_ORDER_GERM_WITNESSES.tsv", ["id", "germ", "first_nonzero_order", "first_nonzero_derivative", "gradient_regular", "sign_behavior", "zero_geometry"], germ_rows)

    regularity = [
        ("M01", "REGULAR_LORENTZIAN", "nonzero determinant inertia 1/3 or 3/1", "P02_CARRYFORWARD"),
        ("M02", "REGULAR_OTHER_SIGNATURE", "nonzero determinant other inertia", "P02_CARRYFORWARD_NOT_FOUNDATION_EXCLUDED"),
        ("M03", "DEGENERATE_FIXED_RANK", "rank zero through three at a locus", "P02_CARRYFORWARD"),
        ("M04", "SIGNATURE_TYPE_CHANGE", "inertia changes across determinant-zero locus", "GLOBAL_EXTENSION_OPEN"),
        ("M05", "SMOOTH_CHART_EXTENSION", "components singular or degenerate in one chart but regular in another", "ATLAS_TRANSITION_REQUIRED"),
        ("M06", "FINITE_DIFFERENTIABILITY", "metric is Ck but not Ckplus1", "JET_MATCHING_BRANCH"),
        ("M07", "PIECEWISE_SMOOTH_INTERFACE", "one-sided jets exist with jumps", "DISTRIBUTIONAL_OR_MATCHING_BRANCH"),
        ("M08", "CURVATURE_SINGULAR", "invariant curvature diverges or fails distributionally", "RETAINED_OUTCOME"),
        ("M09", "METRIC_INCOMPLETE_WITH_EXTENSION_OPEN", "finite affine reach without supplied completion", "GLOBAL_CONTINUATION_BRANCH"),
        ("M10", "NONMANIFOLD_OR_STRATIFIED_METRIC_SPACE", "local manifold model fails at a stratum", "RETAINED_GLOBAL_BRANCH"),
        ("M11", "OTHER_REGULARITY_OR_GENERALIZED_GEOMETRY", "unclassified regularity completion", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("METRIC_REGULARITY_ATLAS.tsv", ["id", "family", "defining_property", "status"], [{"id": i, "family": f, "defining_property": d, "status": s} for i, f, d, s in regularity])

    matching = [
        ("J01", "NO_DISTINGUISHED_JOIN", "single atlas with no marked completion surface", "no matching equation"),
        ("J02", "C0_JOIN", "metric and fields agree in value under transition", "higher jets may jump"),
        ("J03", "C1_JOIN", "value and first jets agree under transition", "second and higher jets may jump"),
        ("J04", "C2_JOIN", "jets through order two agree under transition", "higher jets may jump"),
        ("J05", "CK_JOIN", "jets through declared finite k agree under transition", "k is free branch datum"),
        ("J06", "CINFINITY_JOIN", "all finite jets match under full transition", "analyticity does not follow"),
        ("J07", "ANALYTIC_JOIN", "convergent local expansions agree", "analyticity is an extra premise"),
        ("J08", "DISTRIBUTIONAL_JOIN", "finite jumps with declared weak geometry", "junction functional and products open"),
        ("J09", "SINGULAR_OR_OTHER_MATCHING", "transition or jet class outside listed regularities", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    check("matching_remainder", matching[-1][3] == "OTHER_UNENUMERATED_REQUIRED")
    write_tsv("JET_MATCHING_ATLAS.tsv", ["id", "family", "condition", "limit"], [{"id": i, "family": f, "condition": c, "limit": l} for i, f, c, l in matching])

    causal = [
        ("T01", "NO_DISTINGUISHED_SURFACE", "none", "static_or_time_live"),
        ("T02", "REGULAR_TIMELIKE_SURFACE", "spacelike normal", "fixed_moving_or_general"),
        ("T03", "REGULAR_NULL_SURFACE", "null normal", "characteristic_status_law_dependent"),
        ("T04", "REGULAR_SPACELIKE_SURFACE", "timelike normal", "initial_final_or_internal_role_law_dependent"),
        ("T05", "CAUSAL_TYPE_CHANGING_SURFACE", "normal norm changes sign", "transition locus retained"),
        ("T06", "DEGENERATE_NORMAL_OR_METRIC", "normal or inverse metric undefined", "separate generalized branch"),
        ("T07", "STATIC_EMBEDDING", "embedding independent of time coordinate", "one time-live stratum only"),
        ("T08", "STATIONARY_NONSTATIC_EMBEDDING", "time symmetry with nonzero shifts or rotation", "mixed slots retained"),
        ("T09", "GENERAL_MOVING_EMBEDDING", "all coordinate dependence", "no velocity law supplied"),
        ("T10", "BRANCHING_MERGING_OR_MULTICOMPONENT_HISTORY", "surface incidence changes", "global time topology open"),
        ("T11", "OTHER_NONSURFACE_OR_GENERALIZED_HISTORY", "not captured by regular embeddings", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("CAUSAL_TIME_LIVE_ATLAS.tsv", ["id", "family", "geometric_data", "scope"], [{"id": i, "family": f, "geometric_data": d, "scope": s} for i, f, d, s in causal])

    field = [
        ("F01", "METRIC_ONLY", "metric or conformal-metric transition", "phi is derived coordinate or absent only if branch says so"),
        ("F02", "INDEPENDENT_ORDINARY_PHI_SCALAR", "scalar transition", "global scalar and zero set required"),
        ("F03", "INDEPENDENT_TWISTED_OR_SIGN_PHI", "line-bundle equivariant transition", "bundle and cocycle required"),
        ("F04", "COFRAME_FIELD", "Lorentz conformal or broader supplied soldering", "frame gauge and torsion status required"),
        ("F05", "PROJECTOR_OR_PLANE_FIELD", "Grassmannian/projector transition", "rank integrability and type change retained"),
        ("F06", "MULTIPLIER_OR_CONSTRAINT_FIELD", "dual-bundle transition", "variation domain changes"),
        ("F07", "TWO_STAGE_OR_BRIDGE_FIELDS", "stagewise transition and matching", "no bridge operator exists"),
        ("F08", "INDEPENDENT_CONNECTION", "affine/principal-bundle connection transition", "torsion nonmetricity and holonomy open"),
        ("F09", "CARRIER_OR_OTHER_EXTRA_FIELD", "field-specific bundle transition", "carrier agnostic parent retained"),
        ("F10", "MIXED_FIELD_REALIZATION", "several preceding objects simultaneously", "complete equation census required later"),
        ("F11", "OTHER_COMPATIBLE_FIELD_BUNDLE", "unclassified field-dependent transition", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("FIELD_BUNDLE_ATLAS.tsv", ["id", "family", "transition_kind", "required_data"], [{"id": i, "family": f, "transition_kind": t, "required_data": r} for i, f, t, r in field])

    angular = [
        ("A01", "POSITIVE_REGULAR_SCREEN", "arbitrary three screen metric slots", "all coordinates"),
        ("A02", "INDEFINITE_OR_DEGENERATE_SCREEN", "all split inertia closures", "type change retained"),
        ("A03", "NONZERO_SCREEN_SHEAR", "rank one or two shear", "CSN invariant rank"),
        ("A04", "ZERO_OR_NONZERO_TWIST", "integrable and nonintegrable screen distributions", "both retained"),
        ("A05", "TIME_ANGULAR_SHIFT", "M07 and M08 slots", "stationary and time-live mixing"),
        ("A06", "DEPTH_ANGULAR_SHIFT", "M09 and M10 slots", "radial/depth twist and mixing"),
        ("A07", "MOVING_EIGENDIRECTIONS", "off-diagonal screen shape and chart transitions", "no global diagonal gauge"),
        ("A08", "NO_COLLAPSE_BOUNDARY", "screen remains nondegenerate at finite incidence", "boundary data open"),
        ("A09", "ONE_OR_MORE_CYCLE_COLLAPSES", "rank loss with local lattice/cap data", "toric and nontoric branches"),
        ("A10", "TORIC_PRIMITIVE_AND_NONPRIMITIVE_CAPS", "bounded lattice witness families", "not global exhaustive"),
        ("A11", "NON_TORIC_CAP_OR_FIXED_SET", "general group action or no group action", "functional topology open"),
        ("A12", "ANGULAR_TOPOLOGY_CHANGE_OR_STRATIFICATION", "screen bundle incidence changes", "generalized branch"),
        ("A13", "OTHER_ANGULAR_MIXED_COMPLETION", "arbitrary screen bundle metric and transition remainder", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    check("mixed_slots_present", {a[0] for a in angular if "SHIFT" in a[1]} == {"A05", "A06"})
    write_tsv("ANGULAR_MIXED_ATLAS.tsv", ["id", "family", "data", "scope"], [{"id": i, "family": f, "data": d, "scope": s} for i, f, d, s in angular])

    global_rows = [
        ("I01", "COMPACT_WITHOUT_BOUNDARY", "closed manifold or generalized closed space", "cover topology unbounded"),
        ("I02", "ONE_OR_MORE_RETAINED_BOUNDARIES", "boundary incidence and corners", "component count unbounded"),
        ("I03", "SMOOTH_EXTENSION_ACROSS_MARKED_SET", "single manifold continuation", "marked set may be bookkeeping"),
        ("I04", "PIECEWISE_INTERFACE", "two or more regions with matching data", "jump functional open"),
        ("I05", "PAIRWISE_GLUING", "boundary components joined by diffeomorphism and field transition", "mapping class unbounded"),
        ("I06", "MULTIPLE_OR_GRAPH_GLUING", "cell complex or network incidence", "combinatorial family unbounded"),
        ("I07", "CAP_COMPLETION", "one or more directions collapse", "local regularity and global topology separate"),
        ("I08", "FREE_QUOTIENT", "proper free action", "quotient has no fixed boundary"),
        ("I09", "FIXED_SET_QUOTIENT", "action with isotropy", "boundary orbifold or stratum by representation"),
        ("I10", "PERIODIC_OR_MAPPING_TORUS_COMPLETION", "cyclic base and monodromy", "transition class unbounded"),
        ("I11", "NONORIENTABLE_OR_TIME_NONORIENTABLE_COMPLETION", "orientation bundle nontrivial", "not excluded by local metric"),
        ("I12", "SINGULAR_OR_STRATIFIED_COMPLETION", "manifold regularity fails on strata", "retained"),
        ("I13", "MIXED_COMPLETION", "several incidence operations combined", "not reducible to one label"),
        ("I14", "OTHER_GLOBAL_INCIDENCE", "arbitrary cover nerve gluing and topology remainder", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("GLOBAL_INCIDENCE_ATLAS.tsv", ["id", "family", "construction", "scope"], [{"id": i, "family": f, "construction": c, "scope": s} for i, f, c, s in global_rows])

    quotient = [
        ("Q01", "TRIVIAL_ACTION", 0, "no quotient change"),
        ("Q02", "FREE_PROPER_ACTION", 0, "manifold quotient without fixed stratum"),
        ("Q03", "CODIMENSION_ONE_REFLECTION_ISOTROPY", 1, "local manifold-with-boundary model"),
        ("Q04", "CODIMENSION_TWO_ISOTROPY", 2, "orbifold or stratified transverse cone"),
        ("Q05", "CODIMENSION_THREE_ISOTROPY", 3, "higher-codimension fixed stratum"),
        ("Q06", "ISOLATED_FIXED_POINT", 4, "point singularity or orbifold model"),
        ("Q07", "NONFINITE_OR_CONTINUOUS_ISOTROPY", "variable", "orbit-type stratification"),
        ("Q08", "NONPROPER_ACTION", "variable", "non-Hausdorff or generalized quotient possible"),
        ("Q09", "FIELD_DEPENDENT_OR_AFFINE_ACTION", "variable", "full bundle equivariance required"),
        ("Q10", "OTHER_GROUP_OR_GROUPOID_ACTION", "unbounded", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("GROUP_ACTION_QUOTIENT_ATLAS.tsv", ["id", "family", "fixed_codimension", "local_result"], [{"id": i, "family": f, "fixed_codimension": c, "local_result": r} for i, f, c, r in quotient])

    variation = [
        ("V01", "NO_DYNAMICS_LOADED", "configuration family only", "no stationarity claim"),
        ("V02", "ONE_SIDED_FIXED_EMBEDDING", "raw field current", "functional and polarization open"),
        ("V03", "ONE_SIDED_MOVING_EMBEDDING", "field current plus displacement response", "shape functional open"),
        ("V04", "TWO_SIDED_SMOOTH_MATCHING", "difference of oriented currents", "cancellation requires complete matching"),
        ("V05", "TWO_SIDED_INTERFACE", "jump field and shape channels", "interface functional open"),
        ("V06", "CAP_REGULARITY", "shrinking-orbit and corner limits", "action-dependent differentiability"),
        ("V07", "QUOTIENT_DESCENT", "equivariant allowed variations", "fixed/free action dependent"),
        ("V08", "NULL_OR_CHARACTERISTIC_DATA", "generator cross-section and joint channels", "law dependent"),
        ("V09", "DEGENERATE_OR_TYPE_CHANGE_VARIATION", "inverse-free or generalized formulation required", "operator absent"),
        ("V10", "BOUNDARY_CORNER_LEGENDRE_IMPROVEMENT", "primitive polarization and corner ambiguity", "functional family unselected"),
        ("V11", "OTHER_VARIATION_COMPLETION", "unclassified off-shell domain", "OTHER_UNENUMERATED_REQUIRED"),
    ]
    write_tsv("VARIATION_CHANNEL_ATLAS.tsv", ["id", "family", "channel", "scope"], [{"id": i, "family": f, "channel": c, "scope": s} for i, f, c, s in variation])

    outputs = [
        ("O01", "PHYSICAL_CSN_REPRESENTATIVE", "NOT_EVALUABLE", "selection map absent"),
        ("O02", "ABSOLUTE_SCALE", "NOT_EVALUABLE", "scale breaker absent"),
        ("O03", "XMAX", "NOT_EVALUABLE", "complete global metric and scale closure absent"),
        ("O04", "PROPER_VOLUME", "BRANCH_FUNCTIONAL_OPEN", "complete slice and representative absent"),
        ("O05", "NATIVE_MASS_AND_CHARGE", "NOT_EVALUABLE", "source generator normalization absent"),
        ("O06", "TOTAL_DENSITY", "NOT_EVALUABLE", "mass and proper volume absent"),
        ("O07", "BOOTSTRAP_ADMISSIBILITY", "NOT_EVALUABLE", "complete matter-bearing solutions absent"),
        ("O08", "OTHER_GLOBAL_OUTPUT", "OTHER_UNENUMERATED_REQUIRED", "future complete theory may add derived outputs"),
    ]
    write_tsv("GLOBAL_OUTPUT_ATLAS.tsv", ["id", "object", "status", "reason"], [{"id": i, "object": o, "status": s, "reason": r} for i, o, s, r in outputs])

    relations = [
        ("R01", "dphi_nonzero_on_phi_zero", "regular_codimension_one_local_level_set", "DOES_NOT_SET_GLOBAL_INCIDENCE"),
        ("R02", "dphi_zero_on_phi_zero", "critical_zero_family", "ZERO_SET_DIMENSION_AND_SHAPE_NOT_FIXED"),
        ("R03", "positive_CSN", "preserves_metric_inertia_and_dphi_causal_type", "DOES_NOT_SELECT_REPRESENTATIVE"),
        ("R04", "Ck_gluing", "all_transformed_jets_through_k_match", "FULL_TRANSITION_REQUIRED"),
        ("R05", "free_proper_group_action", "manifold_quotient_without_fixed_set", "GLOBAL_ACTION_STILL_INPUT"),
        ("R06", "reflection_isotropy_codim_one", "local_boundary_quotient_model", "NOT_GLOBAL_ONTOLOGY_SELECTION"),
        ("R07", "higher_codimension_isotropy", "stratified_or_orbifold_local_model", "REPRESENTATION_DEPENDENT"),
        ("R08", "primitive_local_cycle_collapse", "local_smooth_toric_cap_possible", "DOES_NOT_FIX_MUTUAL_LATTICE_OR_TOPOLOGY"),
        ("R09", "finite_cell", "requires_finite_global_completion", "DOES_NOT_FIX_COVER_TOPOLOGY_OR_BOUNDARY"),
        ("R10", "static_odd_phi_rule", "one_static_zero_value_and_parity_stratum", "DOES_NOT_FIX_GLOBAL_ZERO_SET"),
        ("R11", "smooth_two_sided_soldering", "oppositely_oriented_internal_currents_may_cancel", "MATCHING_AND_ACTION_REQUIRED"),
        ("R12", "unmatched_interface", "jump_and_corner_channels_survive", "FUNCTIONAL_REQUIRED"),
        ("R13", "conditional_L01_or_L02_operator", "dynamics_status_index_only", "NO_COMPLETION_FAMILY_RANKING"),
        ("R14", "no_dynamics", "configuration_and_constraint_atlas_only", "NO_PHYSICAL_SOLUTION_LABEL"),
        ("R15", "finite_witness_list", "bounded_subfamily", "OTHER_UNENUMERATED_REMAINDER_REQUIRED"),
        ("R16", "time_dependent_configuration", "kinematic_history", "NOT_PHYSICAL_EVOLUTION_WITHOUT_OPERATOR"),
        ("R17", "regularity_class", "reported_property", "NOT_UNIVERSAL_MERIT_FILTER"),
        ("R18", "global_output_placeholder", "unevaluable_until_defining_objects_exist", "NO_CIRCULAR_CLOSURE"),
    ]
    write_tsv("COMPATIBILITY_RELATIONS.tsv", ["id", "antecedent", "consequence", "limit"], [{"id": i, "antecedent": a, "consequence": c, "limit": l} for i, a, c, l in relations])

    field_lanes = []
    for lane in ("L01_CONDITIONAL_C2", "L02_CONDITIONAL_EH", "L03_OPEN_BRIDGE"):
        for realization in ("C01_METRIC_ONLY", "C02_INDEPENDENT_PHI", "C03_COFRAME", "C04_PROJECTOR", "C05_MULTIPLIER", "C06_BRIDGE_FIELDS", "C07_CONNECTION_OR_EXTRA_FIELD"):
            field_lanes.append({
                "pair_id": f"{lane.split('_')[0]}_{realization.split('_')[0]}",
                "lane": lane,
                "realization": realization,
                "atlas_role": "STATUS_BOOKKEEPING_ONLY",
                "completion_status": "OPEN_OR_CONDITIONAL_UNSOLVED",
                "P06_ready": "NO",
            })
    check("field_lane_pairs", len(field_lanes) == 21 and len({r["pair_id"] for r in field_lanes}) == 21)
    check("no_p06_ready", all(r["P06_ready"] == "NO" for r in field_lanes))
    write_tsv("FIELD_LANE_STATUS.tsv", ["pair_id", "lane", "realization", "atlas_role", "completion_status", "P06_ready"], field_lanes)

    completeness = [
        ("C01", "FIELDS", "all ten metric slots plus field-bundle families retained", "complete off-shell field content remains open"),
        ("C02", "ACTION_TERMS", "conditional statuses indexed only", "native bulk boundary bridge and matter action absent"),
        ("C03", "FULL_EQUATIONS", "none solved", "all global nonlinear equations absent"),
        ("C04", "DOMAIN_COORDINATES", "all-coordinate local data and global incidence schema", "actual cover and atlas unselected"),
        ("C05", "BOUNDARY_REGULARITY", "regular degenerate matching and variation families", "complete boundary functional absent"),
        ("C06", "TOPOLOGY", "bounded witnesses plus mandatory unenumerated remainders", "global topology unclassified"),
        ("C07", "DYNAMICAL_CHARACTER", "static stationary moving and type-change configurations", "physical evolution law absent"),
        ("C08", "BRANCH_BIFURCATION", "configuration-family incidence only", "EOM branch graph absent"),
        ("C09", "STABILITY", "not entered", "complete perturbation operator absent"),
        ("C10", "REGIME_VALIDITY", "current-authority configuration/constrained space", "future laws and global solutions may regrade map"),
    ]
    write_tsv("TEN_CRITERION_SCOPE.tsv", ["id", "criterion", "covered", "open"], [{"id": i, "criterion": c, "covered": v, "open": o} for i, c, v, o in completeness])

    anti = [
        ("A01", "named edge seam or quotient used as organizing target", "ABSENT"),
        ("A02", "branch ranking or preference score", "ABSENT"),
        ("A03", "static spherical diagonal or round assumption", "ABSENT"),
        ("A04", "angular mixed shifts shear or twist omitted", "ABSENT"),
        ("A05", "regularity used as merit filter", "ABSENT"),
        ("A06", "finite witness list called exhaustive", "ABSENT"),
        ("A07", "unbounded functional remainder hidden", "ABSENT"),
        ("A08", "conditional action used to rank configurations", "ABSENT"),
        ("A09", "time dependence called physical evolution", "ABSENT"),
        ("A10", "GR carrier mass or empirical target loaded", "ABSENT"),
        ("A11", "degenerate singular trivial or disconnected family removed", "ABSENT"),
        ("A12", "P06 readiness inferred", "ABSENT"),
        ("A13", "global topology reduced to toric witnesses", "ABSENT"),
        ("A14", "phi zero set reduced to regular hypersurface", "ABSENT"),
        ("A15", "unknown global output filled by definition", "ABSENT"),
    ]
    check("anti_imposition_count", len(anti) == 15)
    write_tsv("ANTI_IMPOSITION_AUDIT.tsv", ["id", "failure_mode", "present"], [{"id": i, "failure_mode": f, "present": p} for i, f, p in anti])

    graph = {
        "schema": "udt-finite-cell-completion-atlas-graph-1.0",
        "layers": ["P00_CONFIGURATION", "P02_LOCAL_JETS", "P03_FOUNDED_CONSTRAINTS", "P03G_GLOBAL_ASSEMBLY", "CURRENT_COMPLETION_TYPE_SPACE", "FUTURE_DYNAMICAL_SOLUTIONS"],
        "axes": [r["axis"] for r in axis_rows],
        "edges": [
            ["P00_CONFIGURATION", "P02_LOCAL_JETS", "local jet projection"],
            ["P02_LOCAL_JETS", "P03_FOUNDED_CONSTRAINTS", "cited premise action"],
            ["P03_FOUNDED_CONSTRAINTS", "P03G_GLOBAL_ASSEMBLY", "cover and cocycle extension"],
            ["P03G_GLOBAL_ASSEMBLY", "CURRENT_COMPLETION_TYPE_SPACE", "completion family expansion"],
            ["CURRENT_COMPLETION_TYPE_SPACE", "FUTURE_DYNAMICAL_SOLUTIONS", "requires complete selected operator and variation domain"],
        ],
        "forbidden_edges": [
            "named desired boundary -> atlas acceptance",
            "conditional action -> configuration ranking",
            "regular witness -> exhaustive global topology",
            "time dependence -> physical evolution",
            "configuration atlas -> P06 readiness",
        ],
        "classification": CLASSIFICATION,
    }
    (HERE / "ATLAS_GRAPH.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    table_counts = {
        "p02_carryforward": len(carry_rows), "completion_axes": len(axis_rows), "phi_zero_families": len(phi_rows),
        "finite_germs": len(germ_rows), "metric_regularity": len(regularity), "jet_matching": len(matching),
        "causal_time_live": len(causal), "field_bundle": len(field), "angular_mixed": len(angular),
        "global_incidence": len(global_rows), "quotient_action": len(quotient), "variation": len(variation),
        "global_outputs": len(outputs), "relations": len(relations), "field_lane_pairs": len(field_lanes),
        "completeness": len(completeness), "anti_imposition": len(anti),
    }
    remainder_rows = [phi_rows[-1], regularity[-1], matching[-1], causal[-1], field[-1], angular[-1], global_rows[-1], quotient[-1], variation[-1], outputs[-1]]
    check("all_required_remainders", all("OTHER_UNENUMERATED_REQUIRED" in " ".join(map(str, row)) for row in remainder_rows))
    result = {
        "schema": "udt-finite-cell-completion-atlas-1.0",
        "status": "PASS",
        "classification": CLASSIFICATION,
        "maximum_conclusion": MAXIMUM,
        "checks": len(checks),
        "sources": len(SOURCES),
        "parent_p02_strata": 89,
        "parent_p03_accounted": 89,
        "parent_p03g_axes": 12,
        "parent_p03g_uncounted": 15,
        "table_counts": table_counts,
        "finite_exhaustiveness_claim": False,
        "branch_ranking_used": False,
        "dynamics_loaded": False,
        "solutions_run": 0,
        "P06_ready_pairs": 0,
        "gpu_used": False,
        "evidence_grade": "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW",
        "checks_passed": checks,
    }
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_FINITE_CELL_COMPLETION_ATLAS=PASS",
        f"checks={len(checks)}",
        f"classification={CLASSIFICATION}",
        "P02_marginal_strata=89/89",
        "P03_accounted_strata=89/89",
        "P03G_axes=12 uncounted_moduli=15",
        "completion_axes=10",
        f"phi_zero_families={len(phi_rows)} including_unbounded_remainder=YES",
        f"angular_mixed_families={len(angular)} including_unbounded_remainder=YES",
        f"global_incidence_families={len(global_rows)} including_unbounded_remainder=YES",
        f"field_lane_pairs={len(field_lanes)}/{len(field_lanes)} P06_ready=0",
        "branch_ranking=NO",
        "dynamics=NO solutions=0 gpu=NO",
        f"maximum_conclusion={MAXIMUM}",
    ]
    (HERE / "ATLAS_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()
