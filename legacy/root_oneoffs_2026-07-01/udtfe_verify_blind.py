"""
udtfe_verify_blind.py — BLIND ADVERSARIAL VERIFIER (independent re-derivation).

I do NOT trust the constructor. I re-derive every claim from scratch with sympy.
Axes A-E per the prosecution brief. DATA-BLIND: no mass/ratio numbers.

Nothing committed is changed by this script.
"""
import sympy as sp

def banner(s):
    print("\n" + "="*72)
    print(s)
    print("="*72)

t, r, th, ph = sp.symbols('t r theta varphi', real=True)
c0 = sp.symbols('c0', positive=True)

# generic potential phi(r)
phi = sp.Function('phi')(r)

# ===========================================================================
banner("AXIS A — v_local for general diagonal metric; then off-diagonal shift")
# ===========================================================================
# General static diagonal: g = diag(-N(r)^2, L(r)^2, ...)
# Local measured speed of light = (proper distance)/(proper time) along ds^2=0.
N = sp.Function('N')(r)
Lr = sp.Function('L')(r)

# Radial null: -N^2 dt^2 + L^2 dr^2 = 0  => (dr/dt) = N/L  (coordinate speed, in
# units where c-anchor = 1 for the metric's t having units of length OR explicit).
# Be fully explicit about units: let proper time = sqrt(N^2) dt / c0 only if N
# already carries c0. To avoid ambiguity, derive purely from ds^2 invariant.
# Proper length dl = L dr ; proper time c0*dtau = N dt  (so dtau = N dt / c0).
# v_local = dl/dtau = L dr / (N dt / c0) = c0 * (L/N) * (dr/dt) = c0*(L/N)*(N/L) = c0
coord_speed = N/Lr
dl = Lr
dtau = N/c0   # proper time (so that dl/dtau has units of c0 when dr/dt=coord_speed)
v_local = sp.simplify(dl*coord_speed/dtau)
print("  general diagonal: coordinate (dr/dt) =", coord_speed)
print("  general diagonal: v_local =", v_local, "  -> independent of N,L:",
      v_local == c0)

# Now the STRONGEST attack: add off-diagonal shift g_{tr}=s(r).
# Metric block (t,r):  [[-N^2, s],[s, L^2]]  (using N^2 absorbing c0 via N=c0*n later)
s = sp.Function('s')(r)
n_lapse = sp.symbols('Nl', positive=True)  # placeholder, use functions below
# We work with the 2x2 block and a true null condition. Light cone: g_ab dx^a dx^b=0.
# -N^2 dt^2 + 2 s dt dr + L^2 dr^2 = 0  (signature handling: g_tt=-N^2, g_tr=s, g_rr=L^2)
N2, S, L2 = sp.symbols('Nsq Ssh Lsq', positive=False)  # treat as numbers per point
dtv, drv = sp.symbols('dt dr', real=True)
# Solve the null quadratic for (dr/dt):
g_tt, g_tr, g_rr = -N**2, s, Lr**2
# -N^2 dt^2 + 2 g_tr dt dr + L^2 dr^2 = 0
x = sp.symbols('x', real=True)  # x = dr/dt
null_quad = g_tt + 2*g_tr*x + g_rr*x**2
roots = sp.solve(sp.Eq(null_quad, 0), x)
print("\n  Off-diagonal g_tr=s: coordinate dr/dt roots (out/in-going):")
for rt in roots:
    print("    ", sp.simplify(rt))

