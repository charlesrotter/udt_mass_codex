"""CGE1 direct connection/arrival checks. No imported UDT solver or data fit."""
from pathlib import Path
import json,sys,platform,hashlib
import sympy as S
import mpmath as mp
B=Path(__file__).resolve().parent
t,r,th,ph=S.symbols('t r theta phi',real=True)
m,lam=S.symbols('m Lambda',real=True)
f=S.Function('f')(r); coords=[t,r,th,ph]
g=S.diag(-f,1/f,r*r,r*r*S.sin(th)**2); inv=g.inv()
G=[[[S.simplify(sum(inv[i,l]*(S.diff(g[l,k],coords[j])+S.diff(g[l,j],coords[k])-S.diff(g[j,k],coords[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
Ric=S.Matrix(4,4,lambda i,j:S.simplify(sum(S.diff(G[k][i][j],coords[k])-S.diff(G[k][i][k],coords[j])+sum(G[k][k][l]*G[l][i][j]-G[k][j][l]*G[l][i][k] for l in range(4)) for k in range(4))))
F=1-2*m/r-lam*r*r/3
def sub(expr): return S.simplify(expr.subs(f,F).doit())
res=(Ric-lam*g).applyfunc(sub)
assert res==S.zeros(4)
Gq=[[[sub(G[i][j][k]).subs(th,S.pi/2) for k in range(4)] for j in range(4)] for i in range(4)]
gq=g.applyfunc(sub).subs(th,S.pi/2)
Om=S.sqrt(m/r**3-lam/3); h=1-3*m/r
ue=S.Matrix([1/S.sqrt(h),0,0,Om/S.sqrt(h)])
assert S.simplify((ue.T*gq*ue)[0]+1)==0
assert all(S.simplify(sum(Gq[i][j][k]*ue[j]*ue[k] for j in range(4) for k in range(4)))==0 for i in range(4))
energy,b=S.symbols('E b',positive=True);v=S.sqrt(energy**2-F);s=S.sqrt(1-F*b*b/r**2)
uo=S.Matrix([energy/F,v,0,0]);k=S.Matrix([1/F,s,0,b/r**2])
for name,x in [('receiver',uo),('ray',k)]:
 residual=[S.simplify(x[1]*S.diff(x[i],r)+sum(Gq[i][j][q]*x[j]*x[q] for j in range(4) for q in range(4))) for i in range(4)]
 assert residual==[0]*4,(name,residual)
assert S.simplify((k.T*gq*k)[0])==0
assert S.simplify((uo.T*gq*uo)[0]+1)==0
er=S.Matrix([v/F,energy,0,0]);ep=S.Matrix([0,0,0,1/r]);et=S.Matrix([0,0,1/r,0])
frame=S.Matrix.hstack(uo,er,et,ep)
assert (frame.T*gq*frame-S.diag(-1,1,1,1)).applyfunc(S.simplify)==S.zeros(4)
wo=(energy-v*s)/F;we=(1-Om*b)/S.sqrt(h)
assert S.simplify(-(k.T*gq*uo)[0]-wo)==0
assert S.simplify(-(k.T*gq*ue)[0]-we)==0
nr=(energy*s-v)/(energy-v*s);np=F*b/(r*(energy-v*s))
assert S.simplify(nr**2+np**2-1)==0
ell2=S.symbols('ell2',real=True)
V=F*(1+ell2/r**2);lc=S.simplify(r**3*S.diff(F,r)/(2*F-r*S.diff(F,r)))
vpp=S.simplify(S.diff(V,r,2).subs(ell2,lc))
assert S.simplify(S.diff(V,r).subs(ell2,lc))==0
symbolic={'Ricci_before_substitution':str(Ric),'original_Einstein_residual':str(res),'circular_ell_squared':str(lc),'radial_potential_second_derivative':str(vpp),'original_geodesic_checks':['circular','radial_receiver','affine_null'],'tetrad_and_frequency':'exact PASS','sympy_version':S.__version__}

records=[]; summaries=[]
for dps in [36,60]:
 mp.mp.dps=dps
 for ls in ['0','0.0001']:
  L=mp.mpf(ls);a=mp.mpf(10);R0=mp.mpf(50);E=mp.mpf(1)
  ff=lambda x:1-2/x-L*x*x/3
  vv=lambda x:mp.sqrt(E*E-ff(x))
  om=mp.sqrt(1/a**3-L/3);hh=1-3/a
  orbit_vpp=mp.mpf(str(S.N(vpp.subs({m:1,lam:S.Rational(ls),r:10}),dps)))
  assert orbit_vpp>0 and ff(a)>0
  for ps in ['-0.2','0.2']:
   phi0=mp.mpf(ps); group=[]
   for ts in ['-0.001','-0.0005','0','0.0005','0.001']:
    te=mp.mpf(ts)
    def calc(R,impact):
     ss=lambda x:mp.sqrt(1-ff(x)*impact*impact/(x*x))
     T=mp.quad(lambda x:1/(ff(x)*ss(x)),[a,R])
     P=mp.quad(lambda x:impact/(x*x*ss(x)),[a,R])
     O=mp.quad(lambda x:E/(ff(x)*vv(x)),[R0,R])
     return te+T-O,phi0+om*te+P
    R,impact=mp.findroot(calc,(mp.mpf(75),-phi0/(1/a-mp.mpf(1)/75)),tol=mp.mpf(10)**(-(dps-8)),maxsteps=30)
    residual=max(abs(x) for x in calc(R,impact))
    assert residual<mp.mpf(10)**(-(dps-12))
    # Whole interval margins: f concave for Lambda>=0; f/r² decreases for r>3.
    fmin=min(ff(a),ff(R));s2min=1-ff(a)*impact**2/a**2
    assert R>R0>a>3 and fmin>0 and s2min>0 and L>=0
    vr=vv(R);sr=mp.sqrt(1-ff(R)*impact**2/R**2);A=(E-vr*sr)/ff(R)
    Z=(1-om*impact)/(mp.sqrt(hh)*A)
    tau=mp.quad(lambda x:1/vv(x),[R0,R]);nrn=(E*sr-vr)/(E-vr*sr);npn=ff(R)*impact/(R*(E-vr*sr))
    I=mp.quad(lambda x:1/(x*x*(1-ff(x)*impact**2/x**2)**mp.mpf('1.5')),[a,R])
    det=-I*A/vr
    assert Z>0 and A>0 and det<0 and abs(nrn*nrn+npn*npn-1)<mp.mpf(10)**(-(dps-7))
    row={'dps':dps,'Lambda':ls,'phi0':ps,'t_e':ts,'R':str(R),'b':str(impact),'tau_o':str(tau),'Z_endpoint':str(Z),'n_propagation':[str(nrn),str(npn)],'incidence_residual':str(residual),'min_f_bound':str(fmin),'min_s_squared_bound':str(s2min),'min_v_squared_bound':str(2/R),'incidence_jacobian_det':str(det),'radial_orbit_Vpp':str(orbit_vpp)}
    records.append(row);group.append(row)
   mid=group[2];errs=[];drifts=[]
   for low,high,dt in [(0,4,mp.mpf('.001')),(1,3,mp.mpf('.0005'))]:
    minus,plus=group[low],group[high]
    tm,tc,tp=map(mp.mpf,[minus['tau_o'],mid['tau_o'],plus['tau_o']])
    de=dt*mp.sqrt(hh)
    za=(tp-tm)/(2*de);arr2=(tp-2*tc+tm)/de**2
    err=abs(za-mp.mpf(mid['Z_endpoint']));errs.append(err)
    dz_o=(mp.mpf(plus['Z_endpoint'])-mp.mpf(minus['Z_endpoint']))/(tp-tm)
    from_arrival=arr2/za
    drift_err=abs(dz_o-from_arrival);drifts.append(drift_err)
    assert err<mp.mpf('1e-7') and drift_err<mp.mpf('1e-7')
   assert errs[1]<mp.mpf('.4')*errs[0]+mp.mpf('1e-25')
   assert drifts[1]<mp.mpf('.4')*drifts[0]+mp.mpf('1e-25')
   summaries.append({'dps':dps,'Lambda':ls,'phi0':ps,'arrival_frequency_errors':list(map(str,errs)),'optical_drift_arrival_errors':list(map(str,drifts))})
mp.mp.dps=65
precision_errors=[]
for row in records[:20]:
 other=next(q for q in records[20:] if (q['Lambda'],q['phi0'],q['t_e'])==(row['Lambda'],row['phi0'],row['t_e']))
 for key in ['R','b','tau_o','Z_endpoint']:
  err=abs(mp.mpf(row[key])-mp.mpf(other[key]))/max(1,abs(mp.mpf(other[key])))
  precision_errors.append(err);assert err<mp.mpf('1e-23')
# Rational radial-identifiability checks independent of all incidence numerics.
deg=[]
for ls in [S.Rational(0),S.Rational(1,100000),S.Rational(1,10000)]:
 RR=S.Rational(60);HH=S.Rational(7,10);ZZ=S.Integer(2);w=ZZ*S.sqrt(HH);fo=F.subs({m:1,lam:ls,r:RR})
 ee=(w+fo/w)/2;vvv=(w-fo/w)/2
 assert fo>0 and vvv>0 and S.simplify(ee**2-vvv**2-fo)==0
 assert S.simplify((ee+vvv)/S.sqrt(HH)-ZZ)==0
 assert vpp.subs({m:1,lam:ls,r:10})>0
 deg.append({'Lambda':str(ls),'a':'10','R':'60','target_Z':'2','E_exact':str(ee),'v_exact':str(vvv)})
out={'status':'PASS','scope':'conditional finite 4-query construction, not native selection/data fit','python':sys.version,'platform':platform.platform(),'mpmath_version':mp.__version__,'symbolic':symbolic,'ray_records':records,'query_summaries':summaries,'radial_degeneracy_cases':deg,'max_relative_precision_error':str(max(precision_errors)),'ray_count':len(records),'numerical_claim':'finite high-precision quadrature and local root checks, not interval/global certification','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (B/'CONSTRUCTION_RESULT.json').open('x') as fh: json.dump(out,fh,indent=2);fh.write('\n')
print(json.dumps({'status':'PASS','ray_records':len(records),'queries':4,'dps':[36,60],'max_relative_precision_error':out['max_relative_precision_error'],'max_arrival_error':max(float(x) for q in summaries for x in q['arrival_frequency_errors']),'max_drift_error':max(float(x) for q in summaries for x in q['optical_drift_arrival_errors'])}))
