"""
Step 3: the responsive elimination and n_eff per block.

Family matching convention (pinned):
  SL family: (y^2 u')' = (lambda y^q + mu) u,  mu = (1-n) q(1-q) = 2s(1-n),
  q = 1/3, s = 1/9, 2s = 2/9.   =>  n_eff = 1 - mu_eff/(2s).
  A channel with quadratic action int (1/4)y^2 x'^2 + (1/2) m(y) x^2 has
  (y^2 x')' = 2 m(y) x, so  mu_eff(y) = 2 m(y) - lambda y^q.
  On the demanded background F = y^{-q}, V_AB = y^q M_AB(kappa(y)) and
  y^{-q} = (9/4)(L-2kappa)/kappa  (capacity law), hence STATIC-algebraic
     mu_eff/(2s) = 2 kappa (2 M_eff(kappa) - lambda) / (L - 2 kappa)
     n_eff(kappa) = 1 - 2 kappa (2 M_eff - lambda)/(L - 2 kappa).
"""
import pickle, sympy as sp
import mpmath as mp
mp.mp.dps = 30
PASS=[];FAIL=[]
def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ")+name+("   "+detail if detail else ""))

with open('/tmp/wff_entries.pkl','rb') as fh:
    D = pickle.load(fh)
k = D['k']
M0, M1, M22, Pg = D['M0'], D['M1'], D['M22'], D['Pg']
Lsym = sp.log((1+k)/(1-k))

# ---------- symbolic n_eff(kappa) per block ----------
lam_a, lam_g = 2, 6
S_m1_a = sp.simplify(M1[(1,1)] - M1[(1,2)]**2/M1[(2,2)])      # a1 kept, gamma1 eliminated
S_m1_g = sp.simplify(M1[(2,2)] - M1[(1,2)]**2/M1[(1,1)])      # gamma1 kept, a1 eliminated
S_m2   = M22                                                   # no partner in class

def neff_expr(S, lam):
    return 1 - 2*k*(2*S - lam)/(Lsym - 2*k)

n_m1_a   = neff_expr(S_m1_a, lam_a)
n_m1_g   = neff_expr(S_m1_g, lam_g)
n_m2     = neff_expr(S_m2,  lam_g)
# frozen readings (no elimination, partner channel frozen):
n_m1_a_frozen = neff_expr(M1[(1,1)], lam_a)
n_W_frozen    = neff_expr(M0[(0,0)], 0)      # frozen-a reading of the monopole channel

# kappa->0 limits (exact)
lims = {}
for nm, ex in [("m=1 a-channel (lam=2), responsive", n_m1_a),
               ("m=1 g-channel (lam=6), responsive", n_m1_g),
               ("m=2 g-channel (lam=6), diagonal",   n_m2),
               ("m=1 a-channel frozen-gamma",        n_m1_a_frozen),
               ("monopole W frozen-a",               n_W_frozen)]:
    lim0 = sp.limit(ex, k, 0, '+')
    lims[nm] = lim0
    print(f"kappa->0 limit  {nm}:  n_eff -> {lim0}")
check("frozen-a monopole reading -> n = -1 at kappa->0", lims["monopole W frozen-a"]==-1)
check("responsive m=1 a-channel -> 11/10 at kappa->0", lims["m=1 a-channel (lam=2), responsive"]==sp.Rational(11,10),
      str(lims["m=1 a-channel (lam=2), responsive"]))
check("m=1 g-channel -> -25/14", lims["m=1 g-channel (lam=6), responsive"]==sp.Rational(-25,14),
      str(lims["m=1 g-channel (lam=6), responsive"]))
check("m=2 -> -17/7", lims["m=2 g-channel (lam=6), diagonal"]==sp.Rational(-17,7),
      str(lims["m=2 g-channel (lam=6), diagonal"]))
check("frozen-gamma m=1 a-channel -> -7/5", lims["m=1 a-channel frozen-gamma"]==sp.Rational(-7,5),
      str(lims["m=1 a-channel frozen-gamma"]))

# kappa->1 limits
for nm, ex in [("m=1 a resp", n_m1_a), ("m=1 g resp", n_m1_g), ("m=2", n_m2)]:
    lim1 = sp.limit(ex, k, 1, '-')
    print(f"kappa->1 limit  {nm}: n_eff -> {lim1}")
    check(f"deep limit {nm} -> 1", lim1==1)