# Local measured speed with a shift: the physically meaningful test is whether the
# TWO-WAY (round-trip averaged) local speed differs from c0, OR whether the
# proper-frame light speed is anisotropic. Build the local orthonormal frame.
# A static observer has 4-velocity u^a along dt only: u = (u^t,0,0,0),
# normalized g_ab u^a u^b = -c0^2  => -N^2 (u^t)^2 = -c0^2 => u^t = c0/N.
# Measured speed of a photon by this observer:
#   v = (spatial proper distance)/(proper time), using the projector h_ab = g_ab + u_a u_b/c0^2
# This is the standard ADM/threading result. Compute via the 1+3 split.
# Spatial metric (threading): gamma_ij = g_ij - g_ti g_tj / g_tt
# Here only r: gamma_rr = g_rr - g_tr^2/g_tt = L^2 - s^2/(-N^2) = L^2 + s^2/N^2
gamma_rr = sp.simplify(g_rr - g_tr**2/g_tt)
print("\n  threading spatial metric gamma_rr =", gamma_rr)
# proper time of static observer: dtau = sqrt(-g_tt)/c0 dt = N/c0 dt
# For a photon, the measured speed (each direction) using the threading lapse/shift:
# Standard result: locally measured one-way speed depends on shift (anisotropy),
# but the proper-frame measured speed using gamma and proper time is c0.
# Verify: the photon's measured speed = sqrt(gamma_rr) |dr_phys/dtau_phot|...
# Cleanest invariant: contract photon momentum with observer.
# Photon 4-momentum k^a null: g_ab k^a k^b = 0. Energy measured E = -g_ab u^a k^b.
# Measured 3-momentum magnitude p: E^2/c0^2 - p^2 = m^2 c0^2 = 0 => p = E/c0.
# Speed v = p c0^2 / E = c0 ALWAYS for a null k, REGARDLESS of shift, because the
# photon is null in the FULL metric. Demonstrate symbolically:
ut = c0/N  # u^t (static observer), u^r=0
# need u_a = g_ab u^b
u_up = sp.Matrix([ut, 0])
gblock = sp.Matrix([[g_tt, g_tr],[g_tr, g_rr]])
u_low = gblock*u_up
# null photon k^a = (kt, kr) with g_ab k^a k^b = 0
kt, kr = sp.symbols('kt kr', real=True)
k_up = sp.Matrix([kt, kr])
null_cond = (k_up.T*gblock*k_up)[0]
# Energy measured: E = -(1/c0) u_a k^a  (factor to get energy units), magnitude of
# the speed: project. Use the cleanest statement: for ANY null k and timelike u,
# the measured speed |v| = c0. Show E^2/c0^2 = p^2 where p^2 = h_ab k^a k^b /(...).
E_meas = -(u_low.T*k_up)[0]   # = -u_a k^a
# spatial projector h_ab = g_ab + u_a u_b / c0^2
u_low_full = u_low
h = gblock + (u_low_full*u_low_full.T)/c0**2
p2 = (k_up.T*h*k_up)[0]   # = h_ab k^a k^b (>=0, spatial)
# Use null condition to eliminate: g_ab k^a k^b = 0 => substitute
# E^2 = (u_a k^a)^2 ; check E^2/c0^2 - p2 == (something)*nullcond
check = sp.simplify(E_meas**2/c0**2 - p2)
# substitute null condition value (=0) for g_ab k^a k^b
check_on_null = sp.simplify(check - 0)
# Express null_cond and reduce
diff_expr = sp.simplify(E_meas**2/c0**2 - p2 + null_cond/c0**2)
print("\n  E^2/c0^2 - p^2  (should be -(g_ab k^a k^b)/c0^2, =0 on shell):")
print("    E^2/c0^2 - p^2 =", sp.simplify(E_meas**2/c0**2 - p2))
print("    + null_cond/c0^2 =", sp.simplify(diff_expr), " (==0 => measured speed=c0 EVEN WITH SHIFT)")

# ===========================================================================
banner("AXIS B — coordinate (dr/dt)^2 vs committed c_r^2=e^{-4phi}; c_theta")
# ===========================================================================
A = sp.exp(-2*phi)          # -g_tt/c0^2
Bcomp = sp.exp(2*phi)       # g_rr
g_tt_udt = -A*c0**2
g_rr_udt = Bcomp
coord_dr_dt_sq = sp.simplify(-g_tt_udt/g_rr_udt)
print("  (dr/dt)_coord^2 =", coord_dr_dt_sq)
print("  committed c_r^2 = e^{-4phi} =", sp.exp(-4*phi))
print("  MATCH (up to c0^2):", sp.simplify(coord_dr_dt_sq - c0**2*sp.exp(-4*phi)) == 0)
# c_theta: transverse coordinate speed from g_tt and g_thth = r^2
g_thth = r**2
c_th_sq = sp.simplify(-g_tt_udt/g_thth)
print("  c_theta^2 = -g_tt/g_thth =", c_th_sq)
print("  committed c_theta^2 = e^{-2phi}/r^2 ; ratio to mine:",
      sp.simplify(c_th_sq/(sp.exp(-2*phi)/r**2)), " (=c0^2 => match)")

