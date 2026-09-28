"""Independent exact/high-precision checks of the inverse and extrapolated tails.

No construction modules imported. Rational saved decimals define the tested
point estimates; source uncertainty is not inferred from these computations.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='2'
import json,resource,sys,platform
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import sympy as s
import mpmath as mp
P=Path(__file__).resolve().parents[1]; R=P/'review'
fits=json.loads((P/'data/results/full_fits.json').read_text())
x,T=s.symbols('x T',real=True)
rat=lambda v:s.Rational(str(v))
p2=sum(rat(v)*x**j for j,v in enumerate(fits['F2']['beta'][1:],1))
p3=sum(rat(v)*x**j for j,v in enumerate(fits['F3']['beta'][1:],1))
P2=s.Poly(1+x*s.diff(p2,x),x);P3=s.Poly(1+x*s.diff(p3,x),x)
mp.mp.dps=65
aa,bb=[mp.mpf(str(v)) for v in fits['F2']['beta'][1:]]
xs=mp.findroot(lambda u:1+aa*u+2*bb*u*u,2.2)
f=lambda u:u*mp.exp(aa*u+bb*u*u)
fp=lambda u:mp.exp(aa*u+bb*u*u)*(1+aa*u+2*bb*u*u)
fpp=mp.diff(fp,xs);fs=f(xs)
constant=mp.exp(xs-aa*xs-bb*xs*xs)/(-aa-4*bb*xs)
checks={}
# An independently chosen p=2 metric, including exact incidence and curvature.
a=1/(1-T); H=s.diff(a,T)/a
checks['p2_H']=s.simplify(H-a)==0
look=-T; r=1-T; conformal=-T+T*T/2
checks['p2_clock_area_inverse']=s.simplify(conformal-(r*r-1)/2)==0
u=s.symbols('u',nonnegative=True)
checks['p2_affine_extent']=s.integrate(1/(1+u),(u,0,s.oo))==s.oo
checks['p2_proper_extent']=s.integrate(s.Integer(1),(T,-s.oo,0))==s.oo
checks['p2_curvature_limit']=s.limit(6*(s.diff(H,T)+2*H*H),T,-s.oo)==0
checks['p2_deceleration']=s.simplify(-a*s.diff(a,T,2)/s.diff(a,T)**2+2)==0

# Derive the Ricci scalar from metric and Christoffels, without importing a
# cosmological identity or any field equation.
coords=s.symbols('t y1 y2 y3'); tt=coords[0]; A=s.Function('a')(tt)
g=s.diag(-1,A*A,A*A,A*A); gi=g.inv(); n=4
Gam=[[[s.simplify(sum(gi[i,m]*(s.diff(g[m,j],coords[k])+s.diff(g[m,k],coords[j])-s.diff(g[j,k],coords[m]))/2 for m in range(n))) for k in range(n)] for j in range(n)] for i in range(n)]
Ric=s.zeros(n)
for j in range(n):
 for k in range(n):
  Ric[j,k]=s.simplify(sum(s.diff(Gam[i][j][k],coords[i])-s.diff(Gam[i][j][i],coords[k])+sum(Gam[i][i][m]*Gam[m][j][k]-Gam[i][k][m]*Gam[m][j][i] for m in range(n)) for i in range(n)))
scalar=s.simplify(sum(gi[j,k]*Ric[j,k] for j in range(n) for k in range(n)))
checks['metric_ricci_scalar']=s.simplify(scalar-6*(s.diff(A,tt,2)/A+(s.diff(A,tt)/A)**2))==0
assert all(checks.values())
assert P2.count_roots(0,s.oo)==1 and P3.count_roots(0,s.oo)==0
result={'python':sys.version,'sympy':s.__version__,'mpmath':mp.__version__,'platform':platform.platform(),'precision_decimal':65,
 'checks':checks,'F2_positive_roots_exact':int(P2.count_roots(0,s.oo)),'F3_positive_roots_exact':int(P3.count_roots(0,s.oo)),
 'F3_all_real_roots_exact':int(P3.count_roots(-s.oo,s.oo)),'F3_leading_cubic':str(p3.coeff(x,3)),
 'F2_turn':{'x':str(xs),'z':str(mp.expm1(xs)),'F':str(fs),'Fsecond':str(fpp),'singular_H_coefficient':str(constant),
  'lookback':str(mp.quad(lambda u:mp.exp(-u)*fp(u),[0,xs])),
  'affine':str(mp.quad(lambda u:mp.exp(-2*u)*fp(u),[0,xs])),
  'curved_kappa':str(1/fs**2),'curved_turn_H':str(mp.exp(xs)/mp.sqrt(-fs*fpp))},
 'direct_metric_ricci_scalar':str(scalar)}
(R/'INDEPENDENT_ANALYTIC.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
