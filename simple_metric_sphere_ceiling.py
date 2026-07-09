#!/usr/bin/env python3
"""
Sphere-ceiling package (Charles: x_max = max sphere size).

Held:
  D_A = r  (simple metric areal)
  Ceiling: A→0 at finite r = X  (sphere-size bound)
  Full light: d_L = (1+z)^2 D_A
  Static redshift: 1+z = e^φ = 1/sqrt(A)  when A=e^{-2φ}

Primary geometric lead (not χ²-chosen as truth):
  A(r) = 1 - r/X    for 0 ≤ r < X
  ⇒ φ = -½ ln(1 - r/X)
  ⇒ r/X = 1 - 1/(1+z)^2
  ⇒ d_L/X = (1+z)^2 - 1 = z(z+2)

Provenance (honest):
  - Vacuum K-A (ΔA=0) gives A=C0+C1/r, NOT A=1-r/X
  - A=1-r/X is NON-VACUUM: m = c² r²/(2 G X), ρ ∝ 1/(X r) (geometric MS)
  - Same mass lock at bound: M_tot = c² X/(2G) when A(X)=0
  - Related to "critical compactness → 1 at finite r" (KA outer/matter trail)
  - Hyperbolic tanh composition is a DIFFERENT package (not used here)

Contrast (locked, residual-harsh under full light):
  hyp J1: x=X tanh φ, d_L/X = (1+z)^2 ((1+z)^2-1)/((1+z)^2+1)

Do not: half light, free D_A fit, promote by Pantheon alone.
"""
from __future__ import annotations

from typing import Union

import numpy as np

ArrayLike = Union[float, np.ndarray]

C_SI = 299_792_458.0
G_SI = 6.67430e-11
MPC_M = 3.085677581491367e22
M_SUN = 1.98847e30


def as_array(x: ArrayLike) -> np.ndarray:
    return np.atleast_1d(np.asarray(x, dtype=float))


# ----- A = 1 - r/X ceiling -----

def A_linear(r: ArrayLike, X: float) -> np.ndarray:
    r = as_array(r)
    if np.any(r < 0) or np.any(r >= X):
        raise ValueError("need 0 <= r < X")
    return 1.0 - r / X


def phi_of_r_linear(r: ArrayLike, X: float) -> np.ndarray:
    """φ = -½ ln A."""
    return -0.5 * np.log(A_linear(r, X))


def r_of_z_linear(z: ArrayLike, X: float) -> np.ndarray:
    """r/X = 1 - 1/(1+z)^2."""
    ez2 = (1.0 + as_array(z)) ** 2
    return X * (1.0 - 1.0 / ez2)


def DA_of_z_linear(z: ArrayLike, X: float) -> np.ndarray:
    return r_of_z_linear(z, X)


def dL_of_z_linear(z: ArrayLike, X: float) -> np.ndarray:
    """d_L = (1+z)^2 r = X * ((1+z)^2 - 1) = X z (z+2)."""
    z = as_array(z)
    return X * ((1.0 + z) ** 2 - 1.0)


def dL_over_X_linear(z: ArrayLike) -> np.ndarray:
    z = as_array(z)
    return (1.0 + z) ** 2 - 1.0


def m_of_r_linear(r: ArrayLike, X: float, *, c: float = C_SI, G: float = G_SI) -> np.ndarray:
    """MS: m = c² r (1-A)/(2G) = c² r² / (2 G X)."""
    r = as_array(r)
    return (c**2 * r**2) / (2.0 * G * X)


def rho_of_r_linear(r: ArrayLike, X: float, *, c: float = C_SI, G: float = G_SI) -> np.ndarray:
    """
    From m' = 4π r² ρ in geometric identification used with MS
    (c=G=1: ρ = 1/(4π X r); SI restore: ρ = c²/(4π G X r)).
    """
    r = as_array(r)
    return (c**2) / (4.0 * np.pi * G * X * r)


def M_tot_of_X(X: float, *, c: float = C_SI, G: float = G_SI) -> float:
    """At r→X⁻, A→0 ⇒ M = c² X/(2G)."""
    return (c**2 * X) / (2.0 * G)


def M_sun_from_X_Mpc(X_Mpc: float) -> float:
    return M_tot_of_X(X_Mpc * MPC_M) / M_SUN


def X_Mpc_from_M_sun(M_sun: float) -> float:
    X_m = (2.0 * G_SI * M_sun * M_SUN) / (C_SI**2)
    return X_m / MPC_M


# ----- Power family A = 1 - (r/X)^n (characterize; n=1 is live lead) -----

def r_over_X_power(z: ArrayLike, n: float) -> np.ndarray:
    """A=1-(r/X)^n, 1+z=1/sqrt(A) ⇒ (r/X)^n = 1 - 1/(1+z)^2."""
    ez2 = (1.0 + as_array(z)) ** 2
    return (1.0 - 1.0 / ez2) ** (1.0 / n)


def dL_over_X_power(z: ArrayLike, n: float) -> np.ndarray:
    z = as_array(z)
    return (1.0 + z) ** 2 * r_over_X_power(z, n)


# ----- Contrast: hyperbolic J1 (composition package) -----

def dL_over_X_hyp_J1(z: ArrayLike) -> np.ndarray:
    ez = 1.0 + as_array(z)
    return (ez**2) * (ez**2 - 1.0) / (ez**2 + 1.0)


def dL_over_X_const_density_critical(z: ArrayLike) -> np.ndarray:
    """A=1-(r/X)^2 — constant-ρ critical. Regular center; FAILS linear low-z (d_L~√z)."""
    return dL_over_X_power(z, 2.0)


def _self_check():
    X = 1.0
    z = np.array([0.01, 0.1, 0.5, 1.0, 2.0])
    r = r_of_z_linear(z, X)
    A = A_linear(r, X)
    assert np.allclose(A, 1.0 / (1 + z) ** 2)
    assert np.allclose(dL_of_z_linear(z, X), (1 + z) ** 2 * r)
    assert np.allclose(dL_over_X_linear(z), z * (z + 2))
    # series: 2z + z^2
    zg = np.linspace(1e-4, 1e-2, 40)
    assert np.max(np.abs(dL_over_X_linear(zg) - (2 * zg + zg**2))) < 1e-12
    # mass at mid
    rm = 0.5 * X
    m = float(np.asarray(m_of_r_linear(rm, X)).reshape(-1)[0])
    assert abs(m - (C_SI**2 * rm**2) / (2 * G_SI * X)) < 1e-6 * m
    print("simple_metric_sphere_ceiling self-check OK")


if __name__ == "__main__":
    _self_check()
    z = np.array([0.1, 0.5, 1.0, 2.0])
    print("d_L/X linear ceiling:", dL_over_X_linear(z))
    print("d_L/X hyp J1:       ", dL_over_X_hyp_J1(z))