# ===========================================================================
banner("AXIS C — cl(r) in g_tt is pure reparametrization of phi (Kretschmann)")
# ===========================================================================
def curvature_invariants(gmat, coords):
    n = len(coords)
    ginv = gmat.inv()
    # Christoffel
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                ss = 0
                for d in range(n):
                    ss += ginv[l, d]*(sp.diff(gmat[d, m], coords[k])
                                      + sp.diff(gmat[d, k], coords[m])
                                      - sp.diff(gmat[m, k], coords[d]))
                Gam[l][m][k] = sp.simplify(ss/2)
    # Riemann R^a_{bcd}
    def Riem(a, b, c, d):
        term = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
        for e in range(n):
            term += Gam[a][c][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][c]
        return sp.simplify(term)
    # Ricci + scalar
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            ss = 0
            for a in range(n):
                ss += Riem(a, b, a, d)
            Ric[b, d] = sp.simplify(ss)
    Rsc = sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(n)))
    # Kretschmann K = R_{abcd} R^{abcd}
    # lower Riemann: R_{abcd} = g_ae R^e_bcd
    Rlow = {}
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    val = 0
                    for e in range(n):
                        val += gmat[a, e]*Riem(e, b, cc, d)
                    Rlow[(a, b, cc, d)] = sp.simplify(val)
    # raise all: R^{abcd}
    K = 0
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    rup = 0
                    # R^{abcd} = g^aa' g^bb' g^cc' g^dd' R_{a'b'c'd'}
                    # diagonal metric => only same-index terms
                    rup = ginv[a, a]*ginv[b, b]*ginv[cc, cc]*ginv[d, d]*Rlow[(a, b, cc, d)]
                    K += Rlow[(a, b, cc, d)]*rup
    K = sp.simplify(K)
    return Rsc, K

coords = [t, r, th, ph]
# Metric 1: g_tt = -e^{-2phi} c0^2
g1 = sp.diag(-A*c0**2, Bcomp, r**2, r**2*sp.sin(th)**2)
# Metric 2: g_tt = -e^{-2phi} cl(r)^2
cl = sp.Function('cl')(r)
g2 = sp.diag(-A*cl**2, Bcomp, r**2, r**2*sp.sin(th)**2)
# Metric 3: the claimed equivalent with phitilde = phi - ln(cl/c0):
# g_tt = -e^{-2 phitilde} c0^2 = -e^{-2phi} (cl/c0)^2 c0^2 = -e^{-2phi} cl^2  -> SAME as g2.
phit = phi - sp.log(cl/c0)
g3 = sp.diag(-sp.exp(-2*phit)*c0**2, Bcomp, r**2, r**2*sp.sin(th)**2)
print("  g2[tt] - g3[tt] (cl form vs phitilde form) =", sp.simplify(g2[0,0]-g3[0,0]),
      "  (==0 => algebraically identical g_tt)")
# NOTE: but g_rr in g3 should ALSO transform if phitilde replaces phi. The constructor's
# claim is g_tt only is reparametrized. CHECK: does g_rr=e^{2phi} stay, making B=1/A BREAK?
print("  CAUTION: if phi->phitilde everywhere, g_rr would become e^{2phitilde} != e^{2phi}.")
print("           The 'fold cl into phi' only touches g_tt, so B=1/A (g_tt g_rr=-c0^2)")
print("           is BROKEN once cl varies. Check g_tt*g_rr:")
print("    g1: g_tt*g_rr =", sp.simplify(g1[0,0]*g1[1,1]))
print("    g2: g_tt*g_rr =", sp.simplify(g2[0,0]*g2[1,1]), " (cl-dependent => NOT -c0^2)")

R1, K1 = curvature_invariants(g1, coords)
print("\n  Ricci scalar (const-c metric) R1 =", R1)
R2, K2 = curvature_invariants(g2, coords)
print("  Ricci scalar (cl metric)       R2 =", R2)
# Is R2 obtainable from R1 by phi -> phi - ln(cl/c0)?  Substitute and compare.
# Define f = phi - ln(cl/c0); R1 is a functional of phi and its derivs. Replace.
# Build R1 as function of a generic potential, then substitute the shifted one.
psi = sp.Function('psi')(r)
g1psi = sp.diag(-sp.exp(-2*psi)*c0**2, sp.exp(2*psi), r**2, r**2*sp.sin(th)**2)
R1psi, K1psi = curvature_invariants(g1psi, coords)
# substitute psi -> phi (the cl form does NOT shift g_rr, so this is the wrong test;
# we instead directly compare invariants between g2 and the genuine reparam g_full
# where BOTH components use phitilde):
gfull = sp.diag(-sp.exp(-2*phit)*c0**2, sp.exp(2*phit), r**2, r**2*sp.sin(th)**2)
Rfull, Kfull = curvature_invariants(gfull, coords)
print("\n  GENUINE reparam (phi->phitilde in BOTH g_tt and g_rr):")
print("    Ricci(gfull) - [Ricci(g1) with phi->phitilde] =",
      sp.simplify(Rfull - R1psi.subs(psi, phit).doit()))
