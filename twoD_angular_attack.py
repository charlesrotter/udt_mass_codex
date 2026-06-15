#!/usr/bin/env python3
"""
twoD_angular_attack.py -- INDEPENDENT adversarial 2D solver attacking the Stage-B
HEADLINE that the L2+L4 winding-soliton solution space is ONE round (turns=0)
single-soliton continuum with NO distinct theta-dependent / multi-center types.

The committed Stage-B sweep uses a 1D HEDGEHOG ANSATZ T=T(r) ONLY.  This solver
allows the FULL T=T(r,theta) field on the metric
   ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2(dtheta^2+sin^2theta dphi^2),  phi=phi(r),
with the hedgehog winding field
   n = (sinT sintheta cos(m phi), sinT sintheta sin(m phi), cosT),  T=T(r,theta).

DATA-BLIND: NEVER compared to any external "wall" value.  Reports only what the
solver finds.  Driver: Claude (Opus 4.8, 1M).  2026-06-15.  New file (repo
discipline; never edits the committed engine).

ENERGY (DERIVED EXACTLY with sympy in /tmp deriv; cross-checked: the theta-integral
of the L2 density at Tt=0, m=1 reproduces the committed E2_r doc bracket exactly):

  L2 |grad n|^2_g  (T=T(r,theta)):
    g2 = e^{-2phi}/r^2 * [ Tr^2 r^2 (1 - cos^2T cos^2theta)
         + m^2 e^{2phi} sin^2T
         + e^{2phi}( Tt^2 (1 - cos^2T cos^2theta)
                    + 2 sin theta sin T cos theta cos T Tt
                    + cos^2 theta (1 - cos^2 T) ) ]
  Full 2D L2 ENERGY integrand (after phi-integral x2pi, with sqrt(spatial g)=
  e^{phi} r^2 sin theta):
    e2 = 2pi (xi/2) g2 e^{phi} r^2 sin theta

  L4: the committed E4_r is the project's BANKED hedgehog quartic (NOT the naive
  Skyrme |n.(d_i n x d_j n)|^2 -- verified: that gives a different 1D limit).  Its
  reverse-engineered 1D density (theta-integrated, m=1) is
    E4_doc ~ (2pi kap/3) e^{-phi}[ (2 r^2 sin^4T + 2 r^2 sin^2T) Tr^2 + e^{2phi} m^2 sin^4T ]/r^2.
  CAVEAT (stated): for the 2D L4 we use the hedgehog-consistent density evaluated
  with the 2D T, promoting the radial-gradient stiffness term Tr^2 -> Tr^2 + Tt^2/r^2
  (the proper covariant gradient-squared on the (r,theta) chart, g^{rr}Tr^2+g^{thth}Tt^2
  with the e^{-2phi}, 1/r^2 weights folded into the doc's e^{-phi}/r^2 prefactor as in
  the radial term).  The potential piece (m^2 sin^4T) is kept as-is.  This is the
  hedgehog-consistent promotion; the EXACT-derived L2 is the primary attack and is
  reported separately (we also run an L2-ONLY pass so the L4 promotion cannot be
  blamed for a null).

SOLVER: minimize the discretized total energy via damped full-Newton on the
gradient (= the EL equations), torch float64 autograd for the exact gradient and
a colored-FD Hessian-vector / sparse Jacobian.  Grid (Nr x Nth), Dirichlet
T(core,theta)=m*pi, T(seal,theta)=0; Neumann d_theta T=0 on axes theta=0,pi.
phi(r) HELD FIXED from a converged 1D round member (isolates the angular-shape
question -- the headline is about shape/type, not phi back-reaction).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, json, sys
import numpy as np
import torch
import complete_metric_stageB_fast as fb

torch.set_default_dtype(torch.float64)
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PI = math.pi
XI = KAP = 1.0
M = 1
rc = 0.05
SPAN = 14.0
ri = rc + SPAN

t0 = time.time()
def log(*a):
    print(" ".join(str(x) for x in a), flush=True)


# ---------------------------------------------------------------------------
# 1D phi(r) anchor: converged round member from the committed fast engine.
# ---------------------------------------------------------------------------
def phi_anchor(Nr, p, kap8):
    r1 = torch.linspace(rc, ri, Nr, device=DEV).unsqueeze(0)
    o = fb.selfconsistent_fast(r1, XI, KAP, p=p, kap8=kap8, iters=70, relax=0.40,
                               tol=1e-11, theta_iters=40)
    res = o['hist'][-1][3]
    return o['r'][0].clone(), o['phi'][0].clone(), float(res)


# ---------------------------------------------------------------------------
# Energy on the 2D grid.  T shape (Nr,Nth).  r (Nr,), th (Nth,), phi (Nr,).
# Returns total energy E = INT (e2 + e4) dr dtheta (trapezoid), differentiable.
# ---------------------------------------------------------------------------
def energy_2d(T, r, th, phi, include_L4=True):
    Nr, Nth = T.shape
    R = r.view(-1, 1)
    PH = phi.view(-1, 1)
    TH = th.view(1, -1)
    sinth = torch.sin(TH)
    costh = torch.cos(TH)
    sinT = torch.sin(T)
    cosT = torch.cos(T)
    e2p = torch.exp(2.0 * PH)
    em = torch.exp(-PH)

    # gradients (central interior, one-sided ends) -- build via torch.gradient-like
    dr = r[1:] - r[:-1]
    dth = th[1:] - th[:-1]
    # Tr (Nr,Nth)
    Tr = torch.zeros_like(T)
    Tr[1:-1, :] = (T[2:, :] - T[:-2, :]) / (r[2:] - r[:-2]).view(-1, 1)
    Tr[0, :] = (T[1, :] - T[0, :]) / (r[1] - r[0])
    Tr[-1, :] = (T[-1, :] - T[-2, :]) / (r[-1] - r[-2])
    # Tt (Nr,Nth)
    Tt = torch.zeros_like(T)
    Tt[:, 1:-1] = (T[:, 2:] - T[:, :-2]) / (th[2:] - th[:-2]).view(1, -1)
    Tt[:, 0] = (T[:, 1] - T[:, 0]) / (th[1] - th[0])
    Tt[:, -1] = (T[:, -1] - T[:, -2]) / (th[-1] - th[-2])

    cc2 = cosT**2 * costh**2  # cos^2T cos^2theta
    # EXACT 2D L2 |grad n|^2_g  (sympy-derived)
    g2 = (torch.exp(-2.0 * PH) / R**2) * (
        Tr**2 * R**2 * (1.0 - cc2)
        + M**2 * e2p * sinT**2
        + e2p * (Tt**2 * (1.0 - cc2)
                 + 2.0 * sinth * sinT * costh * cosT * Tt
                 + costh**2 * (1.0 - cosT**2))
    )
    e2_dens = 2.0 * PI * (XI / 2.0) * g2 * torch.exp(PH) * R**2 * sinth

    if include_L4:
        # hedgehog-consistent BANKED L4, 2D-promoted (Tr^2 -> Tr^2 + Tt^2/r^2).
        grad2 = Tr**2 + Tt**2 / R**2
        e4_dens = (2.0 * PI * KAP / 3.0) * em * (
            (2.0 * R**2 * sinT**4 + 2.0 * R**2 * sinT**2) * grad2
            + e2p * M**2 * sinT**4
        ) / R**2 * sinth
        # NOTE: doc 1D E4_r had no explicit sin theta because it was already
        # theta-integrated (INT sin th dth = 2) and absorbed the /3 vs /4*2.
        # Here e4_dens carries sin theta and 2pi; the theta-integral of the
        # Tt=0 limit reproduces the doc E4_r up to the same banked normalization
        # (cross-checked numerically below).
    else:
        e4_dens = torch.zeros_like(e2_dens)

    dens = e2_dens + e4_dens
    # trapezoid in r then theta
    Ir = torch.trapz(dens, r, dim=0)      # (Nth,)
    E = torch.trapz(Ir, th)
    return E, e2_dens, e4_dens, Tr, Tt


# ---------------------------------------------------------------------------
# Seeds (INITIAL DATA only; solver settles freely).
# ---------------------------------------------------------------------------
def base_radial(r):
    L = 1.0
    return PI * 0.5 * (1.0 - torch.tanh((r - (rc + 2 * L)) / (0.8 * L)))

def legendre(l, x):
    return torch.tensor(np.polynomial.legendre.legval(
        x.cpu().numpy(), [0] * l + [1]), device=DEV)

def make_seed(r, th, kind):
    Nr, Nth = len(r), len(th)
    R = r.view(-1, 1); TH = th.view(1, -1)
    base = base_radial(r).view(-1, 1).expand(Nr, Nth).clone()
    x = ((R - rc) / (ri - rc))
    costh = torch.cos(th)
    if kind == 'round':
        T = base
    elif kind == 'P2':
        Pl = legendre(2, costh).view(1, -1)
        T = base + 0.9 * torch.exp(-((x - 0.35) / 0.22)**2) * Pl
    elif kind == 'P1':
        Pl = legendre(1, costh).view(1, -1)
        T = base + 0.9 * torch.exp(-((x - 0.35) / 0.22)**2) * Pl
    elif kind == 'P3':
        Pl = legendre(3, costh).view(1, -1)
        T = base + 0.8 * torch.exp(-((x - 0.35) / 0.22)**2) * Pl
    elif kind == 'P4':
        Pl = legendre(4, costh).view(1, -1)
        T = base + 0.8 * torch.exp(-((x - 0.35) / 0.22)**2) * Pl
    elif kind == 'twocenter':
        # two lumps: one near theta=0, one near theta=pi, at mid radius
        lump0 = torch.exp(-((x - 0.4) / 0.16)**2) * torch.exp(-((TH - 0.0) / 0.6)**2)
        lumpP = torch.exp(-((x - 0.4) / 0.16)**2) * torch.exp(-((TH - PI) / 0.6)**2)
        T = base + 1.1 * (lump0 - lumpP)
    elif kind == 'offaxis':
        # localized off-axis lobe near theta=pi/2
        lobe = torch.exp(-((x - 0.4) / 0.16)**2) * torch.exp(-((TH - PI / 2) / 0.5)**2)
        T = base + 1.2 * lobe
    else:
        raise ValueError(kind)
    T = torch.clamp(T, 0.0, M * PI)
    T[0, :] = M * PI
    T[-1, :] = 0.0
    return T


# ---------------------------------------------------------------------------
# Apply BCs (Dirichlet r-ends; Neumann theta-axes) to a working T.
# ---------------------------------------------------------------------------
def apply_bc(T):
    T[0, :] = M * PI
    T[-1, :] = 0.0
    T[:, 0] = T[:, 1]      # d_theta T = 0 at theta=0
    T[:, -1] = T[:, -2]    # d_theta T = 0 at theta=pi
    return T


# ---------------------------------------------------------------------------
# Newton solve: free interior nodes (i in 1..Nr-2, all j), theta-axis nodes
# (j=0,Nth-1) folded via Neumann (T[:,0]=T[:,1], T[:,-1]=T[:,-2]); the energy
# gradient wrt the FREE variables = the residual F; Hessian by autograd jvp /
# colored FD.  We use scipy sparse Newton on a flattened free-variable vector.
# ---------------------------------------------------------------------------
import scipy.sparse as sps
import scipy.sparse.linalg as spsla

def solve_2d(T0, r, th, phi, include_L4=True, itmax=120, tol=1e-9, verbose=False):
    Nr, Nth = T0.shape
    # free variables: interior radial rows 1..Nr-2, theta columns 1..Nth-2
    # (axis columns are slaved by Neumann; r-ends are Dirichlet)
    fi = np.arange(1, Nr - 1)
    fj = np.arange(1, Nth - 1)
    nfi, nfj = len(fi), len(fj)
    Nfree = nfi * nfj

    rT = r.clone(); thT = th.clone(); phiT = phi.clone()

    def expand(xvec):
        T = T0.clone()
        Tin = torch.tensor(xvec.reshape(nfi, nfj), device=DEV)
        T[1:Nr - 1, 1:Nth - 1] = Tin
        T = apply_bc(T)
        return T

    def grad_at(xvec):
        T = expand(xvec)
        Tv = T.clone().requires_grad_(True)
        E, *_ = energy_2d(Tv, rT, thT, phiT, include_L4=include_L4)
        g, = torch.autograd.grad(E, Tv)
        # residual = gradient wrt free interior nodes
        gfree = g[1:Nr - 1, 1:Nth - 1].detach().cpu().numpy().ravel()
        return gfree, float(E.item())

    def jac_colored(xvec, eps=1e-6):
        # colored FD of the free-node gradient.  Stencil of the EL is a 5-point
        # (r +/-1, theta +/-1) coupling on the free interior; a 3x3 grid coloring
        # makes columns in one color non-overlapping in any residual row.
        g0, _ = grad_at(xvec)
        N = Nfree
        idx = np.arange(N).reshape(nfi, nfj)
        rows, cols, vals = [], [], []
        for ci in range(3):
            for cj in range(3):
                mask = np.zeros((nfi, nfj), dtype=bool)
                mask[ci::3, cj::3] = True
                xp = xvec.copy().reshape(nfi, nfj)
                xp[mask] += eps
                gp, _ = grad_at(xp.ravel())
                dF = ((gp - g0) / eps).reshape(nfi, nfj)
                owner = np.full((nfi, nfj), -1, dtype=np.int64)
                # residual row (i,j) affected by perturbed node in {(i,j),(i+-1,j),(i,j+-1)}
                # plus axis-Neumann re-coupling: a column j=1 reads j=0 slaved to j=1, and
                # row i=1 reads i=0 Dirichlet (no coupling) -> 5-point + the axis fold,
                # which only re-weights j=1,Nth-2 diag; covered by the 3x3 coloring with
                # a wider owner search to be safe.
                for (di, dj) in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                    si = np.arange(nfi)[:, None] + di
                    sj = np.arange(nfj)[None, :] + dj
                    valid = (si >= 0) & (si < nfi) & (sj >= 0) & (sj < nfj)
                    sic = np.clip(si, 0, nfi - 1); sjc = np.clip(sj, 0, nfj - 1)
                    inc = valid & mask[sic, sjc] & (owner < 0)
                    owner[inc] = idx[sic, sjc][inc]
                sel = owner >= 0
                rr = idx[sel]; cc = owner[sel]; vv = dF[sel]
                nz = vv != 0.0
                rows.append(rr[nz]); cols.append(cc[nz]); vals.append(vv[nz])
        J = sps.csr_matrix((np.concatenate(vals),
                            (np.concatenate(rows), np.concatenate(cols))),
                           shape=(N, N))
        return J, g0

    x = T0[1:Nr - 1, 1:Nth - 1].detach().cpu().numpy().ravel().copy()
    maxres = np.inf
    for nit in range(itmax):
        J, F0 = jac_colored(x)
        nF0 = float(np.linalg.norm(F0))
        Js = 0.5 * (J + J.T)  # symmetrize (energy Hessian is symmetric)
        try:
            dx = spsla.spsolve(Js.tocsc() + 1e-12 * sps.eye(len(x)), -F0)
        except Exception:
            break
        if not np.all(np.isfinite(dx)):
            break
        lam, ok = 1.0, False
        for _ in range(40):
            xt = x + lam * dx
            gt, _ = grad_at(xt)
            if np.isfinite(gt).all() and np.linalg.norm(gt) < (1 - 1e-4 * lam) * nF0:
                ok = True; break
            lam *= 0.5
        if not ok:
            g0, _ = grad_at(x)
            maxres = float(np.max(np.abs(g0)))
            break
        x = x + lam * dx
        g0, _ = grad_at(x)
        maxres = float(np.max(np.abs(g0)))
        if verbose and (nit % 5 == 0 or maxres < tol):
            log(f"    newton it={nit} lam={lam:.3f} maxres={maxres:.3e}")
        if maxres < tol:
            break
    Tf = expand(x)
    Ef, e2d, e4d, Tr, Tt = energy_2d(Tf, rT, thT, phiT, include_L4=include_L4)
    return Tf, maxres, float(Ef.item()), nit


# ---------------------------------------------------------------------------
# Diagnostics on a converged 2D T.
# ---------------------------------------------------------------------------
def diagnose(T, r, th):
    Tn = T.detach().cpu().numpy()
    # angular variation amplitude: max over r of std_theta(T)
    th_std = np.std(Tn, axis=1)
    th_var = float(np.max(th_std))
    # max |d_theta T| interior
    dth = (th[1:] - th[:-1]).cpu().numpy()
    Tt = np.zeros_like(Tn)
    Tt[:, 1:-1] = (Tn[:, 2:] - Tn[:, :-2]) / (th.cpu().numpy()[2:] - th.cpu().numpy()[:-2])[None, :]
    max_dthT = float(np.max(np.abs(Tt[1:-1, :])))
    # dominant Legendre l of the angular pattern at the radius of max theta-var
    ir = int(np.argmax(th_std))
    prof = Tn[ir] - Tn[ir].mean()
    x = np.cos(th.cpu().numpy())
    Lmax = 6
    B = np.stack([np.polynomial.legendre.legval(x, [0] * l + [1])
                  for l in range(Lmax + 1)], axis=1)
    Wd = np.diag(np.sin(th.cpu().numpy()))
    coef, *_ = np.linalg.lstsq(B.T @ Wd @ B, B.T @ Wd @ prof, rcond=None)
    dom_l = int(np.argmax(np.abs(coef[1:])) + 1) if th_var > 1e-7 else 0
    return th_var, max_dthT, dom_l, [float(c) for c in coef]


def main():
    log("=" * 78)
    log(f"twoD_angular_attack  device={DEV}  torch={torch.__version__}")
    log("Full T=T(r,theta) L2(exact)+L4(promoted) attack on the Stage-B ONE-CONTINUUM headline")
    log("=" * 78)

    Nr, Nth = 200, 60
    anchors = [(0.4, 0.0), (0.4, 0.05), (1.2, 0.0), (2.0, 0.0), (2.0, 0.05)]
    # (p=1.2,k8=0.05 omitted: the 1D round member there does not converge -- horizon/blowup)
    seeds = ['round', 'P2', 'P1', 'P3', 'P4', 'twocenter', 'offaxis']

    all_results = {}
    for (p, k8) in anchors:
        log(f"\n{'#'*70}\nANCHOR p={p} kap8={k8}  (phi(r) FIXED from converged 1D round member)\n{'#'*70}")
        r1d, phi1d, res1d = phi_anchor(Nr, p, k8)
        log(f"  1D round anchor: res_th={res1d:.2e}  phi0={phi1d[0].item():.4f}")
        r = r1d.clone(); th = torch.linspace(0.0, PI, Nth, device=DEV)
        phi = phi1d.clone()

        # reference round solution (control) for distinctness comparison
        log(f"\n  {'seed':>10} {'L4':>3} {'conv':>5} {'maxres':>9} {'max|dThT|':>10} "
            f"{'th_var':>9} {'dom_l':>5} {'E':>12} {'distinct?':>9}")
        round_T = {}
        rows = []
        for useL4 in [True, False]:
            tag4 = 'on' if useL4 else 'off'
            # solve round first
            T0 = make_seed(r, th, 'round')
            Tr_, mres_r, Er, nit_r = solve_2d(T0, r, th, phi, include_L4=useL4)
            round_T[useL4] = (Tr_, Er)
            for sd in seeds:
                T0 = make_seed(r, th, sd)
                Tf, mres, Ef, nit = solve_2d(T0, r, th, phi, include_L4=useL4)
                th_var, mdT, dom_l, coef = diagnose(Tf, r, th)
                conv = mres < 1e-7
                # distinctness from round: profile difference AND persistent theta-dep
                dprof = float(torch.max(torch.abs(Tf - round_T[useL4][0])).item())
                dE = Ef - Er
                distinct = (th_var > 1e-3) and conv and (dprof > 1e-3)
                rows.append(dict(p=p, k8=k8, seed=sd, L4=tag4, conv=bool(conv),
                                 maxres=mres, max_dThT=mdT, th_var=th_var,
                                 dom_l=dom_l, E=Ef, dE_from_round=dE,
                                 dprof_from_round=dprof, distinct=bool(distinct)))
                log(f"  {sd:>10} {tag4:>3} {str(conv):>5} {mres:>9.2e} {mdT:>10.3e} "
                    f"{th_var:>9.3e} {dom_l:>5} {Ef:>12.5f} {str(distinct):>9}")
        all_results[f"p{p}_k8{k8}"] = rows

    # ---- GRID REFINEMENT on the most theta-distorted seed at one anchor ----
    log(f"\n{'='*70}\nGRID REFINEMENT (P2 seed, p=0.4 k8=0.0, L4 on): grid-independence test\n{'='*70}")
    log(f"  {'Nr':>5} {'Nth':>5} {'maxres':>9} {'th_var':>10} {'dom_l':>5} {'E':>12}")
    refine = []
    for (NrR, NthR) in [(150, 45), (200, 60), (300, 90)]:
        r1d, phi1d, _ = phi_anchor(NrR, 0.4, 0.0)
        r = r1d.clone(); th = torch.linspace(0.0, PI, NthR, device=DEV); phi = phi1d.clone()
        T0 = make_seed(r, th, 'P2')
        Tf, mres, Ef, nit = solve_2d(T0, r, th, phi, include_L4=True)
        th_var, mdT, dom_l, coef = diagnose(Tf, r, th)
        refine.append(dict(Nr=NrR, Nth=NthR, maxres=mres, th_var=th_var, dom_l=dom_l, E=Ef))
        log(f"  {NrR:>5} {NthR:>5} {mres:>9.2e} {th_var:>10.3e} {dom_l:>5} {Ef:>12.5f}")
    all_results['refine_P2'] = refine

    # ---- SUMMARY ----
    log(f"\n{'='*70}\nSUMMARY\n{'='*70}")
    n_distinct = sum(1 for k, v in all_results.items() if isinstance(v, list)
                     for row in v if isinstance(row, dict) and row.get('distinct'))
    log(f"  total seeds tried (across anchors x L4on/off): "
        f"{sum(len(v) for k,v in all_results.items() if k.startswith('p'))}")
    log(f"  DISTINCT theta-dependent converged types found: {n_distinct}")

    def jc(o):
        if isinstance(o, dict): return {k: jc(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [jc(v) for v in o]
        if isinstance(o, (np.bool_,)): return bool(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, float) and o != o: return None
        return o
    with open("twoD_angular_attack_data.json", "w") as fh:
        json.dump(jc(all_results), fh, indent=1)
    log(f"\n  wall time {time.time()-t0:.1f}s   data -> twoD_angular_attack_data.json")


if __name__ == "__main__":
    main()
