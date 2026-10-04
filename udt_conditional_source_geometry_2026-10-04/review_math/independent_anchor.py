"""Source-first CGE1 review, no parent implementation imports."""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import resource
resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
import json, platform, sys
from pathlib import Path
import sympy as s
import mpmath as mp

out = {'python':sys.version,'sympy':s.__version__,'mpmath':mp.__version__,
       'platform':platform.platform(),'finite_cases':4,'mp_dps':50,'symbolic':{}}
t,r,th,ph=s.symbols('t r theta phi',real=True)
x=[t,r,th,ph]
f=s.Function('f')(r)
g=s.diag(-f,1/f,r*r,r*r*s.sin(th)**2)
gi=g.inv()
Gam=[[[s.simplify(sum(gi[i,l]*(s.diff(g[l,k],x[j])+s.diff(g[l,j],x[k])-s.diff(g[j,k],x[l]))/2 for l in range(4))) for k in range(4)] for j in range(4)] for i in range(4)]
Ric=s.Matrix(4,4,lambda i,j:s.simplify(sum(s.diff(Gam[k][i][j],x[k])-s.diff(Gam[k][i][k],x[j])+sum(Gam[k][i][j]*Gam[l][k][l]-Gam[l][i][k]*Gam[k][j][l] for l in range(4)) for k in range(4))))
m,lam=s.symbols('m Lambda',real=True)
F=1-2*m/r-lam*r*r/3
subst=lambda z:s.simplify(z.subs(f,F).doit())
assert all(subst(Ric[i,j]-lam*g[i,j])==0 for i in range(4) for j in range(4))
out['symbolic']['Ricci_general_diagonal']=[str(Ric[i,i]) for i in range(4)]
out['symbolic']['all_16_Ricci_residuals_zero']=True
bad=1-2*m/r-lam*r*r/6
bad_ric=s.simplify((Ric[2,2]-lam*g[2,2]).subs(f,bad).doit())
assert bad_ric != 0
out['symbolic']['wrong_Lambda_coefficient_residual']=str(bad_ric)
D=1-3*m/r
Om=s.sqrt(m/r**3-lam/3)
u=s.Matrix([1/s.sqrt(D),0,0,Om/s.sqrt(D)])
G=s.diag(-F,1/F,r*r,r*r)
assert s.simplify((u.T*G*u)[0]+1)==0
orbit_acc=[subst(sum(Gam[i][j][k]*u[j]*u[k] for j in range(4) for k in range(4))).subs(th,s.pi/2).simplify() for i in range(4)]
assert all(v==0 for v in orbit_acc)
out['symbolic']['circular_clock_norm_and_geodesic']=True
eps,b=s.symbols('epsilon b',positive=True)
W=s.sqrt(eps**2-F); q=s.sqrt(1-F*b*b/r**2)
v=s.Matrix([eps/F,W,0,0]); k=s.Matrix([1/F,q,0,b/r**2])
for label,vec in [('receiver',v),('null_ray',k)]:
 acc=[s.simplify(vec[1]*s.diff(vec[i],r)+subst(sum(Gam[i][j][z]*vec[j]*vec[z] for j in range(4) for z in range(4))).subs(th,s.pi/2)) for i in range(4)]
 assert all(a==0 for a in acc), (label,acc)
 assert s.simplify((vec.T*G*vec)[0]+(1 if label=='receiver' else 0))==0
 out['symbolic'][label+'_norm_and_geodesic']=True
er=s.Matrix([W/F,eps,0,0]); eth=s.Matrix([0,0,1/r,0]); eph=s.Matrix([0,0,0,1/r])
T=s.Matrix.hstack(v,er,eth,eph)
assert (T.T*G*T-s.diag(-1,1,1,1)).applyfunc(s.simplify)==s.zeros(4)
om_o=s.simplify(-(k.T*G*v)[0])
sky=s.Matrix([-s.simplify((k.T*G*e)[0]/om_o) for e in [er,eth,eph]])
assert s.simplify((sky.T*sky)[0]-1)==0
out['symbolic']['receiver_tetrad_and_sky_unit']=True
L2=s.simplify(r**4*Om**2/D)
ell=s.symbols('ell',real=True)
V=F*(1+ell**2/r**2)
out['symbolic']['circular_fixed_L_potential_second_derivative']=str(s.factor(s.diff(V,r,2).subs(ell**2,L2)))

