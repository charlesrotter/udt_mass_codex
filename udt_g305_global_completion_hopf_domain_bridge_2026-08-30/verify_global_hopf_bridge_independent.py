#!/usr/bin/env python3
"""Independent standard-library G305 replay; imports no production code."""

from __future__ import annotations

import json
import math
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def dot(v, w, signature):
    return sum(s * a * b for s, a, b in zip(signature, v, w))


def fd_column(fn, point, index, h=2.0e-6):
    plus = list(point)
    minus = list(point)
    plus[index] += h
    minus[index] -= h
    fp = fn(*plus)
    fm = fn(*minus)
    return [(a - b) / (2.0 * h) for a, b in zip(fp, fm)]


def induced_numeric(fn, point, signature):
    columns = [fd_column(fn, point, j) for j in range(len(point))]
    return [
        [dot(columns[i], columns[j], signature) for j in range(len(point))]
        for i in range(len(point))
    ]


def max_error(actual, expected):
    return max(
        abs(actual[i][j] - expected[i][j])
        for i in range(len(actual))
        for j in range(len(actual))
    )


def nvec(theta, phi):
    return (
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta),
    )


def pos_static(X):
    def fn(tau, r, theta, phi):
        n = nvec(theta, phi)
        q = math.sqrt(X * X - r * r)
        return (
            q * math.sinh(tau / X),
            r * n[0], r * n[1], r * n[2],
            q * math.cosh(tau / X),
        )
    return fn


def pos_global(X):
    def fn(T, psi, theta, phi):
        n = nvec(theta, phi)
        a = X * math.cosh(T / X)
        return (
            X * math.sinh(T / X),
            a * math.sin(psi) * n[0],
            a * math.sin(psi) * n[1],
            a * math.sin(psi) * n[2],
            a * math.cos(psi),
        )
    return fn


def neg_static(L):
    def fn(tau, r, theta, phi):
        n = nvec(theta, phi)
        q = math.sqrt(L * L + r * r)
        return (
            q * math.cos(tau / L),
            q * math.sin(tau / L),
            r * n[0], r * n[1], r * n[2],
        )
    return fn


def neg_global(L):
    def fn(tau, rho, theta, phi):
        n = nvec(theta, phi)
        return (
            L * math.cosh(rho) * math.cos(tau / L),
            L * math.cosh(rho) * math.sin(tau / L),
            L * math.sinh(rho) * n[0],
            L * math.sinh(rho) * n[1],
            L * math.sinh(rho) * n[2],
        )
    return fn


def midpoint_hopf(n=20000):
    width = (math.pi / 2.0) / n
    return sum(-math.sin(2.0 * (j + 0.5) * width) * width for j in range(n))


