"""Audit possible native origins of the gamma correction c=1/2.

The working cascade uses

    gamma = N exp(-eta/2).

This script checks whether ordinary classical cell quantities have the right
dimensionless size to supply eta/2. If they do not, the half-factor must come
from a normalized boundary transfer rule, determinant measure, or another
native mechanism, not from the raw shell/core loads.
"""

from __future__ import annotations

import math

from native_cell_spectrum import solve_cell_profile
from native_core_solver import monopole_sector, ordinary_sector, p_roots
from native_energy_normalization import core_action_scale, shell_pressure_scale


ETA = 1.0 / 18.0
TARGET = ETA / 2.0


def cell_loads(source: float) -> tuple[float, float, float]:
    x, _f, fx, p_soft = solve_cell_profile(source, -2.5, 0.5, -20.0, 0.0)
    shell = shell_pressure_scale(float(fx[-1]))
    core = core_action_scale(x, fx)
    return shell, core, p_soft


def main() -> None:
    sectors = [
        ("M1", monopole_sector(1)),
        ("M2", monopole_sector(2)),
        ("E1", ordinary_sector(1)),
    ]
    print("Gamma-origin audit")
    print("working correction exponent per step: eta/2")
    print(f"eta={ETA:.12g}")
    print(f"eta/2={TARGET:.12g}")
    print()
    for key, sector in sectors:
        source = ETA * sector.angular_lambda
        if p_roots(source) is None:
            continue
        shell, core, p_soft = cell_loads(source)
        print(f"{key}:")
        print(f"  lambda={sector.angular_lambda:g}")
        print(f"  p={p_soft:.10g}")
        print(f"  shell_pressure={shell:.10g} shell/(eta/2)={shell / TARGET:.6g}")
        print(f"  core_action={core:.10g} core/(eta/2)={core / TARGET:.6g}")
        print()
    print("candidate origins")
    print("  raw shell pressure: no, too small")
    print("  raw core action: no, branch-dependent and too small except still below target")
    print("  quadratic boundary transfer: plausible source of a half-factor, not derived")
    print("  determinant/measure term: plausible source of a half-factor, not derived")


if __name__ == "__main__":
    main()
