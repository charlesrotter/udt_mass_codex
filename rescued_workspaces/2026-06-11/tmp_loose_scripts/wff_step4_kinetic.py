"""
Step 4: kinetic lifting of the static elimination, tadpole sensitivity,
omega-sector coefficients.

Exact substitution X = -v(y) W + xi in the quadratic action (jet-exact;
no linearization of physics -- the Hessian/Schur structure IS the second
jet). Dropping xi = leading adiabatic order; the xi-coupling is the
O((V^-1 K)^2) remainder, quantified below.

Kept-channel normal form (derived in-session, scalar/vector v):
  (y^2 u')' = [ 2 S_c/(1+|v|^2) + y^2(|v'|^2(1+|v|^2)-(v.v')^2)/(1+|v|^2)^2 ] u
For the m=0 monopole W: S_c = 0 exactly (rank degeneracy) and
  v = (-kappa/sqrt3, 0) EXACTLY (response = scaling direction), giving
  mu_eff^W(y) = 3 y^2 kappa'^2 / (3+kappa^2)^2.
"""
import pickle, sympy as sp
import mpmath as mp
mp.mp.dps = 25
PASS=[];FAIL=[]
def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ")+name+("   "+detail if detail else ""))

with open('/tmp/wff_entries.pkl','rb') as fh:
    D = pickle.load(fh)
k = D['k']
M0, M1, M22sym, Pgsym = D['M0'], D['M1'], D['M22'], D['Pg']

# --- claim: v = M_XX^{-1} M_XW = (-kappa/sqrt3, 0) exactly ---
MXX = sp.Matrix([[M0[(1,1)],M0[(1,2)]],[M0[(1,2)],M0[(2,2)]]])
MXW = sp.Matrix([[M0[(0,1)]],[M0[(0,2)]]])
vvec = sp.simplify(MXX.inv()*MXW)
check("m=0 response v = (-k/sqrt3, 0) exact",
      sp.simplify(vvec[0,0]+k/sp.sqrt(3))==0 and sp.simplify(vvec[1,0])==0,
      f"v = ({sp.simplify(vvec[0,0])}, {sp.simplify(vvec[1,0])})")

# --- m=1 response v1 = M_ag/M_gg ---
v1sym = sp.simplify(M1[(1,2)]/M1[(2,2)])
S1sym = sp.simplify(M1[(1,1)] - M1[(1,2)]**2/M1[(2,2)])

Lk = lambda K: mp.log((1+K)/(1-K))
R  = lambda K: (Lk(K)-2*K)/K
def Rp(K): return 2*K/(1-K**2) - R(K)/K
def ykp(K):                      # y * dkappa/dy  (chain rule from capacity law)
    return -R(K)/(3*Rp(K))
def y_of(K): return ((mp.mpf(9)/4)*R(K))**(-3)

kap1 = mp.findroot(lambda K: R(K) - mp.mpf(4)/9, mp.mpf('0.68'))
# numeric check of ykp by finite difference in y
K2 = mp.findroot(lambda K: R(K) - mp.mpf(4)/9*(mp.mpf('1.001'))**(-mp.mpf(1)/3), kap1)
fd = (K2-kap1)/mp.mpf('0.001')
check("y kappa'(y) chain-rule formula", abs(fd - ykp(kap1)) < 1e-3*abs(fd),
      f"{mp.nstr(fd,8)} vs {mp.nstr(ykp(kap1),8)}")

# ---------------- m=0 W channel: lifted mass ----------------
def muW(K):
    yk = ykp(K); y = y_of(K)
    kp = yk/y
    return 3*(y*kp)**2/(3+K**2)**2     # = 3 (y kappa')^2/(3+k^2)^2 ; y^2 kp^2 = yk^2
print("\n-- m=0 monopole channel, kinetic-lifted mu_eff(y) = 3 y^2 k'^2/(3+k^2)^2 --")
print(f"{'y':>10} {'kappa':>8} {'mu_eff^W':>14} {'n_eff^W':>14}")
for K in [mp.mpf(x) for x in ['0.95','0.9','0.8','0.683095140037122','0.6','0.5','0.4','0.3','0.2','0.1']]:
    mu = muW(K)
    print(f"{mp.nstr(y_of(K),5):>10} {mp.nstr(K,4):>8} {mp.nstr(mu,8):>14} {mp.nstr(1-mp.mpf(9)/2*mu,8):>14}")
muW1 = muW(kap1)
print("ANCHOR  mu_eff^W(y=1) =", mp.nstr(muW1, 13), "  n_eff^W(y=1) =", mp.nstr(1-mp.mpf(9)/2*muW1, 13))
# kappa->0 limit of mu_eff^W and n_eff^W
for K in [mp.mpf('0.01'), mp.mpf('0.001')]:
    print("   small-kappa probe:", mp.nstr(K,3), mp.nstr(muW(K),6), "n:", mp.nstr(1-4.5*muW(K),8))

