"""Factor-graph audit for epsilon-mediated closure choices.

Each closure constraint is a factor with an epsilon/frame label i in {1..N}.
If factors are disconnected, the count is N^k. If equality edges correlate
labels, each connected component contributes only N.

This is the cleanest discrete model for the independence question.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque


def component_count(nodes: int, edges: list[tuple[int, int]]) -> int:
    graph: dict[int, list[int]] = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    seen = set()
    components = 0
    for node in range(nodes):
        if node in seen:
            continue
        components += 1
        queue = deque([node])
        seen.add(node)
        while queue:
            current = queue.popleft()
            for nxt in graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return components


def count_for_edges(n: int, nodes: int, edges: list[tuple[int, int]]) -> int:
    return n ** component_count(nodes, edges)


def chain_edges(nodes: int) -> list[tuple[int, int]]:
    return [(i, i + 1) for i in range(nodes - 1)]


def block_edges(nodes: int, blocks: int) -> list[tuple[int, int]]:
    # Partition nodes into approximately equal contiguous blocks, tying labels
    # within each block.
    edges: list[tuple[int, int]] = []
    blocks = max(1, min(blocks, nodes))
    for block in range(blocks):
        start = (block * nodes) // blocks
        end = ((block + 1) * nodes) // blocks
        for i in range(start, end - 1):
            edges.append((i, i + 1))
    return edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--constraints", type=int, nargs="+", default=[5, 7])
    args = parser.parse_args()

    print("Constraint factor-graph audit")
    print("nodes=closure constraints; node label=epsilon/frame index")
    print(f"N={args.N}")
    print()
    for nodes in args.constraints:
        cases = [
            ("independent nodes", []),
            ("one global equality component", chain_edges(nodes)),
            ("three approximate blocks", block_edges(nodes, 3)),
            ("two approximate blocks", block_edges(nodes, 2)),
        ]
        print(f"constraints={nodes}")
        for label, edges in cases:
            comps = component_count(nodes, edges)
            count = count_for_edges(args.N, nodes, edges)
            print(f"  {label:30s} components={comps:2d} count={count}")
        print()
    print("verdict:")
    print("  the mass-ladder entropy requires the factor graph to be disconnected")
    print("  equality correlations between closure labels collapse N^k to N^components")


if __name__ == "__main__":
    main()
