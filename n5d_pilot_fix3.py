"""n5d_pilot_fix3.py -- FIX-3 structured-seed / continuation-repair diagnostic pilot.

Goal: avoid the stalled near-homogeneous state (contributor 3 of the conditioning diagnosis) by
STARTING from a structured round Branch-P base solution with nontrivial rho'/phi', then injecting
small ell=2 shear and continuing amplitude 0->target.  FIX-1 equilibration/lstsq stays ACTIVE.

NOT a verdict run: bounded diagnostic attempts, no pin-vs-continuum read, no Outcome A/B.
UNCHANGED: equations, BCs, source, readouts, residual, seal conditions.  No S-JC2 gauge pin.
Only the SEED and the continuation warm-start are new (both CHOSE/category-A).

Structured seed (mirror-BC-respecting): phi,rho get a cos(pi(zeta+1)/2) bump -- zero slope at BOTH
ends (satisfies the phi'=rho'=0 mirror BC exactly) with nonzero INTERIOR gradient.  STAGE-A relaxes
(phi,rho,uf,L) through the BASE f2d system (sealbc='off' => a2 pinned 0) to a self-consistent round
Branch-P base.  STAGE-B injects a2=1e-3 and runs the frozen-source shear continuation, both seal BCs.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import json, time, argparse
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev

import cell_solver_f2d as cs
import n5d_pilot as pilot

PRM = pilot.PRM
Nr, Nth = 16, 8


def structured_seed(ctx, phi_amp=0.15, rho_amp=0.08, rho0=0.70710678, L0=1.0, uf_amp=0.02, a2_amp=0.0):
    """Base seed with NONTRIVIAL phi'/rho' interior structure (mirror-BC-safe cos bump) + optional a2."""
    Nr_, Nth_ = ctx["Nr"], ctx["Nth"]
    zeta = ctx["zeta"]; mu = ctx["mu"]
    g = torch.cos(np.pi * (zeta + 1.0) / 2.0)                 # g'(zeta)=0 at both ends; nonzero interior
    phi = phi_amp * g                                          # structured phi (range +phi_amp..-phi_amp)
    rho = rho0 + rho_amp * g                                   # structured rho (>0)
    uf = uf_amp * (1.0 - mu[None, :] ** 2) * torch.cos(np.pi * (zeta + 1.0) / 2.0)[:, None]
    a2 = a2_amp * g
    return cs.pack(phi, rho, uf, float(L0), a2=a2)


def struct_metrics(u, ctx, n5d):
    with torch.no_grad():
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        phip = Q["phip"].cpu().numpy(); rhop = Q["rhop"].cpu().numpy()
        phi = Q["phi"].cpu().numpy(); rho = Q["rho"].cpu().numpy()
    return dict(max_abs_phip=float(np.abs(phip).max()), max_abs_rhop=float(np.abs(rhop).max()),
               phi_range=[float(phi.min()), float(phi.max())],
               rho_range=[float(rho.min()), float(rho.max())])


def eff_cond(u, ctx, n5d):
    """raw cond(J) and the column-scaled cond FIX-1's lstsq effectively faces."""
    J = jacrev(lambda uu: cs.residual(uu, ctx, PRM, n5d=n5d))(u).detach()
    S = torch.linalg.svdvals(J).cpu().numpy()
    dc = cs._col_scale(J); Jc = J * dc[None, :]
    Sc = torch.linalg.svdvals(Jc).cpu().numpy()
    return float(S[0] / S[-1]), float(Sc[0] / Sc[-1])


