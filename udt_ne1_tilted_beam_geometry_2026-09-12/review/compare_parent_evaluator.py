#!/usr/bin/env python3
"""Exposed comparison: parent evaluator versus sealed independent source-first data."""
import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('--mutate',choices=['source_normalization','spatial_hessian'])
args=parser.parse_args()
root=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('parent_ntb1',root/'discover_beams.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
independent=json.loads((root/'review/geodesic_initial.stdout').read_text())
records=[]
failure=None
try:
    for case in independent['cases']:
        eps,xe,mu,psi,to=case['case']
        sol,s,E=p.solve(eps,mu,psi,xe,to,rtol=2e-11,atol=2e-13,step=.05,
                        mutate='drop_spatial_hessian' if args.mutate=='spatial_hessian' else None)
        state=sol.sol(to)
        result=p.readout(to,state,eps,E)
        le=p.fields(1,xe,eps)[0]
        if args.mutate=='source_normalization':le=np.ones(3)
        lo=p.fields(to,state[0],eps)[0]
        X=lo[:,None]*(state[6:].reshape(6,6)[:3,3:]@(le[:,None]*E))
        source=np.array(case['source_basis'])
        ref=np.array(case['physical_variations'])@(source.T@E)
        err=float(np.linalg.norm(X-ref)/max(1,np.linalg.norm(ref)))
        freq=abs(result['frequency']-case['frequency'])/max(1,case['frequency'])
        area=abs(result['area']-case['area'])/max(1,case['area'])
        endpoint=float(np.max(np.abs(state[:3]-np.array(case['endpoint'][:3]))))
        r=dict(case=case['case'],normalized_screen_difference=err,frequency_difference=freq,
               area_difference=area,endpoint_difference=endpoint,
               parent_physical_variations=X.tolist(),independent_transformed=ref.tolist())
        records.append(r)
        assert err<=2e-5,('source_normalized_screen',err)
        assert freq<=2e-8,('frequency',freq)
        assert area<=2e-5,('area',area)
        assert endpoint<=2e-8,('endpoint',endpoint)
except Exception as exc:
    failure=repr(exc)
print(json.dumps(dict(status='FAIL' if failure else 'PASS',mutation=args.mutate,records=records,failure=failure),indent=2))
raise SystemExit(1 if failure else 0)
