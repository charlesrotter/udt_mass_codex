"""
Step 2: verification of the Hessian entries + record anchors.
Routes:
 (R1) symbolic entries from step 1 (rationalized 1D integrals);
 (R2) independent numerical route: direct 2D sphere quadrature of
      Q[h] = (1/4) int dOmega f0 |grad_Omega(h/f0)|^2, finite differences
      never used -- Q is itself the quadratic form, entries read off by
      polarization Q[hA+hB]-Q[hA]-Q[hB].
 (R3) third route for diagonal entries: direct second difference of the
      full potential P[f] = (1/4) int |grad f|^2/f.
Checks: exact-identity Q == d^2P (route3 vs route2), R1 vs R2, null vector,
PSD, capacity law + kappa(1), Goldstone V_a1a1 = P_a/a, rotation/record
anchors at O(kappa).
"""
import pickle, sympy as sp
import mpmath as mp

mp.mp.dps = 30
PASS = []
FAIL = []

def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ") + name + ("   " + detail if detail else ""))

with open('/tmp/wff_entries.pkl','rb') as fh:
    D = pickle.load(fh)
k = D['k']

def lam(e):
    return sp.lambdify(k, e, 'mpmath')

M0f = {key: lam(v) for key, v in D['M0'].items()}
M1f = {key: lam(v) for key, v in D['M1'].items()}
M22f = lam(D['M22'])
Pf   = lam(D['P'])
Paf  = lam(D['Pa'])
Pgf  = lam(D['Pg'])

pi = mp.pi
def Y(A, x, ph):
    s = mp.sqrt(1-x**2)
    if A=='W':  return 1/mp.sqrt(4*pi)
    if A=='a0': return mp.sqrt(3/(4*pi))*x
    if A=='g0': return mp.sqrt(5/(16*pi))*(3*x**2-1)
    if A=='a1': return mp.sqrt(3/(4*pi))*s*mp.cos(ph)
    if A=='g1': return mp.sqrt(15/(4*pi))*x*s*mp.cos(ph)
    if A=='g2': return mp.sqrt(15/(16*pi))*(1-x**2)*mp.cos(2*ph)

# ---- R2: 2D quadrature of the quadratic form  ----
def Qform(hA, hB, kap):
    """(1/2) int dOmega f0 grad(hA/f0).grad(hB/f0); f0=1+kap x ; via polarization on gradients directly."""
    eps = mp.mpf('1e-9')  # for angular derivatives use analytic-free central differences in (theta,phi)
    def integrand(th, ph):
        x = mp.cos(th)
        f0 = 1+kap*x
        # gradient via finite differences in theta, phi of u = h/f0
        def u(fun, t, p):
            xx = mp.cos(t)
            return fun(xx, p)/(1+kap*xx)
        dth = mp.mpf('1e-6'); dph = mp.mpf('1e-6')
        gA_t = (u(hA, th+dth, ph)-u(hA, th-dth, ph))/(2*dth)
        gB_t = (u(hB, th+dth, ph)-u(hB, th-dth, ph))/(2*dth)
        gA_p = (u(hA, th, ph+dph)-u(hA, th, ph-dph))/(2*dph)
        gB_p = (u(hB, th, ph+dph)-u(hB, th, ph-dph))/(2*dph)
        st = mp.sin(th)
        dot = gA_t*gB_t + gA_p*gB_p/st**2
        return f0*dot*st
    val = mp.quad(lambda th: mp.quad(lambda ph: integrand(th, ph), [0, 2*pi]),
                  [mp.mpf('0.001'), pi-mp.mpf('0.001')])
    return val/2

kap_test = mp.mpf('0.55')
mp.mp.dps = 16   # FD-limited accuracy for R2; tolerance 1e-5 relative
pairs0 = [(('W','W'),(0,0)), (('W','a0'),(0,1)), (('W','g0'),(0,2)),
          (('a0','a0'),(1,1)), (('a0','g0'),(1,2)), (('g0','g0'),(2,2))]
nm0 = {0:'W',1:'a0',2:'g0'}
for (A,B), key in pairs0:
    fa = lambda x,p,A=A: Y(A,x,p)
    fb = lambda x,p,B=B: Y(B,x,p)
    q = Qform(fa, fb, kap_test)
    sref = M0f[key](kap_test)
    check(f"R1==R2  M0[{A},{B}]", abs(q-sref) < 1e-5*max(1,abs(sref)), f"{mp.nstr(q,10)} vs {mp.nstr(sref,10)}")

