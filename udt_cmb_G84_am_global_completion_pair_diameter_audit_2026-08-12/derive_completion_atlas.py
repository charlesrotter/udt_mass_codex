#!/usr/bin/env python3
"""Derive the preregistered G84 AM spatial/global-completion atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROFILE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, records: list[dict[str, object]]) -> None:
    assert records
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def verify_sources() -> int:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 14
    for row in manifest:
        target = ROOT / row["path"]
        assert target.is_file() and digest(target) == row["sha256"], target
    return len(manifest)


def scalar_curvature(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Expr:
    size = len(coordinates)
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(sum(
            inverse[i, ell] * (
                sp.diff(metric[ell, k], coordinates[j])
                + sp.diff(metric[ell, j], coordinates[k])
                - sp.diff(metric[j, k], coordinates[ell])
            ) / 2
            for ell in range(size)
        ))
        for k in range(size)] for j in range(size)] for i in range(size)]
    ricci = sp.zeros(size)
    for i in range(size):
        for j in range(size):
            ricci[i, j] = sp.simplify(sum(
                sp.diff(gamma[k][i][j], coordinates[k])
                - sp.diff(gamma[k][i][k], coordinates[j])
                + sum(
                    gamma[k][k][ell] * gamma[ell][i][j]
                    - gamma[k][j][ell] * gamma[ell][i][k]
                    for ell in range(size)
                )
                for k in range(size)
            ))
    return sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(size) for j in range(size)))


def exact_geometry() -> dict[str, object]:
    chi, theta, tau, R = sp.symbols("chi theta tau R", real=True, positive=True)
    separation = sp.symbols("separation", real=True, nonnegative=True)
    x = 2 * sp.sin(chi)
    A = 1 - x**2 / 4
    radial = sp.simplify(sp.diff(x, chi)**2 / A)
    assert sp.trigsimp(A - sp.cos(chi)**2) == 0
    assert sp.trigsimp(radial - 4) == 0
    spatial = sp.diag(4, 4 * sp.sin(chi)**2, 4 * sp.sin(chi)**2 * sp.sin(theta)**2)
    scalar = scalar_curvature(spatial, (chi, theta, sp.symbols("psi", real=True)))
    assert sp.trigsimp(scalar - sp.Rational(3, 2)) == 0

    X0 = 2 * sp.cos(chi) * sp.sinh(tau / 2)
    X4 = 2 * sp.cos(chi) * sp.cosh(tau / 2)
    radius_sq = 4 * sp.sin(chi)**2
    assert sp.trigsimp(-X0**2 + X4**2 + radius_sq - 4) == 0
    static_normal = sp.simplify(-sp.diff(X0, tau)**2 + sp.diff(X4, tau)**2)
    static_radial = sp.simplify(
        -sp.diff(X0, chi)**2 + sp.diff(X4, chi)**2 + sp.diff(2 * sp.sin(chi), chi)**2
    )
    assert sp.trigsimp(static_normal + sp.cos(chi)**2) == 0
    assert sp.trigsimp(static_radial - 4) == 0
    recentered_A = sp.cos(separation / (2 * R))**2
    recentered_phi = -sp.log(sp.cos(separation / (2 * R)))
    assert sp.simplify(sp.exp(-2 * recentered_phi) - recentered_A) == 0
    assert sp.limit(recentered_phi, separation, sp.pi * R, dir="-") == sp.oo
    assert sp.limit(recentered_A, separation, sp.pi * R, dir="-") == 0
    return {
        "coordinate_map": "x=2*sin(chi)",
        "spatial_metric_over_R2": "4*(dchi^2+sin(chi)^2*dOmega2)",
        "spatial_radius_over_R": "2",
        "spatial_sectional_curvature_times_R2": "1/4",
        "spatial_scalar_curvature_times_R2": str(scalar),
        "spatial_injectivity_radius_over_R": "2*pi",
        "spatial_diameter_over_R": "2*pi",
        "equator_x": "2",
        "north_pole_to_equator_over_R": "pi",
        "x_map_multiplicity": "TWO_TO_ONE_OFF_EQUATOR_ON_DOUBLED_S3",
        "zero_mix_embedding": "-X0^2+X1^2+X2^2+X3^2+X4^2=4",
        "zero_mix_static_regions": "TWO_STATIC_PATCHES_PLUS_UNCOVERED_TIMELIVE_REGIONS",
        "zero_mix_recentered_static_limit_over_R": "pi",
        "zero_mix_recentered_depth_law": "phi(s)=-log(cos(s/(2R)))",
        "zero_mix_recentered_c_eff_law": "c_eff(s)/c_E=cos(s/(2R))^2",
        "zero_mix_candidate_Xmax": "pi*R",
        "zero_mix_frame_scope": "GLOBAL_ISOMETRY_ORBIT_OF_CENTRAL_GEODESIC_OBSERVERS",
    }


def profile_atlas() -> list[dict[str, object]]:
    s = sp.symbols("s", real=True)
    profiles = [row for row in rows(PROFILE_PATH) if row["lapse_name"] == "AM"]
    assert len(profiles) == len({row["profile_id"] for row in profiles}) == 197
    output = []
    for row in profiles:
        q = sp.Poly(sp.sympify(row["q_of_s"], locals={"s": s}), s).as_expr()
        q4 = sp.simplify(q.subs(s, 4))
        h_equator = sp.simplify(4 * q4)
        vanishes = bool(q4 == 0)
        if row["shape_id"] == "ZERO":
            extension_class = "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS"
        elif vanishes:
            extension_class = "MIXING_VANISHES_AT_BIFURCATION__FURTHER_EXTENSION_AUDIT_REQUIRED"
        else:
            extension_class = "NONZERO_BIFURCATION_MIXING__STANDARD_SMOOTH_SYMMETRY_EXTENSION_OBSTRUCTED"
        output.append({
            "profile_id": row["profile_id"],
            "shape_id": row["shape_id"],
            "amplitude": row["amplitude"],
            "q_at_s_4_exact": sp.sstr(q4),
            "h_at_x_2_exact": sp.sstr(h_equator),
            "mixing_vanishes_at_candidate_surface": str(vanishes).lower(),
            "extension_class": extension_class,
            "physical_status": "CONTROL_CLASSIFICATION_NOT_SELECTED_PHYSICS",
        })
    return output


def branch_atlas() -> list[dict[str, object]]:
    return [
        {
            "object": "G75_REGISTERED_CELL",
            "domain": "0<=x<=1",
            "status": "INHERITED_CONTROL_REGULAR",
            "owns": "bounded stationary control family",
            "does_not_own": "continuation; global completion; X_max",
        },
        {
            "object": "AM_NORTH_STATIC_BRANCH",
            "domain": "0<=chi<pi/2",
            "status": "FREE_AND_EXPLORED_CONTINUATION",
            "owns": "one stationary chart branch",
            "does_not_own": "antipode; global pair distance; physical endpoint",
        },
        {
            "object": "DOUBLED_SPATIAL_S3",
            "domain": "0<=chi<=pi",
            "status": "DERIVED_INTRINSIC_SPATIAL_COMPLETION_CANDIDATE",
            "owns": "round spatial metric radius 2R and diameter 2piR",
            "does_not_own": "full Lorentzian history; clock-depth law; physical X_max",
        },
        {
            "object": "ZERO_MIXING_LORENTZ_EXTENSION",
            "domain": "complete constant-curvature hyperboloid",
            "status": "DERIVED_FOR_ZERO_MIXING_CONTROL",
            "owns": "smooth extension and frame-shared piR static limit on the central-geodesic isometry orbit",
            "does_not_own": "physical profile; arbitrary observers; mixed orchestra; numerical R",
        },
        {
            "object": "NONZERO_MIXING_STANDARD_EXTENSION",
            "domain": "196 continued AM controls",
            "status": "OBSTRUCTED_WITHIN_SMOOTH_SYMMETRY_PRESERVING_BIFURCATE_CLASS",
            "owns": "local fixed-point obstruction from nonzero h(2)",
            "does_not_own": "generic time-live completion no-go",
        },
    ]


def pair_counterexamples() -> list[dict[str, object]]:
    return [
        {
            "case": "NORTH_POLE_TO_EQUATOR",
            "spatial_distance_over_R": "pi",
            "stationary_depth": "+infinity_limit",
            "meaning": "infinite stationary depth occurs at half the S3 diameter",
        },
        {
            "case": "SAME_LATITUDE_NORTH_PATCH_GAMMA_RANGE",
            "spatial_distance_over_R": "0_to_pi",
            "stationary_depth": "0",
            "meaning": "at chi=pi/4, valid future-directed stationary pairs share phi while d/R=2*acos((1+cos(gamma))/2) varies",
        },
        {
            "case": "EQUATOR_PAIR_VARIABLE_ANGLE",
            "spatial_distance_over_R": "0_to_2*pi",
            "stationary_depth": "stationary_observers_not_timelike",
            "meaning": "one lapse-zero surface contains many pair distances",
        },
    ]


def recenter_atlas() -> list[dict[str, object]]:
    receiver_values = (sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Integer(1))
    output = []
    for receiver in receiver_values:
        old_limit = sp.simplify(sp.pi - 2 * sp.asin(receiver / 2))
        output.append({
            "fixed_chart_receiver_x": sp.sstr(receiver),
            "fixed_chart_distance_to_original_horizon_over_R": sp.sstr(old_limit),
            "recentered_own_horizon_distance_over_R": "pi",
            "recentered_candidate_Xmax_over_R": "pi",
            "recenter_operation": "GLOBAL_ZERO_MIXING_ISOMETRY_TO_NEW_STATIC_PATCH",
            "status": "DERIVED_CONDITIONAL_ZERO_MIXING_GEODESIC_OBSERVER_CLASS",
        })
    return output


def main() -> None:
    sources = verify_sources()
    geometry = exact_geometry()
    profiles = profile_atlas()
    branches = branch_atlas()
    counterexamples = pair_counterexamples()
    recentered = recenter_atlas()
    write_tsv(HERE / "PROFILE_COMPLETION_ATLAS.tsv", profiles)
    write_tsv(HERE / "COMPLETION_BRANCH_ATLAS.tsv", branches)
    write_tsv(HERE / "PAIR_DISTANCE_COUNTEREXAMPLES.tsv", counterexamples)
    write_tsv(HERE / "RECENTERED_OBSERVER_LIMIT_ATLAS.tsv", recentered)
    counts = Counter(row["extension_class"] for row in profiles)
    assert counts == {
        "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS": 1,
        "NONZERO_BIFURCATION_MIXING__STANDARD_SMOOTH_SYMMETRY_EXTENSION_OBSTRUCTED": 196,
    }
    result = {
        "schema": "udt-cmb-g84-am-completion-atlas-v1",
        "status": "PASS",
        "landing": "ZERO_MIXING_BRANCH_HAS_CONDITIONAL_FRAME_SHARED_RECENTERED_ASYMPTOTE__NONZERO_MIXED_COMPLETION_OPEN",
        "source_manifest_rows": sources,
        "geometry": geometry,
        "profile_rows": len(profiles),
        "extension_class_counts": dict(sorted(counts.items())),
        "pair_counterexamples": len(counterexamples),
        "recentered_receiver_rows": len(recentered),
        "zero_mix_recentered_candidate_Xmax_over_R": "pi",
        "zero_mix_recentered_depth_law": "phi(s)=-log(cos(s/(2R)))",
        "zero_mix_recentered_c_eff_law": "c_eff(s)/c_E=cos(s/(2R))^2",
        "zero_mix_frame_sharing_scope": "GLOBAL_ISOMETRY_ORBIT_OF_CENTRAL_GEODESIC_OBSERVERS",
        "physical_X_max_status": "OPEN",
        "physical_scale_R_status": "OPEN",
        "time_live_completion_status": "REQUIRED_NEXT_FOR_NONZERO_MIXING",
        "maximum_conclusion": "BOUNDED_AM_SPATIAL_COMPLETION_AND_STATIONARY_DEPTH_COMPATIBILITY_ATLAS",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
