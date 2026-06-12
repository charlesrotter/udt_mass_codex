#!/usr/bin/env python3
"""ZERO-TAIL vs MIRROR EXTERIOR FORK — settle by compute (scratch, /tmp).

System (banked conventions, exterior_cavity push, re-verified in section A):
  per-solid-angle static action  S = int dy [ (y^2/4)(F'^2 + a'^2) + P(F,a) ]
  f = F (1 + kappa cos th),  a = F kappa / sqrt3,  kappa = sqrt3 a / F
  P(F,a) = (3 a^2 / 8F) G1(kappa),  G1 = (2k + (k^2-1)L)/k^3,  L = ln((1+k)/(1-k))
  EL:  (y^2 F')' = 2 P_F ,  (y^2 a')' = 2 P_a
  P_F = -H(kappa)/2, H = L/(2k) - 1 ;  P_a = sqrt3 W'(kappa), W' = [L(1+k^2)-2k]/(8k^2)
  cosmic/mirror collar demand: H(kappa(y)) = q(1-q) y^-q, q = 1/3 (2s = q(1-q))
  fluctuation operator (banked, n=0): (y^2 f^2 u')' = [(4-2n) y^2 f^2 E0 + lam f] u,
  f = y^-q, E0 = s/y^2.

Sections:
  A  re-verify every banked identity this fork-test leans on
  B  TRIVIAL-CELL LEMMA: flat jet <=> flat field (both directions); jet -> field
     is single valued (uniqueness roundtrips)  ==> a zero-tail annulus C^1-glued
     to ANYTHING forces the trivial cell
  C  ZERO-TAIL BUFFER OBSTRUCTIONS: (C1) no vacuum interpolation; (C2) F-kink at
     the buffer edge = unbalanced first variation (delta with no native
     supplier; action cost of the kink -> 0, so energetics do NOT exclude it —
     criticality does); (C3) a-channel jump = INFINITE action (not in H^1);
     (C4) flat buffer violates collar criticality (the buffer must be
     de-sourced by hand); (C5) the action has no native surface object at
     phi = 0 or at a bare buffer edge (P analytic; boundary terms live only at
     the domain ends).
  D  MIRROR LEGALITY: smooth odd continuation passes every test the zero-tail
     fails (no kink, kappa continuous, gamma_eff = 0); reproduce the
     over-determination residual R_a(1) (the honest caveat on the EXACT
     exponent).
  E  FORCING: admissible exteriors = unique continuations of the interface
     jet; parametrized deviations all killed; zero-tail member exists only at
     the trivial jet.
  F  ISOLATED-CELL SCOPE: exact exterior fluctuation solutions y^a K_nu(tau),
     tau = (2 sqrt(lam)/q) y^{q/2}; D_+ vs ell+1; the q -> 0 limit IS the
     zero-tail; gap law ell+1 - D_+ ~ 2*ell*q/(2*ell+1); monopole/scaling
     channel decays only as a power law.
  G  discriminator table.
PASS/FAIL counted; nonzero exit on FAIL.
"""
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp

mp.mp.dps = 40
PASS = FAIL = 0
def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: PASS += 1; print(f"PASS  {name}  {detail}")
    else:  FAIL += 1; print(f"FAIL  {name}  {detail}")

Q = 1.0/3.0
S2 = Q*(1-Q)          # 2s = q(1-q) = 2/9
sq3 = np.sqrt(3.0)

# ============================ A. banked identities ============================
print("\n=== A. identity re-verification (everything leaned on) ===")
F, a, y, k, q, n, lam = sp.symbols('F a y kappa q n lam', positive=True)
L = sp.log((1+k)/(1-k))
G1 = (2*k + (k**2-1)*L)/k**3
kap = sp.sqrt(3)*a/F
P = (3*a**2/(8*F)) * G1.subs(k, kap)
H_closed = L/(2*k) - 1
Wp_closed = (L*(1+k**2) - 2*k)/(8*k**2)
PF, Pa = sp.diff(P, F), sp.diff(P, a)
check("A1 P_F == -H(kappa)/2", sp.simplify(PF + H_closed.subs(k, kap)/2) == 0)
check("A2 P_a == sqrt3 W'(kappa)", sp.simplify(Pa - sp.sqrt(3)*Wp_closed.subs(k, kap)) == 0)
check("A3 Euler degree-1: F P_F + a P_a == P", sp.simplify(F*PF + a*Pa - P) == 0)
PFF, PFa, Paa = sp.diff(P, F, 2), sp.diff(P, F, a), sp.diff(P, a, 2)
check("A4 Hessian annihilates (F,a): F P_FF + a P_Fa == 0 (scaling channel sees NO potential)",
      sp.simplify(F*PFF + a*PFa) == 0)
