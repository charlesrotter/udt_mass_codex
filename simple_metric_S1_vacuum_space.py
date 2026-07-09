#!/usr/bin/env python3
"""
S1 — Vacuum solution-space inventory on the simple metric.

OBSERVE characters of native vacuum solutions. Full light is a READOUT only
(not used inside solves). No χ² in the solution loop. No imposed A(X)=0 BC.

Forks (SIMPLE_METRIC_MACRO + harmonic triangle):
  K-R1   : (r^2 φ')' = 0           → φ = φ∞ - q/r
  W=1    : (r^2 φ')' = 4 e^{-2φ}   → structure from prior asymptotics tile
  K-UW   : Δ e^{-φ} = 0            → e^{-φ} = C0 + C1/r
  K-A    : Δ e^{-2φ} = 0           → A = C0 + C1/r  (Schw branch C0=1)

Readout (chart origin observer φ=0 at r_o, or exterior observer as noted):
  1+z = e^{φ_s - φ_o},  D_A = r_s (or |r_s-r_o| care),  d_L = (1+z)^2 D_A
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent


def dL_full(z, r):
    return (1.0 + z) ** 2 * r


# ----- K-R1 Coulomb -----
def KR1_phi(r, q, r0):
    """φ(r0)=0, φ = q(1/r0 - 1/r) for r>=r0, q>0 → redshift outward."""
    return q * (1.0 / r0 - 1.0 / r)


def inventory_KR1():
    q, r0 = 1.0, 1.0
    r = np.linspace(r0, 50.0, 500)
    phi = KR1_phi(r, q, r0)
    z = np.exp(phi) - 1.0
    dL = dL_full(z, r)  # D_A = r if origin is not r0 — careful
    # Observer at r0: D_A for source at r is not simply r; for SSS central obs D_A=r_source
    # If observer at r0>0 off-center, harder. Standard inventory: observer at center
    # Coulomb singular at 0 — use observer at r0 with D_A ~ r for rough character if origin chart
    # Character inventory: use central-style with r as label, φ shifted so φ(r_min)=0
    r_c = np.linspace(0.5, 20.0, 400)
    # φ = -q/r + q/r_min so φ(r_min)=0, increasing if we take q<0... for redshift with r increase need φ increase
    # φ = q/r_min - q/r with q>0: increases with r
    phi_c = q * (1.0 / r_c[0] - 1.0 / r_c)
    z_c = np.exp(phi_c) - 1.0
    # low-z: small r-r_min
    return {
        "fork": "K-R1 Coulomb",
        "EL": "(r^2 phi')'=0",
        "solution": "phi = phi_inf - q/r",
        "vacuum": True,
        "center": "singular at r=0 if q≠0 (chart)",
        "far": "phi→phi_inf finite; A→e^{-2 phi_inf}>0",
        "A_to_0_finite_r": False,
        "z_max_outward": float(np.exp(q / r0) - 1.0),  # from r0 to inf
        "hard_barrier_ell": False,
        "low_z_class": "phi~q(r-r0)/r0^2 near r0 → linear in Δr if obs not at 0; at center singular",
        "dL_character": "D_A=r grows without bound; z→z_max finite ⇒ d_L→∞ still via r",
        "ceiling_sphere_size": False,
        "notes": "redder then limited depth; open spatial infinity",
    }


# ----- K-UW -----
def inventory_KUW():
    # e^{-phi} = C0 + C1/r. Horizon if C0*C1 < 0 appropriately: psi=0 at r*=-C1/C0
    # Take C0>0, C1=-C0*r* <0 so zero at r*=r_star
    r_star = 1.0
    C0 = 1.0
    C1 = -C0 * r_star  # psi=0 at r_star
    # Exterior r > r_star: psi = C0(1 - r_star/r) > 0
    # phi = -ln psi → +∞ as r→r_star+
    # For "looking out" from large r to larger r: phi decreases toward inf if...
    # psi→C0 at inf, phi→-ln C0. At r→r_star+, phi→+∞.
    # Observer at large R, source toward horizon: high z. Observer center inside forbidden.
    return {
        "fork": "K-UW clock-harmonic",
        "EL": "Delta e^{-phi}=0",
        "solution": "e^{-phi}=C0+C1/r",
        "vacuum": True,
        "center": "depends on branch; horizon branch has r*= -C1/C0",
        "far": "phi→-ln|C0| if C0≠0",
        "A_to_0_finite_r": True,  # A=psi^2→0 at r*
        "z_max_outward": None,  # outward to inf: finite; toward horizon: ∞
        "hard_barrier_ell": True,  # proper distance to horizon diverges (K-UW known)
        "low_z_class": "local expansion about observer depends on seat",
        "dL_character": "near horizon z→∞ at finite r*; D_A=r* finite ⇒ d_L→∞ via (1+z)^2",
        "ceiling_sphere_size": "horizon at finite r* (inner-type wall from exterior)",
        "notes": "c-like horizon; shift purity issue vs R1 kinetic",
    }


# ----- K-A Schw -----
def inventory_KA():
    # A=1-rs/r, exterior r>rs
    return {
        "fork": "K-A lapse-harmonic / G_theta_theta=0",
        "EL": "Delta A=0; vacuum energy ⇒ A=1-rs/r",
        "solution": "A=1-rs/r, phi=-1/2 ln A",
        "vacuum": True,
        "center": "singularity r=0 inside horizon; exterior chart r>rs",
        "far": "A→1, phi→0 (flat)",
        "A_to_0_finite_r": True,  # at r=rs
        "z_max_outward": 0.0,  # outward to inf z→0 if obs outside; static
        "hard_barrier_ell": "proper distance to horizon finite (Schw)",
        "low_z_class": "weak field ~ rs/r Newtonian",
        "dL_character": "local mass, not cosmic filled ceiling at large r",
        "ceiling_sphere_size": "horizon rs — local hole, not outer cosmic max sphere",
        "notes": "elegant local vacuum; not a filled-universe outer sphere ceiling",
    }


# ----- W=1 uncompensated vacuum -----
def inventory_W1():
    # Integrate (r^2 phi')' = 4 e^{-2phi}, Z=1
    # y = [phi, Q] Q=phi'; Q' = 4 e^{-2phi}/r^2 - 2Q/r
    def integrate(r0=1.0, u0=0.5, r_max=80.0):
        def f(r, y):
            phi, Q = y
            em2 = np.exp(np.clip(-2 * phi, -40, 40))
            Qp = 4.0 * em2 / (r**2) - 2.0 * Q / r
            return [Q, Qp]

        sol = solve_ivp(f, (r0, r_max), [0.0, u0], dense_output=True, rtol=1e-7, atol=1e-9, max_step=0.05)
        r = np.linspace(r0, sol.t[-1], 400)
        phi, Q = sol.sol(r)
        return r, phi, Q, sol.success

    r, phi, Q, ok = integrate()
    z = np.exp(phi - phi[0]) - 1.0
    phi_inf = float(phi[-1])
    # ell
    ell = np.trapezoid(np.exp(phi), r)
    return {
        "fork": "W=1 uncompensated vacuum",
        "EL": "(r^2 phi')' = 4 e^{-2 phi}",
        "solution": "numeric outward; quasi-Coulomb late",
        "vacuum": True,
        "center": "inward deep dilation (prior tile)",
        "far": f"phi→plateau ~{phi_inf:.3f} (sample u0=0.5)",
        "A_to_0_finite_r": False,
        "z_max_outward": float(np.exp(phi_inf) - 1.0),
        "hard_barrier_ell": False,
        "ell_to_rmax_sample": float(ell),
        "low_z_class": "depends on start; locally expandable",
        "dL_character": "r→∞, z→z_max finite ⇒ open universe depth-limited",
        "ceiling_sphere_size": False,
        "numeric_ok": ok,
        "notes": "SQ: source e^{-2phi} dies as phi rises — no vacuum outer wall",
    }


# ----- Optional readout demo: d_L shape class only (no chi2) -----
def shape_classes():
    """Analytic low-z / high-z classes for closed-form forks with D_A=r central."""
    return {
        "KR1_if_forced_through_origin": "singular; not a clean central cosmology",
        "KUW_exterior_to_horizon": "z→∞ at finite r*; d_L→∞; local wall not outer max sphere growth",
        "KA_Schw_exterior": "asymptotically flat; not cosmic ceiling",
        "W1_outward": "finite z_max, r→∞, d_L→∞ slowly",
        "full_light_readout": "d_L=(1+z)^2 r always after solve",
    }


def main():
    print("=" * 70)
    print("S1 vacuum solution-space inventory (characters, no χ² loop)")
    print("=" * 70)
    inv = [
        inventory_KR1(),
        inventory_W1(),
        inventory_KUW(),
        inventory_KA(),
    ]
    for item in inv:
        print(f"\n### {item['fork']}")
        for k in [
            "EL",
            "solution",
            "far",
            "A_to_0_finite_r",
            "ceiling_sphere_size",
            "hard_barrier_ell",
            "z_max_outward",
            "dL_character",
            "notes",
        ]:
            if k in item:
                print(f"  {k}: {item[k]}")

    print("\n### Shape classes (readout)")
    for k, v in shape_classes().items():
        print(f"  {k}: {v}")

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY — who does what (vacuum)")
    print("=" * 70)
    print(
        """
  Redshift outward (looking out):
    K-R1 yes (finite z_max) | W=1 yes (finite z_max) | K-UW toward horizon yes | K-A outward to flat no cosmic z

  A→0 at finite r (infinite redshift wall):
    K-R1 no | W=1 no | K-UW yes (horizon) | K-A yes (Schw rs)

  Outer cosmic sphere ceiling (r grows, then A→0 at large r as max sphere):
    NONE in pure vacuum inventory
    → filled/sourced geometry required for Charles-style outer ceiling (prior KA matter)

  Linear Hubble at regular center under full light + D_A=r:
    forbidden by series theorem if phi~r^2
    vacuum Coulomb singular at 0

  Implication (solver-first):
    vacuum simple-metric space does NOT produce filled outer sphere-ceiling cosmologies
    next S2: sourced solutions with named continuum — observe who develops A→0 at finite r
"""
    )

    out = {
        "inventories": inv,
        "shape_classes": shape_classes(),
        "implication": "vacuum lacks outer sphere ceiling; sourced S2 next",
        "pre_registered": "no chi2 in solve loop; full light readout only",
    }
    path = ROOT / "simple_metric_S1_vacuum_space_out.json"
    # make JSON serializable
    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return float(o)
        if isinstance(o, (np.bool_, bool)):
            return bool(o)
        if o is None or isinstance(o, (str, int)):
            return o
        return str(o)

    path.write_text(json.dumps(clean(out), indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
