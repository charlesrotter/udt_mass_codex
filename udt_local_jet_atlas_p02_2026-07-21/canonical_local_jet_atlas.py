#!/usr/bin/env python3
"""Exact law-neutral local-jet constructions for P02.

This module classifies configuration geometry only.  It contains no action,
field equation, branch merit score, or physical evolution law.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


DIM = 4
ETA = sp.diag(-1, 1, 1, 1)
BIVECTOR_PAIRS = ((0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2))
BIVECTOR_METRIC = sp.diag(-1, -1, -1, 1, 1, 1)


def inertia_triples(dimension: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (negative, positive, dimension - negative - positive)
        for negative in range(dimension + 1)
        for positive in range(dimension - negative + 1)
    )


def inertia_witness(triple: tuple[int, int, int]) -> sp.Matrix:
    negative, positive, zero = triple
    if negative + positive + zero <= 0 or min(triple) < 0:
        raise ValueError("invalid inertia triple")
    return sp.diag(*([-1] * negative + [1] * positive + [0] * zero))


def split_metric(base: sp.Matrix, screen: sp.Matrix, shifts: sp.Matrix) -> sp.Matrix:
    if base.shape != (2, 2) or screen.shape != (2, 2) or shifts.shape != (2, 2):
        raise ValueError("split blocks must be 2x2")
    return (base + shifts.T * screen * shifts).row_join(shifts.T * screen).col_join(
        (screen * shifts).row_join(screen)
    )


def split_congruence_matrix(shifts: sp.Matrix) -> sp.Matrix:
    return sp.eye(2).row_join(sp.zeros(2)).col_join(shifts.row_join(sp.eye(2)))


def pair_lookup(a: int, b: int) -> tuple[int | None, int]:
    if a == b:
        return None, 0
    for index, (left, right) in enumerate(BIVECTOR_PAIRS):
        if (a, b) == (left, right):
            return index, 1
        if (a, b) == (right, left):
            return index, -1
    raise ValueError((a, b))


def tensor_from_bivector_bilinear(bilinear: sp.Matrix) -> sp.MutableDenseNDimArray:
    if bilinear.shape != (6, 6) or bilinear != bilinear.T:
        raise ValueError("bivector bilinear must be symmetric 6x6")
    tensor = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM, DIM)
    for a, b, c, d in product(range(DIM), repeat=4):
        first, first_sign = pair_lookup(a, b)
        second, second_sign = pair_lookup(c, d)
        tensor[a, b, c, d] = (
            0
            if first is None or second is None
            else sp.simplify(first_sign * second_sign * bilinear[first, second])
        )
    return tensor


def bivector_bilinear(tensor) -> sp.Matrix:
    return sp.Matrix(
        6,
        6,
        lambda first, second: tensor[
            BIVECTOR_PAIRS[first][0],
            BIVECTOR_PAIRS[first][1],
            BIVECTOR_PAIRS[second][0],
            BIVECTOR_PAIRS[second][1],
        ],
    )


def curvature_operator(tensor) -> sp.Matrix:
    return sp.simplify(BIVECTOR_METRIC * bivector_bilinear(tensor))


def tensor_from_curvature_operator(operator: sp.Matrix) -> sp.MutableDenseNDimArray:
    bilinear = sp.simplify(BIVECTOR_METRIC * operator)
    return tensor_from_bivector_bilinear(bilinear)


def algebraic_curvature_checks(tensor) -> dict[str, bool]:
    first_pair = all(
        sp.simplify(tensor[a, b, c, d] + tensor[b, a, c, d]) == 0
        for a, b, c, d in product(range(DIM), repeat=4)
    )
    second_pair = all(
        sp.simplify(tensor[a, b, c, d] + tensor[a, b, d, c]) == 0
        for a, b, c, d in product(range(DIM), repeat=4)
    )
    pair_exchange = all(
        sp.simplify(tensor[a, b, c, d] - tensor[c, d, a, b]) == 0
        for a, b, c, d in product(range(DIM), repeat=4)
    )
    first_bianchi = all(
        sp.simplify(
            tensor[a, b, c, d] + tensor[a, c, d, b] + tensor[a, d, b, c]
        )
        == 0
        for a, b, c, d in product(range(DIM), repeat=4)
    )
    return {
        "first_pair_antisymmetry": first_pair,
        "second_pair_antisymmetry": second_pair,
        "pair_exchange": pair_exchange,
        "first_bianchi": first_bianchi,
    }


def ricci_from_riemann(tensor, metric_inverse: sp.Matrix = ETA) -> sp.Matrix:
    return sp.Matrix(
        DIM,
        DIM,
        lambda b, d: sp.simplify(
            sum(
                metric_inverse[a, c] * tensor[a, b, c, d]
                for a in range(DIM)
                for c in range(DIM)
            )
        ),
    )


def scalar_from_ricci(ricci: sp.Matrix, metric_inverse: sp.Matrix = ETA):
    return sp.simplify(
        sum(metric_inverse[a, b] * ricci[a, b] for a in range(DIM) for b in range(DIM))
    )


def schouten_from_ricci(ricci: sp.Matrix, metric: sp.Matrix = ETA) -> sp.Matrix:
    scalar = scalar_from_ricci(ricci, metric.inv())
    return sp.simplify(sp.Rational(1, 2) * (ricci - scalar * metric / 6))


def riemann_from_ricci(ricci: sp.Matrix, metric: sp.Matrix = ETA):
    schouten = schouten_from_ricci(ricci, metric)
    tensor = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM, DIM)
    for a, b, c, d in product(range(DIM), repeat=4):
        tensor[a, b, c, d] = sp.simplify(
            metric[a, c] * schouten[b, d]
            - metric[a, d] * schouten[b, c]
            - metric[b, c] * schouten[a, d]
            + metric[b, d] * schouten[a, c]
        )
    return tensor


def weyl_from_riemann(tensor, metric: sp.Matrix = ETA):
    ricci = ricci_from_riemann(tensor, metric.inv())
    ricci_part = riemann_from_ricci(ricci, metric)
    output = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM, DIM)
    for index in product(range(DIM), repeat=4):
        output[index] = sp.simplify(tensor[index] - ricci_part[index])
    return output


def normal_ddg_from_riemann(tensor) -> sp.MutableDenseNDimArray:
    """Metric second jet in Riemann normal coordinates for the declared convention."""
    second = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM, DIM)
    for a, b, mu, nu in product(range(DIM), repeat=4):
        second[a, b, mu, nu] = sp.simplify(
            -sp.Rational(1, 3) * (tensor[mu, a, nu, b] + tensor[mu, b, nu, a])
        )
    return second


def riemann_from_normal_ddg(second) -> sp.MutableDenseNDimArray:
    tensor = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM, DIM)
    for a, b, mu, nu in product(range(DIM), repeat=4):
        tensor[a, b, mu, nu] = sp.simplify(
            sp.Rational(1, 2)
            * (
                second[mu, b, a, nu]
                - second[mu, a, nu, b]
                - second[nu, b, a, mu]
                + second[nu, a, mu, b]
            )
        )
    return tensor


def sectional_rank_witness(rank: int):
    if rank not in range(7):
        raise ValueError(rank)
    diagonal = [sp.Integer(index + 1) if index < rank else sp.Integer(0) for index in range(6)]
    operator = sp.diag(*diagonal)
    return tensor_from_curvature_operator(operator)


def ricci_rank_witness(rank: int):
    if rank not in range(5):
        raise ValueError(rank)
    mixed_entries = [sp.Integer(index + 1) if index < rank else sp.Integer(0) for index in range(4)]
    mixed = sp.diag(*mixed_entries)
    lower = sp.simplify(ETA * mixed)
    return lower, riemann_from_ricci(lower, ETA)


def petrov_q_witnesses() -> dict[str, sp.Matrix]:
    imaginary = sp.I
    return {
        "I": sp.diag(1, 2, -3),
        "D": sp.diag(1, 1, -2),
        "II": sp.Matrix([[2, imaginary, 0], [imaginary, 0, 0], [0, 0, -2]]),
        "III": sp.Matrix([[0, 1, imaginary], [1, 0, 0], [imaginary, 0, 0]]),
        "N": sp.Matrix([[1, imaginary, 0], [imaginary, -1, 0], [0, 0, 0]]),
        "O": sp.zeros(3),
    }


def weyl_from_q(q_matrix: sp.Matrix):
    if q_matrix.shape != (3, 3) or q_matrix != q_matrix.T or sp.trace(q_matrix) != 0:
        raise ValueError("Q must be symmetric and trace free")
    electric = q_matrix.applyfunc(sp.re)
    magnetic = q_matrix.applyfunc(sp.im)
    operator = (-electric).row_join(-magnetic).col_join(
        magnetic.row_join(-electric)
    )
    return tensor_from_curvature_operator(operator)


def q_from_weyl(tensor) -> sp.Matrix:
    bilinear = bivector_bilinear(tensor)
    electric = bilinear[:3, :3]
    magnetic = bilinear[:3, 3:]
    return sp.simplify(electric + sp.I * magnetic)


def petrov_invariants(q_matrix: sp.Matrix) -> dict[str, object]:
    invariant_i = sp.simplify(sp.trace(q_matrix**2) / 2)
    invariant_j = sp.simplify(-sp.trace(q_matrix**3) / 6)
    delta = sp.simplify(invariant_i**3 - 27 * invariant_j**2)
    return {"I": invariant_i, "J": invariant_j, "Delta": delta}


def classify_petrov(q_matrix: sp.Matrix) -> str:
    zero = sp.zeros(3)
    if q_matrix == zero:
        return "O"
    if sp.simplify(q_matrix**2) == zero:
        return "N"
    if sp.simplify(q_matrix**3) == zero:
        return "III"
    invariants = petrov_invariants(q_matrix)
    if invariants["Delta"] != 0:
        return "I"
    if invariants["I"] != 0:
        repeated = sp.simplify(3 * invariants["J"] / invariants["I"])
        quadratic = sp.simplify(
            (q_matrix - repeated * sp.eye(3)) * (q_matrix + 2 * repeated * sp.eye(3))
        )
        return "D" if quadratic == zero else "II"
    raise ValueError("Q is outside the six nondegenerate/nilpotent Petrov cases")


def first_split_kinematics(
    screen: sp.Matrix,
    shifts: sp.Matrix,
    screen_first: tuple[sp.Matrix, ...],
    shifts_first: tuple[sp.Matrix, ...],
) -> dict[str, object]:
    if screen.shape != (2, 2) or shifts.shape != (2, 2):
        raise ValueError("screen and shifts must be 2x2")
    if len(screen_first) != DIM or len(shifts_first) != DIM:
        raise ValueError("four coordinate derivatives required")
    inverse = screen.inv()
    twist = sp.zeros(2, 1)
    for vertical in range(2):
        twist[vertical] = sp.simplify(
            shifts_first[0][vertical, 1]
            - shifts_first[1][vertical, 0]
            - sum(
                shifts[other, 0] * shifts_first[2 + other][vertical, 1]
                for other in range(2)
            )
            + sum(
                shifts[other, 1] * shifts_first[2 + other][vertical, 0]
                for other in range(2)
            )
        )
    deformations = []
    expansions = []
    shears = []
    for base in range(2):
        horizontal_screen = screen_first[base] - sum(
            (shifts[vertical, base] * screen_first[2 + vertical] for vertical in range(2)),
            sp.zeros(2),
        )
        vertical_derivative = sp.Matrix(
            2,
            2,
            lambda derivative, output: shifts_first[2 + derivative][output, base],
        )
        lie_derivative = sp.simplify(
            horizontal_screen - vertical_derivative * screen - screen * vertical_derivative.T
        )
        deformation = sp.simplify(lie_derivative / 2)
        expansion = sp.simplify(sp.trace(inverse * deformation))
        shear = sp.simplify(deformation - expansion * screen / 2)
        deformations.append(deformation)
        expansions.append(expansion)
        shears.append(shear)
    expansion_matrix = sp.Matrix(expansions)
    shear_map = sp.Matrix(
        [[shears[base][0, 0], shears[base][0, 1], shears[base][1, 1]] for base in range(2)]
    )
    return {
        "twist": twist,
        "twist_rank": twist.rank(),
        "deformations": tuple(deformations),
        "expansion": expansion_matrix,
        "expansion_rank": expansion_matrix.rank(),
        "shears": tuple(shears),
        "shear_map": shear_map,
        "shear_rank": shear_map.rank(),
    }


def split_kinematic_witness(expansion_rank: int, shear_rank: int, twist_rank: int):
    if expansion_rank not in (0, 1) or shear_rank not in (0, 1, 2) or twist_rank not in (0, 1):
        raise ValueError("invalid first-jet ranks")
    screen = sp.eye(2)
    shifts = sp.zeros(2)
    expansions = (sp.Integer(1), sp.Integer(0)) if expansion_rank else (sp.Integer(0), sp.Integer(0))
    basis_zero = sp.zeros(2)
    basis_diagonal = sp.diag(1, -1)
    basis_offdiagonal = sp.Matrix([[0, 1], [1, 0]])
    if shear_rank == 0:
        shears = (basis_zero, basis_zero)
    elif shear_rank == 1:
        shears = (basis_diagonal, basis_zero)
    else:
        shears = (basis_diagonal, basis_offdiagonal)
    screen_first = [sp.zeros(2) for _ in range(DIM)]
    for base in range(2):
        screen_first[base] = sp.simplify(expansions[base] * sp.eye(2) + 2 * shears[base])
    shifts_first = [sp.zeros(2) for _ in range(DIM)]
    if twist_rank:
        shifts_first[0][0, 1] = 1
    return screen, shifts, tuple(screen_first), tuple(shifts_first)


def csn_transform_screen_first(
    screen: sp.Matrix,
    screen_first: tuple[sp.Matrix, ...],
    sigma_first: tuple[sp.Expr, ...],
) -> tuple[sp.Matrix, ...]:
    if len(sigma_first) != DIM:
        raise ValueError("four CSN derivatives required")
    return tuple(
        sp.simplify(screen_first[coordinate] + 2 * sigma_first[coordinate] * screen)
        for coordinate in range(DIM)
    )


def sympy_tensor_to_nested(tensor):
    if len(tensor.shape) != 4:
        raise ValueError("rank-four tensor required")
    return [
        [
            [
                [sp.sstr(tensor[a, b, c, d]) for d in range(DIM)]
                for c in range(DIM)
            ]
            for b in range(DIM)
        ]
        for a in range(DIM)
    ]
