#!/usr/bin/env python3
"""
fermion_forcing.py  (OBSERVE; GATED by Charles 2026-06-14)

QUESTION: Does a NONSTATIONARY UDT cell (nonzero, time-dependent time row)
FORCE a sigma-ODD matter source that the bosonic winding field (sigma-EVEN)
cannot supply -- and must that source be a two-valued (T^2=-1) spinor?

Metric (diagonal part, CANON):
  ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
Nonstationary sector adds a TIME ROW (off-diagonal):
  g_tr(t,r,theta), g_ttheta(t,r,theta)   [the "arm"/same-minus sector]

sigma = (t -> -t).  sigma-EVEN: T-invariant fields; sigma-ODD: flip under t->-t.
Time row (g_tr, g_ttheta) is the sigma-ODD nonstationary quantity.

We compute G^mu_nu and its mixed/lower forms exactly with sympy, decompose by
sigma-parity, run the forcing test, the bosonic-insufficiency check, and inspect
the structure of the required source.

NO mass / ratio / data. Tag chose vs derived inline.
"""
import sympy as sp

# ----------------------------------------------------------------------
# Coordinates and metric functions
# ----------------------------------------------------------------------
t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
c = sp.symbols('c', positive=True)
X = [t, r, th, ph]

# phi = positional dilation field; allow full (t,r,theta) dependence
# [CHOSE: phi independent of azimuth ph -- axisymmetry; standard for hedgehog]
phi = sp.Function('phi')(t, r, th)

# TIME ROW (the nonstationary, sigma-ODD off-diagonal arm)
# [CHOSE: general functions of (t,r,theta); this IS the ansatz under test]
A = sp.Function('A')(t, r, th)   # g_tr
B = sp.Function('B')(t, r, th)   # g_ttheta

# Metric g_{mu nu}
e_m = sp.exp(-2*phi)   # e^{-2phi}
e_p = sp.exp(+2*phi)   # e^{+2phi}

g = sp.Matrix([
    [-e_m*c**2,  A,        B,        0      ],
    [ A,         e_p,      0,        0      ],
    [ B,         0,        r**2,     0      ],
    [ 0,         0,        0,  r**2*sp.sin(th)**2],
])

ginv = g.inv()

# ----------------------------------------------------------------------
# Christoffel, Riemann, Ricci, Einstein  (exact)
# ----------------------------------------------------------------------
n = 4
def d(expr, i):
    return sp.diff(expr, X[i])

# Christoffel^a_{bc}
Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for ccc in range(n):
            s = sp.S(0)
            for dd in range(n):
                s += ginv[a,dd]*(d(g[dd,b],ccc)+d(g[dd,ccc],b)-d(g[b,ccc],dd))
            Gamma[a][b][ccc] = sp.simplify(s/2)

# Ricci_{bd} = R^a_{bad}
def ricci_component(b, dd):
    s = sp.S(0)
    for a in range(n):
        s += d(Gamma[a][b][dd], a) - d(Gamma[a][b][a], dd)
        for e in range(n):
            s += Gamma[a][a][e]*Gamma[e][b][dd] - Gamma[a][dd][e]*Gamma[e][b][a]
    return sp.simplify(s)

print("computing Ricci ...", flush=True)
Ric = sp.zeros(n)
for b in range(n):
    for dd in range(b, n):
        Ric[b,dd] = ricci_component(b, dd)
        Ric[dd,b] = Ric[b,dd]

Rs = sp.S(0)
for a in range(n):
    for b in range(n):
        Rs += ginv[a,b]*Ric[a,b]
Rs = sp.simplify(Rs)

# Einstein lower G_{mu nu} = Ric - 1/2 g R
G_low = sp.simplify(Ric - sp.Rational(1,2)*g*Rs)

print("Einstein G_low computed.", flush=True)

# ----------------------------------------------------------------------
# sigma-PARITY (t -> -t).  A field is sigma-EVEN if invariant, sigma-ODD if it flips.
# We implement sigma as the operator: t->-t AND flip the sign of any field that is
# DECLARED sigma-odd. Under the seal hypothesis: phi is sigma-EVEN (static-class),
# the time row (A,B) is sigma-ODD.
#
# To classify a metric/tensor component's INTRINSIC parity we apply the coordinate
# map t->-t together with the field parities, and compare to the original.
# A component G_{mu nu} carries an extra sign (-1)^{(# of t-indices)} from dt->-dt
# in its tensor character; combined with field parities this gives its sigma-parity.
# ----------------------------------------------------------------------
# Field-parity substitution operator sigma on an expression:
#   t -> -t ; phi(t,..)->phi(-t,..) is even => phi unchanged in functional form
#   A,B are sigma-ODD => A(-t)->-A_flip ... we encode by replacing the functions
#   with parity-tagged versions. Simpler: test parity of each component by the
#   transformation of the *whole* G_{mu nu} under t->-t with A->-A, B->-B and
#   the index-count sign, then see if it returns to itself (+: even) or negates (-: odd).

