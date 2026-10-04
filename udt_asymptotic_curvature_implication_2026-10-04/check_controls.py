"""ACI1 exact controls from original metrics, not a proof of the general bound.

Two supplied Lorentz4 product controls, positive symbolic H; no fitted or native
history. Metric choices are free-and-explored. Full original-coordinate curvature
and null-geodesic equations are checked before endpoint/budget identities.
"""
import json
import platform
import sympy as s
from pathlib import Path

B=Path('udt_asymptotic_curvature_implication_2026-10-04')
t,x,y,z=s.symbols('t x y z', real=True)
H=s.symbols('H',positive=True)
L,T=s.symbols('L T',positive=True)
coords=(t,x,y,z)
checks=[]
details=[]

def zero(name,value):
    r=s.simplify(value)
    assert r==0,(name,r)
    checks.append(name)

for label,a in [('exp',s.exp(H*t)),('cosh',s.cosh(H*t))]:
    g=s.diag(-1,a*a,1,s.exp(2*H*y))
    inv=g.inv()
    Gamma=[[[s.simplify(sum(inv[i,l]*(s.diff(g[l,k],coords[j])+
                  s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l]))
                  for l in range(4))/2) for k in range(4)]
                  for j in range(4)] for i in range(4)]
    R=[[[[s.simplify(s.diff(Gamma[i][d][b],coords[c])-
                  s.diff(Gamma[i][c][b],coords[d])+
                  sum(Gamma[i][c][e]*Gamma[e][d][b]-
                      Gamma[i][d][e]*Gamma[e][c][b] for e in range(4)))
                  for d in range(4)] for c in range(4)]
                  for b in range(4)] for i in range(4)]
    Ric=s.Matrix(4,4,lambda b,d: s.simplify(sum(R[i][b][i][d] for i in range(4))))
    scalar=s.simplify(sum(inv[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
    ric2=s.simplify(sum(inv[i,i]*inv[j,j]*Ric[i,j]**2 for i in range(4) for j in range(4)))
    riem2=s.simplify(sum(inv[i,i]*inv[b,b]*inv[c,c]*inv[d,d]*
                 (g[i,i]*R[i][b][c][d])**2
                 for i in range(4) for b in range(4)
                 for c in range(4) for d in range(4)))
    zero(label+'.scalar_zero',scalar)
    zero(label+'.Ric_square',ric2-4*H**4)
    zero(label+'.Riemann_square',riem2-8*H**4)
    zero(label+'.time_space_curvature',R[0][1][0][1]/a**2-H**2)
    zero(label+'.spatial_curvature',R[2][3][2][3]/s.exp(2*H*y)+H**2)
    for i in range(4):
        zero(label+'.free_clock_'+str(i),Gamma[i][0][0])
    k=s.Matrix([1/a,1/a**2,0,0])
    zero(label+'.null_norm',(k.T*g*k)[0])
    for i in range(4):
        zero(label+'.affine_geodesic_'+str(i),
             sum(k[j]*s.diff(k[i],coords[j]) for j in range(4))+
             sum(Gamma[i][j][l]*k[j]*k[l] for j in range(4) for l in range(4)))
    ray=(1-s.exp(-H*t))/H if label=='exp' else s.atan(s.sinh(H*t))/H
    zero(label+'.null_path_integral',s.diff(ray,t)-1/a)
    zero(label+'.curvature_scale_equation',s.diff(a,t,2)-H**2*a)
    # This primitive check directly verifies the signed triangle integral.
    F=s.diff(a,t)*(L-ray)+s.log(a)
    zero(label+'.curvature_integral_primitive',s.diff(F,t)-H**2*a*(L-ray))
    a0=a.subs(t,0)
    zero(label+'.initial_scale',a0-1)
    curve_initial=s.simplify(s.diff(a,t).subs(t,0))
    zero(label+'.initial_frame_connection',Gamma[1][1][0].subs(t,0)-curve_initial)
    zero(label+'.initial_space_geodesic_connection',Gamma[0][1][1].subs(t,0)-curve_initial)
    # At emission0, arrival derivative is a(T)/a(0). It is checked against
    # affine endpoint frequency, not just defined from that frequency.
    Z=a.subs(t,T)/a0
    endpoint_frequency=1/k[0].subs(t,T)
    zero(label+'.arrival_vs_frequency',Z-endpoint_frequency)
    C=s.simplify(s.log(a.subs(t,T))-curve_initial*ray.subs(t,T))
    zero(label+'.sharp_integrated_bound',s.log(Z)-curve_initial*ray.subs(t,T)-C)
    if label=='exp':
        zero(label+'.distance_redshift',Z.subs(T,-s.log(1-H*L)/H)-1/(1-H*L))
    else:
        # With theta=HL=atan(sinh(HT)), cos(theta)=sech(HT).
        zero(label+'.distance_redshift',s.cos(H*ray.subs(t,T))*Z-1)
    details.append({'family':label,'metric':[str(g[i,i]) for i in range(4)],
       'scalar':str(scalar),'Ric_square':str(ric2),'Riemann_square':str(riem2),
       'nonzero_Christoffels':sum(v!=0 for plane in Gamma for row in plane for v in row),
       'nonzero_Riemann_components':sum(v!=0 for a1 in R for a2 in a1 for row in a2 for v in row),
       'Z_at_emission0':str(Z),'initial_mismatch':str(curve_initial*L),
       'curvature_integral_at_reception':str(C)})

q=s.symbols('q',positive=True)
v=(q*q-1)/(q*q+1)
gamma=(q*q+1)/(2*q)
zero('flat.inertial_arrival',1/(gamma*(1-v))-q)
acc,tau=s.symbols('acc tau',positive=True)
te=s.sinh(acc*tau)/acc-L-(s.cosh(acc*tau)-1)/acc
zero('flat.accelerated_emission',te-((1-s.exp(-acc*tau))/acc-L))
zero('flat.accelerated_arrival_derivative',1/s.diff(te,tau)-s.exp(acc*tau))
zero('flat.accelerated_proper_clock',-s.cosh(acc*tau)**2+s.sinh(acc*tau)**2+1)
zero('flat.acceleration_magnitude',-(acc*s.sinh(acc*tau))**2+(acc*s.cosh(acc*tau))**2-acc**2)
assert len(checks)<=100
result={'status':'EXACT_CONTROLS_PASS','checks':len(checks),'named_checks':checks,
        'families':details,'versions':{'python':platform.python_version(),'sympy':s.__version__},
        'scope':'Exact supplied controls; no general theorem, native admission or numerical/asymptotic certification.'}
with (B/'EXACT_CONTROLS.json').open('x') as f:
    json.dump(result,f,indent=2)
    f.write('\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'families':len(details),
                  'versions':result['versions']}))
