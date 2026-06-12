"""ADVERSARIAL INDEPENDENT RE-DERIVATION of native_weld_status_derivation.py
claims 1-5.  Own conventions, own code paths:
  - exact 4x4 symbolic metric, exact inverse via cofactors, series in eps
  - Einstein tensor via my own Christoffel/Riemann routine (different
    contraction order than the target script)
  - C1 action expanded by hand-checkable route (block 2x2 inverse done
    analytically, NOT sympy .inv() on the full 4x4)
Everything is checked against MY hand derivation (documented in comments),
then compared to the script's claims.
"""
import sympy as sp

t, r, th, ph, eps = sp.symbols("t r theta phi epsilon", real=True)
c = sp.symbols("c", positive=True)
lam = sp.symbols("lam", positive=True)
P0 = sp.Function("phi0", real=True)(r)
dp = sp.Function("dp", real=True)(t, r)     # delta phi amplitude
h1 = sp.Function("h1", real=True)(t, r)     # H1 amplitude
kk = sp.Function("kk", real=True)(t, r)     # K amplitude
Y = sp.Function("Y", real=True)(th)
f = sp.exp(-2 * P0)
P0p = sp.diff(P0, r)
E0 = sp.diff(P0, r, 2) + 2 * P0p / r - 2 * P0p**2
X = [t, r, th, ph]
FAIL = []


def ck(lbl, ok):
    print(("PASS " if ok else "FAIL ") + lbl)
    if not ok:
        FAIL.append(lbl)


def o2(e):  # keep through eps^2
    return sp.expand(sp.series(sp.expand(e), eps, 0, 3).removeO())


def o1(e):  # keep through eps^1
    return sp.expand(sp.series(sp.expand(e), eps, 0, 2).removeO())


# ===== my perturbed metric (UDT ties H0=-2dp, H2=+2dp built in via phi) =====
PHI = P0 + eps * dp * Y                       # full dilation field
gtt = -sp.exp(-2 * PHI)
grr = sp.exp(2 * PHI)
gtr = eps * h1 * Y
gthth = r**2 * (1 + eps * kk * Y)
gphph = gthth * sp.sin(th)**2

g = sp.Matrix([[gtt, gtr, 0, 0], [gtr, grr, 0, 0],
               [0, 0, gthth, 0], [0, 0, 0, gphph]])

# exact 2x2 block inverse, by hand: D = gtt*grr - gtr^2 = -(1 + eps^2 h^2 Y^2)
D = gtt * grr - gtr**2
ck("hand fact: t-r block det = -(1+eps^2 h1^2 Y^2) exactly (B=1/A automatic)",
   sp.simplify(D + 1 + eps**2 * h1**2 * Y**2) == 0)
ginv = sp.Matrix([[grr / D, -gtr / D, 0, 0], [-gtr / D, gtt / D, 0, 0],
                  [0, 0, 1 / gthth, 0], [0, 0, 0, 1 / gphph]])
ck("exact inverse check: g*ginv == Id (exact, all orders)",
   sp.simplify(g * ginv - sp.eye(4)) == sp.zeros(4, 4))
detg = D * gthth * gphph
sqg = sp.sqrt(-detg)
sqg = sqg.rewrite(sp.Abs).subs(sp.Abs(sp.sin(th)), sp.sin(th))
sqg = sp.sqrt((1 + eps**2 * h1**2 * Y**2)) * r**2 * (1 + eps * kk * Y) \
    * sp.sin(th)
ck("sqrt(-g) = r^2 sin(th) (1+eps k Y) sqrt(1+eps^2 h1^2 Y^2) exactly",
   sp.simplify(sqg**2 + detg) == 0)

# ===================== CLAIM 1: second-order C1 action ======================
dPHI = [sp.diff(PHI, x) for x in X]
grad2 = sum(ginv[i, j] * dPHI[i] * dPHI[j] for i in range(4) for j in range(4))
L = -sp.Rational(1, 2) * c * sp.exp(-2 * PHI) * grad2 * sqg
Lser = o2(L)
L2 = sp.expand(Lser.coeff(eps, 2) / sp.sin(th))
L1 = sp.expand(Lser.coeff(eps, 1) / sp.sin(th))
L0 = sp.expand(Lser.coeff(eps, 0) / sp.sin(th))
ck("L0 = -(c/2) f^2 r^2 phi0'^2 (background density)",
   sp.simplify(L0 + sp.Rational(1, 2) * c * f**2 * r**2 * P0p**2) == 0)
