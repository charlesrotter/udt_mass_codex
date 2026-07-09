#!/usr/bin/env python3
"""
Live hyperbolic package under Charles J1 posture (2026-07-09).

CHOSE (Charles): x_max literally defines sphere size
  => composition path x ≡ areal radius r ≡ D_A

POSTULATE: finite X = x_max
DERIVED form: x = X tanh φ, 1+z = e^φ, A = (X-x)/(X+x)
DERIVED (static simple metric): full light d_L = (1+z)^2 D_A
CONDITIONAL mass (J1 + MS GR-form): X = 2 G M_tot / c^2

Not: half light, free D_A(r), P_ell foundation, LCDM targeting.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union

import numpy as np

ArrayLike = Union[float, np.ndarray]

# SI
C_SI = 299_792_458.0
G_SI = 6.67430e-11
MPC_M = 3.085677581491367e22
M_SUN = 1.98847e30


def as_array(x: ArrayLike) -> np.ndarray:
    return np.atleast_1d(np.asarray(x, dtype=float))


# ---------------------------------------------------------------------------
# Core maps (J1)
# ---------------------------------------------------------------------------

def phi_of_x(x: ArrayLike, X: float) -> np.ndarray:
    """φ = arctanh(x/X), |x| < X."""
    u = as_array(x) / X
    if np.any(np.abs(u) >= 1.0):
        raise ValueError("|x| must be < X")
    return np.arctanh(u)


def x_of_phi(phi: ArrayLike, X: float) -> np.ndarray:
    """x = X tanh φ (J1: also D_A = r = x)."""
    return X * np.tanh(as_array(phi))


def A_of_x(x: ArrayLike, X: float) -> np.ndarray:
    """Lapse A = e^{-2φ} = (X-x)/(X+x)."""
    x = as_array(x)
    return (X - x) / (X + x)


def one_plus_z_of_x(x: ArrayLike, X: float) -> np.ndarray:
    """1+z = e^φ = sqrt((X+x)/(X-x))."""
    x = as_array(x)
    return np.sqrt((X + x) / (X - x))


def x_of_z(z: ArrayLike, X: float) -> np.ndarray:
    """
    Invert 1+z = e^φ, x = X tanh φ.
    x/X = ((1+z)^2 - 1) / ((1+z)^2 + 1)
    """
    ez2 = (1.0 + as_array(z)) ** 2
    return X * (ez2 - 1.0) / (ez2 + 1.0)


def DA_of_z(z: ArrayLike, X: float) -> np.ndarray:
    """Angular diameter distance under J1: D_A = x(z)."""
    return x_of_z(z, X)


def dL_of_z(z: ArrayLike, X: float) -> np.ndarray:
    """Full light: d_L = (1+z)^2 D_A = (1+z)^2 x(z)."""
    z = as_array(z)
    return (1.0 + z) ** 2 * DA_of_z(z, X)


def dL_over_X(z: ArrayLike) -> np.ndarray:
    """Shape only (X=1): d_L/X = (1+z)^2 * ((1+z)^2-1)/((1+z)^2+1)."""
    return dL_of_z(z, X=1.0)


def DM_of_z(z: ArrayLike, X: float) -> np.ndarray:
    """Etherington intermediate: D_M = (1+z) D_A (naming only; not FLRW dynamics)."""
    z = as_array(z)
    return (1.0 + z) * DA_of_z(z, X)


# ---------------------------------------------------------------------------
# Series (characterization, not results inputs)
# ---------------------------------------------------------------------------

def dL_over_X_series_coeffs():
    """
    d_L/X = z + (3/2) z^2 + O(z^3)  under J1 + full light.
    Documented for low-z feel; do not use as approximation in fits.
    """
    return {"z": 1.0, "z2": 1.5, "note": "CAS/series of dL_over_X"}


# ---------------------------------------------------------------------------
# Mass lock (conditional: J1 + MS form on simple metric)
# ---------------------------------------------------------------------------

def m_of_x(x: ArrayLike, X: float, *, c: float = C_SI, G: float = G_SI) -> np.ndarray:
    """
    MS: m = c² r (1-A)/(2G) with r=x under J1
      => m = (c²/G) x²/(X+x)
    """
    x = as_array(x)
    return (c**2 / G) * (x**2) / (X + x)


def M_tot_of_X(X: float, *, c: float = C_SI, G: float = G_SI) -> float:
    """M_tot = c² X / (2G)  as x→X⁻."""
    return (c**2 * X) / (2.0 * G)


def X_of_M_tot(M: float, *, c: float = C_SI, G: float = G_SI) -> float:
    """X = 2 G M / c²."""
    return (2.0 * G * M) / (c**2)


def X_Mpc_from_M_sun(M_sun: float) -> float:
    X_m = X_of_M_tot(M_sun * M_SUN)
    return X_m / MPC_M


def M_sun_from_X_Mpc(X_Mpc: float) -> float:
    return M_tot_of_X(X_Mpc * MPC_M) / M_SUN


# ---------------------------------------------------------------------------
# Calibration helpers (nuisance — not theory derivation of X)
# ---------------------------------------------------------------------------

def mu_distance_modulus(dL_Mpc: ArrayLike) -> np.ndarray:
    """μ = 5 log10(d_L/Mpc) + 25."""
    return 5.0 * np.log10(np.maximum(as_array(dL_Mpc), 1e-30)) + 25.0


@dataclass
class HyperbolicJ1Model:
    """Bundle with one scale X [Mpc] for convenience."""

    X_Mpc: float

    def DA(self, z: ArrayLike) -> np.ndarray:
        return DA_of_z(z, self.X_Mpc)

    def dL(self, z: ArrayLike) -> np.ndarray:
        return dL_of_z(z, self.X_Mpc)

    def DM(self, z: ArrayLike) -> np.ndarray:
        return DM_of_z(z, self.X_Mpc)

    def M_tot_Msun(self) -> float:
        return M_sun_from_X_Mpc(self.X_Mpc)

    def mu(self, z: ArrayLike) -> np.ndarray:
        return mu_distance_modulus(self.dL(z))


def _self_check():
    """Cheap identities (not a full test suite)."""
    X = 1.0
    z = np.array([0.01, 0.1, 0.5, 1.0, 2.0])
    x = x_of_z(z, X)
    assert np.allclose(one_plus_z_of_x(x, X), 1 + z)
    assert np.allclose(A_of_x(x, X) * (one_plus_z_of_x(x, X) ** 2), 1.0)
    assert np.allclose(dL_of_z(z, X), (1 + z) ** 2 * x)
    # low-z: d_L/X ≈ z + 1.5 z^2
    zg = np.linspace(1e-4, 1e-2, 50)
    approx = zg + 1.5 * zg**2
    assert np.max(np.abs(dL_over_X(zg) - approx) / zg) < 0.02
    # mass at bound
    assert abs(M_tot_of_X(X) - (C_SI**2 * X) / (2 * G_SI)) < 1e-6 * M_tot_of_X(X)
    print("simple_metric_hyperbolic_J1 self-check OK")


if __name__ == "__main__":
    _self_check()
    z = np.array([0.1, 0.5, 1.0, 2.0])
    print("d_L/X:", dL_over_X(z))
    print("series feel z + 1.5 z^2:", z + 1.5 * z**2)
