#!/usr/bin/env python3
"""
S9 — Native action honesty CAS (re-runnable).

Classifies bulk pieces on the simple metric: shift weight, EL for φ, EH≡0.
No SNe. No package glue.

Re-run: python3 simple_metric_S9_native_action_honesty.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    r = sp.symbols("r", positive=True)
    phi = sp.Function("phi")
    ph = phi(r)
    phip = sp.diff(ph, r)
    phipp = sp.diff(ph, r, 2)
    c = sp.symbols("c")

    out = {"identities": {}, "EL": {}, "ledger": {}}

    print("=" * 70)
    print("S9 native action honesty")
    print("=" * 70)

    A = sp.exp(-2 * ph)
    R2 = 2 / r**2
    K = -2 * sp.exp(-2 * ph) / r**2
    out["identities"]["flat_R2_plus_K"] = str(sp.simplify((R2 + K).subs(ph, 0)))
    out["identities"]["compensated_cancel"] = str(sp.simplify(R2 + sp.exp(2 * ph) * K))

    print("[1] Angular flat / compensated")
    print("  R2+K at φ=0:", out["identities"]["flat_R2_plus_K"])
    print("  R2+e^{2φ}K:", out["identities"]["compensated_cancel"])

    def el(L):
        L = sp.simplify(L.doit())
        return sp.simplify(
            sp.diff(L, ph)
            - sp.diff(sp.diff(L, phip), r)
            + sp.diff(sp.diff(L, phipp), r, 2)
        )

    L_R1 = sp.Rational(1, 2) * r**2 * phip**2
    L_un = L_R1 - 2 * sp.exp(-2 * ph)
    Ap, App = sp.diff(A, r), sp.diff(A, r, 2)
    R4 = (-(r**2) * App - 4 * r * Ap - 2 * A + 2) / r**2
    L_EH = r**2 * R4

    print("\n[2] Vacuum EL for φ")
    for name, L in [
        ("R1", L_R1),
        ("R1_uncomp", L_un),
        ("EH_reduced", L_EH),
    ]:
        e = el(L)
        out["EL"][name] = str(e)
        print(f"  {name}: EL = {e}")
        print(f"    identically 0? {sp.simplify(e) == 0}")

    out["identities"]["EH_EL_identically_zero"] = bool(sp.simplify(el(L_EH)) == 0)
    out["identities"]["R1_EL_is_coulomb"] = " (r^2 phi')' = 0 "

    # shift
    print("\n[3] Shift weights φ→φ+c")
    kin = r**2 * phip**2
    print("  kinetic ratio:", sp.simplify(kin.subs(ph, ph + c) / kin))
    print("  K ratio:", sp.simplify(K.subs(ph, ph + c) / K))

    out["ledger"] = {
        "metric": "THEORY",
        "R1_kinetic": "shift-clean candidate",
        "W_on_K": "FORK",
        "Z": "FREE",
        "L_m": "CHOSE probe",
        "EH_on_ansatz_vary_phi": "EL≡0 — not a φ dynamics package",
        "E_primary": "G=8πT on ansatz (different problem type)",
        "A_primary": "R1 φ-variational",
        "native_package": "OPEN",
    }
    print("\n[4] Ledger")
    for k, v in out["ledger"].items():
        print(f"  {k}: {v}")

    out["verdict"] = (
        "EH reduced vary-φ is empty; R1 is true φ-variational; "
        "E-primary is Einstein-on-ansatz; native package OPEN."
    )
    print("\n" + out["verdict"])

    path = ROOT / "simple_metric_S9_native_action_honesty_out.json"
    path.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {path.name}")
    print("DONE")


if __name__ == "__main__":
    main()
