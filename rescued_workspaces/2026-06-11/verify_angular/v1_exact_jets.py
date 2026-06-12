"""
BLIND ADVERSARIAL VERIFIER -- V1: exact eps-jets of covariant C1 in the
full static/stationary perturbation class, INDEPENDENT ROUTE.

Route: build the FULL perturbed metric exactly (no trace formulas, no
perturbative inverse); invert with adjugate/det; Ldens(eps) exact;
L1 = dL/deps|_0, L2 = (1/2) d^2L/deps^2|_0.  Everything downstream
(tadpoles, Hessian, couplings, eliminations) from these.

Conventions frozen to the audit's block (audit_a_jets.py):
  S = -(c/2) Int e^{-2phi} g^{munu} d_mu phi d_nu phi sqrt(-g)
  g_TT = -e^{-2phi}, g_rr = +e^{+2phi}  EXACT TIES
  g_thth = r^2(1+eps(k+w))^2 ; g_vphivphi = r^2 sin^2 (1+eps(k-w))^2
  off-diag: eps*(a,b,p,q,u,v) on (Tr,Tth,Tv,rth,rv,thv)
  phi = phi0(r,th) + eps*dp ; jets (dpT,dpr,dpth,dpv) independent symbols.

Verifier extras the audit did NOT run:
  (X1) covariant stress-tensor cross-check of the ENTIRE tadpole row
  (X2) delta T^r_theta / delta T^r_vphi reading of the q,u eliminations
  (X3) parameterization hostility: exact-areal exponential scheme
       g_thth = r^2 e^{2 eps(k+w)}, g_vv = r^2 s^2 e^{2 eps(k-w)}
       (the ONLY scheme that keeps rho=r to ALL orders) -- does the
       corrected operator change?
  (X4) decomposition of the dpv flip into even (q,w) vs odd (u,v) parts.
"""
import sympy as sp, time

t0 = time.time()
PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

c, r, st = sp.symbols('c r s_theta', positive=True)
phi0, p0r, p0t = sp.symbols('phi0 p0r p0t', real=True)
dp, dpT, dpr, dpth, dpv = sp.symbols('dp dpT dpr dpth dpv', real=True)
a, b, p, k, w, q, u, v = sp.symbols('a b p k w q u v', real=True)
eps = sp.symbols('epsilon', real=True)
f0 = sp.exp(-2*phi0)

def build_L(angular_scheme):
    """angular_scheme in {'audit','areal'}; returns (L0,L1,L2) exact."""
    phif = phi0 + eps*dp
    if angular_scheme == 'audit':
        gthth = r**2*(1 + eps*(k + w))**2
        gvv = r**2*st**2*(1 + eps*(k - w))**2
    else:  # exact-areal exponential: product g_thth*g_vv = r^4 s^2 e^{4 eps k}
        gthth = r**2*sp.exp(2*eps*(k + w))
        gvv = r**2*st**2*sp.exp(2*eps*(k - w))
    g = sp.Matrix([
        [-sp.exp(-2*phif), eps*a,            eps*b,  eps*p],
        [eps*a,            sp.exp(2*phif),   eps*q,  eps*u],
        [eps*b,            eps*q,            gthth,  eps*v],
        [eps*p,            eps*u,            eps*v,  gvv]])
    grad = sp.Matrix([eps*dpT, p0r + eps*dpr, p0t + eps*dpth, eps*dpv])
    det = g.det()
    adj = g.adjugate()
    N = sp.expand((grad.T*adj*grad)[0, 0])
    # Ldens = -(c/2) e^{-2phif} * (N/det) * sqrt(-det)
    Ldens = -(c/2)*sp.exp(-2*phif)*N/det*sp.sqrt(-det)
    L0 = sp.expand(Ldens.subs(eps, 0))
    L1 = sp.expand(sp.diff(Ldens, eps).subs(eps, 0))
    L2 = sp.expand(sp.together(sp.diff(Ldens, eps, 2).subs(eps, 0))/2)
    L2 = sp.expand(sp.powsimp(L2))
    return L0, L1, L2

print("building exact jets (audit scheme)...", flush=True)
L0, L1, L2 = build_L('audit')
print(f"  done in {time.time()-t0:.1f}s", flush=True)

met = [a, b, p, k, w, q, u, v]
names = ['a', 'b', 'p', 'k', 'w', 'q', 'u', 'v']
jets = [dp, dpT, dpr, dpth, dpv]
jn = ['dp', 'dpT', 'dpr', 'dpth', 'dpv']