# ---------------- m=1 a-channel with gradient correction ----------------
v1f = sp.lambdify(k, v1sym, 'mpmath')
dv1f = sp.lambdify(k, sp.diff(v1sym, k), 'mpmath')
S1f  = sp.lambdify(k, S1sym, 'mpmath')
def mu_m1(K):
    y = y_of(K); yk = ykp(K)
    v1 = v1f(K); s2 = 1+v1**2
    v1p_y = dv1f(K)*yk/y           # dv1/dy
    Sc = y**(mp.mpf(1)/3)*S1f(K)   # y^q * S(kappa)
    grad = (y*v1p_y)**2/s2**2
    mu = 2*Sc/s2 + grad - 2*y**(mp.mpf(1)/3)
    return mu, 2*Sc/s2, grad
print("\n-- m=1 a-channel (lambda=2): static vs gradient-corrected --")
print(f"{'y':>10} {'kappa':>8} {'mu_static':>13} {'mu_grad_add':>13} {'lam_renorm 2S/s2-2S':>12} {'n_eff(grad)':>13}")
for K in [mp.mpf(x) for x in ['0.9','0.8','0.683095140037122','0.5','0.3','0.1']]:
    y = y_of(K)
    mu, pot, grad = mu_m1(K)
    mu_stat = 2*y**(mp.mpf(1)/3)*S1f(K) - 2*y**(mp.mpf(1)/3)
    print(f"{mp.nstr(y,5):>10} {mp.nstr(K,4):>8} {mp.nstr(mu_stat,7):>13} {mp.nstr(grad,7):>13} "
          f"{mp.nstr(pot-2*y**(mp.mpf(1)/3)*S1f(K),7):>12} {mp.nstr(1-mp.mpf(9)/2*mu,8):>13}")
mu1, pot1, grad1 = mu_m1(kap1)
print("ANCHOR m=1 a: mu_eff(grad-corrected, y=1) =", mp.nstr(mu1,13),
      " n_eff =", mp.nstr(1-mp.mpf(9)/2*mu1,13))
print("   v1(kappa1) =", mp.nstr(v1f(kap1),13), "  v1^2 =", mp.nstr(v1f(kap1)**2,8))

# ---------------- expansion-parameter honesty ----------------
# next order ~ ||V_XX^{-1} K|| on the response profile: r = |(y^2 (v)')'/2| / |2 V_min v|
M0f = {key: sp.lambdify(k, v, 'mpmath') for key, v in M0.items()}
M1f = {key: sp.lambdify(k, v, 'mpmath') for key, v in M1.items()}
def vW_of_y(y):
    K = mp.findroot(lambda K: R(K) - mp.mpf(4)/9*y**(-mp.mpf(1)/3), mp.mpf('0.6'))
    return -K/mp.sqrt(3)
h = mp.mpf('1e-4')
y0 = mp.mpf(1)
d2 = (vW_of_y(y0+h)-2*vW_of_y(y0)+vW_of_y(y0-h))/h**2
d1 = (vW_of_y(y0+h)-vW_of_y(y0-h))/(2*h)
Kv = abs(y0**2*d2 + 2*y0*d1)/2
lam_min0 = min(mp.eigsy(mp.matrix([[M0f[(1,1)](kap1),M0f[(1,2)](kap1)],
                                    [M0f[(1,2)](kap1),M0f[(2,2)](kap1)]]), eigvals_only=True))
r_ad0 = Kv/(lam_min0*abs(vW_of_y(y0)))
print("\nadiabatic control parameter (m=0, y=1):  |K v|/(lam_min |v|) =", mp.nstr(r_ad0,6))
def v1_of_y(y):
    K = mp.findroot(lambda K: R(K) - mp.mpf(4)/9*y**(-mp.mpf(1)/3), mp.mpf('0.6'))
    return v1f(K)
d2 = (v1_of_y(y0+h)-2*v1_of_y(y0)+v1_of_y(y0-h))/h**2
d1 = (v1_of_y(y0+h)-v1_of_y(y0-h))/(2*h)
Kv1 = abs(y0**2*d2 + 2*y0*d1)/2
r_ad1 = Kv1/(M1f[(2,2)](kap1)*abs(v1f(kap1)))
print("adiabatic control parameter (m=1, y=1):  |K v1|/(M_gg |v1|) =", mp.nstr(r_ad1,6))

# ---------------- omega sector coefficients ----------------
MXXn = mp.matrix([[M0f[(1,1)](kap1),M0f[(1,2)](kap1)],[M0f[(1,2)](kap1),M0f[(2,2)](kap1)]])
ev, Q = mp.eigsy(MXXn)
MXWn = mp.matrix([M0f[(0,1)](kap1), M0f[(0,2)](kap1)])
c = Q.T*MXWn
print("\n-- omega sector (y=1, kappa1; weight tau conditional) --")
print("V_XX eigenvalues (m=0):", [mp.nstr(e,12) for e in ev])
print("coupling weights c_i^2/lam_i^2:", [mp.nstr((c[i]/ev[i])**2,10) for i in range(2)])
print("sum = |v|^2 =", mp.nstr(sum((c[i]/ev[i])**2 for i in range(2)),12),
      " vs kappa^2/3 =", mp.nstr(kap1**2/3,12))
