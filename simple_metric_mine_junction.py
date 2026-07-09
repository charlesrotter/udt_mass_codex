#!/usr/bin/env python3
"""
GR mine: Israel junction on reciprocal simple metric.
Interior continuum tiles vs exterior Schwarzschild vacuum.

Re-run: python3 simple_metric_mine_junction.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    r, R, rs, X, c, p = sp.symbols("r R rs X c p", positive=True)
    out = {"fallout": []}

    print("=" * 70)
    print("Mine: junction reciprocal interior | Schw exterior")
    print("=" * 70)

    # --- A continuity => mass continuity ---
    A_m = 1 - r / X
    A_p = 1 - rs / r
    cont = sp.simplify(A_m.subs(r, R) - A_p.subs(r, R))
    rs_match = sp.solve(cont, rs)[0]
    print("\n[1] A continuity for ceiling interior:", cont, "=> rs =", rs_match)
    out["rs_from_A_cont_ceiling"] = str(rs_match)
    out["fallout"].append("A continuous ⇔ MS mass continuous")

    # --- Israel jumps with A cont ---
    A0 = sp.simplify(A_m.subs(r, R).subs(rs, rs_match))
    dAm = sp.diff(A_m, r).subs(r, R)
    dAp = sp.diff(A_p, r).subs(r, R).subs(rs, rs_match)
    jump_Ktt = sp.simplify((dAp - dAm) / (2 * sp.sqrt(A0)))
    # S^t_t = 0, S^θ_θ = jump_Ktt / (8π)
    Sth = sp.simplify(jump_Ktt / (8 * sp.pi))
    print("[2] Thin shell (A cont): S^t_t=0, S^θ_θ =", Sth)
    print("    A0 =", A0, " dA-/dr =", dAm, " dA+/dr =", dAp)
    out["S_theta_ceiling_shell"] = str(Sth)
    out["fallout"].append("A cont + A' jump ⇒ σ=0, anisotropic S^θ_θ")

    # --- C1 match power family impossible ---
    print("\n[3] C^1 match A=1-c r^p to Schw")
    # rs = c R^{p+1}, A' match: -c p R^{p-1} = c R^{p-1} => p=-1
    out["C1_power_to_Schw"] = "impossible for p>0 (A' sign)"
    out["fallout"].append(
        "power-lapse ceiling family A' < 0 cannot C1-match Schw A' > 0"
    )
    print("  impossible for p>0 (interior A'<0, exterior A'>0)")

    # --- general A cont shell ---
    A0s, dAm_s, dAp_s = sp.symbols("A0 dAm dAp", positive=True)
    Sth_g = sp.simplify((dAp_s - dAm_s) / (16 * sp.pi * sp.sqrt(A0s)))
    print("\n[4] General A-cont shell S^θ_θ =", Sth_g)
    out["S_theta_general"] = str(Sth_g)

    # --- rooms ---
    out["rooms"] = {
        "star_like": "A increases to surface; can match Schw exterior",
        "filled_cosmos_ceiling": "A→0 at finite X; global wall; not C1 star",
        "thin_shell": "legal; not adopted as UDT edge ontology",
    }
    for k, v in out["rooms"].items():
        print(f"  room {k}: {v}")

    # limit R -> X
    print("\n[5] Shell stress as R→X:", sp.limit(Sth, R, X))
    out["shell_at_wall"] = "diverges as A→0"

    out["verdict"] = (
        "Junction mine: ceiling tiles ≠ star interiors for Schw exterior; "
        "thin shell possible but anisotropic; filled cosmos is separate room."
    )
    print("\n" + out["verdict"])
    path = ROOT / "simple_metric_mine_junction_out.json"
    path.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {path.name}")
    print("DONE")


if __name__ == "__main__":
    main()
