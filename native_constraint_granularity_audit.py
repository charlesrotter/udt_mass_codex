import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Branch:
    name: str
    dimension: int
    prefactor: float


def component_depth(dimension: int, n: int) -> int:
    return n + 2 * max(0, dimension - 1)


def block_count(dimension: int) -> int:
    # One H1 frame block plus up to two shape blocks.
    return 1 + (2 if dimension > 1 else 0)


def component_weight(dimension: int, n: int, eta: float) -> float:
    gamma = n * math.exp(-eta / 2.0)
    return gamma ** component_depth(dimension, n)


def block_weight(dimension: int, n: int, eta: float) -> float:
    # Treat each closure block as one transfer trace. The frame block has rank N.
    # Shape blocks have rank max(1,d-1) if they are subspace traces, not N traces.
    weight = n * math.exp(-eta / 2.0)
    if dimension > 1:
        shape_rank = dimension - 1
        weight *= (shape_rank * math.exp(-eta / 2.0)) ** 2
    return weight


def n_per_scalar_shape_weight(dimension: int, n: int, eta: float) -> float:
    # Intermediate model: one H1 frame trace plus scalar shape equations,
    # each with N possible frame labels.
    gamma = n * math.exp(-eta / 2.0)
    return gamma ** (1 + 2 * max(0, dimension - 1))


def main() -> None:
    n = 3
    eta = 1.0 / 18.0
    me = 0.51099895
    branches = [
        Branch("M1", 2, 1.0),
        Branch("E1", 3, 2.0),  # diagnostic dimension/prefactor placeholder
    ]

    print("Constraint granularity audit")
    print("=" * 29)
    print("Current ladder uses component-level depth:")
    print("  depth = N + 2(d-1)")
    print("This treats each scalar closure equation as its own H1 transfer trace.")
    print()
    print("Alternative block-level view:")
    print("  one full H1 frame block contributes one trace, not N traces.")
    print("  shape subspaces may contribute block traces rather than one trace per component.")
    print()

    for branch in branches:
        comp_depth = component_depth(branch.dimension, n)
        comp = component_weight(branch.dimension, n, eta)
        scalar_shape = n_per_scalar_shape_weight(branch.dimension, n, eta)
        block = block_weight(branch.dimension, n, eta)
        print(branch.name)
        print(f"  dimension d={branch.dimension}")
        print(f"  component depth N+2(d-1)={comp_depth}")
        print(f"  component-level weight={comp:.12g}")
        print(f"  one-frame plus N-labeled scalar-shape weight={scalar_shape:.12g}")
        print(f"  block-level weight={block:.12g}")
        print(f"  diagnostic component mass={me * comp:.6g} MeV")
        print(f"  diagnostic block mass={me * block:.6g} MeV")

    print("\nAudit verdict:")
    print("  - H1 rank by itself gives one trace over a three-dimensional block.")
    print("  - The current depth rule requires a finer granularity: each scalar")
    print("    closure equation must independently carry an H1/frame trace.")
    print("  - This is not yet derived by orthogonality or isotropy alone.")
    print("  - The next derivation must identify scalar boundary equations whose")
    print("    label choices are independent H1-kernel observables.")


if __name__ == "__main__":
    main()
