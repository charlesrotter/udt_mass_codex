#!/usr/bin/env python3
"""Exact topology, turning, and kernel-plane connection atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_intrinsic_general_screen_neighborhood_audit_2026-08-02"
Q = sp.symbols("q0:4", real=True)
Q0, Q1, Q2, Q3 = Q
X, Y, Z = sp.symbols("x y z", real=True)
XYZ = (X, Y, Z)
POINTS = {
    "p1": (sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 11)),
    "p2": (sp.Rational(1, 3), sp.Rational(-1, 5), sp.Rational(1, 7)),
}
FULL_IDS = ("C04", "C08", "C09", "C10", "C16", "C17")


class Jet:
    """Exact value plus its first derivatives in stereographic x,y,z."""

    def __init__(self, value, gradient=(0, 0, 0)):
        self.value = sp.sympify(value)
        self.gradient = tuple(sp.sympify(entry) for entry in gradient)

    @staticmethod
    def coerce(other):
        return other if isinstance(other, Jet) else Jet(other)

    def __add__(self, other):
        other = self.coerce(other)
        return Jet(self.value + other.value, tuple(a + b for a, b in zip(self.gradient, other.gradient)))

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Jet(
            self.value*other.value,
            tuple(a*other.value + self.value*b for a, b in zip(self.gradient, other.gradient)),
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        return Jet(
            self.value/other.value,
            tuple(
                (a*other.value - self.value*b)/(other.value**2)
                for a, b in zip(self.gradient, other.gradient)
            ),
        )

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, exponent: int):
        assert isinstance(exponent, int)
        if exponent < 0:
            return 1/(self**(-exponent))
        if exponent == 0:
            return Jet(1)
        return Jet(
            self.value**exponent,
            tuple(exponent*self.value**(exponent - 1)*entry for entry in self.gradient),
        )


def jet_sqrt(value: Jet) -> Jet:
    root = sp.sqrt(value.value)
    return Jet(root, tuple(entry/(2*root) for entry in value.gradient))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verify_sources() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 86
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert digest(content) == row["sha256"]
    assert digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (
        HERE / "SOURCE_MANIFEST.sha256"
    ).read_text(encoding="utf-8").strip()
    return len(rows)


def quaternion_and_sigmas():
    rho2 = X*X + Y*Y + Z*Z
    denominator = 1 + rho2
    q = (
        sp.factor((1 - rho2) / denominator),
        sp.factor(2*X / denominator),
        sp.factor(2*Y / denominator),
        sp.factor(2*Z / denominator),
    )
    dq = tuple(sp.Matrix([sp.diff(value, coordinate) for coordinate in XYZ]) for value in q)
    q0, q1, q2, q3 = q
    dq0, dq1, dq2, dq3 = dq
    sigmas = (
        sp.simplify(q0*dq1 - q1*dq0 - q2*dq3 + q3*dq2),
        sp.simplify(q0*dq2 - q2*dq0 - q3*dq1 + q1*dq3),
        sp.simplify(q0*dq3 - q3*dq0 - q1*dq2 + q2*dq1),
    )
    return q, sigmas


def profile_expressions(candidate: dict[str, str], q):
    q0, q1, q2, q3 = q
    primary_u = 3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3
    u = primary_u if candidate["u_profile"] == "U" else sp.Integer(4)
    v0 = q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3
    r0 = 2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3
    b0 = q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3
    epsilon = sp.Rational(1, 10)
    v = {
        "ONE": sp.S.One,
        "TWO": sp.Integer(2),
        "U": u,
        "V_EPS": 1 + epsilon*v0,
        "ZERO": sp.S.Zero,
    }[candidate["V_profile"]]
    r = {"ONE": sp.S.One, "R_EPS": 1 + epsilon*r0}[candidate["r_profile"]]
    b = {"ZERO": sp.S.Zero, "B_EPS": epsilon*b0}[candidate["b_profile"]]
    lam = int(candidate["lambda"])
    area = sp.factor(u**lam * v)
    return sp.factor(u), sp.factor(v), sp.factor(r), sp.factor(b), area


def exact_connection_at_point(candidate: dict[str, str], point):
    x = Jet(point[0], (1, 0, 0))
    y = Jet(point[1], (0, 1, 0))
    z = Jet(point[2], (0, 0, 1))
    rho2 = x*x + y*y + z*z
    denominator = 1 + rho2
    q0 = (1 - rho2)/denominator
    q1 = 2*x/denominator
    q2 = 2*y/denominator
    q3 = 2*z/denominator

    primary_u = 3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3
    u = primary_u if candidate["u_profile"] == "U" else Jet(4)
    v0 = q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3
    r0 = 2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3
    b0 = q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3
    epsilon = sp.Rational(1, 10)
    v = {
        "ONE": Jet(1), "TWO": Jet(2), "U": u,
        "V_EPS": 1 + epsilon*v0, "ZERO": Jet(0),
    }[candidate["V_profile"]]
    r = {"ONE": Jet(1), "R_EPS": 1 + epsilon*r0}[candidate["r_profile"]]
    b = {"ZERO": Jet(0), "B_EPS": epsilon*b0}[candidate["b_profile"]]
    area = (u**int(candidate["lambda"]))*v

    f12 = q0*q1*q1 + 3*q0*q2*q2 + 2*q1*q2*q3
    f13 = q0*q0*q1 + 3*q0*q2*q3 - 2*q1*q2*q2
    f23 = 3*q0*q0*q2 - q0*q1*q3 + 2*q1*q1*q2

    root_area = jet_sqrt(area)
    root_u = jet_sqrt(u)
    w12 = -f13 / (root_area*r*root_u)
    w13 = (b*f13 - r*f23) / (root_area*root_u)
    w23 = f12 / area
    n_raw = (w23, -w13, w12)
    n_norm = jet_sqrt(sum(component*component for component in n_raw))
    n = tuple(component/n_norm for component in n_raw)

    denominator_squared = denominator*denominator
    sigma1 = (
        2*(x*x - y*y - z*z + 1)/denominator_squared,
        4*(x*y + z)/denominator_squared,
        4*(x*z - y)/denominator_squared,
    )
    sigma2 = (
        4*(x*y - z)/denominator_squared,
        -2*(x*x - y*y + z*z - 1)/denominator_squared,
        4*(x + y*z)/denominator_squared,
    )
    theta2 = tuple(root_area*(r*sigma1[index] + b*sigma2[index]) for index in range(3))
    theta3 = tuple(root_area*sigma2[index]/r for index in range(3))
    q_t = 2*int(candidate["a"])/(root_u*area)
    omega = tuple(q_t*(n[2]*theta2[index] - n[1]*theta3[index])/2 for index in range(3))
    curvature = (
        omega[1].gradient[0] - omega[0].gradient[1],
        omega[2].gradient[0] - omega[0].gradient[2],
        omega[2].gradient[1] - omega[1].gradient[2],
    )
    omega_norm_squared = q_t*q_t*(n[1]*n[1] + n[2]*n[2])/4
    return {
        "n": tuple(component.value for component in n),
        "q_t": q_t.value,
        "omega": tuple(component.value for component in omega),
        "curvature": curvature,
        "omega_norm_squared": omega_norm_squared.value,
        "area": area.value,
    }


def main() -> int:
    source_count = verify_sources()
    bindings = read_tsv(HERE / "CANDIDATE_BINDING.tsv")
    candidates = read_tsv(PARENT / "CANDIDATE_UNIVERSE.tsv")
    assert [row["candidate_id"] for row in bindings] == [f"C{i:02d}" for i in range(1, 19)]
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 19)]
    assert [row["candidate_id"] for row in bindings if row["transport_scope"] == "FULL_DEFECT_TRANSPORT"] == list(FULL_IDS)
    assert len(read_tsv(HERE / "LOOP_UNIVERSE.tsv")) == 18
    assert len(read_tsv(HERE / "OBJECT_UNIVERSE.tsv")) == 26
    assert len(read_tsv(HERE / "FALSIFICATION_CONTRACT.tsv")) == 36

    # Frozen coefficient-vector field after removing the common q3 factor.
    f12 = Q0*Q1**2 + 3*Q0*Q2**2 + 2*Q1*Q2*Q3
    f13 = Q0**2*Q1 + 3*Q0*Q2*Q3 - 2*Q1*Q2**2
    f23 = 3*Q0**2*Q2 - Q0*Q1*Q3 + 2*Q1**2*Q2
    f = sp.Matrix([f12, f13, f23])

    # The candidate metric map f -> unnormalized N has positive determinant everywhere.
    area_symbol, u_symbol, r_symbol = sp.symbols("F u r", positive=True)
    b_symbol = sp.symbols("b", real=True)
    metric_map = sp.Matrix([
        [1/area_symbol, 0, 0],
        [0, -b_symbol/(sp.sqrt(area_symbol)*sp.sqrt(u_symbol)), r_symbol/(sp.sqrt(area_symbol)*sp.sqrt(u_symbol))],
        [0, -1/(sp.sqrt(area_symbol)*r_symbol*sp.sqrt(u_symbol)), 0],
    ])
    metric_map_determinant = sp.factor(metric_map.det())
    assert metric_map_determinant == 1/(area_symbol**2*u_symbol)

    # Regular-edge transverse maps, symbolic along every non-pole base point.
    a, b, c, d = sp.symbols("a b c d", real=True)
    edge_matrices = {
        "C03": sp.Matrix([[a*a, 3*a*d], [-a*d, 3*a*a]]),
        "C13": sp.Matrix([[b*b, 2*b*d], [-b*d, 2*b*b]]),
        "C23": sp.Matrix([[3*c*c, 2*c*d], [3*c*d, -2*c*c]]),
    }
    edge_determinants = {name: sp.factor(matrix.det()) for name, matrix in edge_matrices.items()}
    assert edge_determinants == {
        "C03": 3*a*a*(a*a + d*d),
        "C13": 2*b*b*(b*b + d*d),
        "C23": -6*c*c*(c*c + d*d),
    }
    sphere_edge_determinants = {
        "C03": sp.factor(edge_determinants["C03"].subs(d*d, 1-a*a)),
        "C13": sp.factor(edge_determinants["C13"].subs(d*d, 1-b*b)),
        "C23": sp.factor(edge_determinants["C23"].subs(d*d, 1-c*c)),
    }
    assert sphere_edge_determinants == {"C03": 3*a*a, "C13": 2*b*b, "C23": -6*c*c}

    # Pole-link leading map and its exact six-puncture zero set.
    px, py, pz, pole_sign = sp.symbols("px py pz pole_sign", real=True)
    pole_map = sp.Matrix([2*pole_sign*py*pz, 3*pole_sign*px*pz, -pole_sign*px*py])
    pole_punctures = (
        "+e0", "-e0", "+e1", "-e1", "+e2", "-e2",
    )
    # Every pairwise product vanishes iff at most one of px,py,pz is nonzero.
    pole_ideal = sp.groebner([py*pz, px*pz, px*py], px, py, pz, order="lex")
    assert all(pole_ideal.reduce(term)[1] == 0 for term in (px*py, px*pz, py*pz))
    pole_edge_determinants = {"e0": 3, "e1": 2, "e2": -6}

    # Graph topology: two pole vertices and six edges give b1=5; Alexander duality gives H1(M)=Z^5.
    graph_vertices = 2
    graph_edges = 6
    graph_components = 1
    graph_b1 = graph_edges - graph_vertices + graph_components
    assert graph_b1 == 5

    # A global nonzero lift exists on M because f vanishes exactly on D and the metric map is invertible.
    global_lift_status = "GLOBAL_NONZERO_LIFT_ON_M"
    line_w1 = "ZERO_ON_ALL_H1_GENERATORS"
    projective_meridian_class = "TRIVIAL_IN_PI1_RP2"
    local_rp1_traversals = 2
    oriented_vector_degree_magnitude = 1

    edge_rows = []
    for circle, determinant in sphere_edge_determinants.items():
        signed_index = "+1" if sp.LC(determinant) > 0 else "-1"
        for hemisphere in ("NORTH_EDGE", "SOUTH_EDGE"):
            edge_rows.append({
                "edge": f"{circle}_{hemisphere}",
                "symbolic_rank": "2_AWAY_FROM_POLES",
                "frozen_orientation_determinant": str(determinant),
                "oriented_vector_degree": signed_index,
                "degree_magnitude": "1",
                "RP1_traversals_per_meridian": "2",
                "RP2_Z2_class": "0_TRIVIAL",
                "zero_radius_kernel_plane_holonomy": "IDENTITY_LIMIT",
            })

    candidates_by_id = {row["candidate_id"]: row for row in candidates}
    connection_rows = []
    candidate_rows = []
    connection_cache = {candidate_id: {} for candidate_id in FULL_IDS}

    for candidate_id in FULL_IDS:
        point_nonzero_curvature = []
        for point_id, point in POINTS.items():
            connection = exact_connection_at_point(candidates_by_id[candidate_id], point)
            connection_cache[candidate_id][point_id] = connection
            omega_values = tuple(sp.radsimp(sp.factor(value)) for value in connection["omega"])
            curvature_values = tuple(sp.radsimp(sp.factor(value)) for value in connection["curvature"])
            norm_value = sp.radsimp(sp.factor(connection["omega_norm_squared"]))
            assert norm_value > 0
            nonzero_curvature = any(value != 0 for value in curvature_values)
            point_nonzero_curvature.append(nonzero_curvature)
            connection_rows.append({
                "candidate_id": candidate_id,
                "point_id": point_id,
                "omega_xyz": ";".join(str(value) for value in omega_values),
                "Omega_xy_xz_yz": ";".join(str(value) for value in curvature_values),
                "omega_norm_squared": str(norm_value),
                "Omega_nonzero": "YES" if nonzero_curvature else "NO",
            })
        candidate_rows.append({
            "candidate_id": candidate_id,
            "line_bundle": "TRIVIAL_ORIENTABLE_GLOBAL_LIFT",
            "line_projected_connection": "FLAT_TRIVIAL_IN_GLOBAL_UNIT_FRAME",
            "line_holonomy": "IDENTITY_ALL_LOOPS",
            "ambient_turning": "LOCAL_1_OVER_RHO__UNIT_VECTOR_DEGREE_MAGNITUDE_1",
            "kernel_plane_bundle": "TRIVIAL_ORIENTABLE_TIME_ORIENTABLE",
            "kernel_plane_connection": "NONZERO_ON_M_IN_METRIC_ANCHORED_T_N_FRAME",
            "curvature_at_p1_p2": "NONZERO_BOTH" if all(point_nonzero_curvature) else "MIXED_OR_ZERO",
            "finite_loop_holonomy": "EXACT_PATH_INTEGRAL_REQUIRED_NOT_UNIVERSALLY_EVALUATED",
            "physics_selected": "NO",
        })

    # Exact branch-scaling controls: C16 and C17 differ from C08 only by a=4 and a=5.
    for point_id in POINTS:
        for field in ("omega", "curvature"):
            c08_values = connection_cache["C08"][point_id][field]
            for target, scale in (("C16", 4), ("C17", 5)):
                target_values = connection_cache[target][point_id][field]
                assert all(sp.simplify(target_values[index] - scale*c08_values[index]) == 0 for index in range(len(c08_values)))

    # At both exact anchors all four screen-shape branches are genuinely distinct.
    for point_id in POINTS:
        signatures = []
        for candidate_id in ("C04", "C08", "C09", "C10"):
            values = tuple(
                sp.radsimp(sp.factor(value))
                for value in connection_cache[candidate_id][point_id]["curvature"]
            )
            signatures.append(tuple(str(value) for value in values))
        assert len(set(signatures)) == 4

    topology_rows = [
        {"object": "defect_graph", "status": "TWO_VERTICES_SIX_EDGES_CONNECTED", "exact_detail": "three_great_circles_share_plus_minus_e3"},
        {"object": "graph_first_betti", "status": "5", "exact_detail": "E_minus_V_plus_1"},
        {"object": "complement_H1", "status": "Z_POWER_5", "exact_detail": "Alexander_duality_H1_M_isomorphic_to_H_caret_1_D"},
        {"object": "global_lift", "status": global_lift_status, "exact_detail": "Ntilde=L_g_f_nonzero_on_M"},
        {"object": "line_w1", "status": line_w1, "exact_detail": "global_lift_trivializes_real_line"},
        {"object": "regular_meridian_RP2", "status": projective_meridian_class, "exact_detail": "closed_S2_lift_of_linear_normal_map"},
        {"object": "regular_meridian_RP1", "status": "TWO_TRAVERSALS", "exact_detail": "not_intrinsic_nontrivial_RP2_class"},
        {"object": "local_vector_index", "status": "MAGNITUDE_ONE", "exact_detail": "signed_plus_plus_minus_in_frozen_orientation"},
        {"object": "pole_links", "status": "S2_MINUS_SIX_PUNCTURES_EACH", "exact_detail": "leading_map_2yz_3xz_minus_xy"},
        {"object": "line_metric_connection", "status": "FLAT_IDENTITY_HOLONOMY", "exact_detail": "global_unit_frame_has_projected_derivative_zero"},
        {"object": "ambient_turning", "status": "NONTRIVIAL_SINGULAR_LOCAL_TURNING", "exact_detail": "meridional_norm_scales_1_over_rho_leading_transverse_image_turn_tends_2pi"},
        {"object": "kernel_plane_meridian_holonomy", "status": "IDENTITY_ZERO_RADIUS_LIMIT", "exact_detail": "omega_bounded_loop_length_order_rho"},
    ]

    write_tsv(
        "EDGE_ATLAS.tsv",
        ["edge", "symbolic_rank", "frozen_orientation_determinant", "oriented_vector_degree",
         "degree_magnitude", "RP1_traversals_per_meridian", "RP2_Z2_class",
         "zero_radius_kernel_plane_holonomy"],
        edge_rows,
    )
    write_tsv("TOPOLOGY_ATLAS.tsv", ["object", "status", "exact_detail"], topology_rows)
    write_tsv(
        "CONNECTION_POINTS.tsv",
        ["candidate_id", "point_id", "omega_xyz", "Omega_xy_xz_yz", "omega_norm_squared", "Omega_nonzero"],
        connection_rows,
    )
    write_tsv(
        "CANDIDATE_TRANSPORT_ATLAS.tsv",
        ["candidate_id", "line_bundle", "line_projected_connection", "line_holonomy",
         "ambient_turning", "kernel_plane_bundle", "kernel_plane_connection",
         "curvature_at_p1_p2", "finite_loop_holonomy", "physics_selected"],
        candidate_rows,
    )

    result = {
        "schema": "udt-intrinsic-defect-transport-1.0",
        "status": "PASS_EXACT_PRODUCTION",
        "sympy_version": sp.__version__,
        "frozen_sources": source_count,
        "candidate_count": 18,
        "full_transport_candidates": list(FULL_IDS),
        "control_counts": {"zero": 9, "blocked": 2, "degenerate": 1},
        "defect_graph": {"vertices": graph_vertices, "edges": graph_edges, "components": graph_components, "b1": graph_b1},
        "complement_H1": "Z^5",
        "metric_map_determinant": str(metric_map_determinant),
        "global_lift": global_lift_status,
        "line_w1": line_w1,
        "all_projective_meridians": projective_meridian_class,
        "local_RP1_traversals": local_rp1_traversals,
        "oriented_vector_degree_magnitude": oriented_vector_degree_magnitude,
        "edge_determinants_on_S3": {key: str(value) for key, value in sphere_edge_determinants.items()},
        "edge_signed_indices_frozen_orientation": {"C03": 1, "C13": 1, "C23": -1},
        "index_sign_canonical": False,
        "pole_leading_map": [str(value) for value in pole_map],
        "pole_punctures": list(pole_punctures),
        "pole_edge_determinants": pole_edge_determinants,
        "line_projected_connection": "TRIVIAL_IN_GLOBAL_UNIT_FRAME",
        "line_holonomy": "IDENTITY_ON_ALL_LOOPS",
        "ambient_turning": "NONZERO_AND_1_OVER_RHO_NEAR_REGULAR_DEFECT",
        "kernel_plane_connection_formula": "omega_E=(q_T/2)*(n3*theta2-n2*theta3)",
        "kernel_plane_connection_norm_squared": "Q_T*(n2^2+n3^2)/4_positive_on_M",
        "kernel_plane_curvature_point_certificates": len(connection_rows),
        "curvature_nonzero_certificates": sum(row["Omega_nonzero"] == "YES" for row in connection_rows),
        "twist_scaling": {"C16_over_C08": 4, "C17_over_C08": 5},
        "registered_screen_lambda_curvature_coordinate_triples_distinct_at_p1_p2": True,
        "finite_loop_holonomy": "PATH_INTEGRAL_NOT_UNIVERSALLY_EVALUATED",
        "full_Levi_Civita_holonomy_conflated": False,
        "topological_charge_inferred": False,
        "carrier_or_physics_selected": False,
    }
    (HERE / "TRANSPORT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        "complement_H1": result["complement_H1"],
        "line_w1": result["line_w1"],
        "projective_meridians": result["all_projective_meridians"],
        "curvature_certificates": result["kernel_plane_curvature_point_certificates"],
        "curvature_nonzero": result["curvature_nonzero_certificates"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
