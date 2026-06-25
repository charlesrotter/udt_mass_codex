#!/usr/bin/env python3
"""
branchGP_native_s2_coupled_OBSERVE.py -- BOUNDED static coupled solve to OBSERVE
whether UDT's native S^2 matter acquires a LOCALIZED body / a selected SCALE on
Branch P (keeps the angular-curvature potential U) vs Branch G (gave a scale-free
defect).  OBSERVE mode, DATA-BLIND.  NOT committed.

============================ FIELD / BC SETUP (for verification) ==================
Unknowns (6 nodal fields, each (Nr,Nth,Nps)):
  a,b,c,d : diagonal metric warps  g_tt=-e^{2a}, g_rr=e^{2b}, g_thth=e^{2c} r^2,
            g_psps=e^{2d} r^2 sin^2th  (full3d_spectral.build_metric; B=1/A NOT tied)
  phi     : the depth field, an INDEPENDENT 6th player (NOT slaved to the metric);
            it enters only the operator (weight f=e^{2phi}, its Hessian, X-kinetic,
            and -- Branch P -- the potential U).
  gtw     : the NATIVE S^2 radial twist.  matter field is the on-S^2 3-vector
            n = (sinth cos(m ps + gtw), sinth sin(m ps + gtw), cos th),  m=1,
            |n|=1 EXACT (free_s2_matter.field_n_freeaz / field_dn_freeaz).  gtw is
            PERIODIC in ps and FREE in r -> the radial matter DOF is LIVE (the very
            DOF the rigid n=x/r slice froze).  This is the GENUINELY NATIVE S^2
            3-vector matter (NOT the S^3 4-vector field_dn used by b1prime's EL_Th).

Operator (DERIVED, branch_operator.py / matter_regrade):
  E^mu_nu = f G^mu_nu + (delta box f - nabla nabla f) - X f(dphi dphi - 1/2 delta (dphi)^2)
            - kap8 f T^mu_nu   [+ delta^mu_nu U(phi) for Branch P]
  phi-EOM = f'[R + X(dphi)^2 + kap8 L_m] - 2X div(f grad phi)  [- 2U'(phi) for Branch P]
  U = e^{2phi}-1,  U' = 2e^{2phi}.   gtw-EOM = autograd dS/d gtw (native S^2 action).
  Matter T and L_m are the TARGET-AGNOSTIC MAT.stress_tensor/MAT.lagrangian fed the
  S^2 dn (free_s2_matter): identical machinery, native 3-vector field.  kap8=1.

Constants (TAGGED): X=-2e5 FREE, xi=kap=2e-2 FREE, kap8=1 DERIVED.  m=1.

BCs (match the native_s2 docs / b1prime gates -- the finite-cell canon):
  core r=rc, seal r=ri (cell = ri-rc).  Dirichlet/anchor rows (weight wbc):
   - a(seal)=0   (asymptotic time-norm anchor)
   - b(core)=+p  (depth dial; p chosen, tagged)
   - c,d = 0 at both ends (round angular gauge at the edges)
   - phi(seal)=0 (seal/finite-cell BC, as native_s2 twist-freed used phi(R)=0)
   - gtw : NATURAL/FREE at both ends (NO imposed twist -- imposing one is an import;
           the native finite-cell BC for the residual phase is free, twist-freed doc).
  Interior residual rows: the well-posed mixed set E^t_t,E^r_r,E^th_th,E^ps_ps and the
  off-diag E^r_th,E^r_ps,E^th_ps (=0 on round), phi-EL, gtw-EL, all on the body mask.

ANTI-HANG: single foreground process, sequential (G then P), bounded grid Nr<=16,
Nth,Nps<=8, LM iters<=30, hard wall-clock cap per solve.  jacrev batched Jacobian
(vmap-safe inv/det from full3d_newton), direct lstsq LM step.
"""
import os, sys, math, time
os.environ['PYTORCH_NVML_BASED_CUDA_CHECK'] = '0'
os.environ['PYTORCH_NO_CUDA_MEMORY_CACHING'] = '1'
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from full3d_spectral import Grid3D, attach_coord_weight, build_metric
from einstein_3d_eval import einstein_mixed_weyl
import whole_metric_3d_matter as MAT
import b1prime_3d_offround_residual as B1
from full3d_newton import inv4x4, det4x4

