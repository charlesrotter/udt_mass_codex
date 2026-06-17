"""
BLIND ADVERSARIAL RE-DERIVATION of the W2 effective-potential claim.

I do NOT read or reuse VERIF_ceff_potential*.py. Everything below is
re-derived from the operator stated in w2_uncovering_results.md lines 29-31:

   bulk quadratic density  L = [2 r^2 sin(theta)/(1+w)^2] * (w_T^2 / f - f w_r^2)
   f = e^{-2 phi},  characteristic speed dr/dT = +- f,  frozen w = 0.

CLAIM TO ATTACK:
  (a) Liouville-normal potential  V(r) = -2 phi' f^2 / r   in tortoise coord
      dr* = dr/f, psi = u*sqrt(P), P = 2 r^2/(1+w)^2 with w=0.
  (b) Regularity BC => Dirichlet at r=0 => NO intrinsic bound state, only box.

PART 1: symbolic SL reduction + Liouville-normal V.
"""
import sympy as sp

r, T, w = sp.symbols('r T w', positive=True)
phi = sp.Function('phi')
f = sp.exp(-2*phi(r))           # f = e^{-2 phi(r)}

# ---- Frozen w = 0.  Density (drop sin(theta), angular integration is a constant)
# L = P * (w_T^2 / f - f w_r^2),  P = 2 r^2 / (1+w)^2  -> at w=0:  P = 2 r^2
P = 2*r**2                      # frozen w=0
print("P(r) =", P)
print("f(r) =", f)

# Euler-Lagrange for the field w(r,T) from L = P*(w_T^2/f) - P*f*w_r^2 :
#   d/dT( 2 P w_T / f )  -  d/dr( -2 P f w_r ) = 0
#   (P/f) w_TT  -  d/dr( P f w_r ) = 0           (P,f time-independent)
# Separate w = u(r) e^{i omega T}:  -omega^2 (P/f) u - (P f u')' = 0
#   =>  (P f u')' + omega^2 (P/f) u = 0      <-- Sturm-Liouville form
# SL:  p = P f,  weight rho = P/f,  q_pot = 0.
p_SL = P*f
rho_SL = P/f
print("\nSL operator (p u')' + omega^2 rho u = 0  with")
print("  p   =", sp.simplify(p_SL))
print("  rho =", sp.simplify(rho_SL))

# ---- Tortoise coordinate  dr* = dr/f  (so d/dr = (1/f) d/dr*) and
# Liouville substitution to remove first-derivative term.
# Standard Liouville-normal: for  (p u')' + omega^2 rho u = 0,
# go to variable x with dx = sqrt(rho/p) dr  and psi = (p*rho)^(1/4) u.
# Here sqrt(rho/p) = sqrt( (P/f)/(P f) ) = sqrt(1/f^2) = 1/f  -> dx = dr/f = dr*.
# Good: the tortoise coord IS the Liouville coordinate. x == r*.
# Then  -psi_xx + V psi = omega^2 psi  with
#   V = (1/W) d^2W/dx^2 ,  W = (p*rho)^(1/4)  ... let's derive carefully.

# Liouville transform result (well-known): with y = (p rho)^(1/4),
#   V(x) = y_xx / y   where x is the Liouville variable, derivatives wrt x.
x = sp.symbols('x')   # x = r*  (tortoise)
# p*rho = (P f)(P/f) = P^2.  So (p rho)^(1/4) = sqrt(P) = sqrt(2) r.
pr = sp.simplify(p_SL*rho_SL)
print("\n p*rho =", pr, "  => (p rho)^(1/4) = sqrt(P) =", sp.sqrt(P))
Wfun = sp.sqrt(P)     # = sqrt(2) r   ;  psi = Wfun * u = sqrt(P) u   (matches claim psi=u sqrt(P))

# Need d/dx = f d/dr.  Compute V = (1/W) d2W/dx2 with d/dx = f d/dr.
def d_dx(expr):
    return f*sp.diff(expr, r)
W = Wfun
Vx = sp.simplify( d_dx(d_dx(W)) / W )
print("\n Liouville-normal potential  V(r) = (1/W) d2W/dx2  with d/dx=f d/dr:")
Vx = sp.simplify(Vx)
print("   V =", Vx)

# Express in terms of phi' :  f = e^{-2phi}, f' = -2 phi' f.
phip = sp.symbols("phip")   # phi'(r)
Vsub = Vx.rewrite(sp.exp)
# substitute derivative of phi
Vsub = Vx.subs(sp.Derivative(phi(r), r), phip)
Vsub = sp.simplify(Vsub)
print("   V (phi' = phip) =", Vsub)

# Claimed:  V = -2 phi' f^2 / r
Vclaim = -2*phip*f**2/r
print("\n Claimed V = -2 phi' f^2 / r =", sp.simplify(Vclaim.subs(phi(r), phi(r))))
diff = sp.simplify(Vsub - Vclaim)
print(" V_derived - V_claim =", diff)
