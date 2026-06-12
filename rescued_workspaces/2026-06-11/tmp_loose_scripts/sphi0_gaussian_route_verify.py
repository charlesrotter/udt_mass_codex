"""Verification record: boundary-measure / Gaussian-reduction route for S_phi0.

Scratch script (NOT for repo). All checks print PASS/FAIL.

Checks:
  V1  Exact C1 second variation in f-variables has no cross terms
      (sympy expansion of the exact density to second order).
  V2  Radial ODE (y^2 u')' = lam y^q u with q=1/3 has DtN
      D(lam) = sqrt(lam) I_4(6 sqrt(lam))/I_3(6 sqrt(lam))   [nu = 1/q = 3]
      -- numeric ODE solve vs Bessel formula, lam in {1/2, 1, 2, 6}.
  V3  Corpus warped family (A = 2 - q/2, nu = 5/2) reproduces banked
      D1 = 0.9796633, D2 = 1.9857855, D3 = 2.9893060, B = 0.692726581294.
  V4  Circle average identity: <exp(-s cos^2 th)> = exp(-s/2) I0(s/2).
  V5  Second moments: S2 <n_a n_b> = delta/3 (and CP1/Hopf pushforward
      gives the same), relative circle <u_i u_j> = delta/2.
  V6  Monopole (gauged) Laplacian lowest eigenvalues:
      n=1 (q_m=1/2): lam = l(l+1)-q_m^2 = 1/2, deg 2;
      n=2 (q_m=1):   lam = 1, deg 3.    (table check vs corpus values)
  V7  Branch-coefficient numerics to 12+ digits (both gluing schemes,
      intrinsic-local and warped branches, warped with nu=5/2 and nu=3).
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
PASS = 0
FAIL = 0


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"PASS  {name} {detail}")
    else:
        FAIL += 1
        print(f"FAIL  {name} {detail}")


# ---------------------------------------------------------------- V1
print("== V1: exact C1 second variation in f-variables ==")
y, lamS, eps = sp.symbols('y lam eps', positive=True)
u = sp.Function('u')
q = sp.Rational(1, 3)
F = y ** (-q)
# Exact C1 density (per unit time, mode-reduced schematically):
#   radial:  (1/4) y^2 (d_y f)^2          with f = F + eps*u(y)
#   angular: |grad_Omega f|^2/(4 f)  -> (lam/4) (eps*u)^2 / f for a single
#            unit-normalized angular mode carried only by the fluctuation.
f_full = F + eps * u(y)
dens = sp.Rational(1, 4) * y**2 * sp.diff(f_full, y)**2 \
    + sp.Rational(1, 4) * lamS * (eps * u(y))**2 / f_full
d2 = sp.series(dens, eps, 0, 3).removeO()
quad = sp.expand(sp.diff(d2, eps, 2).subs(eps, 0) / 2)
target = sp.expand(sp.Rational(1, 4) * y**2 * sp.diff(u(y), y)**2
                   + sp.Rational(1, 4) * lamS * y**q * u(y)**2)
check("V1 second-order density == (1/4)[y^2 u'^2 + lam y^q u^2]",
      sp.simplify(quad - target) == 0)
# cross term u*u' coefficient at second order:
cross = quad.coeff(sp.diff(u(y), y), 1).coeff(u(y), 1)
check("V1 no u*u' cross term at second order", sp.simplify(cross) == 0)

# ---------------------------------------------------------------- V2
print("== V2: C1-exact radial DtN, nu = 1/q = 3 ==")
qn = mp.mpf(1) / 3


def dtn_ode(lam, A):
    """Numeric DtN d ln u/d ln y at y=1 for u'' + (A/y)u' = lam y^(q-2) u,
    regular branch started from the exact Frobenius behavior near 0."""
    lam = mp.mpf(lam)
    nu = abs(1 - A) / qn
    mu = (1 - A) / 2
    # start from Bessel series at small y to set regular initial data,
    # then integrate the ODE numerically and compare endpoint log-deriv.
    beta = qn / 2

    def x_of(yv):
        return (mp.sqrt(lam) / beta) * yv ** beta

    y0 = mp.mpf('1e-6')

    def u_exact(yv):
        return yv ** mu * mp.besseli(nu, x_of(yv))

    u0 = u_exact(y0)
    h = mp.mpf('1e-9')
    du0 = (u_exact(y0 + h) - u_exact(y0 - h)) / (2 * h)

    def rhs(yv, w):
        return [w[1], lam * yv ** (qn - 2) * w[0] - (A / yv) * w[1]]

    f = mp.odefun(rhs, y0, [u0, du0], tol=1e-20)
    u1, du1 = f(mp.mpf(1))
    return du1 / u1  # d ln u/d ln y at y=1


def dtn_bessel(lam, nu):
    x0 = 6 * mp.sqrt(lam)
    return mp.sqrt(lam) * mp.besseli(nu + 1, x0) / mp.besseli(nu, x0)


for lam in ['0.5', '1', '2', '6']:
    lamv = mp.mpf(lam)
    num = dtn_ode(lamv, A=mp.mpf(2))
    formula = dtn_bessel(lamv, nu=3)
    check(f"V2 ODE vs sqrt(lam) I4/I3 at lam={lam}",
          abs(num - formula) < mp.mpf('1e-8'),
          f"ode={mp.nstr(num,12)} bessel={mp.nstr(formula,12)}")

# ---------------------------------------------------------------- V3
print("== V3: corpus warped family nu=5/2 reproduces banked numbers ==")
D1c = dtn_bessel(2, mp.mpf(5) / 2)
D2c = dtn_bessel(6, mp.mpf(5) / 2)
D3c = dtn_bessel(12, mp.mpf(5) / 2)
Bc = mp.besseli(mp.mpf(7) / 2, 6 * mp.sqrt(2)) / \
    mp.besseli(mp.mpf(5) / 2, 6 * mp.sqrt(2))
check("V3 D1 = 0.9796633", abs(D1c - mp.mpf('0.9796633')) < 1e-6,
      mp.nstr(D1c, 12))
check("V3 D2 = 1.9857855", abs(D2c - mp.mpf('1.9857855')) < 1e-6,
      mp.nstr(D2c, 12))
check("V3 D3 = 2.9893060", abs(D3c - mp.mpf('2.9893060')) < 1e-6,
      mp.nstr(D3c, 12))
check("V3 B  = 0.692726581294", abs(Bc - mp.mpf('0.692726581294')) < 1e-11,
      mp.nstr(Bc, 14))
check("V3 D1 = sqrt(2) B exactly", abs(D1c - mp.sqrt(2) * Bc) < 1e-25)
# corpus warped ODE cross-check: A = 2 - q/2 gives the same D1
num52 = dtn_ode(mp.mpf(2), A=2 - qn / 2)
check("V3 ODE (A=2-q/2) vs banked D1", abs(num52 - D1c) < 1e-8,
      mp.nstr(num52, 12))

# ---------------------------------------------------------------- V4
print("== V4: circle average identity ==")
for s in ['0.0138888888888889', '0.5', '2']:
    sv = mp.mpf(s)
    avg = mp.quad(lambda t: mp.e ** (-sv * mp.cos(t) ** 2),
                  [0, 2 * mp.pi]) / (2 * mp.pi)
    ident = mp.e ** (-sv / 2) * mp.besseli(0, sv / 2)
    check(f"V4 <exp(-s cos^2)> = e^(-s/2) I0(s/2), s={s[:6]}",
          abs(avg - ident) < 1e-20)

# ---------------------------------------------------------------- V5
print("== V5: second moments ==")
m_s2 = mp.quad(lambda th: mp.cos(th) ** 2 * mp.sin(th), [0, mp.pi]) / 2
check("V5 S2 <n_z^2> = 1/3", abs(m_s2 - mp.mpf(1) / 3) < 1e-20,
      mp.nstr(m_s2, 12))
# CP1 Fubini-Study pushforward: n_z = cos(chi), FS density sin(chi)/2
m_cp1 = mp.quad(lambda ch: mp.cos(ch) ** 2 * mp.sin(ch), [0, mp.pi]) / 2
check("V5 CP1 pushforward <n_z^2> = 1/3", abs(m_cp1 - mp.mpf(1) / 3) < 1e-20)
m_circ = mp.quad(lambda t: mp.cos(t) ** 2, [0, 2 * mp.pi]) / (2 * mp.pi)
check("V5 relative circle <u_1^2> = 1/2", abs(m_circ - mp.mpf(1) / 2) < 1e-20)

# ---------------------------------------------------------------- V6
print("== V6: monopole lowest eigenvalues (Wu-Yang: lam = l(l+1)-q_m^2) ==")
for n, lam_expect, deg_expect in [(1, mp.mpf(1) / 2, 2), (2, mp.mpf(1), 3)]:
    qm = mp.mpf(n) / 2
    l0 = qm
    lam = l0 * (l0 + 1) - qm ** 2
    deg = int(2 * l0 + 1)
    check(f"V6 n={n}: lam={mp.nstr(lam,6)}, deg={deg}",
          abs(lam - lam_expect) < 1e-25 and deg == deg_expect)

# ---------------------------------------------------------------- V7
print("== V7: branch coefficients (12-digit numerics) ==")
eta = mp.mpf(1) / 18


def report(name, val):
    print(f"   {name} = {mp.nstr(val, 14)}")


print(" -- intrinsic-local branch, raw uniform clock s = (eta/4)*lam*|v|^2")
C_M1 = mp.e ** (2 * (eta / 2 - eta / 8))            # = exp(3 eta/4)
C_E1_joint = mp.e ** (2 * (eta - eta / 2))          # = exp(eta)
I0q = mp.besseli(0, eta / 4)
C_E1_indep = mp.e ** eta * I0q ** 4
C_M2_joint = mp.e ** (2 * (eta - eta / 4))          # = exp(3 eta/2)
C_M2_indep = mp.e ** (3 * eta / 2) * mp.besseli(0, eta / 8) ** 4
report("C_M1            = exp(1/24)            ", C_M1)
report("C_E1 (joint)    = exp(1/18)            ", C_E1_joint)
report("C_E1 (indep)    = exp(1/18) I0(1/72)^4 ", C_E1_indep)
report("C_E1/C_M1 (joint) = exp(1/72)          ", C_E1_joint / C_M1)
report("C_M2 (joint, if active) = exp(1/12)    ", C_M2_joint)
report("C_M2 (indep, if active)                ", C_M2_indep)
check("V7 C_M1 == exp(1/24)", abs(C_M1 - mp.e ** (mp.mpf(1) / 24)) < 1e-25)
check("V7 C_E1 joint == exp(1/18)",
      abs(C_E1_joint - mp.e ** (mp.mpf(1) / 18)) < 1e-25)
check("V7 ratio joint == exp(1/72)",
      abs(C_E1_joint / C_M1 - mp.e ** (mp.mpf(1) / 72)) < 1e-25)

print(" -- warped branch, banked family nu = 5/2 (spatial Dirichlet probe)")


def warped_coeffs(nu):
    D = {lam: dtn_bessel(mp.mpf(lam), nu) for lam in ('0.5', '1', '2')}
    s_unit = lambda lam: (eta / 2) * D[lam] / mp.sqrt(2)  # per unit move
    sH = s_unit('2')              # frame / H1 sector step (= (eta/2)B at nu=5/2)
    # frozen warped ladder books (eta/2)*B_banked per node:
    sB = (eta / 2) * Bc
    # frame nodes (3), then per-side residuals:
    T_M1 = mp.e ** (-(3 * sH + 2 * s_unit('0.5')))
    T_E1 = mp.e ** (-(3 * sH + 2 * sH))            # joint: |u|^2 = 1 per side
    T_E1_ind = mp.e ** (-3 * sH) * (mp.e ** (-sH / 2)
                                    * mp.besseli(0, sH / 2)) ** 4
    T_M2 = mp.e ** (-(3 * sH + 2 * s_unit('1')))
    lad5 = mp.e ** (-5 * sB)
    lad7 = mp.e ** (-7 * sB)
    return (T_M1 / lad5, T_E1 / lad7, T_E1_ind / lad7, T_M2 / lad7,
            D, sH)


CwM1, CwE1, CwE1i, CwM2, D52, sH52 = warped_coeffs(mp.mpf(5) / 2)
report("D(1/2) nu=5/2", D52['0.5'])
report("D(1)   nu=5/2", D52['1'])
report("D(2)   nu=5/2", D52['2'])
report("C_M1^w  (joint)", CwM1)
report("C_E1^w  (joint)", CwE1)
report("C_E1^w  (indep)", CwE1i)
report("C_E1^w/C_M1^w (joint)", CwE1 / CwM1)
report("C_M2^w  (joint, if active)", CwM2)

print(" -- warped branch, C1-exact family nu = 3 (this route's derivation)")
CwM1_3, CwE1_3, CwE1i_3, CwM2_3, D3f, sH3 = warped_coeffs(mp.mpf(3))
report("D(1/2) nu=3", D3f['0.5'])
report("D(1)   nu=3", D3f['1'])
report("D(2)   nu=3", D3f['2'])
report("B_C1 = D(2)/sqrt(2) nu=3", D3f['2'] / mp.sqrt(2))
report("C_M1^w3 (joint)", CwM1_3)
report("C_E1^w3 (joint)", CwE1_3)
report("C_E1^w3 (indep)", CwE1i_3)
report("C_E1^w3/C_M1^w3 (joint)", CwE1_3 / CwM1_3)
report("C_M2^w3 (joint, if active)", CwM2_3)

print(" -- normalized-kernel alternative clock (per-sector unit eigenvalue)")
C_M1_nk = mp.mpf(1)
C_E1_nk = C_E1_joint
report("C_M1 (norm-kernel)  = 1", C_M1_nk)
report("C_E1 (norm-kernel)  = exp(1/18)", C_E1_nk)
report("C_M2 (norm-kernel)  = exp(1/18)  [DEGENERATE with E1 - flag]",
       C_E1_nk)

print()
print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