T, R, TH, PS = 0, 1, 2, 3
PI = math.pi

# ---- production constants (tagged) ----
X_PROD   = -2.0e5   # FREE
XI_PROD  = 2.0e-2   # FREE
KAP_PROD = 2.0e-2   # FREE
KAP8     = 1.0      # DERIVED
M_WIND   = 1


# ===========================================================================
# NATIVE S^2 matter (free-azimuth twist), with VMAP-SAFE analytic dn.
#   n = (sth cos Psi, sth sin Psi, cth),  Psi = m*ps + gtw(r,ps),  gtw periodic.
#   dn carried analytically (grid cannot spectrally differentiate bare sin theta);
#   d_r,d_ps of gtw spectral-exact.  Mirrors free_s2_matter.field_dn_freeaz but
#   written with G.d_r/G.d_ps so it is vmap-safe for jacrev.
# ===========================================================================
def s2_dn_freeaz(G, gtw, m=1):
    sth = G.STHg; cth = torch.cos(G.THg)
    Psi = m * G.PSg + gtw
    cP, sP = torch.cos(Psi), torch.sin(Psi)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dn = torch.zeros(Nr, Nth, Nps, 4, 3, device=gtw.device)
    Psi_r = G.d_r(gtw)                 # d_r(m ps)=0
    Psi_p = float(m) + G.d_ps(gtw)     # d_ps(m ps)=m analytic + spectral d_ps gtw
    z3 = torch.zeros_like(sth)
    dn[..., R, :]  = torch.stack([-sth*sP*Psi_r, sth*cP*Psi_r, z3], dim=-1)
    dn[..., TH, :] = torch.stack([cth*cP, cth*sP, -sth], dim=-1)
    dn[..., PS, :] = torch.stack([-sth*sP*Psi_p, sth*cP*Psi_p, z3], dim=-1)
    return dn


def s2_Tmix_and_Lm(G, g, ginv, gtw, xi, kap, m=1):
    """Native S^2 T^mu_nu (mixed) and L_m scalar, target-agnostic MAT machinery."""
    dn = s2_dn_freeaz(G, gtw, m=m)
    Tab, L, L2, L4 = MAT.stress_tensor(g, ginv, dn, xi, kap)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    return Tmix, L


# ===========================================================================
# vmap-safe covariant building blocks (clone of b1prime's, using inv4x4/det4x4
# so jacrev can batch).  d_t = 0 (static).
# ===========================================================================
def coord_grad(G, f):
    z = torch.zeros_like(f)
    return torch.stack([z, G.d_r(f), G.d_th(f), G.d_ps(f)], dim=-1)


def coord_hess(G, f):
    fr = G.d_r(f); ft = G.d_th(f); fp = G.d_ps(f)
    frr = G.d_r(fr); ftt = G.d_th(ft); fpp = G.d_ps(fp)
    frt = G.d_th(fr); frp = G.d_ps(fr); ftp = G.d_ps(ft)
    H = torch.zeros(*f.shape, 4, 4, device=f.device)
    H[..., R, R] = frr; H[..., TH, TH] = ftt; H[..., PS, PS] = fpp
    H[..., R, TH] = H[..., TH, R] = frt
    H[..., R, PS] = H[..., PS, R] = frp
    H[..., TH, PS] = H[..., PS, TH] = ftp
    return H


