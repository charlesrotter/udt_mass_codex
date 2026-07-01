#!/usr/bin/env python3
"""Caveat #3 of the kap8 characterization: OFF-DIAGONALS-OFF control on native-S2 matter.

Isolates the off-diagonal DOF effect. The off-ON native-S2 run gave a MILD diagonal warp-trend
(Nr=8 -> 1.022, Nr=10 -> 1.181, x1.16) vs the OLD diagonal-only+S3 run's x2.12. TWO things changed
at once (off-diagonals completed AND matter S3->S2), so the milder trend is CONFOUNDED. This control
changes EXACTLY ONE variable: re-solve the SAME 11-field / 7-Einstein-row / native-S2 / Branch-G /
kap8=1 system but FREEZE e_rt=e_rp=e_tp=0 (mask their Newton update). Compare the diagonal warp.
  off-OFF warp ~ off-ON warp  => off-diagonals barely matter; the S3->S2 matter swap tamed it
                                 -> the "it was the frozen off-diagonal DOF" cure-story FALSIFIED.
  off-OFF warp >> off-ON warp => the off-diagonals DID tame it -> story supported.
NOTE: with e_* frozen, the rth Einstein row cannot floor (it needed e_rt=0.11); the ACTIVE rows
(tt,rr,thth,psps,elphi,elN) still floor. Warp = max|a,b,c,d| from the constrained solve.

CHOSE-OR-DERIVED (physics premises this rides):
  branch='G'  FREE (the silent G/P fork; matches the off-ON comparison run)
  kap8=1      THEORY (derived strong coupling)
  X=-2e5      FREE (Cassini-bounded placeholder; matches off-ON)
  xi=kap=1    THEORY baseline ; matter = native-S2 winding (seed homotopy class)
CATEGORY-A conditioning (soundness, not derivation): Nr, Nth=6, Nps=8, maxit, lam, X-ladder.

Run MYSELF, bounded, single process, NO nohup, output->file.  MODE A = warm-start from the saved
converged off-ON Nr=8 field (cheap, minutes).  MODE B (--cold Nr) = full cold X-continuation (~hrs).
"""
import os, sys, time, math
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D

KAP8, BRANCH, XTGT = 1.0, "G", -2.0e5


def offdiag_mask(G):
    """1 for active DOF, 0 for the 3 off-diagonal blocks e_rt,e_rp,e_tp (blocks 8,9,10 of 11)."""
    n = G.Nr * G.Nth * G.Nps
    m = torch.ones(11 * n, device=G.dev)
    m[8 * n:11 * n] = 0.0
    return m


def warp_of(u, G):
    a, b, c, d = P1.unpack11(u, G)[:4]
    return max(float(x.abs().max()) for x in (a, b, c, d))


def newton_masked(u, G, X, mask, maxit=40, lam0=1e-4, tol=1e-11, lam_min=1e-14, verbose=True):
    u = u.detach().clone(); lam = lam0
    F = P1.residual_vector_p1(u, G, 1.0, KAP8, X=X, branch=BRANCH)
    Phi = float((F * F).sum()); nU = u.numel(); I = torch.eye(nU, device=u.device)
    for it in range(maxit):
        if Phi < tol:
            break
        J, F = P1.jacobian_p1(u, G, 1.0, KAP8, X=X, branch=BRANCH)
        accepted = False
        for _try in range(12):
            try:
                Jaug = torch.cat([J, math.sqrt(lam) * I], dim=0)
                Faug = torch.cat([-F, torch.zeros(nU, device=u.device)], dim=0)
                du = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            du = du * mask                                   # FREEZE off-diagonal DOF
            un = u + du
            Pn = float((P1.residual_vector_p1(un, G, 1.0, KAP8, X=X, branch=BRANCH) ** 2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam * 0.25, lam_min); accepted = True; break
            lam *= 4.0
        if verbose:
            print(f"    [masked-newton] it={it:3d} Phi={Phi:.4e} warp={warp_of(u,G):.4f} "
                  f"lam={lam:.1e} {'acc' if accepted else 'STALL'}", flush=True)
        if not accepted:
            break
    return u.detach(), Phi


def report(u, G, tag, X):
    cr = P1.component_residuals_p1(u, G, 1.0, KAP8, X=X, branch=BRANCH)
    active = max(cr[k] for k in ('tt', 'rr', 'thth', 'psps', 'elphi', 'elN'))
    print(f"  [{tag}] warp={warp_of(u,G):.4f}  ACTIVE-rows-resid(max)={active:.2e}  "
          f"rth(frozen)={cr['rth']:.2e}  eoff_max={cr['eoff_max']:.2e}  phi_max={cr['phi_max']:.4f}",
          flush=True)
    return warp_of(u, G)


def run_warm(Nr=8):
    """MODE A: warm-start from the saved off-ON converged field, mask off-diagonals, re-floor."""
    t0 = time.time()
    G = attach_coord_weight(Grid3D(Nr=Nr, Nth=6, Nps=8, rc=0.1, cell=8.0))
    mask = offdiag_mask(G)
    d = torch.load(f'solved_fields_nr{Nr}_G_kap8_1.pt', map_location='cpu', weights_only=False)
    u_on = d['u'].to(G.dev); Xfin = float(d['Xfin'])
    print(f"=== off-ON saved field (Nr={Nr}, Xfin={Xfin:.2e}) ===", flush=True)
    report(u_on, G, "off-ON", Xfin)
    # zero the off-diagonals, then re-floor the active DOF with the mask on
    a, b, c, dd, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u_on, G)
    z = torch.zeros_like(ert)
    u0 = P1.pack11(a, b, c, dd, n1, n2, n3, phi, z, z, z)
    print(f"=== re-floor with e_*=0 FROZEN (warm start) ===", flush=True)
    u_off, Phi = newton_masked(u0, G, Xfin, mask, maxit=15)
    w = report(u_off, G, "off-OFF", Xfin)
    torch.save({'u': u_off.cpu(), 'Xfin': Xfin, 'Nr': Nr, 'branch': BRANCH, 'kap8': KAP8,
                'control': 'offdiag_OFF_warm'}, f'control_offdiagOFF_nr{Nr}_G_kap8_1.pt')
    print(f"\nWARP COMPARISON (Nr={Nr}): off-ON={warp_of(u_on,G):.4f}  off-OFF={w:.4f}  "
          f"ratio={w/warp_of(u_on,G):.3f}   (t={time.time()-t0:.0f}s)", flush=True)


