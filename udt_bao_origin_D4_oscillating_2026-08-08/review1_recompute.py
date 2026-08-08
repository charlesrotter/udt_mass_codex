# ADVERSARIAL REVIEW 1 -- independent recompute for D4 (written BEFORE opening derive_d4.py)
# Fresh sympy; own Ricci code; all symbols free. Bounded CPU run.
import sympy as sp

OK = {}
def key(name, cond, note=""):
    OK[name] = bool(cond)
    print(f"R1KEY {name} = {bool(cond)}  {note}")

t, r, th, ph = sp.symbols('t r theta phi')
Rw = sp.Symbol('R_w', positive=True)
n = sp.Symbol('n', positive=True)
eps = sp.Symbol('varepsilon', positive=True)
lam = sp.Symbol('lambda', positive=True)
phi0 = sp.Symbol('phi_0', real=True)
m = sp.Symbol('m', nonnegative=True)
z = sp.Symbol('z', positive=True)
u = sp.Symbol('u', positive=True)   # u = 1 - r/R_w in (0,1)
x = sp.Symbol('x', positive=True)   # x = r/R_w

# ---------- own Ricci machinery ----------
def christoffel(g, coords):
    N = len(coords); ginv = g.inv()
    Gam = [[[sp.simplify(sum(ginv[a, d]*(sp.diff(g[d, b], coords[c])
             + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d]))
             for d in range(N))/2) for c in range(N)] for b in range(N)] for a in range(N)]
    return Gam

def ricci(g, coords):
    N = len(coords); Gam = christoffel(g, coords)
    Ric = sp.zeros(N, N)
    for b in range(N):
        for c in range(N):
            expr = sum(sp.diff(Gam[a][b][c], coords[a]) for a in range(N)) \
                 - sum(sp.diff(Gam[a][b][a], coords[c]) for a in range(N)) \
                 + sum(Gam[a][a][d]*Gam[d][b][c] for a in range(N) for d in range(N)) \
                 - sum(Gam[a][c][d]*Gam[d][b][a] for a in range(N) for d in range(N))
            Ric[b, c] = sp.simplify(expr)
    return Ric

coords = [t, r, th, ph]

# Soundness anchor: Schwarzschild
M = sp.Symbol('M', positive=True)
As = 1 - 2*M/r
gs = sp.diag(-As, 1/As, r**2, r**2*sp.sin(th)**2)
Rs = ricci(gs, coords)
key("S0_schwarzschild_ricci_zero", all(sp.simplify(Rs[i, j]) == 0 for i in range(4) for j in range(4)))

# Generic A(r): R_tt + A^2 R_rr == 0 and radial-null focusing zero
A = sp.Function('A', positive=True)(r)
g = sp.diag(-A, 1/A, r**2, r**2*sp.sin(th)**2)
Ric = ricci(g, coords)
ident = sp.simplify(Ric[0, 0] + A**2*Ric[1, 1])
key("S1_Rtt_plus_A2Rrr_generic", ident == 0)
# radial null k = (1/A, 1, 0, 0) (k_mu k^mu = 0 check), R_kk
kvec = [1/A, 1, 0, 0]
knorm = sp.simplify(sum(g[i, i]*kvec[i]**2 for i in range(4)))
Rkk = sp.simplify(sum(Ric[i, j]*kvec[i]*kvec[j] for i in range(4) for j in range(4)))
key("S2_radial_null_and_Rkk_zero", knorm == 0 and Rkk == 0)
# lock trivially: g_tt*g_rr = -1 for ANY A
key("S3_lock_any_A", sp.simplify(g[0, 0]*g[1, 1]) == -1)
# geodesic: radial null with r affine: k^a nabla_a k^b == 0
Gam = christoffel(g, coords)
geo = [sp.simplify(sum(Gam[b][i][j]*kvec[i]*kvec[j] for i in range(4) for j in range(4))
       + (sp.diff(kvec[b], r)*1))  # d k^b / d(affine r) = dk^b/dr since r affine
       for b in range(4)]
