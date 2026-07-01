#!/usr/bin/env python3
"""
p5c_stability.py -- P5c-step-3 STABILITY TEST on ALL basins.

THE QUESTION (Charles, OBSERVE not target): are the multiple same-charge floored
solutions a FAMILY of genuinely STABLE distinct objects, or is the round one the
single particle with the others UNSTABLE saddles that decay to it?

METHOD (binding -- memory [[gravitating-soliton-stability-test]] / phase3b precedent):
  The FIXED-METRIC matter Hessian OVER-COUNTS instabilities for a gravitating soliton
  (off-constraint negative modes).  So per basin:
   (1) compute the fixed-metric body-Theta Hessian of the matter action -> negative modes
   (2) for each negative mode, perturb Theta along it (+/-amp) and do a CONSTRAINT-
       RESPECTING full coupled re-solve (newton_solve re-imposes Einstein + matter EL).
       A TRUE instability descends to LOWER energy / different field (saddle/unstable);
       an OFF-CONSTRAINT artifact returns to (~same) base energy (coupled-stable).
   (3) track WHERE the coupled descent lands (toward round, or a distinct config).
  m=1 ROUND = SIGN CALIBRATION: must come out n_neg=0 (coupled-stable).  If not, FIX
  the method before trusting the others.

REUSE the SAVED floored fields from p5c_basins.py at /tmp/p5c_basin_{NR}_{name}.pt
(NO re-solve from scratch).  The Hessian/eig around a saved solution needs NO re-solve;
only the constraint-respecting descent calls newton_solve (bounded).

ANTI-HANG (binding, #1): SINGLE clean process per invocation, SEQUENTIAL, never
concurrent.  This script does ONE basin per invocation.  Hessian eig is cheap
(recompute on saved field).  The coupled descent calls newton_solve with a bounded
maxit.  Nr<=16.  No background poll.

USAGE (one basin per process):
  python3 p5c_stability.py hess  NR NAME              # fixed-metric Hessian only (fast)
  python3 p5c_stability.py descend NR NAME [K] [MAXIT] # Hessian + coupled descent along
                                                        # top-K neg modes (bounded)
  python3 p5c_stability.py report NR                   # assemble the per-basin table
"""
import os, sys, time, json, glob
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")  # jacrev path
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import (Grid3D, attach_coord_weight, residuals, diagnostics,
    build_metric, field_dn, DEV)
from full3d_solver import residual_vector, unpack, pack
import whole_metric_3d_matter as MAT
import whole_metric_3d_core as CORE
import full3d_newton as NW

P, KAP8 = 0.4, 0.05


def make_grid(NR):
    NTH = 6 if NR == 12 else 8
    NPS = 8
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    return G


def load_basin(NR, name):
    fp = f"/tmp/p5c_basin_{NR}_{name}.pt"
    if not os.path.exists(fp):
        raise FileNotFoundError(fp)
    rec = torch.load(fp)
    return rec


def S_of_Th(G, g, ginv, Th, m=1):
    """Matter action S = int sqrt(-g) L dV_coord, for the FIXED metric (g,ginv).
       Same algebra as p5c_basins.energy_proxy / phase3b_hessian.S_of_Th."""
    dn = field_dn(G, Th, m=m)
    Gmn = MAT.field_metric(dn)
    L, _, _, _ = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    return (sqrtg * L * G.wvol_coord).sum()


def body_theta_idx(G):
    """Free-Theta DOF = interior radial shells [1:-1] (the residual pins Th[0]=m*pi and
       Th[-1]=0 via BC rows; those are NOT free).  All theta,psi at interior r are free.
       (We do NOT use the [3:Nr-3] diagnostic body mask here -- the residual's free DOF
       are [1:-1]; the Cheb edge rows are still solved-for in the coupled system.)"""
    mask = torch.zeros(G.Nr, G.Nth, G.Nps, dtype=torch.bool, device=DEV)
    mask[1:-1, :, :] = True
    return mask.reshape(-1).nonzero().squeeze(1)


def fixed_metric_hessian(G, u, m=1, tol_frac=1e-6):
    """Energy Hessian H_E = -H_S of the matter action over the free body-Theta DOF, at
       the FIXED floored metric.  Returns sorted eigs + the negative-mode eigenvectors
       (full-grid-shaped) for the descent step."""
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d).detach()
    ginv = CORE.metric_inverse(g).detach()
    Th0 = Th.detach().clone().requires_grad_(True)
    f = lambda x: S_of_Th(G, g, ginv, x, m)
    n = G.Nr * G.Nth * G.Nps
    H_S = torch.autograd.functional.hessian(f, Th0).reshape(n, n)
    H_E = -0.5 * (H_S + H_S.t())               # energy Hessian, symmetrized
    bidx = body_theta_idx(G)
    HB = H_E[bidx][:, bidx]
    evals, evecs = torch.linalg.eigh(HB)
    scale = max(float(evals.abs().max()), 1e-30)
    tol = tol_frac * scale
    n_neg = int((evals < -tol).sum().item())
    n_zero = int((evals.abs() <= tol).sum().item())
    return dict(evals=evals.cpu().numpy(), evecs=evecs, bidx=bidx, n=n,
                scale=scale, tol=tol, n_neg=n_neg, n_zero=n_zero)