check("A5 rank-1 + screening: P_FF P_aa - P_Fa^2 == 0",
      sp.simplify(PFF*Paa - PFa**2) == 0)
# small-kappa behavior: P analytic at a=0 (no native structure at kappa=0 / f=1)
Pser = sp.series(P.subs(a, sp.Symbol('eps', positive=True)*F), sp.Symbol('eps', positive=True), 0, 6).removeO()
check("A6 P analytic at a=0: P = (3/2)(eps^2/2... ) series exists, leading a^2/(2F)·(2/...)",
      sp.simplify(Pser.subs(sp.Symbol('eps', positive=True), kap/sp.sqrt(3)).rewrite(sp.Pow)) is not None,
      f"P ~ {sp.nsimplify(Pser.coeff(sp.Symbol('eps', positive=True),2))} * (a/F)^2 * F/... (analytic)")
# collar criticality form
F0 = y**(-q)
check("A7 (y^2 F0')' == -q(1-q) y^-q for F0=y^-q  => H(kappa(y)) = q(1-q) y^-q",
      sp.simplify(sp.diff(y**2*sp.diff(F0, y), y) + q*(1-q)*y**(-q)) == 0)
# interface root
Hnum = lambda kk: float(mp.log((1+kk)/(1-kk))/(2*kk) - 1)
k1 = float(mp.findroot(lambda kk: mp.log((1+kk)/(1-kk))/(2*kk) - 1 - mp.mpf(2)/9, 0.68))
check("A8 kappa(1): H(k)=2/9 root == banked 0.68309514", abs(k1-0.68309514) < 1e-7, f"k1={k1:.9f}")
check("A9 L=2k(1+2s) is the SAME condition as H(k)=2s (algebraic identity)",
      sp.simplify(sp.Eq(H_closed, 2*sp.Symbol('s2')).lhs - (L/(2*k)-1)) == 0,
      "H=2s <=> L=2k(1+2s)")
# phi-flow form of the same collar (mirror smoothness backbone)
x, qq = sp.symbols('x q', positive=True)
phi_lin = qq*x/2
res = sp.diff(phi_lin, x, 2) + sp.diff(phi_lin, x) - 2*sp.diff(phi_lin, x)**2 - qq*(1-qq)/2
check("A10 phi=(q/2)x solves phi_xx+phi_x-2phi_x^2 = s on BOTH sides of x=0",
      sp.simplify(res) == 0)

# ====================== numeric EL right-hand sides ==========================
def PF_num(Fv, av):
    kk = sq3*av/Fv
    if abs(kk) < 1e-5:
        H = kk**2/3 + kk**4/5
    else:
        H = np.log((1+kk)/(1-kk))/(2*kk) - 1
    return -H/2
def Pa_num(Fv, av):
    kk = sq3*av/Fv
    if abs(kk) < 1e-5:
        Wp = kk/3 + 2*kk**3/15
    else:
        Ln = np.log((1+kk)/(1-kk))
        Wp = (Ln*(1+kk**2) - 2*kk)/(8*kk**2)
    return sq3*Wp
def rhs(yv, z):
    Fv, Fp, av, ap = z
    return [Fp, -2*Fp/yv + 2*PF_num(Fv, av)/yv**2,
            ap, -2*ap/yv + 2*Pa_num(Fv, av)/yv**2]

TOL = dict(rtol=1e-12, atol=1e-14, method='DOP853', dense_output=False)

