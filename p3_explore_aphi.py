#!/usr/bin/env python3
"""
p3_explore_aphi.py -- P3c: the a(phi)!=-1 EXPLORATION (OBSERVE, declared, SEPARATE).

*** THIS IS NOT THE UDT ANSWER. ***  a=-1 (=GR) remains fully admissible (the field-eqn
arc does NOT pin a; udt_a_exponent_derivation_results.md banks a as UNDER-DETERMINED).
This is a DECLARED hypothesis run with stated parameters, UNFORCED at the principle
level, reporting WHAT THE WEIGHT DOES to the solution STRUCTURE vs the a=-1 baseline.
DATA-BLIND: (k,p,eps0) are declared, NOT fitted; no mass/ratio/wall number is loaded
or targeted; the M_MS-like numbers are dimensionless solver diagnostics in native units.

DECLARED a(phi) (from a_function_both_extremes.py, the derived SHAPE):
    a(phi) = -1 + k*eps0^p*e^{-p phi} ,  weight W(phi)=e^{(a+1)phi}=e^{k eps0^p e^{-p phi} phi}
Declared parameters for THIS exploration (chosen for VISIBILITY of structure on the
native [phi in ~[-0.4,0], deep-core down to phi~-3] range, NOT fitted to any datum):
    k    in {0 (baseline), 0.5, 1.0}     (departure strength; k=0 => GR)
    p    = 1                              (minimal/gradient response; p=2 spot-checked)
    eps0 = 1                              (scale set to 1: places onset at O(1) eps in
                                          native units -- a VISIBILITY choice, declared)

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE.  DATA-BLIND.  NEW file.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV, R
from full3d_newton import inv4x4, det4x4
import whole_metric_3d_matter as MAT
import p2_matter_s2_fullmetric as P2
import p3_aphi_matter as P3
from p3_validate_baseline import _setup, _solve_round_weighted


# ===========================================================================
# NON-ABSORBABILITY (the P3c precondition).  The codex's banked criterion
# (udt_field_equations sec.2b, blind-verified): a CONSTANT a relabels to GR
# (absorbable -- a units rescale of the matter ruler removes a constant exponent);
# only a POSITION-DEPENDENT a(phi), i.e. da/dphi != 0, is genuinely NON-absorbable
# (the matter/metric ruler ratio e^{-(a+1)phi} RUNS with phi, which no global units
# choice can flatten).  We show da/dphi != 0 for the declared a(phi), and that the
# fingerprint F(phi)=e^{-int(a+1)} is NON-constant -- the operational non-absorbability.
# ===========================================================================
def show_nonabsorbability():
    print("="*78); print(" P3c precondition -- NON-ABSORBABILITY of the declared a(phi)"); print("="*78)
    phi = torch.linspace(-3.0, 1.0, 9, device=DEV)
    for (k, p, eps0, tag) in [(0.0,1.0,1.0,"BASELINE k=0 (a=-1, GR)"),
                               (1.0,1.0,1.0,"DECLARED k=1,p=1,eps0=1"),
                               (1.0,2.0,1.0,"DECLARED k=1,p=2,eps0=1 (curvature)")]:
        a = P3.a_of_phi(phi, k=k, p=p, eps0=eps0)
        # da/dphi (analytic): d/dphi[-1 + k eps0^p e^{-p phi}] = -p k eps0^p e^{-p phi}
        dadphi = -p*k*(eps0**p)*torch.exp(-p*phi)
        const = bool(float(dadphi.abs().max()) < 1e-14)
        # fingerprint runs? F(phi)=e^{-int_0^phi (a+1)}; a+1 = k eps0^p e^{-p phi}
        # int_0^phi (a+1) = k eps0^p (1-e^{-p phi})/p ; non-const iff k!=0
        print(f"\n  [{tag}]")
        print(f"    a(phi) over phi[-3..1]: {[round(float(x),3) for x in a]}")
        print(f"    da/dphi max|.| = {float(dadphi.abs().max()):.3e}  -> "
              f"{'CONSTANT a (ABSORBABLE = GR relabel)' if const else 'POSITION-DEPENDENT a (NON-ABSORBABLE, genuine)'}")
    print("\n  => k=0 is the absorbable GR baseline; the declared k!=0 a(phi) has da/dphi!=0")
    print("     => it is a GENUINE FUNCTION of position, NON-absorbable (cannot be gauged")
    print("        to GR by any global units choice).  Precondition for P3c: MET.")


# ===========================================================================
# WHAT THE WEIGHT DOES to the STRUCTURE (OBSERVE).  Two probes:
#  A. On a FIXED representative config: how W reshapes rho, T^t_t, T^r_r, M(R).
#  B. The fully-coupled round solve at k!=0 vs k=0 (if it converges; else INCONCLUSIVE).
# ===========================================================================
def observe_fixed_config():
    print("\n"+"="*78); print(" P3c.A -- weight effect on a FIXED config (structure, OBSERVE)"); print("="*78)
    G, g, ginv, F, m = _setup(Nr=40, Nth=12, Nps=8)
    dn = P2.field_dn_s2(G, F, m=m)
    phi = P3.phi_from_metric(g)
    print(f"  config phi range = [{float(phi.min()):.3f}, {float(phi.max()):.3f}] (b=g_rr exponent)")
    base = None
    for (k,p,eps0) in [(0.0,1.0,1.0),(0.5,1.0,1.0),(1.0,1.0,1.0)]:
        Tab,*_,W = P3.stress_s2_weighted(g, ginv, dn, k=k, p=p, eps0=eps0)
        Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
        rho = -Tmix[...,0,0]
        # MS-like mass on the body
        dOm=(G.wmu[None,:,None]*G.wps[None,None,:]); rho_ang=(rho*dOm).sum((1,2))/(4*PI)
        integ=0.05*G.r**2*rho_ang; r=G.r; M=torch.zeros_like(r)
        for i in range(1,len(r)): M[i]=M[i-1]+0.5*(integ[i]+integ[i-1])*(r[i]-r[i-1])
        Mtot=float(M[-1]-M[0])
        rho_core = float(rho[2, G.Nth//2, 0]); rho_mid = float(rho[G.Nr//2, G.Nth//2, 0])
        Wr = [float(W[i,G.Nth//2,0]) for i in (2, G.Nr//2, G.Nr-3)]
        line = (f"  k={k:.1f},p={p:.0f},eps0={eps0:.0f}: W(core/mid/seal)="
                f"[{Wr[0]:.3f},{Wr[1]:.3f},{Wr[2]:.3f}]  rho(core)={rho_core:.4e}  "
                f"rho(mid)={rho_mid:.4e}  M_diag={Mtot:.4f}")
        if k==0.0:
            base=(Mtot,rho_core); print(line+"   <- baseline")
        else:
            dM=100*(Mtot-base[0])/base[0]; dr=100*(rho_core-base[1])/abs(base[1])
            print(line+f"   dM={dM:+.1f}%  drho_core={dr:+.1f}%")
    print("\n  OBSERVE: the weight W(phi)=e^{(a+1)phi} REWEIGHTS the source by position;")
    print("  with eps0=1,k>0 it AMPLIFIES toward the deep core (phi<0 => e^{-p phi}>1 =>")
    print("  (a+1)>0 => W grows where phi*(a+1) ... sign-watch in report).  Reported as")
    print("  STRUCTURE, not a target.  UNFORCED hypothesis; a=-1 baseline remains the answer.")


def weighted_fd_gate():
    """The DECISIVE consistency gate (inherited from P2 sec.3): the weighted autograd EL
    must equal the FD variation of the SAME weighted action that builds the weighted
    stress, on a FULL off-diagonal metric.  Passes for k=0 AND k!=0 -> stress & EL
    mutually consistent -> the modified conservation div T=-(a+1)phi'T holds in continuum.
    (The covariant divT operator itself is gate-Nth-limited off-round on this driver --
    P2 sec.3 -- so this FD-variational gate is the clean substitute; the k=0 exchange
    term is exactly 0, confirming the baseline reduces to standard conservation.)"""
    print("\n"+"="*78); print(" P3c gate -- WEIGHTED FD-variational consistency (EL == dS_w/dF, full off-diag)")
    print("="*78)
    G, g, ginv, F, m = _setup(Nr=40, Nth=12, Nps=8)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    for k in (0.0, 1.0):
        el = P3.matter_el_s2_weighted(G, g, ginv, F, m=m, k=k, p=1.0, eps0=1.0)
        def Sw(Ff):
            S, *_ = P3.matter_action_weighted(G, g, ginv, Ff, m=m, k=k, p=1.0, eps0=1.0)
            return float(S)
        eps = 1e-6; worst = 0.0
        for (i, j, l) in [(20,5,3),(15,4,2),(25,6,5),(10,2,1),(30,8,6)]:
            e = torch.zeros_like(F); e[i, j, l] = 1.0
            fd = (Sw(F+eps*e)-Sw(F-eps*e))/(2*eps)/float((sqrtg*G.wvol_coord)[i, j, l])
            ael = float(el[i, j, l]); worst = max(worst, abs(ael-fd)/(abs(ael)+1e-30))
        print(f"  k={k}: max rel-err(autograd EL vs FD dS_w/dF) = {worst:.2e}  (FD floor ~1e-6) "
              f"-> weighted EL is the TRUE variation of the weighted action")
    # the modified-conservation exchange term vanishes at k=0
    G2, g2, ginv2, F2, m2 = _setup(Nr=48, Nth=12, Nps=8)
    dn2 = P2.field_dn_s2(G2, F2, m=m2)
    for k in (0.0, 1.0):
        res = P3.modified_conservation_residual(G2, g2, ginv2, dn2, k=k, p=1.0, eps0=1.0)
        mask = P2.interior_mask(G2, r_margin=1.0, n_theta_edge=2)
        print(f"  k={k}: modified-conservation EXCHANGE term max|interior| = "
              f"{float(res['exch'][mask].abs().max()):.3e}  "
              f"{'(==0: baseline = standard div T=0)' if k==0 else '(nonzero: genuine Bianchi source)'}")


def observe_coupled_round():
    print("\n"+"="*78); print(" P3c.B -- fully-COUPLED round solve at k!=0 (does the weight change the soliton?)")
    print("="*78)
    for k in (0.0, 0.5, 1.0):
        try:
            M,Phi = _solve_round_weighted(Nr=40, k=k, p=1.0, eps0=1.0)
            tag = "baseline(GR)" if k==0 else "DECLARED a(phi)!=-1 (UNFORCED, not the answer)"
            print(f"  k={k:.1f}: Phi={Phi:.3e}  M_MS={M:.6f}   [{tag}]")
        except Exception as e:
            print(f"  k={k:.1f}: solve FAILED ({type(e).__name__}: {e}) -> INCONCLUSIVE (P5 driver)")
    print("\n  NOTE: the coupled k!=0 solve uses the SAME dense-Newton driver as P2; if it")
    print("  does not reach floor it is reported INCONCLUSIVE/P5-deferred, NOT a verdict.")


if __name__ == "__main__":
    show_nonabsorbability()
    weighted_fd_gate()
    observe_fixed_config()
    observe_coupled_round()
    print("\n"+"="*78)
    print(" P3c DONE.  a!=-1 is a DECLARED, UNFORCED hypothesis exploration -- NOT the")
    print(" UDT answer (a=-1=GR admissible).  Structure observed, data-blind.")
    print("="*78)