def christoffel_vsafe(G, g):
    ginv = inv4x4(g)
    Nr, Nth, Nps = G.Nr, G.Nth, G.Nps
    dg = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for mu in range(4):
        for nu in range(4):
            comp = g[..., mu, nu]
            dg[..., R, mu, nu] = G.d_r(comp)
            dg[..., TH, mu, nu] = G.d_th(comp)
            dg[..., PS, mu, nu] = G.d_ps(comp)
    # Gamma^a_{bc} = 1/2 g^{ad}(d_b g_dc + d_c g_db - d_d g_bc)
    term = (dg.permute(0, 1, 2, 4, 3, 5) + dg.permute(0, 1, 2, 5, 3, 4)
            - dg.permute(0, 1, 2, 3, 4, 5))   # [.., d, b, c] combos
    # build explicitly to avoid index confusion
    Gamma = torch.zeros(Nr, Nth, Nps, 4, 4, 4, device=g.device)
    for a in range(4):
        for bb in range(4):
            for cc in range(4):
                acc = torch.zeros(Nr, Nth, Nps, device=g.device)
                for dd in range(4):
                    acc = acc + ginv[..., a, dd]*(
                        dg[..., bb, dd, cc] + dg[..., cc, dd, bb] - dg[..., dd, bb, cc])
                Gamma[..., a, bb, cc] = 0.5*acc
    return Gamma, ginv


def cov_hessian_f(G, f, Gamma):
    H = coord_hess(G, f)
    df = coord_grad(G, f)
    corr = torch.einsum('...amn,...a->...mn', Gamma, df)
    return H - corr


def U_pot(phi):
    return torch.exp(torch.clamp(2.0*phi, max=60.0)) - 1.0


def U_prime(phi):
    return 2.0*torch.exp(torch.clamp(2.0*phi, max=60.0))


# ===========================================================================
# THE BRANCHED MIXED OPERATOR with NATIVE S^2 matter (vmap-safe assembly).
# E^mu_nu = f G + (delta box f - nabla nabla f) - X f(...) - kap8 f T^S2  [+ delta U for P]
# ===========================================================================
def E_mixed_s2(G, a, b, c, d, phi, gtw, X, xi, kap, m=1, kap8=1.0, branch="G"):
    g = build_metric(G, a, b, c, d)
    Gmix = einstein_mixed_weyl(G, a, b, c, d)
    Gamma, ginv = christoffel_vsafe(G, g)
    f = torch.exp(torch.clamp(2*phi, max=60.0))
    covHf = cov_hessian_f(G, f, Gamma)
    covHf_mix = torch.einsum('...ma,...an->...mn', ginv, covHf)
    boxf = torch.einsum('...mn,...mn->...', ginv, covHf)
    delta = torch.eye(4, device=g.device).expand(*f.shape, 4, 4)
    fterm = delta*boxf[..., None, None] - covHf_mix
    dphi = coord_grad(G, phi)
    dphi_up = torch.einsum('...ma,...a->...m', ginv, dphi)
    dphi2 = torch.einsum('...m,...m->...', dphi_up, dphi)
    kin_mix = torch.einsum('...m,...n->...mn', dphi_up, dphi)
    kinterm = -X*f[..., None, None]*(kin_mix - 0.5*delta*dphi2[..., None, None])
    Tmix, _ = s2_Tmix_and_Lm(G, g, ginv, gtw, xi, kap, m=m)
    E = (f[..., None, None]*Gmix + fterm + kinterm - kap8*f[..., None, None]*Tmix)
    if branch == "P":
        E = E + delta*U_pot(phi)[..., None, None]
    return E, ginv, g