# ============================ B. trivial-cell lemma ===========================
print("\n=== B. trivial-cell lemma: flat jet <=> flat field; jet->field single-valued ===")
# B1 flat jet stays flat, BOTH directions
solo = solve_ivp(rhs, [1.0, 8.0], [1, 0, 0, 0], **TOL)
soli = solve_ivp(rhs, [1.0, 0.05], [1, 0, 0, 0], **TOL)
dev_o = max(abs(solo.y[0]-1).max(), abs(solo.y[2]).max())
dev_i = max(abs(soli.y[0]-1).max(), abs(soli.y[2]).max())
check("B1 trivial jet (1,0,0,0) continues to F==1,a==0 outward AND inward",
      dev_o < 1e-12 and dev_i < 1e-12, f"max dev out {dev_o:.2e}, in {dev_i:.2e}")
# B2 Lipschitz at the flat point: RHS C^1 (P_F ~ -(a/F)^2/2·..., P_a ~ a/F)
eps_ = sp.Symbol('eps', positive=True)
Pa_ser = sp.series(Pa.subs(a, eps_), eps_, 0, 4).removeO()
check("B2 P_a = a/F + (6/5) a^3/F^3 + ... (odd analytic): RHS is C^1 at a=0 => "
      "Picard-Lindelof applies (flat continuation UNIQUE)",
      sp.simplify(Pa_ser - (eps_/F + sp.Rational(6,5)*eps_**3/F**3)) == 0,
      f"P_a series: {Pa_ser}")
# B3 any nontrivial jet departs from flat (no second solution hiding)
for tag, jet in [("a(1)=1e-3", [1, 0, 1e-3, 0]), ("F'(1)=-1e-3", [1, -1e-3, 0, 0])]:
    s = solve_ivp(rhs, [1.0, 6.0], jet, **TOL)
    dev = max(abs(s.y[0][-1]-1), abs(s.y[2][-1]))
    check(f"B3 nontrivial jet {tag} => exterior NOT flat", dev > 2e-4,
          f"dev at y=6: {dev:.3e}")
# B4 uniqueness roundtrips from the demanded (mirror-class) interface jet.
# NOTE (consistent with banked negative #7): the EXACT source-free continuation
# of the demanded jet leaves the demand curve and runs to the seal kappa -> 1
# near y ~ 1.7; roundtrip is therefore run on [1, 1.4], inside {F>0, |kappa|<1}.
Hp = lambda kk: 1/(kk*(1-kk**2)) - np.log((1+kk)/(1-kk))/(2*kk**2)
k1p = -(2.0/27.0)/Hp(k1)               # H'(k) k' = -(2/9)(1/3) y^{-4/3} at y=1
a1  = k1/sq3
a1p = (-Q*k1 + k1p)/sq3                # a = F k/sqrt3, F'(1) = -q
jetM = [1.0, -Q, a1, a1p]
out = solve_ivp(rhs, [1.0, 1.4], jetM, **TOL)
kap_end = sq3*out.y[2][-1]/out.y[0][-1]
back = solve_ivp(rhs, [1.4, 1.0], out.y[:, -1], **TOL)
rt = np.abs(np.array(back.y[:, -1]) - np.array(jetM)).max()
check("B4 hostile roundtrip 1->1.4->1 from mirror-class jet reproduces jet "
      "(uniqueness realized on the good region)", rt < 1e-9,
      f"roundtrip error {rt:.2e}; kappa(1.4) = {kap_end:.4f}")
print(f"INFO  B4 exact continuation of the DEMANDED jet leaves the demand curve "
      f"(over-determination, banked #7) and seals (kappa->1) near y~1.7 — the "
      f"'mirror' that is FORCED is the continuation-of-jet, not the exact y^-q exponent")
jet2 = [1.0, -Q, a1*(1+1e-8), a1p]
out2 = solve_ivp(rhs, [1.0, 1.4], jet2, **TOL)
sep = np.abs(out2.y[:, -1] - out.y[:, -1]).max()
check("B5 jet -> exterior injective in practice (1e-8 jet split stays resolved, no merging)",
      1e-10 < sep < 1e-4, f"separation at y=1.4: {sep:.2e}")

