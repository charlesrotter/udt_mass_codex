#!/usr/bin/env python3
"""
particles_coeff_structure.py

Probe (data-blind structure first, compare last): do the REQUIRED wall
coefficients C_M1, C_E1 carry an internal sector structure consistent with
the phi-angular SEAL CORRECTION being the missing object?

Banked facts used:
  - p_F = gamma/2 bare; the public charge is shifted by a phi-angular seal
    correction Delta p_F, which is 100% angular-sourced (c=0 => 0) and ~ -2.5%
    at gamma=1 (mass_audit). The seal correction scales with the angular drive.
  - readout weights W(A3)=1/4, W(S5)=5/12, W(T8)=2/3; gaps W(S5)-W(A3)=1/6=q/2.
  - depths: e=0, mu=5(S5), tau=7(L7); transfer g=3 e^{-1/36}.

We do NOT fit. We compute the required coefficients (from data, walled) and
test whether their RATIOS / LOGS land on alphabet numbers, which would tell us
the FORM of the seal correction even though no single bare candidate hits 1e-4.
"""
import mpmath as mp
mp.mp.dps = 40
LOG=open("/tmp/particles_coeff.log","w",buffering=1)
def out(*a):
    s=" ".join(str(x) for x in a); print(s); LOG.write(s+"\n")

# alphabet numbers (data-blind)
eta=mp.mpf(1)/18; etah=eta/2; q=mp.mpf(1)/3
g=mp.mpf(3)*mp.e**(-etah)
out("g =", mp.nstr(g,18))

# DATA WALL
m_e=mp.mpf("0.51099895"); m_mu=mp.mpf("105.6583755"); m_tau=mp.mpf("1776.86")
C_M1=(m_mu/m_e)/g**5
C_E1=(m_tau/m_e)/g**7
out("C_M1=",mp.nstr(C_M1,15)," C_E1=",mp.nstr(C_E1,15))

# --- structural probes -------------------------------------------------
out("\n[1] logs of required coeffs in units of eta and eta/2:")
for nm,C in (("C_M1",C_M1),("C_E1",C_E1)):
    L=mp.log(C)
    out(f"   ln({nm})={mp.nstr(L,8)}  = {mp.nstr(L/eta,8)} * eta  = {mp.nstr(L/etah,8)} * (eta/2)")

out("\n[2] C_E1 / C_M1 and ln of it:")
rr=C_E1/C_M1
out("   ratio=",mp.nstr(rr,12)," ln(ratio)=",mp.nstr(mp.log(rr),8),
    " = ",mp.nstr(mp.log(rr)/eta,6)," eta")

# the depth difference is 7-5=2; ratio = (m_tau/m_mu)/g^2.
# If C were pure g-power residual, ln(ratio) ~ small. It's ~0.68.
out("\n[3] Is C_E1 ~ 2 and C_M1 ~ 1 with a COMMON multiplicative seal factor k?")
out("   C_M1/1 =",mp.nstr(C_M1,10),"  C_E1/2 =",mp.nstr(C_E1/2,10))
out("   if same k: k=C_M1=",mp.nstr(C_M1,10)," vs C_E1/2=",mp.nstr(C_E1/2,10),
    " differ by",mp.nstr((C_E1/2-C_M1)/C_M1,5))

out("\n[4] DEPTH-DEPENDENT seal: suppose C_d = base_d * exp(kappa * d * eta)")
out("    i.e. the seal correction accumulates per transfer rung at rate kappa*eta.")
out("    base_mu=1 (A3-anchored), base_tau=2 (S5->doubled active image), depths 5,7:")
# solve for kappa from each:
# C_M1 = 1*exp(kappa*5*eta) -> kappa = ln(C_M1)/(5 eta)
# C_E1 = 2*exp(kappa*7*eta) -> kappa = ln(C_E1/2)/(7 eta)
k_mu = mp.log(C_M1)/(5*eta)
k_tau= mp.log(C_E1/2)/(7*eta)
out("   kappa from muon  =",mp.nstr(k_mu,8))
out("   kappa from tau   =",mp.nstr(k_tau,8))
out("   agree to:",mp.nstr((k_tau-k_mu)/k_mu,4)," (a SINGLE kappa would mean one seal rate)")

out("\n[5] same with base_tau=2*(1-eta/2)=35/18 (the active-image readout):")
k_tau2= mp.log(C_E1/(mp.mpf(35)/18))/(7*eta)
out("   kappa_mu=",mp.nstr(k_mu,8)," kappa_tau(35/18 base)=",mp.nstr(k_tau2,8),
    " agree:",mp.nstr((k_tau2-k_mu)/k_mu,4))

out("\n[6] reverse: hold ONE kappa, predict the OTHER coeff (data-blind cross-check)")
out("    use kappa from a NATIVE value? test kappa=-q=-1/3, -eta=-1/18, -1/2 ...")
for knm,kv in (("-q",-q),("-1/2",mp.mpf(-1)/2),("-eta",-eta),("-1",mp.mpf(-1)),
               ("-q/2",-q/2),("-3/2",mp.mpf(-3)/2)):
    pm = 1*mp.e**(kv*5*eta)      # predict C_M1 with base 1
    pt = 2*mp.e**(kv*7*eta)      # predict C_E1 with base 2
    out(f"   kappa={knm:5s}: pred C_M1={mp.nstr(pm,10):>14s}(dev {mp.nstr((pm-C_M1)/C_M1,3)})"
        f"  C_E1={mp.nstr(pt,10):>14s}(dev {mp.nstr((pt-C_E1)/C_E1,3)})")

out("\nDONE /tmp/particles_coeff.log")
LOG.close()
