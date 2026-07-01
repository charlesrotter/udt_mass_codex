"""Zoom-out scorecard for candidate native hierarchy mechanisms."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Mechanism:
    name: str
    hierarchy_power: str
    selection_power: str
    assumptions: str
    failure_mode: str
    next_test: str


MECHANISMS = [
    Mechanism(
        "classical finite-cell spectrum",
        "O(1) ratios only",
        "gives finite-cell modes",
        "cell boundary and electron anchor",
        "compressed spectrum",
        "done; use as coefficients, not hierarchy source",
    ),
    Mechanism(
        "common radius-flow stabilization",
        "too weak with common coefficients",
        "none by itself",
        "extra positive-power energy term",
        "requires huge sector-dependent B",
        "only revisit if B derives from native running",
    ),
    Mechanism(
        "endpoint admissibility/self-similarity",
        "selects sectors, not full hierarchy",
        "strong: p=0 excludes scalar, p=1/3 selects E1, ell=2 excluded",
        "eta normalization",
        "does not create large ratios alone",
        "derive eta/source normalization",
    ),
    Mechanism(
        "compact bundle/topology",
        "selects M1 anchor, not full hierarchy",
        "strong conditional: |n|=1 primitive",
        "Pbundle0 nontrivial compact bundle occupancy",
        "bundle not forced by metric alone",
        "derive Pbundle0 or find non-bundle anchor",
    ),
    Mechanism(
        "angular determinant/RG",
        "can supply log-scale corrections",
        "unclear",
        "native subtraction/measure",
        "scheme dependence; easy residual fitting",
        "derive subtraction from boundary action",
    ),
    Mechanism(
        "boundary closure entropy",
        "strong: N^5/N^7 scale",
        "strong if constraints are epsilon-mediated",
        "independent epsilon/frame choice per constraint",
        "overcounting if choices globally correlated",
        "derive factorized epsilon-mediated boundary constraints",
    ),
]


def main() -> None:
    print("Native mechanism scorecard")
    print("Zoom-out audit: avoid locking onto one mechanism too early.")
    print()
    for mechanism in MECHANISMS:
        print(mechanism.name)
        print(f"  hierarchy power: {mechanism.hierarchy_power}")
        print(f"  selection power: {mechanism.selection_power}")
        print(f"  assumptions: {mechanism.assumptions}")
        print(f"  failure mode: {mechanism.failure_mode}")
        print(f"  next test: {mechanism.next_test}")
        print()
    print("verdict:")
    print("  current best hierarchy source is boundary closure entropy")
    print("  current best selection sources are endpoint admissibility and compact topology")
    print("  determinant/RG remains a correction candidate, not the main mechanism yet")


if __name__ == "__main__":
    main()
