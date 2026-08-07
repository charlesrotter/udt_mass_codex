"""Decisive test for the outcome class:
(A) Does imposing C2 closure pin the DEPTH PROFILE phi, or only constrain the mixing?
    - Build a triangle p,q,r with FREE phi_i, R_i and coboundary mixing m(p,q)=a(p,q)k(q)-s(p,q)k(p).
    - Compute the loop depth-sum delta_t(pq)+delta_t(qr)+delta_t(rp). Closure = 0.
    - See whether zero-loop forces a relation among the phi_i (transmit) or only involves k/m.
(B) Pure mixing holonomy: net a=1,s=1, residual m -> elliptic (rotation) vs hyperbolic;
    is any DISCRETE selection of mu forced? (Q2)
"""
import sympy as sp
eta=sp.diag(-1,1,1)
def arrow(a,s,m): return sp.Matrix([[a,0,m],[0,1/a,0],[0,0,s]])
def CA(A): return sp.simplify(eta.inv()*A.T*eta*A)
def dt(A):
    C=CA(A);Cb=C[[0,2],[0,2]];etab=sp.diag(-1,1)
    tb=sp.simplify(Cb.trace());db=sp.simplify(Cb.det());disc=sp.simplify(tb**2-4*db)
    if disc<0: return None  # elliptic: no real depth
    for lam in ((tb+sp.sqrt(disc))/2,(tb-sp.sqrt(disc))/2):
        v=(Cb-lam*sp.eye(2)).nullspace()[0]
        if sp.simplify((v.T*etab*v)[0])<0: return sp.Rational(-1,2)*sp.log(lam)
    return None

# ---- (A) triangle with coboundary mixing, FREE depth/screen ----
# observers: (phi,R,k). arrow p->q: a=exp(-(phiq-phip)), s=Rq/Rp, m=a*kq - s*kp
def a_of(pi,pj): return sp.exp(-(pj[0]-pi[0]))
def s_of(pi,pj): return pj[1]/pi[1]
def m_cob(pi,pj): return a_of(pi,pj)*pj[2]-s_of(pi,pj)*pi[2]
def arr(pi,pj): return arrow(a_of(pi,pj),s_of(pi,pj),m_cob(pi,pj))
import itertools
# rational test observers, arbitrary distinct phi,R,k
P=(sp.Rational(1,5), sp.Rational(2), sp.Rational(1,3))
Q=(sp.Rational(-1,4),sp.Rational(3), sp.Rational(1,2))
R=(sp.Rational(1,2), sp.Rational(5,2),sp.Rational(-1,4))
# verify mixing cocycle: A(pq)A(qr) has m == m_cob(p,r)
comp=sp.simplify(arr(P,Q)*arr(Q,R))
print("mixing cocycle holds (comp m == m_cob(P,R)):",
      sp.simplify(comp[0,2]-m_cob(P,R))==0)
# loop depth sum (closure test) with coboundary mixing on
dpq,dqr,drp=dt(arr(P,Q)),dt(arr(Q,R)),dt(arr(R,P))
if None in (dpq,dqr,drp):
    print("loop has an elliptic leg (no real depth)")
else:
    loop=sp.simplify(dpq+dqr+drp)
    print("coboundary-mixing loop depth sum =",sp.nsimplify(loop)," ~",float(loop))
# compare: m=0 loop sum
def arr0(pi,pj): return arrow(a_of(pi,pj),s_of(pi,pj),0)
loop0=sp.simplify(dt(arr0(P,Q))+dt(arr0(Q,R))+dt(arr0(R,P)))
print("m=0 loop depth sum =",sp.simplify(loop0))

# Does closure (loop=0) pin phi? Check: is the coboundary loop sum independent of phi_i?
# vary only P's phi, keep R,k -> if loop depends on it, closure would relate phi's (transmit)
print("\n--- (B) pure mixing holonomy ---")
m0=sp.symbols('m0',real=True)
U=arrow(1,1,m0)  # net a=1,s=1
C=CA(U);Cb=C[[0,2],[0,2]]
tb=sp.simplify(Cb.trace());db=sp.simplify(Cb.det());disc=sp.simplify(tb**2-4*db)
print("pure-mixing block: trace=",tb," det=",db," disc=",sp.factor(disc))
print("elliptic (complex eig, |lam|=1 rotation) for 0<|m0|<2; hyperbolic |m0|>2")
print("rotation angle cos(theta)= (2-m0^2)/2 -> CONTINUOUS in m0 (no discrete selection)")