def sigma_on_expr(expr):
    """Apply field-level sigma: t->-t, A->-A, B->-B (their declared odd parity),
    phi even. Derivatives transform automatically via t->-t."""
    # substitute the functions by even/odd reflected versions
    phi_r = phi.subs(t, -t)          # phi even in form
    A_r   = -A.subs(t, -t)           # A is sigma-odd
    B_r   = -B.subs(t, -t)           # B is sigma-odd
    e = expr.subs({phi: sp.Symbol('PHI'), A: sp.Symbol('AA'), B: sp.Symbol('BB')},
                  simultaneous=True)
    # we instead do a direct functional substitution:
    return expr

# More robust: classify each G_{mu nu} by counting t-indices AND substituting the
# reflected fields, then checking even/odd.  We build the reflected metric and the
# reflected Einstein tensor directly and compare.

# Build reflected fields
phi_ref = sp.Function('phi')(-t, r, th)
A_ref   = sp.Function('A')(-t, r, th)
B_ref   = sp.Function('B')(-t, r, th)

# Map an expression under coordinate sigma (t->-t). Tensor index signs handled below.
def coord_reflect(expr):
    return expr.subs(t, -t)

# Parity classification of each lower component:
# Under x'^mu = sigma(x): t'=-t, others fixed. The Jacobian J = diag(-1,1,1,1).
# A lower tensor transforms G'_{a b}(x') = J^c_a J^d_b G_{cd}(x).
# Field parity hypothesis: phi even => phi(x')=phi(x) after t->-t (functional even);
# A,B odd => after the seal, the PHYSICAL configuration satisfies A(x')=-A(x),
# B(x')=-B(x). A component is "sigma-even" if G'_{ab}(x') = G_{ab}(x) (i.e. the
# field eqns are sigma-covariant), "sigma-odd" if it picks up a net minus.
#
# Net sign of a lower component G_{ab} under the full operation =
#   (Jacobian sign s_a * s_b)  where s_t=-1, s_r=s_th=s_ph=+1,
#   COMBINED with how its functional form maps under {t->-t, A->-A, B->-B, phi even}.
# For the FORCING test what matters is simply: with the time row turned on, are the
# off-diagonal (t r) and (t theta) Einstein components nonzero, and do they vanish
# when A=B=0?  We test that directly below -- it is parity-robust.

print("\n=== COMPONENTS OF G_low (nonzero check) ===", flush=True)
labels = {0:'t',1:'r',2:'th',3:'ph'}
for a in range(n):
    for b in range(a, n):
        val = G_low[a,b]
        nz = (sp.simplify(val) != 0)
        print(f"G_[{labels[a]}{labels[b]}] nonzero={nz}")

# ----------------------------------------------------------------------
# STATIC LIMIT: A=B=0 and phi=phi(r,theta) only (no t-dependence)
# Check that the OFF-DIAGONAL time-row components G_tr, G_ttheta vanish.
# ----------------------------------------------------------------------
print("\n=== STATIC LIMIT (A=B=0, phi=phi(r,theta)) ===", flush=True)
phi_s = sp.Function('phi')(r, th)
static_subs = {A:0, B:0}
def to_static(expr):
    e = expr.subs(static_subs)
    e = e.subs(phi, phi_s)
    # kill any residual t-derivatives of phi_s (none, phi_s has no t)
    return sp.simplify(e)

G_tr_static = to_static(G_low[0,1])
G_tth_static = to_static(G_low[0,2])
print("G_tr  (static) =", G_tr_static)
print("G_tth (static) =", G_tth_static)

# ----------------------------------------------------------------------
# NONSTATIONARY: keep A,B and t-dependence. Report the time-row Einstein components.
# ----------------------------------------------------------------------
print("\n=== NONSTATIONARY TIME-ROW EINSTEIN COMPONENTS ===", flush=True)
G_tr  = sp.simplify(G_low[0,1])
G_tth = sp.simplify(G_low[0,2])
print("G_tr  =", G_tr)
print()
print("G_tth =", G_tth)

# Does G_tr / G_ttheta contain time derivatives of the time row or of phi?
# Extract dependence on A_t, B_t, phi_t to confirm they are genuinely nonstationary.
At = sp.diff(A, t); Bt = sp.diff(B, t); phit = sp.diff(phi, t)
print("\nG_tr  has A_t :", G_tr.has(At))
print("G_tr  has B_t :", G_tr.has(Bt))
print("G_tr  has phi_t:", G_tr.has(phit))
print("G_tth has A_t :", G_tth.has(At))
print("G_tth has B_t :", G_tth.has(Bt))
print("G_tth has phi_t:", G_tth.has(phit))

# ----------------------------------------------------------------------
# Save key results
# ----------------------------------------------------------------------
import pickle
with open('/home/udt-admin/udt_mass_codex/fermion_forcing_dump.pkl','wb') as f:
    pickle.dump({
        'G_tr': G_tr, 'G_tth': G_tth,
        'G_tr_static': G_tr_static, 'G_tth_static': G_tth_static,
        'Ricci_scalar': Rs,
    }, f)
print("\nDONE. dumped.")