ck("L1 contains NO h1 (background stationary in g_tr direction: T_tr[bg]=0)",
   not L1.has(h1))
# L1 k-content is the background-EL/g_thth direction (NOT zero -> K ambiguity)
ck("L1 DOES contain k linearly (background NOT stationary in g_thth dir)",
   L1.has(kk))

# angular reduction with MY extraction
Yp = sp.Derivative(Y, th)
A_ = L2.coeff(Y**2)
B_ = L2.coeff(Yp**2)
ck("L2 angular content is only Y^2 and Y'^2",
   sp.simplify(L2 - A_ * Y**2 - B_ * Yp**2) == 0)
L2m = sp.expand(A_ + lam * B_)

dpt = sp.Derivative(dp, t)
dpr = sp.Derivative(dp, r)
# MY hand-derived closed form (derived on paper, see analysis):
L2_hand = c * (sp.Rational(1, 2) * r**2 * dpt**2
               - sp.Rational(1, 2) * f**2 * r**2 * dpr**2
               + 4 * f**2 * r**2 * P0p * dp * dpr
               - 4 * f**2 * r**2 * P0p**2 * dp**2
               - sp.Rational(1, 2) * lam * f * dp**2
               - f * r**2 * P0p * h1 * dpt
               + sp.Rational(1, 4) * f**2 * r**2 * P0p**2 * h1**2
               + f**2 * r**2 * P0p * (2 * P0p * dp - dpr) * kk)
ck("CLAIM1a: L2(mode) == my hand-derived closed form (incl. h1^2 = "
   "(c/4)f^2 r^2 phi0'^2 from sqrt(-g)[+1/2] and g^rr[-1] corrections)",
   sp.simplify(L2m - L2_hand) == 0)
ck("CLAIM1b: L2 has NO derivatives of h1 or kk (auxiliary fields)",
   not any(L2m.has(d) for d in [sp.Derivative(h1, t), sp.Derivative(h1, r),
                                sp.Derivative(kk, t), sp.Derivative(kk, r)]))
ELh = sp.expand(sp.diff(L2m, h1))
ck("CLAIM1c: EL_H1 == (c/2) r^2 f^2 phi0' (phi0' h1 - 2 e^{2phi0} d_t dp); "
   "=0 <=> f phi0' h1 = 2 d_t dp <=> f' h1 = -4 d_t dp (ALGEBRAIC weld)",
   sp.simplify(ELh - sp.Rational(1, 2) * c * r**2 * f**2 * P0p
               * (P0p * h1 - 2 * sp.exp(2 * P0) * dpt)) == 0)
# f' h1 = -4 dpt  form:
ck("CLAIM1c': f phi0' = -f'/2 so the weld reads f' h1 = -4 d_t dp",
   sp.simplify(f * P0p + sp.diff(f, r) / 2) == 0)

# physical identification: EL_H1 = 0 is exactly first-order T_tr = 0
T_tr_full = c * sp.exp(-2 * PHI) * (dPHI[0] * dPHI[1]
                                    - sp.Rational(1, 2) * gtr * grad2)
T_tr_1 = o1(T_tr_full).coeff(eps, 1)
ck("STRUCTURAL ID (mine): EL_H1 = 0  <=>  delta T_tr = 0 at first order "
   "(matter-only action varied wrt g_tr gives T_tr = 0, the no-radial-"
   "energy-flux condition; in GR this slot is G_tr = 8piG T_tr)",
   sp.simplify(T_tr_1 - c * f * (P0p * dpt
                                 - sp.Rational(1, 2) * f * P0p**2 * h1)
               * Y) == 0)

# ===================== CLAIM 2: elimination and ellipticity =================
h1_star = sp.solve(sp.Eq(ELh, 0), h1)
ck("h1* = 2 e^{2phi0} d_t dp / phi0' (unique, phi0' != 0)",
   h1_star == [2 * sp.exp(2 * P0) * dpt / P0p])
