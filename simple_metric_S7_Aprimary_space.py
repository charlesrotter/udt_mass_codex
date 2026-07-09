#!/usr/bin/env python3
"""
S7 — A-primary (R1 EL) solution-space census (OBSERVE only).

Compensated R1 + dilated dust L_m = -ρ r² e^{-2φ}:
  Z (r² φ')' = 2 ρ r² e^{-2φ}
  ⇔  ρ_EL = Z (r² φ')' / (2 r² e^{-2φ})

Also uncompensated vacuum: Z (r² φ')' = 4 e^{-2φ}

Observe:
  (1) free φ families → ρ_EL required (symbolic)
  (2) ρ_EL vs Einstein ρ_E on same φ (joint residual character)
  (3) numeric integrate EL for free prescribed ρ → what φ, A, walls emerge
  (4) uncompensated vacuum character

No profile shopping. No χ². No mechanism to glue E and A.

Re-run: python3 simple_metric_S7_Aprimary_space.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent


def main():
    out = {"mode": "OBSERVE", "free_phi_tiles": [], "numeric_EL": [], "notes": []}
    r, Z, a, b, k, X, q = sp.symbols("r Z a b k X q", positive=True)

    print("=" * 70)
    print("S7 A-primary R1 EL solution space — observe only")
    print("=" * 70)

    def rho_EL(phiexpr, Zval=1):
        phip = sp.diff(phiexpr, r)
        LHS = sp.diff(r**2 * phip, r)
        return sp.simplify(Zval * LHS / (2 * r**2 * sp.exp(-2 * phiexpr)))

    def rho_E(phiexpr):
        A = sp.exp(-2 * phiexpr)
        Ap = sp.diff(A, r)
        return sp.simplify((1 - A - r * Ap) / (8 * sp.pi * r**2))

    # ----- (1) free φ tiles -----
    print("\n[1] Free φ → ρ_EL (compensated R1+dust), vs ρ_E")
    families = [
        ("const", a + 0 * r),
        ("coulomb", a - q / r),
        ("linear_phi", a + b * r),
        ("quad_phi", a + b * r**2),
        ("log_phi", a + b * sp.log(r)),
        ("E_ceiling_phi", -sp.Rational(1, 2) * sp.log(1 - r / X)),
        ("schw_phi", -sp.Rational(1, 2) * sp.log(1 - k / r)),
    ]
    for name, ph in families:
        rEL = rho_EL(ph, 1)
        rE = rho_E(ph)
        A = sp.simplify(sp.exp(-2 * ph))
        ratio = sp.simplify(rE / rEL) if rEL != 0 else "rEL=0"
        tile = {
            "name": name,
            "phi": str(ph),
            "A": str(A),
            "rho_EL": str(rEL),
            "rho_E": str(rE),
            "rho_E_over_rho_EL": str(ratio),
            "joint": str(ratio) == "1",
        }
        # wall: A→0
        try:
            zeros = sp.solve(sp.Eq(A, 0), r)
            tile["A_zeros"] = [str(z) for z in zeros]
        except Exception:
            tile["A_zeros"] = []
        out["free_phi_tiles"].append(tile)
        print(f"  {name}:")
        print(f"    ρ_EL = {rEL}")
        print(f"    ρ_E  = {rE}")
        print(f"    ρ_E/ρ_EL = {ratio}")
        print(f"    A zeros: {tile.get('A_zeros')}")

    # ----- (2) uncompensated vacuum -----
    print("\n[2] Uncompensated vacuum Z(r²φ')' = 4 e^{-2φ}")
    # try known: series / exact
    # Let u = e^{-2φ}, then φ' = -u'/(2u), (r²φ')' = d/dr(-r² u'/(2u))
    # Z d/dr(-r² u'/(2u)) = 4 u
    u = sp.Function("u")
    # Known from SIMPLE_METRIC_MACRO: not always closed form.
    # Numeric later; symbolic check coulomb fails:
    ph_c = a - q / r
    LHS = sp.simplify(sp.diff(r**2 * sp.diff(ph_c, r), r))
    RHS = sp.simplify(4 * sp.exp(-2 * ph_c))
    print("  Coulomb LHS", LHS, "RHS", RHS, "equal?", sp.simplify(LHS - RHS) == 0)
    out["uncomp_coulomb_is_sol"] = bool(sp.simplify(LHS - RHS) == 0)

    # power series u = u0 + u1 r + u2 r^2 + ... for uncomp vacuum
    # Or integrate numeric uncomp vacuum with BC
    print("  Numeric uncompensated vacuum BC φ(0)=0, φ'(0)=s small")

    def uncomp_ode(r, y, Zval=1.0):
        # y = [φ, π] with π = φ';  π' from Z (r² π)' = 4 e^{-2φ}
        # Z (2 r π + r² π') = 4 e^{-2φ}
        phi, pi = y
        if r < 1e-8:
            return [pi, 0.0]
        # π' = (4 e^{-2φ}/Z - 2 r π) / r²
        pp = (4 * np.exp(-2 * phi) / Zval - 2 * r * pi) / (r**2)
        return [pi, pp]

    uncomp_runs = []
    for s in [0.0, 0.01, 0.05, 0.1]:
        # start at r_eps with φ≈0, φ'≈s; for s=0 flat is NOT solution of uncomp
        re = 1e-3
        sol = solve_ivp(
            lambda rr, y: uncomp_ode(rr, y, 1.0),
            (re, 2.0),
            [0.0 + s * re, s],  # φ(re)≈s re if linear
            dense_output=False,
            max_step=0.01,
            rtol=1e-6,
            atol=1e-8,
        )
        if not sol.success:
            uncomp_runs.append({"s": s, "ok": False})
            continue
        phi = sol.y[0]
        A = np.exp(-2 * phi)
        imin = int(np.argmin(A))
        uncomp_runs.append(
            {
                "s": s,
                "ok": True,
                "A_min": float(np.min(A)),
                "A_end": float(A[-1]),
                "phi_end": float(phi[-1]),
                "r_end": float(sol.t[-1]),
                "A_min_r": float(sol.t[imin]),
            }
        )
        print(
            f"    s={s}: A_min={np.min(A):.4g} at r~{sol.t[imin]:.3g}, "
            f"A_end={A[-1]:.4g}"
        )
    out["uncomp_vacuum_numeric"] = uncomp_runs

    # ----- (3) numeric compensated EL with free prescribed ρ -----
    print("\n[3] Compensated EL with prescribed free ρ (integrate φ)")
    # Z (r² φ')' = 2 ρ r² e^{-2φ}
    # y=[φ,π], π=φ'
    # Z (2r π + r² π') = 2 ρ r² e^{-2φ}
    # π' = (2 ρ r² e^{-2φ}/Z - 2 r π) / r² = 2ρ e^{-2φ}/Z - 2π/r

    def comp_ode(r, y, rho_fn, Zval=1.0):
        phi, pi = y
        if r < 1e-8:
            return [pi, 0.0]
        pp = 2 * rho_fn(r) * np.exp(-2 * phi) / Zval - 2 * pi / r
        return [pi, pp]

    rho_cases = {
        "const_0.05": lambda r: 0.05,
        "const_0.2": lambda r: 0.2,
        "rho_1_r": lambda r: 0.05 / max(r, 1e-6),
        "rho_r": lambda r: 0.05 * r,
        "gauss": lambda r: 0.5 * np.exp(-(r**2) / 0.25),
    }

    for name, rfn in rho_cases.items():
        re = 1e-3
        # regular center: φ(0)=0, φ'(0)=0
        sol = solve_ivp(
            lambda rr, y: comp_ode(rr, y, rfn, 1.0),
            (re, 3.0),
            [0.0, 0.0],
            max_step=0.005,
            rtol=1e-7,
            atol=1e-9,
            dense_output=False,
        )
        rec = {"name": name, "ok": bool(sol.success)}
        if sol.success and len(sol.t) > 5:
            phi = sol.y[0]
            A = np.exp(-2 * phi)
            edge = None
            for i, Ai in enumerate(A):
                if Ai <= 1e-8:
                    edge = float(sol.t[i])
                    break
            rec.update(
                {
                    "A_min": float(np.min(A)),
                    "A_end": float(A[-1]),
                    "phi_end": float(phi[-1]),
                    "edge": edge,
                    "phi_max": float(np.max(phi)),
                }
            )
            # Einstein ρ at a mid point vs prescribed
            i = len(sol.t) // 3
            ri = sol.t[i]
            # numerical A'
            Ap = np.gradient(A, sol.t)
            rhoE = (1 - A[i] - ri * Ap[i]) / (8 * np.pi * ri**2)
            rhoA = rfn(ri)
            rec["rho_prescribed_mid"] = float(rhoA)
            rec["rho_E_mid"] = float(rhoE)
            rec["ratio_E_over_prescribed_mid"] = (
                float(rhoE / rhoA) if abs(rhoA) > 1e-30 else None
            )
        out["numeric_EL"].append(rec)
        print(
            f"  {name}: A_min={rec.get('A_min')} edge={rec.get('edge')} "
            f"ρE/ρ_pres mid={rec.get('ratio_E_over_prescribed_mid')}"
        )

    # ----- (4) structure notes -----
    notes = [
        "A-primary compensated: vacuum ⇒ Coulomb φ; ρ_EL=0. Einstein vacuum Schw is different φ.",
        "Free φ defines ρ_EL; that ρ_EL almost never equals Einstein ρ_E (joint thin).",
        "E-ceiling φ requires ρ_EL ≠ ρ_E (known residual) — not an A-primary solution for Einstein density.",
        "Numeric EL with free ρ + regular BC φ=φ'=0: φ grows, A=e^{-2φ} drops but may not hit geometric MS wall the same way — characterize A_min, not force A=0.",
        "Uncompensated vacuum sources e^{-2φ} self-coupling — different branch from compensated.",
        "No unique continuum selected; A-primary and E-primary remain two maps of 'matter + simple metric'.",
    ]
    print("\n[4] Structure")
    for n in notes:
        print("  •", n)
        out["notes"].append(n)

    out["verdict"] = (
        "A-primary space: vacuum Coulomb; free φ ⇒ ρ_EL catalog; "
        "prescribed-ρ EL numerics yield φ with A=e^{-2φ} declining; "
        "ρ_E ≠ ρ_prescribed in general — routes stay split. No winner, no glue."
    )
    print("\n" + out["verdict"])

    def san(o):
        if isinstance(o, dict):
            return {str(k): san(v) for k, v in o.items()}
        if isinstance(o, list):
            return [san(v) for v in o]
        if isinstance(o, (float, np.floating)):
            x = float(o)
            if np.isnan(x) or np.isinf(x):
                return str(x)
            return x
        if isinstance(o, (int, np.integer)):
            return int(o)
        if isinstance(o, (bool, str)) or o is None:
            return o
        return str(o)

    path = ROOT / "simple_metric_S7_Aprimary_space_out.json"
    path.write_text(json.dumps(san(out), indent=2))
    print(f"Wrote {path.name}")
    print("DONE")
    return out


if __name__ == "__main__":
    main()