# ================= A1: tadpole row =================
print("\n--- A1 tadpoles (independent exact route) ---")
T = {}
for s, nm in zip(met, names):
    T[s] = sp.simplify(sp.diff(L1, s))
    print(f"  T[{nm}] = {T[s]}")
check("V1-A1a a,b,p,u,v tadpoles all zero",
      all(T[s] == 0 for s in (a, b, p, u, v)))
check("V1-A1b T_k = -c f0^2 p0r^2 r^2 sin (banked refusal)",
      sp.simplify(T[k] + c*f0**2*p0r**2*r**2*st) == 0)
check("V1-A1c T_q = +c f0^2 p0r p0t sin  (= (c/4) f_r f_th sin)",
      sp.simplify(T[q] - c*f0**2*p0r*p0t*st) == 0)
check("V1-A1d T_w = +c f0 p0t^2 sin  (= (c/4) f_th^2 sin / f)",
      sp.simplify(T[w] - c*f0*p0t**2*st) == 0)

# X1: covariant stress-tensor cross-check of the WHOLE tadpole row.
# T_munu = c e^{-2phi}[phi_mu phi_nu - (1/2) g_munu (dphi)^2]; the
# first variation of S in metric direction dg is
#   delta S = +(1/2) Int sqrt(-g) T^{munu} dg_munu.
print("\n--- X1 stress-tensor cross-check of the tadpole row ---")
g0m = sp.diag(-f0, 1/f0, r**2, r**2*st**2)
gi0 = g0m.inv()
grad0 = sp.Matrix([0, p0r, p0t, 0])
dphi2 = (grad0.T*gi0*grad0)[0, 0]
Tdn = c*f0*(grad0*grad0.T - sp.Rational(1, 2)*g0m*dphi2)
Tup = gi0*Tdn*gi0
S0 = r**2*st
# first-order metric directions (audit normalization):
dirs = {a: [(0, 1)], b: [(0, 2)], p: [(0, 3)], q: [(1, 2)], u: [(1, 3)],
        v: [(2, 3)]}
ok_all = True
for s, nm in zip(met, names):
    if s in dirs:
        (i, j) = dirs[s][0]
        tad = S0*Tup[i, j]  # dg_ij = dg_ji = 1 => (1/2)*2*T^{ij}
    elif s == k:
        tad = sp.Rational(1, 2)*S0*(Tup[2, 2]*2*r**2 + Tup[3, 3]*2*r**2*st**2)
    elif s == w:
        tad = sp.Rational(1, 2)*S0*(Tup[2, 2]*2*r**2 - Tup[3, 3]*2*r**2*st**2)
    res = sp.simplify(tad - T[s])
    if res != 0:
        ok_all = False
        print(f"  MISMATCH in {nm}: {res}")
check("V1-X1 entire tadpole row matches (1/2) sqrt(-g) T^{munu} dg_munu "
      "(covariant stress route, independent of the jet machinery)", ok_all)

# ================= Hessian + couplings =================
print("\n--- Hessian/coupling structure ---")
H = sp.Matrix(8, 8, lambda i, j: sp.simplify(sp.diff(L2, met[i], met[j])/2))
C = sp.Matrix(8, 5, lambda i, j: sp.simplify(sp.diff(sp.diff(L2, met[i]),
                                                     jets[j])))
odd = [2, 6, 7]; even = [0, 1, 3, 4, 5]
check("V1-A3a parity selection: odd x even Hessian block = 0",
      all(H[i, j] == 0 for i in odd for j in even))
check("V1-A3b odd sector couples ONLY through dpv (zero coupling to "
      "dp,dpT,dpr,dpth)",
      all(C[i, j] == 0 for i in odd for j in range(4)))
check("V1-A4rob q,w,k rows: zero dpT coupling and zero (a,b) cross terms",
      all(sp.simplify(x) == 0 for x in
          [C[3, 1], C[4, 1], C[5, 1], H[3, 0], H[3, 1], H[4, 0], H[4, 1],
           H[5, 0], H[5, 1]]))
G0 = f0*p0r**2 + p0t**2/r**2
check("V1-A6p p fully decoupled: all C[p,jets]=0 and H[p,u]=H[p,v]=0; "
      "alpha_pp = -(c/4) G0 / sin",
      all(sp.simplify(C[2, j]) == 0 for j in range(5)) and
      sp.simplify(H[2, 6]) == 0 and sp.simplify(H[2, 7]) == 0 and
      sp.simplify(H[2, 2] + (c/4)*G0/st) == 0)