L2_eff = sp.expand(L2m.subs(h1, h1_star[0]).subs(kk, 0))
ck("CLAIM2a: time-kinetic coefficient after elimination = -(c/2) r^2 "
   "(flip from +(c/2) r^2; cross term contributes exactly -c r^2)",
   sp.simplify(sp.expand(L2_eff).coeff(dpt, 2)
               + sp.Rational(1, 2) * c * r**2) == 0)
EL_eff = sp.expand(sp.diff(L2_eff, dp) - sp.diff(sp.diff(L2_eff, dpt), t)
                   - sp.diff(sp.diff(L2_eff, dpr), r))
target = c * (r**2 * sp.diff(dp, t, 2)
              + sp.diff(r**2 * f**2 * sp.diff(dp, r), r)
              - 4 * r**2 * f**2 * E0 * dp - lam * f * dp)
ck("CLAIM2b: on-shell eq == +r^2 d_t^2 dp + d_r(r^2 f^2 d_r dp) "
   "- 4 r^2 f^2 E0 dp - lam f dp = 0 (ELLIPTIC: both 2nd-deriv coeffs >0)",
   sp.simplify(EL_eff - target) == 0)
# quadratic form WITH E0 kept (my sharpening of the no-real-omega claim)
u = sp.Function("u", real=True)(r)
w = sp.symbols("omega", real=True)
mode = sp.simplify(target.subs(dp, u * sp.cos(w * t)).doit()
                   / (c * sp.cos(w * t)))
ck("mode eq (E0 kept): (r^2 f^2 u')' = (om^2 r^2 + lam f + 4 r^2 f^2 E0) u",
   sp.simplify(mode - (-w**2 * r**2 * u
                       + sp.diff(r**2 * f**2 * sp.diff(u, r), r)
                       - lam * f * u - 4 * r**2 * f**2 * E0 * u)) == 0)
ck("integration-by-parts identity behind the spectral claim",
   sp.simplify(u * sp.diff(r**2 * f**2 * sp.diff(u, r), r)
               - sp.diff(r**2 * f**2 * u * sp.diff(u, r), r)
               + r**2 * f**2 * sp.diff(u, r)**2) == 0)
# => int[r^2 f^2 u'^2 + (lam f + 4 r^2 f^2 E0) u^2 + om^2 r^2 u^2] = 0.
# Positive-definite ONLY if E0 >= 0 (or |4 r^2 f E0| < lam pointwise).
# Vacuum E0=0: claim holds.  Sourced collar with E0<0: NOT guaranteed.

# contrast: H1 excluded by hand -> hyperbolic
L2_noh = sp.expand(L2m.subs(h1, 0).subs(kk, 0))
EL_noh = sp.expand(sp.diff(L2_noh, dp) - sp.diff(sp.diff(L2_noh, dpt), t)
                   - sp.diff(sp.diff(L2_noh, dpr), r))
ck("contrast (H1 excluded): -r^2 d_t^2 dp + d_r(r^2 f^2 d_r dp) - ... = 0 "
   "(HYPERBOLIC, speed f)",
   sp.simplify(EL_noh - c * (-r**2 * sp.diff(dp, t, 2)
                             + sp.diff(r**2 * f**2 * sp.diff(dp, r), r)
                             - 4 * r**2 * f**2 * E0 * dp
                             - lam * f * dp)) == 0)

# ===================== CLAIM 3: K parametrization ambiguity =================
gthII = r**2 * sp.exp(eps * kk * Y)
gII = sp.Matrix([[gtt, gtr, 0, 0], [gtr, grr, 0, 0],
                 [0, 0, gthII, 0], [0, 0, 0, gthII * sp.sin(th)**2]])
DII = D
ginvII = sp.Matrix([[grr / DII, -gtr / DII, 0, 0],
                    [-gtr / DII, gtt / DII, 0, 0],
                    [0, 0, 1 / gthII, 0],
                    [0, 0, 0, 1 / (gthII * sp.sin(th)**2)]])
