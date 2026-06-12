"""Symplectic-gluing / Schur-complement route: numerical verification.

Scratch script (NOT for repo). All checks are exact-structure checks of the
derivation chain in the report:

  A. self-similar collar mode equation and its Bessel solutions (residual check)
  B. two-boundary (annulus) DtN matrix Lambda = [[Lcc, Lc0],[L0c, L00]]:
     symmetry Lc0 = L0c (Wronskian), closed form b = -W0/Delta
  C. regular-core limit: L00 -> D_ell (banked values), and the cross coupling
     b_ell and core stiffness Lcc vanish like yc^{(2-q)/2}
  D. Schur identity: eliminating the core slot (free core) equals the
     Neumann-inner DtN exactly, and -> D_ell as yc -> 0
  E. composition / bookkeeping identities (exact rationals)
  F. 12-digit records of the branch-coefficient formulas (normalization N
     explicit; NO comparisons to any data)
"""
import mpmath as mp

mp.mp.dps = 40
PASS = 0
FAIL = 0
def check(name, ok):
    global PASS, FAIL
    if ok: PASS += 1
    else: FAIL += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

def collar(q, ell):
    """Return solution pair F (regular branch), G (singular branch), weight w."""
    q = mp.mpf(q)
    beta = q/2
    m = (1 - 2/q)/2          # negative
    nu = -m
    L = mp.mpf(ell*(ell+1))
    def x(y): return mp.sqrt(L)/beta * y**beta
    def F(y):
        xx = x(y); return xx**m * mp.besseli(nu, xx)
    def G(y):
        xx = x(y); return xx**m * mp.besselk(nu, xx)
    def w(y): return y**(2 - q/2)
    return F, G, w, beta, m, nu, L

def dmode(f, y):  return mp.diff(f, y)

def dtn_matrix(q, ell, yc):
    """Two-boundary DtN of the collar annulus [yc,1] per (ell,m) mode.
    Convention: S_onshell = (1/2)(ac,a0) Lambda (ac,a0)^T with outward momenta
    p0 = w(1)a'(1), pc = -w(yc)a'(yc)."""
    F, G, w, beta, m, nu, L = collar(q, ell)
    yc = mp.mpf(yc); one = mp.mpf(1)
    # sigma vanishes at 1, tau vanishes at yc
    sigma = lambda y: F(y)*G(one) - G(y)*F(one)
    tau   = lambda y: F(y)*G(yc)  - G(y)*F(yc)
    L00 = w(one) * dmode(tau, one) / tau(one)
    Lc0 = w(one) * dmode(sigma, one) / sigma(yc)
    L0c = -w(yc) * dmode(tau, yc) / tau(one)
    Lcc = -w(yc) * dmode(sigma, yc) / sigma(yc)
    return Lcc, Lc0, L0c, L00

def D_ell(q, ell):
    q = mp.mpf(q); beta = q/2
    nu = (2/q - 1)/2
    L = mp.mpf(ell*(ell+1)); x0 = mp.sqrt(L)/beta
    return beta * x0 * mp.besseli(nu+1, x0) / mp.besseli(nu, x0)

print("="*72)
print("A. mode-equation residual for both Bessel branches (q=1/3, ell=1)")
q = mp.mpf(1)/3
F, G, w, beta, m, nu, L = collar(q, 1)
for name, f in (("F", F), ("G", G)):
    y0 = mp.mpf("0.7")
    res = mp.diff(f, y0, 2) + (2 - q/2)*mp.diff(f, y0)/y0 - L*y0**(q-2)*f(y0)
    check(f"residual({name}) ~ 0 (rel)", abs(res)/abs(L*y0**(q-2)*f(y0)) < mp.mpf(10)**-25)

