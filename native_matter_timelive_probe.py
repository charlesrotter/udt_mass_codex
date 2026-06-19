#!/usr/bin/env python3
"""
native_matter_timelive_probe.py -- INDEPENDENT live-audit of the pivotal SCOPE
claim made by the parallel native_matter_step run: "the native L2+L4 hedgehog is
static (T_tr=0), so adding native matter does NOT supply a G_tr momentum source and
does NOT unfreeze time -> the time-live kernel is orthogonal here."

This is the BACKGROUND sanity-anchor track's value-add: do NOT inherit that scope
reduction; TEST it.  If T_tr is identically 0 for any time-dependent native config,
the parallel run's static/round reduction is justified (the native hedgehog cannot
host time-life, so re-running the static radial #56 solver is the right object).
If T_tr != 0 when Theta is allowed to depend on t, then freezing time WALLED OFF a
live DOF and the static read-off is a SLICE dressed as the whole.

Method: symbolic (sympy), exact.  The native field is the unit 3-vector with a
radial+time profile Theta(t,r) on the round metric ds^2=-e^{2a}dt^2+e^{2b}dr^2+
r^2 dOmega^2 (a,b functions of t,r in general).  Compute the FULL Hilbert stress
T_{mu nu} for L2 (and note L4 preserves the structure per CANON C-2026-06-14-1),
read off T_{tr}.  No solver, no dial, no data.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta varphi', real=True)
xi = sp.symbols('xi', positive=True)

# metric functions (general t,r dependence; we only need the structure of T_tr)
a = sp.Function('a')(t, r)
b = sp.Function('b')(t, r)

# unit-3-vector hedgehog with a TIME-DEPENDENT radial profile Theta(t,r):
#   n = (sinTheta sinth cosph, sinTheta sinth sinph, cosTheta)
Th = sp.Function('Theta')(t, r)
n1 = sp.sin(Th)*sp.sin(th)*sp.cos(ph)
n2 = sp.sin(Th)*sp.sin(th)*sp.sin(ph)
n3 = sp.cos(Th)
n = sp.Matrix([n1, n2, n3])

# coordinates and inverse metric (diagonal round)
coords = [t, r, th, ph]
g = sp.diag(-sp.exp(2*a), sp.exp(2*b), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()

# L2 = -(xi/2) g^{mn} d_m n . d_n n.  The Hilbert stress for a sigma-model
#   T_{mu nu} = xi [ d_mu n . d_nu n - (1/2) g_{mu nu} g^{ab} d_a n . d_b n ]
dn = [n.diff(c) for c in coords]   # dn[mu] is the 3-vector d_mu n

def dot(u, v):
    return (u.T * v)[0]

# kinetic scalar K = g^{ab} d_a n . d_b n
K = 0
for i in range(4):
    for j in range(4):
        K += ginv[i, j] * dot(dn[i], dn[j])
K = sp.simplify(K)

def T_lower(mu, nu):
    val = xi*(dot(dn[mu], dn[nu]) - sp.Rational(1, 2)*g[mu, nu]*K)
    return sp.simplify(val)

print("=" * 78)
print("INDEPENDENT PROBE: is T_tr identically 0 for a TIME-DEPENDENT native field?")
print("=" * 78)

# T_tr  (mu=t index 0, nu=r index 1)
Ttr = T_lower(0, 1)
print("\nT_{tr} (Theta=Theta(t,r), general a,b) =")
sp.pprint(Ttr)
print("\nsimplified:", sp.simplify(Ttr))

# The momentum-constraint source is G_tr = kap8 T_tr.  For comparison, the vacuum
# Birkhoff result was G_tr = 2 d_t phi / r.  What sources d_t phi != 0?
# Factor out the structure:
Ttr_s = sp.simplify(Ttr)
print("\nFactored:", sp.factor(Ttr_s))

# Now the STATIC slice: Theta=Theta(r) only (d_t Theta = 0)
Ttr_static = Ttr_s.subs(sp.Derivative(Th, t), 0)
Ttr_static = sp.simplify(Ttr_static)
print("\n--- STATIC slice (d_t Theta = 0): T_tr =", Ttr_static)

print("\n" + "=" * 78)
print("VERDICT LOGIC:")
print("  - If T_tr = 0 ONLY when d_t Theta = 0 (i.e. T_tr ~ d_t Theta * d_r Theta),")
print("    then a TIME-DEPENDENT native profile DOES source the momentum constraint")
print("    -> it CAN unfreeze time (escape Birkhoff) -> the parallel run's 'native")
print("    hedgehog is static, time-live orthogonal' is a SLICE: it froze d_t Theta.")
print("  - If T_tr = 0 IDENTICALLY (even for d_t Theta != 0), the native hedgehog")
print("    genuinely cannot source G_tr -> static reduction justified.")
print("=" * 78)
