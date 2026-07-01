#!/usr/bin/env python3
"""
winding_catalog_map.py -- MAP the topological winding-soliton sectors m=1,2,3,4 of
the UDT coupled Einstein+L2+L4 static metric.  OBSERVE mode.  DATA-BLIND (L=1).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.

WHAT IT DOES (one tile):
  For each winding m in {1,2,3,4}:
    1. SEED  = radial soliton solved AT winding m (spectral_radial_soliton.solve(m=m)),
       which produces a Theta(r) that winds m*pi -> 0, broadcast to the 3-D grid (c=d=0).
       This is a TOPOLOGICALLY-PROTECTED seed: an m=2 config cannot relax to m=1 because
       the Theta winding BC (core=m*pi, seal=0) is hard-pinned in the residual (wbc rows).
    2. CONVERGE the FULL 3-D coupled residual (full3d_newton.newton_solve), B=1/A FREE,
       all five fields (a,b,c,d,Th) free, angular Einstein eqns imposed.
    3. REPORT: converged Phi, M_MS (Misner-Sharp), shape (tvar radial-angular, psivar
       non-axisym witness), per-component residuals (confirm angular Einstein satisfied).
    4. STABILITY PROBE (honest, stated):
       (a) matter-action second variation E''(eps) along controlled mode shapes added to
           Theta (at the converged metric): an OBLATE axisym P2(cos th) mode, and several
           psi-BREAKING modes cos(k*psi)*sin(th)  for k=1,2.  Negative E'' => downhill
           => a negative mode; if the softest negative is psi-breaking => a non-axisym
           (platonic) ground state likely exists in that sector.  This is the LEADING
           matter-sector stability indicator (the metric responds adiabatically); it does
           NOT include the full coupled gravitational second variation -- stated honestly.
       (b) RELAX TEST: add a finite psi-breaking deformation to Theta, RE-SOLVE the full
           coupled residual, and see whether the psi-structure DECAYS (relaxes back to
           axisym -> axisym is stable) or GROWS/persists with lower M_MS (-> off-axisym
           member).  This is the topologically-honest companion to (a).

Category-A only: the residual physics is imported verbatim; no B=1/A tie, no injected
term, no tuning to a target.  The winding BC is the topological charge, not a patch.
"""
import os, sys, time, json
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    matter_action, residuals, diagnostics, field_dn, matter_el_3d,
    DEV, PI, T, R, TH, PS)
import whole_metric_3d_core as CORE
import whole_metric_3d_matter as MAT
import full3d_solver as FS
from full3d_solver import pack, unpack
import full3d_newton as NEW
import spectral_radial_soliton as SR


def _E(G, f):
    return torch.tensor(f, device=DEV)[:, None, None].expand(
        G.Nr, G.Nth, G.Nps).contiguous()


def analytic_winding_seed(G, m, p=0.4):
    """Smooth analytic seed: Theta winds m*pi (core) -> 0 (seal) via a cos ramp;
    b a linear depth ramp -p (core) -> 0 (seal); a = -b (round-ish); c=d=0.
    A topologically-correct starting point for the full3d Newton solve when the
    radial LM (spectral_radial_soliton) cannot converge the steep m>=2 profile."""
    r = G.r.cpu().numpy(); rc, ri = G.rc, G.ri
    x = (r - rc) / (ri - rc)                 # 0..1
    Th = m*PI * 0.5*(1.0 + np.cos(PI*x))     # m*pi at core, 0 at seal, smooth
    b = -p * (1.0 - x)                       # -p at core, 0 at seal
    a = -b
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
    return pack(_E(G, a), _E(G, b), z.clone(), z.clone(), _E(G, Th)), None


def winding_seed(G, m, p=0.4, kap8=0.05):
    """Radial soliton solved AT winding m, broadcast to 3-D (c=d=0).  Falls back to
    the analytic winding seed if the radial LM does not converge (NaN/large F).
    Returns (u0, radial_sol_or_None)."""
    try:
        sol = SR.solve(G.Nr-1, rc=G.rc, cell=G.ri-G.rc, p=p, kap8=kap8, m=m,
                       maxit=120, tol=1e-12)
        if (not np.isfinite(sol['M_MS'])) or (sol['Fnorm'] > 1e-4) \
           or (not np.all(np.isfinite(sol['Th']))):
            raise RuntimeError(f"radial LM did not converge (M={sol['M_MS']}, "
                               f"F={sol['Fnorm']})")
        assert np.allclose(G.r.cpu().numpy(), sol['r']), "radial node mismatch"
        z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
        u = pack(_E(G, sol['a']), _E(G, sol['b']), z.clone(), z.clone(),
                 _E(G, sol['Th']))
        return u, sol
    except Exception as e:
        print(f"  [seed] m={m}: radial seed unavailable ({e}); using analytic seed")
        return analytic_winding_seed(G, m, p=p)


