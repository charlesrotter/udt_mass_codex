#!/usr/bin/env python3
"""Exact exterior-calculus ownership checks for the native current/energy audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
coords = sp.symbols("t x y z", real=True)
t, x, y, z = coords


def canonical(indices: tuple[int, ...]):
    if len(set(indices)) != len(indices):
        return 0, ()
    inversions = sum(
        indices[i] > indices[j]
        for i in range(len(indices))
        for j in range(i + 1, len(indices))
    )
    return (-1) ** inversions, tuple(sorted(indices))


def add_term(form, indices, coefficient):
    sign, key = canonical(tuple(indices))
    if sign == 0:
        return
    form[key] = sp.simplify(form.get(key, 0) + sign * coefficient)
    if form[key] == 0:
        del form[key]


def exterior_derivative(form):
    result = {}
    for basis, coefficient in form.items():
        for axis, coordinate in enumerate(coords):
            add_term(result, (axis,) + basis, sp.diff(coefficient, coordinate))
    return result


STAR_2 = {
    (0, 1): (-1, (2, 3)),
    (0, 2): (+1, (1, 3)),
    (0, 3): (-1, (1, 2)),
    (1, 2): (+1, (0, 3)),
    (1, 3): (-1, (0, 2)),
    (2, 3): (+1, (0, 1)),
}


def hodge_2_minkowski(form):
    result = {}
    for basis, coefficient in form.items():
        sign, target = STAR_2[basis]
        add_term(result, target, sign * coefficient)
    return result


def gradient_form(scalar):
    return {(axis,): sp.diff(scalar, coordinate) for axis, coordinate in enumerate(coords)}


def add_forms(left, right):
    result = dict(left)
    for basis, coefficient in right.items():
        add_term(result, basis, coefficient)
    return result


def scale_form(form, scalar):
    return {basis: sp.simplify(scalar * value) for basis, value in form.items()}


def equal_forms(left, right):
    keys = set(left) | set(right)
    return all(sp.simplify(left.get(key, 0) - right.get(key, 0)) == 0 for key in keys)


def serialize(form):
    return {"".join(map(str, basis)): str(sp.simplify(value)) for basis, value in sorted(form.items())}


def main():
    # Arbitrary smooth local connection. No equation of motion is imposed.
    A_functions = [sp.Function(f"A{axis}")(*coords) for axis in range(4)]
    A = {(axis,): component for axis, component in enumerate(A_functions)}
    F = exterior_derivative(A)
    dF = exterior_derivative(F)
    H = hodge_2_minkowski(F)
    J3 = exterior_derivative(H)
    dJ3 = exterior_derivative(J3)
    assert equal_forms(dF, {})
    assert equal_forms(dJ3, {})

    # Gauge invariance is exact; response-current normalization is not selected.
    gauge = sp.Function("lambda")(*coords)
    A_gauge = add_forms(A, gradient_form(gauge))
    assert equal_forms(exterior_derivative(A_gauge), F)
    coupling = sp.symbols("coupling", nonzero=True, real=True)
    assert equal_forms(
        exterior_derivative(hodge_2_minkowski(scale_form(F, coupling))),
        scale_form(J3, coupling),
    )

    # Catch proof: d(*F)=0 is not an identity. This smooth A has nonzero response.
    A_counter = {(1,): t**2}
    F_counter = exterior_derivative(A_counter)
    H_counter = hodge_2_minkowski(F_counter)
    J_counter = exterior_derivative(H_counter)
    assert J_counter
    assert not equal_forms(J_counter, {})
    assert equal_forms(exterior_derivative(F_counter), {})
    assert equal_forms(exterior_derivative(J_counter), {})

    # The metric Hamiltonian owns phase-space volume preservation, not a distribution law.
    phase_coordinates = sp.symbols("x0 x1 x2 x3 p0 p1 p2 p3", real=True)
    xs = phase_coordinates[:4]
    ps = phase_coordinates[4:]
    hamiltonian = sp.Function("Hamiltonian")(*phase_coordinates)
    flow = [sp.diff(hamiltonian, momentum) for momentum in ps] + [
        -sp.diff(hamiltonian, position) for position in xs
    ]
    phase_divergence = sp.simplify(
        sum(sp.diff(component, coordinate) for component, coordinate in zip(flow, phase_coordinates))
    )
    assert phase_divergence == 0
    # On flat phase space, an arbitrary distribution f=x0 is not transported automatically.
    p0, p1, p2, p3 = ps
    flat_hamiltonian = sp.Rational(1, 2) * (-p0**2 + p1**2 + p2**2 + p3**2)
    flat_flow = [sp.diff(flat_hamiltonian, momentum) for momentum in ps] + [0, 0, 0, 0]
    arbitrary_distribution = xs[0]
    transport_residual = sp.simplify(
        sum(
            component * sp.diff(arbitrary_distribution, coordinate)
            for component, coordinate in zip(flat_flow, phase_coordinates)
        )
    )
    assert transport_residual == -p0

    # Conditional energy-ratio theorem. The normalization cancels, but identifying a
    # physical carried covector with the geometric null query remains an extra premise.
    omega_source, omega_observer, normalization = sp.symbols(
        "omega_source omega_observer normalization", positive=True
    )
    redshift = omega_source / omega_observer
    energy_ratio = sp.simplify(
        normalization * omega_observer / (normalization * omega_source)
    )
    assert sp.simplify(energy_ratio - 1 / redshift) == 0

    result = {
        "homogeneous_identity_dF_zero": True,
        "response_definition_J3_dstarF": True,
        "response_conservation_dJ3_zero": True,
        "source_free_dstarF_zero_is_identity": False,
        "source_free_counterexample": {
            "A": "t^2 dx",
            "F": serialize(F_counter),
            "starF": serialize(H_counter),
            "J3": serialize(J_counter),
        },
        "gauge_invariance": True,
        "response_normalization_free": True,
        "hamiltonian_phase_volume_preserved": True,
        "arbitrary_distribution_transport_residual": str(transport_residual),
        "distribution_transport_selected_by_metric": False,
        "conditional_energy_ratio": "epsilon=1/Z after physical p proportional to null-query covector",
        "physical_carrier_identification_selected": False,
        "landing": (
            "GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY"
            "__PHYSICAL_TRANSFER_OPEN"
        ),
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