def run(budget_per_bc=100.0, maxit=30, skip_stageA=False):
    st, source_rc, source_sh2 = pilot.load_frozen_source()
    if st.get("blocker"):
        print("BLOCKER:", st["blocker"]); return
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)

    if skip_stageA:
        # DIRECT structured seed for the coupled continuation at L0=1.0 (matched to the pilot's L0);
        # no pre-flatten -- isolates 'structured phi/rho seed' vs the pilot's flat seed at same L0.
        print("=== DIRECT MODE: coupled shear continuation seeded from STRUCTURED phi/rho at L0=1.0 ===")
        u_base = structured_seed(ctx, a2_amp=0.0, L0=1.0)
        L0 = 1.0
        mS = struct_metrics(u_base, ctx, dict(sealbc="off"))
        print(f"  structured seed: max|phi'|={mS['max_abs_phip']:.3e}  max|rho'|={mS['max_abs_rhop']:.3e}  "
              f"(vs pilot flat seed max|rho'|~2e-1 collapsing to ~3e-3)  L0={L0}")
    else:
        # ---------- STAGE A: relax the structured seed through the BASE system (a2 pinned off) ------
        print("=== STAGE A: structured Branch-P base relaxation (sealbc='off', a2 pinned 0, FIX-1 on) ===")
        u = structured_seed(ctx, a2_amp=0.0)
        n5d_off = dict(sealbc="off")
        m0 = struct_metrics(u, ctx, n5d_off)
        print(f"  structured SEED: max|phi'|={m0['max_abs_phip']:.3e}  max|rho'|={m0['max_abs_rhop']:.3e}  "
              f"phi_range={m0['phi_range']}  rho_range={m0['rho_range']}")
        t0 = time.time()
        u, histA = cs.newton_lm_solve(u, ctx, PRM, maxit=maxit, tol=pilot.PHI_TOL,
                                      verbose=False, time_budget=budget_per_bc, n5d=n5d_off, equilibrate=True)
        mA = struct_metrics(u, ctx, n5d_off)
        HrA = cs.H_of_r(u, ctx, PRM).cpu().numpy()
        print(f"  STAGE-A relaxed: finalPhi={histA[-1]:.4e} ({len(histA)-1} it, {time.time()-t0:.1f}s)  "
              f"max|phi'|={mA['max_abs_phip']:.3e}  max|rho'|={mA['max_abs_rhop']:.3e}")
        print(f"  STAGE-A base: H_seal={HrA[-1]:+.4e}  phi_range={mA['phi_range']}  rho_range={mA['rho_range']}")
        u_base = u.detach().clone()
        L0 = float(cs.unpack(u_base, ctx, n5d=True)[-1])
        print(f"  STAGE-A structured base has nontrivial gradients: "
              f"{'YES' if mA['max_abs_rhop']>1e-2 and mA['max_abs_phip']>1e-4 else 'NO (flattened)'}  (L0={L0:.4f})")

    # ---------- STAGE B: inject a2=1e-3 and run the frozen-source shear continuation, both BCs -------
    results = {}
    for sealbc in ("S-Dir", "S-JC2"):
        print(f"\n=== STAGE B [{sealbc}]: inject a2=1e-3 on the structured base, continue amp 0->1 ===")
        # structured shear seed on the base (keep phi,rho,uf,L; set a2 block)
        phi, rho, uf, a2, L = cs.unpack(u_base, ctx, n5d=True)
        g = torch.cos(np.pi * (ctx["zeta"] + 1.0) / 2.0)
        a2_seed = pilot.A2_SEED * g
        u = cs.pack(phi, rho, uf, float(L), a2=a2_seed)
        t0 = time.time(); finalPhi = float("nan")
        for amp in pilot.CONT_AMPS:
            rem = budget_per_bc - (time.time() - t0)
            if rem <= 1.0:
                break
            Tshear = pilot.build_Tshear(ctx, L0, amp, source_rc, source_sh2)
            n5d = dict(sealbc=sealbc, Tshear=Tshear, a2_mirror=0.0)
            u, hist = cs.newton_lm_solve(u, ctx, PRM, maxit=maxit, tol=pilot.PHI_TOL,
                                         verbose=False, time_budget=rem, n5d=n5d, equilibrate=True)
            finalPhi = hist[-1]
        n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, pilot.CONT_AMPS[-1],
                                                            source_rc, source_sh2), a2_mirror=0.0)
        diag = pilot.final_diagnostics(u, ctx, n5d)
        craw, ceff = eff_cond(u, ctx, n5d)
        conv = bool(finalPhi < 1e-8)
        m = struct_metrics(u, ctx, n5d)
        results[sealbc] = dict(finalPhi=finalPhi, converged=conv, craw=craw, ceff=ceff, diag=diag,
                               max_abs_phip=m["max_abs_phip"], max_abs_rhop=m["max_abs_rhop"])
        print(f"  finalPhi={finalPhi:.4e}  converged={conv}  raw_cond={craw:.3e}  eff_cond={ceff:.3e}")
        print(f"  q_raw={diag['q_raw']:.4e}  Pi_phi={diag['Pi_phi']:.4e}  M_readout={diag['M_readout']:.4e}")
        print(f"  H_seal={diag['H_seal']:+.4e}  Derrick_res={diag['derrick_residual']:+.3e}  "
              f"a2_peak={diag['a2_peak_abs']:.4e}")
        print(f"  phi_nodes={diag['phi_node_count']}  turning_pts={diag['reduced_source_turning_points']}  "
              f"max|phi'|={m['max_abs_phip']:.3e}  max|rho'|={m['max_abs_rhop']:.3e}")

    # ---------- comparison vs the stalled-state pilot (Outcome D) ----------
    print("\n=== COMPARISON: FIX-3 structured seed  vs  stalled-state pilot (Outcome D) ===")
    stalled = {"S-Dir": dict(finalPhi=8.10e-5, craw=4.175e15, a2_peak=5.140e-3, H_seal=-5.578e-3,
                             max_abs_rhop=3.13e-3, turns=1),
               "S-JC2": dict(finalPhi=4.10e-4, craw=9.203e16, a2_peak=1.911e-5, H_seal=-6.376e-3,
                             max_abs_rhop=1.60e-3, turns=3)}
    for bc in ("S-Dir", "S-JC2"):
        r = results[bc]; s = stalled[bc]
        print(f"  [{bc}] finalPhi {s['finalPhi']:.2e} -> {r['finalPhi']:.2e} | "
              f"raw_cond {s['craw']:.2e} -> {r['craw']:.2e} | "
              f"max|rho'| {s['max_abs_rhop']:.2e} -> {r['max_abs_rhop']:.2e} | "
              f"H_seal {s['H_seal']:+.2e} -> {r['diag']['H_seal']:+.2e}")
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=100.0)
    ap.add_argument("--maxit", type=int, default=30)
    ap.add_argument("--skip-stageA", action="store_true", dest="skip_stageA",
                    help="direct structured seed for the coupled continuation at L0=1.0 (matched to pilot)")
    args = ap.parse_args()
    assert Nr <= 24, "anti-hang"
    run(budget_per_bc=args.budget, maxit=args.maxit, skip_stageA=args.skip_stageA)