def full_diag(u, G, p, kap8, m):
    """M_MS + shape + per-component residuals via the INDEPENDENT committed path."""
    a, b, c, d, Th = unpack(u, G)
    out = residuals(G, (a, b, c, d, Th), p, kap8, m=m)
    dg = diagnostics(G, out, kap8)
    comp = NEW.component_residuals(u, G, p, kap8, m=m)
    return dg, comp


def _matter_action_scalar(G, g, ginv, Th, m):
    """Self-contained matter action S = int sqrt(-g) L dV (L = L2+L4).  We do NOT
    use full3d_spectral.matter_action because that helper's return statement
    references an undefined name (`n`) and raises -- so we duplicate the (small)
    scalar assembly here from the committed primitives MAT.field_metric/lagrangian.
    Value-identical to the action whose autograd is the committed matter EL.

    SIGN NOTE: L2,L4 < 0 for spacelike gradients, so S < 0; the static matter
    ENERGY E = -S.  Hence a downhill (negative-mode) direction in ENERGY appears
    as a POSITIVE curvature of S (S'' > 0).  We report S'' and interpret with the
    m=1 round soliton as the sign calibrator + the (sign-free) relax test as arbiter."""
    dn = field_dn(G, Th, m=m)
    Gmn = MAT.field_metric(dn)
    L, L2, L4, SS = MAT.lagrangian(ginv, Gmn, 1.0, 1.0)
    sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
    S = (sqrtg * L * G.wvol_coord).sum()
    return S


def matter_energy(G, u, m):
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d)
    ginv = CORE.metric_inverse(g)
    return float(_matter_action_scalar(G, g, ginv, Th, m=m))


def mode_shapes(G):
    """Controlled perturbation profiles for Theta (radial bump * angular shape),
    vanishing at core and seal so the winding BC is untouched."""
    r = G.Rg; sth = G.STHg; cth = torch.cos(G.THg); ps = G.PSg
    rc, ri = G.rc, G.ri
    # radial envelope vanishing at both ends (so Theta core/seal BC preserved)
    env = torch.sin(PI * (r - rc) / (ri - rc))
    P2 = 0.5*(3*cth**2 - 1.0)                 # axisym oblate (l=2,m=0)
    modes = {
        'oblate_P2':   env * P2,
        'psi_cos1':    env * sth * torch.cos(ps),       # psi-breaking k=1
        'psi_cos2':    env * sth * torch.cos(2*ps),     # psi-breaking k=2
        'psi_sin1':    env * sth * torch.sin(ps),
    }
    return modes


def secondvar_probe(G, u, m, amps=(-0.04, -0.02, 0.02, 0.04)):
    """matter-action second variation along each controlled mode (metric fixed at u).
    Returns dict mode -> (E0, curvature E'' estimate, list of (amp,dE)).
    E'' < 0 along a mode => that mode is a downhill (negative) direction."""
    a, b, c, d, Th = unpack(u, G)
    g = build_metric(G, a, b, c, d)
    ginv = CORE.metric_inverse(g)
    S0 = float(_matter_action_scalar(G, g, ginv, Th, m=m))
    out = {}
    for nm, sh in mode_shapes(G).items():
        rec = []
        for eps in amps:
            Th_p = Th + eps*sh
            Sp = float(_matter_action_scalar(G, g, ginv, Th_p, m=m))
            rec.append((eps, Sp - S0))
        # symmetric 2nd-derivative estimate from the two smallest |amp|
        e1 = amps[1]; e2 = amps[2]  # -0.02, +0.02 (symmetric)
        dEm = dict(rec)[e1]; dEp = dict(rec)[e2]
        d2 = (dEp + dEm) / (e2*e2)   # ~ E''(0) (since e2=-e1 in magnitude)
        out[nm] = dict(E0=S0, curv=d2, samples=rec)
    return out


def relax_test(G, u, m, p, kap8, amp=0.06, maxit=25):
    """Add a finite psi-breaking (cos(2psi)) deformation to Theta, re-solve the FULL
    coupled residual, and report whether the psi-structure decays (-> axisym stable)
    or persists/grows (-> off-axisym member).  Returns (psivar_before, psivar_after,
    M_before, M_after, Phi_after)."""
    a, b, c, d, Th = unpack(u, G)
    sh = mode_shapes(G)['psi_cos2']
    Th2 = Th + amp*sh
    u_seed = pack(a, b, c, d, Th2)
    dg0, _ = full_diag(u, G, p, kap8, m)
    # measure injected psivar
    dg_seed, _ = full_diag(u_seed, G, p, kap8, m)
    u_re, hist = NEW.newton_solve(u_seed, G, p, kap8, m=m, maxit=maxit,
                                  tol=1e-11, verbose=False)
    dg1, comp1 = full_diag(u_re, G, p, kap8, m)
    return dict(psivar_round=dg0['psivar'], psivar_seed=dg_seed['psivar'],
                psivar_relaxed=dg1['psivar'], M_round=dg0['M_MS'],
                M_relaxed=dg1['M_MS'], Phi_after=hist[-1])


