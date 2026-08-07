"""Q0/GATE (F-GAUGE): is the clock->screen mixing mu a non-gauge invariant of C_A?
Model: reciprocal-lock + one live screen slot. 3 slots: 0=clock(timelike),
1=x(radial), 2=y(screen). eta = diag(-1,1,1).
A carries: depth boost (reciprocal in 0-1: diag(r^-1, r)), screen ratio (s in slot 2),
and an explicit UNIPOTENT clock->screen mixing mu in the (0,2) block (upper-unitriangular).
Exact sympy, float-free.
"""
import sympy as sp

r, s, mu = sp.symbols('r s mu', positive=True)  # r=e^delta>0, s=R_q/R_p>0; mu real (use symbol)
mu = sp.symbols('mu', real=True)
L = sp.symbols('L')  # char-poly variable

eta = sp.diag(-1, 1, 1)

# Comparison arrow A: upper-triangular, mixing in (0,2)
A = sp.Matrix([[1/r, 0,  mu],
               [0,   r,  0 ],
               [0,   0,  s ]])

# metric adjoint on flat endpoint frames g_p=g_q=eta (ground PART 0 convention)
Adag = eta.inv() * A.T * eta
C = sp.simplify(Adag * A)
print("C_A =")
sp.pprint(C)

charpoly = sp.factor(sp.expand((C - L*sp.eye(3)).det()))
print("\ncharpoly det(C - L I) =")
sp.pprint(charpoly)

# invariants
trace = sp.simplify(C.trace())
det = sp.simplify(C.det())
# second invariant (sum of principal 2x2 minors)
c2 = sp.simplify(sp.Rational(1,2)*(trace**2 - (C*C).trace()))
print("\nTrace(C)   =", sp.simplify(trace))
print("Inv2(C)    =", sp.simplify(c2))
print("Det(C)     =", sp.simplify(det))

# eigenvalues
eig = C.eigenvals()
print("\neigenvalues:")
for k,v in eig.items():
    print("  mult", v, ":", sp.simplify(k))