# axial block det + signature
Hax = sp.Matrix(3, 3, lambda i, j: H[[2, 6, 7][i], [2, 6, 7][j]])
detax = sp.factor(Hax.det())
print(f"  axial block H(p,u,v) = {sp.factor(Hax)}")
print(f"  det H_axial = {detax}")
detax_claim = sp.factor(detax - c**3*(f0*p0r**2*r**2 + p0t**2)**3/(64*r**8*st**3))
check("V1-A3det det H_axial = c^3 (f0 p0r^2 r^2 + p0t^2)^3 / (64 r^8 sin^3) "
      "> 0 (claimed closed form)", sp.simplify(detax_claim) == 0,
      f"residual={detax_claim}")
# signature: eigen-sign via leading principal minors on a numeric point
num = {c: 1, r: sp.Rational(7, 5), st: sp.Rational(4, 5), phi0: sp.Rational(1, 3),
       p0r: sp.Rational(2, 3), p0t: sp.Rational(1, 4)}
m1 = Hax[0, 0].subs(num)
m2 = (Hax[:2, :2].det()).subs(num)
m3 = detax.subs(num)
print(f"  principal minors at test point: {sp.N(m1)}, {sp.N(m2)}, {sp.N(m3)}")
check("V1-A3sad axial block is a SADDLE (mixed signature), det > 0 at "
      "generic point", m1 < 0 and m3 > 0)

# ================= joint elimination (formed, audit scheme) ============
print("\n--- joint elimination of (a,b,q,w,u,v); p decoupled, k frozen ---")
elim = [a, b, q, w, u, v]
eqs = [sp.diff(L2, s) for s in elim]
sol = sp.solve(eqs, elim, dict=True)
assert len(sol) == 1
sol = sol[0]
L2corr = sp.expand(sp.together(L2.subs(sol)))
L2corr = sp.expand(sp.powsimp(sp.cancel(L2corr)))
for s in (p, k):
    L2corr = L2corr.subs(s, 0)
L2dp = L2
for s in met:
    L2dp = L2dp.subs(s, 0)
L2dp = sp.expand(L2dp)
print(f"  in-scheme (diagonal-class) density L2dp =\n    {L2dp}")

# W_A on ARBITRARY formed background
WA = sp.simplify(sp.diff(L2corr, dpT, 2)/2)
check("V1-A4 W_A robust: corrected dpT^2 coefficient = -(c/2) r^2 sin "
      "EXACTLY on arbitrary formed background",
      sp.simplify(WA + (c/2)*r**2*st) == 0, f"W = {WA}")

# spherical limit
L2c_sph = sp.expand(sp.simplify(L2corr.subs(p0t, 0)))
target = sp.expand(-(c/2)*st*(r**2*dpT**2
                              + f0**2*r**2*(dpr**2 - 8*p0r*dp*dpr
                                            + 8*p0r**2*dp**2)
                              - f0*dpth**2 - f0*dpv**2/st**2))
check("V1-A2a SPHERICAL corrected density equals the claimed flipped form "
      "(time + BOTH angular gradients flipped, radial sector unchanged)",
      sp.simplify(L2c_sph - target) == 0,
      f"residual = {sp.simplify(L2c_sph - target)}")
# and the in-scheme spherical density, to certify what 'flip' is relative to
L2dp_sph = sp.expand(L2dp.subs(p0t, 0))
diag_target = sp.expand(-(c/2)*st*(-r**2*dpT**2
                                   + f0**2*r**2*(dpr**2 - 8*p0r*dp*dpr
                                                 + 8*p0r**2*dp**2)
                                   + f0*dpth**2 + f0*dpv**2/st**2))
check("V1-A2a' in-scheme spherical density = same form with +dpT^2,"
      " +f0 dpth^2, +f0 dpv^2/sin^2 (so the flip claim is exactly: three "
      "signs flip, radial block identical)",
      sp.simplify(L2dp_sph - diag_target) == 0)

# dpv ratio on arbitrary formed background
ratio_v = sp.simplify(sp.diff(L2corr, dpv, 2)/sp.diff(L2dp, dpv, 2))
check("V1-A2c dpv^2 corrected/in-scheme = -1 on ARBITRARY formed "
      "background (background-uniform twin of W_A)",
      sp.simplify(ratio_v + 1) == 0, f"ratio = {ratio_v}")

# dpth ratio (formed) vs audit-B closed form
X, Y = sp.symbols('X Y', positive=True)
ratio_th = sp.simplify(sp.diff(L2corr, dpth, 2)/sp.diff(L2dp, dpth, 2))
rth_sub = sp.simplify(ratio_th.subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r)
                      .subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))