def EL_phi_s2(G, a, b, c, d, phi, gtw, X, xi, kap, m=1, kap8=1.0, branch="G"):
    """phi-EOM with the NATIVE S^2 L_m in the algebraic piece + Branch-P -2U'."""
    g = build_metric(G, a, b, c, d)
    Gamma, ginv = christoffel_vsafe(G, g)
    f = torch.exp(torch.clamp(2*phi, max=60.0)); fp = 2.0*f
    Gmix_w = einstein_mixed_weyl(G, a, b, c, d)
    Rscal = -torch.einsum('...mm->...', Gmix_w)
    dphi = coord_grad(G, phi)
    dphi_up = torch.einsum('...ma,...a->...m', ginv, dphi)
    dphi2 = torch.einsum('...m,...m->...', dphi_up, dphi)
    _, Lm = s2_Tmix_and_Lm(G, g, ginv, gtw, xi, kap, m=m)
    alg = fp*(Rscal + X*dphi2 + kap8*Lm)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    Hphi = coord_hess(G, phi)
    df = coord_grad(G, f)
    term_hess = f*torch.einsum('...mn,...mn->...', ginv, Hphi)
    term_fdphi = torch.einsum('...mn,...m,...n->...', ginv, df, dphi)
    conn = torch.zeros_like(f)
    SGgup = sqrtg[..., None, None]*ginv
    for mu in range(1, 4):
        for nu in range(1, 4):
            comp = SGgup[..., mu, nu]
            if mu == R:   dcomp = G.d_r(comp)
            elif mu == TH: dcomp = G.d_th(comp)
            else:          dcomp = G.d_ps(comp)
            conn = conn + dcomp*dphi[..., nu]
    conn = f*conn/torch.clamp(sqrtg, min=1e-30)
    div = term_hess + term_fdphi + conn
    elphi = alg - 2.0*X*div
    if branch == "P":
        elphi = elphi - 2.0*U_prime(phi)
    return elphi


def EL_gtw_s2(G, a, b, c, d, gtw, xi, kap, m=1, f=None):
    """Native S^2 twist EOM density = (1/measure) dS/d gtw, via functorch.grad of the
    action (functorch-composable, so it nests safely inside jacrev -- unlike
    torch.autograd.grad/requires_grad_).  S_m = sum sqrtg * f * L * wvol; f=e^{2phi} is
    gtw-independent so it rides as part of the measure (matches
    free_s2_matter.matter_el_autograd_freeaz, with the e^{2phi} weight on)."""
    from torch.func import grad as fgrad
    g = build_metric(G, a, b, c, d)
    ginv = inv4x4(g)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    fw = sqrtg if f is None else sqrtg*f
    def action_of_gtw(gt):
        dn = s2_dn_freeaz(G, gt, m=m)
        Gmn = MAT.field_metric(dn)
        L, _, _, _ = MAT.lagrangian(ginv, Gmn, xi, kap)
        return (fw*L*G.wvol_coord).sum()
    gG = fgrad(action_of_gtw)(gtw)
    meas = torch.clamp(fw*G.wvol_coord, min=1e-30)
    return gG/meas


# ===========================================================================
# Packed residual vector (interior body rows + BC anchor rows).
# ===========================================================================
def pack6(a, b, c, d, phi, gtw):
    return torch.stack([a, b, c, d, phi, gtw], dim=0)


def unpack6(u):
    return u[0], u[1], u[2], u[3], u[4], u[5]


def residual_vec(u, G, p, X, xi, kap, m=1, kap8=1.0, branch="G", wbc=30.0):
    a, b, c, d, phi, gtw = unpack6(u)
    E, ginv, g = E_mixed_s2(G, a, b, c, d, phi, gtw, X, xi, kap, m=m, kap8=kap8, branch=branch)
    elphi = EL_phi_s2(G, a, b, c, d, phi, gtw, X, xi, kap, m=m, kap8=kap8, branch=branch)
    fwt = torch.exp(torch.clamp(2*phi, max=60.0))
    elg = EL_gtw_s2(G, a, b, c, d, gtw, xi, kap, m=m, f=fwt)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg*G.wvol_coord); W = W/W[G.body].mean()
    bod = G.body
    rows = []
    for (mm, nn) in [(T, T), (R, R), (TH, TH), (PS, PS), (R, TH), (R, PS), (TH, PS)]:
        rows.append((W*E[..., mm, nn])[bod])
    rows.append((W*elphi)[bod])
    rows.append((W*elg)[bod])
    # BC anchor rows
    rows.append(wbc*a[-1, :, :].reshape(-1))            # a(seal)=0
    rows.append(wbc*(b[0, :, :].reshape(-1) + p))       # b(core)=-(-p)=+p depth dial
    rows.append(wbc*c[0, :, :].reshape(-1)); rows.append(wbc*c[-1, :, :].reshape(-1))
    rows.append(wbc*d[0, :, :].reshape(-1)); rows.append(wbc*d[-1, :, :].reshape(-1))
    rows.append(wbc*phi[-1, :, :].reshape(-1))          # phi(seal)=0
    # gtw: NATURAL/FREE at both ends -- NO BC row (imposing one is an import)
    return torch.cat([rr.reshape(-1) for rr in rows])