# m=0 exact flat statements: det(M0)=0 and Schur onto W / onto a0 vanish
M0m = sp.Matrix([[M0[(0,0)],M0[(0,1)],M0[(0,2)]],
                 [M0[(0,1)],M0[(1,1)],M0[(1,2)]],
                 [M0[(0,2)],M0[(1,2)],M0[(2,2)]]])
det = sp.simplify(M0m.det())
check("det M0 == 0 (exact, all kappa)", det==0, str(det))
qW = (sp.Matrix([[M0[(0,1)],M0[(0,2)]]])
      * sp.Matrix([[M0[(1,1)],M0[(1,2)]],[M0[(1,2)],M0[(2,2)]]]).inv()
      * sp.Matrix([[M0[(0,1)]],[M0[(0,2)]]]))[0,0]
check("static Schur onto W == 0 exactly", sp.simplify(M0[(0,0)] - qW)==0, str(sp.simplify(M0[(0,0)]-qW)))
qA = (sp.Matrix([[M0[(0,1)],M0[(1,2)]]])
      * sp.Matrix([[M0[(0,0)],M0[(0,2)]],[M0[(0,2)],M0[(2,2)]]]).inv()
      * sp.Matrix([[M0[(0,1)]],[M0[(1,2)]]]))[0,0]
check("static Schur onto a0 == 0 exactly", sp.simplify(M0[(1,1)] - qA)==0, str(sp.simplify(M0[(1,1)]-qA)))

# ---------- 12-digit record numerics at the anchor kappa(1) ----------
Lk = lambda K: mp.log((1+K)/(1-K))
kap1 = mp.findroot(lambda K: (Lk(K)-2*K)/K - mp.mpf(4)/9, mp.mpf('0.68'))
print("\nkappa(1) =", mp.nstr(kap1, 15))
fns = {nm: sp.lambdify(k, ex, 'mpmath') for nm, ex in
       [("n_m1_a", n_m1_a), ("n_m1_g", n_m1_g), ("n_m2", n_m2),
        ("n_m1_a_frozen", n_m1_a_frozen), ("n_W_frozen", n_W_frozen),
        ("S_m1_a", S_m1_a), ("S_m1_g", S_m1_g)]}
print("\n-- values at the anchor y=1 (kappa = kappa(1)) --")
for nm in ["n_m1_a","n_m1_g","n_m2","n_m1_a_frozen","n_W_frozen"]:
    print(f"{nm}(kappa1) = {mp.nstr(fns[nm](kap1), 13)}")
# mu_eff values too  (mu = 2s(1-n))
for nm in ["n_m1_a","n_m1_g","n_m2"]:
    mu = mp.mpf(2)/9*(1-fns[nm](kap1))
    print(f"mu_eff[{nm}](kappa1) = {mp.nstr(mu, 13)}")

# ---------- profile over the collar ----------
def y_of_kappa(K):
    return ((mp.mpf(9)/4)*(Lk(K)-2*K)/K)**(-3)
print("\n-- collar profile (static-algebraic) --")
print(f"{'y':>10} {'kappa':>10} {'n_m1_a':>12} {'n_m1_g':>12} {'n_m2':>12} {'n_frozen_W':>12}")
for K in [mp.mpf(x) for x in ['0.999','0.99','0.95','0.9','0.8','0.683095140037122','0.6','0.5','0.4','0.3','0.2','0.1','0.05']]:
    print(f"{mp.nstr(y_of_kappa(K),5):>10} {mp.nstr(K,5):>10} {mp.nstr(fns['n_m1_a'](K),7):>12} "
          f"{mp.nstr(fns['n_m1_g'](K),7):>12} {mp.nstr(fns['n_m2'](K),7):>12} {mp.nstr(fns['n_W_frozen'](K),7):>12}")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL: print("FAILED:", FAIL)

import pickle as pk
with open('/tmp/wff_step3.pkl','wb') as fh:
    pk.dump({'n_m1_a': str(sp.simplify(n_m1_a)), 'S_m1_a': str(S_m1_a)}, fh)
