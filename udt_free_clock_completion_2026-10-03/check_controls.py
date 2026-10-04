"""Exact finite FCL1 controls; no field equation or native admission assumed."""
import json, platform
import sympy as S

R=S.Rational
x,y,z,v=S.symbols('x y z v', real=True)
coords=[x,y,z,v]
N=1+x/5+y/7+z/11+v/13
a=[1+x/3+y*y/5,1+x/4+z*z/6,1+x/5+v*v/7]
h=[q*q for q in a]
gd=[-N*N/x**2]+[q/x**2 for q in h]
dg=[[S.diff(gd[i],q) for q in coords] for i in range(4)]
points=[(R(1,2),R(1,3),-R(1,4),R(1,5)),
        (R(1,3),-R(1,5),R(1,4),R(1,6)),
        (R(1,4),R(1,7),R(1,6),-R(1,5))]
vels=[(R(3,4),0,0),(R(1,2),R(1,2),R(1,4))]
cases=[]
for point in points:
    at=dict(zip(coords,point));xx=at[x]
    G=[q.subs(at) for q in gd]
    D=[[q.subs(at) for q in row] for row in dg]
    nn=N.subs(at);hh=[q.subs(at) for q in h]
    aa=[q.subs(at) for q in a]
    assert xx>0 and nn>0 and all(q>0 for q in hh)
    def christ(k,i,j):
        return ((D[k][i] if k==j else 0)+(D[k][j] if k==i else 0)
                -(D[i][k] if i==j else 0))/(2*G[k])
    for velocity in vels:
        gamma=S.sqrt(1+sum(q*q for q in velocity))
        T=[-gamma/nn]+[S.sympify(q)/aa[i] for i,q in enumerate(velocity)]
        u=[xx*q for q in T]
        acc=[-sum(christ(k,i,j)*u[i]*u[j] for i in range(4) for j in range(4))
             for k in range(4)]
        norm=S.simplify(sum(G[i]*u[i]**2 for i in range(4))+1)
        assert norm==0
        residuals=[];omission=[]
        for i in range(3):
            # Differentiate w_i=h_ii*u^i/x along the original geodesic.
            actual=(sum(S.diff(h[i],coords[j]).subs(at)*u[j]*u[i+1]/xx
                        for j in range(4))+hh[i]*acc[i+1]/xx
                    -hh[i]*u[i+1]*u[0]/xx**2)/u[0]
            wi=hh[i]*T[i+1]
            force=S.diff(N,coords[i+1]).subs(at)*gamma-nn/(2*gamma)*sum(
                S.diff(h[j],coords[i+1]).subs(at)*T[j+1]**2 for j in range(3))
            residuals.append(S.simplify(actual-wi/xx-force))
            omission.append(S.simplify(actual-wi/xx))
        assert residuals==[0,0,0]
        assert any(q!=0 for q in omission)
        cases.append({'point':list(map(str,point)),'orthonormal_spatial_velocity':list(map(str,velocity)),
                      'unit_residual':str(norm),'momentum_residuals':list(map(str,residuals)),
                      'omitted_force_residuals':list(map(str,omission))})

t=S.symbols('t',positive=True)
metric=[-1/t**2,1/t**2,1/t**2,1/t**2]
def flat_conformal_residual(u):
    out=[]
    for k in range(4):
        conn=0
        for i in range(4):
            for j in range(4):
                deriv=lambda a,b: S.diff(metric[a],t) if b==0 else S.S.Zero
                gamma=((deriv(k,i) if k==j else 0)+(deriv(k,j) if k==i else 0)
                       -(deriv(i,k) if i==j else 0))/(2*metric[k])
                conn+=gamma*u[i]*u[j]
        out.append(S.simplify(u[0]*S.diff(u[k],t)+conn))
    return out
gamm=S.sqrt(1+t*t)
uf=[-t*gamm,t*t,0,0]
yf=2-gamm;ef=yf+t
rf=flat_conformal_residual(uf)
assert rf==[0,0,0,0]
assert S.simplify(sum(metric[i]*uf[i]**2 for i in range(4))+1)==0
assert S.simplify(S.diff(yf,t)-uf[1]/uf[0])==0
zf=ef/(t*(gamm-t))
zf_clock=(1/uf[0])/(-S.diff(ef,t)/ef)
assert S.simplify(zf-zf_clock)==0
assert S.simplify(ef-t-yf)==0
assert S.limit(t*zf,t,0,dir='+')==1

ua=[-(1+t*t)/2,(t*t-1)/2,0,0]
ya=1-t+2*S.atan(t);ea=ya+t
ra=flat_conformal_residual(ua)
asq=S.simplify(sum(metric[i]*ra[i]**2 for i in range(4)))
assert S.simplify(sum(metric[i]*ua[i]**2 for i in range(4))+1)==0
assert S.simplify(S.diff(ya,t)-ua[1]/ua[0])==0
assert asq==1/t**2
# kbar=(-1,1,0,0)/x_e; omega_o=x*(-T^0-T^1)/x_e.
omega_a=S.simplify((-ua[0]-ua[1])/ea)
za=S.simplify(1/omega_a)
za_clock=S.simplify((1/ua[0])/(-S.diff(ea,t)/ea))
assert S.simplify(za-za_clock)==0
assert S.simplify(ea-t-ya)==0
assert S.limit(za,t,0,dir='+')==1
assert S.limit(t*za,t,0,dir='+')==0
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':S.__version__,
    'scope':'Three exact supplied-control families, not proof by sampling or native admission',
    'nonuniform_cases':cases,
    'free_receiver':{'geodesic_residuals':list(map(str,rf)),'xZ_limit':'1',
                     'emitter_x':str(ef),'Z':str(zf),'actual_clock_ratio_agrees':True},
    'accelerated_receiver':{'acceleration':list(map(str,ra)),'proper_acceleration_squared':str(asq),
                            'Z_limit':'1','xZ_limit':'0','emitter_x':str(ea),
                            'actual_clock_ratio_agrees':True}},indent=2))