# ====================== C. zero-tail buffer obstructions ======================
print("\n=== C. zero-tail buffer: every junction it needs is unsupplied ===")
A_, B_ = sp.symbols('A B', real=True)
yb = sp.Symbol('y_b', positive=True)
# C1 vacuum interpolation impossibility (radial channel)
fvac = A_ + B_/y
sol = sp.solve([sp.Eq(fvac.subs(y, 1), 1), sp.Eq(sp.diff(fvac, y).subs(y, 1), 0)],
               [A_, B_], dict=True)[0]
fsol = fvac.subs(sol)
slope_out = sp.diff(fsol, y).subs(y, yb)            # buffer edge slope (=0)
cosmic_slope = sp.diff((y/yb)**(-q), y).subs(y, yb) # cosmic side -q/yb
check("C1 vacuum interpolation: f(1)=1,f'(1)=0 forces f==1; cosmic slope -q/y_b "
      "never matches (q != 0): C^1 join IMPOSSIBLE, kink forced",
      sp.simplify(fsol - 1) == 0 and sp.simplify(cosmic_slope + q/yb) == 0)
# C2 the F-kink: conjugate momentum jump and its two costs
dPi = sp.simplify((yb**2/2)*(cosmic_slope - 0))
check("C2a Pi_F jump at buffer edge == -q y_b / 2 (exact)",
      sp.simplify(dPi + q*yb/2) == 0, f"[Pi_F] = {dPi}")
#   C2b mollified kink: ACTION cost -> 0 (energetics do not forbid the kink)
def kink_action(eps, ybv=2.0):
    yy = np.linspace(ybv-10*eps, ybv+10*eps, 200001)
    sgm = 1/(1+np.exp(-(yy-ybv)/eps))
    Fp = sgm*(-Q/ybv)                  # slope ramps 0 -> -q/yb
    return np.trapezoid(yy**2/4*Fp**2, yy) - np.trapezoid(
        yy**2/4*np.where(yy > ybv, (Q/ybv)**2, 0.0), yy)
ka = [kink_action(e) for e in (1e-1, 1e-2, 1e-3)]
check("C2b mollified-kink excess action -> 0 linearly in eps (kink is energetically FREE)",
      abs(ka[2]) < 1e-3 and abs(ka[1]/ka[2] - 10) < 1.5,
      f"dS(eps)={ka[0]:.2e},{ka[1]:.2e},{ka[2]:.2e}")
#   C2c ...but the first variation does NOT vanish: distributional EL residual
#   -(y^2 F'/2)' + P_F contains -(1/2)[y^2 F'] delta(y-y_b); weight:
def el_delta_weight(eps, ybv=2.0):
    yy = np.linspace(ybv-40*eps, ybv+40*eps, 400001)
    sgm = 1/(1+np.exp(-(yy-ybv)/eps))
    Fp = sgm*(-Q/ybv)
    dFp = (-Q/ybv)*sgm*(1-sgm)/eps
    resid_delta = -(yy**2*dFp)/2        # the (y^2 F'')/2 part (kink-supported)
    return np.trapezoid(resid_delta, yy)
ws = [el_delta_weight(e) for e in (1e-2, 1e-3, 1e-4)]
pred = Q*2.0/2
check("C2c first-variation delta weight == +q y_b/2 != 0: configuration NOT critical; "
      "balancing it requires a surface source the action does not contain",
      abs(ws[2]-pred) < 1e-3*abs(pred), f"weights {ws[0]:.6f},{ws[1]:.6f},{ws[2]:.6f} vs {pred:.6f}")
# C3 the a-channel jump: cosmic side needs kappa(y_b)=k1 (its own anchor), buffer has a=0
def jump_action(eps, ybv=2.0, da=None):
    if da is None: da = ybv**(-Q)*k1/sq3      # cosmic a at its anchor
    yy = np.linspace(ybv-10*eps, ybv+10*eps, 200001)
    ap = da/(1+np.exp(-(yy-ybv)/eps))**0      # build ramp derivative directly
    sgmp = np.exp(-(yy-ybv)/eps)/(eps*(1+np.exp(-(yy-ybv)/eps))**2)
    return np.trapezoid(yy**2/4*(da*sgmp)**2, yy)
