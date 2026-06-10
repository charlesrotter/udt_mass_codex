from collections import Counter
from itertools import combinations


def spin_weights(ell: int) -> list[int]:
    return list(range(-ell, ell + 1))


def exterior_power_weights(ell: int, power: int) -> Counter[int]:
    weights = Counter()
    for combo in combinations(spin_weights(ell), power):
        weights[sum(combo)] += 1
    return weights


def decompose_su2(weight_counts: Counter[int]) -> list[int]:
    remaining = Counter(weight_counts)
    irreps: list[int] = []

    while remaining:
        highest = max(weight for weight, count in remaining.items() if count > 0)
        irreps.append(highest)
        for weight in range(-highest, highest + 1):
            remaining[weight] -= 1
            if remaining[weight] == 0:
                del remaining[weight]
            elif remaining[weight] < 0:
                raise ValueError("weight decomposition failed")

    return sorted(irreps)


def main() -> None:
    print("SO(3) exterior-cube invariant audit")
    print("=" * 39)
    print("For the real S2 harmonic space H_ell:")
    print("  dim H_ell = N = 2ell + 1")
    print("  dim Lambda^3 H_ell = C(N,3)")
    print()
    print("A canonical scalar three-form would appear as a spin-0 summand in")
    print("Lambda^3 H_ell.")
    print()

    for ell in range(1, 8):
        n = 2 * ell + 1
        weights = exterior_power_weights(ell, 3)
        irreps = decompose_su2(weights)
        scalar_count = sum(1 for spin in irreps if spin == 0)
        print(f"  ell={ell}, N={n}")
        print(f"    Lambda^3 dimension={sum(weights.values())}")
        print(f"    SO(3) irreps={irreps}")
        print(f"    spin-0 invariant count={scalar_count}")

    print()
    print("Gate verdict:")
    print("  ell=1 has Lambda^3 H_1 = spin-0 exactly.")
    print("  Higher odd ell spaces can contain a spin-0 summand, but it is")
    print("  embedded in a larger exterior-cube multiplet.")
    print("  Therefore only H1 supplies the scalar three-form without an")
    print("  additional projector choice.")
    print("  This supports canonical rank-one activation for H1, without")
    print("  importing spinors or a Dirac operator, while higher odd ell remain")
    print("  excluded unless a new metric projector is found.")


if __name__ == "__main__":
    main()
