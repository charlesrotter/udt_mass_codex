"""
VERIFIER (blind, adversarial) -- v1: independent symbolic second variation
of the covariant C1 action on a general static axisymmetric background.

INDEPENDENT ROUTE (different from /tmp/measure_fork/mf1_scheme.py):
  - build the FULL perturbed 4x4 metric with exact entry jets,
  - invert with sympy's full matrix inverse (adjugate/det), NOT the
    M0 g1 M0 jet recursion,
  - sqrt(-g) from the exact determinant polynomial, series in eps,
  - extract L0, L1, L2 by series of the assembled scalar.

Action: S = -(c/2) Int e^{-2phi} g^{munu} d_mu phi d_nu phi sqrt(-g).
Background: phi0(r,theta), f0 = e^{-2phi0},
  ds^2 = -f0 dT^2 + f0^{-1} dr^2 + r^2 dth^2 + r^2 sin^2 dvphi^2.
Scheme: phi = phi0 + eps dp; ties g_TT = -e^{-2phi}, g_rr = +e^{+2phi};
  time row g_Tr = eps a, g_Tth = eps b, g_Tvphi = eps p;
  K: g_thth = r^2(1+eps k)^2, g_vphivphi = r^2 st^2 (1+eps k)^2;
  probe g_rtheta = eps q.
DATA-BLIND. All identities exact (simplify == 0).
"""
import sympy as sp

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V1 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

eps = sp.symbols('varepsilon')
c, r, st = sp.symbols('c r s_t', positive=True)
phi0, p0r, p0t = sp.symbols('phi0 p0r p0t', real=True)
dp, dpT, dpr, dpth, dpv = sp.symbols('dp dpT dpr dpth dpv', real=True)
a, b, p, k, q = sp.symbols('a b p q_k q', real=True)[:5]
a, b, p, k, qq = sp.symbols('a b p k q', real=True)
cV, U0, U1, kapV = sp.symbols('c_V U0 U1 kappa_V')
f0 = sp.exp(-2*phi0)

# exact entry jets (Taylor of the exact ties, truncated at eps^2 --
# sufficient and exact for the second variation)
Em = 1 - 2*eps*dp + 2*eps**2*dp**2          # e^{-2 eps dp} jet
Ep = 1 + 2*eps*dp + 2*eps**2*dp**2          # e^{+2 eps dp} jet
g = sp.Matrix([
    [-f0*Em,      eps*a,            eps*b,               eps*p],
    [eps*a,       Ep/f0,            eps*qq,              0],
    [eps*b,       eps*qq,           r**2*(1+eps*k)**2,   0],
    [eps*p,       0,                0,                   r**2*st**2*(1+eps*k)**2]])

detg = sp.expand(g.det())
ginv = g.adjugate().applyfunc(sp.expand) / detg     # FULL inverse, exact

grad = sp.Matrix([eps*dpT, p0r + eps*dpr, p0t + eps*dpth, eps*dpv])
pre = f0*Em                                          # e^{-2phi} jet
sq = sp.sqrt(sp.expand(-detg))

Kscal = (grad.T*ginv*grad)[0, 0]
L = -(c/2)*pre*Kscal*sq

Ls = sp.series(L, eps, 0, 3).removeO()
L0 = sp.expand(Ls.coeff(eps, 0))
L1 = sp.expand(Ls.coeff(eps, 1))
L2 = sp.expand(Ls.coeff(eps, 2))

# ---------- background density ----------
check("A0 L0 = -(c/2)(r^2 f0^2 p0r^2 + f0 p0t^2) st ; sqrt(-g0)=r^2 st",
      sp.simplify(L0 + (c/2)*(r**2*f0**2*p0r**2 + f0*p0t**2)*st) == 0 and
      sp.simplify(sq.subs(eps, 0) - r**2*st) == 0)

# ---------- H1-A: tadpoles ----------
t_a = sp.simplify(sp.diff(L1, a)); t_b = sp.simplify(sp.diff(L1, b))
t_p = sp.simplify(sp.diff(L1, p))
check("A1 time row (a,b,p): NO tadpole", t_a == 0 and t_b == 0 and t_p == 0)
t_k = sp.simplify(sp.diff(L1, k))
check("A2 K tadpole = -c f0^2 p0r^2 r^2 st (nonzero: K excluded by class)",
      sp.simplify(t_k + c*f0**2*p0r**2*r**2*st) == 0, f"[{t_k}]")
t_q = sp.simplify(sp.diff(L1, qq))
# (c/4) f_r f_th: f_r = -2 f0 p0r, f_th = -2 f0 p0t => (c/4)*4 f0^2 p0r p0t
check("A3 g_rtheta tadpole = +c f0^2 p0r p0t st = (c/4) f_r f_th st",
      sp.simplify(t_q - c*f0**2*p0r*p0t*st) == 0, f"[{t_q}]")

