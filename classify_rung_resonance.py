#!/usr/bin/env python3
"""Class-B rung-resonance per-rung classification (OBSERVE-only, NO build).
Charles's spec 2026-07-07: geometric angular seal target T_ang,seal = 2 (= 2+H_amb, H_amb(N)=0).
Ladder data = stageD_frozen_forecast.md FORECAST table (N=20..39). Couplings Z=8, xi=kappa=1, I_4theta=1 (rigid).
Reconstructed inputs flagged. NOT a physics verdict, NOT a mass prediction. Data-blind on lepton numbers.
"""
import math

Z, XI, KAP, I4 = 8.0, 1.0, 1.0, 1.0          # THEORY couplings (canon) + rigid-normalization I_4theta=1
PHI_C = -math.log(1101.0)                      # shared anchor depth ln(1/1101) = -7.004 (x_c=1/1101)

# (N, Theta, a_seal, q)  verbatim from stageD_frozen_forecast.md:70-89 ; parity: even N -> rho_s>1, odd N -> rho_s<1
ROWS = [
 (20,66.5273,0.042512,0.41594),(21,69.6465,0.040608,0.39732),(22,72.7681,0.038866,0.38028),
 (23,75.8918,0.037266,0.36464),(24,79.0175,0.035792,0.35023),(25,82.1449,0.034429,0.33691),
 (26,85.2739,0.033165,0.32456),(27,88.4043,0.031991,0.31309),(28,91.5361,0.030896,0.30239),
 (29,94.6690,0.029873,0.29240),(30,97.8031,0.028916,0.28304),(31,100.9382,0.028018,0.27426),
 (32,104.0742,0.027173,0.26601),(33,107.2112,0.026378,0.25824),(34,110.3489,0.025628,0.25091),
 (35,113.4874,0.024919,0.24399),(36,116.6266,0.024249,0.23743),(37,119.7664,0.023613,0.23122),
 (38,122.9068,0.023009,0.22532),(39,126.0477,0.022436,0.21972),
]

def rho_s(N, a):                               # ladder: |rho_s-1| = a_seal, parity sign
    return 1.0 + a if (N % 2 == 0) else 1.0 - a

def E_ang_natural(rho, Nw):                     # (xi/2)(1+Nw^2) + (kap Nw^2/2)(I4/rho^2), rigid hedgehog I_theta=I_s=I4=1
    return 0.5*XI*(1.0 + Nw*Nw) + 0.5*KAP*Nw*Nw*(I4/rho**2)

def A_N(rho, Nw):                               # angular screen vs geometric target 2
    return E_ang_natural(rho, Nw) - 2.0

def Ir_req(q, rho, Nw, piprime_amb):            # [q^2/(Z rho^3) + kap Nw^2 I4/rho^3 - pi'_rho,amb]/(xi rho)
    return (q*q/(Z*rho**3) + KAP*Nw*Nw*I4/rho**3 - piprime_amb) / (XI*rho)

def Ir_req_value_needed(q, rho, Nw):            # the pi'_rho,amb value that would make I_r_req = 0 (resonance)
    return q*q/(Z*rho**3) + KAP*Nw*Nw*I4/rho**3

for Nw in (1, 2):
    print(f"\n{'='*118}\n N_w = {Nw}   (winding degree; INDEPENDENT of ladder node index N)   [Z=8, xi=kap=1, I_4theta=1, T_ang,seal=2]\n{'='*118}")
    print(f"{'N':>3} {'par':>4} {'Theta':>9} {'q_N':>8} {'rho_s':>8} {'Dphi_N':>8} | "
          f"{'A_N':>9} {'ang-flag':>9} | {'Ir_req(pia=0)':>13} {'pia_needed':>11} {'pia_sign':>8} {'Ir-flag':>16}")
    for (N, Th, a, q) in ROWS:
        r = rho_s(N, a); par = 'even' if N%2==0 else 'odd'
        A = A_N(r, Nw)
        ang = 'CANDIDATE' if abs(A) < 0.05 else 'blocked'
        ir0 = Ir_req(q, r, Nw, 0.0)                     # agnostic reference pi'_rho,amb = 0
        need = Ir_req_value_needed(q, r, Nw)            # pi'_rho,amb needed for resonance
        pia_sign = '+ (max)' if N%2==0 else '- (min)'   # structural: seal=rho'-node, sign(pi'_amb) = -sign(rho''_amb) = parity
        # I_r branch, structural: odd N -> pi'_amb<0 -> Ir_req strictly MORE positive (never resonance);
        #                         even N -> pi'_amb>0 -> resonance POSSIBLE iff |pi'_amb| ~ need (magnitude UNRECONSTRUCTED)
        if N % 2 == 1:
            irflag = 'RADIAL-REQ(odd)'
        else:
            irflag = 'poss-if-pia~need'
        print(f"{N:>3} {par:>4} {Th:>9.3f} {q:>8.5f} {r:>8.5f} {PHI_C:>8.4f} | "
              f"{A:>9.4f} {ang:>9} | {ir0:>13.5f} {need:>11.5f} {pia_sign:>8} {irflag:>16}")
    # summary
    As = [A_N(rho_s(N,a), Nw) for (N,_,a,_) in ROWS]
    print(f"  A_N range over N=20..39: [{min(As):+.4f}, {max(As):+.4f}]  -> "
          f"{'crosses 0 (CANDIDATE)' if (min(As) < 0 < max(As)) else 'SINGLE-SIGNED (blocked, no angular resonance)'}")
    # where would A_N=0 require rho_s?  Nw=1: 1/(2rho^2)-1=0 -> rho=0.7071 ; Nw=2: 0.5+2/rho^2 always>0
    if Nw == 1:
        print("  A_N(N_w=1)=0 would require rho_s=1/sqrt2=0.7071; ladder rho_s in [0.957,1.043] (a_seal<=0.043) NEVER reaches it.")
        # rho_s=0.707 needs a_seal=0.293 -> Theta=sqrt8/0.293=9.65 -> N+1~3 -> N~2 (far below banked scope N>=8 & forecast N=20..39)
        print("     (that crossing sits at N~2, below the banked ladder scope N>=8 and far below the forecast N=20..39.)")
    else:
        print("  A_N(N_w=2)=0.5+2/rho_s^2 >= 2.3 for all ladder rho_s; never near zero.")
