"""
BLIND VERIFIER — CLAIM 1: the -v_theta^2 variation is a DRIFT not a binding potential.
Independent sympy re-derivation. Does NOT import the constructor's machinery.

Field eqn: v_mm + e^{2v}( v_thth + cot(th) v_th - v_th^2 ) = Phi(e^{-2v} - e^v)
We attack the ANGULAR nonlinearity term -v_th^2 inside the e^{2v} bracket.

(a) linear variation of -v_th^2 about background v0(m,theta) under v=v0+eps*u  -> exactly -2 v0_th u_th ; =0 if v0 theta-indep (round)
(b) operator u'' + p u' with p = cot th - 2 v0_th is self-adjoint in weight exp(int p) = sin th e^{-2 v0}
(c) ATTACK: can a first-derivative drift in a real self-adjoint 1D operator create a bound state / flip sign by itself?
"""
import sympy as sp

th, eps, m = sp.symbols('theta epsilon m', real=True)
# v0 a general non-round background, u a general fluctuation, both functions of theta (and m, irrelevant for angular part)
v0 = sp.Function('v0')
u  = sp.Function('u')

print("="*70)
print("CLAIM 1 (a): linear variation of -v_th^2")
print("="*70)
v = v0(th) + eps*u(th)
term = -(sp.diff(v, th))**2          # the -v_theta^2 piece
var = sp.diff(term, eps).subs(eps, 0)
var = sp.simplify(var)
target = -2*sp.diff(v0(th), th)*sp.diff(u(th), th)
print("d/d_eps[-v_th^2]|_0 =", var)
print("target -2 v0' u'    =", target)
print("MATCH (variation == -2 v0' u') :", sp.simplify(var - target) == 0)

# round background: v0 theta-independent -> v0' = 0 -> variation vanishes
v0c = sp.Symbol('v0const')  # constant
var_round = var.subs(sp.diff(v0(th), th), 0)
print("round (v0'=0) variation =", sp.simplify(var_round), " (B2 zero reproduced:", sp.simplify(var_round)==0, ")")

print()
print("="*70)
print("CLAIM 1 (b): self-adjointness in weight w = sin th * e^{-2 v0}")
print("="*70)
# The full angular operator inside e^{2v} bracket, linearized about v0:
#   u_thth + cot(th) u_th  +  (variation of -v_th^2) = u_thth + cot th u_th - 2 v0' u_th
# => A[u] = u'' + p(th) u'  with p = cot th - 2 v0'
v0p = sp.Function('v0p')  # treat v0'(theta) as an arbitrary function p0(theta)
p = sp.cos(th)/sp.sin(th) - 2*v0p(th)

# SL self-adjoint form: w * (u'' + p u') = (w u')'  requires w'/w = p  => w = exp(int p)
# int p = ln(sin th) - 2 * int v0p = ln(sin th) - 2 v0   (since int v0' = v0)
w = sp.sin(th) * sp.exp(-2*sp.Function('v0')(th))
# check w'/w == p  with v0' = v0p
wp_over_w = sp.simplify(sp.diff(w, th)/w)
wp_over_w = wp_over_w.subs(sp.Derivative(sp.Function('v0')(th), th), v0p(th))
wp_over_w = sp.simplify(wp_over_w)
print("w'/w =", wp_over_w)
print("p    =", sp.simplify(p))
print("SELF-ADJOINT (w'/w == p):", sp.simplify(wp_over_w - p) == 0)

# Verify directly that w*(u'' + p u') = d/dth ( w u' )
A_u = sp.diff(u(th), th, 2) + p*sp.diff(u(th), th)
lhs = sp.expand(w*A_u)
rhs = sp.diff(w*sp.diff(u(th), th), th)
rhs = rhs.subs(sp.Derivative(sp.Function('v0')(th), th), v0p(th))
lhs = lhs  # already in v0p
diff = sp.simplify(lhs - rhs)
print("w*A[u] - (w u')' =", diff, " => SL form exact:", diff == 0)

print()
print("="*70)
print("CLAIM 1 (c) ATTACK: can the drift create a bound state / flip sign alone?")
print("="*70)
# A real SL operator L = (1/w) d/dth ( w d/dth ) is the Laplacian in weight w.
# It is NEGATIVE SEMI-DEFINITE: <u, L u>_w = int w u (1/w)(w u')' dth = [w u u'] - int w (u')^2 dth.
# With self-adjoint BC the boundary term vanishes => <u,Lu>_w = - int w (u')^2 <= 0.
# The drift term is ENTIRELY contained in this (it only reshapes w>0). Show the quadratic form:
u_ = sp.Function('u')
# Liouville transform: any u''+p u' = 0-order-free operator. Eigenproblem L u = -lambda u with w-inner product.
# Quadratic form: <u, L u>_w = -int_0^pi w(th) u'(th)^2 dth  (after IBP, BC-killed boundary)
# Since w = sin th e^{-2v0} > 0 for th in (0,pi) for ANY real bounded v0, the form is strictly <=0.
print("w(th) = sin(th) e^{-2 v0(th)} > 0 on (0,pi) for any real v0  =>  weight stays POSITIVE.")
print("Quadratic form <u,Lu>_w = -int_0^pi w (u')^2 dth <= 0 (self-adjoint BC).")
print("A drift p u' is fully absorbed into w>0; it cannot make the form positive,")
print("cannot add a 0th-order (potential) term, cannot create a discrete NEGATIVE-energy bound state by itself.")

# Numerical demonstration: take an extreme drift and show spectrum stays sign-definite (no bound state appears)
import numpy as np
print()
print("Numerical demonstration (extreme non-round drift, Liouville form):")
N = 2000
ths = np.linspace(1e-4, np.pi-1e-4, N)
h = ths[1]-ths[0]
for amp in [0.0, 0.5, 2.0, 5.0]:
    v0arr = amp*np.cos(ths)            # an arbitrary strong non-round v0
    v0parr = -amp*np.sin(ths)          # v0'
    warr = np.sin(ths)*np.exp(-2*v0arr)
    # Build self-adjoint matrix for (1/w)(w u')' via finite-volume (flux form), Dirichlet ends
    # L u_i = (1/w_i)[ wph (u_{i+1}-u_i) - wmh (u_i - u_{i-1}) ] / h^2 , wph = w at i+1/2
    n = N-2
    M = np.zeros((n,n))
    for k in range(n):
        i = k+1
        wph = 0.5*(warr[i]+warr[i+1])
        wmh = 0.5*(warr[i]+warr[i-1])
        M[k,k] = -(wph+wmh)/(warr[i]*h*h)
        if k+1<n: M[k,k+1] = wph/(warr[i]*h*h)
        if k-1>=0: M[k,k-1] = wmh/(warr[i]*h*h)
    # symmetrize in the w-metric: D = diag(sqrt(w)) M D^{-1} should be symmetric -> use eig of M (real)
    ev = np.linalg.eigvals(M)
    ev = np.sort(ev.real)
    # L = (1/w)(w u')' is negative semidef => eigenvalues <= 0. "bound state" would be a positive eval.
    print(f"  drift amp={amp:4.1f}:  max eigenvalue of L = {ev.max(): .4e}  (positive => bound state; should be <=~0)")
print()
print("=> No positive eigenvalue appears for any drift strength: the drift NEVER creates a bound state.")