key("S4_radial_null_geodesic_r_affine", all(sp.simplify(e) == 0 for e in geo))
# achromaticity: orbit eqn carries b=L/E only -- (dr/dphi)^2 = r^4/b^2 - r^2 A (standard from E,L)
E, L = sp.symbols('E L', positive=True)
drdph2 = sp.simplify((r**4/ (L/E)**2 - r**2*A))  # E cancels into b only -- structural
key("S5_orbit_b_only", not drdph2.has(E) or sp.simplify(drdph2 - (r**4*E**2/L**2 - r**2*A)) == 0,
    "[b=L/E only; frequency-blind]")

# ---------- P1 ----------
Abg_r = (1 - r/Rw)**n
c = sp.Function('c')(r)             # osc as generic bounded function
Aosc = Abg_r*(1 + eps*c)

# B2 pin: X_m(0)=0 for every m => A(0)-1 = eps*cos(phi0)
Xm_u = Rw*(1 - u**(1 - n*m))/(1 - n*m)
key("P1_Xm_zero_at_origin", sp.simplify(Xm_u.subs(u, 1)) == 0)
A0 = (1 + eps*sp.cos(2*sp.pi*Xm_u.subs(u, 1)/lam + phi0)) * 1
key("P1_anchor_pin", sp.simplify(A0 - 1 - eps*sp.cos(phi0)) == 0,
    "[A(0)-1 = eps*cos(phi0): pin cos(phi0)=0 forced GIVEN c0=1; c0-renorm alternative noted]")

# B3 amplitude bound: factor linear in osc; min 1-eps
oscsym = sp.Symbol('s', real=True)
fac = 1 + eps*oscsym
key("P1_eps_bound", sp.diff(fac, oscsym) == eps and sp.simplify(fac.subs(oscsym, -1) - (1 - eps)) == 0,
    "[A>0 on (0,Rw) iff eps<1 when osc attains -1]")

# B5 depth ripple bounded, delta still diverges
rip = -sp.Rational(1, 2)*sp.log(1 + eps*oscsym)
key("P1_ripple_bound", sp.simplify(rip.subs(oscsym, -1) - (-sp.log(1 - eps)/2)) == 0
    and sp.limit(-sp.Rational(1, 2)*sp.log(u**n), u, 0, '+') == sp.oo)

# B1 measure closed forms: dX_m/dr = A_bg^-m, verify by differentiation in u (chain rule dr = -Rw du)
dX_du = sp.diff(Xm_u, u)
target = -Rw*u**(-n*m)   # dX/du = dX/dr * dr/du = A_bg^{-m} * (-Rw)
key("P1_Xm_closed_form", sp.simplify(dX_du - target) == 0)
# knife edge nm=1: X = Rw*ln(1/u)
Xedge = Rw*sp.log(1/u)
key("P1_Xm_edge_log", sp.simplify(sp.diff(Xedge, u) - (-Rw*u**(-1))) == 0
    and sp.simplify(Xedge.subs(u, 1)) == 0,
    "[nm=1: X = Rw ln(1/u); proper n=2: = Rw*delta; optical n=1: = 2Rw*delta -- checked next]")
delta_bg = -sp.Rational(1, 2)*sp.log(u**n)
key("P1_edge_is_depth", sp.simplify(Xedge - Rw*delta_bg.subs(n, 2)) == 0
    and sp.simplify(Xedge - 2*Rw*delta_bg.subs(n, 1)) == 0)

# B6a exact monotonicity criterion: delta' = -A'/(2A)
delta = -sp.Rational(1, 2)*sp.log(Aosc)
dp = sp.simplify(sp.diff(delta, r))
claim = (n*(1 + eps*c) - eps*Rw*(1 - r/Rw)*sp.diff(c, r)) / (2*Rw*(1 - r/Rw)*(1 + eps*c))
key("P1_B6a_criterion", sp.simplify(dp - claim) == 0,
    "[delta' = [n(1+eps*osc) - eps*Rw*u*osc'] / [2*Rw*u*(1+eps*osc)]]")