def continuation_masked(u0, G, mask, X_target=XTGT, X_start=-1.0, n_steps=20, maxit=15, verbose=True):
    """COLD X-ladder with off-diagonals frozen. Fixed fine geometric ladder, warm-start each step
    (no floor-based subdivision -- the frozen system cannot floor, so a floor criterion would loop
    forever). NaN-abort guard. Reports warp+Phi at every step so tracking is visible."""
    logs = list(-np.geomspace(abs(X_start), abs(X_target), n_steps))
    u = u0; last = None
    for i, X in enumerate(logs):
        u, Phi = newton_masked(u, G, float(X), mask, maxit=maxit, verbose=False)
        w = warp_of(u, G)
        if verbose:
            print(f"  [Xcont-masked] step {i+1:2d}/{len(logs)} X={float(X):.3e} Phi={Phi:.3e} "
                  f"warp={w:.4f}", flush=True)
        if not np.isfinite(Phi) or not np.isfinite(w):
            print(f"  [Xcont-masked] NON-FINITE at step {i+1} -- ABORT", flush=True); break
        last = (float(X), Phi, w)
    return u, last[0] if last else float(logs[-1]), last


def run_cold(Nr, n_steps=20, maxit=15):
    """MODE B: full COLD frozen-off X-continuation from the round-native seed."""
    t0 = time.time()
    G = attach_coord_weight(Grid3D(Nr=Nr, Nth=6, Nps=8, rc=0.1, cell=8.0))
    mask = offdiag_mask(G)
    u0 = P1.seed_round_native(G, p=1.0, m=1)
    print(f"=== COLD frozen-off (e_*=0): Nr={Nr} branch={BRANCH} kap8={KAP8} X->-2e5 ===", flush=True)
    report(u0, G, "seed", -1.0)
    u, Xfin, last = continuation_masked(u0, G, mask, n_steps=n_steps, maxit=maxit)
    w = report(u, G, "off-OFF-cold", Xfin)
    torch.save({'u': u.cpu(), 'Xfin': Xfin, 'Nr': Nr, 'branch': BRANCH, 'kap8': KAP8,
                'control': 'offdiag_OFF_cold'}, f'control_offdiagOFF_cold_nr{Nr}_G_kap8_1.pt')
    print(f"=== off-OFF-cold warp(Nr={Nr}) = {w:.4f}   (Xfin={Xfin:.2e}, t={time.time()-t0:.0f}s) ===\n",
          flush=True)
    return w


if __name__ == '__main__':
    if '--cold' in sys.argv:
        # clean matched trend: cold Nr=8 then cold Nr=10, single process, sequential
        nrs = [int(x) for x in sys.argv[sys.argv.index('--cold') + 1].split(',')] \
            if sys.argv.index('--cold') + 1 < len(sys.argv) and ',' in sys.argv[sys.argv.index('--cold') + 1] \
            else [8, 10]
        warps = {}
        for Nr in nrs:
            warps[Nr] = run_cold(Nr)
        print("================ CAVEAT #3 TREND COMPARISON ================", flush=True)
        print(f"  off-ON (live off-diag):  Nr=8 warp=1.022 -> Nr=10 warp=1.181   (x1.16)", flush=True)
        on = {8: 1.022, 10: 1.181}
        line = "  off-OFF (frozen, cold):  " + " -> ".join(f"Nr={k} warp={warps[k]:.3f}" for k in nrs)
        if len(nrs) >= 2:
            ks = sorted(nrs); line += f"   (x{warps[ks[-1]]/warps[ks[0]]:.2f})"
        print(line, flush=True)
        print("  Mild off-OFF trend (~x1.1, near off-ON) => off-diagonals IRRELEVANT to the warp;", flush=True)
        print("    the S3->S2 matter swap (not off-diag completion) tamed the divergence.", flush=True)
        print("  Steep off-OFF trend (~x2)            => off-diagonals DID tame it.", flush=True)
    else:
        Nr = int(sys.argv[sys.argv.index('--nr') + 1]) if '--nr' in sys.argv else 8
        run_warm(Nr)
