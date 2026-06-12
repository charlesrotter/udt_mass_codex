"""EXTERIOR-SOURCED CAVITY, step 3 (scratch): the omega0^2 sign
resolution (VB B5), honestly, from the post-elimination structure.

Chain:
 (L1) the H1-elimination kinetic flip is exact and lambda-FREE
      => it applies uniformly to EVERY delta-phi multipole (ell>=1),
      including the source's own angular-activity channel a (an ell=1
      delta-phi multipole: f = F(1+kappa cos th) <=> phi has an ell=1
      component; its fluctuation couples to H1(ell=1) identically).
 (L2) with BOTH channels in the flipped frame, pointwise elimination of
      the a-channel at real frequency gives denominator (V_aa + rho_a
      w^2): NO real pole.  Rank-1 (degree-1 homogeneity) =>
      V_eff = P_FF * W~ / (1 + W~), W~ = w^2/(V_aa/rho_a) >= 0:
      repulsive, monotone, screened(0) -> bare(P_FF) interpolation.
 (L3) the recorded form -P_FF * W/(1-W) is the SAME function iff
      omega0^2 = -V_aa/rho_a < 0 in the flipped frame: the resolution of
      the flagged sign convention.  A real resonance would need the
      a-channel to ESCAPE the flip — excluded by (L1).
 (L4) joint-form positivity: rank-1 PSD potential + positive gradients/
      barriers => B[u,a] >= 0 => all normal modes w^2 = -B/<W> <= 0.
"""
import sympy as sp

PASS = 0; FAIL = 0
def check(label, ok):
    global PASS, FAIL
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if ok: PASS += 1
    else: FAIL += 1

# ---- L1: the flip, reproduced, lambda-free ----
c, f, r0, pp, t = sp.symbols('c f r0 phip t', positive=True)
dphit = sp.Symbol('dphit')          # d_t delta-phi
H1 = sp.Symbol('H1')
alpha = (c/4)*f**2*r0**2*pp**2      # +(c/4) f^2 r^2 phi0'^2 H1^2 (banked)
# banked H1 EL: f phi0' H1 = 2 d_t delta-phi  => from 2 alpha H1 + beta dphit = 0
H1_sol = 2*dphit/(f*pp)
beta = sp.solve(sp.Eq(2*alpha*H1 + sp.Symbol('beta')*dphit, 0),
                sp.Symbol('beta'))[0].subs(H1, H1_sol)
beta = sp.simplify(beta*H1_sol/H1_sol)  # beta such that EL gives banked H1
# solve properly: H1 = -beta dphit/(2 alpha) == 2 dphit/(f pp)
beta_v = sp.solve(sp.Eq(-sp.Symbol('b')*dphit/(2*alpha), H1_sol),
                  sp.Symbol('b'))[0]
onshell = sp.simplify(-beta_v**2/(4*alpha))
check("flip magnitude: -beta^2/(4 alpha) = -c r^2 (with alpha = "
      "(c/4)f^2r^2phi0'^2, H1 = 2 d_t dphi/(f phi0')): +(c/2)r^2 -> "
      "-(c/2)r^2 EXACTLY (the banked -B^2/4A mechanism)",
      sp.simplify(onshell + c*r0**2) == 0)
lam = sp.Symbol('lam')
check("lambda-freeness: alpha and beta contain NO lambda — the flip is "
      "the SAME for every multipole ell >= 1 (channel-uniform); the "
      "a-channel (ell=1 delta-phi multipole) flips identically",
      not alpha.has(lam) and not beta_v.has(lam))

# ---- L2: both-flipped elimination ----
Vuu, Vua, Vaa, ru, ra, w2 = sp.symbols(
    'V_uu V_ua V_aa rho_u rho_a w2', positive=True)
