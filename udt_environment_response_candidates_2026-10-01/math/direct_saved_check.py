"""Exposed independent metric-only saved-artifact ERC1 recomputation."""
import hashlib,json,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.interpolate import make_interp_spline
from scipy.integrate import quad
from scipy.optimize import brentq

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
binding=[]
for file in ['PARENT_CANDIDATE_FREEZE.json','PARENT_OUTPUT_FREEZE.json']:
    freeze=json.loads((ROOT/file).read_text())
    for name,wanted in freeze['sha256'].items():
        path=Path(name)
        if path.name=='check_candidates.py' and hashlib.sha256(path.read_bytes()).hexdigest()!=wanted:
            path=path.with_name('check_candidates_initial.py')
        got=hashlib.sha256(path.read_bytes()).hexdigest()
        assert got==wanted,(str(path),got,wanted)
        binding.append({'path':str(path),'sha256':got})

# Differentiate polynomial ODE expressions, not the parent's series utility.
H,R,P,a,alpha=s.symbols('H R P a alpha')
vector=[R/6-2*H*H,P,-3*H*P-R/(6*alpha),a*H]
variables=[H,R,P,a]
deriv=lambda f:s.expand(sum(s.diff(f,x)*v for x,v in zip(variables,vector)))
at0={H:0,R:0,a:1}
value=a; series=[]
for n in range(1,6):
    value=deriv(value)
    series.append(s.simplify(value.subs(at0)/s.factorial(n)))
assert series==[0,0,P/36,0,-P/(4320*alpha)]

# Exact Vandermonde differentiation weights, with centered subtraction for
# constants. No parent finite_diff_weights/correlation implementation is used.
nodes=list(range(-5,6))
V=s.Matrix([[s.Integer(j)**k for j in nodes] for k in range(11)])
weights={}
for d in range(1,5):
    target=s.zeros(11,1);target[d]=s.factorial(d)
    rational=V.inv()*target
    weights[d]=np.array([np.longdouble(str(s.N(q,30))) for q in rational])
def derivatives(values,step):
    values=values.astype(np.longdouble)
    windows=np.lib.stride_tricks.sliding_window_view(values,11)
    centered=windows-windows[:,5,None]
    return [(centered@weights[d])/np.longdouble(step)**d for d in range(1,5)]

summary=json.loads((ROOT/'parent_full/summary.json').read_text())
records=[]
for case in summary['cases']:
    name=case['id'];lam=case['Lambda'];original=case['levels'][-1]
    record={'id':name,'grids':[]}
    for n in [32,64,128]:
        path=ROOT/'parent_full'/name/'level_2'/f'grid_{n}.npz'
        with np.load(path) as data:
            times=data['t']; states=data['y']
        assert times.shape==(n+1,) and states.shape==(5,n+1)
        assert np.isfinite(states).all()
        Hs,Rs,Ps,av,eta=states
        step=times[1]-times[0]
        a1,a2,a3,a4=derivatives(av,step)
        aa=av[5:-5].astype(np.longdouble);hh=a1/aa
        rr=6*(a2/aa+hh*hh)
        rp=6*(a3/aa+a1*a2/aa**2-2*a1**3/aa**3)
        rpp=6*(a4/aa+a2*a2/aa**2-8*a1*a1*a2/aa**3+6*a1**4/aa**4)
        F=1+2*rr;f=rr+rr*rr
        e00=-3*F*a2/aa+f/2+6*hh*rp-lam
        eii=F*(a2/aa+2*hh*hh)-f/2-2*(rpp+2*hh*rp)+lam
        residual=float(max(np.max(np.abs(e00)),np.max(np.abs(eii))))
        row={'n':n,'metric_only_original_tensor_absolute':residual,
             'saved_H_difference':float(np.max(np.abs(hh-Hs[5:-5]))),
             'saved_R_difference':float(np.max(np.abs(rr-Rs[5:-5])))}
        if n==128:assert residual<1e-7,(name,row)
        spline=make_interp_spline(times,av,k=5)
        eta_from_a=lambda t:quad(lambda u:1/float(spline(u)),0,t,epsabs=2e-12,epsrel=2e-12)[0]
        reconstructed=[]
        for item in original['clocks']:
            distance=item['L']
            tb=brentq(lambda t:eta_from_a(t)-distance,0,times[-1],xtol=1e-13)
            ta=brentq(lambda t:eta_from_a(t)-2*distance,0,times[-1],xtol=1e-13)
            p=float(spline(tb)/spline(0));total=float(spline(ta)/spline(0));q=total/p
            values={'first_arrival':tb,'echo_arrival':ta,'p':p,'q':q,'total':total}
            diffs={k:abs(v-item[k]) for k,v in values.items()}
            reconstructed.append({'L':distance,**values,'parent_absolute_differences':diffs})
            if n==128:assert max(diffs.values())<1e-7,(name,diffs)
        row['clocks']=reconstructed
        if n==128 and name=='flat_event':
            cubic=[]
            for item in original['cubic']:
                ell=item['L'];beta=.03/36
                lp=math.log1p(item['p']-1);lq=math.log1p(item['q']-1)
                cubic.append({'L':ell,'p_remainder':lp-beta*ell**3,
                   'q_remainder':lq-7*beta*ell**3,
                   'p_remainder_over_L5':(lp-beta*ell**3)/ell**5,
                   'q_remainder_over_L5':(lq-7*beta*ell**3)/ell**5,
                   'predicted_quintic_p':-.03/4320,
                   'predicted_quintic_q':-31*.03/4320})
            record['saved_clock_cubic_remainders']=cubic
        record['grids'].append(row)
    records.append(record)

result={'pass':True,'exposure':'parent candidate/code/outputs read before this check',
 'method':'saved a-only metric derivatives and a-only null quadrature; no parent imports or RHS',
 'frozen_plan_sha256':hashlib.sha256((OUT/'DIRECT_CHECK_PLAN.md').read_bytes()).hexdigest(),
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'binding_count':len(binding),'bindings':binding,
 'flat_event_a_coefficients':[str(v) for v in series],
 'cases':records}
(OUT/'direct_saved_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':True,'binding_count':len(binding),'case_count':len(records),
 'worst_finest_metric_only_residual':max(r['grids'][-1]['metric_only_original_tensor_absolute'] for r in records),
 'worst_finest_clock_difference':max(max(c['parent_absolute_differences'].values()) for r in records for c in r['grids'][-1]['clocks']),
 'flat_event_a_coefficients':result['flat_event_a_coefficients']},indent=2))
