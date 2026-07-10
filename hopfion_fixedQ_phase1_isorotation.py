#!/usr/bin/env python3
"""Phase 1 pilot: stationary isorotation on flat FS (L2+L4).

Ansatz: n(T,x) = R_z(ω T) n(x)  (target-space rotation about ê_z).
Noether charge Q = ω I[n]; effective energy at fixed Q:
  E_Q[n] = E_static[n] + Q² / (2 I[n])
with I = moment of inertia for ê_z isorotation (L2 + L4 time-space).

Object: Q_H≈1 hopfion sector (toroidal seed / optional restart).
Bounded anti-hang: modest N, capped steps, single process.

Usage:
  python3 hopfion_fixedQ_phase1_isorotation.py
  python3 hopfion_fixedQ_phase1_isorotation.py --N 48 --steps 80 --Q 0,0.5,1
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch

# import banked FS infrastructure
sys.path.insert(0, str(Path(__file__).resolve().parent / "hopfion_arc_scripts_2026-07-05"))
import fs_hopfion as m  # noqa: E402

torch.set_default_dtype(torch.float64)
DEV = m.dev


def cross(a, b):
    return torch.stack(
        [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ],
        0,
    )


def inertia_z(n, h, xi, kappa):
    """Moment of inertia for target-space rotation about ê_z.

    ∂_t n = ω ê_z × n = ω (-n_y, n_x, 0)
    |∂_t n|² / ω² = n_x² + n_y² = 1 - n_z²

    L2: I2 = ∫ ξ (1-n_z²) dV
    L4: Ω_0i = n · (∂_t n × ∂_i n) = ω n · ((ê_z×n) × ∂_i n)
         I4 from (κ/2) sum_i Ω_0i² / ω²  (matches Skyrme time-space weight used in FS literature)
    """
    n = n / n.norm(dim=0, keepdim=True)
    dn = m.grads(n, h)
    dV = h**3
    # L2
    sin2 = (n[0] * n[0] + n[1] * n[1]).clamp(min=0.0)
    I2 = (xi * sin2).sum() * dV
    # ê_z × n
    ez_x_n = torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)
    # Ω_0i / ω = n · (ez_x_n × ∂_i n)
    I4 = torch.zeros((), device=n.device, dtype=n.dtype)
    for i in range(3):
        omi = (n * cross(ez_x_n, dn[i])).sum(0)
        I4 = I4 + 0.5 * kappa * (omi * omi).sum() * dV
    return I2 + I4, I2, I4


def energy_static(n, h, xi, kappa):
    E, E2, E4, n_u, _ = m.energy(n, h, xi, kappa)
    return E, E2, E4, n_u


def E_Q_of(n, h, xi, kappa, Q):
    E, E2, E4, n_u = energy_static(n, h, xi, kappa)
    I, I2, I4 = inertia_z(n_u, h, xi, kappa)
    I_safe = I.clamp(min=1e-30)
    EQ = E + (Q * Q) / (2.0 * I_safe)
    return EQ, E, E2, E4, I, I2, I4, n_u


@torch.no_grad()
def project_tangent(n, g):
    """Project gradient to T_n S²: remove radial component."""
    n = n / n.norm(dim=0, keepdim=True)
    return g - (g * n).sum(0, keepdim=True) * n


def pin_inf(n, n_inf, w=2):
    n = n.clone()
    n[:, :w, :, :] = n_inf
    n[:, -w:, :, :] = n_inf
    n[:, :, :w, :] = n_inf
    n[:, :, -w:, :] = n_inf
    n[:, :, :, :w] = n_inf
    n[:, :, :, -w:] = n_inf
    return n / n.norm(dim=0, keepdim=True)


def relax_fixed_Q(n0, h, xi, kappa, Q, steps, dt, n_inf, log_every=20):
    """Arrested gradient flow on E_Q = E + Q²/(2I)."""
    n = n0.detach().clone().requires_grad_(True)
    hist = []
    for s in range(steps):
        EQ, E, E2, E4, I, I2, I4, n_u = E_Q_of(n, h, xi, kappa, Q)
        # autograd of EQ w.r.t n
        if n.grad is not None:
            n.grad.zero_()
        EQ.backward()
        g = project_tangent(n.detach(), n.grad.detach())
        with torch.no_grad():
            n_new = n.detach() - dt * g
            n_new = n_new / n_new.norm(dim=0, keepdim=True)
            n_new = pin_inf(n_new, n_inf)
            n = n_new.requires_grad_(True)
        if s % log_every == 0 or s == steps - 1:
            row = {
                "step": s,
                "EQ": float(EQ.detach().cpu()),
                "E": float(E.detach().cpu()),
                "E2": float(E2.detach().cpu()),
                "E4": float(E4.detach().cpu()),
                "I": float(I.detach().cpu()),
                "I2": float(I2.detach().cpu()),
                "I4": float(I4.detach().cpu()),
                "omega": float((Q / max(float(I.detach().cpu()), 1e-30))),
            }
            hist.append(row)
            print(
                f"Q={Q:g} step={s:4d} EQ={row['EQ']:.4f} E={row['E']:.4f} "
                f"E2/E4={row['E2']/max(row['E4'],1e-30):.4f} I={row['I']:.4f} ω={row['omega']:.4e}",
                flush=True,
            )
    # final hopf charge with correct N,L
    return n.detach(), hist


def hopf_charge_fixed(n, h, N, L):
    return m.hopf_charge(n, h, N, L)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=48)
    ap.add_argument("--L", type=float, default=5.0)
    ap.add_argument("--xi", type=float, default=1.0)
    ap.add_argument("--kappa", type=float, default=1.0)
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--dt", type=float, default=0.02)
    ap.add_argument("--Q", type=str, default="0,0.5,1.0")
    ap.add_argument("--seed", type=str, default="tor", choices=["tor", "hopf"])
    ap.add_argument("--ssize", type=float, default=1.2)
    ap.add_argument("--static_pre", type=int, default=40, help="static (Q=0) warm steps before Q>0")
    args = ap.parse_args()

    N, L = args.N, args.L
    X, Y, Z, h = m.make_grid(N, L)
    n_inf = torch.tensor([0.0, 0.0, -1.0], device=DEV).view(3, 1, 1, 1)

    if args.seed == "tor":
        n0 = m.toroidal_seed(X, Y, Z, args.ssize, 0.5 * args.ssize)
    else:
        n0 = m.hopf_seed(X, Y, Z, args.ssize)
    n0 = pin_inf(n0 / n0.norm(dim=0, keepdim=True), n_inf)

    Qs = [float(x) for x in args.Q.split(",") if x.strip() != ""]
    results = {
        "grade": "PHASE1_PILOT",
        "device": DEV,
        "N": N,
        "L": L,
        "h": h,
        "xi": args.xi,
        "kappa": args.kappa,
        "steps": args.steps,
        "dt": args.dt,
        "seed": args.seed,
        "ssize": args.ssize,
        "premise": {
            "I": "isorotation about target ê_z",
            "E_Q": "E_static + Q^2/(2I)",
            "metric": "flat FS (Phase 1) — no backreaction",
            "object": "Q_H~1 sector seed; not f2d hedgehog",
        },
        "runs": [],
    }

    # warm start at Q=0
    print(f"[phase1] device={DEV} N={N} L={L} static_pre={args.static_pre}", flush=True)
    n, hist0 = relax_fixed_Q(
        n0, h, args.xi, args.kappa, 0.0, args.static_pre, args.dt, n_inf, log_every=max(1, args.static_pre // 4)
    )
    q0 = hopf_charge_fixed(n, h, N, L)
    print(f"[phase1] after static_pre |Q_H|={abs(q0):.4f}", flush=True)

    n_cur = n
    for Q in Qs:
        n_cur, hist = relax_fixed_Q(
            n_cur, h, args.xi, args.kappa, Q, args.steps, args.dt, n_inf, log_every=max(1, args.steps // 5)
        )
        qh = hopf_charge_fixed(n_cur, h, N, L)
        last = hist[-1]
        last["Q_H"] = qh
        last["Q_charge"] = Q
        last["held_topology"] = abs(qh) > 0.5  # coarse pilot threshold
        results["runs"].append({"Q": Q, "final": last, "history_tail": hist[-3:]})
        print(f"[phase1] Q={Q} done |Q_H|={abs(qh):.4f} EQ={last['EQ']:.4f} I={last['I']:.4f}", flush=True)

    out = Path("hopfion_fixedQ_phase1_isorotation_out.json")
    # json-safe
    def conv(o):
        if isinstance(o, dict):
            return {k: conv(v) for k, v in o.items()}
        if isinstance(o, list):
            return [conv(v) for v in o]
        if isinstance(o, (float, int, str, bool)) or o is None:
            return o
        return float(o)

    out.write_text(json.dumps(conv(results), indent=2))
    print("wrote", out, flush=True)


if __name__ == "__main__":
    main()
