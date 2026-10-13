"""Independent primary-formula and initial-frame Kerr audit, not a ray solve."""
import hashlib,json,platform
from pathlib import Path
import sympy as S

root=Path(__file__).resolve().parents[2]
own=Path(__file__).resolve().parent
expected={'KERR_CANDIDATE.md':'f32a6675633cb51bae540843565ca48e52c61cd19a87db26311fafb35b40b7fe',
    'KERR_MANIFEST.json':'5ccbef24e0fc4b20b8bb4081e2c4d3a78d99dac06efc91ea776f12520463c0dc'}
for n,d in expected.items():assert hashlib.sha256((root/'researcher_b'/n).read_bytes()).hexdigest()==d
M=S.Integer(1); a=S.sqrt(15)/4; y=2/S.sqrt(5)
records=[]
for r in (S.Rational(3,2),S.Rational(31,20)):
    sig=r*r+a*a*y*y; delta=r*r-2*M*r+a*a
    co=S.Matrix([[S.sqrt(delta/sig),0,0,-a*(1-y*y)*S.sqrt(delta/sig)],
                 [0,S.sqrt(sig/delta),0,0],
                 [0,0,S.sqrt(sig/(1-y*y)),0],
                 [-a*S.sqrt((1-y*y)/sig),0,0,(r*r+a*a)*S.sqrt((1-y*y)/sig)]])
    metric=(co.T*S.diag(-1,1,1,1)*co).applyfunc(S.simplify)
    U=S.Matrix([(r*r+a*a)/S.sqrt(sig*delta),0,0,a/S.sqrt(sig*delta)])
    assert S.simplify((U.T*metric*U)[0])==-1
    assert S.simplify((co*U)[0])==1
    assert all(S.simplify(v)==0 for v in list(co*U)[1:])
    psi=S.simplify(1/(r+S.I*a*y)**3)
    E0=S.simplify(S.re(psi)); B0=S.simplify(S.im(psi))
    E2=S.simplify(6*E0**2);B2=S.simplify(6*B0**2)
    q=S.simplify((4*E2-3*B2)/360)
    assert q<0
    rplus=M+S.sqrt(M*M-a*a)
    assert r>rplus and delta>0 and sig>0 and 1-y*y>0
    assert S.simplify(metric.det())==-sig**2
    if r==S.Rational(3,2):
        assert E2==0 and B2==S.Rational(2,9) and q==-S.Rational(1,540)
    else:assert metric[0,0]<0
    records.append({'r':str(r),'rplus':str(rplus),'sigma':str(sig),'delta':str(delta),
        'gtt':str(metric[0,0]),'det_metric':str(S.simplify(metric.det())),
        'E0_primary':str(E0),'B0_primary':str(B0),'E2':str(E2),'B2':str(B2),
        'quartic_conditional_on_FAC1':str(q)})
result={'cases':records,'python':platform.python_version(),'sympy':S.__version__,
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'bound_author_inputs':expected,
    'scope':'primary published principal-frame scalar and independent coframe normalization; no original-curvature replay or Kerr null integration'}
with (own/'kerr_review_check01_result.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