def run_sector(G, m, p=0.4, kap8=0.05, do_relax=True, verbose=True, maxit=40,
               relax_maxit=18):
    t0 = time.time()
    u0, rsol = winding_seed(G, m, p=p, kap8=kap8)
    Phi0 = float((NEW.residual_vector_vsafe(u0, G, p, kap8, m=m)**2).sum())
    u, hist = NEW.newton_solve(u0, G, p, kap8, m=m, maxit=maxit, tol=1e-11,
                               lam0=1e-4, verbose=verbose)
    Phi = hist[-1]
    dg, comp = full_diag(u, G, p, kap8, m)
    # B=1/A freedom witness
    a, b, c, d, Th = unpack(u, G)
    maxB1A = float((a + b)[G.body].abs().max())
    sv = secondvar_probe(G, u, m)
    rec = dict(m=m, Phi0=Phi0, Phi=Phi, niter=len(hist)-1,
               M_MS=dg['M_MS'], tvar=dg['tvar'], psivar=dg['psivar'],
               maxB1A=maxB1A, comp=comp, secondvar=sv,
               M_radial_seed=(rsol['M_MS'] if rsol is not None else float('nan')),
               seed_kind=('radial' if rsol is not None else 'analytic'),
               t=time.time()-t0)
    if do_relax:
        try:
            rec['relax'] = relax_test(G, u, m, p, kap8, maxit=relax_maxit)
        except Exception as e:
            rec['relax'] = {'error': repr(e)}
    return rec, u


def fmt_sector(rec):
    L = []
    L.append(f"=== m={rec['m']} === ({rec['t']:.0f}s, {rec['niter']} it, "
             f"seed={rec.get('seed_kind','?')})")
    L.append(f"  Phi: {rec['Phi0']:.3e} -> {rec['Phi']:.3e}   "
             f"M_MS={rec['M_MS']:.6f}  (radial-seed M={rec['M_radial_seed']:.6f})")
    L.append(f"  shape: tvar(rad-ang)={rec['tvar']:.4e}  psivar(non-axisym)={rec['psivar']:.4e}")
    L.append(f"  B=1/A freedom maxB1A={rec['maxB1A']:.3e}")
    c = rec['comp']
    L.append(f"  res: tt={c['tt']:.2e} rr={c['rr']:.2e} thth={c['thth']:.2e} "
             f"psps={c['psps']:.2e} rth={c['rth']:.2e} el={c['el']:.2e}")
    L.append(f"  2nd-var (matter action E'' along modes; <0 = downhill):")
    for nm, d in rec['secondvar'].items():
        flag = "  <-- NEGATIVE" if d['curv'] < 0 else ""
        L.append(f"     {nm:12s} E''={d['curv']:+.4e}{flag}")
    if 'relax' in rec:
        r = rec['relax']
        if 'error' in r:
            L.append(f"  relax-test: ERROR {r['error']}")
        else:
            L.append(f"  relax-test (psi_cos2 amp injected, re-solved):")
            L.append(f"     psivar round={r['psivar_round']:.3e} seed={r['psivar_seed']:.3e} "
                     f"relaxed={r['psivar_relaxed']:.3e}  Phi_after={r['Phi_after']:.2e}")
            L.append(f"     M_MS round={r['M_round']:.6f} relaxed={r['M_relaxed']:.6f}")
    return "\n".join(L)


if __name__ == "__main__":
    Nr = int(os.environ.get("NR", 22))
    Nth = int(os.environ.get("NTH", 8))
    Nps = int(os.environ.get("NPS", 8))
    ms = [int(x) for x in os.environ.get("MS", "1,2,3,4").split(",")]
    do_relax = os.environ.get("RELAX", "1") == "1"
    p = float(os.environ.get("P", 0.4))
    kap8 = float(os.environ.get("KAP8", 0.05))
    print(f"GRID Nr={Nr} Nth={Nth} Nps={Nps}  p={p} kap8={kap8}  ms={ms}  "
          f"relax={do_relax}  cuda={torch.cuda.is_available()}")
    G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    results = []
    for m in ms:
        try:
            rec, u = run_sector(G, m, p=p, kap8=kap8, do_relax=do_relax,
                                verbose=(os.environ.get("V","0")=="1"),
                                maxit=int(os.environ.get("MAXIT","40")),
                                relax_maxit=int(os.environ.get("RELAXIT","18")))
            results.append(rec)
            print(fmt_sector(rec)); sys.stdout.flush()
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"=== m={m} === FAILED: {e!r}"); sys.stdout.flush()
    # machine-readable dump
    def clean(o):
        if isinstance(o, dict): return {k: clean(v) for k,v in o.items()}
        if isinstance(o, (list,tuple)): return [clean(x) for x in o]
        if isinstance(o, (np.floating,)): return float(o)
        return o
    with open(os.environ.get("OUT","winding_catalog_out.json"),"w") as f:
        json.dump(clean(results), f, indent=1)
    print("\nWROTE", os.environ.get("OUT","winding_catalog_out.json"))
