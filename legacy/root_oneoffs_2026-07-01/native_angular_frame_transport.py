"""Angular frame transport from the UDT metric.

The UDT metric has angular block r^2 dOmega^2. After rescaling by r, every
finite-radius boundary has the same unit S^2 angular metric. A radial cell with
fixed angular coordinates therefore has a canonical pullback between boundary
angular Hilbert spaces for ordinary spherical harmonics.

This derives identity overlap for ordinary angular modes under radial transport.
It does not by itself derive compact-flux sectors or any non-abelian dynamics.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.special import sph_harm_y


def inner_product_y(ell: int, m1: int, m2: int) -> complex:
    def theta_integrand(theta: float) -> complex:
        def phi_integrand(phi: float) -> complex:
            return (
                np.conjugate(sph_harm_y(ell, m1, theta, phi))
                * sph_harm_y(ell, m2, theta, phi)
                * math.sin(theta)
            )

        real, _ = quad(lambda ph: float(phi_integrand(ph).real), 0.0, 2.0 * math.pi)
        imag, _ = quad(lambda ph: float(phi_integrand(ph).imag), 0.0, 2.0 * math.pi)
        return real + 1j * imag

    real, _ = quad(lambda th: float(theta_integrand(th).real), 0.0, math.pi)
    imag, _ = quad(lambda th: float(theta_integrand(th).imag), 0.0, math.pi)
    return real + 1j * imag


def overlap_matrix(ell: int) -> np.ndarray:
    ms = list(range(-ell, ell + 1))
    mat = np.zeros((len(ms), len(ms)), dtype=complex)
    for i, m1 in enumerate(ms):
        for j, m2 in enumerate(ms):
            mat[i, j] = inner_product_y(ell, m1, m2)
    return mat


def main() -> None:
    print("Angular frame transport from metric")
    print("metric angular block: r^2 dOmega^2")
    print("unit angular metric is identical at every radius")
    print()
    for ell in [0, 1, 2]:
        mat = overlap_matrix(ell)
        err = np.max(np.abs(mat - np.eye(2 * ell + 1)))
        print(f"ell={ell}:")
        print(f"  dimension={2 * ell + 1}")
        print(f"  trace overlap={np.trace(mat).real:.12g}")
        print(f"  max |overlap-I|={err:.3e}")
        print()
    print("verdict:")
    print("  ordinary S2 angular frames have canonical identity overlap across radius")
    print("  this derives the ordinary-sector part of Pframe from phi-blind angular geometry")


if __name__ == "__main__":
    main()
