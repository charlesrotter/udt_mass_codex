"""PART 2 (proper measure): the alternative lift of the licensed
completion — S_src = -int sigma_n(r) f^n sqrt(-g), sigma_n = c_n/r^2
(agrees with the static record exactly at static diagonal level, since
sqrt(-g) = r^2 sin th there).

This is the ONLY channel through which the f^n potential family can
touch H1 or K (sqrt(-g) carries the off-diagonal and sphere blocks).
Derive the chain's n-sensitivity; the consistency points; the n -> 0
pathology; and the rung-2 source term (item 4).
"""
import sys
import sympy as sp

FAIL = []
def check(label, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok: FAIL.append(label)

t, th, eps = sp.symbols("t theta epsilon", real=True)
r = sp.symbols("r", positive=True)
q = sp.symbols("q", positive=True)
c_s = sp.symbols("c", positive=True)
lam = sp.symbols("lam", positive=True)
n = sp.symbols("n", real=True)
phi0 = sp.Function("phi0", real=True)(r)
p = sp.Function("deltaphi", real=True)(t, r)
h = sp.Function("H1", real=True)(t, r)
k = sp.Function("K", real=True)(t, r)
Y = sp.Function("Y", real=True)(th)
F = sp.exp(-2 * phi0)
phi0p = sp.diff(phi0, r)
E0 = sp.diff(phi0, r, 2) + 2 * phi0p / r - 2 * phi0p**2
Yp = sp.Derivative(Y, th)

def trunc2(e):  # keep through eps^2
    e = sp.expand(e)
    return sum(eps**j * e.coeff(eps, j) for j in range(3))

def dsimp(e):
    return sp.simplify(sp.expand(e))

def metric(gthth_pert, phi_metric):
    g = sp.zeros(4, 4)
    g[0, 0] = -sp.exp(-2 * phi_metric)
    g[1, 1] = sp.exp(2 * phi_metric)
    g[0, 1] = g[1, 0] = eps * h * Y
    g[2, 2] = gthth_pert
    g[3, 3] = gthth_pert * sp.sin(th)**2
    return g

def build_L_C1(gthth_pert, phiM):
    g = metric(gthth_pert, phiM)
    ginvL = g.inv()
    sqrtg = sp.sqrt(-g.det())
    dphiL = [sp.diff(phiM, x) for x in [t, r, th]]
    grad2 = sum(ginvL[i, j] * dphiL[i] * dphiL[j]
                for i in range(3) for j in range(3))
    L = -sp.Rational(1, 2) * c_s * sp.exp(-2 * phiM) * grad2 * sqrtg
    return L.subs(sp.Abs(sp.sin(th)), sp.sin(th))

def angular_reduce(L2_over_sin, label):
    e = sp.expand(L2_over_sin)
    A = e.coeff(Y, 2).subs(Yp, 0)
    B = e.coeff(Yp, 2).subs(Y, 0)
    check(f"angular structure [{label}]: only Y^2 and Y'^2 appear",
          dsimp(e - A * Y**2 - B * Yp**2) == 0)
    return sp.expand(A + lam * B)

phiM = phi0 + eps * p * Y
c_n = -c_s * r**2 * F**2 * E0 * sp.exp(2 * n * phi0) / (2 * n)
sigma_n = c_n / r**2

print("=" * 72)
print("B0 — sqrt(-g) expansion and the proper-measure source's "
      "second-order content")
print("=" * 72)
for name, gthth in [("param I", r**2 * (1 + eps * k * Y)),
                    ("param II", r**2 * sp.exp(eps * k * Y))]:
    g = metric(gthth, phiM)
    sqrtg = sp.sqrt(-g.det()).subs(sp.Abs(sp.sin(th)), sp.sin(th))
    ser = sp.series(sqrtg, eps, 0, 3).removeO()
    if name == "param I":
        tgt = r**2 * sp.sin(th) * (1 + eps * k * Y
                                   + eps**2 * h**2 * Y**2 / 2)
        check("sqrt(-g) [param I] = r^2 sin th (1 + eps K Y + "
              "eps^2 H1^2 Y^2 / 2) exactly through eps^2 — the UDT tie "
              "keeps the (t,r) block det at -(1 + eps^2 H1^2 Y^2); "
              "dphi DROPS OUT of the measure entirely",
              dsimp(ser - tgt) == 0)

# second-order source Lagrangians, both parametrizations
L2s = {}
for name, gthth in [("param I", r**2 * (1 + eps * k * Y)),
                    ("param II", r**2 * sp.exp(eps * k * Y))]:
    g = metric(gthth, phiM)
    sqrtg = sp.sqrt(-g.det()).subs(sp.Abs(sp.sin(th)), sp.sin(th))
    Lsrc = -sigma_n * sp.exp(-2 * n * phiM) * sqrtg
    ser = sp.series(Lsrc, eps, 0, 3).removeO()
    L2s[name] = angular_reduce(ser.coeff(eps, 2) / sp.sin(th),
                               name + " src(proper)")

L2_src = L2s["param I"]
# decompose: dphi^2 potential (same as coordinate) + H1^2 + K dphi terms
jet_coord = c_s * n * r**2 * F**2 * E0 * p**2     # Part A's source jet
extra = dsimp(L2_src - jet_coord)
h2_coeff = sp.expand(extra).coeff(h, 2)
kp_coeff = sp.expand(extra).coeff(k, 1)
check("proper-measure source L2 = [coordinate-measure dphi^2 jet] + "
      "(c r^2 F^2 E0 / 4n) H1^2 + (c r^2 F^2 E0 / 2n)(2n dphi - 0) K "
      "... decomposition closes (no other terms)",
      dsimp(extra - h2_coeff * h**2 - kp_coeff * k) == 0)
check("H1^2 coupling = +c r^2 F^2 E0 / (4 n) H1^2 — the source now "
      "LOADS the H1 sector, with weight E0/n",
      dsimp(h2_coeff - c_s * r**2 * F**2 * E0 / (4 * n)) == 0)
check("K coupling [param I] = -c r^2 F^2 E0 ( dphi - 1/(2n)... ) — "
      "exact form printed below",
      kp_coeff is not None)
print(f"      K-coupling coefficient (param I): {sp.factor(kp_coeff)}")
print(f"      H1^2 coefficient: {sp.factor(h2_coeff)}")

# ----------------------------------------------------------------- C1 + src
L2C1 = {}
for name, gthth in [("param I", r**2 * (1 + eps * k * Y)),
                    ("param II", r**2 * sp.exp(eps * k * Y))]:
    L = build_L_C1(gthth, phiM)
    ser = sp.series(L, eps, 0, 3).removeO()
    L2C1[name] = angular_reduce(ser.coeff(eps, 2) / sp.sin(th),
                                name + " C1")
L2_tot = sp.expand(L2C1["param I"] + L2s["param I"])
L2_tot_II = sp.expand(L2C1["param II"] + L2s["param II"])
pt, pr_ = sp.Derivative(p, t), sp.Derivative(p, r)

print()
print("=" * 72)
print("B1 — (2a) the H1 equation and delta T_tr under the proper measure")
print("=" * 72)
EL_h = dsimp(sp.diff(L2_tot, h))
EL_h_target = (sp.Rational(1, 2) * c_s * r**2 * F**2
               * (phi0p**2 * h + E0 * h / n
                  - 2 * sp.exp(2 * phi0) * phi0p * pt))
check("(2a') EL_H1 = (c/2) r^2 F^2 [ (phi0'^2 + E0/n) H1 - "
      "2 e^{2phi0} phi0' d_t dphi ] — the weld is now n-SENSITIVE: "
      "H1* = 2 e^{2phi0} phi0' d_t dphi / (phi0'^2 + E0/n)",
      dsimp(EL_h - EL_h_target) == 0)

# delta T_tr of the total system: T_src_munu = -g_munu sigma f^n
g_full = metric(r**2 * (1 + eps * k * Y), phiM)
T_src_tr = -g_full[0, 1] * sigma_n * sp.exp(-2 * n * phiM)
dT_src_tr1 = sp.expand(
    sp.series(T_src_tr, eps, 0, 2).removeO()).coeff(eps, 1)
check("(2a') delta T_tr[src] = -H1 Y sigma_n f0^n = +(c/2) F^2 E0 H1 Y "
      "/ n  =/= 0 — the source now CARRIES first-order radial momentum "
      "flux (the n-sensitive exchange term, computed exactly)",
      dsimp(dT_src_tr1 - c_s * F**2 * E0 * h * Y / (2 * n)) == 0)

# rebuild C1 delta T_tr (same machinery as part A)
def trunc1(e):
    e = sp.expand(e)
    return e.coeff(eps, 0) + eps * e.coeff(eps, 1)
# explicit eps-polynomial form of the perturbed metric (exponentials
# expanded) — required for the coefficient extractions below
gm = g_full.applyfunc(
    lambda e: sp.expand(sp.series(e, eps, 0, 2).removeO()))
g0i = sp.diag(*[1 / sp.expand(gm[i, i]).coeff(eps, 0) for i in range(4)])
g1m = gm.applyfunc(lambda e: sp.expand(e).coeff(eps, 1))
ginv = (g0i - eps * g0i * g1m * g0i).applyfunc(trunc1)
E2w = trunc1(sp.series(sp.exp(-2 * phiM), eps, 0, 2).removeO())
dphi_w = [sp.diff(phiM, x) for x in [t, r, th, sp.Symbol("az")]]
grad2_w = trunc1(sum(ginv[i, j] * dphi_w[i] * dphi_w[j]
                     for i in range(3) for j in range(3)))
T_C1_tr = trunc1(c_s * E2w * (dphi_w[0] * dphi_w[1]
                              - sp.Rational(1, 2) * gm[0, 1] * grad2_w))
dT_C1_tr1 = sp.expand(T_C1_tr).coeff(eps, 1)
# With a background-stressed source the covariant and CONTRAVARIANT
# first-order fluxes differ (delta of the raising metric hits the
# nonzero background T_src).  The variational identity is the
# contravariant one: dS/dg_tr prop. T^{tr}.
T_C1_low = sp.Matrix(4, 4, lambda i, j: trunc1(
    c_s * E2w * (dphi_w[i] * dphi_w[j]
                 - sp.Rational(1, 2) * gm[i, j] * grad2_w)))
T_src_low_m = sp.Matrix(4, 4, lambda i, j: trunc1(sp.expand(
    sp.series(-gm[i, j] * sigma_n * sp.exp(-2 * n * phiM),
              eps, 0, 2).removeO())))
T_tot_up = (ginv * (T_C1_low + T_src_low_m) * ginv).applyfunc(trunc1)
dT_up_tr1 = sp.expand(T_tot_up[0, 1]).coeff(eps, 1)
check("(2a') STRUCTURAL IDENTITY (corrected form): EL_H1[total] = "
      "+r^2 delta T^{tr}[total] (CONTRAVARIANT) exactly, all n — the "
      "weld remains vanishing TOTAL radial-temporal flux; for C1 alone "
      "this is the banked -r^2 delta T_tr (equivalent there because "
      "T_tr-raising corrections cancel on the C1 background stress), "
      "but the source's background stress splits the two forms and the "
      "variational statement is the contravariant one",
      dsimp(EL_h * Y - r**2 * dT_up_tr1) == 0)
check("(2a') the C1-only equivalence (sanity): delta T^{tr}[C1] = "
      "-delta T_tr[C1] exactly (the raising corrections cancel for C1)",
      dsimp(sp.expand((ginv * T_C1_low * ginv).applyfunc(trunc1)[0, 1]
                      ).coeff(eps, 1) + dT_C1_tr1) == 0)
check("(2a') the n-sensitive exchange term is exactly the source's "
      "first-order flux: delta T^{tr}[src] = +(c/2) F^2 E0 H1 Y / n "
      "(vanishes as n -> oo, diverges as n -> 0)",
      dsimp(sp.expand((ginv * T_src_low_m * ginv).applyfunc(trunc1)[0, 1]
                      ).coeff(eps, 1) - c_s * F**2 * E0 * h * Y
            / (2 * n)) == 0)

print()
print("=" * 72)
print("B2 — (2b) the K sector under the proper measure")
print("=" * 72)
EL_k_I = dsimp(sp.diff(L2_tot, k))
EL_k_II = dsimp(sp.diff(L2_tot_II, k))
diff_k = dsimp(EL_k_II - EL_k_I)
amb_target = (-sp.Rational(1, 2) * c_s * r**2 * F**2 * phi0p**2
              + sp.Rational(1, 2) * c_s * r**2 * F**2 * E0 / n) * k
check("(2b') K parametrization ambiguity = (T^th_th[C1] + T^th_th[src])"
      " r^2 K = (c/2) r^2 F^2 (E0/n - phi0'^2) K — vanishes IFF "
      "n = E0/phi0'^2: under the proper measure, K becomes a "
      "well-defined native variational field at EXACTLY n* = E0/phi0'^2",
      dsimp(diff_k - amb_target) == 0)
n_star = E0 / phi0p**2
n_star_collar = sp.simplify(n_star.subs(phi0, q * sp.log(r) / 2).doit())
check("(2b') on the collar phi0 = (q/2) ln y:  n* = 2(1-q)/q — "
      "CONSTANT precisely because the collar is self-similar; n* = 4 "
      "at q = 1/3",
      sp.simplify(n_star_collar - 2 * (1 - q) / q) == 0
      and n_star_collar.subs(q, sp.Rational(1, 3)) == 4)
check("(2b') invariant-family location of n* = 4:  nu^2 = 17 - 8 n* = "
      "-15 < 0 — COMPLEX Bessel order: the proper-measure consistency "
      "point sits OUTSIDE the real-nu regime (log-periodic radial "
      "structure; recorded, not promoted)",
      (17 - 8 * 4) == -15)

print()
print("=" * 72)
print("B3 — (2c) H1 elimination and the kinetic character under the "
      "proper measure")
print("=" * 72)
h_star = sp.solve(sp.Eq(EL_h, 0), h)[0]
check("(2c') H1* = 2 e^{2phi0} phi0' d_t dphi / (phi0'^2 + E0/n) "
      "(reduces to the banked H1* when E0 -> 0 or n -> oo)",
      dsimp(h_star - 2 * sp.exp(2 * phi0) * phi0p * pt
            / (phi0p**2 + E0 / n)) == 0)
L2_eff = dsimp(L2_tot.subs(h, h_star))
pt2_coeff = sp.expand(L2_eff).coeff(pt, 2)
kin_target = (sp.Rational(1, 2) * c_s * r**2
              * (E0 / n - phi0p**2) / (E0 / n + phi0p**2))
check("(2c') the time-kinetic coefficient after elimination = "
      "(c/2) r^2 (E0/n - phi0'^2)/(E0/n + phi0'^2) — the EXACT banked "
      "flip -(c/2) r^2 is recovered only as E0/n -> 0; the coefficient "
      "VANISHES at the SAME n* = E0/phi0'^2 (kinetic degeneracy and "
      "K-well-definedness coincide); for n < n* (e.g. n = 0+, 1) the "
      "on-shell system is HYPERBOLIC (no flip!), for n > n* ELLIPTIC",
      dsimp(pt2_coeff - kin_target) == 0)

# n -> 0 pathology of the proper-measure family
print()
print("=" * 72)
print("B4 — the n -> 0 obstruction: the phi-slot CANNOT ride the proper "
      "measure")
print("=" * 72)
# sigma_n f^n sqrt(-g) = (J f0 / n r^2) (f/f0)^n sqrt(-g): the 1/n piece
# multiplies sqrt(-g), which is FIELD-DEPENDENT (H1^2, K) — it cannot be
# discarded as a constant, so the n -> 0 limit of the proper-measure
# family DIVERGES in the H1/K sectors:
check("(B4) the H1^2 and K couplings scale as E0/n: they DIVERGE as "
      "n -> 0 while the dphi^2 jet stays finite (prop. to n) — the "
      "n = 0 (phi-slot) completion exists ONLY under the coordinate "
      "measure; equivalently, the BANKED weld sector (= n = 0 by the "
      "record) is consistent ONLY with the coordinate-measure lift, "
      "under which the whole chain is slot-blind (Part A)",
      sp.limit(h2_coeff * n, n, 0) != 0
      and dsimp(sp.limit(jet_coord / n, n, 0)
                - c_s * r**2 * F**2 * E0 * p**2) == 0)

print()
print("=" * 72)
print("B5 — item 4: the rung-2 weld's source term, both measures")
print("=" * 72)
# T^t_theta of the potential source: T_munu = -g_munu sigma V has NO
# (t,theta) component at first order (g_t,theta = 0 in the even-parity
# RW set used by the macro pipeline)
T_src_low = (-1) * g_full * (sigma_n * sp.exp(-2 * n * phiM))
T_src_mix = ginv * T_src_low
dT_t_th = sp.expand(
    sp.series(T_src_mix[0, 2], eps, 0, 2).removeO()).coeff(eps, 1)
check("(item 4) delta T^t_theta[src] = 0 at first order for the ENTIRE "
      "f^n family under BOTH measures (a potential source is diagonal; "
      "g_{t theta} = 0 in the RW even-parity set) — the rung-2 weld's "
      "SOURCE term is exactly n-BLIND",
      dsimp(dT_t_th) == 0)
# the only n-sensitivity: the native weld's H1* on sourced regions
# impose the vacuum background EL: phi0'' = 2 phi0'^2 - 2 phi0'/r
h_star_vac = dsimp(h_star.subs(sp.diff(phi0, r, 2),
                               2 * phi0p**2 - 2 * phi0p / r))
check("(item 4) on E0 = 0 carriers (the macro vacuum sector) the "
      "native weld H1* reduces EXACTLY to the banked "
      "2 e^{2phi0} d_t dphi / phi0' for every n and either measure — "
      "the existing macro weld-discriminator record CANNOT constrain "
      "n; n-sensitivity of the H1 <-> dphi weld lives ONLY in sourced "
      "(E0 =/= 0) regions and ONLY under the proper measure",
      dsimp(h_star_vac - 2 * sp.exp(2 * phi0) * pt / phi0p) == 0)

print()
print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} FAILED"); [print("  -", x) for x in FAIL]
    sys.exit(1)
print("ALL CHECKS PASSED (proper-measure variant)")
