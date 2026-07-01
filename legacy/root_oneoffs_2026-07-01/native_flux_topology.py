"""Native topology/flux probe for the negative-phi endpoint.

The vacuum negative-phi branch f=1+a/r removes r=0 as a curvature-singular
endpoint. The spatial domain is then (0, infinity) x S^2, so a radial U(1)
flux sector is topologically possible. This script checks the classical energy
scaling of electric/magnetic radial flux on the UDT metric.

Key point: for ds^2=-f dt^2+f^-1 dr^2+r^2 dOmega^2, the static Maxwell energy
weight N sqrt(gamma) cancels phi:

    N sqrt(gamma) = r^2 sin(theta)

and radial flux energy scales as int dr / r^2. The negative-phi core does not
regularize the flux divergence by itself.
"""

from __future__ import annotations

import argparse


def radial_flux_energy(cutoff: float, rmax: float, flux: float = 1.0) -> float:
    """Return the phi-independent radial scaling for unit-normalized flux energy."""

    if cutoff <= 0:
        raise ValueError("cutoff must be positive")
    if rmax <= cutoff:
        raise ValueError("rmax must exceed cutoff")
    return flux * flux * (1.0 / cutoff - 1.0 / rmax)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rmax", type=float, default=10.0)
    parser.add_argument("--flux", type=float, default=1.0)
    parser.add_argument(
        "--cutoffs",
        type=float,
        nargs="+",
        default=[1.0, 0.5, 0.25, 0.125, 0.0625],
    )
    args = parser.parse_args()

    print("Native radial U(1) flux energy scaling")
    print("metric: ds^2=-f dt^2+f^-1 dr^2+r^2 dOmega^2")
    print("static Maxwell radial integral: flux^2 * integral dr/r^2")
    print(f"rmax={args.rmax:g} flux={args.flux:g}")
    print()
    for cutoff in args.cutoffs:
        energy = radial_flux_energy(cutoff, args.rmax, args.flux)
        print(f"cutoff={cutoff:10.6g}  energy_scale={energy:12.6g}")

    print()
    print("verdict: energy diverges as 1/cutoff; phi does not soften radial flux")


if __name__ == "__main__":
    main()

