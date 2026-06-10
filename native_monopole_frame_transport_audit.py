"""Audit frame transport for compact-flux monopole sectors.

Ordinary S2 harmonics have a canonical radial identity map because the angular
metric is r^2 dOmega^2. Monopole harmonics additionally depend on a compact
U(1) bundle/connection. Identity transport across radius is natural only if the
flux sector and gauge patching are held fixed across the finite cell.

This script records the distinction without trying to compute explicit monopole
harmonic overlaps.
"""

from __future__ import annotations


def main() -> None:
    print("Monopole frame-transport audit")
    print()
    print("ordinary angular sector:")
    print("  depends only on unit S2 metric")
    print("  radial transport is canonical because r^2 dOmega^2 rescales to dOmega^2")
    print("  identity overlap is metric-derived")
    print()
    print("compact-flux monopole sector:")
    print("  depends on unit S2 metric plus U(1) bundle/connection")
    print("  radial identity transport additionally requires fixed flux integer")
    print("  and fixed gauge patching/parallel transport convention")
    print()
    print("implication for current branches:")
    print("  E1 ordinary triplet Pframe is strongly metric-native")
    print("  M1 primitive compact-flux anchor still depends on Pflux/Pbundle")
    print()
    print("verdict:")
    print("  Pframe is partially derived for ordinary sectors")
    print("  compact-flux anchor needs a separate bundle-transport assumption")


if __name__ == "__main__":
    main()
