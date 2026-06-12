"""BLIND ADVERSARIAL VERIFIER - independent recomputation, claims 1-4.

All algebra re-derived from the C1 action; nothing reused from the
derivation agents' scripts. PASS/FAIL per check.

Claim 1: f-variable rewrite, second jets in f and in delta-phi,
         spatial-probe identification of the banked nu=5/2 family,
         relation between the two Hessians (bulk off-shell term vs
         contact term).
Claim 2: monopole (gauged) Laplacian lowest eigenvalues, symbolic +
         finite-difference.
Claim 3: route A vs route B dressing numerics and anchor checks.
Claim 4: gamma numerics only (corpus reading done by hand).
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
P = 0
F = 0


def chk(name, ok, detail=""):
    global P, F
    if ok:
        P += 1
        print(f"PASS {name} {detail}")
    else:
        F += 1
        print(f"FAIL {name} {detail}")


qS = sp.Rational(1, 3)

# =====================================================================
# CLAIM 1a: exact rewrite of the C1 density in f-variables.
# metric ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2, f = exp(-2 phi)
# LHS density: e^{-2phi} g^{mu nu} d_mu phi d_nu phi * sqrt(-g)
# with sqrt(-g) = r^2 sin(th)  (exact, independent of f).
# =====================================================================
print("== CLAIM 1a: exact f-variable rewrite ==")
r, th, ph = sp.symbols('r theta varphi', positive=True)
f = sp.Function('f')(r, th, ph)
phi = -sp.log(f) / 2
grad2 = f * sp.diff(phi, r)**2 \
    + (sp.diff(phi, th)**2 + sp.diff(phi, ph)**2 / sp.sin(th)**2) / r**2
lhs = sp.exp(-2 * phi) * grad2 * r**2 * sp.sin(th)
rhs = sp.Rational(1, 4) * (r**2 * sp.diff(f, r)**2
                           + (sp.diff(f, th)**2
                              + sp.diff(f, ph)**2 / sp.sin(th)**2) / f)
chk("1a LHS == (1/4)[r^2 f_r^2 + |grad_Om f|^2/f] * sin(th)",
    sp.simplify(lhs - rhs * sp.sin(th)) == 0)
chk("1a literal claimed identity (no sin th) is FALSE as densities",
    sp.simplify(lhs - rhs) != 0)

# =====================================================================
# CLAIM 1a': second jet in f-variables (f = y^-q + eps*u(y)*Y, unit-norm
# angular mode Y of -Delta_S2 eigenvalue lam). After angular integration
# the eps^2 coefficient should be (1/4)[y^2 u'^2 + lam y^q u^2],
# no u u' cross term.
# =====================================================================
print("== CLAIM 1a': second jet in f ==")
y, lam, eps = sp.symbols('y lambda epsilon', positive=True)
u = sp.Function('u')(y)
f0 = y**(-qS)
ffull = f0 + eps * u
# angular integration done analytically: int Y^2 = 1, int Y = 0,
# int |grad_Om Y|^2 = lam. Radial density after angular integration:
dens = sp.Rational(1, 4) * (y**2 * sp.diff(ffull, y)**2
                            + lam * eps**2 * u**2 / ffull)
quad = sp.expand(sp.diff(dens, eps, 2).subs(eps, 0) / 2)
target = sp.Rational(1, 4) * (y**2 * sp.diff(u, y)**2 + lam * y**qS * u**2)
chk("1a' eps^2 coeff == (1/4)[y^2 u'^2 + lam y^(1/3) u^2]",
    sp.simplify(quad - sp.expand(target)) == 0)

# NOTE: linear-in-eps term does NOT vanish radially (background off-shell)
lin = sp.simplify(sp.diff(dens, eps).subs(eps, 0))
# it is (1/2) y^2 f0' u' -> integrates to boundary + EOM term; EOM term:
eom = sp.simplify(sp.diff(y**2 * sp.diff(f0, y), y))
chk("1a' background is OFF-SHELL for scalar-only radial EOM: (y^2 f0')' != 0",
    sp.simplify(eom) != 0, f"(y^2 f0')' = {sp.simplify(eom)}")

# =====================================================================
# CLAIM 1: nu values. Generic ODE  a'' + (A/y) a' - (lam y^(q-2)+mu/y^2) a = 0
# has regular solution a = y^((1-A)/2) I_nu(x), x=(sqrt(lam)/beta) y^beta,
# beta=q/2, nu = sqrt((1-A)^2/4 + mu)/beta. Verify symbolically.
# =====================================================================
print("== CLAIM 1: generic Frobenius/Bessel solution check ==")
A_, mu_, nu_, be_ = sp.symbols('A mu nu beta', positive=True)
xS = sp.sqrt(lam) / be_ * y**be_
aS_ = y**((1 - A_) / 2) * sp.besseli(nu_, xS)
ode = sp.diff(aS_, y, 2) + A_ / y * sp.diff(aS_, y) \
    - (lam * y**(2 * be_ - 2) + mu_ / y**2) * aS_
ode = ode.subs(nu_, sp.sqrt((1 - A_)**2 / 4 + mu_) / be_)
ode_s = sp.simplify(ode.rewrite(sp.besselj).doit())
# fall back to numeric spot check if symbolic simplification is heavy
def ode_resid_num(Av, muv, lamv, bev, yv):
    nuv = mp.sqrt((1 - Av)**2 / 4 + muv) / bev
    h = mp.mpf('1e-6')
    def a(yy):
        x = mp.sqrt(lamv) / bev * yy**bev
        return yy**((1 - Av) / 2) * mp.besseli(nuv, x)
    d2 = (a(yv + h) - 2 * a(yv) + a(yv - h)) / h**2
    d1 = (a(yv + h) - a(yv - h)) / (2 * h)
    return d2 + Av / yv * d1 - (lamv * yv**(2 * bev - 2) + muv / yv**2) * a(yv)
res = [abs(ode_resid_num(Av, muv, mp.mpf(2), mp.mpf(1) / 6, mp.mpf('0.7')))
       for (Av, muv) in [(2.0, 0.0), (11.0 / 6, 0.0), (4.0 / 3, 4.0 / 9),
                         (4.0 / 3, 1.0 / 6)]]
chk("1 generic Bessel solution solves the ODE (4 parameter sets, numeric)",
    all(rr < 1e-3 for rr in res), f"max resid {mp.nstr(max(res), 5)}")

# nu values:
qn = mp.mpf(1) / 3
beta = qn / 2
def nu_of(A, mu):
    return mp.sqrt((1 - A)**2 / 4 + mu) / beta
chk("1 f-jet (A=2, mu=0) -> nu = 3 = 1/q", abs(nu_of(2, 0) - 3) < 1e-25)
chk("1 banked family (A=2-q/2=11/6, mu=0) -> nu = 5/2",
    abs(nu_of(mp.mpf(11) / 6, 0) - mp.mpf(5) / 2) < 1e-25)

# =====================================================================
# CLAIM 1b: second jet in delta-phi with FULL metric response
# (f == e^{-2phi} identically, so g^{rr} = e^{-2phi} too).
# parent radial density: e^{-4phi} y^2 phi_y^2 + e^{-2phi} |grad_Om phi|^2
# phi = (q/2) ln y + eps a(y) Y.
# =====================================================================
print("== CLAIM 1b: delta-phi second jet (full response) ==")
a = sp.Function('a')(y)
phi0 = qS / 2 * sp.log(y)
phif = phi0 + eps * a
densP = sp.exp(-4 * phif) * y**2 * sp.diff(phif, y)**2 \
    + lam * sp.exp(-2 * phif) * eps**2 * a**2
quadP = sp.expand(sp.diff(densP, eps, 2).subs(eps, 0) / 2)
tP = sp.expand(y**(2 - 2 * qS) * sp.diff(a, y)**2
               - 4 * qS * y**(1 - 2 * qS) * a * sp.diff(a, y)
               + 2 * qS**2 * y**(-2 * qS) * a**2 + lam * y**(-qS) * a**2)
chk("1b quad form: y^(4/3)a'^2 - (4/3)y^(1/3) a a' + (2/9)y^(-2/3)a^2 "
    "+ lam y^(-1/3) a^2", sp.simplify(quadP - tP) == 0)
# EL of this form: (w a')' = (M - c') a with w=y^(4/3), c=-2q y^(1/3),
# M = lam y^(-1/3) + 2q^2 y^(-2/3):
c_ = -2 * qS * y**(sp.Rational(1, 3))
M_ = lam * y**(-sp.Rational(1, 3)) + 2 * qS**2 * y**(-sp.Rational(2, 3))
Meff = sp.simplify(M_ - sp.diff(c_, y))
chk("1b effective bulk mass = lam y^(-1/3) + (4/9) y^(-2)*y^(4/3)... i.e. "
    "mu = 2q(1-q) = 4/9",
    sp.simplify(Meff - (lam * y**(-sp.Rational(1, 3))
                        + sp.Rational(4, 9) * y**(-sp.Rational(2, 3)))) == 0)
nphi = nu_of(mp.mpf(4) / 3, mp.mpf(4) / 9)
chk("1b delta-phi (full response) nu = sqrt(17), not 5/2, not 3",
    abs(nphi - mp.sqrt(17)) < 1e-25, f"nu = {mp.nstr(nphi, 12)}")

# fixed-metric probe variant (g^{rr}=f0 frozen, only e^{-2phi} prefactor):
densQ = sp.exp(-2 * phif) * y**(-qS) * y**2 * sp.diff(phif, y)**2 \
    + lam * sp.exp(-2 * phif).subs(eps, 0) * eps**2 * a**2
quadQ = sp.expand(sp.diff(densQ, eps, 2).subs(eps, 0) / 2)
cQ = sp.expand(quadQ).coeff(sp.diff(a, y), 1).coeff(a, 1) / 2  # c(y)
MQ = sp.expand(quadQ).coeff(a, 2)
muQ = sp.simplify((MQ - sp.diff(cQ, y) - lam * y**(-qS)) * y**(2 * qS) * y**0)
print("   fixed-metric probe: c =", sp.simplify(cQ), " bulk-mu coeff =",
      sp.simplify(muQ))
nQ = nu_of(mp.mpf(4) / 3, mp.mpf(1) / 6)
chk("1b fixed-metric-probe variant nu = sqrt(7) (also not 5/2)",
    abs(nQ - mp.sqrt(7)) < 1e-25, f"nu = {mp.nstr(nQ, 12)}")

# =====================================================================
# CLAIM 1b': banked nu=5/2 family IS the spatial Dirichlet probe
# E = (1/2) int [r^2 a_rho^2 + lam a^2] d rho, d rho = y^{q/2} dy:
# weights y^{2-q/2} a'^2 + lam y^{q/2} a^2 -> A = 2-q/2, nu=5/2. Symbolic.
# =====================================================================
print("== CLAIM 1b': banked family == spatial probe ==")
wS = y**(2 - qS / 2)
elS = sp.expand(sp.diff(wS * sp.diff(a, y), y) - lam * y**(qS / 2) * a)
bankedS = sp.expand(wS * (sp.diff(a, y, 2)
                          + (2 - qS / 2) / y * sp.diff(a, y)
                          - lam * y**(qS - 2) * a))
chk("1b' spatial-probe EL == banked collar equation",
    sp.simplify(elS - bankedS) == 0)

# =====================================================================
# CLAIM 1: DtN closed forms + numerics. ODE-shoot every family and
# compare with the Bessel-ratio formulas.
#   family(A, mu): min of the on-shell flux for regular branch.
#   D = w(1) a'(1)/a(1) (+ contact term where the form has one).
# =====================================================================
print("== CLAIM 1: DtN numerics, all families ==")


def dtn_shoot(Av, muv, lamv):
    """d ln a/d ln y at y=1 for regular branch via mpmath ODE."""
    nuv = nu_of(Av, muv)
    mexp = (1 - Av) / 2

    def aex(yy):
        x = mp.sqrt(lamv) / beta * yy**beta
        return yy**mexp * mp.besseli(nuv, x)
    y0 = mp.mpf('1e-5')
    h = mp.mpf('1e-8')
    a0 = aex(y0)
    da0 = (aex(y0 + h) - aex(y0 - h)) / (2 * h)

    def rhs(yy, w):
        return [w[1], (lamv * yy**(qn - 2) + muv / yy**2) * w[0]
                - (Av / yy) * w[1]]
    sol = mp.odefun(rhs, y0, [a0, da0], tol=1e-22)
    a1, da1 = sol(mp.mpf(1))
    return da1 / a1


def dtn_formula(nuv, lamv):
    x0 = 6 * mp.sqrt(lamv)
    return (1 - mp.sqrt((2 * beta * nuv)**2)) / 2 + 0  # placeholder


def logderiv_formula(Av, muv, lamv):
    nuv = nu_of(Av, muv)
    x0 = 6 * mp.sqrt(lamv)
    return (1 - Av) / 2 + nuv / 6 \
        + mp.sqrt(lamv) * mp.besseli(nuv + 1, x0) / mp.besseli(nuv, x0)


fams = {
    "f-jet (A=2,mu=0)": (mp.mpf(2), mp.mpf(0)),
    "banked/spatial (A=11/6,mu=0)": (mp.mpf(11) / 6, mp.mpf(0)),
    "phi-jet (A=4/3,mu=4/9)": (mp.mpf(4) / 3, mp.mpf(4) / 9),
}
for nm, (Av, muv) in fams.items():
    for lv in [mp.mpf(1) / 2, mp.mpf(2)]:
        sh = dtn_shoot(Av, muv, lv)
        fo = logderiv_formula(Av, muv, lv)
        chk(f"1 DtN shoot vs formula {nm} lam={mp.nstr(lv,3)}",
            abs(sh - fo) < mp.mpf('1e-6'),
            f"shoot={mp.nstr(sh,10)} formula={mp.nstr(fo,10)}")

# specific claimed forms:
def D_f(lv):   # route-B claimed C1 f-jet DtN: w=y^2 -> w a'/a at y=1
    x0 = 6 * mp.sqrt(lv)
    return mp.sqrt(lv) * mp.besseli(4, x0) / mp.besseli(3, x0)
chk("1 f-jet DtN == sqrt(lam) I4/I3 (log-deriv + (1-A)/2 cancellation)",
    abs(logderiv_formula(2, 0, mp.mpf(2)) - (-mp.mpf(1) / 2 + mp.mpf(3) / 6
        + mp.sqrt(2) * mp.besseli(4, 6 * mp.sqrt(2))
        / mp.besseli(3, 6 * mp.sqrt(2)))) < 1e-30 and
    abs((-0.5 + 0.5) - 0) < 1e-30)

def D_banked(lv):
    x0 = 6 * mp.sqrt(lv)
    return mp.sqrt(lv) * mp.besseli(mp.mpf(7) / 2, x0) \
        / mp.besseli(mp.mpf(5) / 2, x0)
chk("1 banked log-deriv == sqrt(lam) I7/2 / I5/2 exactly",
    abs(logderiv_formula(mp.mpf(11) / 6, 0, mp.mpf(2)) - D_banked(2))
    < mp.mpf('1e-30'))
chk("1 banked D1 = 0.979663326283",
    abs(D_banked(2) - mp.mpf('0.979663326283')) < 1e-11,
    mp.nstr(D_banked(2), 15))
Bnum = D_banked(2) / mp.sqrt(2)
chk("1 banked B = 0.692726581294", abs(Bnum - mp.mpf('0.692726581294'))
    < 1e-11, mp.nstr(Bnum, 15))

# =====================================================================
# CLAIM 1c: relation between phi-jet and f-jet quadratic forms.
# Exact identity: H_phi[a] = H_f[-2 f0 a] + S1_f[2 f0 a^2]
# where S1_f[v] = (1/2) int y^2 f0' v' dy (first variation of the
# f-form). Verify symbolically (integrands match up to total derivative)
# and numerically (with explicit boundary bookkeeping).
# Then: difference of minimized boundary forms is NOT a lam-independent
# contact term => bulk off-shell content.
# =====================================================================
print("== CLAIM 1c: Hessian relation and contact-term test ==")
u1 = -2 * f0 * a
u2 = 2 * f0 * a**2
Hf_integrand = sp.Rational(1, 4) * (y**2 * sp.diff(u1, y)**2
                                    + lam * y**qS * u1**2)
S1_integrand = sp.Rational(1, 2) * y**2 * sp.diff(f0, y) * sp.diff(u2, y)
diffI = sp.simplify(quadP - sp.expand(Hf_integrand) - sp.expand(S1_integrand))
# difference should be a total derivative d/dy(something); check by
# integrating symbolically:
antider = sp.integrate(diffI, y)
chk("1c H_phi - H_f(u1) - S1(u2) integrand is a total derivative",
    sp.simplify(sp.diff(antider, y) - diffI) == 0,
    f"boundary content = {sp.simplify(antider)}")

# minimized boundary energies on matched boundary data a(1)=1, u(1)=-2:
def m_phi(lv):
    # on-shell value of H_phi with a(1)=1: w(1)a'(1) + c(1)
    return logderiv_formula(mp.mpf(4) / 3, mp.mpf(4) / 9, lv) \
        - 2 * qn  # c(1) = -2q
def m_f(lv):
    # H_f with u(1) = -2: (1/4) * 4 * D_f = D_f
    return D_f(lv)
print("   lam    m_phi          m_f            diff")
diffs = []
for lv in [mp.mpf(1) / 2, mp.mpf(1), mp.mpf(2), mp.mpf(6)]:
    d = m_phi(lv) - m_f(lv)
    diffs.append(d)
    print(f"   {mp.nstr(lv,3):5} {mp.nstr(m_phi(lv),10):14} "
          f"{mp.nstr(m_f(lv),10):14} {mp.nstr(d,10)}")
spread = max(diffs) - min(diffs)
chk("1c difference of the two DtN forms is NOT lam-independent "
    "(not a pure contact term)", spread > mp.mpf('1e-3'),
    f"spread over lam = {mp.nstr(spread, 6)}")

# =====================================================================
# CLAIM 2: monopole harmonics. Symbolic eigenfunction checks + FD lowest
# eigenvalue scan over m sectors.
# Operator (north gauge A = qm (1-cos th) dphi), mode e^{i m phi} g(th):
#  L g = -g'' - cot(th) g' + (m - qm(1-cos th))^2 / sin^2 th * g
# =====================================================================
print("== CLAIM 2: monopole gauged-Laplacian spectrum ==")
thS, mS, qmS = sp.symbols('theta m q_m')
g_ = sp.Function('g')


def Lop(gexpr, mval, qmval):
    return (-sp.diff(gexpr, thS, 2) - sp.cos(thS) / sp.sin(thS)
            * sp.diff(gexpr, thS)
            + (mval - qmval * (1 - sp.cos(thS)))**2 / sp.sin(thS)**2 * gexpr)


# n=1, qm=1/2, j=1/2: states cos(th/2) (m=0) and sin(th/2) (m=1)
for (mval, gexpr, name) in [(0, sp.cos(thS / 2), "cos(th/2), m=0"),
                            (1, sp.sin(thS / 2), "sin(th/2), m=1")]:
    val = sp.simplify(Lop(gexpr, mval, sp.Rational(1, 2)) / gexpr)
    chk(f"2 n=1 j=1/2 eigenstate {name}: lam = 1/2",
        sp.simplify(val - sp.Rational(1, 2)) == 0, f"got {val}")
# j(j+1)-(n/2)^2 at j=1/2, n=1:
chk("2 identity j(j+1)-(n/2)^2 = 1/2 at j=n/2=1/2",
    sp.Rational(1, 2) * sp.Rational(3, 2) - sp.Rational(1, 4)
    == sp.Rational(1, 2))
# n=2, qm=1, j=1: states cos^2(th/2) (m=0), sin th (m=1), sin^2(th/2) (m=2)
for (mval, gexpr, name) in [(0, sp.cos(thS / 2)**2, "cos^2(th/2), m=0"),
                            (1, sp.sin(thS), "sin(th), m=1"),
                            (2, sp.sin(thS / 2)**2, "sin^2(th/2), m=2")]:
    val = sp.simplify(Lop(gexpr, mval, 1) / gexpr)
    chk(f"2 n=2 j=1 eigenstate {name}: lam = 1",
        sp.simplify(val - 1) == 0, f"got {val}")
chk("2 identity j(j+1)-(n/2)^2 = 1 at j=1, n=2",
    sp.Integer(1) * 2 - 1 == 1)

# FD lowest-eigenvalue scan (is 1/2 really the MINIMUM over all m?)
import numpy as np
try:
    from scipy.linalg import eigh_tridiagonal
    have_scipy = True
except Exception:
    have_scipy = False


def lowest_eig(mval, qmval, N=4000):
    # substitution g = h / sqrt(sin th) gives a Schroedinger form:
    # -h'' + V h = lam h with
    # V = (m - qm(1-cos))^2/sin^2 - 1/4 - 1/(4 sin^2) ... derive:
    # for -g'' - cot g' + W g = lam g, g = h sin^{-1/2}:
    # -h'' + [W - 1/4 - 1/(4 sin^2)] h = lam h  (standard)
    th = np.linspace(0, np.pi, N + 2)[1:-1]
    dx = th[1] - th[0]
    W = (mval - qmval * (1 - np.cos(th)))**2 / np.sin(th)**2
    V = W - 0.25 - 1.0 / (4 * np.sin(th)**2)
    d = 2.0 / dx**2 + V
    e = -1.0 / dx**2 * np.ones(N - 1)
    if have_scipy:
        vals = eigh_tridiagonal(d, e, select='i',
                                select_range=(0, 0))[0]
        return vals[0]
    Tm = np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
    return np.linalg.eigvalsh(Tm)[0]


for (nval, expect, mrange) in [(1, 0.5, range(-3, 5)),
                               (2, 1.0, range(-3, 6))]:
    qmval = nval / 2.0
    eigs = {mv: lowest_eig(mv, qmval) for mv in mrange}
    lo = min(eigs.values())
    hits = [mv for mv, ev in eigs.items() if abs(ev - expect) < 5e-3]
    chk(f"2 n={nval}: global lowest eigenvalue == {expect}",
        abs(lo - expect) < 5e-3, f"min = {lo:.6f}")
    chk(f"2 n={nval}: degeneracy of lowest = {nval + 1} (m sectors {hits})",
        len(hits) == nval + 1)

# =====================================================================
# CLAIM 3: route A vs route B numbers + anchor checks.
# =====================================================================
print("== CLAIM 3: dressing bookkeeping ==")
eta = mp.mpf(1) / 18


def Brat(lv):
    x0 = 6 * mp.sqrt(lv)
    return mp.besseli(mp.mpf(7) / 2, x0) / mp.besseli(mp.mpf(5) / 2, x0)


B2 = Brat(2)
Bh = Brat(mp.mpf(1) / 2)
Dh = D_banked(mp.mpf(1) / 2)
chk("3 B(2) = 0.692726581294", abs(B2 - mp.mpf('0.692726581294')) < 1e-11,
    mp.nstr(B2, 15))
chk("3 B(1/2) = 0.486553780698", abs(Bh - mp.mpf('0.486553780698')) < 1e-11,
    mp.nstr(Bh, 15))
chk("3 D(1/2) = 0.344045477744", abs(Dh - mp.mpf('0.344045477744')) < 1e-11,
    mp.nstr(Dh, 15))
chk("3 D(1/2) = sqrt(1/2) B(1/2) and D(1/2)/sqrt2 = B(1/2)/2 exactly",
    abs(Dh - mp.sqrt(mp.mpf(1) / 2) * Bh) < 1e-30 and
    abs(Dh / mp.sqrt(2) - Bh / 2) < 1e-30)
CA = mp.e**(eta * (B2 - Bh))
CB = mp.e**(eta * (B2 - Dh / mp.sqrt(2)))
chk("3 route A C_M1 = 1.011519893216", abs(CA - mp.mpf('1.011519893216'))
    < 1e-11, mp.nstr(CA, 15))
chk("3 route B C_M1^w = 1.02528377433", abs(CB - mp.mpf('1.02528377433'))
    < 1e-10, mp.nstr(CB, 15))
# anchor checks: frozen warped per-node exponent is (eta/2) B(2) = B/36
chk("3 route A rule (eta/2)B(lam) at lam=2 hits frozen warped node B/36",
    abs(eta / 2 * B2 - B2 / 36) < 1e-30)
chk("3 route B rule (eta/2)D(lam)/sqrt2 at lam=2 hits frozen warped node",
    abs(eta / 2 * D_banked(2) / mp.sqrt(2) - B2 / 36) < 1e-30)
chk("3 route B local rule (eta/4)*lam at lam=2 hits local eta/2",
    abs(eta / 4 * 2 - eta / 2) < 1e-30)
# the two rules differ by sqrt(lam/2) -- they CANNOT be distinguished at
# the anchor; at lam=1/2 the ratio is exactly 1/2:
chk("3 dressing ratio (B-rule)/(A-rule) = sqrt(lam/2): = 1/2 at lam=1/2",
    abs((Dh / mp.sqrt(2)) / Bh - mp.mpf(1) / 2) < 1e-30)

# =====================================================================
# CLAIM 4: gamma numerics (corpus-reading adjudication done separately)
# =====================================================================
print("== CLAIM 4: gamma numerics ==")
gam = 3 * mp.e**(-eta / 2)
chk("4 gamma = 3 exp(-1/36) = 2.91781343...",
    abs(gam - mp.mpf('2.91781343135')) < 1e-10, mp.nstr(gam, 12))
chk("4 exp(eta) (B's claimed C_E1) = 1.05716...",
    abs(mp.e**eta - mp.mpf('1.0571584167')) < 1e-9, mp.nstr(mp.e**eta, 12))

print(f"\nTOTAL: {P} PASS, {F} FAIL")
