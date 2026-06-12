"""Scratch verification for the DtN/Calderon derivation of S_phi0[typed nodes].

All checks PASS/FAIL printed. mpmath high precision. No repo files touched.
"""
import mpmath as mp

mp.mp.dps = 40
PASS = 0
FAIL = 0
def check(name, ok, detail=""):
    global PASS, FAIL
    if ok: PASS += 1
    else: FAIL += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")

q = mp.mpf(1)/3
beta = q/2                      # 1/6
nu = abs((1 - 2/q)/2)           # 5/2
eta = q/6                       # 1/18

def x_of(y, lam):
    return mp.sqrt(lam) * y**beta / beta

def a_reg(y, lam):
    x = x_of(y, lam)
    m = (1 - 2/q)/2             # -5/2
    return x**m * mp.besseli(nu, x)

def D_of(lam):
    if lam == 0: return mp.mpf(0)
    x0 = mp.sqrt(lam)/beta
    return beta * x0 * mp.besseli(nu+1, x0) / mp.besseli(nu, x0)

def B_of(lam):
    """relative dressing B(lam) = D(lam)/sqrt(lam) = I_{nu+1}(x0)/I_nu(x0)."""
    x0 = mp.sqrt(lam)/beta
    return mp.besseli(nu+1, x0) / mp.besseli(nu, x0)