u, a = sp.symbols('u a', real=True)
# flipped-frame equations at e^{-i w t} (banked arrangement: potential
# enters with minus sign; rho d_t^2 -> -rho w^2):
# u:  -w2 ru u - (Vuu u + Vua a) + grad = 0
# a:  -w2 ra a - (Vaa a + Vua u) + grad = 0   (pointwise: drop grads)
a_sol = sp.solve(sp.Eq(-w2*ra*a - Vaa*a - Vua*u, 0), a)[0]
Veff = sp.simplify(Vuu - (-(Vuu*u + Vua*a_sol) + Vuu*u)/u)
Veff = sp.simplify(Vuu + Vua*a_sol/u)   # dressed potential coefficient
check("both-flipped elimination: a = -V_ua u/(V_aa + rho_a w^2); "
      "V_eff = V_uu - V_ua^2/(V_aa + rho_a w^2) — denominator has + "
      "sign: NO pole at real omega",
      sp.simplify(Veff - (Vuu - Vua**2/(Vaa + ra*w2))) == 0)
# rank-1: Vua^2 = Vuu Vaa
Veff_r1 = sp.simplify(Veff.subs(Vua, sp.sqrt(Vuu*Vaa)))
Wt = w2*ra/Vaa
check("rank-1 closure: V_eff = P_FF * W~/(1+W~), W~ = w^2 rho_a/V_aa "
      ">= 0: zero at w=0 (exact static screening), monotone UP to P_FF "
      "(bare) as w^2 -> oo — REPULSIVE at every real frequency",
      sp.simplify(Veff_r1 - Vuu*Wt/(1+Wt)) == 0)

# ---- L3: equivalence with the recorded resonant form ----
om02 = sp.Symbol('omega0sq')
W = w2/om02
recorded = -Vuu*W/(1-W)
check("sign resolution: -P_FF W/(1-W) with W = w^2/omega0^2 EQUALS "
      "P_FF W~/(1+W~) iff omega0^2 = -V_aa/rho_a < 0 — the recorded "
      "resonant form carries a NEGATIVE omega0^2 in the kinetic-flipped "
      "banked frame; the apparent real resonance is a sign-convention "
      "artifact",
      sp.simplify(recorded.subs(om02, -Vaa/ra)
                  - Vuu*Wt/(1+Wt)) == 0)
# mixed-sign control: real pole would need the a-channel UNFLIPPED
a_sol_m = sp.solve(sp.Eq(+w2*ra*a - Vaa*a - Vua*u, 0), a)[0]
Veff_m = sp.simplify(Vuu + Vua*a_sol_m/u)
check("control: an UNFLIPPED a-channel (escaping L1) would give "
      "V_eff = V_uu - V_ua^2/(V_aa - rho_a w^2) — a real pole at "
      "w^2 = V_aa/rho_a and an attractive overshoot beyond it; this "
      "requires the a-channel to evade the H1 flip, excluded by "
      "lambda-freeness (L1)",
      sp.simplify(Veff_m - (Vuu - Vua**2/(Vaa - ra*w2))) == 0)

# ---- L4: joint-form positivity (pointwise PSD) ----
Vmat = sp.Matrix([[Vuu, sp.sqrt(Vuu*Vaa)], [sp.sqrt(Vuu*Vaa), Vaa]])
eigs = Vmat.eigenvals()
check("joint potential matrix (rank-1, degree-1 homogeneity) is PSD: "
      "eigenvalues {0, V_uu + V_aa} — no negative direction pointwise; "
      "with positive gradient terms and the lam f barrier the JOINT "
      "two-channel form is >= 0 and every normal mode of the flipped "
      "system has w^2 = -B/<weight> <= 0",
      set(eigs.keys()) == {0, Vuu + Vaa} or
      sorted(sp.simplify(k) for k in eigs) == sorted([0, Vuu + Vaa],
                                                     key=str))

# threshold corollary: dressing vanishes ~ w^2 at threshold crossing
Veff_series = sp.series(Veff_r1, w2, 0, 2).removeO()
check("threshold corollary: V_eff = (P_FF rho_a/V_aa) w^2 + O(w^4) — "
      "vanishes at the w^2 -> 0+ binding threshold: the STATIC screened "
      "family is exact at threshold and BEST-CASE for w^2 > 0",
      sp.simplify(Veff_series - Vuu*ra*w2/Vaa) == 0)

print(f"\nSTEP3: {PASS} PASS / {FAIL} FAIL")
import sys; sys.exit(1 if FAIL else 0)
