"""Source-first review: exact metric jets; no author-code imports.

FREE supplied compact datum: gamma=I, K=diag(1/3-3q^2/4,-2/3-q,-2/3+q),
q=e*cos(x), x periodic 2pi, transverse translations arbitrary fixed periods.
PINNED equation: owner-provisional Ric=0 sector; K=-gamma_t/2.
One thread, exact SymPy arithmetic, no grid or PDE approximation claim.
"""
import itertools
import json
import platform
import sympy as S

x, e = S.symbols('x e', real=True)
q = e*S.cos(x)
k = [S.Rational(1,3)-3*q*q/4, -S.Rational(2,3)-q, -S.Rational(2,3)+q]
tau = sum(k)
assert S.simplify(tau*tau-sum(z*z for z in k)) == 0
assert S.diff(k[1]+k[2], x) == 0
rdot = [S.diff(k[1]+k[2],x,2),S.diff(k[1],x,2),S.diff(k[2],x,2)]
gt = [-2*z for z in k]
gtt = [-2*tau*z+4*z*z for z in k]
gttt = [-2*r-4*tau*tau*z+12*tau*z*z-8*z*z*z for z,r in zip(k,rdot)]
covjets = [[S.Integer(1)]*3,gt,gtt,gttt]
eps = S.LeviCivita
indices = range(4)

def metric_reconstruction(x0):
    sub = {x:x0,e:S.Rational(1,6)}
    def val(z):
        return S.simplify(S.sympify(z).subs(sub))
    def gjet(a,b,ds=()):
        if a!=b:
            return S.Integer(0)
        if a==0:
            return S.Integer(-1 if not ds else 0)
        if any(d in (2,3) for d in ds):
            return S.Integer(0)
        nt,nx=ds.count(0),ds.count(1)
        return val(S.diff(covjets[nt][a-1],x,nx))
    gi=S.diag(-1,1,1,1)
    gid=[-gi*S.Matrix(4,4,lambda a,b:gjet(a,b,(d,)))*gi for d in indices]
    def low(a,b,c):
        return (gjet(a,b,(c,))+gjet(a,c,(b,))-gjet(b,c,(a,)))/2
    G={(a,b,c):sum(gi[a,h]*low(h,b,c) for h in indices)
       for a,b,c in itertools.product(indices,repeat=3)}
    Gd={(a,b,c,d):sum(gid[d][a,h]*low(h,b,c)+gi[a,h]*(
        gjet(h,b,(c,d))+gjet(h,c,(b,d))-gjet(b,c,(h,d)))/2
        for h in indices)
        for a,b,c,d in itertools.product(indices,repeat=4)}
    def R(a,b,c,d):
        lin=(gjet(a,d,(b,c))+gjet(b,c,(a,d))-gjet(a,c,(b,d))-gjet(b,d,(a,c)))/2
        return S.simplify(lin+sum(gjet(h,j)*(G[h,b,c]*G[j,a,d]-G[h,b,d]*G[j,a,c])
            for h,j in itertools.product(indices,repeat=2)))
    RR={(a,b,c,d):R(a,b,c,d) for a,b,c,d in itertools.product(indices,repeat=4)}
    def Rd(a,b,c,d,n):
        lin=(gjet(a,d,(b,c,n))+gjet(b,c,(a,d,n))-gjet(a,c,(b,d,n))-gjet(b,d,(a,c,n)))/2
        return S.simplify(lin+sum(
            gjet(h,j,(n,))*(G[h,b,c]*G[j,a,d]-G[h,b,d]*G[j,a,c])+
            gjet(h,j)*(Gd[h,b,c,n]*G[j,a,d]+G[h,b,c]*Gd[j,a,d,n]
                     -Gd[h,b,d,n]*G[j,a,c]-G[h,b,d]*Gd[j,a,c,n])
            for h,j in itertools.product(indices,repeat=2)))
    RT={(a,b,c,d):Rd(a,b,c,d,0) for a,b,c,d in itertools.product(indices,repeat=4)}
    ric=S.Matrix(4,4,lambda b,d:sum(gi[a,c]*RR[a,b,c,d] for a,c in itertools.product(indices,repeat=2)))
    rict=S.Matrix(4,4,lambda b,d:sum(gid[0][a,c]*RR[a,b,c,d]+gi[a,c]*RT[a,b,c,d]
        for a,c in itertools.product(indices,repeat=2)))
    assert ric==S.zeros(4)
    assert rict==S.zeros(4)
    kk=[val(z) for z in k]
    # E_ij=R_i0j0. B_ij=(1/2)eps_i^kl R_kl0j; this equals +curl K.
    E=S.Matrix(3,3,lambda i,j:RR[i+1,0,j+1,0])
    B=S.Matrix(3,3,lambda i,j:sum(eps(i,h,l)*RR[h+1,l+1,0,j+1]/2 for h,l in itertools.product(range(3),repeat=2)))
    Et=S.Matrix(3,3,lambda i,j:RT[i+1,0,j+1,0]+(kk[i]+kk[j])*E[i,j])
    # Fermi transport supplies a basis derivative for all three spatial slots.
    Bt=S.Matrix(3,3,lambda i,j:sum(eps(i,h,l)*(RT[h+1,l+1,0,j+1]+(kk[h]+kk[l]+kk[j])*RR[h+1,l+1,0,j+1])/2
        for h,l in itertools.product(range(3),repeat=2)))
    Q=E+S.I*B
    W=Et+S.I*Bt
    i2=S.trace(Q*Q);i3=S.trace(Q**3)
    a=S.factor(1-6*i3*i3/i2**3)
    da=S.factor(36*i3*(i3*S.trace(Q*W)-i2*S.trace(Q*Q*W))/i2**4)
    return dict(x=str(x0),E=str(E),B=str(B),normal_E=str(Et),normal_B=str(Bt),
        I2=str(i2),I3=str(i3),A=str(a),normal_A=str(da)),Q,W

first,Q,W=metric_reconstruction(S.Integer(0))
K0=S.diag(*[S.simplify(z.subs(x,0)) for z in k])
E0=S.simplify(S.trace(K0)*K0-K0*K0)
C=S.diag(0,e,-e)
I2=S.factor(S.trace(E0*E0));I3=S.factor(S.trace(E0**3))
da=S.factor(36*I3*(I3*S.trace(E0*C)-I2*S.trace(E0*E0*C))/I2**4)
assert Q==E0.subs(e,S.Rational(1,6))
assert W==(2*S.trace(K0)*E0+C).subs(e,S.Rational(1,6))
assert da.subs(e,S.Rational(1,6))!=0
second,_,_=metric_reconstruction(S.pi/2)
print(json.dumps(dict(python=platform.python_version(),sympy=S.__version__,
    symbolic_normal_A=str(da),metric_jet_events=[first,second],
    scope='Exact finite metric-jet checks; analytic globally lawful data plus conditional local-development theorem supplies realizations; no finite-jet existence inference'),indent=2))