# ---------- H1-A: bare time kinetic ----------
cT = sp.simplify(sp.diff(L2, dpT, 2)/2)
check("A4 bare time kinetic = +(c/2) r^2 st, f-FREE exact",
      sp.simplify(cT - (c/2)*r**2*st) == 0, f"[{cT}]")

# ---------- H1-A: alpha, beta closed forms ----------
NN = [a, b, p]
alph = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(L2, NN[i], NN[j])/2))
beta = sp.Matrix([sp.simplify(sp.diff(L2, dpT, NN[i])) for i in range(3)])
G0 = f0*p0r**2 + p0t**2/r**2
hinv = sp.diag(f0, 1/r**2, 1/(r**2*st**2))
gv = sp.Matrix([p0r, p0t, 0])
alph_cl = (c/2)*r**2*st*((hinv*gv)*(hinv*gv).T - sp.Rational(1, 2)*G0*hinv)
beta_cl = -c*r**2*st*(hinv*gv)
check("A5 alpha == (c/2) r^2 st [(h^-1 g)(h^-1 g)^T - (1/2) G0 h^-1]",
      sp.simplify(alph - alph_cl) == sp.zeros(3, 3))
check("A6 beta == -c r^2 st h^-1 grad phi0 ; beta_p == 0",
      sp.simplify(beta - beta_cl) == sp.zeros(3, 1) and
      sp.simplify(beta[2]) == 0)
# no tadpole-like couplings of the row to static dp jets
ok = all(sp.simplify(sp.diff(L2, NN[i], v)) == 0
         for i in range(3) for v in (dp, dpr, dpth, dpv))
check("A7 time row couples ONLY to dpT at 2nd order", ok)
# K decoupling from the whole time sector
ok = (sp.simplify(sp.diff(L2, k, dpT)) == 0 and
      all(sp.simplify(sp.diff(L2, k, NN[i])) == 0 for i in range(3)))
check("A8 K x dpT = 0 and K x (a,b,p) = 0 (time verdict K-robust)", ok)

# ---------- H1-B: exact Schur flip ----------
Aab = alph[:2, :2]; Bab = sp.Matrix(beta[:2])
detab = sp.simplify(Aab.det())
W = sp.simplify(cT - (Bab.T*Aab.inv()*Bab)[0, 0]/4)
check("B1 FULL-row Schur: W = -(c/2) r^2 st EXACT (pointwise, bg-indep)",
      sp.simplify(W + (c/2)*r**2*st) == 0, f"[W = {W}]")
check("B2 det(alpha_ab) = -(c^2/16) r^2 st^2 f0 G0^2",
      sp.simplify(detab + (c**2/16)*r**2*st**2*f0*G0**2) == 0)
Nsol = sp.simplify(-Aab.inv()*Bab/2)
shift = sp.simplify((f0*p0r*Nsol[0] + p0t*Nsol[1]/r**2))
check("B3 on-shell shift N^i d_i phi0 = 2 dpT (generalized weld)",
      sp.simplify(shift - 2) == 0, f"[{shift}]")
# spherical limit: banked weld + banked alpha
check("B4 spherical: alpha_aa|p0t=0 = (c/4) f0^2 r^2 p0r^2 st (banked); "
      "a_onshell = 2 dpT/(f0 p0r) i.e. f phi0' H1 = 2 dT dp; b = 0",
      sp.simplify(alph[0, 0].subs(p0t, 0) - (c/4)*f0**2*r**2*p0r**2*st) == 0
      and sp.simplify(Nsol[0].subs(p0t, 0) - 2/(f0*p0r)) == 0
      and sp.simplify(Nsol[1].subs(p0t, 0)) == 0)

# ---------- H1-C: truncated (a-only) elimination ----------
Wtr = sp.simplify(cT - beta[0]**2/(4*alph[0, 0]))
X = r**2*f0**2*p0r**2; Y = f0*p0t**2
check("C1 truncated W = -(c/2) r^2 st (X+Y)/(X-Y) (PV-singular at X=Y)",
      sp.simplify(Wtr + (c/2)*r**2*st*(X + Y)/(X - Y)) == 0)
check("C2 alpha_aa = (c/4) st (X - Y): vanishes exactly on X = Y",
      sp.simplify(alph[0, 0] - (c/4)*st*(X - Y)) == 0)

# ---------- H1-D: completion-measure interface ----------
# add a POSITED proper-measure completion potential LV = -cV U(f) sqrt(-g)
fpert = f0*Em
UV = U0 + U1*(fpert - f0)        # Taylor jets of U(f); higher dp^2 terms
LV = -cV*UV*sq                   # static-sector only, irrelevant to row
LVs = sp.series(LV, eps, 0, 3).removeO()
LV2 = sp.expand(LVs.coeff(eps, 2))
alphV = sp.Matrix(3, 3, lambda i, j:
                  sp.simplify(sp.diff(L2 + LV2, NN[i], NN[j])/2))