mp.mp.dps=50
mass=mp.mpf(1); la=mp.mpf(1)/10000; a=mp.mpf(10); R0=mp.mpf(20); ep=mp.mpf(6)/5; b0=mp.mpf(2)
ff=lambda rr:1-2*mass/rr-la*rr*rr/3
ww=lambda rr:mp.sqrt(ep*ep-ff(rr))
qq=lambda rr,bb:mp.sqrt(1-ff(rr)*bb*bb/(rr*rr))
dd=1-3*mass/a; oo=mp.sqrt(mass/a**3-la/3)
assert ff(a)>0 and ff(R0)>0 and dd>0 and oo>0 and ww(R0)>0
travel=lambda bb,rr:mp.quad(lambda z:1/(ff(z)*qq(z,bb)),[a,rr])
angle=lambda bb,rr:mp.quad(lambda z:bb/(z*z*qq(z,bb)),[a,rr])
T0=travel(b0,R0); P0=angle(b0,R0)
recv_t=lambda rr:T0+mp.quad(lambda z:ep/(ff(z)*ww(z)),[R0,rr])
recv_tau=lambda rr:mp.quad(lambda z:1/ww(z),[R0,rr])
Z=ff(R0)*(1-b0*oo)/(mp.sqrt(dd)*(ep-ww(R0)*qq(R0,b0)))
def incidence(te):
 fun=lambda bb,rr:(te+travel(bb,rr)-recv_t(rr),oo*te+angle(bb,rr)-P0)
 bb,rr=mp.findroot(fun,(b0,R0),tol=mp.mpf('1e-45'),maxsteps=30)
 res=max(abs(vv) for vv in fun(bb,rr))
 assert res<mp.mpf('1e-40')
 return recv_tau(rr),bb,rr,res
rows=[]
for h in [mp.mpf('1e-4'),mp.mpf('1e-5')]:
 plus=incidence(h); minus=incidence(-h)
 arr=(plus[0]-minus[0])/(2*h*mp.sqrt(dd))
 error=abs(arr-Z)
 assert error<mp.mpf('1e-9')
 rows.append({'h':str(h),'arrival_derivative':str(arr),'abs_error':str(error),
 'plus_b_R_residual':[str(z) for z in plus[1:]],'minus_b_R_residual':[str(z) for z in minus[1:]]})
assert mp.mpf(rows[0]['abs_error'])/mp.mpf(rows[1]['abs_error'])>50
wrong=ff(R0)*(1-b0*oo)/(mp.sqrt(dd)*(ep+ww(R0)*qq(R0,b0)))
assert abs(wrong-Z)>mp.mpf('0.1')
out['incidence']={'inputs':{'m':'1','Lambda':'1/10000','a':'10','R0':'20','epsilon':'6/5','b0':'2'},'endpoint_Z':str(Z),'emitter_Omega':str(oo),'observer_phi':str(P0),'reception_t0':str(T0),'arrival_checks':rows,'wrong_sign_Z':str(wrong)}

ambiguity=[]
A=s.Rational(6,5)
for lval in [-s.Rational(1,10000),s.S(0),s.Rational(1,10000)]:
 fR=F.subs({m:1,r:20,lam:lval}); ea=(A*A+fR)/(2*A); wa=(A*A-fR)/(2*A)
 assert fR>0 and wa>0 and s.simplify(ea*ea-wa*wa-fR)==0
 assert s.simplify(ea+wa-A)==0
 assert (m/r**3-lam/3).subs({m:1,r:10,lam:lval})>0
 ambiguity.append({'Lambda':str(lval),'f_R':str(fR),'epsilon':str(ea),'W':str(wa),'Z':str(A/s.sqrt(s.Rational(7,10)))})
out['exact_shift_ambiguity']=ambiguity
out['status']='PASS_SCOPED_INDEPENDENT_ANCHOR'
dest=Path(__file__).with_name('ANCHOR_RESULT.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
