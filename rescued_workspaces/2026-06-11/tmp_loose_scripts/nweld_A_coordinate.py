"""PART 1 + 2 (coordinate measure): n-symbolic weld fluctuation system.

Total action = C1 + licensed source completion S_src = -int c_n(r) f^n
(coordinate measure, per solid angle; Lagrangian sign such that the
static record's functional = -(Lagrangian)).  Criticality fixes
    c_n = -c r^2 F^2 E0 f0^{-n} / (2n)      [general background phi0(r)]
which on the collar f0 = y^{-q} equals the record's c_n = J f0^{1-n}/n,
J = -s y^{-q}, s = q(1-q)/2.

Derive the full time-dependent second-order system (dphi, H1, K), n
symbolic; check every element of the banked weld chain for
n-sensitivity; anchor at n=0 (banked operator, exact) and n=1
(halved E0); reproduce the static invariant family mu(n) = (1-n)q(1-q).
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
n = sp.symbols("n", real=True)          # the source slot exponent (symbolic!)
phi0 = sp.Function("phi0", real=True)(r)
p = sp.Function("deltaphi", real=True)(t, r)
h = sp.Function("H1", real=True)(t, r)
k = sp.Function("K", real=True)(t, r)
Y = sp.Function("Y", real=True)(th)
F = sp.exp(-2 * phi0)
phi0p = sp.diff(phi0, r)
E0 = sp.diff(phi0, r, 2) + 2 * phi0p / r - 2 * phi0p**2
Yp = sp.Derivative(Y, th)
coords = [t, r, th]

def trunc(e):
    e = sp.expand(e)
    return e.coeff(eps, 0) + eps * e.coeff(eps, 1)

def dsimp(e):
    return sp.simplify(sp.expand(e))

# --------------------------------------------------------------- C1 sector
def build_L(gthth_pert, phi_metric, phi_scalar):
    g = sp.zeros(4, 4)
    g[0, 0] = -sp.exp(-2 * phi_metric)
    g[1, 1] = sp.exp(2 * phi_metric)
    g[0, 1] = g[1, 0] = eps * h * Y
    g[2, 2] = gthth_pert
    g[3, 3] = gthth_pert * sp.sin(th)**2
    ginvL = g.inv()
    sqrtg = sp.sqrt(-g.det())
    dphiL = [sp.diff(phi_scalar, x) for x in [t, r, th]]
    grad2 = sum(ginvL[i, j] * dphiL[i] * dphiL[j]
                for i in range(3) for j in range(3))
    L = -sp.Rational(1, 2) * c_s * sp.exp(-2 * phi_scalar) * grad2 * sqrtg
    return L.subs(sp.Abs(sp.sin(th)), sp.sin(th))

def angular_reduce(L2_over_sin, label):
    e = sp.expand(L2_over_sin)
    A = e.coeff(Y, 2).subs(Yp, 0)
    B = e.coeff(Yp, 2).subs(Y, 0)
    check(f"angular structure [{label}]: only Y^2 and Y'^2 appear",
          dsimp(e - A * Y**2 - B * Yp**2) == 0)
    return sp.expand(A + lam * B)

phiM = phi0 + eps * p * Y

# --------------------------------------------------- source sector (coord)
# c_n(r): explicit function of r fixed by criticality of the TOTAL action
c_n = -c_s * r**2 * F**2 * E0 * sp.exp(2 * n * phi0) / (2 * n)   # f0^{-n}=e^{2n phi0}
L_src_full = -c_n * sp.exp(-2 * n * phiM) * sp.sin(th)   # coordinate measure
# (sin(th) is the coordinate angular measure; NO sqrt(-g), NO metric fields)

print("=" * 72)
print("A0 — source normalization anchors (collar f0 = y^{-q}, c = 2)")
print("=" * 72)
s_sym = q * (1 - q) / 2
collar = {phi0: q * sp.log(r) / 2}
def on_collar(e):
    return sp.simplify(e.subs(phi0, q * sp.log(r) / 2).doit())
c_n_collar = on_collar(c_n.subs(c_s, 2))
J_rec = -s_sym * r**(-q)
c_n_record = J_rec * (r**(-q))**(1 - n) / n
check("c_n on collar == record's J f0^{1-n}/n with J = -s y^{-q}, "
      "s = q(1-q)/2  (general n, q symbolic)",
      sp.simplify(sp.powsimp(c_n_collar - c_n_record, force=True)) == 0)

# background criticality: total phi0-EL vanishes identically (any phi0!)
# c_n must be FROZEN (an explicit function of r) during the variation
Cfun = sp.Function("Cfun", real=True)(r)
L_src0_opaque = -Cfun * sp.exp(-2 * n * phi0)
EL_src_bg = sp.diff(L_src0_opaque, phi0).subs(Cfun, c_n)
L0_C1 = -sp.Rational(1, 2) * c_s * F**2 * r**2 * phi0p**2
EL_C1_bg = sp.diff(L0_C1, phi0) - sp.diff(sp.diff(L0_C1, phi0p), r)
check("criticality (general background, general n): EL_phi0[C1] + "
      "EL_phi0[src] == 0 identically  — the completion is on-shell by "
      "construction", dsimp(EL_C1_bg + EL_src_bg) == 0)

# second jet of the source on the collar = the record's -2 n s f0^2 dphi^2
jet2_src = sp.expand(
    sp.series(-c_n * sp.exp(-2 * n * (phi0 + eps * p)), eps, 0, 3
              ).removeO()).coeff(eps, 2)
jet2_record_form = 2 * n * s_sym * r**(-2 * q) * p**2   # LAGRANGIAN sign
check("source second jet (Lagrangian) on collar = +2 n s f0^2 dphi^2 "
      "(record's S_src jet is the sign-flipped -2 n s f0^2 dphi^2)  [c=2]",
      sp.simplify(on_collar(jet2_src.subs(c_s, 2)) - jet2_record_form) == 0)

# ------------------------------------------------------- full 2nd order L2
print()
print("=" * 72)
print("A1 — the n-symbolic second-order system (time-dependent, "
      "(dphi, H1, K) kept)")
print("=" * 72)
L2red = {}
L2red_C1 = {}
for name, gthth in [("param I", r**2 * (1 + eps * k * Y)),
                    ("param II", r**2 * sp.exp(eps * k * Y))]:
    L = build_L(gthth, phiM, phiM)
    ser = sp.series(L, eps, 0, 3).removeO()
    L2_C1 = angular_reduce(ser.coeff(eps, 2) / sp.sin(th), name + " C1")
    ser_s = sp.series(L_src_full, eps, 0, 3).removeO()
    L2_s = angular_reduce(ser_s.coeff(eps, 2) / sp.sin(th), name + " src")
    L2red_C1[name] = L2_C1
    L2red[name] = sp.expand(L2_C1 + L2_s)

L2 = L2red["param I"]
L2_C1only = L2red_C1["param I"]
pt, pr_ = sp.Derivative(p, t), sp.Derivative(p, r)

# STRUCTURAL LEMMA: the source sector touches NOTHING but the dphi potential
L2_src_only = sp.expand(L2 - L2_C1only)
check("STRUCTURAL LEMMA (coordinate measure): the source's entire "
      "second-order content is a pure dphi^2 potential — no H1, no K, no "
      "time or radial derivatives of anything",
      not any(L2_src_only.has(v) for v in
              [h, k, sp.Derivative(p, t), sp.Derivative(p, r),
               sp.Derivative(h, t), sp.Derivative(h, r),
               sp.Derivative(k, t), sp.Derivative(k, r)])
      and dsimp(L2_src_only - 2 * c_s * n * r**2 * F**2 * E0 * p**2 / 2
                ) == 0)
print(f"      L2_src = {sp.factor(L2_src_only)}")

# (a) the H1 equation
EL_h = dsimp(sp.diff(L2, h))
EL_h_C1 = dsimp(sp.diff(L2_C1only, h))
check("(2a) EL_H1[total] == EL_H1[C1]  for ALL n — the source does not "
      "enter the H1 variation; the algebraic weld f phi0' H1 = 2 d_t dphi "
      "is n-INSENSITIVE", dsimp(EL_h - EL_h_C1) == 0)
check("(2a) the weld itself: EL_H1 = (c/2) r^2 F^2 phi0' (phi0' H1 - "
      "2 e^{2phi0} d_t dphi) — unchanged from the banked form",
      dsimp(EL_h - sp.Rational(1, 2) * c_s * r**2 * F**2 * phi0p
            * (phi0p * h - 2 * sp.exp(2 * phi0) * pt)) == 0)

# delta T_tr of the total system: source carries NO metric dependence
# under the coordinate measure => T_src == 0 => delta T_tr[total] =
# delta T_tr[C1]; rebuild T_tr[C1] from scratch to re-verify the identity
gm = sp.zeros(4, 4)
gm[0, 0] = -F + eps * 2 * F * p * Y
gm[1, 1] = 1 / F + eps * (2 / F) * p * Y
gm[0, 1] = gm[1, 0] = eps * h * Y
gm[2, 2] = r**2 * (1 + eps * k * Y)
gm[3, 3] = r**2 * sp.sin(th)**2 * (1 + eps * k * Y)
g0i = sp.diag(*[1 / sp.expand(gm[i, i]).coeff(eps, 0) for i in range(4)])
g1m = gm.applyfunc(lambda e: sp.expand(e).coeff(eps, 1))
ginv = (g0i - eps * g0i * g1m * g0i).applyfunc(trunc)
phi_w = phi0 + eps * p * Y
E2w = trunc(sp.series(sp.exp(-2 * phi_w), eps, 0, 2).removeO())
dphi_w = [sp.diff(phi_w, x) for x in [t, r, th, sp.Symbol("az")]]
grad2_w = trunc(sum(ginv[i, j] * dphi_w[i] * dphi_w[j]
                    for i in range(3) for j in range(3)))
T_tr = trunc(c_s * E2w * (dphi_w[0] * dphi_w[1]
                          - sp.Rational(1, 2) * gm[0, 1] * grad2_w))
dT_tr1 = sp.expand(T_tr).coeff(eps, 1)
check("(2a) T_src(coordinate measure) == 0 identically (no metric "
      "anywhere in S_src), so delta T_tr[TOTAL] = delta T_tr[C1]; and "
      "EL_H1 = -r^2 (delta T_tr[TOTAL]) holds verbatim for every n — the "
      "weld is STILL exactly vanishing TOTAL radial energy flux",
      dsimp(EL_h * Y + r**2 * dT_tr1) == 0)

# (b) the K equation and the parametrization ambiguity
EL_k_I = dsimp(sp.diff(L2red["param I"], k))
EL_k_II = dsimp(sp.diff(L2red["param II"], k))
EL_k_I_C1 = dsimp(sp.diff(L2red_C1["param I"], k))
check("(2b) EL_K[total] == EL_K[C1] for ALL n (source has no K under "
      "the coordinate measure)", dsimp(EL_k_I - EL_k_I_C1) == 0)
diff_k = dsimp(EL_k_II - EL_k_I)
check("(2b) the K parametrization ambiguity is UNCHANGED: EL_K[II] - "
      "EL_K[I] = T^th_th[bg] r^2 K = -(c/2) r^2 F^2 phi0'^2 K for all n "
      "— K remains variationally ill-defined; K = 0 canon slice stands, "
      "n-INSENSITIVE",
      dsimp(diff_k + sp.Rational(1, 2) * c_s * r**2 * F**2 * phi0p**2 * k
            ) == 0)

# (c) H1 elimination and the kinetic flip
h_star = 2 * sp.exp(2 * phi0) * pt / phi0p
L2_eff = dsimp(L2.subs(h, h_star))
pt2_coeff = sp.expand(L2_eff).coeff(pt, 2)
check("(2c) H1 elimination: H1* = 2 e^{2phi0} d_t dphi / phi0' is the "
      "SAME for all n, and the kinetic flip is EXACTLY the banked "
      "-(c/2) r^2 — n-INSENSITIVE (source carries no d_t dphi, no H1)",
      dsimp(pt2_coeff + sp.Rational(1, 2) * c_s * r**2) == 0)

# the on-shell n-symbolic operator
EL_p_eff = dsimp(sp.diff(L2_eff, p) - sp.diff(sp.diff(L2_eff, pt), t)
                 - sp.diff(sp.diff(L2_eff, pr_), r)).subs(k, 0)
EL_p_eff = dsimp(EL_p_eff.doit())
target_n = c_s * (r**2 * sp.diff(p, t, 2)
                  + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
                  - (4 - 2 * n) * r**2 * F**2 * E0 * p
                  - lam * F * p)
check("(1) THE n-SYMBOLIC ON-SHELL WELD SYSTEM (K = 0):  r^2 d_t^2 dphi "
      "+ d_r(r^2 f^2 d_r dphi) - (4 - 2n) r^2 f^2 E0 dphi - lam f dphi "
      "= 0   — the ONLY n-dependence in the entire chain is "
      "E0 -> (1 - n/2) E0", dsimp(EL_p_eff - target_n) == 0)
check("(1) ANCHOR n = 0: exactly the banked operator (E0 coefficient "
      "-4 r^2 f^2 E0)", dsimp(EL_p_eff.subs(n, 0)
      - c_s * (r**2 * sp.diff(p, t, 2)
               + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
               - 4 * r**2 * F**2 * E0 * p - lam * F * p)) == 0)
check("(1) ANCHOR n = 1: E0 coefficient exactly HALVED "
      "(-2 r^2 f^2 E0 = E0_eff = E0/2 slot) — the record's n = 1 form",
      dsimp(EL_p_eff.subs(n, 1)
      - c_s * (r**2 * sp.diff(p, t, 2)
               + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
               - 2 * r**2 * F**2 * E0 * p - lam * F * p)) == 0)

# ------------------------------------------- static collar map -> mu(n)
print()
print("=" * 72)
print("A2 — collar map: reproduce the static invariant family "
      "mu(n) = (1-n) q (1-q), now from the WELD system")
print("=" * 72)
u = sp.Function("u", real=True)(r)
om = sp.symbols("omega", real=True)
# dphi = -u/(2 f0) * cos(omega t)  (the record's static map, time-harmonic)
subst = {p: -u * sp.cos(om * t) / (2 * sp.exp(q * sp.log(r) * (-1)) )}
# f0 = r^{-q}; -u/(2 f0) = -u r^{q} / 2
p_map = -u * r**q * sp.cos(om * t) / 2
expr = EL_p_eff.subs(phi0, q * sp.log(r) / 2)
expr = expr.subs(p, p_map).doit()
expr = sp.expand(sp.simplify(expr / (c_s * sp.cos(om * t))))
mu_n = (1 - n) * q * (1 - q)
target_map = -sp.Rational(1, 2) * r**(-q) * (
    sp.diff(r**2 * sp.diff(u, r), r)
    - (lam * r**q + mu_n + om**2 * r**(2 + 2 * q)) * u)
diffmap = sp.simplify(sp.powsimp(sp.expand(expr - target_map), force=True))
check("(1) collar map (general n, q, omega): the weld system maps under "
      "dphi = -(u/2) y^q cos(omega t) to  -(y^{-q}/2) [ (y^2 u')' - "
      "(lam y^q + mu(n) + omega^2 y^{2+2q}) u ]  with "
      "mu(n) = (1-n) q (1-q)  — the verified static invariant family at "
      "omega = 0, with the elliptic omega^2 term ADDING to the "
      "confining side (real omega never opens the window on the collar)",
      diffmap == 0)
check("(1) mu(0) = q(1-q) = 2s (banked weld slot, nu = sqrt(17) at "
      "q = 1/3)", sp.simplify(mu_n.subs(n, 0) - 2 * s_sym) == 0)
check("(1) mu(1) = 0 (nu = 3 slot)", sp.simplify(mu_n.subs(n, 1)) == 0)
check("(1) nu(n)^2 = (1 + 4 mu(n))/q^2 = 17 - 8n at q = 1/3",
      sp.simplify(((1 + 4 * mu_n) / q**2).subs(q, sp.Rational(1, 3))
                  - (17 - 8 * n)) == 0)

# the conservation exchange at background order: n-blind on shell
dVdphi_bg = sp.diff(-Cfun * sp.exp(-2 * n * phi0), phi0).subs(Cfun, c_n)
check("(2a) exchange bookkeeping: the source's phi-equation supply "
      "dL_src/dphi|_bg = -c r^2 F^2 E0 (cancelling EL_C1 = +c r^2 F^2 "
      "E0) — the n's CANCEL on shell: criticality pins the FIRST jet "
      "regardless of n; n enters the exchange only at second-jet order "
      "(the mass term above)",
      dsimp(dVdphi_bg + c_s * r**2 * F**2 * E0) == 0)

print()
print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} FAILED");  [print("  -", x) for x in FAIL]
    sys.exit(1)
print("ALL CHECKS PASSED (coordinate-measure n-symbolic weld system)")