# ---------------------------------------------------------------
# CHECK 1: a_reg solves the banked mode equation
#   a'' + (2-q/2) a'/y - lam y^(q-2) a = 0
# at several y for lam = 2 (ell=1), 1/2 (M1 monopole), 6 (ell=2)
for lam in (mp.mpf(2), mp.mpf(1)/2, mp.mpf(6), mp.mpf(1)):
    ok = True
    for yy in (mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.9')):
        f  = lambda t, l=lam: a_reg(t, l)
        d1 = mp.diff(f, yy)
        d2 = mp.diff(f, yy, 2)
        res = d2 + (2 - q/2)*d1/yy - lam*yy**(q-2)*f(yy)
        scale = abs(d2) + abs(d1/yy) + abs(lam*yy**(q-2)*f(yy))
        ok = ok and abs(res)/scale < mp.mpf('1e-25')
    check(f"mode equation solved by x^m I_nu(x), lam={lam}", ok)

# CHECK 2: Sturm-Liouville form equivalence (w a')' = lam v a, w=y^(2-q/2), v=y^(q/2)
lam = mp.mpf(2)
yy = mp.mpf('0.7')
w  = lambda t: t**(2 - q/2)
g  = lambda t: w(t)*mp.diff(lambda s: a_reg(s, lam), t)
lhs = mp.diff(g, yy)
rhs = lam * yy**(q/2) * a_reg(yy, lam)
check("Sturm-Liouville form (w a')' = lam v a", abs(lhs-rhs)/abs(rhs) < mp.mpf('1e-22'),
      f"rel err {mp.nstr(abs(lhs-rhs)/abs(rhs),3)}")

# CHECK 3: DtN values reproduce banked digits
D1 = D_of(2); D2v = D_of(6); D3 = D_of(12)
check("D_1 banked", abs(D1 - mp.mpf('0.979663326282794223')) < mp.mpf('1e-17'), mp.nstr(D1, 20))
check("D_2 banked", abs(D2v - mp.mpf('1.98578554532783401')) < mp.mpf('1e-16'), mp.nstr(D2v, 20))
check("D_3 banked", abs(D3 - mp.mpf('2.98930596601578915')) < mp.mpf('1e-16'), mp.nstr(D3, 20))
B2 = B_of(2)
check("B banked = 0.692726581294", abs(B2 - mp.mpf('0.692726581294')) < mp.mpf('1e-12'), mp.nstr(B2, 20))
check("D_1 = sqrt(2) B", abs(D1 - mp.sqrt(2)*B2) < mp.mpf('1e-30'))

# CHECK 4: deep-end boundary term w a a' -> 0 with exponent 1+q/2 = 7/6
lam = mp.mpf(2)
vals = []
for yy in (mp.mpf('1e-4'), mp.mpf('1e-5')):
    t = w(yy)*a_reg(yy, lam)*mp.diff(lambda s: a_reg(s, lam), yy)
    vals.append(t)
slope = mp.log(vals[1]/vals[0]) / mp.log(mp.mpf('1e-5')/mp.mpf('1e-4'))
check("deep-end flux exponent = 7/6", abs(slope - mp.mpf(7)/6) < mp.mpf('1e-3'), mp.nstr(slope, 8))

# CHECK 5: on-shell action equals (1/2) D(lam) u^2  (Dirichlet principle), u = a(1)
for lam in (mp.mpf(2), mp.mpf(1)/2):
    uu = a_reg(mp.mpf(1), lam)
    integrand = lambda t, l=lam: w(t)*mp.diff(lambda s: a_reg(s, l), t)**2 \
                                 + l*t**(q/2)*a_reg(t, l)**2
    Sbulk = mp.mpf('0.5')*mp.quad(integrand, [0, 1])
    Sbdy  = mp.mpf('0.5')*D_of(lam)*uu**2
    check(f"on-shell bulk action = (1/2) D u^2, lam={lam}",
          abs(Sbulk - Sbdy)/abs(Sbdy) < mp.mpf('1e-20'),
          f"rel err {mp.nstr(abs(Sbulk-Sbdy)/abs(Sbdy),3)}")

# ---------------------------------------------------------------
# CHECK 6: two-end DtN matrix on [yc,1]; self-similar limit decoupling.
# Solve with two independent solutions: a_reg and a_sing = x^m K_nu(x).
def a_sing(y, lam):
    x = x_of(y, lam)
    m = (1 - 2/q)/2
    return x**m * mp.besselk(nu, x)

def two_end_K(yc, lam):
    """K matrix of quadratic form S=(1/2)[u_c,u_0] K [u_c,u_0]^T on [yc,1]."""
    # basis solutions and derivatives at the ends
    f1 = lambda t: a_reg(t, lam); f2 = lambda t: a_sing(t, lam)
    M = mp.matrix([[f1(yc), f2(yc)], [f1(mp.mpf(1)), f2(mp.mpf(1))]])
    # solution with (u_c, u_0): coeffs = M^{-1} (u_c,u_0)
    Minv = M**-1
    def flux(t, c1, c2):
        d = c1*mp.diff(f1, t) + c2*mp.diff(f2, t)
        return w(t)*d
    K = mp.zeros(2,2)
    for j,(uc,u0) in enumerate(((1,0),(0,1))):
        c = Minv * mp.matrix([uc,u0])
        # S = (1/2)[w a a']_{yc}^{1}; Hessian columns from boundary fluxes:
        # dS/du_c = -flux(yc), dS/du_0 = +flux(1)
        K[0,j] = -flux(yc, c[0], c[1])
        K[1,j] =  flux(mp.mpf(1), c[0], c[1])
    return K

lam = mp.mpf(1)/2
rows = []
for yc in (mp.mpf('1e-2'), mp.mpf('1e-3'), mp.mpf('1e-4')):
    K = two_end_K(yc, lam)
    rows.append((yc, K[0,0], K[0,1], K[1,1]))
# symmetry of K
Ks = two_end_K(mp.mpf('1e-3'), lam)
check("two-end K symmetric", abs(Ks[0,1]-Ks[1,0])/abs(Ks[0,1]) < mp.mpf('1e-20'))
# K_00 -> D(lam)
check("K_00 -> D(lam) as yc->0", abs(rows[-1][3] - D_of(lam))/D_of(lam) < mp.mpf('1e-3'),
      f"K00={mp.nstr(rows[-1][3],10)} vs D={mp.nstr(D_of(lam),10)}")
# off-diagonal scaling exponent 5q/2 = 5/6
e_off = mp.log(abs(rows[2][2]/rows[1][2]))/mp.log(rows[2][0]/rows[1][0])
check("end-to-end coupling ~ yc^(5/6)", abs(e_off - mp.mpf(5)/6) < mp.mpf('1e-2'), mp.nstr(e_off, 8))
# K_cc -> 0
e_cc = mp.log(abs(rows[2][1]/rows[1][1]))/mp.log(rows[2][0]/rows[1][0])
check("deep-end diagonal K_cc -> 0 (positive exponent)", e_cc > 0, f"exponent {mp.nstr(e_cc,8)}")
print("    two-end K rows (yc, K_cc, K_c0, K_00):")
for r in rows:
    print("      ", mp.nstr(r[0],3), mp.nstr(r[1],8), mp.nstr(r[2],8), mp.nstr(r[3],10))

# ---------------------------------------------------------------
# CHECK 7: two-sided Calderon projector, general + symmetric weld + Dirichlet limit
def calderon(Dm, Dp):
    s = Dm + Dp
    return mp.matrix([[Dp/s, 1/s],[Dm*Dp/s, Dm/s]])

Dm, Dp = D_of(2), mp.mpf(3)   # generic pair
C = calderon(Dm, Dp)
check("Calderon idempotent C^2=C", mp.norm(C*C - C) < mp.mpf('1e-30'))
Cc = mp.eye(2) - C
check("complement idempotent", mp.norm(Cc*Cc - Cc) < mp.mpf('1e-30'))
v = mp.matrix([1, Dm]); check("C fixes core graph (1,D-)", mp.norm(C*v - v) < mp.mpf('1e-28'))
v2 = mp.matrix([1, -Dp]); check("C kills exterior graph (1,-D+)", mp.norm(C*v2) < mp.mpf('1e-28'))
# symmetric weld
Csym = calderon(Dm, Dm)
check("symmetric weld C = (1/2)[[1,1/D],[D,1]]",
      mp.norm(Csym - mp.matrix([[mp.mpf('0.5'), 1/(2*Dm)],[Dm/2, mp.mpf('0.5')]])) < mp.mpf('1e-30'))
# Dirichlet-fiber limit -> banked P_lambda
lamg = eta/2
Pl = mp.matrix([[1,0],[lamg,0]])
Cl = calderon(lamg, mp.mpf('1e25'))
check("D_ext->inf limit = banked P_{eta/2}", mp.norm(Cl - Pl) < mp.mpf('1e-20'))
check("banked P_{eta/2} idempotent", mp.norm(Pl*Pl - Pl) < mp.mpf('1e-30'))

# ---------------------------------------------------------------
# CHECK 8: monopole eigenvalues (tensor identity): lam = j(j+1) - (n/2)^2
lam_M1 = mp.mpf(1)/2*(mp.mpf(1)/2+1) - mp.mpf(1)/4   # n=1, j=1/2
check("M1 monopole eigenvalue = 1/2, degeneracy 2", lam_M1 == mp.mpf(1)/2)
lam_M2 = mp.mpf(1)*(2) - mp.mpf(1)                   # n=2, j=1
check("M2 (n=2,j=1) eigenvalue = 1, degeneracy 3", lam_M2 == 1)

# CHECK 9: half-integer closed forms ratio identity at x = 3 sqrt(2)
x = 3*mp.sqrt(2)
I52 = mp.sinh(x) - 3*mp.cosh(x)/x + 3*mp.sinh(x)/x**2
I72 = mp.cosh(x) - 6*mp.sinh(x)/x + 15*mp.cosh(x)/x**2 - 15*mp.sinh(x)/x**3
ratio_cf = I72/I52
check("closed-form ratio = Bessel ratio at 3 sqrt2",
      abs(ratio_cf - B_of(mp.mpf(1)/2)) < mp.mpf('1e-30'))

# ---------------------------------------------------------------
# RECORD: 12-digit numerics (record only, no comparisons)
print()
print("=== RECORD (12 digits) ===")
B_half = B_of(mp.mpf(1)/2)
B_one  = B_of(mp.mpf(1))
D_half = D_of(mp.mpf(1)/2)
print("B(2)    = I_{7/2}(6 sqrt2)/I_{5/2}(6 sqrt2)      =", mp.nstr(B2, 13))
print("B(1/2)  = I_{7/2}(3 sqrt2)/I_{5/2}(3 sqrt2)      =", mp.nstr(B_half, 13))
print("B(1)    = I_{7/2}(6)/I_{5/2}(6)                  =", mp.nstr(B_one, 13))
print("D(2)    = sqrt(2) B(2)                           =", mp.nstr(D_of(2), 13))
print("D(1/2)  = (1/sqrt2) B(1/2)                       =", mp.nstr(D_half, 13))
print("D(1)    = B(1)                                   =", mp.nstr(D_of(1), 13))
gam_loc = 3*mp.e**(-eta/2)
gam_wrp = 3*mp.e**(-eta/2*B2)
print("gamma_local  = 3 exp(-1/36)                      =", mp.nstr(gam_loc, 13))
print("gamma_warped = 3 exp(-B(2)/36)                   =", mp.nstr(gam_wrp, 13))
CM1_R1 = mp.e**(eta*(B2 - B_half))
print("C_M1 (R1 per-node dressing, warped) = exp(eta (B(2)-B(1/2))) =", mp.nstr(CM1_R1, 13))
print("C_M1 (R1, local)  = 1")
print("C_E1 (R1, both)   = 1")
CM1_R2w = D_of(2)/D_half
print("C_M1 (R2 Gaussian ratio, warped) = D(2)/D(1/2) = 2B(2)/B(1/2) =", mp.nstr(CM1_R2w, 13))
check("R2 warped identity D(2)/D(1/2) = 2 B(2)/B(1/2)",
      abs(D_of(2)/D_half - 2*B2/B_half) < mp.mpf('1e-30'))
print("C_M1 (R2, intrinsic) = lam_1/lam_M1 = 2/(1/2)   = 4")
print("C_E1 (R2, both)   = 1")
print("M2 record: dressing B(1) =", mp.nstr(B_one, 13), " (n=2, j=1 triplet reading)")
print()
print(f"TOTAL: {PASS} PASS, {FAIL} FAIL")