def jac_jacrev(u, G, p, X, xi, kap, m, kap8, branch, wbc, chunk_size=128):
    from torch.func import jacrev
    fwd = lambda uu: residual_vec(uu, G, p, X, xi, kap, m=m, kap8=kap8, branch=branch, wbc=wbc)
    J = jacrev(fwd, chunk_size=chunk_size)(u)
    F = fwd(u).detach()
    return J.detach(), F


def lm_solve(u0, G, p, X, xi, kap, m=1, kap8=1.0, branch="G", maxit=30, lam0=1e-3,
             tol=1e-12, wbc=30.0, wall_cap=300.0, chunk_size=128, verbose=True):
    t0 = time.time()
    u = u0.detach().clone()
    fwd = lambda uu: residual_vec(uu, G, p, X, xi, kap, m=m, kap8=kap8, branch=branch, wbc=wbc)
    F = fwd(u); Phi = float((F*F).sum()); hist = [Phi]
    nU = u.numel(); I = torch.eye(nU, device=u.device); lam = lam0
    capped = False
    for it in range(maxit):
        if Phi < tol: break
        if time.time()-t0 > wall_cap:
            capped = True; break
        J, F = jac_jacrev(u, G, p, X, xi, kap, m, kap8, branch, wbc, chunk_size)
        J = J.reshape(J.shape[0], nU)                 # (nF, 6,Nr,Nth,Nps) -> (nF, nU)
        accepted = False
        for _t in range(10):
            try:
                Jaug = torch.cat([J, math.sqrt(lam)*I], dim=0)
                Faug = torch.cat([-F, torch.zeros(nU, device=u.device)], dim=0)
                du = torch.linalg.lstsq(Jaug, Faug).solution.reshape(u.shape)
            except Exception:
                lam *= 4.0; continue
            un = u + du
            Pn = float((fwd(un)**2).sum())
            if np.isfinite(Pn) and Pn < Phi:
                u = un; Phi = Pn; lam = max(lam*0.3, 1e-13); accepted = True; break
            lam *= 4.0
        hist.append(Phi)
        if verbose:
            print(f"    [{branch}] it={it:2d} Phi={Phi:.4e} lam={lam:.1e} "
                  f"t={time.time()-t0:.0f}s {'acc' if accepted else 'STALL'}")
        if not accepted: break
        if time.time()-t0 > wall_cap:
            capped = True; break
    return u.detach(), hist, time.time()-t0, capped


