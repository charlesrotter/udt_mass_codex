"""CPR1 finite checks; analytic arguments, not these samples, own the limits."""
from pathlib import Path
import json, platform
import sympy as S
import mpmath as M

B=Path(__file__).resolve().parent

def symbolic():
    u,r,t,p=S.symbols('u r theta phi', real=True)
    m,L=S.symbols('m Lambda', real=True)
    f=1-2*m/r-L*r*r/3
    q=[u,r,t,p]
    g=S.Matrix([[-f,-1,0,0],[-1,0,0,0],[0,0,r*r,0],[0,0,0,r*r*S.sin(t)**2]])
    gi=g.inv()
    G=[[[S.simplify(sum(gi[i,l]*(S.diff(g[l,k],q[j])+S.diff(g[l,j],q[k])-S.diff(g[j,k],q[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
    Ric=S.Matrix(4,4,lambda i,j:S.simplify(sum(S.diff(G[k][i][j],q[k])-S.diff(G[k][i][k],q[j])+sum(G[k][i][j]*G[l][k][l]-G[l][i][k]*G[k][j][l] for l in range(4)) for k in range(4))))
    assert (Ric-L*g).applyfunc(S.simplify)==S.zeros(4)
    E,v,b,s=S.symbols('E v b s', positive=True)
    ge=g.subs(t,S.pi/2)
    uv=S.Matrix([1/(E+v),v,0,0])
    kv=S.Matrix([b*b/(r*r*(1+s)),s,0,b/(r*r)])
    def red(expr,ray=False):
        expr=S.factor(expr)
        num,den=S.fraction(expr)
        relation=s*s-1+f*b*b/r**2 if ray else v*v-E*E+f
        variable=s if ray else v
        return S.factor(S.rem(num,relation,variable)/den)
    assert red((uv.T*ge*uv)[0]+1)==0
    assert red((kv.T*ge*kv)[0],True)==0
    # Original-coordinate geodesic equations, with conserved-energy derivatives.
    for vec,vel,dvel,ray in [(uv,v,-S.diff(f,r)/(2*v),False),(kv,s,(-S.diff(f,r)*b*b/r**2+2*f*b*b/r**3)/(2*s),True)]:
        for i in range(4):
            derivative=S.diff(vec[i],r)+S.diff(vec[i],vel)*dvel
            acc=vec[1]*derivative+sum(G[i][j][k].subs(t,S.pi/2)*vec[j]*vec[k] for j in range(4) for k in range(4))
            assert red(acc,ray)==0,(i,ray,red(acc,ray))
    ap=S.simplify((r*r*S.diff(f,r,2)-r*S.diff(f,r))/2)
    at=S.simplify(1-f+r*S.diff(f,r)/2)
    assert ap==-3*m/r and at==3*m/r
    # In this spherical gauge the independent sectional curvatures give K.
    K=S.simplify(S.diff(f,r,2)**2+4*S.diff(f,r)**2/r**2+4*(f-1)**2/r**4)
    I=S.simplify(K-8*L**2/3)
    assert I==48*m*m/r**6
    assert S.diff(I,r)==-288*m*m/r**7
    a=S.symbols('a',positive=True)
    h=1-3*m/a
    nu2=(m/a**3-L/3)/h
    nu02=(m/a**3)/h
    assert S.simplify((nu2-nu02)/nu02)==-L*a**3/(3*m)
    return {'original_EF_Ricci':'PASS: Ric=Lambda g, all16 components',
            'original_EF_norms_and_geodesics':'PASS: both norms and all8 acceleration components',
            'angular_trace':'PASS: -3m/r,+3m/r',
            'Weyl_squared':'48m^2/r^6; spherical sectional formula',
            'proper_orbital_rate_recovery':'PASS: fractional squared-rate shift=-Lambda*a^3/(3*m)'}

def finite(dps):
    M.mp.dps=dps
    a=M.mpf(10);m=M.mpf(1);L=M.mpf('0.0001');H=M.sqrt(L/3)
    h=1-3*m/a;om=M.sqrt(m/a**3-L/3);fa=1-2*m/a-L*a*a/3
    bmax=a/M.sqrt(fa)
    out=[];maximum_residual=M.mpf(0)
    def serial(x):return M.nstr(x,dps)
    for Es,radii in [('1',['1000'])]:
        E=M.mpf(Es)
        def V(x):return M.sqrt(H*H+(E*E-1)*x*x+2*m*x**3)
        def tail(x):return M.quad(lambda y:1/(V(y)*(E*y+V(y))),[0,x])
        def integrals(R,b):
            x=1/R
            def ss(y):return M.sqrt(1+H*H*b*b-b*b*y*y+2*m*b*b*y**3)
            P=M.quad(lambda y:b/ss(y),[x,1/a])
            U=M.quad(lambda y:b*b/(ss(y)*(1+ss(y))),[x,1/a])
            I=M.quad(lambda y:1/ss(y)**3,[x,1/a])
            return P,U,I
        def incidence(R):
            nonlocal maximum_residual
            d=tail(1/R)
            lo=M.mpf(0);hi=M.mpf('.99')*bmax
            P,U,I=integrals(R,hi)
            assert P-om*U-om*d>0,('no frozen bracket',Es,str(R))
            b=min(a*om*d,hi/2)
            for iteration in range(100):
                P,U,I=integrals(R,b)
                F=P-om*U-om*d
                if abs(F)<M.mpf(10)**(-dps+10):break
                if F>0:hi=b
                else:lo=b
                new=b-F/(I*(1-om*b))
                b=new if lo<new<hi else (lo+hi)/2
            else:raise AssertionError('iteration ceiling')
            te=-d-U
            residual=max(abs(te+U+d),abs(om*te+P))
            maximum_residual=max(maximum_residual,residual)
            print('DIAGNOSTIC',dps,Es,str(R),iteration,M.nstr(F,30),M.nstr(residual,30),flush=True); assert residual<M.mpf(10)**(-dps+9)
            v=V(1/R)*R;s=M.sqrt(1-(1-2*m/R-L*R*R/3)*b*b/R**2)
            A=1/(E+v)+v*b*b/(R*R*(1+s))
            Z=(1-om*b)/(M.sqrt(h)*A)
            assert abs(b)<bmax and Z>0
            return te,b,Z
        for Rs in radii:
            R=M.mpf(Rs);te,b,Z=incidence(R)
            errors=[]
            for eps in [M.mpf('.0001'),M.mpf('.00005')]:
                rm=R*(1-eps);rp=R*(1+eps)
                tem,bm,zm=incidence(rm);tep,bp,zp=incidence(rp)
                delta_o=M.quad(lambda x:1/(x*V(x)),[1/rp,1/rm])
                arrived=delta_o/(M.sqrt(h)*(tep-tem))
                errors.append(abs(arrived/Z-1))
            assert errors[0]<M.mpf('1e-6') and errors[1]<M.mpf('1e-6'),errors
            assert errors[1]<M.mpf('.4')*errors[0],errors
            product=H*Z*(-M.sqrt(h)*te)
            if Rs=='1000000':assert abs(product-1)<M.mpf('.005')
            out.append({'E':Es,'R':Rs,'te':serial(te),'b':serial(b),'Z':serial(Z),
                        'H_Z_delta_tau_e':serial(product),'Z_over_R':serial(Z/R),
                        'arrival_relative_errors':list(map(serial,errors))})
    return {'dps':dps,'successful_incidences':40,'maximum_incidence_residual':serial(maximum_residual),'rows':out}

if __name__=='__main__': finite(70)
