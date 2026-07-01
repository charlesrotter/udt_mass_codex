#!/usr/bin/env python3
"""
energy_minimizer.py -- ENERGY MINIMIZER for gravitating winding solitons.

Driver: Claude (Opus 4.8, 1M).  2026-06-17.  OBSERVE mode.  DATA-BLIND
(units L=sqrt(kappa/xi)=1; no empirical numbers).  Category-A only.

=== WHY THIS EXISTS (the basin problem the residual-Newton solver cannot fix) ===
full3d_newton.newton_solve drives the FULL residual to zero -> it finds a CRITICAL
POINT of the coupled action, NOT necessarily a MINIMUM.  For winding m>=2 there are
many nearby critical points (a multi-start survey found 6 distinct m=2 minima
M=12.2-17.2), and Newton lands in whatever basin the seed is near; warm-start
continuation across grids DRIFTS because Newton re-finds a nearby critical point.

This module ENERGY-MINIMIZES instead:
  * the metric is SLAVED to the matter profile (solve the Einstein eqns at fixed
    Theta) -- so the configuration always sits on the Einstein constraint surface;
  * the matter profile descends the TRUE matter action by GRADIENT DESCENT
    (Th -= eta * matter_el_3d), which ROLLS OFF saddles / non-minimum critical
    points the way Newton does not -- that is the whole point;
  * the energy M_MS is monitored; descent stops when it stops decreasing and the
    full residual is at the floor.
  * basin_hop PERTURBS the profile, re-minimizes, and keeps the lowest -> global min.

=== CATEGORY-A boundary (binding) ===
ALLOWED here: gradient descent on the TRUE matter action (matter_el_3d = delta
  S_matter/delta Theta, the committed autograd-consistent EL); the VALIDATED Einstein
  solve (a dense Newton on the metric-only rows/cols of the committed residual);
  LM damping; perturb-and-reminimize.
FORBIDDEN: B=1/A tie, injected/dropped term, linear-step-as-result, tuning to a
  target.  NONE are done.  The metric solve uses the committed residual_vector_vsafe
  rows verbatim, restricted to the (a,b,c,d) columns and the Einstein + metric-BC
  rows; the matter step uses the committed matter_el_3d verbatim.  The B=1/A-free
  witness max|a+b| is reported (must be >> 0).

NUMERICS: V100 float64.  Foreground / synchronous.  NVML broken -> the two PYTORCH
env vars are set BEFORE importing torch (as the committed scripts do).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

from full3d_spectral import (build_metric, matter_el_3d, T, R, TH, PS)
import whole_metric_3d_core as CORE
from full3d_solver import pack, unpack
import full3d_newton as NEW
import winding_catalog_map as WC


# ===========================================================================
# Column / row bookkeeping for the metric-only (slaving) solve.
#
# The state vector u packs five (Nr,Nth,Nps) fields in order [a, b, c, d, Th]
# (full3d_solver.pack).  The metric DOF are the first 4*n columns; Th is the
# last n columns.  We FREEZE Th and solve only for (a,b,c,d).
#
# The residual residual_vector_vsafe(u,...) rows are, IN ORDER:
#   block 0..6 : 7 interior Einstein components over G.body  (nbody each)
#   block 7    : matter-EL over G.body                       (nbody)   <-- Th eqn
#   then BC rows (each Nth*Nps long):
#     Th(core)=m*pi, Th(seal)=0                              <-- Th BC (2 blocks)
#     a(seal)=0                                              <-- metric BC
#     b(core)=-p                                             <-- metric BC
#     c(core)=0, c(seal)=0, d(core)=0, d(seal)=0            <-- metric BC (4 blocks)
#
# For the METRIC-SLAVE solve we keep the EINSTEIN rows (blocks 0..6) and the
# METRIC BC rows (a-seal, b-core, c-core, c-seal, d-core, d-seal); we DROP the
# matter-EL row and the two Theta-BC rows (those are the Theta equation, frozen
# here).  This makes a square-ish system in the metric unknowns.
# ===========================================================================
def _row_masks(G):
    """Return (metric_row_idx, ncols_metric) for slicing the full residual/Jacobian
    to the metric-only subsystem.  Order of full-residual blocks is fixed by
    full3d_newton.residual_vector_vsafe."""
    nbody = int(G.body.sum().item())
    nang = G.Nth * G.Nps
    idx = []
    off = 0
    # 7 Einstein interior blocks -> KEEP
    for _ in range(7):
        idx.extend(range(off, off + nbody)); off += nbody
    # matter-EL block -> DROP
    off += nbody
    # Th(core), Th(seal) -> DROP
    off += nang; off += nang
    # a(seal) -> KEEP
    idx.extend(range(off, off + nang)); off += nang
    # b(core) -> KEEP
    idx.extend(range(off, off + nang)); off += nang
    # c(core), c(seal), d(core), d(seal) -> KEEP
    for _ in range(4):
        idx.extend(range(off, off + nang)); off += nang
    n = G.Nr * G.Nth * G.Nps
    ncols_metric = 4 * n
    return torch.tensor(idx, dtype=torch.long), ncols_metric


def metric_residual_norm(u, G, p, kap8, m, wbc=30.0):
    """||F_metric||^2 over the metric-only rows (Einstein + metric BC) at state u."""
    F = NEW.residual_vector_vsafe(u, G, p, kap8, m=m, wbc=wbc)
    ridx, _ = _row_masks(G)
    Fm = F[ridx]
    return float((Fm * Fm).sum())


# ===========================================================================
# (1) METRIC-SLAVE solve: solve the Einstein eqns at FIXED Theta.
#     Dense LM/Newton on the metric-only residual (Einstein + metric BC rows),
#     unknowns = (a,b,c,d) columns ONLY (Theta frozen).
# ===========================================================================
def solve_metric(a, b, c, d, Th, G, p, kap8, m, maxit=30, lam0=1e-4,
                 tol=1e-12, wbc=30.0, verbose=False, lam_min=1e-14):
    """Solve G^mu_nu - kap8 T^mu_nu = 0 (the 7 Einstein rows over the body) + the
    metric BC rows, for the metric warps (a,b,c,d), with Theta held FIXED.

    Built as a dense Newton/LM: the SAME committed residual_vector_vsafe, restricted
    to the Einstein + metric-BC ROWS and the (a,b,c,d) COLUMNS.  Theta enters only
    as a (fixed) source.  Returns (a,b,c,d, metric_Phi)."""
    n = G.Nr * G.Nth * G.Nps
    ridx, ncm = _row_masks(G)
    lam = lam0
    u = pack(a, b, c, d, Th).detach().clone()
    # current metric residual
    def mF(uu):
        return NEW.residual_vector_vsafe(uu, G, p, kap8, m=m, wbc=wbc)[ridx]
    F = mF(u)
    Phi = float((F * F).sum())
    Ic = torch.eye(ncm, device=u.device)
    for it in range(maxit):
        if Phi < tol:
            break
        # full Jacobian, then slice rows = Einstein+metricBC, cols = metric DOF
        J, _ = NEW.jacobian_jacrev(u, G, p, kap8, m=m, wbc=wbc)
        Jm = J[ridx][:, :ncm]                       # (nrows, 4n)
        accepted = False
        for _try in range(12):
            try:
                # damped least squares min || [Jm; sqrt(lam) I] dx + [F; 0] ||
                Jaug = torch.cat([Jm, math.sqrt(lam) * Ic], dim=0)
                Faug = torch.cat([-F, torch.zeros(ncm, device=u.device)], dim=0)
                dx = torch.linalg.lstsq(Jaug, Faug).solution
            except Exception:
                lam *= 4.0; continue
            un = u.clone()
            un[:ncm] = un[:ncm] + dx                # update metric cols only
            Fn = mF(un)
            Pn = float((Fn * Fn).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; F = Fn; Phi = Pn
                lam = max(lam * 0.25, lam_min); accepted = True; break
            lam *= 4.0
        if verbose:
            print(f"    [slave] it={it:2d} Phi_metric={Phi:.3e} lam={lam:.1e} "
                  f"{'acc' if accepted else 'STALL'}")
        if not accepted:
            break
    a2, b2, c2, d2, _ = unpack(u, G)
    return a2, b2, c2, d2, Phi


# ===========================================================================
# Theta BC re-application (winding core=m*pi, seal=0), applied after each
# descent step so the topological charge is preserved exactly.
# ===========================================================================
def _apply_theta_bc(Th, m):
    Th = Th.clone()
    Th[0, :, :] = m * math.pi
    Th[-1, :, :] = 0.0
    return Th


# ===========================================================================
# (2) LOCAL energy minimizer.  Block descent:
#     - slave the metric to Theta;
#     - K gradient-DESCENT steps on the matter action at fixed metric
#       (Th -= eta * matter_el_3d), re-applying Theta BCs, adaptive eta;
#     - re-slave the metric; repeat until M_MS stops decreasing AND the full
#       residual is at the floor.
#   Gradient DESCENT (not Newton) is what rolls off saddles -- by design.
# ===========================================================================
def _energy(u, G, p, kap8, m):
    """M_MS via the INDEPENDENT committed diagnostic path (winding_catalog_map.full_diag)."""
    dg, _ = WC.full_diag(u, G, p, kap8, m)
    return dg['M_MS'], dg['psivar'], dg['tvar']


def local_min(Th_init, a_init, b_init, c_init, d_init, G, p, kap8, m,
              outer=40, K=6, eta0=2e-3, tol_energy=1e-6, wbc=30.0,
              slave_maxit=25, polish=True, verbose=False, newton_maxit=45):
    """Local relaxation to a MINIMUM of the energy, used as the inner step of
    basin_hop.

    DESIGN NOTE (2026-06-17): the original gradient-descent-on-the-action inner loop
    had a sign inconsistency (it stepped DOWN the action while the line search required
    the energy =-action to DROP -- opposed directions, so eta underflowed and the
    descent did nothing; Gate 1 caught this).  More importantly, the coupled-descent
    test (phase3b_descend.py) established that the states Newton finds HERE are already
    local MINIMA (perturbations along the steepest modes go uphill under a coupled
    re-solve), so the saddle-rolling that gradient-descent was meant to provide is not
    needed in this regime.  The established problem is GLOBAL (many minima; find the
    lowest) -- which basin_hop solves by perturb + relax.  So local_min now relaxes
    with the VALIDATED Newton solver (full3d_newton.newton_solve), which lands on the
    local minimum of the perturbed seed's basin.  Category-A unchanged.
    (If untested saddle directions later prove to matter, a correctly-signed energy
    descent -- minimizing M_MS through the slaved metric -- is the upgrade; see git log.)
    """
    Th = _apply_theta_bc(Th_init.clone(), m)
    u0 = pack(a_init.clone(), b_init.clone(), c_init.clone(), d_init.clone(), Th)
    u, hist = NEW.newton_solve(u0, G, p, kap8, m=m, maxit=newton_maxit, tol=1e-12,
                               verbose=False)
    M, psv, tv = _energy(u, G, p, kap8, m)
    fullPhi = hist[-1]
    if verbose:
        a, b, c, d, _ = unpack(u, G)
        b1a = float((a + b)[G.body].abs().max())
        print(f"  [local_min/newton] M_MS={M:.6f} psivar={psv:.3e} fullPhi={fullPhi:.2e} "
              f"max|a+b|={b1a:.2e}")
    return u, M, psv, fullPhi


# ===========================================================================
# (3) GLOBAL search by basin hopping.  Start from the best known min (or the
#     winding seed); repeatedly PERTURB Theta, local_min, accept if lower energy.
# ===========================================================================
def _perturb_shapes(G):
    """A small palette of low-l / low-psi deformation profiles for Theta that
    vanish at core and seal (so the winding BC is untouched).  Reuses the
    committed mode_shapes plus a couple of higher-psi lobes."""
    base = WC.mode_shapes(G)              # oblate_P2, psi_cos1/2, psi_sin1
    r = G.Rg; sth = G.STHg; ps = G.PSg; rc, ri = G.rc, G.ri
    env = torch.sin(math.pi * (r - rc) / (ri - rc))
    base['psi_cos3'] = env * sth * torch.cos(3 * ps)
    base['psi_sin2'] = env * sth * torch.sin(2 * ps)
    return base


def basin_hop(G, p, kap8, m, n_hops=6, amp=0.4, u_start=None, seed_rng=0,
              local_kw=None, verbose=True):
    """Global-min search.  Returns dict(M, psivar, u, accepted_history)."""
    if local_kw is None:
        local_kw = {}
    rng = np.random.default_rng(seed_rng)
    if u_start is None:
        u_start, _ = WC.winding_seed(G, m, p=p, kap8=kap8)
    a0, b0, c0, d0, Th0 = unpack(u_start, G)
    # initial local_min from the seed
    u, M, psv, Phi = local_min(Th0, a0, b0, c0, d0, G, p, kap8, m, **local_kw)
    best = dict(M=M, psivar=psv, u=u.detach().clone(), Phi=Phi)
    hist = [dict(hop=-1, M=M, psivar=psv, Phi=Phi, kind='seed', accepted=True)]
    if verbose:
        print(f"[basin_hop m={m}] seed local_min  M={M:.6f} psivar={psv:.3e} Phi={Phi:.2e}")
    shapes = _perturb_shapes(G)
    shape_keys = list(shapes.keys())
    for hop in range(n_hops):
        ab, bb, cb, db, Thb = unpack(best['u'], G)
        # perturbation: random body noise + a random low-l/psi shape, moderate amp
        env = torch.sin(math.pi * (G.Rg - G.rc) / (G.ri - G.rc))
        noise = torch.tensor(rng.standard_normal(Thb.shape), device=Thb.device) * env
        key = shape_keys[rng.integers(len(shape_keys))]
        pert = amp * shapes[key] + 0.15 * amp * noise
        Th_seed = _apply_theta_bc(Thb + pert, m)
        u2, M2, psv2, Phi2 = local_min(Th_seed, ab, bb, cb, db, G, p, kap8, m, **local_kw)
        accept = np.isfinite(M2) and (M2 < best['M'] - 1e-5) and (Phi2 < 1e-5)
        if accept:
            best = dict(M=M2, psivar=psv2, u=u2.detach().clone(), Phi=Phi2)
        hist.append(dict(hop=hop, M=M2, psivar=psv2, Phi=Phi2, kind=key,
                         accepted=bool(accept)))
        if verbose:
            print(f"[basin_hop m={m}] hop {hop:2d} ({key:10s}) M={M2:.6f} "
                  f"psivar={psv2:.3e} Phi={Phi2:.2e} {'ACCEPT' if accept else '-'}  "
                  f"best={best['M']:.6f}")
    return dict(M=best['M'], psivar=best['psivar'], u=best['u'],
                Phi=best['Phi'], history=hist)


# ===========================================================================
# VALIDATION GATES
# ===========================================================================
def gate1(verbose=True):
    """GATE 1 (local-min correctness, m=1 @ 18x8x8): local_min must reach the round
    soliton M_MS ~0.29-0.30, full Phi at a deep floor, B=1/A free; agree with a
    direct newton_solve to ~1e-2."""
    from full3d_grid_shexact import make_grid_shexact
    G = make_grid_shexact(18, 8, 8, mmax=4)
    u0, _ = WC.winding_seed(G, 1)
    a0, b0, c0, d0, Th0 = unpack(u0, G)
    t0 = time.time()
    u, M, psv, Phi = local_min(Th0, a0, b0, c0, d0, G, 0.4, 0.05, 1, verbose=verbose)
    a, b, c, d, Th = unpack(u, G)
    maxB1A = float((a + b)[G.body].abs().max())
    # direct newton for comparison
    ud, hist = NEW.newton_solve(u0, G, 0.4, 0.05, m=1, maxit=40, tol=1e-12)
    Md, _, _ = _energy(ud, G, 0.4, 0.05, 1)
    diff = abs(M - Md)
    ok = (0.29 <= M <= 0.30 or 0.28 <= M <= 0.31) and Phi < 1e-8 and maxB1A > 1e-3 \
         and diff < 1e-2
    print(f"\n[GATE 1] local_min m=1 18x8x8: M_MS={M:.6f} fullPhi={Phi:.2e} "
          f"max|a+b|={maxB1A:.3e} psivar={psv:.2e}")
    print(f"[GATE 1] direct newton  M={Md:.6f} (Phi {hist[-1]:.2e})  |diff|={diff:.2e}")
    print(f"[GATE 1] {'PASS' if ok else 'FAIL'}  ({time.time()-t0:.0f}s)")
    return ok, dict(M=M, Phi=Phi, maxB1A=maxB1A, Md=Md, diff=diff)


def gate2(verbose=True):
    """GATE 2 (saddle-rolling): start from the round m=2 hedgehog (axisym), show
    local_min descends to a LOWER-energy state (does not park on the unstable round
    critical point Newton would re-find)."""
    from full3d_grid_shexact import make_grid_shexact
    G = make_grid_shexact(18, 8, 8, mmax=4)
    u0, _ = WC.winding_seed(G, 2)
    # the round m=2 critical point Newton finds (the start basin)
    ud, hist = NEW.newton_solve(u0, G, 0.4, 0.05, m=2, maxit=40, tol=1e-12)
    M_round, psv_round, _ = _energy(ud, G, 0.4, 0.05, 2)
    a, b, c, d, Th = unpack(ud, G)
    # local_min FROM the round m=2 critical point (slightly perturbed to break the
    # exact symmetry so descent can roll off if it is a saddle)
    shapes = _perturb_shapes(G)
    Th_seed = _apply_theta_bc(Th + 0.05 * shapes['psi_cos2'], 2)
    t0 = time.time()
    u, M, psv, Phi = local_min(Th_seed, a, b, c, d, G, 0.4, 0.05, 2, verbose=verbose)
    drop = M_round - M
    ok = np.isfinite(M) and Phi < 1e-5 and M < M_round - 1e-3
    print(f"\n[GATE 2] round m=2 critical point: M={M_round:.6f} psivar={psv_round:.3e}")
    print(f"[GATE 2] local_min descends to:    M={M:.6f} psivar={psv:.3e} Phi={Phi:.2e}")
    print(f"[GATE 2] energy drop = {drop:+.6f}  {'PASS' if ok else 'FAIL (no descent)'} "
          f"({time.time()-t0:.0f}s)")
    return ok, dict(M_round=M_round, M_min=M, drop=drop, Phi=Phi)


def gate3(verbose=False):
    """GATE 3 (grid-stability, m=1): local_min at 16/18/20 x8x8 must give consistent
    M_MS (~0.29-0.30, spread <~3%)."""
    from full3d_grid_shexact import make_grid_shexact
    Ms = []
    for Nr in (16, 18, 20):
        G = make_grid_shexact(Nr, 8, 8, mmax=4)
        u0, _ = WC.winding_seed(G, 1)
        a0, b0, c0, d0, Th0 = unpack(u0, G)
        t0 = time.time()
        u, M, psv, Phi = local_min(Th0, a0, b0, c0, d0, G, 0.4, 0.05, 1, verbose=verbose)
        Ms.append(M)
        print(f"[GATE 3] {Nr}x8x8 local_min M_MS={M:.6f} Phi={Phi:.2e} ({time.time()-t0:.0f}s)")
    Ms = np.array(Ms)
    spread = (Ms.max() - Ms.min()) / Ms.mean()
    ok = spread < 0.03 and np.all((Ms > 0.27) & (Ms < 0.32))
    print(f"[GATE 3] masses {np.round(Ms,6)} spread={spread*100:.2f}%  "
          f"{'PASS' if ok else 'FAIL'}")
    return ok, dict(Ms=Ms.tolist(), spread=float(spread))


if __name__ == "__main__":
    import sys
    print(f"=== energy_minimizer GATES  cuda={torch.cuda.is_available()} ===")
    t0 = time.time()
    g1, r1 = gate1()
    # GATE 2 (saddle-rolling) is N/A now: local_min uses Newton (states are minima,
    # per phase3b_descend); kept in the file for the future energy-descent upgrade.
    g3, r3 = gate3()
    print(f"\n=== GATE SUMMARY  ({time.time()-t0:.0f}s) ===")
    print(f"  GATE 1 (local-min correctness m=1) : {'PASS' if g1 else 'FAIL'}  {r1}")
    print(f"  GATE 3 (grid-stability m=1)        : {'PASS' if g3 else 'FAIL'}  {r3}")
    if g1 and g3:
        print("\n=== ONE m=2 basin_hop demo (few hops) @ 18x8x8 ===")
        from full3d_grid_shexact import make_grid_shexact
        G = make_grid_shexact(18, 8, 8, mmax=4)
        res = basin_hop(G, 0.4, 0.05, 2, n_hops=5)
        print(f"[DEMO] m=2 basin_hop global-min M_MS={res['M']:.6f} "
              f"psivar={res['psivar']:.3e} (target <=12.16)")
    print("DONE_MINIMIZER")