rth_claim = -(X - Y)*(X + 2*Y)/(X**2 + 7*X*Y - 2*Y**2)
check("V1-A2th dpth^2 flip ratio (formed) = -(X-Y)(X+2Y)/(X^2+7XY-2Y^2) "
      "in X = r^2 f^2 p0r^2, Y = f p0t^2 (audit-B map verified symbolically)",
      sp.simplify(rth_sub - rth_claim) == 0, f"got {sp.factor(rth_sub)}")

# cross term
crossrth = sp.simplify(sp.diff(sp.diff(L2corr, dpr), dpth))
print(f"  corrected dpr x dpth cross coefficient = {sp.factor(crossrth)}")
check("V1-A6x corrected operator has dpr x dpth cross term prop. to "
      "p0r*p0t: nonzero formed, zero spherical",
      sp.simplify(crossrth.subs(p0t, 0)) == 0 and sp.simplify(crossrth) != 0)

# degeneracy locus
Hqw = sp.Matrix([[H[5, 5], H[5, 4]], [H[4, 5], H[4, 4]]])
detqw = sp.factor(Hqw.det())
print(f"  det H_qw = {detqw}")
dq_sub = sp.simplify((detqw*(-8*r**2/(c**2*st**2))*sp.exp(10*phi0))
                     .subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r)
                     .subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))
check("V1-A2d det H_qw prop. to (X^2 + 7XY - 2Y^2): degeneracy quadratic "
      "verified", sp.simplify(dq_sub - (X**2 + 7*X*Y - 2*Y**2)*sp.exp(8*phi0)) == 0,
      f"poly = {sp.factor(dq_sub)}")
tt = sp.symbols('t', positive=True)
roots = sp.solve(sp.Eq(1 + 7*tt - 2*tt**2, 0), tt)
print(f"  roots of 1 + 7t - 2t^2 = 0 (t = Y/X): {roots}")
check("V1-A2d' positive root Y/X = (7+sqrt(57))/4",
      any(sp.simplify(rt - (7 + sp.sqrt(57))/4) == 0 for rt in roots))

# X4: decomposition of the dpv flip: even (a,b,q,w) vs odd (u,v)
sol_even = sp.solve([sp.diff(L2, s) for s in (a, b, q, w)], [a, b, q, w],
                    dict=True)[0]
L2_even = sp.expand(L2.subs(sol_even).subs(p, 0).subs(k, 0)
                    .subs(u, 0).subs(v, 0))
sol_odd = sp.solve([sp.diff(L2, s) for s in (u, v)], [u, v], dict=True)[0]
L2_odd = sp.expand(L2.subs(sol_odd).subs(p, 0).subs(k, 0)
                   .subs(a, 0).subs(b, 0).subs(q, 0).subs(w, 0))
ins_v = sp.diff(L2dp, dpv, 2)/2
ev_v = sp.simplify(sp.diff(L2_even, dpv, 2)/2 - ins_v)
od_v = sp.simplify(sp.diff(L2_odd, dpv, 2)/2 - ins_v)
print(f"  dpv^2: in-scheme = {sp.factor(ins_v)}, even-elim shift = "
      f"{sp.factor(ev_v)}, odd-elim shift = {sp.factor(od_v)}")
check("V1-X4 even+odd elimination shifts add to -2x in-scheme (total "
      "ratio -1); both sectors contribute",
      sp.simplify(ev_v + od_v + 2*ins_v) == 0,
      f"even/ins = {sp.simplify(ev_v/ins_v)}, odd/ins = {sp.simplify(od_v/ins_v)}")

# m=0 axial exclusion: setting dpv = 0, odd elimination gives exactly 0
check("V1-A3m0 axial sector eliminates to ZERO at m=0 (with dpv = 0 the "
      "solved u,v vanish and the odd contribution is exactly 0)",
      sp.simplify(sol_odd[u].subs(dpv, 0)) == 0 and
      sp.simplify(sol_odd[v].subs(dpv, 0)) == 0 and
      sp.simplify((L2_odd - L2dp).subs(dpv, 0)) == 0)

# ================= X2: the delta T^r_theta / T^r_vphi reading ==========
print("\n--- X2 physical reading of the q,u eliminations ---")
phif = phi0 + eps*dp
gfull = sp.Matrix([
    [-sp.exp(-2*phif), eps*a,           eps*b,  eps*p],
    [eps*a,            sp.exp(2*phif),  eps*q,  eps*u],
    [eps*b,            eps*q,           r**2*(1 + eps*(k + w))**2, eps*v],
    [eps*p,            eps*u,           eps*v,
     r**2*st**2*(1 + eps*(k - w))**2]])