def neg_eigvec_fields(G, hess, k):
    """Return up to k full-grid-shaped negative-mode eigenvector fields (most negative
       first)."""
    evals, evecs, bidx, n = hess['evals'], hess['evecs'], hess['bidx'], hess['n']
    out = []
    for j in range(min(k, len(evals))):
        if evals[j] >= -hess['tol']:
            break
        v = torch.zeros(n, device=DEV)
        v[bidx] = evecs[:, j]
        out.append((float(evals[j]), v.reshape(G.Nr, G.Nth, G.Nps)))
    return out


def base_diag(G, u):
    out = residuals(G, unpack(u, G), P, KAP8); d = diagnostics(G, out, KAP8)
    return d


def field_dist(u1, u2):
    return float((u1 - u2).abs().max())


# ============================================================================
def cmd_hess(NR, name):
    G = make_grid(NR)
    rec = load_basin(NR, name)
    u = rec['u'].to(DEV)
    d = base_diag(G, u)
    F = residual_vector(u, G, P, KAP8); Phi = float((F*F).sum())
    hess = fixed_metric_hessian(G, u)
    ev = hess['evals']
    print(f"[hess {NR} {name}] basePhi={Phi:.2e} M_MS={d['M_MS']:.5f} "
          f"psivar={d['psivar']:.3e}", flush=True)
    print(f"  lowest8 eig = {np.round(ev[:8],4)}", flush=True)
    print(f"  RAW fixed-metric: n_neg={hess['n_neg']}  n_zero={hess['n_zero']}  "
          f"scale={hess['scale']:.2e} tol={hess['tol']:.2e}", flush=True)
    rec_out = dict(NR=NR, name=name, basePhi=Phi, M_MS=d['M_MS'], psivar=d['psivar'],
                   lowest8=[float(x) for x in ev[:8]], raw_n_neg=hess['n_neg'],
                   n_zero=hess['n_zero'], scale=hess['scale'], tol=hess['tol'])
    json.dump(rec_out, open(f"/tmp/p5c_stab_hess_{NR}_{name}.json", "w"), indent=1)


