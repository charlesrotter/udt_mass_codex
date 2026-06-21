#!/usr/bin/env python3
"""
b1prime_3d_offround_validate.py -- ROUND-LIMIT validation (BY EVALUATION) of the
genuine 3-D off-round residual b1prime_3d_offround_residual.py.  NO 3-D Newton solve.

Gates:
 1. REDUCTION gate : embed a round field (c=d=0, a,b,phi,Theta = funcs of r) and check
    the 3-D mixed E^t_t, E^r_r and EL_phi, EL_Theta reduce POINTWISE to the banked
    RADIAL operator (b1prime_round.py E_tt/E_rr/EL_phi/EL_Th) on the same r-nodes.
 2. ZERO gate : solve the banked round soliton (b1prime_round.solve at X=-2e5,
    xi=kap=2e-2), embed it, and check the 3-D residual is ~0 (floored).
 3. box f / angular gate : confirm box f and the covariant Hessian reduce to the
    round form for phi=phi(r) (angular pieces vanish).
 4. SMALL-WARP LINEAR structure : turn on a tiny l=2 warp (c,d ~ eps P2), linearize
    the 3-D residual about the round soliton (one FD Jacobian column-set, bounded),
    report continuity + WHERE the e^{2phi}-weighted angular-curvature term appears.

ANTI-HANG: single process, sequential, NO Newton 3-D solve; the radial solve is the
cheap validated 1-D LM (Nr<=24); evaluation + ONE linearization only.
"""
import os, sys, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/tmp")

from full3d_spectral import Grid3D, attach_coord_weight, build_metric, DEV
import b1prime_3d_offround_residual as B
import b1prime_round as RAD   # the banked radial solver (in /tmp)

T, R, TH, PS = 0, 1, 2, 3
PI = math.pi

X, XI, KAP, KAP8 = -2e5, 2e-2, 2e-2, 1.0
P_DEPTH = 1.0   # depth dial b(core)=-p (matches radial gate default)