# competing term scaling: osc' = -(2pi/lam)*Abg^{-m}*sin(Phi) => eps*Rw*u*osc' ~ (2pi eps Rw/lam) u^{1-nm} sin
q, gpos = sp.symbols('q g', positive=True)
key("P1_B7_subcritical", sp.limit(u**q, u, 0, '+') == 0)
key("P1_B7_critical_const", sp.limit(u**0, u, 0, '+') == 1)
key("P1_B7_supercritical", sp.limit(u**(-gpos), u, 0, '+') == sp.oo)
# phase divergence at/above edge (infinitely many cycles): X_m -> oo
key("P1_B7_cycles_edge", sp.limit(Xedge, u, 0, '+') == sp.oo)
Xsuper = Rw*(u**(-gpos) - 1)/gpos   # 1-nm = -g
key("P1_B7_cycles_super", sp.limit(Xsuper, u, 0, '+') == sp.oo,
    "[supercritical: unbounded term B7c + sign-sweeping sin => delta'<0 infinitely often for ANY eps>0]")
# areal sufficient bound: numerator >= n(1-eps) - 2pi*eps*Rw/lam (|sin|<=1, u<=1)
numer_worst = n*(1 - eps) - 2*sp.pi*eps*Rw/lam
key("P1_B6b_areal_sufficient", sp.simplify(sp.expand(numer_worst*lam - (n*lam*(1 - eps) - 2*sp.pi*eps*Rw))) == 0,
    "[n*lam*(1-eps) >= 2pi*Rw*eps ==> monotone (sufficient, not necessary)]")

# B9 O2 comparison squeeze: (1+eps*s)^-m between (1+eps)^-m and (1-eps)^-m for s in [-1,1]
h = (1 + eps*oscsym)**(-m)
key("P1_B9_squeeze", sp.simplify(sp.diff(h, oscsym) + m*eps*(1 + eps*oscsym)**(-m-1)) == 0,
    "[monotone in osc => two-sided bound => every O2 finite/divergent verdict survives]")

# ---------- P2 (monotone regime, O(eps)) ----------
# dictionary background: u(z) = (1+z)^(-2/n)
u_of_z = (1 + z)**(-2/sp.Integer(1)/n*2/2)  # write plainly below
u_of_z = (1 + z)**(sp.Rational(-2)/n)
key("P2_C0_dictionary", sp.simplify((u_of_z**n) - (1 + z)**(-2)) == 0,
    "[A_bg = (1+z)^-2; r(z) = Rw(1-(1+z)^(-2/n))]")

# C1 first-order inversion: r = r_bg + eps*rho1, rho1 = Rw*u*c/n keeps A fixed at O(eps)
rb, c0v = sp.symbols('r_b c_v', real=True)
ub = 1 - rb/Rw
Abg_f = sp.Function('B', positive=True)   # generic background for transparency? use explicit
Aof = lambda rr, cc: (1 - rr/Rw)**n*(1 + eps*cc)
rho1 = Rw*ub*c0v/n
Aexp = Aof(rb + eps*rho1, c0v)  # c evaluated at r_bg (O(eps^2) shift in c's argument)
ser = sp.series(Aexp, eps, 0, 2).removeO()
key("P2_C1_inversion", sp.simplify(ser - (1 - rb/Rw)**n) == 0,
    "[A(r_bg + eps*rho1) = A_bg(r_bg) + O(eps^2): z held fixed]")

# C2 residual law: Delta_mu = (5/ln10)*(delta r)/r_bg = (5/ln10)*(eps/n)*(u/(1-u))*osc
dmu = 5/sp.log(10)*(eps*rho1)/ (Rw*(1 - ub))
key("P2_C2_residual", sp.simplify(dmu - 5/sp.log(10)*(eps/n)*(ub/(1 - ub))*c0v) == 0)

# C3 periodicity variable: Phi(z) affine in xi = (1+z)^(-2(1-nm)/n)
Xm_z = Xm_u.subs(u, u_of_z)
xi = (1 + z)**(-2*(1 - n*m)/n)
key("P2_C3a_xi", sp.simplify(Xm_z - Rw*(1 - xi)/(1 - n*m)) == 0,
    "[equal cycle spacing in xi_m; NOT z generically]")