sqgII = sp.sqrt(1 + eps**2 * h1**2 * Y**2) * r**2 * sp.exp(eps * kk * Y) \
    * sp.sin(th)
grad2II = sum(ginvII[i, j] * dPHI[i] * dPHI[j]
              for i in range(4) for j in range(4))
LII = -sp.Rational(1, 2) * c * sp.exp(-2 * PHI) * grad2II * sqgII
L2II = sp.expand(o2(LII).coeff(eps, 2) / sp.sin(th))
AII = L2II.coeff(Y**2)
BII = L2II.coeff(Yp**2)
L2mII = sp.expand(AII + lam * BII)
ELk_I = sp.expand(sp.diff(L2m, kk))
ELk_II = sp.expand(sp.diff(L2mII, kk))
ck("CLAIM3a: EL_K param I = -c r^2 f phi0' d_r(f dp)  (a dp-constraint!)",
   sp.simplify(ELk_I + c * r**2 * f * P0p * sp.diff(f * dp, r)) == 0)
ck("CLAIM3b: EL_K(II) - EL_K(I) = -(c/2) r^2 f^2 phi0'^2 k "
   "= T^th_th[bg] * r^2 * k exactly (parametrization ambiguity = banked "
   "angular stress)",
   sp.simplify(ELk_II - ELk_I
               + sp.Rational(1, 2) * c * r**2 * f**2 * P0p**2 * kk) == 0)
ck("CLAIM3b': EL_H1 is parametrization-SAFE (same in I and II)",
   sp.simplify(sp.diff(L2mII, h1) - ELh) == 0)
# the linear-k term in L1 is the nonstationarity witness:
ck("CLAIM3c: dL1/dk = -(c/2) f^2 r^2 phi0'^2 * Y = T^th_th[bg] r^2 Y "
   "(background EL in the g_thth direction != 0; in GR this is killed by "
   "the theta-theta Einstein eq, which UDT provably does not impose)",
   sp.simplify(sp.diff(L1, kk)
               + sp.Rational(1, 2) * c * f**2 * r**2 * P0p**2 * Y) == 0)

# ============== CLAIMS 4+5: my own Einstein tensor & divergences ============
# O(eps)-truncated geometry, MY routine (lower-index Riemann contraction).
gT = g.applyfunc(o1)
g0 = gT.applyfunc(lambda e: e.coeff(eps, 0))
g1 = gT.applyfunc(lambda e: e.coeff(eps, 1))
g0i = g0.inv()
giT = (g0i - eps * g0i * g1 * g0i).applyfunc(o1)


def christoffel(gm, gi):
    Gm = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for d in range(b, 4):
                e = sum(gi[a, s] * (sp.diff(gm[s, b], X[d])
                                    + sp.diff(gm[s, d], X[b])
                                    - sp.diff(gm[b, d], X[s]))
                        for s in range(4)) / 2
                e = o1(e)
                Gm[a][b][d] = e
                Gm[a][d][b] = e
    return Gm


Gam = christoffel(gT, giT)
# Ricci via my contraction R_{bd} = d_a Gam^a_{bd} - d_d Gam^a_{ba} + ...
Ric = sp.zeros(4, 4)
for b in range(4):
    for d in range(b, 4):
        e = (sum(sp.diff(Gam[a][b][d], X[a]) for a in range(4))
             - sum(sp.diff(Gam[a][b][a], X[d]) for a in range(4))
             + sum(Gam[a][a][s] * Gam[s][b][d]
                   for a in range(4) for s in range(4))
             - sum(Gam[a][d][s] * Gam[s][b][a]
                   for a in range(4) for s in range(4)))
        Ric[b, d] = o1(e)
        Ric[d, b] = Ric[b, d]
