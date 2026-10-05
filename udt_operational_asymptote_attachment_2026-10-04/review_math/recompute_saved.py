"""Exposed saved-artifact replay; independent direct radial-log quadrature."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import hashlib,json,resource,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import mpmath as mp

p=Path(__file__).resolve().parent
source=p.parent/'CONSTRUCTION_RESULT.json'
saved=json.loads(source.read_text())['precisions'][1]
selected=[r for r in saved['rows'] if r['R'] in ['1000','1000000']]
start=time.time()
records=[]
out=p/'saved_recompute_raw.jsonl'
with out.open('x') as stream:
 for dps in [60,100]:
  mp.mp.dps=dps
  m,a,Lambda=mp.mpf(1),mp.mpf(10),mp.mpf('.0001')
  H=mp.sqrt(Lambda/3); h=1-3*m/a; Om=mp.sqrt(m/a**3-Lambda/3)
  f=lambda r:1-2*m/r-Lambda*r*r/3
  for old in selected:
   row={'kind':'saved_incidence','case':len(records)+1,'dps':dps,'E':old['E'],'R':old['R']}
   try:
    E,R,b,te=[mp.mpf(old[k]) for k in ['E','R','b','te']]
    s=lambda r:mp.sqrt(1-f(r)*b*b/(r*r))
    v=lambda r:mp.sqrt(E*E-f(r))
    zmax=mp.log(R/a)
    knots=[zmax*j/8 for j in range(9)]
    L=mp.quad(lambda z:a*mp.exp(z)/s(a*mp.exp(z)),knots)
    P=mp.quad(lambda z:b/(a*mp.exp(z)*s(a*mp.exp(z))),knots)
    U=mp.quad(lambda z:b*b/(a*mp.exp(z)*s(a*mp.exp(z))*(1+s(a*mp.exp(z)))),knots)
    # Integrate the receiver tail on a distinct exponential map to a finite unit interval.
    V=lambda x:mp.sqrt(H*H+(E*E-1)*x*x+2*m*x**3)
    tail=mp.quad(lambda y:1/(R*V(y/R)*(E*y/R+V(y/R))),[0,1])
    uu=1/(E+v(R));ku=b*b/(R*R*(1+s(R)))
    A=f(R)*uu*ku+uu*s(R)+v(R)*ku
    we=(1-Om*b)/mp.sqrt(h)
    Do=A*L;De=we*L;Z=we/A;deficit=1/H-Do
    # C(0)=-a, not a saved parent residue input.
    K=a/H+E/H**2
    pole=(a+E/H)/mp.sqrt(h)
    vals={'L':L,'A':A,'omega_e':we,'Z':Z,'D_o':Do,'D_e':De,'deficit':deficit,'U':U,'P':P,'receiver_retarded_tail':tail,'R_deficit_over_K':R*deficit/K,'Z_deficit_over_residue':Z*deficit/pole}
    errors={k:abs(value-mp.mpf(old[k]))/max(1,abs(mp.mpf(old[k]))) for k,value in vals.items()}
    incidence=max(abs(te+U+tail),abs(Om*te+P))
    row.update(values={k:mp.nstr(q,dps) for k,q in vals.items()},scaled_errors={k:mp.nstr(q,dps) for k,q in errors.items()},incidence_residual=mp.nstr(incidence,dps),analytic_K=mp.nstr(K,dps),analytic_pole_residue=mp.nstr(pole,dps),passed=bool(max(errors.values())<mp.mpf('1e-50') and incidence<mp.mpf('1e-50')))
   except Exception as exc:
    row.update(passed=False,failure=repr(exc))
   records.append(row);stream.write(json.dumps(row,sort_keys=True)+'\n');stream.flush()
   print(json.dumps({'case':row['case'],'kind':row['kind'],'dps':dps,'passed':row['passed'],'failure':row.get('failure')}),flush=True)
  rc=mp.mpf(saved['outer_root'])
  kc=Lambda*2*rc/3-2*m/rc**2
  for old in saved['radar_control']:
   if old['delta'] not in ['.01','.000001']:continue
   row={'kind':'saved_static_radar_control','case':len(records)+1,'dps':dps,'delta':old['delta']}
   try:
    delta=mp.mpf(old['delta'])
    drad=mp.sqrt(f(a))*mp.quad(lambda y:delta/f(rc-delta*y),[mp.mpf('.5'),1])
    dslice=mp.quad(lambda y:delta/mp.sqrt(f(rc-delta*y)),[mp.mpf('.5'),1])
    vals={'radar_increment':drad,'slice_increment':dslice,'radar_asymptotic_ratio':drad/(mp.sqrt(f(a))*mp.log(2)/kc),'slice_asymptotic_ratio':dslice/(2*(mp.sqrt(delta)-mp.sqrt(delta/2))/mp.sqrt(kc))}
    errors={k:abs(value-mp.mpf(old[k]))/max(1,abs(mp.mpf(old[k]))) for k,value in vals.items()}
    row.update(values={k:mp.nstr(q,dps) for k,q in vals.items()},scaled_errors={k:mp.nstr(q,dps) for k,q in errors.items()},passed=bool(max(errors.values())<mp.mpf('1e-45')))
   except Exception as exc:
    row.update(passed=False,failure=repr(exc))
   records.append(row);stream.write(json.dumps(row,sort_keys=True)+'\n');stream.flush()
   print(json.dumps({'case':row['case'],'kind':row['kind'],'dps':dps,'passed':row['passed'],'failure':row.get('failure')}),flush=True)
result={'all_passed':all(r['passed'] for r in records),'cases':len(records),'source_first_cases':18,'combined_cases':18+len(records),'elapsed_s':time.time()-start,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'max_scaled_error':mp.nstr(max(mp.mpf(x) for r in records for x in r.get('scaled_errors',{}).values()),50),'limits':'finite floating-point saved-value replay, not formal interval or empirical certification'}
(p/'SAVED_RECOMPUTE_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True),flush=True)
