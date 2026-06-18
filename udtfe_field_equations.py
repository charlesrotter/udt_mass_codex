"""
udtfe_field_equations.py — Crux derivation: UDT modified field equations.

Mode: careful DERIVE + honest determination. Category-A, DATA-BLIND.
Constructor: Claude Opus 4.8 (1M), 2026-06-18.

Purpose: carry the GR/Einstein structure through with
    c -> c(phi)  and  source rest-mass -> m(phi)
as POSITION-FIELDS, and determine HONESTLY whether the resulting field
equations are genuinely modified (UDT != GR) or reduce to GR.

All symbolic claims tagged in the prose are produced/checked here.
"""

import sympy as sp

print("="*70)
print("UDT FIELD EQUATIONS — symbolic derivation")
print("="*70)

# ---------------------------------------------------------------------------
# 0. Symbols
# ---------------------------------------------------------------------------
t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
phi = sp.Function('phi')(r)        # position-dilation scalar phi(r) (static slice)
phip = sp.diff(phi, r)
phipp = sp.diff(phi, r, 2)
c0 = sp.symbols('c0', positive=True)   # the constant calibration speed (units anchor)

# ---------------------------------------------------------------------------
# 1. PIN c(phi) and m(phi) FROM the metric + principle
# ---------------------------------------------------------------------------
print("\n[1] c(phi), m(phi) from metric form g_tt=-e^{-2phi}c^2, g_rr=e^{2phi}")

# The metric form (CANON C-2026-06-18-1). We keep c as a symbol c(phi) and ASK
# what it must be. Write the diagonal static spherical slice with a LOCAL light
# speed function cloc(phi) appearing in g_tt:
cloc = sp.Function('cloc')(r)  # local light speed as a function of position

# Two readings of g_tt:
#   reading C-2026-06-18-1 literal:  g_tt = -e^{-2phi} c^2   (c the SAME constant everywhere)
#   varying-c reading:               g_tt = -e^{-2phi} cloc(phi)^2

# LOCAL light speed from a metric: along a radial null ray ds^2=0:
#   g_tt dt^2 + g_rr dr^2 = 0  => (dr/dt)_coord = sqrt(-g_tt/g_rr)
# The LOCALLY MEASURED speed uses proper length / proper time:
#   v_local = (sqrt(g_rr) dr) / (sqrt(-g_tt)/c_unit dt)
# In ANY metric of the form g_tt=-N(r)^2, g_rr=L(r)^2 the locally measured null
# speed is  L dr / (N dt / c)  with coord (dr/dt)=N/L  =>  v_local = c  identically.

A = sp.exp(-2*phi)          # so that g_tt = -A * cspeed^2  (A=e^{-2phi})
B = sp.exp(2*phi)           # g_rr = e^{2phi}
print("  A = -g_tt/c^2 =", A, "   B = g_rr =", B, "   A*B =", sp.simplify(A*B))

# Coordinate null speed with CONSTANT c (literal C-2026-06-18-1):
g_tt_const = -A*c0**2
g_rr = B
coord_null_speed = sp.sqrt(-g_tt_const/g_rr)
print("  coord null speed (const c):  dr/dt =", sp.simplify(coord_null_speed))
# Locally measured speed = (proper length / proper time):
#   proper length dl = sqrt(g_rr) dr ; proper time dtau = sqrt(-g_tt) dt / c0
v_local_const = sp.simplify( sp.sqrt(g_rr)*coord_null_speed / (sp.sqrt(-g_tt_const)/c0) )
print("  locally measured null speed (const c):  v_local =", v_local_const, " (== c0 => GR-trivial)")

# ---------------------------------------------------------------------------
# 2. THE DEEP DETERMINATION: physical vs absorbable
# ---------------------------------------------------------------------------
print("\n[2] PHYSICAL-vs-ABSORBABLE determination")

# Now make c a GENUINE position field cloc=cloc(phi) appearing in g_tt, and ALSO
# let it appear in the matter sector via m(phi). Question: is there a coordinate
# + units rescaling that removes all phi-dependence of cloc?

# General lapse N(r), radial L(r). Locally measured null speed is ALWAYS
# v_local = N L^{-1} * (L / (N/c_unit)) ... let's compute fully generally:
N = sp.Function('N')(r)   # sqrt(-g_tt) (has units of c_unit)
L = sp.Function('L')(r)   # sqrt(g_rr)
c_unit = sp.symbols('c_unit', positive=True)
coord = N/L                                   # (dr/dt) coordinate null speed
dl = L                                        # proper length per dr
dtau_per_dt = N/c_unit                        # proper time per dt
v_local_general = sp.simplify( dl*coord / dtau_per_dt )
print("  v_local for ARBITRARY N(r),L(r):  v_local =", v_local_general,
      " (== c_unit identically -- metric form alone CANNOT make physical c vary)")

# KEY LEMMA (printed): for ANY diagonal metric, the locally measured light speed
# is the unit constant c_unit, regardless of N,L. So a varying PHYSICAL c cannot
# come from the metric components alone -- it must come from the MATTER COUPLING
# (how rods/clocks/masses are built), i.e. from m(phi). This is the pivot.

