#!/usr/bin/env python3
"""Independent exact-Fraction replay without SymPy or production imports."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def poly_add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_scale(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar * coefficient}


def poly_derivative(poly, axis):
    result = {}
    for monomial, coefficient in poly.items():
        power = monomial[axis]
        if not power:
            continue
        reduced = list(monomial)
        reduced[axis] -= 1
        key = tuple(reduced)
        result[key] = result.get(key, Fraction(0)) + coefficient * power
    return {key: value for key, value in result.items() if value}


def monomial(dimension, powers, coefficient=1):
    key = [0] * dimension
    for axis, power in powers.items():
        key[axis] = power
    return {tuple(key): Fraction(coefficient)}


def canonical(indices):
    if len(set(indices)) != len(indices):
        return 0, ()
    inversions = sum(
        indices[i] > indices[j]
        for i in range(len(indices))
        for j in range(i + 1, len(indices))
    )
    return (-1) ** inversions, tuple(sorted(indices))


def form_add_term(form, basis, poly):
    sign, key = canonical(tuple(basis))
    if sign == 0:
        return
    signed = poly_scale(poly, Fraction(sign))
    form[key] = poly_add(form.get(key, {}), signed)
    if not form[key]:
        del form[key]


def exterior_derivative(form, dimension=4):
    result = {}
    for basis, poly in form.items():
        for axis in range(dimension):
            form_add_term(result, (axis,) + basis, poly_derivative(poly, axis))
    return result


STAR_2 = {
    (0, 1): (-1, (2, 3)),
    (0, 2): (+1, (1, 3)),
    (0, 3): (-1, (1, 2)),
    (1, 2): (+1, (0, 3)),
    (1, 3): (-1, (0, 2)),
    (2, 3): (+1, (0, 1)),
}


def hodge_2(form):
    result = {}
    for basis, poly in form.items():
        sign, target = STAR_2[basis]
        form_add_term(result, target, poly_scale(poly, Fraction(sign)))
    return result


def gradient(scalar, dimension=4):
    return {(axis,): derivative for axis in range(dimension) if (derivative := poly_derivative(scalar, axis))}


def form_add(left, right):
    result = {key: dict(value) for key, value in left.items()}
    for basis, poly in right.items():
        form_add_term(result, basis, poly)
    return result


def main():
    # A polynomial connection with multiple mixed derivatives.
    A1 = poly_add(monomial(4, {0: 2}), monomial(4, {1: 1, 2: 1}))
    A2 = poly_add(monomial(4, {0: 1, 3: 1}), monomial(4, {2: 3}))
    A3 = monomial(4, {1: 2, 3: 1})
    A = {(1,): A1, (2,): A2, (3,): A3}
    F = exterior_derivative(A)
    dF = exterior_derivative(F)
    J3 = exterior_derivative(hodge_2(F))
    dJ3 = exterior_derivative(J3)
    assert not dF
    assert not dJ3
    assert J3

    # Exact gauge replay with a nontrivial scalar.
    gauge = poly_add(monomial(4, {0: 1, 1: 1, 2: 1}), monomial(4, {3: 3}))
    F_gauge = exterior_derivative(form_add(A, gradient(gauge)))
    assert F_gauge == F

    # Source-free is not an identity: A=t^2 dx gives J3=-2 dt^dy^dz.
    counter_A = {(1,): monomial(4, {0: 2})}
    counter_F = exterior_derivative(counter_A)
    counter_J = exterior_derivative(hodge_2(counter_F))
    assert counter_J
    assert not exterior_derivative(counter_F)
    assert not exterior_derivative(counter_J)

    # Independent polynomial Hamiltonian check in 8D canonical phase space.
    H = poly_add(
        monomial(8, {0: 1, 4: 2}),
        poly_add(monomial(8, {1: 1, 2: 1, 7: 1}), monomial(8, {5: 3})),
    )
    flow = [poly_derivative(H, 4 + axis) for axis in range(4)] + [
        poly_scale(poly_derivative(H, axis), Fraction(-1)) for axis in range(4)
    ]
    divergence = {}
    for axis, component in enumerate(flow):
        divergence = poly_add(divergence, poly_derivative(component, axis))
    assert not divergence

    # A generic phase-space density is not forced to obey transport.
    flat_flow = [monomial(8, {4: 1}, -1), monomial(8, {5: 1}), monomial(8, {6: 1}), monomial(8, {7: 1})] + [{}, {}, {}, {}]
    density = monomial(8, {0: 1})
    transport = {}
    for axis, component in enumerate(flat_flow):
        # Only multiplication by the constant derivative of x0 is needed here.
        derivative = poly_derivative(density, axis)
        if derivative:
            assert derivative == monomial(8, {})
            transport = poly_add(transport, component)
    assert transport == monomial(8, {4: 1}, -1)

    omega_source = Fraction(3, 2)
    omega_observer = Fraction(1, 1)
    normalization = Fraction(7, 3)
    redshift = omega_source / omega_observer
    epsilon = normalization * omega_observer / (normalization * omega_source)
    assert epsilon == 1 / redshift == Fraction(2, 3)

    result = {
        "implementation": "stdlib_Fraction_polynomial_exterior_algebra_no_SymPy_no_primary_import",
        "dF_zero": not dF,
        "dJ3_zero": not dJ3,
        "J3_nonzero_generic_witness": bool(J3),
        "source_free_counterexample_nonzero": bool(counter_J),
        "gauge_invariance": F_gauge == F,
        "phase_volume_divergence_zero": not divergence,
        "arbitrary_density_transport_nonzero": bool(transport),
        "conditional_energy_ratio": str(epsilon),
        "all_pass": True,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

