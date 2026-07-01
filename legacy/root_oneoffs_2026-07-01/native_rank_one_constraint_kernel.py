import math
import numpy as np


def projector(i: int, n: int = 3) -> np.ndarray:
    p = np.zeros((n, n))
    p[i, i] = 1.0
    return p


def main() -> None:
    n = 3
    eta = 1.0 / 18.0
    side = eta / 2.0
    gamma = n * math.exp(-side)

    print("Rank-one constraint-kernel audit")
    print("=" * 34)
    print("For one scalar closure equation measured in H1:")
    print("  admissible label projectors P_i = |i><i|, i=1..N")
    print("  each label carries one-sided action eta/2")
    print("  Z_1 = sum_i exp(-eta/2) = N exp(-eta/2)")
    print(f"  Z_1 = {gamma:.12g}")
    print()

    summed_projector = sum(projector(i, n) for i in range(n))
    print("Sum over rank-one projectors:")
    print(f"  sum_i P_i = I_{n}")
    print(f"  trace(sum_i P_i) = {np.trace(summed_projector):.12g}")
    print()

    print("For k scalar closure equations:")
    for k in range(1, 6):
        tensor_weight = gamma**k
        block_weight = gamma
        print(f"  k={k}: tensor-product weight={tensor_weight:.12g}, one-block weight={block_weight:.12g}")

    print("\nGranularity verdict:")
    print("  - A full H1 block gives one trace.")
    print("  - k independent scalar closure equations give a tensor product of k")
    print("    rank-one H1 label traces, hence gamma^k.")
    print("  - The current depth rule requires the boundary action to factor at the")
    print("    scalar-equation level, not merely at the H1-block level.")
    print("  - The remaining metric task is to identify the scalar closure equations")
    print("    and show their projectors are independent.")


if __name__ == "__main__":
    main()