# ===========================================================================
# DIAGNOSTICS on a converged field -- the OBSERVE quantities.
# ===========================================================================
def diagnose(u, G, X, xi, kap, m=1, kap8=1.0, branch="G"):
    a, b, c, d, phi, gtw = unpack6(u)
    g = build_metric(G, a, b, c, d); ginv = inv4x4(g)
    Tmix, Lm = s2_Tmix_and_Lm(G, g, ginv, gtw, xi, kap, m=m)
    rho = -Tmix[..., T, T]                       # energy density (mixed)
    # radial profile at a mid angular node
    jt, jp = G.Nth//2, G.Nps//2
    r = G.r.cpu().numpy()
    rho_r = rho[:, jt, jp].cpu().numpy()
    phi_r = phi[:, jt, jp].cpu().numpy()
    a_r = a[:, jt, jp].cpu().numpy(); b_r = b[:, jt, jp].cpu().numpy()
    gtw_r = gtw[:, jt, jp].cpu().numpy()
    # proper-measure energy density e^{B} r^2 rho  (body) -> look for an interior peak
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    bod = G.body.cpu().numpy()
    # M_MS proxy: integrate rho * proper volume over the cell body
    measp = (sqrtg*G.wvol_coord)
    M_MS = float((rho*measp)[G.body].sum())
    # twist energy (extra energy carried by gtw' -- 0 if twist trivial)
    Psi_r_grad = G.d_r(gtw)
    tw_amp = float(gtw[G.body].abs().max())
    tw_grad = float(Psi_r_grad[G.body].abs().max())
    # localization: where is rho*proper-measure peaked vs the core?
    proper_rho = (sqrtg.cpu().numpy())[:, jt, jp]*rho_r  # ~ e^B r^2 rho radial line
    bidx = np.arange(3, G.Nr-3)
    if len(bidx):
        ipk = bidx[np.argmax(np.abs(proper_rho[bidx]))]
        r_peak = float(r[ipk])
    else:
        r_peak = float('nan')
    # B=1/A break proxy:  max|a+b| in body (B=1/A => a+b=0)
    AB = float((a+b)[G.body].abs().max())
    return dict(r=r, rho_r=rho_r, phi_r=phi_r, a_r=a_r, b_r=b_r, gtw_r=gtw_r,
                M_MS=M_MS, tw_amp=tw_amp, tw_grad=tw_grad, r_peak=r_peak,
                proper_rho=proper_rho, AB=AB,
                phi_min=float(phi[G.body].min()), phi_max=float(phi[G.body].max()))