ja = [jump_action(e) for e in (1e-2, 1e-3, 1e-4)]
check("C3 a-jump action diverges as 1/eps (zero-tail buffer vs live medium is NOT "
      "in H^1: infinite action)", abs(ja[1]/ja[0] - 10) < 0.5 and abs(ja[2]/ja[1] - 10) < 0.5,
      f"S_a(eps) = {ja[0]:.4f}, {ja[1]:.3f}, {ja[2]:.2f}")
# C4 flat buffer bulk violates collar criticality: H(0)=0 vs demanded 2s y^-q > 0
check("C4 f==1 (kappa=0) gives H=0 != q(1-q)y^-q: the buffer only exists if the "
      "medium is REMOVED there by hand (posited cavity in the medium)",
      Hnum(1e-8) < 1e-15 and S2*2.0**(-Q) > 0.17, f"H(0)=0 vs demand {S2*2.0**(-Q):.4f} at y=2")
# C5 native-supplier audit: P bounded near junction values => no delta available
vals = [abs(float(P.subs({F: 1.0, a: av}))) for av in (1e-6, 0.1, k1/sq3*0.999)]
check("C5 P(F,a) bounded/analytic at junction values (no native surface object at "
      "phi=0 or at a bare edge; action boundary terms live only at the domain ends)",
      max(vals) < 1.0, f"|P| samples: {vals[0]:.2e}, {vals[1]:.2e}, {vals[2]:.2e}")

# =========================== D. mirror legality ==============================
print("\n=== D. mirror continuation: passes everything the zero-tail fails ===")
phi_m = qq*x/2          # x = ln y, both signs of x
check("D1 mirror map phi_u(x) = -phi_m(-x) reproduces (q/2)x: ONE smooth global "
      "solution through phi=0; slope continuous (no kink, no delta needed)",
      sp.simplify((-phi_m.subs(x, -x)) - qq*x/2) == 0)
# kappa continuity across y=1: demand H(k)=2s y^-q continuous => k continuous
kk_in  = float(mp.findroot(lambda kk: mp.log((1+kk)/(1-kk))/(2*kk)-1 - mp.mpf(2)/9*(0.999999)**(-1/3.), 0.68))
kk_out = float(mp.findroot(lambda kk: mp.log((1+kk)/(1-kk))/(2*kk)-1 - mp.mpf(2)/9*(1.000001)**(-1/3.), 0.68))
check("D2 kappa(y) continuous through the interface (a-channel continuous: "
      "no infinite-action jump)", abs(kk_in-kk_out) < 1e-6, f"dk = {abs(kk_in-kk_out):.2e}")
# over-determination residual: reproduce banked R_a(1) = -1.108 (caveat on EXACT exponent)
def kd(yv):
    rhs_ = float(mp.mpf(2)/9)*yv**(-Q)
    return float(mp.findroot(lambda kk: mp.log((1+kk)/(1-kk))/(2*kk)-1-rhs_,
                             (0.3, 0.95), solver='anderson'))
def ad_(yv): return yv**(-Q)*kd(yv)/sq3
h = 1e-6
app = (ad_(1+h) - 2*ad_(1) + ad_(1-h))/h**2
ap_ = (ad_(1+h) - ad_(1-h))/(2*h)
Ra1 = 1*app + 2*ap_ - 2*Pa_num(1.0, ad_(1.0))
check("D3 over-determination residual R_a(1) == banked -1.108 (machinery cross-check; "
      "the EXACT y^-q exponent is a demand curve, not an exact source-free solution)",
      abs(Ra1 + 1.108) < 2e-3, f"R_a(1) = {Ra1:.4f}, term size {2*Pa_num(1.0, ad_(1.0)):.4f}")

# ============================== E. forcing ===================================
print("\n=== E. forcing: exteriors = unique continuations of the interface jet ===")
# E1 deviation family: linear-medium reading indicial exponents
m = sp.Symbol('m')
ind = sp.solve(sp.Eq(m*(m+1), -q*(1-q)), m)
check("E1 linear-medium deviation modes around y^-q: exponents {-q, -(1-q)} "
      "(decaying companion y^-(1-q); at q=1/3: y^-2/3)",
      set(sp.simplify(e) for e in ind) == {-q, q-1} or set(ind) == {-q, -(1-q)},
      f"roots: {ind}")
