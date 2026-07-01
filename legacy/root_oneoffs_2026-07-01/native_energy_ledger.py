"""Energy-scale ledger for the native matter-cell scaffold.

This diagnostic lists how currently identified contributions scale with cell
radius R after the electron anchor is applied. It is not a solver.

The purpose is to identify which terms could break the compressed finite-cell
linear spectrum. Terms that all scale like 1/R cannot generate hierarchy by
themselves after one electron anchor.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnergyTerm:
    name: str
    scaling: str
    status: str
    hierarchy_potential: str
    note: str


TERMS = [
    EnergyTerm(
        "linear cell eigenfrequency",
        "1/R",
        "computed",
        "low",
        "sets compressed omega spectrum; electron anchor fixes R-scale",
    ),
    EnergyTerm(
        "angular-source core action",
        "dimensionless/R? normalization open",
        "computed shape, normalization open",
        "medium",
        "depends on lambda and eta; may shift sectors but currently smooth",
    ),
    EnergyTerm(
        "phi=0 shell pressure",
        "surface term ~ R^0 or 1/R depending action normalization",
        "bookkept, not derived",
        "medium",
        "boundary stiffness can move spectra if large",
    ),
    EnergyTerm(
        "abelian Coulomb",
        "alpha/R",
        "native phi-blind dynamics",
        "low-medium",
        "same scaling as linear cell unless alpha runs or charge structure changes",
    ),
    EnergyTerm(
        "epsilon selection",
        "no energy",
        "derived kinematic selection",
        "none",
        "observability/composite eligibility only",
    ),
    EnergyTerm(
        "rank-2 angular coupling",
        "unknown magnitude",
        "deferred",
        "unknown",
        "matrix structure solid; origin/magnitude open",
    ),
    EnergyTerm(
        "spinor/probe zero-point",
        "unknown here",
        "deferred/postulate candidate",
        "unknown",
        "could change spectrum but imports spin structure",
    ),
    EnergyTerm(
        "running/quantum collective effects",
        "non-power/log/exponential possible",
        "open",
        "high",
        "most plausible route to hierarchy if native",
    ),
]


def main() -> None:
    print("Native matter-cell energy ledger")
    print("Question: what can break the compressed 1/R spectrum after electron anchor?")
    print()
    for term in TERMS:
        print(term.name)
        print(f"  scaling: {term.scaling}")
        print(f"  status: {term.status}")
        print(f"  hierarchy potential: {term.hierarchy_potential}")
        print(f"  note: {term.note}")
        print()


if __name__ == "__main__":
    main()