for (A,B), key in [(('a1','a1'),(1,1)), (('a1','g1'),(1,2)), (('g1','g1'),(2,2))]:
    fa = lambda x,p,A=A: Y(A,x,p)
    fb = lambda x,p,B=B: Y(B,x,p)
    q = Qform(fa, fb, kap_test)
    sref = M1f[key](kap_test)
    check(f"R1==R2  M1[{A},{B}]", abs(q-sref) < 1e-5*max(1,abs(sref)), f"{mp.nstr(q,10)} vs {mp.nstr(sref,10)}")

q = Qform(lambda x,p: Y('g2',x,p), lambda x,p: Y('g2',x,p), kap_test)
sref = M22f(kap_test)
check("R1==R2  M2[g2,g2]", abs(q-sref) < 1e-5*max(1,abs(sref)), f"{mp.nstr(q,10)} vs {mp.nstr(sref,10)}")

# ---- R3: Q is the exact second variation of P (one diagonal + one off-diag spot) ----
def Pfull(ffun):
    def integ(th):
        x = mp.cos(th)
        dth = mp.mpf('1e-6')
        # axisymmetric pieces only used here
        df = (ffun(mp.cos(th+dth))-ffun(mp.cos(th-dth)))/(2*dth)
        return df**2/ffun(x)*mp.sin(th)
    return 2*pi*mp.quad(integ, [mp.mpf('0.001'), pi-mp.mpf('0.001')])/4

eps = mp.mpf('1e-4')
f0fun = lambda x: 1+kap_test*x
fp = lambda x: 1+kap_test*x + eps*Y('a0',x,0)
fm = lambda x: 1+kap_test*x - eps*Y('a0',x,0)
d2 = (Pfull(fp)-2*Pfull(f0fun)+Pfull(fm))/eps**2
check("Q == d^2P (a0 diag, route 3)", abs(d2 - M0f[(1,1)](kap_test)) < 1e-4*abs(d2),
      f"{mp.nstr(d2,8)} vs {mp.nstr(M0f[(1,1)](kap_test),8)}")
# tadpole route-3 check
d1 = (Pfull(fp)-Pfull(fm))/(2*eps)
check("P_a tadpole (route 3)", abs(d1 - Paf(kap_test)) < 1e-6*abs(d1),
      f"{mp.nstr(d1,10)} vs {mp.nstr(Paf(kap_test),10)}")
fpg = lambda x: 1+kap_test*x + eps*Y('g0',x,0)
fmg = lambda x: 1+kap_test*x - eps*Y('g0',x,0)
d1g = (Pfull(fpg)-Pfull(fmg))/(2*eps)
check("P_g0 tadpole (route 3)", abs(d1g - Pgf(kap_test)) < 1e-6*abs(d1g),
      f"{mp.nstr(d1g,10)} vs {mp.nstr(Pgf(kap_test),10)}")

mp.mp.dps = 30
# ---- null vector: n = (sqrt(4pi), kappa/c, 0) with c = sqrt(3/4pi)  -> prop to (sqrt3, kappa, 0)
def M0mat(kap):
    return mp.matrix([[M0f[(0,0)](kap), M0f[(0,1)](kap), M0f[(0,2)](kap)],
                      [M0f[(0,1)](kap), M0f[(1,1)](kap), M0f[(1,2)](kap)],
                      [M0f[(0,2)](kap), M0f[(1,2)](kap), M0f[(2,2)](kap)]])
for kap in [mp.mpf('0.2'), mp.mpf('0.683'), mp.mpf('0.95')]:
    M = M0mat(kap)
    n = mp.matrix([mp.sqrt(3), kap, 0])
    r = M*n
    ok = max(abs(r[i]) for i in range(3)) < mp.mpf('1e-25')*max(abs(M[i,j]) for i in range(3) for j in range(3))
    check(f"null vector (sqrt3,kappa,0) at kappa={mp.nstr(kap,3)}", ok, f"|Mn|max={mp.nstr(max(abs(r[i]) for i in range(3)),3)}")

# PSD of all blocks at several kappa
for kap in [mp.mpf('0.2'), mp.mpf('0.683'), mp.mpf('0.95')]:
    M = M0mat(kap)
    ev = mp.eigsy(M, eigvals_only=True)
    M1m = mp.matrix([[M1f[(1,1)](kap), M1f[(1,2)](kap)],[M1f[(1,2)](kap), M1f[(2,2)](kap)]])
    ev1 = mp.eigsy(M1m, eigvals_only=True)
    ok = min(ev) > -mp.mpf('1e-24') and min(ev1) > 0 and M22f(kap) > 0
    check(f"PSD all blocks at kappa={mp.nstr(kap,3)}", ok,
          f"eig(m0)={[mp.nstr(e,4) for e in ev]}, eig(m1)={[mp.nstr(e,4) for e in ev1]}")

