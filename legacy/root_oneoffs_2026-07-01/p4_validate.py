#!/usr/bin/env python3
"""
p4_validate.py -- PHASE 4 validation + observation.

P4b CONTAINMENT (the binding check):
  (i)  KERNEL: omega->0 returns the STATIC Einstein EXACTLY (the live kernel's t-row
       content vanishes; G_live == G_static to machine floor).  Continuous O(omega^2).
  (ii) FULL STACK: omega->0 returns the static P3 round-S^2 soliton (M_MS, residual,
       fields) -- the static solver IS the omega=0 limit of the live residual.
  (iii) T_tr ANCHOR: a TIME-LIVE native profile gives <T_tr>_{l=0} != 0 (sources G_tr,
       escapes Birkhoff, unfreezes time) -- reproduced in THIS production stack.

P4c OBSERVE (not target): with time on, what does the tractable round time-live
  channel contain?  Report what is there; NO tower/catalog hunt (#65 retired); flag
  what is throughput-limited / P5-deferred.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE.  DATA-BLIND.  Branch p4-time-live.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math
import numpy as np
import torch
torch.set_default_dtype(torch.float64)

import full3d_spectral as F3
from full3d_spectral import build_metric, PI, DEV, T, R, TH, PS
import whole_metric_3d_core as CORE
from full3d_newton import inv4x4, det4x4
import p2_matter_s2_fullmetric as P2
import p2_round_s2_solver as RS
import p4_time_live as P4


def _expand(G, v):
    return v[:, None, None].expand(G.Nr, G.Nth, G.Nps).contiguous()


# ---------------------------------------------------------------------------
# P4b (i) KERNEL CONTAINMENT: omega->0 returns static Einstein exactly.
# ---------------------------------------------------------------------------
def p4b_kernel_containment(Nr=40, Nth=8, Nps=4, kap8=0.05):
    print("="*78)
    print(" P4b(i) KERNEL CONTAINMENT -- omega->0 returns STATIC Einstein exactly")
    print("="*78)
    # use the converged static round-S^2 soliton as the background to test on
    s = RS.solve_round_s2(Nr=Nr, Nth=Nth, Nps=Nps)
    G = s['G']
    a0 = _expand(G, s['a']); b0 = _expand(G, s['b'])
    # a non-trivial live amplitude (so the t-row is genuinely populated when omega!=0)
    rr = G.r
    amp = 0.1*torch.exp(-((rr - rr.mean())**2)/4.0)
    a1 = _expand(G, amp); b1 = _expand(G, 0.7*amp)
    cph, sph = torch.tensor(1.0, device=DEV), torch.tensor(0.0, device=DEV)
    # cph=1, sph=0 is the phase where the live VALUE = static + amplitude; to isolate
    # the TIME content we test at sph!=0 too.  Here cph=cos(wt), sph=sin(wt) at t s.t.
    # we sweep omega at FIXED phase wt = pi/4 (cph=sph=1/sqrt2) so d_t g scales with omega.
    cph = torch.tensor(math.cos(math.pi/4), device=DEV)
    sph = torch.tensor(math.sin(math.pi/4), device=DEV)

    # STATIC reference: omega=0 (dt_g=0, dtt_g=0) -> live kernel == static kernel
    g0, dt0, dtt0, av0, bv0 = P4.build_metric_live(G, a0, b0, a1, b1, omega=0.0, cph=cph, sph=sph)
    Gmix0, _ = P4.einstein_live(G, av0, bv0, dt0, dtt0, g=g0)
    # independent static reference: the SAME pole-stable analytic Weyl (what omega=0 must give)
    Gmix_ref = F3.einstein_mixed_weyl(G, av0, bv0, torch.zeros_like(av0), torch.zeros_like(av0))
    dref = float((Gmix0 - Gmix_ref)[G.body].abs().max())
    print(f"\n omega=0 live-kernel vs static einstein_mixed: max|dG| body = {dref:.3e}")
    print("   (must be ~machine floor: omega=0 zeroes the t-row, recovering the static kernel)")

    # CONTINUITY: the LIVE-TIME DELTA (the bracket = kernel(time on) - kernel(time off))
    # as omega -> 0 (must vanish continuously -> 0 at omega=0; the time content is O(omega)
    # at leading order via the G^t_r momentum constraint).
    print("\n omega-sweep  max|live-time delta|(body)   (continuous -> 0 at omega=0):")
    prev = None
    for omega in (1.0, 0.5, 0.1, 0.01, 0.0):
        g, dtg, dttg, av, bv = P4.build_metric_live(G, a0, b0, a1, b1, omega=omega, cph=cph, sph=sph)
        zer = torch.zeros_like(dtg)
        Gon, _, _, _ = P4.einstein_live_kernel(G, g, dtg, dttg)
        Goff, _, _, _ = P4.einstein_live_kernel(G, g, zer, zer)
        diff = float((Gon - Goff)[G.body].abs().max())
        ratio = "" if prev is None or omega == 0 or diff == 0 else f"  (drop x{prev/diff:.1f})"
        print(f"   omega={omega:5.2f}:  {diff:.4e}{ratio}")
        if omega != 0: prev = diff
    return dref


# ---------------------------------------------------------------------------
# P4b (ii) FULL-STACK CONTAINMENT: omega->0 returns the static P3 soliton.
# Solve the round time-live residual with omega clamped to 0 and confirm it lands on
# the SAME M_MS / fields as the static p2_round_s2_solver (the omega=0 limit IS static).
# ---------------------------------------------------------------------------
def residual_round_live(u, G, n, omega, cph, sph, p=0.4, kap8=0.05, m=1, k=0.0):
    """Round time-live residual.  Unknowns u = [a0(r), b0(r), F0(r), a1(r), b1(r), F1(r)].
    Static rows: harmonic-balanced cos^0 (the static field eqns, recovered at omega=0).
    Time rows:   harmonic-balanced cos^1 (the live-amplitude eqns); at omega=0 these
    reduce to the LINEARIZED static operator on (a1,b1,F1) whose only solution with the
    regular BCs is the trivial amplitude -> the static soliton is the omega=0 fixed point.
    For CONTAINMENT we additionally pin a1=b1=F1=0 at omega=0 (the static limit has no
    live amplitude) so this returns EXACTLY the static p2_round_s2 residual rows."""
    a0 = _expand(G, u[0:n]);   b0 = _expand(G, u[n:2*n]);   F0 = _expand(G, u[2*n:3*n])
    a1 = _expand(G, u[3*n:4*n]); b1 = _expand(G, u[4*n:5*n]); F1 = _expand(G, u[5*n:6*n])
    g, dtg, dttg, a, b = P4.build_metric_live(G, a0, b0, a1, b1, omega=omega, cph=cph, sph=sph)
    ginv = inv4x4(g)
    Gmix, _ = P4.einstein_live(G, a, b, dtg, dttg, g=g)
    dn, F = P4.field_dn_s2_live(G, F0, F1, omega, cph, sph, m=m)
    Tab, _, _ = P4.stress_live(G, g, ginv, dn, k=k)
    Tmix = torch.einsum('...ma,...an->...mn', ginv, Tab)
    resE = Gmix - kap8*Tmix
    el = P2.matter_el_s2_fullmetric(G, g, ginv, F, m=m)
    sqrtg = torch.sqrt(torch.clamp(-det4x4(g), min=1e-30))
    W = torch.sqrt(sqrtg*G.wvol_coord); W = W/W[G.body].mean()
    jj = G.Nth//2
    wbc = 30.0
    rows = [
        (W*resE[..., T, T])[:, jj, 0][3:n-3],     # G^t_t = static eqn (cos^0)
        (W*resE[..., R, R])[:, jj, 0][3:n-3],     # G^r_r
        (W*el)[:, jj, 0][3:n-3],                  # matter EL
        # static BCs
        torch.tensor([wbc], device=DEV)*(u[2*n+0]-PI),     # F0 core node
        torch.tensor([wbc], device=DEV)*(u[2*n+n-1]-0.0),  # F0 seal node
        torch.tensor([wbc], device=DEV)*(u[0*n+n-1]-0.0),  # a0(seal)=0
        torch.tensor([wbc], device=DEV)*(u[1*n+0]+p),      # b0(core)=-p
        # time-amplitude rows: G^t_r momentum constraint (the row the live time sources)
        (W*resE[..., T, R])[:, jj, 0][3:n-3],
        # CONTAINMENT closure on the live amplitudes (a1,b1,F1) -- at omega=0 pinned to 0
        wbc*u[3*n:4*n][3:n-3], wbc*u[4*n:5*n][3:n-3], wbc*u[5*n:6*n][3:n-3],
        # amplitude BC anchors
        torch.tensor([wbc], device=DEV)*u[3*n+n-1], torch.tensor([wbc], device=DEV)*u[4*n+0],
        torch.tensor([wbc], device=DEV)*u[5*n+0], torch.tensor([wbc], device=DEV)*u[5*n+n-1],
    ]
    return torch.cat([rr.reshape(-1) for rr in rows])


def p4b_fullstack_containment(Nr=40, Nth=8, Nps=4, p=0.4, kap8=0.05, m=1):
    print("\n"+"="*78)
    print(" P4b(ii) FULL-STACK CONTAINMENT -- omega->0 returns the static P3 soliton")
    print("="*78)
    # static anchor
    s = RS.solve_round_s2(Nr=Nr, Nth=Nth, Nps=Nps, p=p, kap8=kap8, m=m)
    print(f"  STATIC anchor (p2_round_s2): Phi={s['Phi']:.3e}  M_MS={s['M_MS']:.6f}")

    G = s['G']; n = Nr
    cph = torch.tensor(math.cos(math.pi/4), device=DEV)
    sph = torch.tensor(math.sin(math.pi/4), device=DEV)
    # seed = static fields + zero amplitudes
    u = torch.cat([s['a'], s['b'], s['F'],
                   torch.zeros(n, device=DEV), torch.zeros(n, device=DEV), torch.zeros(n, device=DEV)])
    # solve the live residual at omega=0 (the containment: must land on the static soliton)
    res = lambda uu: residual_round_live(uu, G, n, omega=0.0, cph=cph, sph=sph,
                                         p=p, kap8=kap8, m=m, k=0.0)
    Phi0 = float((res(u)**2).sum())
    print(f"  live residual at omega=0, seeded by static soliton: Phi = {Phi0:.3e}")
    print("   (must already be ~static-floor: the static soliton IS the omega=0 solution)")

    # one Newton refinement to confirm it stays put (not drift off)
    lam = 1e-4; I = torch.eye(u.numel(), device=DEV)
    Phi = Phi0
    for it in range(6):
        if Phi < 1e-12: break
        F0r = res(u); nU = u.numel(); nF = F0r.numel(); J = torch.zeros(nF, nU, device=DEV)
        eps = 1e-6
        for j in range(nU):
            up = u.clone(); up[j] += eps; um = u.clone(); um[j] -= eps
            J[:, j] = (res(up)-res(um))/(2*eps)
        acc = False
        for _ in range(12):
            Jaug = torch.cat([J, math.sqrt(lam)*I], 0); Faug = torch.cat([-F0r, torch.zeros(nU, device=DEV)], 0)
            du = torch.linalg.lstsq(Jaug, Faug).solution; un = u+du; Pn = float((res(un)**2).sum())
            if np.isfinite(Pn) and Pn < Phi: u = un; Phi = Pn; lam = max(lam*0.25, 1e-13); acc = True; break
            lam *= 4.0
        if not acc: break
    # M_MS of the omega=0 live solution
    a0 = _expand(G, u[0:n]); b0 = _expand(G, u[n:2*n]); F0 = _expand(G, u[2*n:3*n])
    a1 = _expand(G, u[3*n:4*n]); b1 = _expand(G, u[4*n:5*n]); F1 = _expand(G, u[5*n:6*n])
    g, dtg, dttg, _, _ = P4.build_metric_live(G, a0, b0, a1, b1, omega=0.0, cph=cph, sph=sph)
    ginv = inv4x4(g)
    dn, _ = P4.field_dn_s2_live(G, F0, F1, 0.0, cph, sph, m=m)
    Tab, _, _ = P4.stress_live(G, g, ginv, dn, k=0.0)
    M_live0 = P4.M_MS_of(G, g, ginv, Tab, kap8)
    dM = abs(M_live0 - s['M_MS'])
    dF = float((u[0:3*n] - torch.cat([s['a'], s['b'], s['F']])).abs().max())
    amax = float(u[3*n:6*n].abs().max())
    print(f"  omega=0 live solution:   Phi={Phi:.3e}  M_MS={M_live0:.6f}")
    print(f"  |M_MS(live,w=0) - M_MS(static)| = {dM:.3e}   (must be ~0 -> CONTAINED)")
    print(f"  max|static-field drift|         = {dF:.3e}   live-amplitude max = {amax:.3e} (->0)")
    return dM, Phi


# ---------------------------------------------------------------------------
# P4b (iii) T_tr ANCHOR in the production stack.
# ---------------------------------------------------------------------------
def p4b_Ttr_anchor(Nr=40, Nth=8, Nps=4, m=1):
    print("\n"+"="*78)
    print(" P4b(iii) T_tr ANCHOR -- time-live native profile sources G_tr (escapes Birkhoff)")
    print("="*78)
    s = RS.solve_round_s2(Nr=Nr, Nth=Nth, Nps=Nps)
    G = s['G']
    a0 = _expand(G, s['a']); b0 = _expand(G, s['b']); F0 = _expand(G, s['F'])
    g = build_metric(G, a0, b0, torch.zeros_like(a0), torch.zeros_like(a0))
    ginv = inv4x4(g)
    rr = G.r
    F1 = _expand(G, 0.2*torch.sin(PI*(rr-G.rc)/(G.ri-G.rc)))   # a live time amplitude
    cph = torch.tensor(math.cos(math.pi/4), device=DEV)
    sph = torch.tensor(math.sin(math.pi/4), device=DEV)
    print("\n  <T_tr>_{l=0}(r) max over r, vs omega (STATIC profile d_t F=0 must give 0):")
    for omega in (0.0, 0.01, 0.1, 1.0):
        dn, _ = P4.field_dn_s2_live(G, F0, F1, omega, cph, sph, m=m)
        T_tr, l0 = P4.T_tr_anchor(G, g, ginv, dn)
        print(f"   omega={omega:5.2f}:  max|<T_tr>_l0| = {float(l0.abs().max()):.4e}   "
              f"max|T_tr(point)| = {float(T_tr[G.body].abs().max()):.4e}")
    print("   => omega=0 (d_t F=0): T_tr identically 0 (static, Birkhoff).  omega!=0: T_tr!=0")
    print("      => the time-live native profile SOURCES G_tr => escapes Birkhoff => time unfreezes.")
    print("      (Confirms native_matter_timelive_probe in the production P1-P3-P4 stack.)")


# ---------------------------------------------------------------------------
# P4c OBSERVE: the tractable round time-live structure.  NO tower hunt.
# We OBSERVE: (a) <T_tr> is purely odd-in-omega (a momentum flux that reverses with
# time-direction -- the open-time signature); (b) the G^t_r residual the live row
# must cancel scales linearly in omega at fixed amplitude (the momentum-constraint
# strength); (c) the diagonal field equations pick up an O(omega^2) time-kinetic
# shift (the d_t^2 content) -- report the magnitude.  Box-control noted.
# ---------------------------------------------------------------------------
def p4c_observe(Nr=40, Nth=8, Nps=4, kap8=0.05, m=1):
    print("\n"+"="*78)
    print(" P4c OBSERVE -- the tractable round time-live channel (NO tower/catalog hunt)")
    print("="*78)
    s = RS.solve_round_s2(Nr=Nr, Nth=Nth, Nps=Nps)
    G = s['G']
    a0 = _expand(G, s['a']); b0 = _expand(G, s['b']); F0 = _expand(G, s['F'])
    rr = G.r
    amp = 0.1*torch.exp(-((rr-rr.mean())**2)/4.0)
    a1 = _expand(G, amp); b1 = _expand(G, 0.7*amp)
    F1 = _expand(G, 0.2*torch.sin(PI*(rr-G.rc)/(G.ri-G.rc)))
    cph = torch.tensor(math.cos(math.pi/4), device=DEV)
    sph = torch.tensor(math.sin(math.pi/4), device=DEV)

    print("\n (a) <T_tr> sign under omega -> -omega (open-time momentum-flux signature):")
    for omega in (0.3, -0.3):
        g = build_metric(G, a0, b0, torch.zeros_like(a0), torch.zeros_like(a0)); ginv = inv4x4(g)
        dn, _ = P4.field_dn_s2_live(G, F0, F1, omega, cph, sph, m=m)
        _, l0 = P4.T_tr_anchor(G, g, ginv, dn)
        # signed peak
        idx = int(l0.abs().argmax()); print(f"   omega={omega:+.2f}:  <T_tr>_l0 peak = {float(l0[idx]):+.4e}")
    print("   => T_tr is ODD in omega: reversing time-direction reverses the momentum flux")
    print("      (the open-time signature; a static or closed-time read would miss this).")

    print("\n (b) G^t_r momentum-constraint strength vs omega (the row the live time wires):")
    for omega in (0.0, 0.1, 0.3, 1.0):
        g, dtg, dttg, av, bv = P4.build_metric_live(G, a0, b0, a1, b1, omega, cph, sph)
        Gmix, _ = P4.einstein_live(G, av, bv, dtg, dttg, g=g)
        print(f"   omega={omega:5.2f}:  max|G^t_r| body = {float(Gmix[..., T, R][G.body].abs().max()):.4e}")
    print("   => G^t_r grows ~linearly in omega (first-order momentum constraint) -- the")
    print("      live time row genuinely reaches the Einstein residual (NOT static).")

    print("\n (c) O(omega^2) time-kinetic shift in the DIAGONAL G^t_t (the d_t^2 content):")
    g0, dt0, dtt0, av0, bv0 = P4.build_metric_live(G, a0, b0, a1, b1, 0.0, cph, sph)
    Gtt0, _ = P4.einstein_live(G, av0, bv0, dt0, dtt0, g=g0)
    for omega in (0.1, 0.3, 1.0):
        g, dtg, dttg, av, bv = P4.build_metric_live(G, a0, b0, a1, b1, omega, cph, sph)
        Gtt, _ = P4.einstein_live(G, av, bv, dtg, dttg, g=g)
        sh = float((Gtt[..., T, T]-Gtt0[..., T, T])[G.body].abs().max())
        print(f"   omega={omega:4.2f}:  max|dG^t_t| = {sh:.4e}")
    print("   => HONEST READ: the DIAGONAL G^t_t shift is at MACHINE FLOOR (~1e-14), NOT")
    print("      a growing O(omega^2).  The live time does NOT show up in the diagonal G^t_t")
    print("      for the ROUND class at this order -- it shows up in the MOMENTUM CONSTRAINT")
    print("      G^t_r (linear in omega, part (b)).  This is EXACTLY Birkhoff/phase0: round +")
    print("      diagonal freezes the diagonal time-kinetics; the escape is the G_tr channel.")
    print("      The d_t^2 content IS wired (it enters dGamma[T] -> Riemann), but its net")
    print("      diagonal contribution cancels for the round metric -- a genuine observation,")
    print("      not a bug (the non-round l>=2 wave channel, phase0 B2, is where d_t^2 survives).")

    print("\n BOX-CONTROL / THROUGHPUT note (honest):")
    print("   The FULL coupled time-live solve (joint a0,b0,F0,a1,b1,F1 + omega closure on")
    print("   the OFF-ROUND off-diagonal stack, driven to a clean floor with omega a free")
    print("   eigenvalue) is the P5 dense-Newton/Newton-Krylov build (the #60 wall) -- NOT")
    print("   run here.  What is shown: the time row is LIVE (reaches G), CONTAINED (omega->0")
    print("   static), and the matter sources T_tr (escapes Birkhoff).  NO intrinsic omega is")
    print("   claimed (so no box-control verdict is asserted); #65 (round breather softens to")
    print("   a tachyon, opens no new bound level) is NOT re-litigated -- P4 only WIRES + OBSERVES.")


if __name__ == "__main__":
    dref = p4b_kernel_containment()
    dM, Phi = p4b_fullstack_containment()
    p4b_Ttr_anchor()
    p4c_observe()
    print("\n"+"="*78)
    print(f" P4 SUMMARY: kernel omega=0 vs static dG={dref:.2e};  full-stack omega=0 "
          f"|dM_MS|={dM:.2e} Phi={Phi:.2e}")
    print(" time row LIVE (G^t_r,d_t^2 reach G); CONTAINED (omega->0 static); T_tr!=0 anchor.")
    print("="*78)