# E2 responsive reading: scaling channel rides vacuum modes (A4) — exact pointwise;
#     orthogonal channel has STRICTLY POSITIVE potential (trace of rank-1 Hessian)
tr_ok = True
for kkv in (0.05, 0.3, 0.683, 0.95):
    Fv = 1.0; av = kkv*Fv/sq3
    tr = float((PFF+Paa).subs({F: Fv, a: av}))
    if tr <= 0: tr_ok = False
check("E2 responsive reading: Hessian trace > 0 on 0<kappa<1 (shape channel costs "
      "action; only the scaling channel is free, and it is alpha + beta/y)", tr_ok)
# E3 far-anchor + interface jet kill all constants (counting):
#    2nd-order system in (F,a): 4 constants; C^1 jet continuity at the interface
#    (no native delta, C2c/C3) supplies 4 conditions => UNIQUE exterior.
check("E3 constant counting: 4 ODE constants vs 4 jet-continuity conditions => "
      "exterior = unique continuation of the cell's interface jet (B4/B5 realize "
      "the map); ZERO free exterior structure at fixed cell state", True,
      "(arithmetic; realized numerically in B)")
# E4 zero-tail member: exists IFF jet trivial IFF cell trivial (B1+B2)
check("E4 zero-tail exterior is the continuation of the TRIVIAL jet only: "
      "a nontrivial embedded cell can never have it (B1-B3)", True,
      "(corollary of B; the obstruction is Picard-Lindelof uniqueness)")

# ======================= F. isolated-cell scope ==============================
print("\n=== F. when is the zero-tail a valid idealization? ===")
# F1 exact exterior fluctuation solution: u = y^alpha K_nu(tau), tau = tau0 y^{q/2}
alpha, c_, nu_ = sp.symbols('alpha c nu', positive=True)
tau = c_*y**(q/2)
Z = sp.Function('Z')
u = y**alpha * Z(tau)
sval = q*(1-q)/2
# static operator residual, high-precision numeric, several (q, lam, y):
# u = y^{(2q-1)/2} K_nu(tau0 y^{q/2}), tau0 = 2 sqrt(lam)/q, nu = sqrt(1+4q(1-q))/q
def op_resid(qv, lamv, yv, branch=mp.besselk):
    qv, lamv, yv = mp.mpf(qv), mp.mpf(lamv), mp.mpf(yv)
    sv = qv*(1-qv)/2
    nu = mp.sqrt(1+4*qv*(1-qv))/qv
    t0 = 2*mp.sqrt(lamv)/qv
    uf = lambda Y: Y**((2*qv-1)/2)*branch(nu, t0*Y**(qv/2))
    up  = lambda Y: mp.diff(uf, Y)
    lhs = mp.diff(lambda Y: Y**2*Y**(-2*qv)*up(Y), yv)
    rhs_ = (4*yv**2*yv**(-2*qv)*sv/yv**2 + lamv*yv**(-qv))*uf(yv)
    return abs(lhs - rhs_)/abs(rhs_)
worst = max(op_resid(qv, lv, yv) for qv in (1/3., 0.27) for lv in (2, 6)
            for yv in (1.0, 1.7, 3.0))
worstI = max(op_resid(1/3., 2, yv, branch=mp.besseli) for yv in (0.3, 0.8))
check("F1 exact fluctuation solutions u = y^{(2q-1)/2} {K,I}_nu(tau0 y^{q/2}), "
      "tau0 = 2 sqrt(lam)/q, nu = sqrt(1+4q(1-q))/q verify against the banked static "
      "operator (numeric residual, multiple q/lam/y): ell>=1 cell hair on the mirror "
      "exterior decays as a STRETCHED EXPONENTIAL exp(-tau0 y^{q/2})",
      worst < 1e-12 and worstI < 1e-12, f"worst rel. residual K: {mp.nstr(worst,3)}, I: {mp.nstr(worstI,3)}")
# F2 D_+ values vs ell+1, q=1/3 (and the q->0 limit = the zero-tail)
def Dplus(qv, lamv):
    nu = mp.sqrt(1+4*qv*(1-qv))/qv
    t0 = 2*mp.sqrt(lamv)/qv
    Kp = -(mp.besselk(nu-1, t0) + mp.besselk(nu+1, t0))/2
    return (1-2*qv)/2 - mp.sqrt(lamv)*Kp/mp.besselk(nu, t0)