print("    -> if 0, gfull is just g1 relabeled (true reparam).")
print("  Kretschmann: K(g2 cl-only) - K(gfull genuine) =", sp.simplify(K2 - Kfull))
print("    -> if NONZERO, cl-in-g_tt-only is NOT the same geometry as a phi shift.")

# ===========================================================================
banner("AXIS D — ruler ratio phi-independent iff a=-1; global rescaling cannot absorb")
# ===========================================================================
a = sp.symbols('a', real=True)
# Compton ruler ~ e^{-a phi}; metric ruler ~ e^{phi}; ratio:
ratio = sp.simplify(sp.exp(-a*phi)/sp.exp(phi))
print("  ruler ratio = e^{-(a+1)phi}:", ratio)
print("  d(ratio)/dphi = 0 for all phi  iff a=-1:")
dratio = sp.diff(ratio, phi)
print("    derivative =", sp.simplify(dratio), " ; =0 identically iff a=-1:",
      sp.simplify(dratio.subs(a, -1)) == 0)
# Global rescaling: multiply by constant K (units of hbar,G,charge). ratio -> K*ratio.
K = sp.symbols('K', positive=True)
print("  global const rescale K: K*ratio still has phi-dependence e^{-(a+1)phi}:",
      sp.simplify(sp.diff(K*ratio, phi)), " (K factors out, cannot kill phi-dep unless a=-1)")

# ===========================================================================
banner("AXIS E — vacuum: Einstein tensor, does 'a' enter? Schwarzschild?")
# ===========================================================================
# Compute mixed Einstein tensor of g1 (the locked const-c form) independently.
def einstein_mixed(gmat, coords):
    n = len(coords)
    ginv = gmat.inv()
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                ss = 0
                for d in range(n):
                    ss += ginv[l, d]*(sp.diff(gmat[d, m], coords[k])
                                      + sp.diff(gmat[d, k], coords[m])
                                      - sp.diff(gmat[m, k], coords[d]))
                Gam[l][m][k] = sp.simplify(ss/2)
    Ric = sp.zeros(n, n)
    for m in range(n):
        for nn in range(n):
            ss = 0
            for l in range(n):
                ss += sp.diff(Gam[l][m][nn], coords[l]) - sp.diff(Gam[l][m][l], coords[nn])
                for k in range(n):
                    ss += Gam[l][l][k]*Gam[k][m][nn] - Gam[l][nn][k]*Gam[k][m][l]
            Ric[m, nn] = sp.simplify(ss)
    Rsc = sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(n)))
    Gmix = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            Gmix[i, j] = sp.simplify(sum(ginv[i, k]*(Ric[k, j]
                          - sp.Rational(1, 2)*gmat[k, j]*Rsc) for k in range(n)))
    return Gmix

Gmix1 = einstein_mixed(g1, coords)
print("  G^t_t =", Gmix1[0, 0])
print("  G^r_r =", Gmix1[1, 1])
print("  G^th_th =", Gmix1[2, 2])
print("  G^t_t - G^r_r =", sp.simplify(Gmix1[0, 0] - Gmix1[1, 1]), " (==0 => B=1/A)")
print("  'a' (mass exponent) appears in vacuum Einstein tensor?  NO symbol 'a' present:",
      not Gmix1[0, 0].has(a))

# Vacuum solve: G^t_t = 0  => -2 r phi' - e^{2phi}+1 = 0 type. Solve ODE.
fr = sp.Function('f')  # let u = e^{2phi}? We instead solve G^t_t=0 for phi.
eq = sp.Eq(Gmix1[0, 0], 0)
print("\n  Vacuum G^t_t=0 equation:", sp.simplify(Gmix1[0, 0]), "= 0")
# Solve: introduce m(r)=... standard. Let y=e^{-2phi}=A (so g_rr=1/A). Schwarzschild
# has A_schw = 1-2GM/(c0^2 r). Check that A=1-K/r solves it.
Kc = sp.symbols('Ks', real=True)
phi_schw = -sp.Rational(1,2)*sp.log(1 - Kc/r)  # so e^{-2phi}=1-K/r
test = Gmix1[0, 0].subs(phi, phi_schw).doit()
print("  Substitute Schwarzschild phi (e^{-2phi}=1-K/r) into G^t_t:",
      sp.simplify(test), " (==0 => Schwarzschild solves vacuum)")
# also check G^th_th vanishes on it
test_th = Gmix1[2, 2].subs(phi, phi_schw).doit()
print("  Same into G^th_th:", sp.simplify(test_th), " (==0 => full vacuum solution)")

print("\nDONE — verifier complete.")
