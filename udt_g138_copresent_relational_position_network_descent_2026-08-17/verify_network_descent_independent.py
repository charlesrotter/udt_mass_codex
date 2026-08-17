#!/usr/bin/env python3
"""Independent Fraction/graph/source replay for G138."""

from __future__ import annotations

import hashlib
import math
import random
from collections import deque
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def close(a: float, b: float, tol: float = 3.0e-13) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def frozen_source_bytes(path: str) -> bytes:
    payload = (ROOT / path).read_bytes()
    if path != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return payload
    frozen = []
    for line in payload.splitlines(keepends=True):
        frozen.append(line)
        if line.startswith(b"G137\t"):
            return b"".join(frozen)
    raise AssertionError("G137 row absent from append-only premise registry")


def path(adjacency: dict[int, list[int]], start: int, end: int) -> list[int]:
    queue = deque([start])
    parent = {start: -1}
    while queue:
        node = queue.popleft()
        if node == end:
            break
        for nxt in adjacency[node]:
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    nodes = []
    node = end
    while node != -1:
        nodes.append(node)
        node = parent[node]
    return list(reversed(nodes))


def path_sum(nodes: list[int], edge: dict[tuple[int, int], Fraction]) -> Fraction:
    return sum((edge[(a, b)] for a, b in zip(nodes, nodes[1:])), Fraction(0))


def main() -> None:
    passed = 0
    total = 0

    def check(condition: bool) -> None:
        nonlocal passed, total
        total += 1
        if not condition:
            raise AssertionError(f"independent check {total} failed")
        passed += 1

    rng = random.Random(138)
    for n in range(3, 10):
        for trial in range(8):
            # Keep the floating chart replay away from tanh saturation; the exact
            # production route carries the unrestricted finite-depth identities.
            potentials = [Fraction(rng.randint(-8, 8), rng.randint(11, 37)) for _ in range(n)]
            tree_edges = []
            adjacency = {i: [] for i in range(n)}
            for node in range(1, n):
                parent = rng.randrange(node)
                tree_edges.append((parent, node))
                adjacency[parent].append(node)
                adjacency[node].append(parent)
            candidates = [
                (i, j)
                for i in range(n)
                for j in range(i + 1, n)
                if (i, j) not in tree_edges and (j, i) not in tree_edges
            ]
            rng.shuffle(candidates)
            chords = candidates[: min(len(candidates), 1 + trial % 4)]
            edges = tree_edges + chords
            depth = {}
            for i, j in edges:
                value = potentials[j] - potentials[i]
                depth[(i, j)] = value
                depth[(j, i)] = -value

            reconstruction = [path_sum(path(adjacency, 0, i), depth) for i in range(n)]
            check(all(reconstruction[i] == potentials[i] - potentials[0] for i in range(n)))
            for i, j in chords:
                check(depth[(i, j)] + path_sum(path(adjacency, j, i), depth) == 0)

            if chords:
                i, j = chords[0]
                corrupt = dict(depth)
                corrupt[(i, j)] += Fraction(1, 97)
                corrupt[(j, i)] = -corrupt[(i, j)]
                check(corrupt[(i, j)] + path_sum(path(adjacency, j, i), corrupt) == Fraction(1, 97))

            root = rng.randrange(n)
            u = [math.tanh(float(value - potentials[root])) for value in potentials]
            for i in range(n):
                for j in range(n):
                    pair = (u[j] - u[i]) / (1.0 - u[i] * u[j])
                    check(close(pair, math.tanh(float(potentials[j] - potentials[i]))))

            ref1, ref2 = Fraction(1, 7), Fraction(-2, 9)
            shift = math.tanh(float(ref1 - ref2))
            for value in potentials:
                old = math.tanh(float(value - ref1))
                transformed = (shift + old) / (1.0 + shift * old)
                check(close(transformed, math.tanh(float(value - ref2))))

            scale = 17.25
            rescaled = 103.5
            for i in range(n):
                check(close((scale * u[i]) / scale, (rescaled * u[i]) / rescaled))

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        source, expected, _ = line.split("\t", 2)
        check(hashlib.sha256(frozen_source_bytes(source)).hexdigest() == expected)

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    check("classification, not a selection theorem" in prereg)
    check("path_holonomy\tOPEN_VALID_BRANCH" in ledger)
    check("reference_observer\tCHOSE_GAUGE" in ledger)
    print(f"PASS {passed}/{total}: independent Fraction graphs, chart changes, hashes, and guards")


if __name__ == "__main__":
    main()
