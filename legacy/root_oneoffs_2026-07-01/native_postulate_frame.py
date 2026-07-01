"""Working postulate frame for the native matter-cell rebuild.

This script prints the current provisional input set and immediate derived
consequences. It is a guardrail: downstream scans can assume these postulates,
but the file keeps clear what is assumed versus derived.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    symbol: str
    kind: str
    statement: str
    consequence: str


ENTRIES = [
    Entry(
        "Pcell",
        "working postulate",
        "finite-action negative-phi matter cell closes at phi=0 via a boundary layer",
        "gives finite cell spectra; boundary condition defaults to natural flux unless derived otherwise",
    ),
    Entry(
        "Pepsilon",
        "working postulate",
        "unique N=3 epsilon sector fixes global angular-source normalization eta=1/(2N^2)=1/18",
        "ordinary ell=1 allowed, ell=2 excluded, ell=1 endpoint p=1/3",
    ),
    Entry(
        "Pflux",
        "optional working postulate",
        "compact endpoint flux sectors may exist",
        "monopole ladders supply doublet/triplet endpoint sectors",
    ),
    Entry(
        "F",
        "scale input",
        "electron mass is the single dimensionful anchor",
        "converts dimensionless spectra to MeV; does not create hierarchy",
    ),
]


def main() -> None:
    print("Native matter-cell working postulate frame")
    print()
    for entry in ENTRIES:
        print(f"{entry.symbol} [{entry.kind}]")
        print(f"  statement: {entry.statement}")
        print(f"  consequence: {entry.consequence}")
        print()
    print("discipline:")
    print("  use postulates provisionally to explore consequences")
    print("  do not relabel postulate consequences as derived")
    print("  try to eliminate or derive each postulate later")


if __name__ == "__main__":
    main()

