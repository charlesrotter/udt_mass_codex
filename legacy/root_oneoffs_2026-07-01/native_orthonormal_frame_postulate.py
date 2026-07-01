"""Minimal orthonormal-frame postulate candidate.

This records the smallest extra rule that turns epsilon volume-form uniqueness
into the trace transfer used by the mass-ladder candidate:

    Pframe:
      the finite negative-phi cell transports an oriented orthonormal angular
      frame between its two boundaries.

Then the transported basis overlap is identity, the epsilon orientation is
preserved, and the transfer trace is N.
"""

from __future__ import annotations


def main() -> None:
    print("Minimal orthonormal-frame postulate candidate")
    print()
    print("Pframe:")
    print("  a closed finite negative-phi matter cell transports an oriented")
    print("  orthonormal angular frame between the core-side boundary and the")
    print("  phi=0 boundary.")
    print()
    print("consequences:")
    print("  epsilon volume form is preserved")
    print("  transported basis-label overlap is identity")
    print("  transfer multiplicity is tr(I_N)=N")
    print("  hard diagonal epsilon transfer is justified at leading order")
    print()
    print("status:")
    print("  this is a smaller postulate than importing a spinor/Dirac operator")
    print("  it is still a postulate until derived from boundary geometry")


if __name__ == "__main__":
    main()
