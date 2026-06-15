#!/usr/bin/env python3
"""
winding_stress.py  (OBSERVE)

TASK 4: Does the sigma-EVEN winding field n (static hedgehog, unit 3-vector,
S^2 sigma model, the DERIVED B=1/A source) have any sigma-ODD (time-row)
stress components T_tr, T_ttheta?

Field: unit 3-vector n_a(x), |n|=1, target S^2.  Minimal 2-derivative sigma model
  L = -(Lambda/2) g^{mu nu} d_mu n_a d_nu n_a        [CHOSE: minimal L2, no Skyrme,
                                                       matches angular_lagrangian_results]
Stress tensor:
  T_{mu nu} = Lambda [ d_mu n_a d_nu n_a - (1/2) g_{mu nu} (d n)^2 ]

If n is STATIC (no t-dependence) and the metric time row is OFF for this check
(we ask whether the field ITSELF can carry time-row stress), then d_t n_a = 0
=> T_{tr} = Lambda d_t n . d_r n = 0, T_{ttheta} = Lambda d_t n . d_theta n = 0.

We confirm symbolically, then test: could a TIME-DEPENDENT (but sigma-EVEN) n
supply a time-row stress? sigma-EVEN means n(-t)=n(t) => d_t n is sigma-ODD =>
T_tr = d_t n . d_r n is a product (odd)x(even) = sigma-ODD in PARITY but its
value at the seal (fixed pt of sigma, t such that d_t n=0) vanishes. Examine.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
c = sp.symbols('c', positive=True)
X = [t, r, th, ph]
phi = sp.Function('phi')(r, th)   # static phi for this check
e_m = sp.exp(-2*phi); e_p = sp.exp(2*phi)

# diagonal metric (time row OFF here: we test the field's OWN stress structure)
g = sp.diag(-e_m*c**2, e_p, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()

# ---- CASE 1: STATIC hedgehog n = (sin Th cos Ph, sin Th sin Ph, cos Th), Th=Th(r,theta)
Th = sp.Function('Theta')(r, th)
Ph = ph
n = sp.Matrix([sp.sin(Th)*sp.cos(Ph), sp.sin(Th)*sp.sin(Ph), sp.cos(Th)])

Lam = sp.symbols('Lambda', positive=True)
def dn(mu):
    return sp.Matrix([sp.diff(n[a], X[mu]) for a in range(3)])

def dn_dot_dn(mu, nu):
    return sum(sp.diff(n[a], X[mu])*sp.diff(n[a], X[nu]) for a in range(3))

# (d n)^2 = g^{mu nu} dn_mu . dn_nu
dn2 = sp.S(0)
for mu in range(4):
    for nu in range(4):
        dn2 += ginv[mu,nu]*dn_dot_dn(mu,nu)
dn2 = sp.simplify(dn2)

def Tlow(mu,nu):
    return sp.simplify(Lam*(dn_dot_dn(mu,nu) - sp.Rational(1,2)*g[mu,nu]*dn2))

print("=== CASE 1: STATIC hedgehog, Theta=Theta(r,theta) ===")
print("T_tr   =", Tlow(0,1))
print("T_ttheta =", Tlow(0,2))
print("T_tt   =", Tlow(0,0))
print("T_rr   =", Tlow(1,1))

# ---- CASE 2: sigma-EVEN but TIME-DEPENDENT n: Theta=Theta(t,r,theta) with Theta EVEN in t
# A genuinely sigma-EVEN field has n(-t)=n(t). Take Theta = Th0(r,theta)+ tau(t,r,theta)
# with tau EVEN in t (e.g. function of t^2). Then d_t n is sigma-ODD.
Th2 = sp.Function('Theta')(t, r, th)
n2 = sp.Matrix([sp.sin(Th2)*sp.cos(Ph), sp.sin(Th2)*sp.sin(Ph), sp.cos(Th2)])
def dn2_dot(mu,nu):
    return sum(sp.diff(n2[a], X[mu])*sp.diff(n2[a], X[nu]) for a in range(3))
print("\n=== CASE 2: time-dependent Theta(t,r,theta) ===")
T_tr2 = sp.simplify(dn2_dot(0,1))   # = Theta_t * Theta_r (the (d_t n).(d_r n) part)
print("T_tr  ~ (d_t n).(d_r n) =", T_tr2)
print("   structure: proportional to Theta_t * Theta_r")
print("   Theta_t is sigma-ODD for n sigma-EVEN; Theta_r is sigma-EVEN")
print("   => product is sigma-ODD in PARITY, but VANISHES at the seal where Theta_t=0")
print("   (sigma-EVEN field has Theta_t(t=0 fixed surface)=0 by evenness).")