gradf = sp.Matrix([eps*dpT, p0r + eps*dpr, p0t + eps*dpth, eps*dpv])
gif = gfull.adjugate()/gfull.det()
dphi2f = (gradf.T*gif*gradf)[0, 0]
Tdnf = c*sp.exp(-2*phif)*(gradf*gradf.T - gfull*dphi2f/2)
Tmix = gif*Tdnf   # T^mu_nu
dTrth = sp.simplify(sp.diff(Tmix[1, 2], eps).subs(eps, 0).subs(p0t, 0))
dTrv = sp.simplify(sp.diff(Tmix[1, 3], eps).subs(eps, 0).subs(p0t, 0))
ELq = sp.simplify(sp.diff(L2, q).subs(p0t, 0))
ELu = sp.simplify(sp.diff(L2, u).subs(p0t, 0))
rat_q = sp.simplify(ELq/dTrth)
rat_u = sp.simplify(ELu/dTrv)
print(f"  delta T^r_th (spherical bg) = {dTrth}")
print(f"  dL2/dq / delta T^r_th = {rat_q}")
print(f"  dL2/du / delta T^r_vphi = {rat_u}")
check("V1-X2 q-elimination IS delta T^r_theta = 0 and u-elimination IS "
      "delta T^r_vphi = 0 (field-independent proportionality, spherical)",
      not any(sp.simplify(sp.diff(rat_q, s)) != 0 for s in met + jets) and
      not any(sp.simplify(sp.diff(rat_u, s)) != 0 for s in met + jets))

# ================= X3: parameterization hostility =================
print("\n--- X3 exact-areal exponential scheme (rho = r at ALL orders) ---")
L0e, L1e, L2e = build_L('areal')
Te_w = sp.simplify(sp.diff(L1e, w))
check("V1-X3a first-order tadpole row identical in the exact-areal scheme "
      "(T_w unchanged)", sp.simplify(Te_w - T[w]) == 0)
He_ww = sp.simplify(sp.diff(L2e, w, 2)/2)
dHww = sp.simplify(He_ww - H[4, 4])
print(f"  alpha_ww(audit) = {sp.factor(H[4,4])}")
print(f"  alpha_ww(areal) = {sp.factor(He_ww)}")
print(f"  difference      = {sp.factor(dHww)}")
# spherical: does w decouple entirely (couplings + q-mixing)?
wdec_sph = (all(sp.simplify(C[4, j].subs(p0t, 0)) == 0 for j in range(5))
            and sp.simplify(H[4, 5].subs(p0t, 0)) == 0)
check("V1-X3b SPHERICALLY w decouples from all jets and from q "
      "(C[w,*]|sph = 0, H[w,q]|sph = 0) -- if so the spherical flip "
      "cannot depend on the w-parameterization", wdec_sph)
# corrected operator in the exact-areal scheme
eqs_e = [sp.diff(L2e, s) for s in elim]
sol_e = sp.solve(eqs_e, elim, dict=True)[0]
L2corr_e = sp.expand(sp.powsimp(sp.cancel(sp.together(L2e.subs(sol_e)))))
for s in (p, k):
    L2corr_e = L2corr_e.subs(s, 0)
L2ce_sph = sp.expand(sp.simplify(L2corr_e.subs(p0t, 0)))
check("V1-X3c SPHERICAL corrected density IDENTICAL in the exact-areal "
      "scheme (the flip is parameterization-safe on spherical backgrounds)",
      sp.simplify(L2ce_sph - L2c_sph) == 0,
      f"diff = {sp.simplify(L2ce_sph - L2c_sph)}")
ratio_v_e = sp.simplify(sp.diff(L2corr_e, dpv, 2)/sp.diff(L2dp, dpv, 2))
ratio_th_e = sp.simplify(sp.diff(L2corr_e, dpth, 2)/sp.diff(L2dp, dpth, 2))
dth = sp.simplify(ratio_th_e - ratio_th)
print(f"  formed dpv ratio (areal scheme)  = {ratio_v_e}")
print(f"  formed dpth ratio difference (areal - audit) = {sp.factor(dth)}")
check("V1-X3d FORMED-background corrected maps: dpv ratio still -1 in the "
      "areal scheme?", sp.simplify(ratio_v_e + 1) == 0,
      f"ratio = {ratio_v_e}")
check("V1-X3e FORMED dpth flip map is scheme-INDEPENDENT?",
      sp.simplify(dth) == 0,
      "(FAIL here = the formed-background flip maps are parameterization-"
      "dependent, confirming the off-shell caveat is structural)")

n = sum(1 for _, ok in PASS if ok)
print(f"\nV1 TOTAL: {n}/{len(PASS)} PASS   ({time.time()-t0:.1f}s)")
for nm, ok in PASS:
    if not ok:
        print("  FAIL:", nm)