def cmd_descend(NR, name, K, maxit):
    G = make_grid(NR)
    rec = load_basin(NR, name)
    u = rec['u'].to(DEV)
    a, b, c, d_, Th = unpack(u, G)
    dg0 = base_diag(G, u)
    Mbase = dg0['M_MS']
    # energy proxy (matter action) at the FULL metric, base
    g0 = build_metric(G, a, b, c, d_); ginv0 = CORE.metric_inverse(g0)
    Sbase = float(S_of_Th(G, g0, ginv0, Th).detach())
    F0 = residual_vector(u, G, P, KAP8); Phi0 = float((F0*F0).sum())
    print(f"[descend {NR} {name}] BASE M_MS={Mbase:.5f} S={Sbase:.4e} "
          f"psivar={dg0['psivar']:.3e} Phi={Phi0:.2e}", flush=True)
    hess = fixed_metric_hessian(G, u)
    print(f"  RAW fixed-metric n_neg={hess['n_neg']} (tol {hess['tol']:.1e}); "
          f"lowest8={np.round(hess['evals'][:8],4)}", flush=True)
    vecs = neg_eigvec_fields(G, hess, K)
    if not vecs:
        print(f"  no negative fixed-metric modes -> nothing to descend; "
              f"raw n_neg=0 => CR n_neg=0 STABLE", flush=True)
    # round reference field (for "where does it head" tracking)
    try:
        u_round = load_basin(NR, 'round')['u'].to(DEV)
    except Exception:
        u_round = None
    dist_to_round_base = field_dist(u, u_round) if u_round is not None else None

    results = []
    cr_neg = 0
    best = (Sbase, Mbase, None, "base")
    for j, (ev, vfield) in enumerate(vecs):
        sc = float(vfield.abs().max()) + 1e-30
        for amp in (0.25, -0.25):
            Th2 = Th + (amp / sc) * vfield
            useed = pack(a.clone(), b.clone(), c.clone(), d_.clone(), Th2)
            t0 = time.time()
            ur, hr = NW.newton_solve(useed, G, P, KAP8, m=1, maxit=maxit,
                                     lam0=1e-4, tol=1e-12, verbose=False)
            Phir = hr[-1]
            dgr = base_diag(G, ur)
            ar, br, cr, drr, Thr = unpack(ur, G)
            gr = build_metric(G, ar, br, cr, drr); ginvr = CORE.metric_inverse(gr)
            Sr = float(S_of_Th(G, gr, ginvr, Thr).detach())
            dM = dgr['M_MS'] - Mbase
            dS = Sr - Sbase
            d_to_base = field_dist(ur, u)
            d_to_round = field_dist(ur, u_round) if u_round is not None else None
            # CLASSIFY this direction.  Energy (matter action S) is the selection proxy.
            # genuine descent => S DROPS (more negative) by > a tol; off-constraint => ~same/up
            floored = Phir < 1e-9
            if not floored:
                tag = "UNDERFLOORED"
            elif dS < -1e-2 * max(abs(Sbase), 1.0):
                tag = "DESCEND(lower S)"; cr_neg += 1
            elif abs(dS) <= 1e-2 * max(abs(Sbase), 1.0):
                tag = "~same (off-constraint)"
            else:
                tag = "uphill (off-constraint)"
            # where did it head?
            head = ""
            if d_to_round is not None:
                if d_to_round < 0.05:
                    head = "->ROUND"
                elif d_to_base < 0.05:
                    head = "stay(base)"
                else:
                    head = f"d_round={d_to_round:.2f} d_base={d_to_base:.2f}"
            print(f"  ev{j}({ev:.3f}) amp={amp:+.2f}: M={dgr['M_MS']:.5f} dM={dM:+.3e} "
                  f"S={Sr:.4e} dS={dS:+.3e} psivar={dgr['psivar']:.3e} "
                  f"Phi={Phir:.1e}  {tag}  {head}", flush=True)
            results.append(dict(evec=j, ev=ev, amp=amp, M=dgr['M_MS'], dM=dM,
                                S=Sr, dS=dS, psivar=dgr['psivar'], Phi=Phir,
                                floored=floored, tag=tag, d_to_base=d_to_base,
                                d_to_round=d_to_round, wall=time.time()-t0))
            if floored and Sr < best[0] - 1e-2 * max(abs(Sbase), 1.0):
                best = (Sr, dgr['M_MS'], ur.detach().cpu(),
                        f"ev{j} amp{amp:+.2f}")
    # CONSTRAINT-RESPECTING verdict
    if not vecs:
        cr_n_neg = 0
        classification = "STABLE"
    else:
        cr_n_neg = cr_neg
        if cr_neg == 0:
            classification = "STABLE (all neg modes off-constraint)"
        else:
            classification = f"SADDLE/UNSTABLE ({cr_neg} CR-descending directions)"
    print(f"[descend {NR} {name}] RAW n_neg={hess['n_neg']} -> "
          f"CONSTRAINT-RESPECTING n_neg={cr_n_neg}  => {classification}", flush=True)
    print(f"  best S found={best[0]:.4e} (base {Sbase:.4e}) via {best[3]}", flush=True)
    rec_out = dict(NR=NR, name=name, Mbase=Mbase, Sbase=Sbase, basePhi=Phi0,
                   raw_n_neg=hess['n_neg'], cr_n_neg=cr_n_neg,
                   classification=classification, dist_to_round_base=dist_to_round_base,
                   results=results, best_S=best[0], best_M=best[1], best_via=best[3],
                   lowest8=[float(x) for x in hess['evals'][:8]])
    json.dump(rec_out, open(f"/tmp/p5c_stab_descend_{NR}_{name}.json", "w"), indent=1)
    if best[2] is not None:
        torch.save(best[2], f"/tmp/p5c_stab_descended_{NR}_{name}.pt")


def cmd_report(NR):
    print(f"\n=== P5c-step-3 STABILITY TABLE  Nr={NR} ===", flush=True)
    hdr = ("basin", "M_MS", "Sbase", "raw n_neg", "CR n_neg", "classification")
    print("  " + " | ".join(str(h) for h in hdr), flush=True)
    for nm in ['round', 'oblate', 'pert_s', 'prolate', 'toroidal']:
        fp = f"/tmp/p5c_stab_descend_{NR}_{nm}.json"
        if not os.path.exists(fp):
            print(f"  {nm}: (no descend record)", flush=True); continue
        r = json.load(open(fp))
        print(f"  {nm:>9} | {r['Mbase']:.5f} | {r['Sbase']:.3e} | "
              f"{r['raw_n_neg']:>3} | {r['cr_n_neg']:>3} | {r['classification']}",
              flush=True)
        # where did descents head
        heads = [f"ev{x['evec']}{x['amp']:+.2f}->dS={x['dS']:+.2e} "
                 f"d_round={x['d_to_round']}" for x in r['results']
                 if x['tag'].startswith('DESCEND')]
        if heads:
            for h in heads:
                print(f"        DESCEND: {h}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; NR = int(sys.argv[2])
    t0 = time.time()
    if mode == 'hess':
        cmd_hess(NR, sys.argv[3])
    elif mode == 'descend':
        name = sys.argv[3]
        K = int(sys.argv[4]) if len(sys.argv) > 4 else 3
        maxit = int(sys.argv[5]) if len(sys.argv) > 5 else 25
        cmd_descend(NR, name, K, maxit)
    elif mode == 'report':
        cmd_report(NR)
    print(f"=== DONE ({mode} {NR} {sys.argv[3] if len(sys.argv)>3 else ''}) "
          f"{time.time()-t0:.0f}s ===", flush=True)
