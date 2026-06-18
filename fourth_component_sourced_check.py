#!/usr/bin/env python3
"""
fourth_component_sourced_check.py -- DECISIVE data-blind symbolic check:
is the FOURTH field component (the n_4=cosTheta of the S^3/SU(2) hedgehog)
genuinely SOURCED by the native UDT action, or an unsourced PASSENGER?

Driver: Claude (Opus 4.8, 1M).  2026-06-18.  DATA-BLIND (no mass/ratio/wall
number).  Uses the EXACT committed action forms (matter_ansatz_derive.py /
native_stabilizer_results.md / complete_metric_batched.py stress()), NOT a
memory reconstruction.

Action (committed):
  L2 = -(xi/2)    g^{mn} d_m n . d_n n
  L4 = -(kappa/4) g^{mp}g^{nq} S_mn.S_pq ,
       S_mn.S_pq = (d_m n.d_p n)(d_n n.d_q n) - (d_m n.d_q n)(d_n n.d_p n)
  n = unit vector into the target sphere (S^2 if 3-comp, S^3 if 4-comp).

Metric: ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2.

S^3 hedgehog (the catalog carrier under suspicion):
  n4 = ( sinTheta sinth cosps, sinTheta sinth sinps, sinTheta costh, cosTheta )
The 4th component is n_4 = cosTheta(r).  The S^2 texture is Theta == pi/2
(n_4 == 0), the equatorial unit-3-vector m-winding configuration.

TASK 1: derive the Theta(r) Euler-Lagrange ODE from L2+L4 on the metric.
TASK 2: substitute Theta == pi/2 (n_4 == 0) into the Theta-EL.  If it is
        satisfied identically -> n_4=0 is a consistent BULK solution ->
        4th component NOT forced by the EOM (PASSENGER candidate).
        If a nonzero source remains -> n_4 forced (SOURCED).
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
xi, kap, c = sp.symbols('xi kappa c', positive=True)
phi = sp.Function('phi')(r)
Th  = sp.Function('Theta')(r)
coords = [t, r, th, ps]

# UDT metric (exact, committed)
g  = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
gi = g.inv()
sqrtg = sp.sqrt(-g.det())          # = c * r^2 * sin th  (covariant 4-volume)

def dot(a, b): return (a.T*b)[0]

def derivs(n):
    d = len(n)
    return [sp.Matrix([sp.diff(n[k], cc) for k in range(d)]) for cc in coords]

def Lagrangian_density(n):
    """L2+L4 (Lagrange-identity Skyrme), any target dim, on the UDT metric."""
    dn = derivs(n)
    gg = [[dot(dn[m], dn[k]) for k in range(4)] for m in range(4)]
    L2 = -(xi/2)*sum(gi[m, m]*gg[m][m] for m in range(4))
    L4 = -(kap/4)*sum(gi[m, m]*gi[k, k]*(gg[m][m]*gg[k][k] - gg[m][k]*gg[k][m])
                      for m in range(4) for k in range(4))
    return sp.simplify(L2 + L4)

# ---- S^3 Skyrme hedgehog (the 4-vector catalog carrier) ----
n4 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ps),
                sp.sin(Th)*sp.sin(th)*sp.sin(ps),
                sp.sin(Th)*sp.cos(th),
                sp.cos(Th)])
print("|n4|^2 =", sp.simplify(dot(n4, n4)), "(unit S^3 check)")

L = Lagrangian_density(n4)
print("\nLagrangian density L(Theta,Theta') (x sqrt|g| stripped of sin th meas):")
Lr = sp.simplify(L)
# The action S = INT L sqrt(-g) d^4x ; effective radial Lagrangian density
# (drop the trivial angular integration; the EL in Theta(r) follows from the
#  full covariant action with measure sqrt(-g) = c r^2 sin th).
Leff = sp.simplify(L*sqrtg)
print("  L * sqrt(-g) =", sp.simplify(Leff))

# ---- Euler-Lagrange for Theta(r) from the covariant action ----
Thp = sp.diff(Th, r)
# Treat Leff as function of Th, Thp, r, th (angular vars enter only via meas).
# EL: d/dr( dLeff/dThp ) - dLeff/dTh = 0   (after the angular measure is a constant
# multiplier for the EL in r; we keep sin th explicit and divide it out).
Th_f = sp.Function('Theta')
# build symbol-level Lagrangian to differentiate wrt Th and Thp independently
T_, Tp_ = sp.symbols('T_ Tp_', real=True)
Leff_sym = Leff.subs({sp.Derivative(Th, r): Tp_, Th: T_})
dL_dTp = sp.diff(Leff_sym, Tp_)
dL_dT  = sp.diff(Leff_sym, T_)
# put functions back, take total d/dr
dL_dTp_f = dL_dTp.subs({T_: Th, Tp_: Thp})
dL_dT_f  = dL_dT.subs({T_: Th, Tp_: Thp})
EL = sp.simplify(sp.diff(dL_dTp_f, r) - dL_dT_f)
# divide out the common positive angular measure (c r^2 sin th era) where possible
EL = sp.simplify(EL)
print("\nTASK 1 -- Theta(r) Euler-Lagrange (=0):")
sp.pprint(EL)

# ---- TASK 2: substitute Theta == pi/2 (n_4 == 0) ----
print("\n" + "="*70)
print("TASK 2: substitute Theta == pi/2  (n_4 = cosTheta = 0, the S^2 texture)")
print("="*70)
# Theta(r) = pi/2 constant => Theta' = Theta'' = 0
subs_eq = {sp.diff(Th, r, 2): 0, sp.diff(Th, r): 0, Th: sp.pi/2}
EL_eq = sp.simplify(EL.subs(subs_eq))
print("  Theta-EL evaluated at Theta == pi/2 :", EL_eq)
if EL_eq == 0:
    print("  => Theta == pi/2 SATISFIES the bulk Theta-EL identically.")
    print("     n_4 == 0 is a CONSISTENT bulk solution.  The 4th component is")
    print("     NOT forced by the equation of motion (PASSENGER, in the bulk).")
else:
    print("  => Theta == pi/2 leaves a NONZERO source:", EL_eq)
    print("     The bulk EOM FORCES Theta away from pi/2 -> n_4 is SOURCED.")

# ---- also: is Theta==pi/2 a critical point of the energy?  dE/dTheta at pi/2 ----
# The static energy density is -T^t_t; here we directly use the EL source above,
# which is the variational derivative.  Confirm via the L2-only and L4-only parts.
print("\n[cross-check] split bulk EL source at Theta=pi/2 by L2 vs L4:")
def split_EL(coeff_kill):
    Lc = Lagrangian_density(n4)
    # zero out one coupling
    Lc = Lc.subs(coeff_kill)
    Le = sp.simplify(Lc*sqrtg)
    Le_s = Le.subs({sp.Derivative(Th, r): Tp_, Th: T_})
    a = sp.diff(Le_s, Tp_).subs({T_: Th, Tp_: Thp})
    b = sp.diff(Le_s, T_ ).subs({T_: Th, Tp_: Thp})
    e = sp.simplify(sp.diff(a, r) - b)
    return sp.simplify(e.subs(subs_eq))
print("  L2-only EL at Theta=pi/2 (kappa->0):", split_EL({kap: 0}))
print("  L4-only EL at Theta=pi/2 (xi->0)   :", split_EL({xi: 0}))