print("="*72)
print("B. two-boundary DtN: symmetry and closed-form off-diagonal")
for ell in (1, 2):
    for yc in ("0.5", "0.2", "0.05"):
        Lcc, Lc0, L0c, L00 = dtn_matrix(q, ell, yc)
        check(f"Lc0=L0c  ell={ell} yc={yc}", abs(Lc0-L0c)/abs(Lc0) < mp.mpf(10)**-25)
        # closed form b = +W0/Delta with W0 = beta*(sqrt(L)/beta)^{2m},
        # Delta = F(yc)G(1)-G(yc)F(1)   (Delta<0 as yc->0, so b<0)
        F, G, wfun, beta, m, nu, L = collar(q, ell)
        W0 = beta*(mp.sqrt(L)/beta)**(2*m)
        Delta = F(mp.mpf(yc))*G(mp.mpf(1)) - G(mp.mpf(yc))*F(mp.mpf(1))
        check(f"b = W0/Delta ell={ell} yc={yc}", abs(Lc0 - W0/Delta)/abs(Lc0) < mp.mpf(10)**-22)

# Wronskian constancy
F, G, wfun, beta, m, nu, L = collar(q, 1)
vals = [wfun(y)*(F(y)*dmode(G,y) - G(y)*dmode(F,y)) for y in (mp.mpf("0.3"), mp.mpf("0.8"))]
check("w(FG'-GF') constant", abs(vals[0]-vals[1])/abs(vals[0]) < mp.mpf(10)**-25)
check("w(FG'-GF') = -beta(sqrtL/beta)^{2m}", abs(vals[0] + beta*(mp.sqrt(L)/beta)**(2*m))/abs(vals[0]) < mp.mpf(10)**-25)

print("="*72)
print("C. regular-core limit and vanishing rates")
banked = {1: mp.mpf("0.979663326282794223"),
          2: mp.mpf("1.98578554532783401"),
          3: mp.mpf("2.98930596601578915")}
for ell in (1,2,3):
    check(f"D_{ell} matches banked", abs(D_ell(q, ell)-banked[ell]) < mp.mpf(10)**-17)
Bratio = mp.besseli(mp.mpf(7)/2, 6*mp.sqrt(2))/mp.besseli(mp.mpf(5)/2, 6*mp.sqrt(2))
check("B = D_1/sqrt(2)", abs(Bratio - D_ell(q,1)/mp.sqrt(2)) < mp.mpf(10)**-30)

expo = (2-q)/2  # predicted vanishing exponent = 5/6 at q=1/3
# asymptotic regime requires x_c = (sqrt(L)/beta) yc^beta << 1, i.e. very small yc
for ell in (1, 2):
    F, G, wfun, beta, m, nu, L = collar(q, ell)
    bconst_pred = -beta/(2**(nu-1)*mp.gamma(nu)*F(mp.mpf(1)))  # derived asymptote
    rows = []
    for yc in ("1e-16", "1e-20", "1e-24"):
        Lcc, Lc0, L0c, L00 = dtn_matrix(q, ell, yc)
        ycm = mp.mpf(yc)
        rows.append((ycm, Lcc/ycm**expo, Lc0/ycm**expo, L00 - D_ell(q, ell)))
    c1, c2 = rows[-2][1], rows[-1][1]
    check(f"Lcc ~ ((2-q)/2) yc^(5/6)  ell={ell}", abs(c2 - expo)/expo < mp.mpf(10)**-2 and abs(c2-expo) < abs(c1-expo))
    b1, b2 = rows[-2][2], rows[-1][2]
    check(f"b_ell -> -beta/(2^(nu-1)Gamma(nu)F_ell(1)) yc^(5/6)  ell={ell}",
          abs(b2-bconst_pred)/abs(bconst_pred) < mp.mpf(10)**-2 and abs(b2-bconst_pred) < abs(b1-bconst_pred))
    check(f"L00 -> D_ell  ell={ell}", abs(rows[-1][3]) < mp.mpf(10)**-3 and abs(rows[-1][3]) < abs(rows[-2][3]))
    print(f"    ell={ell}: b/yc^(5/6) at 1e-20,1e-24: {mp.nstr(b1,12)}, {mp.nstr(b2,12)}; pred {mp.nstr(bconst_pred,12)}")
    print(f"    ell={ell}: Lcc/yc^(5/6) -> {mp.nstr(c2,12)} (target 5/6 = {mp.nstr(expo,12)})")

# q-generality of the exponent at q=0.4 -> (2-q)/2 = 0.8
q2 = mp.mpf("0.4"); expo2 = (2-q2)/2
r = []
for yc in ("1e-20","1e-24"):
    Lcc, Lc0, L0c, L00 = dtn_matrix(q2, 1, yc)
    r.append(Lcc/mp.mpf(yc)**expo2)