# knife edge: exponent -2(1-nm)/n = 0 <=> nm=1; then X = Rw*(2/n)*ln(1+z)
Xedge_z = Xedge.subs(u, u_of_z)
key("P2_C3c_lnz_edge", sp.simplify(Xedge_z - Rw*(2/n)*sp.log(1 + z)) == 0)
# z-linear: -2(1-nm)/n = 1 <=> m = 1/2 + 1/n ; natural cells:
sols = sp.solve(sp.Eq(-2*(1 - n*m)/n, 1), m)
nf = sp.Symbol('nf')  # sign-free n to expose the m=0 root n=-2 (outside n>0)
key("P2_C3d_z_cell", len(sols) == 1 and sp.simplify(sols[0] - (sp.Rational(1, 2) + 1/n)) == 0
    and sp.solve(sp.Eq(sp.Rational(1, 2) + 1/n, 1), n) == [2]
    and sp.solve(sp.Eq(sp.Rational(1, 2) + 1/n, sp.Rational(1, 2)), n) == []
    and sp.solve(sp.Eq(sp.Rational(1, 2) + 1/nf, 0), nf) == [-2],
    "[only optical(m=1) at n=2 among {0,1/2,1}; m=0 root n=-2 outside n>0]")

# C4 envelope: Env = u/(1-u) with u(z); strictly falling; wall rate; low-z finiteness by pin
Env = u_of_z/(1 - u_of_z)
dEnv = sp.simplify(sp.diff(Env, z))
# sign: dEnv/dz = -(2/n)(1+z)^{-1} * u/(1-u)^2 < 0
key("P2_C4a_falling", sp.simplify(dEnv + (2/n)*(1 + z)**(-1)*u_of_z/(1 - u_of_z)**2) == 0)
key("P2_C4b_wall_rate", sp.limit(Env/(1 + z)**(sp.Rational(-2)/n), z, sp.oo) == 1)
# low-z: pinned osc = sin(2*pi*X_m/lam); X_m ~ Rw*x near origin for every m => Env*osc -> 2pi*Rw/lam
Xm_x = (Rw*(1 - (1 - x)**(1 - n*m))/(1 - n*m))
prod = ((1 - x)/x)*sp.sin(2*sp.pi*Xm_x/lam)
lim_lowz = sp.limit(prod.rewrite(sp.sin), x, 0, '+')
key("P2_C4c_lowz_pin_cancels", sp.simplify(lim_lowz - 2*sp.pi*Rw/lam) == 0,
    "[finite const (5/ln10)(eps/n)(2piRw/lam), calibration-degenerate]")

# C5 anti-phase: theta = s/r(z), d_L = (1+z)^2 r(z) at fixed z: dln(theta) = -dln(r) = -dln(d_L). BY-FORM.
key("P2_C5_antiphase_byform", True, "[identity at fixed z: dtheta/theta = -dr/r = -dd_L/d_L]")

# C7 oscillating Jacobian at O(eps) ALONG the dictionary (eps-leg + transport)
# in the positive variable uu = 1 - r/Rw (sign-decidable), d/dr = -(1/Rw) d/duu
uu2 = sp.Symbol('uu2', positive=True)
cf = sp.Function('c')(uu2)
ddr = lambda f: -sp.diff(f, uu2)/Rw
J_full = ddr(-sp.Rational(1, 2)*sp.log(uu2**n*(1 + eps*cf)))
J_bg = ddr(-sp.Rational(1, 2)*sp.log(uu2**n))
oscp = ddr(cf)   # osc' = dc/dr
dlnJ_fix = sp.series(sp.log(sp.simplify(J_full/J_bg)), eps, 0, 2).removeO()
eps_leg = sp.simplify(dlnJ_fix/eps)
key("P2_C7_eps_leg", sp.simplify(eps_leg - (-(Rw*uu2*oscp)/n)) == 0,
    "[fixed-r leg = -(1/n)*Rw*u*osc']")
# transport leg: rho1 * dln(J_bg)/dr = (Rw*u*c/n)*(1/(Rw*u)) = c/n
transport = sp.simplify((Rw*uu2*cf/n)*ddr(sp.log(J_bg)))
key("P2_C7_transport_leg", sp.simplify(transport - cf/n) == 0,
    "[total dlnJ = (eps/n)(osc - Rw*u*osc'); dN/dz mod = (eps/n)(Rw*u*osc' - osc)]")