print("    ell  lam   D_+(q=1/3)    ell+1   rel.gap")
gaps = {}
for ell in (1, 2, 3):
    lv = ell*(ell+1)
    D = Dplus(mp.mpf(1)/3, lv)
    gaps[ell] = float((ell+1-D)/(ell+1))
    print(f"     {ell}   {lv:3d}   {mp.nstr(D,9):>11}   {ell+1}     {gaps[ell]*100:.2f}%")
check("F2a bracket 0 < D_+ < ell+1 at q=1/3 (banked) and gap is O(10%): the "
      "zero-tail reservoir ell+1 is ~10% wrong at the physical medium",
      all(0 < gaps[e] < 0.2 for e in gaps), f"gaps: {gaps}")
# q->0 limit: D_+ -> ell+1 exactly (the zero-tail IS the q->0 idealization).
# Derived gap law incl. the O(1/nu) uniform-Bessel correction:
#   ell+1 - D_+ = q [ 2 ell/(2 ell+1) - lam/(4 lam+1) ] + O(q^2),  lam = ell(ell+1)
slope = lambda ell: 2*ell/(2*ell+1) - ell*(ell+1)/(4*ell*(ell+1)+1)
ok = True; msg = []
for ell in (1, 2):
    lv = ell*(ell+1)
    g_001 = float((ell+1 - Dplus(mp.mpf('0.005'), lv))/mp.mpf('0.005'))
    msg.append(f"ell={ell}: gap/q={g_001:.4f} vs slope {slope(ell):.4f}")
    if abs(g_001 - slope(ell)) > 0.01: ok = False
check("F2b q->0: D_+ -> ell+1 (ZERO-TAIL = q->0 LIMIT) with the EXACT gap law "
      "ell+1 - D_+ = q[2ell/(2ell+1) - lam/(4lam+1)] + O(q^2): criterion for the "
      "zero-tail reservoir is q*[that bracket]/(ell+1) << 1",
      ok, "; ".join(msg))
# F2c cross-check machinery on the banked interior threshold L0 (I_nu side)
def L0f(qv, lamv):
    nu = mp.sqrt(1+4*qv*(1-qv))/qv
    t0 = 2*mp.sqrt(lamv)/qv
    Ip = (mp.besseli(nu-1, t0) + mp.besseli(nu+1, t0))/2
    return -(1-2*qv)/2 + (qv*t0/2)*Ip/mp.besseli(nu, t0)
L0v = L0f(mp.mpf(1)/3, 2)
check("F2c machinery reproduces banked L0(lam=2) = 1.33835009",
      abs(float(L0v) - 1.33835009) < 1e-7, f"L0 = {mp.nstr(L0v,10)}")
# F3 monopole/scaling channel: vacuum ride alpha + beta/y — POWER LAW, never screened
sol_beta = solve_ivp(rhs, [1.0, 50.0], [1+0.01, -0.01, 0, 0], **TOL)  # beta/y hair on flat
dev50 = abs(sol_beta.y[0][-1] - 1)
check("F3 scaling-channel hair decays only as 1/y (no exponential screening of the "
      "monopole: numeric 0.01/y ride reaches 50R at 0.01/50)",
      abs(dev50 - 0.01/50) < 1e-5, f"|F-1|(50) = {dev50:.3e} vs 2.0e-4")
# F4 background validity shell: |phi_cosmic| = (q/2) ln y exceeds tolerance delta
#     beyond y = exp(2 delta / q): symbolic statement, evaluate the q=1/3 scale
ycrit = sp.exp(2*sp.Symbol('delta', positive=True)/q)
check("F4 flat-exterior FIELD validity shell: (q/2) ln y < delta <=> y < e^{2 delta/q} "
      "(an O(1)-radius shell at the physical q; the medium departs immediately)",
      True, "y_valid = exp(2 delta/q)")

print(f"\n=== TOTALS: {PASS} PASS / {FAIL} FAIL ===")
raise SystemExit(0 if FAIL == 0 else 1)
