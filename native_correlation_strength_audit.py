"""Soft-correlation audit for epsilon-mediated closure choices.

The previous factor-graph audit used hard equality edges. This script uses a
soft Potts-like coupling between neighboring closure labels:

    weight = exp(kappa) if labels are equal, 1 otherwise.

For kappa=0, labels are independent and the entropy count is N^k. As kappa
grows, neighboring labels become correlated and the Shannon effective state
count drops toward the shared-label limit, even though the unnormalized
partition sum can grow.
"""

from __future__ import annotations

import argparse
import itertools
import math


def partition_and_entropy(n_labels: int, nodes: int, kappa: float) -> tuple[float, float]:
    weights = []
    for labels in itertools.product(range(n_labels), repeat=nodes):
        equal_edges = sum(1 for a, b in zip(labels, labels[1:]) if a == b)
        weights.append(math.exp(kappa * equal_edges))
    total = sum(weights)
    entropy = 0.0
    for weight in weights:
        p = weight / total
        entropy -= p * math.log(p)
    return total, entropy


def effective_components(n_labels: int, entropy: float) -> float:
    return entropy / math.log(n_labels)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--constraints", type=int, nargs="+", default=[5, 7])
    parser.add_argument("--kappas", type=float, nargs="+", default=[-2.0, -1.0, 0.0, 0.5, 1.0, 2.0, 5.0])
    args = parser.parse_args()

    print("Soft correlation strength audit")
    print("chain coupling: exp(kappa) reward for adjacent equal labels")
    print("reports Shannon effective state count, not raw partition sum")
    print(f"N={args.N}")
    print()
    for nodes in args.constraints:
        print(f"constraints={nodes}")
        z0 = args.N**nodes
        for kappa in args.kappas:
            z, entropy = partition_and_entropy(args.N, nodes, kappa)
            components = effective_components(args.N, entropy)
            print(
                f"  kappa={kappa:6.2f} Z={z:12.6g} "
                f"Z/Z_ind={z/z0:10.6g} entropy_count={math.exp(entropy):12.6g} "
                f"effective_components={components:8.4f}"
            )
        print()
    print("verdict:")
    print("  soft correlations reduce entropy continuously")
    print("  hard equality is the limiting collapse to one component")


if __name__ == "__main__":
    main()
