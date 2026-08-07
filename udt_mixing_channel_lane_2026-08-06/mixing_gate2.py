"""Gate, part 2: (a) char-poly is frame-invariant (ground sec.2) and depends on mu
=> mu NOT Lorentz-gauge. (b) exhibit reciprocal-lock-defect invariant. (c) confirm
which eigenline is timelike; (d) explicit attempt to remove mu by an endpoint O(1,2)
boost in the 0-2 plane -> shows diagonalizing C is a FRAME move that preserves the
mu-dependent eigenvalues (does NOT set the ARROW mixing to 0)."""
import sympy as sp

r, s = sp.symbols('r s', positive=True)
mu = sp.symbols('mu', real=True)
L = sp.symbols('L')
eta = sp.diag(-1, 1, 1)
A = sp.Matrix([[1/r,0,mu],[0,r,0],[0,0,s]])
Adag = eta.inv()*A.T*eta
C = sp.simplify(Adag*A)

# (a) frame invariance check: conjugate C by an explicit O(1,2) boost L_p in 0-2 plane
ch = sp.symbols('chi', real=True)  # rapidity
Lp = sp.Matrix([[sp.cosh(ch),0,sp.sinh(ch)],
                [0,1,0],
                [sp.sinh(ch),0,sp.cosh(ch)]])
# verify Lp in O(1,2): Lp^T eta Lp = eta
print("Lp^T eta Lp - eta =", sp.simplify(Lp.T*eta*Lp - eta))
Cconj = sp.simplify(Lp*C*Lp.inv())
cp_C  = sp.factor(sp.expand((C - L*sp.eye(3)).det()))
cp_Cc = sp.factor(sp.expand((Cconj - L*sp.eye(3)).det()))
print("charpoly invariant under Lp-conjugation:", sp.simplify(cp_C - cp_Cc)==0)
print("charpoly still contains mu:", 'mu' in str(cp_C))

# (b) reciprocal-lock-defect invariant: lambda_time * lambda_radial
# radial eigenvalue = r^2 (slot-1 eigenline, eta-orthogonal to the 0-2 mixing plane)
tb = sp.Rational(1,1)/r**2 + s**2 - mu**2      # block trace
db = s**2/r**2                                  # block det (mu-independent)
disc = sp.simplify(tb**2 - 4*db)
lam_minus = sp.simplify((tb - sp.sqrt(disc))/2)   # timelike block eigenvalue
lam_plus  = sp.simplify((tb + sp.sqrt(disc))/2)
I_lock = sp.simplify(lam_minus * r**2)          # =1 iff reciprocal lock intact
print("\nblock trace  =", tb)
print("block det    =", db, " (mu-independent)")
print("lambda_-*r^2 (lock invariant):", sp.simplify(I_lock))
print("lock defect at mu=0:", sp.simplify(I_lock.subs(mu,0)))
# solve lambda_- = 1/r^2  => mu?
sol = sp.solve(sp.Eq(lam_minus, 1/r**2), mu)
print("lambda_time = 1/r^2  <=>  mu in", sol)

# (c) causal check: is the lambda_- eigenline timelike? eigenvector norm sign under eta
Cb = sp.Matrix([[1/r**2, mu/r],[-mu/r, s**2-mu**2]])   # 0-2 block of C
etab = sp.diag(-1,1)
for name,lam in [("lambda_-",lam_minus),("lambda_+",lam_plus)]:
    v = (Cb - lam*sp.eye(2)).nullspace()
    if v:
        vv = v[0]
        nrm = sp.simplify((vv.T*etab*vv)[0])
        print(f"{name}: eta-norm sign of eigvec =", sp.simplify(sp.sign(sp.nsimplify(nrm.subs({r:sp.Rational(1,2),s:sp.Rational(3,2),mu:sp.Rational(1,10)})))))
