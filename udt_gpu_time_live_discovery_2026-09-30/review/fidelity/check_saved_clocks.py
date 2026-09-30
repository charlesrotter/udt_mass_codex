#!/usr/bin/env python3
"""Independent dense trigonometric reconstruction of saved metric clock queries."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import hashlib
import json
from pathlib import Path
import resource
import time
resource.setrlimit(resource.RLIMIT_CPU,(180,180))
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np
started=time.monotonic()
root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
run_names=['survey_n256','challenge_n256','period_k050_n256','period_k100_n256']
result={'method':'Dense direct DFT clock reconstruction and cotangent collocation derivative; no production/reviewer imports',
        'numpy':np.__version__,'runs':{},'artifact_hashes':{}}
parent_clocks=json.loads((root/'SURVEY_CLOCKS.json').read_text())
parent_map={(r['id'],r['te'],r['d']):r for r in parent_clocks}
for name in run_names:
    path=root/'runs'/name
    assert (path/'metadata.json').exists(),name
    meta=json.loads((path/'metadata.json').read_text())
    data=np.load(path/'fields.npz')
    u,t=data['state'],data['times']; spec=meta['spec']; n=spec['n']; k=spec['k']
    ids=[r['id'] for r in spec['cases']]
    theta=2*np.pi*np.arange(n)/n
    modes=np.r_[np.arange(n//2),np.arange(-n//2,0)]
    dft=np.exp(-1j*np.outer(modes,theta))/n
    offsets=np.arange(n)[:,None]-np.arange(n)[None,:]
    safe=np.where(offsets==0,1,offsets)
    D=np.where(offsets==0,0,.5*k*(-1.)**safe/np.tan(np.pi*safe/n))
    px=u[:,:,0]@D.T; qx=u[:,:,2]@D.T; lx=u[:,:,4]@D.T
    current=2*t[:,None,None]*(u[:,:,1]*px+np.exp(2*u[:,:,0])*u[:,:,3]*qx)
    constraint=float(np.max(np.abs(lx-current)))
    integral_mean=float(np.max(np.abs(np.mean(current,axis=-1))))
    rows=[]; parent_error=0.
    for te in (1.,4.,8.,16.):
        for d in (1.,2.,4.,8.):
            if te+d>t[-1]:continue
            ie=np.flatnonzero(np.abs(t-te)<1e-12); io=np.flatnonzero(np.abs(t-(te+d))<1e-12)
            assert len(ie)==len(io)==1
            coeff=u[io[0],:,4]@dft.T
            shifted=(coeff@np.exp(1j*np.outer(modes,theta+k*d))).real
            delta=(shifted-u[ie[0],:,4])/4
            logz=delta-.25*np.log((te+d)/te)
            for j,case in enumerate(ids):
                row={'id':case,'te':te,'d':d,'logZ_min':float(logz[j].min()),
                     'logZ_max':float(logz[j].max()),'logZ_mean':float(logz[j].mean()),
                     'delta_logZ_vs_homogeneous_min':float(delta[j].min()),
                     'delta_logZ_vs_homogeneous_max':float(delta[j].max())}
                rows.append(row)
                if name=='survey_n256':
                    prior=parent_map[(case,te,d)]
                    parent_error=max(parent_error,*(abs(row[q]-prior[q]) for q in row if q not in ('id','te','d')))
    correction_ratios=[]
    for j,case in enumerate(spec['cases']):
        raw_v=sum((amp*np.cos(m*theta+phase) for m,amp,phase in case.get('V',[])),np.zeros(n))
        denom=np.linalg.norm(raw_v)
        correction_ratios.append({'id':case['id'],'relative_L2_velocity_projection':
            float(np.linalg.norm(u[0,j,1]-raw_v)/denom) if denom else 0.})
    summary={'shape':list(u.shape),'clock_query_case_count':len(rows),
       'sampled_logZ_range':[min(q['logZ_min'] for q in rows),max(q['logZ_max'] for q in rows)],
       'sampled_delta_vs_constant_lambda_Taub_min':min(q['delta_logZ_vs_homogeneous_min'] for q in rows),
       'dense_momentum_constraint_max':constraint,'integrability_current_mean_max':integral_mean,
       'parent_clock_summary_max_error':parent_error if name=='survey_n256' else None,
       'initial_velocity_projection_ratios':correction_ratios,
       'sample_extrema':'Finite emitter spatial mesh and listed te,d only; not continuum extrema',
       'queries':rows}
    assert constraint<2e-5
    assert summary['sampled_delta_vs_constant_lambda_Taub_min']>-1e-11
    assert parent_error<1e-10
    result['runs'][name]=summary
    for p in [path/'fields.npz',path/'metadata.json']:
        result['artifact_hashes'][str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
result['elapsed_seconds']=time.monotonic()-started
result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
result['verdict']='PASS_SCOPED_NUMERICAL_RECOMPUTATION'
(out/'SAVED_CLOCK_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**{key:val for key,val in result.items() if key not in ('runs','artifact_hashes')},
    'runs':{name:{key:val for key,val in data.items() if key not in ('queries','initial_velocity_projection_ratios')}
            for name,data in result['runs'].items()}},indent=2))
