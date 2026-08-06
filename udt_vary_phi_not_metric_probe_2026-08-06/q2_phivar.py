import sympy as sp

r = sp.symbols('r', positive=True)
M = sp.symbols('M')
phi = sp.Function('phi')
p = phi(r)
p1 = sp.Derivative(p, r)
p2 = sp.Derivative(p, (r,2))

# --- Q1 free-metric: solve G^t_t = 0  (-2 r phi' - e^{2phi} + 1 = 0) ---
sol = sp.dsolve(sp.Eq(-2*r*sp.diff(p,r) - sp.exp(2*p) + 1, 0), p)
print("=== Q1 free-g solution of G^t_t=0 ===")
print(sol)

# --- Q2: reduce action.  R from q1; sqrt(-g)=r^2 sin(theta). Drop 4pi (angular) & sin. ---
# R (from q1), multiply by r^2 -> radial Lagrangian density L(phi,phi',phi'')
pf, pf1, pf2 = sp.symbols("f f1 f2")  # placeholders phi, phi', phi''
R = 2*(-2*r**2*pf1**2 + r**2*pf2 + 4*r*pf1 + sp.exp(2*pf) - 1)*sp.exp(-2*pf)/r**2
L = sp.simplify(R * r**2)   # = R * sqrt(-g)/sin(th), the radial integrand
print("=== radial Lagrangian L = R*r^2 ===")
print(sp.simplify(L))

# Euler-Lagrange with second derivative: dL/df - d/dr(dL/df1) + d^2/dr^2(dL/df2)
dLdf  = sp.diff(L, pf)
dLdf1 = sp.diff(L, pf1)
dLdf2 = sp.diff(L, pf2)

# substitute placeholders back to functions to take total r-derivatives
def tofunc(expr):
    return expr.subs({pf2:p2, pf1:p1, pf:p})
def toplace(expr):
    return expr.subs({p2:pf2, p1:pf1, p:pf})

term1 = tofunc(dLdf)
term2 = sp.diff(tofunc(dLdf1), r)
term3 = sp.diff(tofunc(dLdf2), r, 2)
EL = sp.simplify(term1 - term2 + term3)
print("=== phi-EL equation E[phi] = 0 ===")
print(EL)
print("=== EL simplified/factored ===")
print(sp.simplify(sp.factor(EL)))
