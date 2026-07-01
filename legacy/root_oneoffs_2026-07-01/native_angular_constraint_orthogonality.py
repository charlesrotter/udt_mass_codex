"""Orthogonality audit for ordinary angular closure constraints.

If non-scalar angular endpoint constraints are carried by orthogonal angular
modes, the boundary quadratic form is diagonal at leading order. That supports
factorization of angular closure constraints, though it does not by itself
derive epsilon mediation.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.special import sph_harm_y


def inner(ell: int, m1: int, m2: int) -> complex:
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


def gram(ell: int) -> np.ndarray:
    ms = list(range(-ell, ell + 1))
    mat = np.zeros((len(ms), len(ms)), dtype=complex)
    for a, m1 in enumerate(ms):
        for b, m2 in enumerate(ms):
            mat[a, b] = inner(ell, m1, m2)
    return mat


def main() -> None:
    print("Angular constraint orthogonality audit")
    print("ordinary spherical harmonic Gram matrices")
    print()
    for ell in [1, 2]:
        mat = gram(ell)
        offdiag = mat - np.diag(np.diag(mat))
        max_offdiag = float(np.max(np.abs(offdiag)))
        max_diag_err = float(np.max(np.abs(np.diag(mat) - 1.0)))
        print(f"ell={ell}:")
        print(f"  dimension={2 * ell + 1}")
        print(f"  max offdiag={max_offdiag:.3e}")
        print(f"  max diag error={max_diag_err:.3e}")
        print()
    print("verdict:")
    print("  ordinary angular boundary modes are orthogonal at leading order")
    print("  this supports factorized angular constraints, not epsilon mediation by itself")


if __name__ == "__main__":
    main()