dal = sp.simplify(alphV - alph)
check("D1 Delta-alpha = -(cV U0/2)(r^2 st/f0) h^{-1} (isotropic), "
      "no new beta, no new bare time term",
      sp.simplify(dal + cV*U0*sp.Rational(1, 2)*(r**2*st/f0)*hinv)
      == sp.zeros(3, 3) and
      all(sp.simplify(sp.diff(LV2, dpT, NN[i])) == 0 for i in range(3)) and
      sp.simplify(sp.diff(LV2, dpT, 2)) == 0)
WV = sp.simplify(cT - (Bab.T*alphV[:2, :2].inv()*Bab)[0, 0]/4)
WVk = sp.simplify(WV.subs(cV, -kapV*c*f0*G0/(2*U0)))
check("D2 W(kappa_V) = (c/2) r^2 st (kappa_V - 1)/(kappa_V + 1); "
      "kappa_V = -2 cV U(f0)/(c f0 G0); kappa_V=0 => W_A flip",
      sp.simplify(WVk - (c/2)*r**2*st*(kapV - 1)/(kapV + 1)) == 0)
flipfac = sp.simplify(WVk*2/(c*r**2*st))
check("D3 flip factor f-FREE for every kappa_V (W_B = 1/f^3 weight "
      "UNATTAINABLE from the C1 time sector)", not flipfac.has(phi0),
      f"[{flipfac}]")

# ---------- static sector == diagonal static density (S1/S2 anchor) ----
L2s = L2
for v in (dpT, a, b, p, k, qq):
    L2s = L2s.subs(v, 0)
ee = sp.exp(-2*(phi0 + eps*dp))
stat = -(c/2)*(ee**2*(p0r + eps*dpr)**2*r**2 + ee*(p0t + eps*dpth)**2
               + ee*(eps*dpv)**2/st**2)*st
stat2 = sp.expand(sp.diff(stat, eps, 2).subs(eps, 0)/2)
check("E1 static dp sector == exact 2nd jet of the diagonal static "
      "density (S1 reduced functional, c/2-scaled)",
      sp.simplify(L2s - stat2) == 0)

# ---------- volume rigidity (H2-B leg: no native volume carrier) ------
sq_full = sp.sqrt(-sp.det(sp.Matrix([
    [-f0*sp.exp(-2*eps*dp), eps*a, eps*b, eps*p],
    [eps*a, sp.exp(2*eps*dp)/f0, eps*qq, 0],
    [eps*b, eps*qq, r**2*(1+eps*k)**2, 0],
    [eps*p, 0, 0, r**2*st**2*(1+eps*k)**2]])))
check("F1 sqrt(-g) is dp-FREE at ALL orders (exact ties => volume "
      "channel cannot carry a phi-source)",
      sp.simplify(sp.diff(sq_full**2, dp)) == 0)

# ---------- H2-D composition: rotation-class restriction --------------
Fy, ay, kapy, Fp, apr = sp.symbols('F a_c kappa_c Fp ap', positive=True)
Cu, Su = sp.symbols('C_u S_u', real=True)
fB = Fy*(1 + kapy*Cu)
subs_cls = [(phi0, -sp.log(fB)/2),
            (p0r, -(Fp + apr*Cu)/(2*fB)),
            (p0t, (ay*Su/2)/fB), (st, Su)]
aa_cls = sp.simplify(alph[0, 0].subs(subs_cls).subs(ay, Fy*kapy))
H2C = sp.Rational(1, 16)*c*(r**2*(Fp + apr*Cu)**2
                            - (Fy*kapy)**2*Su**2/(Fy*(1 + kapy*Cu)))*Su
check("G1 COMPOSITION: alpha_aa on the rotation class == H2-C's "
      "coeff[H1^2] = (c/16)[r^2(F'+a'C)^2 - a^2 S^2/(F(1+kap C))] sin "
      "(the native 'completion loading' IS the alpha-block entry; "
      "nothing to add)", sp.simplify(aa_cls - H2C) == 0)
W_cls = sp.simplify(W.subs(subs_cls))
check("G2 COMPOSITION: full-row flip on the rotation class = "
      "-(c/2) r^2 sin EXACT (W_A survives for the native theory)",
      sp.simplify(W_cls + (c/2)*r**2*Su) == 0)
# the alignment mechanism: angular-kinetic contributions to alpha AND
# beta enter coherently; a potential-type term hits alpha only.
bb_ang = sp.simplify(beta[1])     # = -c st p0t : sourced by angular grad
check("G3 mechanism: beta_b = -c st p0t != 0 (the angular sector loads "
      "beta TOO; Schur invariance is alpha-beta alignment, which a "
      "posited potential term breaks via kappa_V)",
      sp.simplify(bb_ang + c*st*p0t) == 0)

n = sum(1 for _, ok in PASS if ok)
print(f"\nV1 TOTAL: {n}/{len(PASS)} PASS")