# ---------------------------------------------------------------------------
# 3. The genuinely-new ingredient: m(phi). Build the dimensionless ratio.
# ---------------------------------------------------------------------------
print("\n[3] m(phi): the new SOURCE effect (GR has invariant rest mass)")

# Principle P1: m = m(phi). The ONLY phi-built scalar with the same exponential
# composition law (R1+R2) as the clock rate is m(phi) = m0 e^{a phi}.
a = sp.symbols('a', real=True)
m_of_phi = sp.symbols('m0', positive=True)*sp.exp(a*phi)
print("  m(phi) = m0 e^{a phi}  (only composition-consistent form; a = exponent to pin)")

# The dimensionless, gauge-relevant quantity is the RATIO of the Compton length
# (a mass-built ruler) to the metric ruler. Compton length lambda_C = hbar/(m c).
# If c is constant: lambda_C ~ 1/m ~ e^{-a phi}. The metric proper ruler is
# e^{phi} dr. The ratio (matter ruler)/(metric ruler):
ratio_ruler = sp.exp(-a*phi) / sp.exp(phi)
print("  (matter Compton ruler)/(metric ruler) ~ e^{-(a+1)phi}")
print("  -> phi-INDEPENDENT (absorbable) IFF a = -1; PHYSICAL (non-absorbable) otherwise")

# ---------------------------------------------------------------------------
# 4. Einstein tensor of the locked form (reduction / vacuum check)
# ---------------------------------------------------------------------------
print("\n[4] Einstein tensor of locked diagonal form (vacuum reduction check)")

# Full metric: ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + R(r)^2 dОmega^2
# Use areal-like radius function R(r); take spherical areal r^2 first.
Rad = r  # areal radius (CHOICE -- tag in ledger)
g = sp.diag(-A*c0**2, B, Rad**2, Rad**2*sp.sin(th)**2)
ginv = g.inv()
coords = [t, r, th, ph]

def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                s = 0
                for d in range(n):
                    s += ginv[l, d]*(sp.diff(g[d, m], coords[k])
                                     + sp.diff(g[d, k], coords[m])
                                     - sp.diff(g[m, k], coords[d]))
                Gamma[l][m][k] = sp.simplify(s/2)
    return Gamma

Gamma = christoffel(g, ginv, coords)

def ricci(Gamma, coords):
    n = len(coords)
    Ric = sp.zeros(n, n)
    for m in range(n):
        for nn in range(n):
            s = 0
            for l in range(n):
                s += sp.diff(Gamma[l][m][nn], coords[l]) - sp.diff(Gamma[l][m][l], coords[nn])
                for k in range(n):
                    s += Gamma[l][l][k]*Gamma[k][m][nn] - Gamma[l][nn][k]*Gamma[k][m][l]
            Ric[m, nn] = sp.simplify(s)
    return Ric

Ric = ricci(Gamma, coords)
Rscal = sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(4)))
G = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        G[i, j] = sp.simplify(Ric[i, j] - sp.Rational(1, 2)*g[i, j]*Rscal)

# Mixed Einstein tensor G^mu_nu
Gmix = sp.simplify(ginv*G)
print("  G^t_t =", sp.simplify(Gmix[0, 0]))
print("  G^r_r =", sp.simplify(Gmix[1, 1]))
print("  G^th_th =", sp.simplify(Gmix[2, 2]))
print("  G^t_t - G^r_r =", sp.simplify(Gmix[0, 0] - Gmix[1, 1]),
      "  (==0 => B=1/A consequence, source-free)")

# Vacuum: set G^th_th = 0 and solve for phi(r) -> is it Schwarzschild?
print("\n  Vacuum eqn G^th_th = 0:")
vac = sp.simplify(Gmix[2, 2])
print("   ", vac, " = 0")

# ---------------------------------------------------------------------------
# 5. Now the MODIFICATION: let c be a field in g_tt AND in the coupling 8piG/c^4
#    and in the matter stress. Recompute G^t_t with g_tt=-e^{-2phi} cloc(phi)^2.
# ---------------------------------------------------------------------------
print("\n[5] Modified: g_tt = -e^{-2phi} cloc(phi)^2 with cloc varying")

cfun = sp.Function('cl')(r)  # cloc as fn of r (through phi)
g2 = sp.diag(-A*cfun**2, B, Rad**2, Rad**2*sp.sin(th)**2)
ginv2 = g2.inv()
Gamma2 = christoffel(g2, ginv2, coords)
Ric2 = ricci(Gamma2, coords)
Rscal2 = sp.simplify(sum(ginv2[i, i]*Ric2[i, i] for i in range(4)))
G2 = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        G2[i, j] = sp.simplify(Ric2[i, j] - sp.Rational(1, 2)*g2[i, j]*Rscal2)
Gmix2 = sp.simplify(ginv2*G2)
print("  G^t_t (varying c) =", sp.simplify(Gmix2[0, 0]))
print("  G^r_r (varying c) =", sp.simplify(Gmix2[1, 1]))
print("  G^t_t - G^r_r (varying c) =", sp.simplify(Gmix2[0, 0] - Gmix2[1, 1]))
print("  -> does an overall cloc(r) factor in g_tt change the mixed Einstein tensor?")

print("\nDONE.")
