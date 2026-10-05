#!/usr/bin/env python3
import hashlib,json,os,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import mpmath as mp

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'CONSTRUCTION_RESULT.json'
data=json.loads(SOURCE.read_text())
saved=next(r for p in data['precisions'] if p['dps']==70 for r in p['rows']
           if r['E']=='10' and r['R']=='1000000')
rows=[]
for dps in (45,75):
    mp.mp.dps=dps
    a,m,E,R=map(mp.mpf,['10','1','10','1000000'])
    H=mp.sqrt(mp.mpf('.0001')/3)
    b,te=mp.mpf(saved['b']),mp.mpf(saved['te'])
    h=1-3*m/a
    Om=mp.sqrt(m/a**3-H**2)
    f=lambda r:1-2*m/r-H*H*r*r
    v=lambda r:mp.sqrt(E*E-f(r))
    s=lambda r:mp.sqrt(1-f(r)*b*b/(r*r))
    breaks=list(map(mp.mpf,['10','100','1000','10000','100000','1000000']))
    L=mp.quad(lambda r:1/s(r),breaks)
    P=mp.quad(lambda r:b/(r*r*s(r)),breaks)
    U=mp.quad(lambda r:b*b/(r*r*s(r)*(1+s(r))),breaks)
    tail=mp.quad(lambda r:1/(v(r)*(E+v(r))),[R,10*R,100*R,mp.inf])
    def dot(r,X,Y):
        return -f(r)*X[0]*Y[0]-X[0]*Y[1]-X[1]*Y[0]+r*r*X[2]*Y[2]
    K=lambda r:[b*b/(r*r*(1+s(r))),s(r),b/(r*r)]
    uo=[1/(E+v(R)),v(R),mp.mpf(0)]
    ue=[1/mp.sqrt(h),mp.mpf(0),Om/mp.sqrt(h)]
    A=-dot(R,K(R),uo)
    omega=-dot(a,K(a),ue)
    Z=omega/A
    Do=A*L
    computed={'L':L,'P':P,'U':U,'receiver_retarded_tail':tail,'A':A,'Z':Z,
              'D_o':Do,'D_e':omega*L,
              'Z_deficit_over_residue':Z*(1/H-Do)/((a+E/H)/mp.sqrt(h))}
    errors={k:abs(x-mp.mpf(saved[k]))/max(1,abs(x)) for k,x in computed.items()}
    incidence=max(abs(te+U+tail),abs(Om*te+P))
    ok=incidence<mp.mpf('1e-30') and max(errors.values())<mp.mpf('1e-30')
    row={'dps':dps,'saved_case':{'E':'10','R':'1000000'},'passed':bool(ok),
         'computed':{k:str(x) for k,x in computed.items()},
         'relative_errors':{k:str(x) for k,x in errors.items()},
         'original_incidence_residual':str(incidence)}
    rows.append(row)
    print('SAVED_REPLAY',dps,'PASS',ok,'max_error',str(max(errors.values())),
          'incidence',str(incidence),flush=True)
result={'parent_artifact_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':sys.version,'mpmath':mp.__version__,'case_count':2,
        'cumulative_cases_including_failure':71,'rows':rows,
        'passed':all(r['passed'] for r in rows)}
(HERE/'SAVED_RECOMPUTATION.json').write_text(json.dumps(result,indent=2)+'\n')
if not result['passed']:
    raise SystemExit(1)