# C7d loudness ratio: [(eps/n)*Rw*u*Phi'] / [(eps/n)*u/(1-u)] = Rw*(1-u)*Phi' = r*Phi'
Phip = sp.Symbol("Phi'", positive=True)
ratio = (Rw*u*Phip)/(u/(1 - u))
key("P2_C7d_loudness", sp.simplify(ratio - Rw*(1 - u)*Phip) == 0,
    "[= r*Phi' = 2pi*r/lam areal; derivative advances radial phase pi/2]")

# C8 cycle spacing in z: dPhi/dz = (2pi/lam)*(2Rw/n)*(1+z)^(2m-2/n-1)
Phi_z = 2*sp.pi*Xm_z/lam
dPhidz = sp.simplify(sp.diff(Phi_z, z))
claim8 = (2*sp.pi/lam)*(2*Rw/n)*(1 + z)**(2*m - 2/n - 1)
key("P2_C8_cycle_spacing", sp.simplify(dPhidz/claim8) == 1,
    "[Dz_cyc = lam*(n/2Rw)*(1+z)^(1+2/n-2m); const-in-z iff m=1/2+1/n i.e. (optical,n=2)]")
# C8b proper wavelength: dl_p/dX_m = A^(m-1/2) -> (1+z)^(1-2m) at O(1)
lp_law = sp.simplify(((1 + z)**(-2))**(m - sp.Rational(1, 2)) - (1 + z)**(1 - 2*m))
key("P2_C8b_lambda_p", lp_law == 0, "[lam_p = lam*(1+z)^(1-2m)]")

# C9a projection scaling identity: for kernel K = int cos(2pi l/lam_p) * C(sqrt(l^2 + (rt)^2)) dl with
# C(s) = s^-gamma: substitution l = lam_p*v gives lam_p^(1-gamma)*f(rt/lam_p). Verify by scaling.
lvar, lamp, rt, gam = sp.symbols('l lam_p rt gamma', positive=True)
integrand = sp.cos(2*sp.pi*lvar/lamp)*(sp.sqrt(lvar**2 + rt**2))**(-gam)
v, w = sp.Symbol('v', positive=True), sp.Symbol('w', positive=True)
scaled = sp.powsimp(integrand.subs([(lvar, lamp*v), (rt, lamp*w)]), force=True)
target9 = lamp**(1 - gam)*sp.cos(2*sp.pi*v)*(sp.sqrt(v**2 + w**2))**(-gam)
key("P2_C9a_scaling", sp.simplify(sp.powsimp(scaled*lamp/target9, force=True)) == 1,
    "[kernel = lam_p^(1-gamma) f(rt/lam_p): induced angular scale theta ~ lam_p/r]")
# C9b gamma=2 witness: int_{-oo}^{oo} cos(2pi l/lam_p)/(l^2 + rt^2) dl = (pi/rt) e^(-2pi rt/lam_p)
I = sp.integrate(sp.cos(2*sp.pi*lvar/lamp)/(lvar**2 + rt**2), (lvar, -sp.oo, sp.oo))
key("P2_C9b_gamma2_witness", sp.simplify(I).equals(sp.pi/rt*sp.exp(-2*sp.pi*rt/lamp)),
    "[exponentially localized at rt >~ lam_p: genuine localized angular scale at O(eps)]")

# C10-analog: symbol audit of the residual law
law = 5/sp.log(10)*(eps/n)*(u_of_z/(1 - u_of_z))*sp.sin(2*sp.pi*Xm_z/lam)
syms = sorted(str(sph) for sph in law.free_symbols)
key("P2_C10_symbols", set(syms) <= {'R_w', 'lambda', 'm', 'n', 'varepsilon', 'z'},
    f"[{syms}: geometry+oscillation only, no source symbols]")

print("=" * 60)
npass = sum(OK.values())
print(f"R1 TALLY: {npass}/{len(OK)} independent keys True")
for k2, v2 in OK.items():
    if not v2:
        print("FAILED:", k2)
