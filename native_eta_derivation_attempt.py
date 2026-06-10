"""Attempt to derive eta=1/(2N^2) from ell=1 angular averaging.

The attractive candidate is

    eta = 1/(2N^2), N=2ell+1=3 -> 1/18.

This script audits simple angular normalizations from the ell=1 triplet:

    normalized mode density,
    averaged density over N modes,
    pair/triple combinatoric normalizations,
    variance/quadrupole norms of the ell=1 angular distribution.

It does not promote a derivation. It reports which routes naturally hit 1/18
and which require inserting an extra factor.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import quad
from scipy.special import sph_harm_y


TARGET = 1.0 / 18.0


@dataclass(frozen=True)
class Candidate:
    name: str
    value: float
    note: str


def sphere_integral_real(func) -> float:
    def theta_integrand(theta: float) -> float:
        def phi_integrand(phi: float) -> float:
            return float(func(theta, phi) * math.sin(theta))

        val, _err = quad(phi_integrand, 0.0, 2.0 * math.pi, epsabs=1e-11)
        return val

    val, _err = quad(theta_integrand, 0.0, math.pi, epsabs=1e-11)
    return val


def y(l: int, m: int, theta: float, phi: float) -> complex:
    return complex(sph_harm_y(l, m, theta, phi))


def main() -> None:
    ell = 1
    n = 2 * ell + 1

    # Addition theorem check: sum_m |Y_lm|^2 = N/(4pi).
    addition = sphere_integral_real(
        lambda th, ph: sum(abs(y(ell, m, th, ph)) ** 2 for m in range(-ell, ell + 1))
    )
    avg_triplet_density = n / (4.0 * math.pi)
    per_mode_avg_density = 1.0 / (4.0 * math.pi)

    # Quadrupole-like anisotropy for a single m=0 real density against uniform.
    uniform = 1.0 / (4.0 * math.pi)
    variance_m0 = sphere_integral_real(
        lambda th, ph: (abs(y(1, 0, th, ph)) ** 2 - uniform) ** 2
    )

    # Dimensionless variance after multiplying by 4pi converts density to
    # "per average sphere density" units.
    variance_m0_scaled = (4.0 * math.pi) * variance_m0

    candidates = [
        Candidate("1/N", 1.0 / n, "triplet average"),
        Candidate("1/N^2", 1.0 / (n * n), "two independent triplet averages"),
        Candidate("1/(2N^2)", 1.0 / (2.0 * n * n), "two averages plus quadratic-action 1/2"),
        Candidate("1/(N(N+1))", 1.0 / (n * (n + 1)), "symmetric-pair-like"),
        Candidate("1/(N(N-1))", 1.0 / (n * (n - 1)), "antisymmetric-pair-like"),
        Candidate("addition integral / N^2", addition / (n * n), "addition theorem integral divided by N^2"),
        Candidate("per-mode avg density", per_mode_avg_density, "raw normalized mode density average"),
        Candidate("triplet avg density", avg_triplet_density, "raw triplet density average"),
        Candidate("m0 density variance scaled", variance_m0_scaled, "single-mode angular anisotropy size"),
        Candidate("variance/(2N)", variance_m0_scaled / (2.0 * n), "anisotropy plus averaging trial"),
    ]

    print("Eta derivation attempt from ell=1 angular averaging")
    print(f"N=2ell+1={n}")
    print(f"target eta=1/18={TARGET:.12g}")
    print(f"addition theorem integral sum_m |Y_1m|^2 dOmega = {addition:.12g}")
    print(f"single m=0 scaled density variance = {variance_m0_scaled:.12g}")
    print()
    for cand in candidates:
        diff = cand.value - TARGET
        rel = diff / TARGET
        hit = "HIT" if abs(rel) < 1e-12 else ""
        print(
            f"{cand.name:32s} value={cand.value:14.10g} "
            f"rel_to_target={rel:12.6g} {hit}"
        )
        print(f"  note: {cand.note}")
    print()
    print("audit verdict:")
    print("  1/(2N^2) is algebraically natural if two independent triplet averages")
    print("  and the quadratic action factor 1/2 are both justified.")
    print("  The angular average alone gives 1/N or 1/N^2, not the extra 1/2.")
    print("  Therefore eta=1/18 is not derived until the source-action factorization")
    print("  is explicitly derived from the UDT action.")


if __name__ == "__main__":
    main()