Rsc = o1(sum(giT[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Glow = (Ric - sp.Rational(1, 2) * Rsc * gT).applyfunc(o1)
Gmix = (giT * Glow).applyfunc(o1)

dG_tth = sp.simplify(Gmix[0, 2].coeff(eps, 1))
claim5 = sp.exp(2 * P0) * (-sp.Rational(1, 2) * sp.diff(f * h1, r)
                           + sp.Derivative(dp, t)
                           + sp.Rational(1, 2) * sp.Derivative(kk, t)) \
    * sp.diff(Y, th)
ck("CLAIM5a: dG^t_theta = e^{2phi0}[-1/2 d_r(e^{-2phi0}h1) + d_t dp "
   "+ 1/2 d_t k] d_th Y exactly (general phi0; my own G-routine)",
   sp.simplify(dG_tth - claim5) == 0)
ck("CLAIM5a': no Y(th) (coefficient of Y exactly 0) and no Y'' / "
   "ell(ell+1) content",
   not sp.simplify(dG_tth / sp.diff(Y, th)).has(th))

# stress tensor, full, then truncated
Tlow_full = sp.Matrix(4, 4, lambda i, j: c * sp.exp(-2 * PHI)
                      * (dPHI[i] * dPHI[j]
                         - sp.Rational(1, 2) * g[i, j] * grad2))
TlowT = Tlow_full.applyfunc(o1)
Tmix = (giT * TlowT).applyfunc(o1)
ck("CLAIM5b: dT^t_theta[C1] = 0 at first order exactly",
   sp.simplify(Tmix[0, 2].coeff(eps, 1)) == 0)


def div_mixed(Amix, nu):
    return o1(sum(sp.diff(Amix[m, nu], X[m]) for m in range(4))
              + sum(Gam[m][m][la] * Amix[la, nu]
                    for m in range(4) for la in range(4))
              - sum(Gam[la][m][nu] * Amix[m, la]
                    for m in range(4) for la in range(4)))


divG2 = div_mixed(Gmix, 2)
ck("Bianchi sanity (my routine): (div G)_theta = 0 at orders 0 and 1",
   sp.simplify(divG2.coeff(eps, 0)) == 0
   and sp.simplify(divG2.coeff(eps, 1)) == 0)
divT2 = div_mixed(Tmix, 2)
divT2_1 = sp.simplify(divT2.coeff(eps, 1))
claim4 = c * f**2 * (E0 - P0p**2) * dp * sp.diff(Y, th)
ck("CLAIM4: (div T)_theta first order = c f^2 (E0 - phi0'^2) dp d_th Y "
   "exactly; h1- and k-INDEPENDENT",
   sp.simplify(divT2_1 - claim4) == 0
   and not divT2_1.has(h1) and not divT2_1.has(kk))
divT1_0 = sp.simplify(div_mixed(Tmix, 1).coeff(eps, 0))
ck("background leak: (div T)_r = c f^2 phi0'(E0 - phi0'^2); on vacuum "
   "(E0=0) = -c f^2 phi0'^3 = (c/8) f'^3/f != 0 (gr-balance leftover)",
   sp.simplify(divT1_0 - c * f**2 * P0p * (E0 - P0p**2)) == 0)
fg = sp.Function("f", positive=True)(r)
ck("f-language: -c f^2 phi0'^3 == (c/8) f'^3 / f under phi0 = -ln(f)/2",
   sp.simplify((-c * f**2 * P0p**3).subs(P0, -sp.log(fg) / 2).doit()
               - c * sp.diff(fg, r)**3 / (8 * fg)) == 0)

# Einstein-weld vs native-weld inequivalence witness (my own witness)
fw = 1 + sp.Rational(7, 2) / r   # different vacuum member than the script's
ck("witness background solves vacuum: (r^2 f')' = 0",
   sp.simplify(sp.diff(r**2 * sp.diff(fw, r), r)) == 0)
pw = sp.sin(t) * r**2            # different breathing than the script's
hw = -4 * sp.diff(pw, t) / sp.diff(fw, r)
ck("witness: native weld satisfied, Einstein weld residual != 0 "
   "(the two welds are inequivalent equations)",
   sp.simplify(-sp.diff(fw, r) / 2 * hw - 2 * sp.diff(pw, t)) == 0
   and sp.simplify(sp.diff(fw * hw, r) - 2 * sp.diff(pw, t)) != 0)

print()
print(f"{len(FAIL)} failures" if FAIL else "ALL INDEPENDENT CHECKS PASS")
for x in FAIL:
    print("  FAIL:", x)