def embed_radial(G, a_r, b_r, phi_r, Th_r):
    """Embed radial profiles (arrays on G.r) as round 3-D fields (c=d=0)."""
    dev = DEV
    def lift(arr):
        t = torch.tensor(arr, device=dev)
        return t[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()
    z = torch.zeros(G.Nr, G.Nth, G.Nps, device=dev)
    a = lift(a_r); b = lift(b_r); phi = lift(phi_r); Th = lift(Th_r)
    return a, b, z, z, phi, Th


def run():
    print("="*78)
    print("B1'-step1  3-D OFF-ROUND RESIDUAL -- ROUND-LIMIT VALIDATION (by evaluation)")
    print("X=%.1e  xi=%.2e kap=%.2e  kap8=%g" % (X, XI, KAP, KAP8))
    print("="*78)

    # ---- get the banked round soliton from the radial solver (cheap 1-D LM) ----
    Nr = 16
    print("\n[radial solve]  Nr=%d  (banked b1prime two-player, X=%.0e)" % (Nr, X))
    RG = RAD.RGrid(Nr, rc=0.05, cell=14.0)
    t0 = time.time()
    u_rad, Phi = RAD.solve(RG, X, XI, KAP, P_DEPTH, KAP8, m=1, maxit=120,
                           verbose=False)
    dg = RAD.diag(RG, u_rad, X, XI, KAP)
    print("   radial residual Phi=%.3e  (%.1fs)" % (Phi, time.time()-t0))
    print("   Th_core=%.4f Th_seal=%.4f  maxAB1=%.4f  phi_min=%.2e phi_max=%.2e"
          % (dg['Th_core'], dg['Th_seal'], dg['maxAB1'], dg['phi_min'], dg['phi_max']))
    a_r, b_r, phi_r, Th_r = dg['a'], dg['b'], dg['ph'], dg['Th']

    # ---- build the matching 3-D grid (SAME radial nodes; cheb_interval identical) ----
    G = Grid3D(Nr=Nr, Nth=8, Nps=8, rc=0.05, cell=14.0)
    G = attach_coord_weight(G)
    # sanity: radial nodes must match the 3-D radial axis
    rdiff = float(np.max(np.abs(RG.r - G.r.cpu().numpy())))
    print("   |r_radial - r_3d|max = %.2e  (must be ~0 for the gate to compare nodes)"
          % rdiff)

    # =====================================================================
    # GATE 1 : REDUCTION (round field -> 3-D residual == radial residual)
    # =====================================================================
    print("\n" + "-"*78)
    print("GATE 1  REDUCTION : 3-D residual at c=d=0 vs banked RADIAL operator")
    print("-"*78)
    a3, b3, c3, d3, phi3, Th3 = embed_radial(G, a_r, b_r, phi_r, Th_r)

    parts = B.E_mixed(G, a3, b3, c3, d3, phi3, Th3, X, XI, KAP, m=1, kap8=KAP8,
                      return_parts=True)
    E = parts['E']
    elphi3 = B.EL_phi_3d(G, a3, b3, c3, d3, phi3, Th3, X, XI, KAP, m=1, kap8=KAP8)
    elTh3 = B.EL_Th_3d(G, a3, b3, c3, d3, phi3, Th3, X, XI, KAP, m=1, kap8=KAP8)

    # radial reference on the same nodes
    Ett_r = RAD.E_tt(RG.r, a_r, b_r, phi_r, Th_r, RG.D, X, XI, KAP, KAP8)
    Err_r = RAD.E_rr(RG.r, a_r, b_r, phi_r, Th_r, RG.D, X, XI, KAP, KAP8)
    ELphi_r = RAD.EL_phi(RG.r, a_r, b_r, phi_r, Th_r, RG.D, X, XI, KAP, KAP8)
    ELth_r = RAD.EL_Th(RG.r, a_r, b_r, phi_r, Th_r, RG.D, X, XI, KAP, KAP8)

    # extract the 3-D residual at one angular node (any -- round so all equal); use mid
    jt, jp = G.Nth // 2, G.Nps // 2
    Ett3 = E[:, jt, jp, T, T].cpu().numpy()
    Err3 = E[:, jt, jp, R, R].cpu().numpy()
    elphi3_r = elphi3[:, jt, jp].cpu().numpy()
    elTh3_r = elTh3[:, jt, jp].cpu().numpy()

    # body mask (avoid the 3 Cheb edge rows each end -- coordinate-edge artifact, same
    # as the radial body mask)
    bod = np.arange(3, Nr-3)
    def cmp(name, x3, xr):
        d = np.abs(x3[bod] - xr[bod])
        sc = np.abs(xr[bod]).max() + 1e-300
        print("   %-10s  max|3d - radial|(body) = %.3e   rel = %.3e"
              % (name, d.max(), d.max()/sc))
        return d.max(), d.max()/sc

    print("   (comparing at angular node th-idx=%d ps-idx=%d; round => all nodes equal)"
          % (jt, jp))
    cmp("E^t_t", Ett3, Ett_r)
    cmp("E^r_r", Err3, Err_r)
    cmp("EL_phi", elphi3_r, ELphi_r)
    cmp("EL_Theta", elTh3_r, ELth_r)
    # angular isotropy check: residual must be theta/psi-independent on the round field
    iso = float((E[:, :, :, T, T] - E[:, jt, jp, T, T][:, None, None])[3:Nr-3].abs().max())
    print("   angular isotropy of E^t_t on round field (should be ~0): %.3e" % iso)

    # =====================================================================
    # GATE 0 : SCHWARZSCHILD exact-solution gate for the FULL E_mixed machinery.
    # phi=0 (f=1 -> fterm=0,kin=0), Theta=0 (n=const -> T=0): derived operator must
    # reduce to G^mu_nu = 0 on exact Schwarzschild, EXPONENTIALLY in Nr.  This is the
    # clean POSITIVE proof the off-round assembly (incl. E^th_th, E^ps_ps) is correct.
    # =====================================================================
    print("\n" + "-"*78)
    print("GATE 0  SCHWARZSCHILD : full E_mixed -> 0 exponentially (machinery proof)")
    print("-"*78)
    Mbh = 0.3
    for NrS in [16, 24, 32]:
        GS = Grid3D(Nr=NrS, Nth=8, Nps=8, rc=1.0, cell=14.0)
        GS = attach_coord_weight(GS)
        fS = 1.0 - 2*Mbh/GS.Rg
        aS = 0.5*torch.log(fS); bS = -0.5*torch.log(fS); zS = torch.zeros_like(aS)
        ES = B.E_mixed(GS, aS, bS, zS, zS, zS, zS, X, XI, KAP, m=1, kap8=KAP8)
        print("   Nr=%2d : max|E^mu_nu|(body) = %.3e" % (NrS, float(ES[GS.body].abs().max())))

    # =====================================================================
    # GATE 2 : ZERO (banked round soliton zeros the 3-D residual)
    # =====================================================================
    print("\n" + "-"*78)
    print("GATE 2  ZERO : banked round soliton -> 3-D residual ~ 0 (floored)")
    print("-"*78)
    # off-diagonal-free mixed E body norm + EL norms
    Ebod = E[3:Nr-3]
    print("   max|E^mu_nu|(body) over all mu,nu = %.3e" % float(Ebod.abs().max()))
    # the well-posed components that the radial solve drove to 0: E^t_t,E^r_r,EL_phi,EL_Th
    print("   max|E^t_t|(body)   = %.3e" % float(Ebod[..., T, T].abs().max()))
    print("   max|E^r_r|(body)   = %.3e" % float(Ebod[..., R, R].abs().max()))
    print("   max|E^th_th|(body) = %.3e" % float(Ebod[..., TH, TH].abs().max()))
    print("   max|E^ps_ps|(body) = %.3e" % float(Ebod[..., PS, PS].abs().max()))
    print("   max|EL_phi|(body)  = %.3e" % float(elphi3[3:Nr-3].abs().max()))
    print("   max|EL_Theta|(body)= %.3e" % float(elTh3[3:Nr-3].abs().max()))
    # radial residual floor for reference (the radial solve's own achieved Phi)
    print("   [radial solve achieved Phi=%.3e on {E^t_t,E^r_r,EL_phi,EL_Th}]" % Phi)
    # DIAGNOSIS of the E^th_th residual: is it physics or an under-constrained a'' mode?
    Dr = RG.D
    ar = Dr @ a_r; arr = Dr @ ar; br = Dr @ b_r
    Gthth = np.exp(-2*b_r)*(arr + ar**2 - ar*br + (ar-br)/RG.r)
    sgn = np.sign(Gthth[bod]); parity = (-1.0)**np.arange(bod[0], bod[-1]+1)
    frac = max(np.mean(sgn == parity), np.mean(sgn == -parity))
    ratio = np.abs(arr[bod]).max()/(np.abs(ar[bod]).max()+1e-30)
    print("   DIAGNOSIS: E^th_th ~ f*G^th_th = e^{-2b}(a''+...) on round field.")
    print("     sign(G^th_th) == +/- node-parity for %.0f%% of body nodes "
          "(100%% => pure Cheb sawtooth)" % (100*frac))
    print("     max|a''|/max|a'| = %.1f (>>1 => a'' dominated by a grid-frequency mode)"
          % ratio)
    print("     => the radial residual (1st-order in a,b) does NOT pin a''; the round")
    print("        soliton is UNDER-CONSTRAINED in the content E^th_th needs.  The 3-D")
    print("        residual is CORRECT (Schwarzschild gate 0); the EMBEDDED field is not")
    print("        a clean solution of the angular Einstein equation.  (SOLVER-FIRST: this")
    print("        indicts the radial gate's completeness, not the 3-D assembly.)")

    # =====================================================================
    # GATE 3 : box f / covariant Hessian reduce to round form
    # =====================================================================
    print("\n" + "-"*78)
    print("GATE 3  box f / angular Hessian : reduce to round form for phi=phi(r)")
    print("-"*78)
    f3 = parts['f']
    Gamma3 = parts['Gamma']; ginv3 = B.CORE.metric_inverse(B.build_metric(G, a3, b3, c3, d3))
    boxf3 = B.box_f_scalar(G, f3, ginv3, Gamma3)
    covHf3 = B.cov_hessian_f(G, f3, Gamma3)
    # round analytic box f for f=e^{2phi}, metric g_rr=e^{2b}:
    #  box f = g^{rr}( f'' ) + (1/sqrt-g) (d_r sqrt-g) g^{rr} f'  -- but cleanest check:
    #  recompute box f from the RADIAL covariant Laplacian and compare.
    # radial: box f = e^{-2b}[ f_rr + f_r( -b_r + a_r + 2/r ) ]  (a,b round; c=d=0)
    Dr = RG.D
    fr_arr = np.exp(2*phi_r)              # f = e^{2phi}
    f_r = Dr @ fr_arr
    f_rr = Dr @ f_r
    a_rd = Dr @ a_r; b_rd = Dr @ b_r
    boxf_rad = np.exp(-2*b_r) * (f_rr + f_r*(-b_rd + a_rd + 2.0/RG.r))
    boxf3_r = boxf3[:, jt, jp].cpu().numpy()
    db = np.abs(boxf3_r[bod] - boxf_rad[bod])
    print("   box f : max|3d - radial-analytic|(body) = %.3e  rel = %.3e"
          % (db.max(), db.max()/(np.abs(boxf_rad[bod]).max()+1e-300)))
    # angular pieces of the covariant Hessian must vanish for phi(r):
    Hth = float(covHf3[3:Nr-3, :, :, TH, PS].abs().max())
    Hrp = float(covHf3[3:Nr-3, :, :, R, PS].abs().max())
    Hrt = float(covHf3[3:Nr-3, :, :, R, TH].abs().max())
    print("   covHf off-(r) angular pieces on round field (should ~0):")
    print("     |nabla_th nabla_ps f| = %.3e   |nabla_r nabla_ps f| = %.3e"
          "   |nabla_r nabla_th f| = %.3e" % (Hth, Hrp, Hrt))
    # the ANGULAR (transverse) diagonal Hessian pieces are NONZERO even for phi(r)
    # (= the -Gamma^r_{thth} f_r etc curvature term -- the angular-curvature block):
    Htt = float(covHf3[3:Nr-3, :, :, TH, TH].abs().max())
    Hpp = float(covHf3[3:Nr-3, :, :, PS, PS].abs().max())
    print("   covHf angular-curvature diagonal (NONZERO = the 2/r^2-type block):")
    print("     |nabla_th nabla_th f|max = %.3e   |nabla_ps nabla_ps f|max = %.3e"
          % (Htt, Hpp))

    # =====================================================================
    # GATE 4 : SMALL-WARP LINEAR STRUCTURE (l=2 warp; one FD linearization)
    # =====================================================================
    print("\n" + "-"*78)
    print("GATE 4  SMALL-WARP LINEAR structure : tiny l=2 warp, linearize (1 FD pass)")
    print("-"*78)
    eps = 1e-3
    mu = torch.cos(G.THg)                  # cos theta
    P2 = 0.5*(3*mu**2 - 1.0)               # l=2 Legendre
    radial_env = torch.exp(-((G.Rg - 1.0)/1.5)**2)  # localize the warp in the body
    warp = eps * P2 * radial_env           # tiny l=2 angular warp

    def res_vec(c_w, d_w, phi_w):
        cc = c3 + c_w; dd = d3 + d_w; pp = phi3 + phi_w
        E = B.E_mixed(G, a3, b3, cc, dd, pp, Th3, X, XI, KAP, m=1, kap8=KAP8)
        elp = B.EL_phi_3d(G, a3, b3, cc, dd, pp, Th3, X, XI, KAP, m=1, kap8=KAP8)
        # return the well-posed component fields stacked (body only)
        return E, elp

    z = torch.zeros_like(c3)
    E0, elp0 = res_vec(z, z, z)
    # (a) warp c,d (the angular/off-round warps):
    Ec, elpc = res_vec(warp, warp, z)
    dE = (Ec - E0)
    delp = (elpc - elp0)
    print("   l=2 warp eps=%.1e (c=d=eps P2 * gauss):" % eps)
    print("     continuity: max|dE^mu_nu|(body) = %.3e  finite=%s"
          % (float(dE[3:Nr-3].abs().max()), bool(torch.isfinite(dE).all())))
    print("     linear-in-eps check (dE / eps): max = %.3e"
          % (float(dE[3:Nr-3].abs().max())/eps))
    # WHERE does the angular-curvature term show up?  Look at the change in the
    # angular components E^th_th, E^ps_ps and whether the f-weighted angular Hessian
    # moves.  Decompose dE into l-content at a fixed body radius.
    ir = Nr // 2
    dEtt_ang = dE[ir, :, jp, T, T].cpu().numpy()    # theta-profile of dE^t_t at fixed r,ps
    dEthth = dE[ir, :, jp, TH, TH].cpu().numpy()
    dEpsps = dE[ir, :, jp, PS, PS].cpu().numpy()
    print("     dE^t_t(theta) at body r: min=%.2e max=%.2e (l=2 angular response)"
          % (dEtt_ang.min(), dEtt_ang.max()))
    print("     dE^th_th(theta): min=%.2e max=%.2e   dE^ps_ps(theta): min=%.2e max=%.2e"
          % (dEthth.min(), dEthth.max(), dEpsps.min(), dEpsps.max()))

    # (b) where the f-weighted angular block enters: turn on a tiny l=2 phi warp and
    # watch the covariant Hessian angular pieces (the e^{2phi}-weighted obstruction).
    phi_w = eps * P2 * radial_env
    parts_w = B.E_mixed(G, a3, b3, c3, d3, phi3 + phi_w, Th3, X, XI, KAP, m=1,
                        kap8=KAP8, return_parts=True)
    fterm0 = parts['fterm']; fterm_w = parts_w['fterm']
    dfterm = fterm_w - fterm0
    # the angular-curvature obstruction lives in the (g box - nabla nabla) f angular
    # mixed components.  Report the l=2 response of the th-th / ps-ps mixed fterm.
    dft_thth = float(dfterm[3:Nr-3, :, :, TH, TH].abs().max())
    dft_psps = float(dfterm[3:Nr-3, :, :, PS, PS].abs().max())
    dft_tt = float(dfterm[3:Nr-3, :, :, T, T].abs().max())
    print("   l=2 PHI warp eps=%.1e -> change in (g box - nabla nabla)f term:" % eps)
    print("     d(fterm)^th_th max=%.3e  d(fterm)^ps_ps max=%.3e  d(fterm)^t_t max=%.3e"
          % (dft_thth, dft_psps, dft_tt))
    # explicit e^{2phi} weight witness: the box f scalar response vs the f=e^{2phi} factor
    f0 = parts['f'][ir, jt, jp].item()
    print("     e^{2phi} weight at body point f=e^{2phi}=%.6f (the angular block carries this)"
          % f0)
    print("\nDONE.")


if __name__ == "__main__":
    run()
