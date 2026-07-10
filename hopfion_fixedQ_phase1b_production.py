#!/usr/bin/env python3
"""Phase 1b: production arrested-Newton on E_Q from a resolved-ish H3 field.

1) Build/relax static hopfion with arrested-Newton + damped Derrick rescale (H3 production recipe).
2) Continue in fixed target charge Q with the SAME flow on E_Q = E + Q^2/(2I).
3) Halt if |Q_H| < Qmin (topology protection).

Usage (bounded example):
  python3 hopfion_fixedQ_phase1b_production.py --N 128 --L 6 --static_steps 250 --q_steps 120 \\
      --Q 0,0.5,1.0 --rescale_every 25 --dt 0.02
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch

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
    n = n / n.norm(dim=0, keepdim=True)
    dn = m.grads(n, h)
    dV = h**3
    sin2 = n[0] * n[0] + n[1] * n[1]
    I2 = (xi * sin2).sum() * dV
    ez_x_n = torch.stack([-n[1], n[0], torch.zeros_like(n[0])], 0)
    I4 = torch.zeros((), device=n.device, dtype=n.dtype)
    for i in range(3):
        omi = (n * cross(ez_x_n, dn[i])).sum(0)
        I4 = I4 + 0.5 * kappa * (omi * omi).sum() * dV
    return I2 + I4, I2, I4


def metrics(n, h, xi, kappa, N, L, Q):
    E, E2, E4, n_u, _ = m.energy(n, h, xi, kappa)
    I, I2, I4 = inertia_z(n_u, h, xi, kappa)
    Icl = float(I.clamp(min=1e-30).item())
    EQ = float(E.item()) + (Q * Q) / (2.0 * Icl)
    qh = abs(m.hopf_charge(n_u, h, N, L)[0])
    return {
        "EQ": EQ,
        "E": float(E.item()),
        "E2": float(E2.item()),
        "E4": float(E4.item()),
        "E2_over_E4": float(E2.item()) / max(float(E4.item()), 1e-30),
        "I": Icl,
        "I2": float(I2.item()),
        "I4": float(I4.item()),
        "omega": Q / Icl,
        "Q_H": qh,
    }


def make_rescale(N, device):
    base = torch.stack(
        torch.meshgrid(
            torch.linspace(-1, 1, N, device=device),
            torch.linspace(-1, 1, N, device=device),
            torch.linspace(-1, 1, N, device=device),
            indexing="ij",
        ),
        -1,
    )

    def rescale(n_raw, lam):
        with torch.no_grad():
            nn = (n_raw / n_raw.norm(dim=0, keepdim=True)).unsqueeze(0)
            g = (base / lam).flip(-1).unsqueeze(0)
            out = torch.nn.functional.grid_sample(
                nn, g, mode="bilinear", padding_mode="border", align_corners=True
            ).squeeze(0)
            out = out / out.norm(dim=0, keepdim=True)
            n_raw.copy_(out)
        return n_raw

    return rescale


def arrested_newton_EQ(
    nseed,
    h,
    xi,
    kappa,
    Q,
    N,
    L,
    steps,
    dt,
    n_inf,
    rescale_every=0,
    qmin=0.85,
    log_every=25,
    tag="run",
):
    """Arrested Newton on E_Q (Q=0 => pure static E)."""
    nr = nseed.clone().requires_grad_(True)
    v = torch.zeros_like(nseed)
    rescale = make_rescale(N, nseed.device)
    hist = []
    halted = None

    def tgrad():
        if nr.grad is not None:
            nr.grad.zero_()
        E, E2, E4, n_u, _ = m.energy(nr, h, xi, kappa)
        I, _, _ = inertia_z(n_u, h, xi, kappa)
        I_safe = I.clamp(min=1e-30)
        EQ = E + (Q * Q) / (2.0 * I_safe)
        EQ.backward()
        with torch.no_grad():
            nn = nr / nr.norm(dim=0, keepdim=True)
            g = nr.grad - (nr.grad * nn).sum(0, keepdim=True) * nn
        return g, float(EQ.item()), float(E.item()), float(E2.item()), float(E4.item()), float(I_safe.item())

    with torch.no_grad():
        Eprev = metrics(nr, h, xi, kappa, N, L, Q)["EQ"]
    narr = 0

    for s in range(1, steps + 1):
        g, EQ, E, E2, E4, Ival = tgrad()
        with torch.no_grad():
            v -= dt * g
            nn = nr / nr.norm(dim=0, keepdim=True)
            v = v - (v * nn).sum(0, keepdim=True) * nn
            nr += dt * v
            m.pin_boundary(nr, n_inf, 2)
            nr.div_(nr.norm(dim=0, keepdim=True))
            Enew = metrics(nr, h, xi, kappa, N, L, Q)["EQ"]
            if Enew > Eprev:
                v.zero_()
                narr += 1
            Eprev = Enew

        if rescale_every and s % rescale_every == 0 and E2 > 0 and E4 > 0 and abs(Q) < 1e-12:
            # Derrick rescale only at Q=0 (static virial); for Q>0 scale mode is modified
            lam_star = math.sqrt(E4 / E2)
            lam = min(1.18, max(0.85, lam_star**0.4))
            with torch.no_grad():
                rescale(nr, lam)
                m.pin_boundary(nr, n_inf, 2)
                nr.div_(nr.norm(dim=0, keepdim=True))
                v.zero_()
                Eprev = metrics(nr, h, xi, kappa, N, L, Q)["EQ"]

        if s % log_every == 0 or s == steps:
            with torch.no_grad():
                row = metrics(nr, h, xi, kappa, N, L, Q)
            row["step"] = s
            row["arrests"] = narr
            hist.append(row)
            print(
                f"[{tag} Q={Q:g}] s={s:4d} EQ={row['EQ']:.3f} E={row['E']:.3f} "
                f"E2/E4={row['E2_over_E4']:.4f} |Q_H|={row['Q_H']:.4f} I={row['I']:.3f} arr={narr}",
                flush=True,
            )
            if row["Q_H"] < qmin:
                halted = f"|Q_H|={row['Q_H']:.4f}<{qmin}"
                print(f"[{tag}] HALT topology: {halted}", flush=True)
                break

    with torch.no_grad():
        n_final = (nr / nr.norm(dim=0, keepdim=True)).detach()
        final = metrics(n_final, h, xi, kappa, N, L, Q)
    return n_final, hist, final, halted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=128)
    ap.add_argument("--L", type=float, default=6.0)
    ap.add_argument("--xi", type=float, default=1.0)
    ap.add_argument("--kappa", type=float, default=1.0)
    ap.add_argument("--static_steps", type=int, default=200)
    ap.add_argument("--q_steps", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.02)
    ap.add_argument("--Q", type=str, default="0,0.5,1.0")
    ap.add_argument("--seed", type=str, default="tor", choices=["tor", "hopf"])
    ap.add_argument("--ssize", type=float, default=1.25)
    ap.add_argument("--rescale_every", type=int, default=25)
    ap.add_argument("--qmin", type=float, default=0.85)
    ap.add_argument("--restart", type=str, default="", help="optional .npz with n,N,L")
    ap.add_argument("--save", type=str, default="hopfion_fixedQ_phase1b_field.npz")
    args = ap.parse_args()

    N, L = args.N, args.L
    X, Y, Z, h = m.make_grid(N, L)
    n_inf = torch.tensor([0.0, 0.0, -1.0], device=DEV).view(3, 1, 1, 1)

    if args.restart:
        dat = np.load(args.restart)
        nc = torch.tensor(dat["n"], device=DEV)
        Nc = int(dat["N"])
        Lc = float(dat["L"])
        xg = torch.linspace(-L, L, N, device=DEV)
        GX, GY, GZ = torch.meshgrid(xg, xg, xg, indexing="ij")
        grid = torch.stack([GZ / Lc, GY / Lc, GX / Lc], -1).unsqueeze(0)
        nc = torch.nn.functional.grid_sample(
            nc.unsqueeze(0), grid, mode="bilinear", padding_mode="border", align_corners=True
        ).squeeze(0)
        nseed = nc / nc.norm(dim=0, keepdim=True)
        print(f"[phase1b] restart {args.restart} N {Nc}->{N} L {Lc}->{L}", flush=True)
    elif args.seed == "tor":
        nseed = m.toroidal_seed(X, Y, Z, args.ssize, 0.5 * args.ssize)
    else:
        nseed = m.hopf_seed(X, Y, Z, args.ssize)
    nseed = nseed / nseed.norm(dim=0, keepdim=True)
    m.pin_boundary(nseed, n_inf, 2)

    Qs = [float(x) for x in args.Q.split(",") if x.strip() != ""]
    out = {
        "grade": "PHASE1B_PILOT",
        "device": DEV,
        "N": N,
        "L": L,
        "h": h,
        "xi": args.xi,
        "kappa": args.kappa,
        "static_steps": args.static_steps,
        "q_steps": args.q_steps,
        "dt": args.dt,
        "rescale_every": args.rescale_every,
        "qmin": args.qmin,
        "seed": args.seed if not args.restart else f"restart:{args.restart}",
        "runs": [],
    }

    print(
        f"[phase1b] device={DEV} N={N} L={L} h={h:.4f} static_steps={args.static_steps} "
        f"q_steps={args.q_steps} rescale_every={args.rescale_every}",
        flush=True,
    )

    # --- static build (Q=0) ---
    n, hist, final, halted = arrested_newton_EQ(
        nseed,
        h,
        args.xi,
        args.kappa,
        0.0,
        N,
        L,
        args.static_steps,
        args.dt,
        n_inf,
        rescale_every=args.rescale_every,
        qmin=args.qmin,
        log_every=max(1, args.static_steps // 8),
        tag="static",
    )
    out["runs"].append(
        {
            "Q": 0.0,
            "phase": "static_build",
            "final": final,
            "halted": halted,
            "hist_tail": hist[-4:],
            "held": final["Q_H"] >= args.qmin and final["E"] > 1.0,
        }
    )
    print(
        f"[phase1b] static done |Q_H|={final['Q_H']:.4f} E={final['E']:.3f} "
        f"E2/E4={final['E2_over_E4']:.4f} held={out['runs'][-1]['held']}",
        flush=True,
    )

    if not out["runs"][-1]["held"]:
        out["verdict"] = "STATIC_BUILD_FAILED_TOPOLOGY_OR_ENERGY"
        Path("hopfion_fixedQ_phase1b_production_out.json").write_text(json.dumps(out, indent=2))
        print("wrote hopfion_fixedQ_phase1b_production_out.json", flush=True)
        return

    # save static field for reuse
    np.savez(
        args.save.replace(".npz", "_Q0.npz"),
        n=n.cpu().numpy(),
        N=N,
        L=L,
        xi=args.xi,
        kappa=args.kappa,
        h=h,
        **{k: final[k] for k in final},
    )

    n_cur = n
    for Q in Qs:
        if abs(Q) < 1e-15:
            continue  # already have Q=0
        n_cur, hist, final, halted = arrested_newton_EQ(
            n_cur,
            h,
            args.xi,
            args.kappa,
            Q,
            N,
            L,
            args.q_steps,
            args.dt,
            n_inf,
            rescale_every=0,  # no pure Derrick at Q>0
            qmin=args.qmin,
            log_every=max(1, args.q_steps // 6),
            tag=f"Q{Q:g}",
        )
        held = final["Q_H"] >= args.qmin and final["E"] > 1.0 and halted is None
        out["runs"].append(
            {
                "Q": Q,
                "phase": "isorotation",
                "final": final,
                "halted": halted,
                "hist_tail": hist[-4:],
                "held": held,
            }
        )
        print(
            f"[phase1b] Q={Q} done |Q_H|={final['Q_H']:.4f} EQ={final['EQ']:.3f} "
            f"E2/E4={final['E2_over_E4']:.4f} ω={final['omega']:.4e} held={held}",
            flush=True,
        )
        if not held:
            out["verdict"] = f"HALTED_OR_LOST_TOPOLOGY_AT_Q={Q}"
            break
        np.savez(
            args.save.replace(".npz", f"_Q{Q:g}.npz"),
            n=n_cur.cpu().numpy(),
            N=N,
            L=L,
            Q=Q,
            **{k: final[k] for k in final},
        )
    else:
        out["verdict"] = "COMPLETED_CONTINUATION"
        # classify
        goods = [r for r in out["runs"] if r.get("held")]
        if len(goods) >= 2 and any(r["Q"] > 0 for r in goods):
            out["verdict"] = "PHASE1B_HOLDS_Q_CONTINUATION"
        elif goods:
            out["verdict"] = "STATIC_ONLY_HELD"

    Path("hopfion_fixedQ_phase1b_production_out.json").write_text(json.dumps(out, indent=2))
    print("verdict:", out["verdict"], flush=True)
    print("wrote hopfion_fixedQ_phase1b_production_out.json", flush=True)


if __name__ == "__main__":
    main()