def print_diag(tag, dg, hist, tsec, capped, G):
    print(f"\n  ---- DIAGNOSE [{tag}] ----")
    print(f"    converged Phi={hist[-1]:.3e}  iters={len(hist)-1}  t={tsec:.0f}s  "
          f"capped={capped}")
    print(f"    M_MS (proper-vol integ rho) = {dg['M_MS']:.4e}")
    print(f"    phi range (body) = [{dg['phi_min']:.4e}, {dg['phi_max']:.4e}]  "
          f"(U pulls phi to a preferred depth?)")
    print(f"    twist: max|gtw|={dg['tw_amp']:.3e}  max|gtw'|={dg['tw_grad']:.3e}  "
          f"(->0 = twist trivial/defect)")
    print(f"    B=1/A break max|a+b|(body) = {dg['AB']:.3e}")
    print(f"    rho-localization: proper-rho peak radius r_peak={dg['r_peak']:.3f}  "
          f"(cell rc={G.rc:.2f}..ri={G.ri:.2f}; peak at core => defect, interior => body)")
    # radial rho profile (a few body nodes) to see monotone-defect vs peaked-body
    r = dg['r']; pr = dg['proper_rho']
    bidx = np.arange(3, G.Nr-3)
    samp = bidx[::max(1, len(bidx)//6)]
    prof = "  ".join(f"r={r[i]:.2f}:{pr[i]:.2e}" for i in samp)
    print(f"    proper-rho(r) body samples: {prof}")
    print(f"    phi(r) body: " + "  ".join(f"{r[i]:.2f}:{dg['phi_r'][i]:.3e}" for i in samp))


# ===========================================================================
# MAIN -- sequential G then P, bounded.
# ===========================================================================
def make_seed(G, p):
    """Round seed: mild a,b depth dial, c=d=0, phi=0, gtw=0 (pure hedgehog winding)."""
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=G.dev)
    r = G.Rg; rc, ri = G.rc, G.ri
    s = (r - rc)/(ri - rc)                          # 0 at core, 1 at seal
    b = p*(1.0 - s)                                 # b(core)=p, b(seal)=0
    a = -p*(1.0 - s)                                # a(core)=-p, a(seal)=0 (mild B~1/A seed)
    phi = z.clone()
    gtw = z.clone()
    return pack6(a, b, z.clone(), z.clone(), phi, gtw)


def run_branch(G, branch, p, wall_cap, label):
    print(f"\n{'='*72}\nBRANCH {branch}  ({label})  grid Nr={G.Nr} Nth={G.Nth} Nps={G.Nps}  "
          f"cell rc={G.rc:.2f} ri={G.ri:.2f}\n{'='*72}")
    u0 = make_seed(G, p)
    F0 = residual_vec(u0, G, p, X_PROD, XI_PROD, KAP_PROD, m=M_WIND, kap8=KAP8, branch=branch)
    print(f"  seed residual Phi0 = {float((F0*F0).sum()):.3e}  (nF={F0.numel()})")
    u, hist, tsec, capped = lm_solve(u0, G, p, X_PROD, XI_PROD, KAP_PROD, m=M_WIND,
                                     kap8=KAP8, branch=branch, maxit=30, wall_cap=wall_cap)
    dg = diagnose(u, G, X_PROD, XI_PROD, KAP_PROD, m=M_WIND, kap8=KAP8, branch=branch)
    print_diag(branch, dg, hist, tsec, capped, G)
    return u, hist, dg, tsec, capped


if __name__ == "__main__":
    P_DEPTH = 1.0          # CHOSE depth dial (matches native_s2 / b1prime gate default)
    CELL = 8.0             # CHOSE cell size (native_s2 twist-freed used R=8)
    RC = 0.1               # CHOSE core radius (native_s2 docs r_core=0.1)
    NR, NTH, NPS = 12, 8, 8

    print("NATIVE S^2 COUPLED OBSERVE: Branch G (control) then Branch P.  DATA-BLIND.")
    print(f"X={X_PROD:.1e} xi={XI_PROD} kap={KAP_PROD} kap8={KAP8} m={M_WIND} p={P_DEPTH}")

    G = attach_coord_weight(Grid3D(Nr=NR, Nth=NTH, Nps=NPS, rc=RC, cell=CELL))

    # ---- Branch G (control) ----
    uG, histG, dgG, tG, capG = run_branch(G, "G", P_DEPTH, 300.0, "control: expect scale-free defect")
    np.savez("/tmp/branchG_native_s2.npz", u=uG.cpu().numpy(),
             r=dgG['r'], rho_r=dgG['rho_r'], phi_r=dgG['phi_r'],
             a_r=dgG['a_r'], b_r=dgG['b_r'], gtw_r=dgG['gtw_r'],
             M_MS=dgG['M_MS'], hist=np.array(histG))

    # ---- Branch P (the test) ----
    uP, histP, dgP, tP, capP = run_branch(G, "P", P_DEPTH, 300.0, "test: localized body? selected scale?")
    np.savez("/tmp/branchP_native_s2.npz", u=uP.cpu().numpy(),
             r=dgP['r'], rho_r=dgP['rho_r'], phi_r=dgP['phi_r'],
             a_r=dgP['a_r'], b_r=dgP['b_r'], gtw_r=dgP['gtw_r'],
             M_MS=dgP['M_MS'], hist=np.array(histP))

    print("\n" + "="*72)
    print("OBSERVE COMPARISON  (G defect-control vs P)")
    print("="*72)
    print(f"  M_MS:        G={dgG['M_MS']:.4e}   P={dgP['M_MS']:.4e}")
    print(f"  phi range:   G=[{dgG['phi_min']:.3e},{dgG['phi_max']:.3e}]  "
          f"P=[{dgP['phi_min']:.3e},{dgP['phi_max']:.3e}]")
    print(f"  twist max:   G={dgG['tw_amp']:.3e}   P={dgP['tw_amp']:.3e}")
    print(f"  rho peak r:  G={dgG['r_peak']:.3f}   P={dgP['r_peak']:.3f}  (rc={RC})")
    print(f"  B=1/A break: G={dgG['AB']:.3e}   P={dgP['AB']:.3e}")
    print(f"  conv Phi:    G={histG[-1]:.2e}(cap={capG})   P={histP[-1]:.2e}(cap={capP})")
    print("\nDONE (G,P fields saved to /tmp/branch[GP]_native_s2.npz).")