check("omega-coefficient |v|^2 = kappa^2/3",
      abs(sum((c[i]/ev[i])**2 for i in range(2)) - kap1**2/3) < 1e-20)
print("m=1: inertia factor 1+v1^2 =", mp.nstr(1+v1f(kap1)**2,12),
      "; first resonance scale 2*V_gg =", mp.nstr(2*M1f[(2,2)](kap1),12))

# ---------------- ell=2 tadpole sensitivity ----------------
Pgf = sp.lambdify(k, Pgsym, 'mpmath')
M22f = sp.lambdify(k, M22sym, 'mpmath')
eps2 = -Pgf(kap1)/M0f[(2,2)](kap1)     # static local ell=2 response amplitude (per F)
print("\n-- ell=2 tadpole --")
print("P_g0(kappa1) =", mp.nstr(Pgf(kap1),10), "  M_g0g0 =", mp.nstr(M0f[(2,2)](kap1),10),
      "  eps2 = -P_g/M_gg =", mp.nstr(eps2,10))

pi = mp.pi
c10 = mp.sqrt(3/(4*pi)); c20v = mp.sqrt(5/(16*pi))
c11 = mp.sqrt(3/(4*pi)); c21 = mp.sqrt(15/(4*pi)); c22 = mp.sqrt(15/(16*pi))
def f0_shift(x, K, e2):
    return 1 + K*x + e2*c20v*(3*x**2-1)
def entry_num(gA, gB, m, K, e2):
    def integ(x):
        f0 = f0_shift(x, K, e2)
        dx = mp.mpf('1e-6')
        uA = lambda xx: gA(xx)/f0_shift(xx, K, e2)
        uB = lambda xx: gB(xx)/f0_shift(xx, K, e2)
        duA = (uA(x+dx)-uA(x-dx))/(2*dx)
        duB = (uB(x+dx)-uB(x-dx))/(2*dx)
        t = (1-x**2)*duA*duB
        if m: t += m**2*uA(x)*uB(x)/(1-x**2)
        return f0*t
    cm = 2*pi if m==0 else pi
    return cm/2*mp.quad(integ, [-1+mp.mpf('1e-8'), 1-mp.mpf('1e-8')])
gA1 = lambda x: c11*mp.sqrt(1-x**2)
gG1 = lambda x: c21*x*mp.sqrt(1-x**2)
gG2 = lambda x: c22*(1-x**2)
mp.mp.dps = 16
# sanity: e2=0 reproduces symbolic
t0 = entry_num(gA1, gA1, 1, kap1, 0)
check("numeric entry route at eps2=0 (M1_aa)", abs(t0-M1f[(1,1)](kap1))<1e-7, f"{mp.nstr(t0,10)}")
Maa = entry_num(gA1, gA1, 1, kap1, eps2)
Mag = entry_num(gA1, gG1, 1, kap1, eps2)
Mgg = entry_num(gG1, gG1, 1, kap1, eps2)
M2s = entry_num(gG2, gG2, 2, kap1, eps2)
S1_shift = Maa - Mag**2/Mgg
Lv = Lk(kap1)
def neff_static(Mefv, lamv, K):
    return 1 - 2*K*(2*Mefv-lamv)/(Lk(K)-2*K)
n_m1a_shift = neff_static(S1_shift, 2, kap1)
n_m1a_orig  = neff_static(S1f(kap1), 2, kap1)
n_m2_shift  = neff_static(M2s, 6, kap1)
n_m2_orig   = neff_static(M22f(kap1), 6, kap1)
Sg_shift = Mgg - Mag**2/Maa
Sg_orig  = M1f[(2,2)](kap1) - M1f[(1,2)](kap1)**2/M1f[(1,1)](kap1)
n_m1g_shift = neff_static(Sg_shift, 6, kap1)
n_m1g_orig  = neff_static(Sg_orig, 6, kap1)
print("\n-- tadpole-shifted background: n_eff at anchor (kappa1 held) --")
print(f"m=1 a-channel: {mp.nstr(n_m1a_orig,10)} -> {mp.nstr(n_m1a_shift,10)}   Delta = {mp.nstr(n_m1a_shift-n_m1a_orig,6)}")
print(f"m=1 g-channel: {mp.nstr(n_m1g_orig,10)} -> {mp.nstr(n_m1g_shift,10)}   Delta = {mp.nstr(n_m1g_shift-n_m1g_orig,6)}")
print(f"m=2 channel  : {mp.nstr(n_m2_orig,10)} -> {mp.nstr(n_m2_shift,10)}   Delta = {mp.nstr(n_m2_shift-n_m2_orig,6)}")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL: print("FAILED:", FAIL)