check("exponent (2-q)/2 generalizes (q=0.4)", abs(r[1]-expo2)/expo2 < mp.mpf(10)**-2 and abs(r[1]-expo2) < abs(r[0]-expo2))

print("="*72)
print("D. Schur identity: free-core elimination == Neumann-inner DtN")
for ell in (1,2):
    for yc in ("0.3","0.05"):
        Lcc, Lc0, L0c, L00 = dtn_matrix(q, ell, yc)
        schur = L00 - Lc0*L0c/Lcc
        F, G, wfun, beta, m, nu, L = collar(q, ell)
        ycm = mp.mpf(yc)
        rho = lambda y: F(y)*dmode(G, ycm) - G(y)*dmode(F, ycm)   # rho'(yc)=0
        dtnN = wfun(mp.mpf(1))*dmode(rho, mp.mpf(1))/rho(mp.mpf(1))
        check(f"Schur == Neumann DtN ell={ell} yc={yc}", abs(schur-dtnN)/abs(dtnN) < mp.mpf(10)**-22)
# limit of the Schur-eliminated operator
sch = []
for yc in ("1e-4","1e-5"):
    Lcc, Lc0, L0c, L00 = dtn_matrix(q, 1, yc)
    sch.append(L00 - Lc0*L0c/Lcc)
check("Schur(free core) -> D_1 as yc->0", abs(sch[1]-D_ell(q,1)) < abs(sch[0]-D_ell(q,1)) and abs(sch[1]-D_ell(q,1)) < mp.mpf(10)**-3)
print(f"    Schur DtN at yc=1e-5: {mp.nstr(sch[1],14)} vs D_1 = {mp.nstr(D_ell(q,1),14)}")

print("="*72)
print("E. exact composition / bookkeeping identities (rationals)")
from fractions import Fraction
qf = Fraction(1,3); eta = (qf/2)/3
check("eta = 1/18", eta == Fraction(1,18))
check("eta/2 + eta/2 = eta (glued edge)", eta/2 + eta/2 == eta)
for s, depth in ((1,5),(2,7)):
    check(f"3+2s = depth (s={s})", 3 + 2*s == depth)
    # per-cell attribution: glued frame action 3*eta splits to 3*eta/2 per cell;
    # glued phi0-shape action 2*s*(eta/2)... per-cell ladder exponent depth*eta/2
    percell = 3*(eta/2) + s*(eta/2) + s*(eta/2)   # frame + core-side + phi0-side
    check(f"per-cell exponent = depth*eta/2 (s={s})", percell == depth*eta/2)

gamma_local  = 3*mp.e**(-mp.mpf(1)/36)
gamma_warped = 3*mp.e**(-Bratio/36)
print(f"    gamma_local  = {mp.nstr(gamma_local, 13)}")
print(f"    gamma_warped = {mp.nstr(gamma_warped, 13)}")
print(f"    B            = {mp.nstr(Bratio, 13)}")

print("="*72)
print("F. branch-coefficient formula records (normalization N EXPLICIT, set N=1")
print("   for the record value only; NO comparison to any data is made)")
D1 = D_ell(q,1)
recs = {
 "warped, glued E1 phi0-pair factor  2*pi/(2*N*D1) @N=1": 2*mp.pi/(2*D1),
 "warped, ratio C_E1/C_M1 (M1-flat scenario)  pi/(N*D1) @N=1": mp.pi/D1,
 "warped, ratio C_E1/C_M1 (M1-stiff scenario) sqrt(pi/(N*D1)) @N=1": mp.sqrt(mp.pi/D1),
 "intrinsic, glued edge eigenvalue eta = 1/18": mp.mpf(1)/18,
 "intrinsic, glued E1 phi0-pair factor 2*pi/(N*eta) @N=1": 2*mp.pi*18,
 "intrinsic, ratio C_E1/C_M1 (M1-flat)  2*pi/(N*eta) @N=1": 2*mp.pi*18,
 "shared-frame glued eigenvalue, warped: 2*N*D1 @N=1": 2*D1,
}
for k,v in recs.items():
    print(f"    {k:64s} = {mp.nstr(v, 13)}")

print("="*72)
print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