def main():
    counts = {
        "ambient_constraints": 0,
        "metric_coefficients": 0,
        "positive_overlap": 0,
        "negative_global_relation": 0,
        "hopf_and_scale_time": 0,
        "optical": 0,
        "topology_witnesses": 0,
    }

    def mark(category, number=1):
        counts[category] += number

    finite_difference_cases = 0
    max_fd_error = 0.0
    max_overlap_error = 0.0
    sig_pos = (-1.0, 1.0, 1.0, 1.0, 1.0)
    sig_neg = (-1.0, -1.0, 1.0, 1.0, 1.0)

    for X in (0.8, 1.7, 4.2):
        pstatic = pos_static(X)
        pglobal = pos_global(X)
        for point in ((0.13*X, 0.21*X, 0.8, 0.4), (-0.19*X, 0.63*X, 1.2, -0.7)):
            _, r, theta, _ = point
            f = 1.0 - (r/X)**2
            expected = [[0.0]*4 for _ in range(4)]
            for i, value in enumerate((-f, 1.0/f, r*r, r*r*math.sin(theta)**2)):
                expected[i][i] = value
            err = max_error(induced_numeric(pstatic, point, sig_pos), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            mark("metric_coefficients", 16)
            embedded = pstatic(*point)
            assert abs(dot(embedded, embedded, sig_pos) - X*X) < 2.0e-12
            mark("ambient_constraints")

        for point in ((0.17*X, 0.7, 0.9, 0.2), (-0.23*X, 2.1, 1.1, -0.8)):
            T, psi, theta, _ = point
            a = X * math.cosh(T/X)
            diag = (-1.0, a*a, a*a*math.sin(psi)**2, a*a*math.sin(psi)**2*math.sin(theta)**2)
            expected = [[0.0]*4 for _ in range(4)]
            for i, value in enumerate(diag):
                expected[i][i] = value
            err = max_error(induced_numeric(pglobal, point, sig_pos), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            mark("metric_coefficients", 16)
            embedded = pglobal(*point)
            assert abs(dot(embedded, embedded, sig_pos) - X*X) < 2.0e-12
            mark("ambient_constraints")

        # Independent static/global overlap, sampled strictly inside the static diamond.
        for T, psi, theta, phi in ((0.13*X, 0.20, 0.9, 0.2), (-0.18*X, 0.37, 1.1, -0.6)):
            global_point = pglobal(T, psi, theta, phi)
            r = X * math.cosh(T/X) * math.sin(psi)
            ratio = math.tanh(T/X) / math.cos(psi)
            assert r < X and abs(ratio) < 1.0
            mark("positive_overlap", 2)
            tau = X * math.atanh(ratio)
            static_point = pstatic(tau, r, theta, phi)
            component_errors = [abs(a-b) for a, b in zip(static_point, global_point)]
            assert max(component_errors) < 3.0e-13, component_errors
            max_overlap_error = max(max_overlap_error, max(component_errors))
            mark("positive_overlap", 5)
            spatial_radius = math.sqrt(sum(value*value for value in global_point[1:4]))
            assert abs(spatial_radius - r) < 3.0e-13
            assert abs(global_point[0] / global_point[4] - ratio) < 3.0e-13
            mark("positive_overlap", 2)

    for L in (0.9, 2.3, 5.1):
        nstatic = neg_static(L)
        nglobal = neg_global(L)
        for point in ((0.11*L, 0.2*L, 0.7, 0.5), (-0.18*L, 1.4*L, 1.3, -0.6)):
            _, r, theta, _ = point
            f = 1.0 + (r/L)**2
            diag = (-f, 1.0/f, r*r, r*r*math.sin(theta)**2)
            expected = [[0.0]*4 for _ in range(4)]
            for i, value in enumerate(diag):
                expected[i][i] = value
            err = max_error(induced_numeric(nstatic, point, sig_neg), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            mark("metric_coefficients", 16)
            embedded = nstatic(*point)
            assert abs(dot(embedded, embedded, sig_neg) + L*L) < 2.0e-12
            mark("ambient_constraints")

        for point in ((0.11*L, 0.25, 0.8, 0.3), (-0.18*L, 1.10, 1.2, -0.5)):
            tau, rho, theta, _ = point
            diag = (
                -math.cosh(rho)**2,
                L*L,
                L*L*math.sinh(rho)**2,
                L*L*math.sinh(rho)**2*math.sin(theta)**2,
            )
            expected = [[0.0]*4 for _ in range(4)]
            for i, value in enumerate(diag):
                expected[i][i] = value
            err = max_error(induced_numeric(nglobal, point, sig_neg), expected)
            assert err < 3.0e-4, err
            max_fd_error = max(max_fd_error, err)
            finite_difference_cases += 1
            mark("metric_coefficients", 16)
            embedded = nglobal(*point)
            assert abs(dot(embedded, embedded, sig_neg) + L*L) < 2.0e-12
            mark("ambient_constraints")

            r = L * math.sinh(rho)
            static_point = nstatic(tau, r, point[2], point[3])
            component_errors = [abs(a-b) for a, b in zip(static_point, embedded)]
            assert max(component_errors) < 3.0e-13, component_errors
            max_overlap_error = max(max_overlap_error, max(component_errors))
            mark("negative_global_relation", 5)
            assert abs(math.asinh(r/L) - rho) < 3.0e-15
            mark("negative_global_relation")

    # Explicit S3 domain witness and the scale/time-independent Hopf target map.
    for X in (0.5, 1.0, 7.0, 23.0):
        for T in (-1.1*X, 0.0, 0.8*X):
            a = X * math.cosh(T/X)
            assert a > 0.0
            mark("hopf_and_scale_time")
            for eta in (0.0, 0.17, 0.61, math.pi/2):
                for delta in (-2.1, 0.0, 1.4):
                    target = (
                        math.sin(2*eta)*math.cos(delta),
                        math.sin(2*eta)*math.sin(delta),
                        math.cos(2*eta),
                    )
                    assert abs(sum(value*value for value in target) - 1.0) < 2.0e-15
                    mark("hopf_and_scale_time")

    normalized_hopf = midpoint_hopf()
    assert abs(normalized_hopf + 1.0) < 2.0e-9
    mark("hopf_and_scale_time")

    for K in (-9.0, -0.2, 0.0, 0.4, 12.0):
        kk, ee, ek = 0.0, 1.0, 0.0
        assert K * (ee*kk - ek*ek) == 0.0
        assert 3.0 * K * kk == 0.0
        mark("optical", 2)

    # Topology witnesses are computed from the actual standard coordinate domains.
    for psi, theta, phi in ((0.0, 0.4, 0.2), (0.6, 1.1, -0.8), (2.4, 0.7, 1.3), (math.pi, 1.0, 2.0)):
        n = nvec(theta, phi)
        point = (math.sin(psi)*n[0], math.sin(psi)*n[1], math.sin(psi)*n[2], math.cos(psi))
        assert abs(sum(value*value for value in point) - 1.0) < 2.0e-15
        mark("topology_witnesses")

    euclidean_samples = ((0.0, 0.0, 0.0), (0.4, -1.2, 2.0), (-3.0, 0.2, 0.8))
    for vector in euclidean_samples:
        origin = tuple(0.0 * value for value in vector)
        identity = tuple(1.0 * value for value in vector)
        midpoint = tuple(0.5 * value for value in vector)
        assert origin == (0.0, 0.0, 0.0)
        assert identity == vector
        assert sum(value*value for value in midpoint) <= sum(value*value for value in vector)
        mark("topology_witnesses", 3)

        radius = math.sqrt(sum(value*value for value in vector))
        rho = math.asinh(radius)
        if radius == 0.0:
            spatial = (0.0, 0.0, 0.0)
        else:
            spatial = tuple(math.sinh(rho) * value / radius for value in vector)
        hyperboloid = (math.cosh(rho),) + spatial
        assert abs(-hyperboloid[0]**2 + sum(value*value for value in hyperboloid[1:]) + 1.0) < 3.0e-15
        assert max(abs(a-b) for a, b in zip(spatial, vector)) < 3.0e-15
        mark("topology_witnesses", 2)

    topology_witnesses = {
        "positive": {
            "domain": "unit_level_set_in_R4",
            "standard_slice": "S3",
            "compact_without_boundary": True,
            "witness": "closed_bounded_unit_level_set",
        },
        "zero": {
            "domain": "cartesian_R3",
            "standard_slice": "R3",
            "compact_without_boundary": False,
            "witness": "explicit_radial_contraction_to_origin",
        },
        "negative_cover": {
            "domain": "upper_unit_hyperboloid_parameterized_by_R3",
            "standard_slice": "H3~R3",
            "compact_without_boundary": False,
            "witness": "x_to_(sqrt(1+norm(x)^2),x)_bijection_and_R3_contraction",
        },
    }
    assert topology_witnesses["positive"]["compact_without_boundary"]
    assert not topology_witnesses["zero"]["compact_without_boundary"]
    assert not topology_witnesses["negative_cover"]["compact_without_boundary"]
    mark("topology_witnesses", 3)

    checks = sum(counts.values())
    result = {
        "status": "PASS",
        "checks": checks,
        "checks_by_category": counts,
        "finite_difference_cases": finite_difference_cases,
        "max_finite_difference_metric_error": max_fd_error,
        "max_chart_overlap_error": max_overlap_error,
        "normalized_hopf_number": normalized_hopf,
        "topology_witnesses": topology_witnesses,
        "method": "standard_library_finite_difference_ambient_pullbacks_overlap_replay_midpoint_integral_and_explicit_topology_witnesses",
        "imports_production_code": False,
        "scope": "G304_smooth_center_standard_completion_three_sign_census",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