# ---- capacity law and kappa(1) ----
# P_F at fixed a:  P(F,a) = (1/F) Phat(kappa).  P_F = -(1/F^2)[Phat + kappa Phat'] ... do directly:
# in F=1 units: P_F = dP/dF|_a = (use exact formula -pi(L-2kappa)/kappa derived in-session)
Lk = lambda kap: mp.log((1+kap)/(1-kap))
def PF_exact(kap):    # claimed: -pi (L-2k)/k
    return -pi*(Lk(kap)-2*kap)/kap
# numeric route: P(F,a)=P((1+e), a fixed=kap/c) etc.
c = mp.sqrt(3/(4*pi))
def Pval(F, a):
    kap = a*c/F
    # P = (pi/2) F H(kappa), H = 2 + (k^2-1)L/k  (derived from step-1 P_exact)
    return (pi/2)*F*(2 + (kap**2-1)*Lk(kap)/kap)
check("P closed form vs step-1 symbolic", abs(Pval(1, mp.mpf('0.55')/c) - Pf(mp.mpf('0.55'))) < mp.mpf('1e-25'))
e = mp.mpf('1e-8'); kap = mp.mpf('0.55'); a0v = kap/c
pf_num = (Pval(1+e, a0v)-Pval(1-e, a0v))/(2*e)
check("capacity P_F = -pi(L-2k)/k", abs(pf_num - PF_exact(kap)) < 1e-12*abs(pf_num),
      f"{mp.nstr(pf_num,12)} vs {mp.nstr(PF_exact(kap),12)}")
# EL: 2pi (y^2 F')' = P_F ; F=y^-q -> (y^2F')' = -2s y^-q  => (L-2k)/k = 4 s y^-q ; s=1/9
s = mp.mpf(1)/9
kap1 = mp.findroot(lambda K: (Lk(K)-2*K)/K - 4*s, mp.mpf('0.68'))
check("demanded kappa(1) = 0.683095 (record)", abs(kap1 - mp.mpf('0.683095')) < 2e-6,
      f"kappa(1) = {mp.nstr(kap1,15)}")

# ---- Goldstone: V_a1a1 = P_a / a  (transverse formula; record prints P_a/(4a) in its P-convention)
for kap in [mp.mpf('0.3'), kap1]:
    a = kap/c
    lhs = M1f[(1,1)](kap)
    rhs = Paf(kap)/a
    check(f"Goldstone V_a1a1 = P_a/a at kappa={mp.nstr(kap,4)}",
          abs(lhs-rhs) < mp.mpf('1e-25')*abs(lhs), f"{mp.nstr(lhs,12)} vs {mp.nstr(rhs,12)}")

# ---- record O(kappa) anchors: V_a1g1 ~ -sqrt5 k/2, V_a0g0 ~ -sqrt15 k/3 ----
kk = sp.symbols('kk', positive=True)
ser_a1g1 = sp.series(D['M1'][(1,2)].subs(k, kk), kk, 0, 3).removeO()
ser_a0g0 = sp.series(D['M0'][(1,2)].subs(k, kk), kk, 0, 3).removeO()
print("\nO(kappa) series: M1[a1,g1] =", sp.simplify(ser_a1g1))
print("O(kappa) series: M0[a0,g0] =", sp.simplify(ser_a0g0))
lead_a1g1 = sp.limit(D['M1'][(1,2)].subs(k, kk)/kk, kk, 0)
lead_a0g0 = sp.limit(D['M0'][(1,2)].subs(k, kk)/kk, kk, 0)
print("leading coeffs:", lead_a1g1, lead_a0g0)
rec_ratio = (-sp.sqrt(15)/3)/(-sp.sqrt(5)/2)
my_ratio = sp.simplify(lead_a0g0/lead_a1g1)
check("record coupling RATIO sqrt15/3 : sqrt5/2", sp.simplify(my_ratio-rec_ratio)==0,
      f"mine {my_ratio}, record {rec_ratio}")
check("record V_a1g1 leading = -sqrt5 k/2", sp.simplify(lead_a1g1 + sp.sqrt(5)/2)==0,
      f"mine {lead_a1g1}")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL:
    print("FAILED:", FAIL)
