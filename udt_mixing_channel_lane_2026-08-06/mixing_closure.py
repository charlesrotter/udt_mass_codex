"""Q1/Q2: composition, C2 closure, and mu-selection.
Arrow A(a,s,m)=[[a,0,m],[0,1/a,0],[0,0,s]] (reciprocal lock b=1/a; a=e^{-Dphi}, s=R-ratio).
delta_t := -(1/2) log(lambda_timelike of C_A). Test: (i) group law; (ii) additivity of
delta_t under composition (C2 cocycle/closure); (iii) mixing cocycle condition & constant-mu
consistency; (iv) loop holonomy: elliptic/hyperbolic, and whether closure QUANTIZES mu."""
import sympy as sp

def arrow(a,s,m):
    return sp.Matrix([[a,0,m],[0,1/a,0],[0,0,s]])
eta=sp.diag(-1,1,1)
def CA(A):
    return sp.simplify(eta.inv()*A.T*eta*A)
def lam_time(A):
    # clock-connected (timelike) eigenvalue of the 0-2 block, via causal label
    C=CA(A); Cb=C[[0,2],[0,2]]; etab=sp.diag(-1,1)
    tb=sp.simplify(Cb.trace()); db=sp.simplify(Cb.det())
    disc=sp.simplify(tb**2-4*db)
    lp=(tb+sp.sqrt(disc))/2; lm=(tb-sp.sqrt(disc))/2
    return lp,lm,disc

# (i) group law
a1,a2,s1,s2,m1,m2=sp.symbols('a1 a2 s1 s2 m1 m2',positive=True)
prod=sp.simplify(arrow(a1,s1,m1)*arrow(a2,s2,m2))
print("A1*A2 =");sp.pprint(prod)
print("=> composed m =", sp.simplify(prod[0,2]),"  (a1*m2 + m1*s2)")

# (ii) additivity defect of delta_t (rational test point, exact)
subs={a1:sp.Rational(1,2),s1:sp.Rational(3,2),m1:sp.Rational(1,7),
      a2:sp.Rational(2,3),s2:sp.Rational(5,4),m2:sp.Rational(1,5)}
A1=arrow(a1,s1,m1).subs(subs);A2=arrow(a2,s2,m2).subs(subs);A12=(A1*A2)
def dt(A):
    lp,lm,disc=lam_time(A)
    # pick timelike eigenvalue by eigenvector eta-norm sign
    C=CA(A);Cb=C[[0,2],[0,2]];etab=sp.diag(-1,1)
    out=[]
    for lam in (lp,lm):
        v=(Cb-lam*sp.eye(2)).nullspace()[0]
        if sp.simplify((v.T*etab*v)[0])<0: out.append(lam)
    lamt=out[0]
    return sp.Rational(-1,2)*sp.log(lamt)
d1,d2,d12=dt(A1),dt(A2),dt(A12)
defect=sp.simplify(d12-d1-d2)
print("\ndelta_t additivity defect (m!=0) =",sp.nsimplify(sp.simplify(defect)),
      " ~", float(defect))
# same at m=0
subs0=dict(subs);subs0[m1]=0;subs0[m2]=0
B1=arrow(a1,s1,m1).subs(subs0);B2=arrow(a2,s2,m2).subs(subs0)
print("additivity defect (m=0) =",sp.simplify(dt(B1)+dt(B2)-dt(B1*B2)))

# (iii) mixing cocycle condition: constant m=mu consistent?
a,ss=sp.symbols('a ss',positive=True);mu=sp.symbols('mu',real=True)
print("\nconstant-mu consistency needs a + s = 1 (a=e^-Dphi,s=R-ratio):",
      sp.simplify(sp.Eq(mu, a*mu+mu*ss)))
