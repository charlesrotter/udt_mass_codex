"""Transmit test, robust. Small mixing (scaled coboundary) so all legs stay hyperbolic.
Q: does the loop depth-obstruction depend on the DEPTH PROFILE phi (=> transmit / pin phi),
or only on the mixing data k (=> constrains mixing, phi free)?"""
import sympy as sp
eta=sp.diag(-1,1,1)
def arrow(a,s,m): return sp.Matrix([[a,0,m],[0,1/a,0],[0,0,s]])
def CA(A): return sp.simplify(eta.inv()*A.T*eta*A)
def dt(A,clock):
    # timelike eigenvalue as perturbation series around the clock slot 'clock' (=a^2 at t=0)
    C=CA(A);Cb=sp.Matrix([[C[0,0],C[0,2]],[C[2,0],C[2,2]]])
    tb=Cb.trace();db=Cb.det()
    c1,c2=sp.symbols('c1 c2')
    lam=clock+c1*t+c2*t**2
    eq=sp.expand(lam**2-tb*lam+db)
    e1=eq.coeff(t,1); e2=eq.coeff(t,2)
    s1=sp.solve(e1,c1)[0]; s2=sp.solve(e2.subs(c1,s1),c2)[0]
    lam=clock+s1*t+s2*t**2
    return sp.Rational(-1,2)*sp.log(lam),True

t=sp.symbols('t',positive=True)  # mixing strength knob (scales k)
def a_of(pi,pj): return sp.exp(-(pj[0]-pi[0]))
def s_of(pi,pj): return pj[1]/pi[1]
def m_cob(pi,pj): return t*(a_of(pi,pj)*pj[2]-s_of(pi,pj)*pi[2])
def arr(pi,pj): return arrow(a_of(pi,pj),s_of(pi,pj),m_cob(pi,pj))

phiP,phiQ,phiR=sp.symbols('phiP phiQ phiR',real=True)
P=(phiP,sp.Rational(2),sp.Rational(1,3))
Q=(phiQ,sp.Rational(3),sp.Rational(1,2))
Rr=(phiR,sp.Rational(5,2),sp.Rational(-1,4))
legs=[(P,Q),(Q,Rr),(Rr,P)]
# series-expand each leg's depth to O(t^2) and sum the loop
loop=0
for (pi,pj) in legs:
    clock=a_of(pi,pj)**2   # timelike eigenvalue at t=0
    d,ok=dt(arr(pi,pj),clock)
    d=sp.series(d,t,0,3).removeO()
    loop+=d
loop=sp.simplify(sp.expand(loop))
print("loop depth-sum, series in mixing strength t (O(t^3) dropped):")
sp.pprint(sp.collect(sp.expand(loop),t))
print("\nO(t^0) term (should be 0: pure depth closes):",
      sp.simplify(loop.coeff(t,0)))
print("O(t^1) term:",sp.simplify(loop.coeff(t,1)))
o2=sp.simplify(loop.coeff(t,2))
print("O(t^2) obstruction:",o2)
print("\nDoes O(t^2) obstruction depend on the depth profile phi?")
print("  d/dphiP =",sp.simplify(sp.diff(o2,phiP)))
print("  d/dphiQ =",sp.simplify(sp.diff(o2,phiQ)))
print("  d/dphiR =",sp.simplify(sp.diff(o2,phiR)))
