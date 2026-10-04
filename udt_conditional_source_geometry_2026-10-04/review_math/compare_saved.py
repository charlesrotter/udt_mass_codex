"""Exposed saved-artifact arithmetic, no parent function imports."""
import json,hashlib
from decimal import Decimal,localcontext
from pathlib import Path
B=Path(__file__).resolve().parent
P=B.parent
data=json.loads((P/'CONSTRUCTION_RESULT.json').read_text())
own=json.loads((B/'ODE_RESULT.json').read_text())
saved=next(q for q in data['ray_records'] if q['dps']==60 and q['Lambda']=='0' and q['phi0']=='-0.2' and q['t_e']=='0')
diffs={key:abs(own[key]-float(saved[key])) for key in ['R','b','tau_o','Z_endpoint']}
diffs['n_r']=abs(own['n_propagation'][0]-float(saved['n_propagation'][0]))
diffs['n_phi']=abs(own['n_propagation'][1]-float(saved['n_propagation'][1]))
assert max(diffs.values())<2e-9
drifts=[]
with localcontext() as ctx:
    ctx.prec=50
    for dps in [36,60]:
        for la in ['0','0.0001']:
            for phi in ['-0.2','0.2']:
                rows=sorted([q for q in data['ray_records'] if q['dps']==dps and q['Lambda']==la and q['phi0']==phi],key=lambda q:Decimal(q['t_e']))
                errors=[]
                wrong=[]
                for i,j in [(0,4),(1,3)]:
                    lo,mid,hi=rows[i],rows[2],rows[j]
                    de=(Decimal(hi['t_e'])-Decimal(lo['t_e']))*Decimal('.7').sqrt()/2
                    tm,tc,tp=[Decimal(q['tau_o']) for q in [lo,mid,hi]]
                    rate=(tp-tm)/(2*de)
                    curvature=(tp-2*tc+tm)/de**2
                    spectral=(Decimal(hi['Z_endpoint'])-Decimal(lo['Z_endpoint']))/(tp-tm)
                    errors.append(abs(spectral-curvature/rate))
                    wrong.append(abs(spectral-curvature/rate**2))
                assert max(errors)<Decimal('1e-7')
                assert errors[1]<Decimal('.4')*errors[0]+Decimal('1e-25')
                assert min(wrong)>Decimal('1e-7')
                drifts.append({'dps':dps,'Lambda':la,'phi0':phi,'recomputed_correct_errors':list(map(str,errors)),'recomputed_initial_wrong_errors':list(map(str,wrong))})
out={'status':'PASS_EXPOSED_SAVED_COMPARISON','ode_vs_saved_abs_errors':diffs,'drift_recomputation':drifts,'reviewed_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'INITIAL_CANDIDATE.md',P/'CANDIDATE_FREEZE.json',P/'INITIAL_CHECK.py',P/'check_construction.py',P/'CONSTRUCTION_RESULT.json',P/'METHOD_REFERENCES.md',B/'ODE_RESULT.json',Path(__file__)]}}
(B/'SAVED_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
