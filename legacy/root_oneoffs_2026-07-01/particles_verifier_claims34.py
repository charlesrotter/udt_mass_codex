#!/usr/bin/env python3
"""
particles_verifier_claims34.py — BLIND VERIFIER for claims 3 & 4.
Independently recompute the wall residuals (no hidden tuning?), the kappa
pointer (honestly not-a-match?), and spot-check the 'SOLID' re-derivations.
Shares no code with the arm scripts.
"""
import math
from fractions import Fraction as F

def out(*a): print(" ".join(str(x) for x in a))

# ---- independent constants (recomputed from scratch) ----
N = 3
q = F(1) - F(2, N)              # 1 - 2/N
eta = q / 6
etahalf = eta / 2
out("="*72); out("CLAIM 4 — spot-check SOLID re-derivations"); out("="*72)
out("q = 1-2/N =", q, "  [arm: 1/3]", "OK" if q==F(1,3) else "FAIL")
out("eta = q/6 =", eta, " [arm: 1/18]", "OK" if eta==F(1,18) else "FAIL")
out("s = q(1-q)/2 =", q*(1-q)/2, " [arm: 1/9]", "OK" if q*(1-q)/2==F(1,9) else "FAIL")
out("1/dim End(H1) = 1/9 =", F(1,9), "  -> s == 1/dimEnd:", q*(1-q)/2==F(1,9))
# N from two-form lock C(N^2,2)=4N^2 -> N^2-1=8
import sympy as sp
nn = sp.symbols('n', positive=True)
sol = sp.solve(sp.Eq(sp.binomial(nn**2,2), 4*nn**2), nn)
out("two-form lock C(N^2,2)=4N^2 solutions:", sol, " -> N=3 forced:", 3 in [sp.nsimplify(x) for x in sol])
# epsilon-singlet C(N,3)
out("dim Lambda^3 V_N = C(N,3):", [(n,math.comb(n,3)) for n in range(1,6)])
# W(P)=Tr(P)/12
S_C1 = q**2/(4*(1-2*q))
out("S_C1/R = q^2/(4(1-2q)) =", S_C1, " == 1/12:", S_C1==F(1,12))
out("  -> W(P)=Tr(P)/12 normalization unit confirmed as 1/12 image unit.")
for nm,tr in (("A3",3),("S5",5),("T8",8)):
    out(f"  W({nm}) = {tr}/12 =", F(tr,12))
out("  W(S5)-W(A3) =", F(5,12)-F(3,12), " == q/2 =", q/2, ":", (F(5,12)-F(3,12))==q/2)

out("\n"+"="*72); out("CLAIM 3 — wall residuals: no hidden tuning?"); out("="*72)
# DATA (public PDG-ish, same as arm)
m_e, m_mu, m_tau = 0.51099895, 105.6583755, 1776.86
g = N * math.exp(-1/36)
out("g = 3 exp(-1/36) =", repr(g))
r_mu, r_tau = m_mu/m_e, m_tau/m_e
C_M1 = r_mu / g**5
C_E1 = r_tau / g**7
ratio = C_E1/C_M1
out("C_M1_req =", C_M1, " [repo wall 0.977679087638]")
out("C_E1_req =", C_E1, " [repo wall 1.93121474779]")
out("ratio_req =", ratio, " [repo wall 1.97530536575]")
out("match repo digits:",
    abs(C_M1-0.977679087638)<1e-9, abs(C_E1-1.93121474779)<1e-8, abs(ratio-1.97530536575)<1e-8)

# best single-candidate (from contract candidate list) — recompute deviations
out("\nbest single candidates (independent):")
cands_M1 = {'1':1.0,'exp(-eta/2)':math.exp(-1/36),'exp(-eta)':math.exp(-1/18),
            '35/36':35/36,'37/36':37/36,'W(T8)=2/3':2/3}
for nm,v in cands_M1.items():
    out(f"  C_M1 {nm:14s} dev={(v-C_M1)/C_M1:+.4%}")
cands_E1 = {'2':2.0,'2exp(-eta/2)':2*math.exp(-1/36),'35/18':35/18,'5/3':5/3,'3/2':1.5}
for nm,v in cands_E1.items():
    out(f"  C_E1 {nm:14s} dev={(v-C_E1)/C_E1:+.4%}")
out("  -> all > 0.01% HIT bar => registry FALSIFICATION PRESSURE stands.")

# ---- the kappa pointer: is the residual being quietly FIT? ----
out("\nkappa pointer audit (claim: NOT a match, pointer-only):")
# arm: C_d = base_d * exp(kappa*d*eta); solve kappa from muon (base 1, d=5)
# and tau (base 2, d=7).
kappa_mu  = math.log(C_M1/1.0) / (5*float(eta))   # solved to FIT muon exactly
kappa_tau = math.log(C_E1/2.0) / (7*float(eta))   # solved to FIT tau exactly
out(f"  kappa(muon, base1) = {kappa_mu:.4f}   [arm -0.0813]")
out(f"  kappa(tau, base2)  = {kappa_tau:.4f}   [arm -0.0900]")
out("  -> these kappas are SOLVED to reproduce the wall exactly (1 free param")
out("     per lepton). That two solved values agree to ~11% is the ONLY content;")
out("     it is NOT a prediction. Honest as a pointer ONLY if NOT banked as fit.")
# native rate kappa=-eta: data-blind prediction
nk = -float(eta)
pred_M1 = 1.0*math.exp(nk*5*float(eta))
pred_E1 = 2.0*math.exp(nk*7*float(eta))
out(f"  native kappa=-eta data-blind: C_M1 pred dev={(pred_M1-C_M1)/C_M1:+.4%}, "
    f"C_E1 pred dev={(pred_E1-C_E1)/C_E1:+.4%}")
out("  -> +0.7%/+1.3%: OUTSIDE the 0.1% LEAD bar. NOT a match. Pointer-only OK.")
out("\n  NO-TUNING CHECK: wall numbers are pure DATA/g^d (g fully fixed by")
out("  q,eta,N — all from N=3). No free parameter enters C_M1/C_E1/ratio.")
out("  The only 'fit' object is kappa, which the arm explicitly labels")
out("  pointer-only and NOT banked. Confirmed: no hidden tuning in the wall.")
