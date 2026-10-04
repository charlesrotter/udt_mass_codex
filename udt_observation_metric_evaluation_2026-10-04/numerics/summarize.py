"""Frozen OEV1 finite-evaluation diagnostics; regression, not physical evidence."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('run');ap.add_argument('output')
    args=ap.parse_args();cfg=json.loads(Path(args.config).read_text());run=Path(args.run)
    meta=json.loads((run/'metadata.json').read_text())
    assert meta['config_sha256']==sha(args.config)
    cases=[c for c in cfg['cases'] if c.get('smoke')] if meta['smoke'] else cfg['cases']
    tolerances=[cfg['tolerances'][-1]] if meta['smoke'] else cfg['tolerances']
    metrics=['null_relative','momentum_relative','metricity_absolute',
             'transported_k_absolute','original_residual_absolute',
             'original_residual_scaled','residual_difference_refinement',
             'endpoint_error','arrival_frequency_relative']
    summary={'scope':'finite supplied controls and queries; no native admission or continuum certification',
             'config_sha256':sha(args.config),'input_sha256':{},'cases':[], 'settings':[]}
    for ti,tol in enumerate(tolerances):
        subset=[]
        for c in cases:
            p=run/(c['id']+'_t'+str(ti)+'.json');r=json.loads(p.read_text())
            assert r['binding']==meta and r['case']==c and r['tolerance']==tol
            tp=p.with_suffix('.npz');assert sha(tp)==r['trajectory_sha256']
            summary['input_sha256'][str(p)]=sha(p);summary['input_sha256'][str(tp)]=sha(tp)
            data=np.load(tp);assert data['state'].shape==(r['center']['saved_nodes'],8)
            assert np.isfinite(data['state']).all()
            item={'id':c['id'],'metric':c['metric'],'L':c['L'],'tolerance':tol,
                  **{k:r['center'][k] for k in metrics},
                  'tr':r['center']['tr'],'Z':r['center']['Z'],'logZ':r['center']['logZ'],
                  'reverse_relative':abs(r['reverse']['Z']/r['center']['Z']-1) if r['reverse'] else None,
                  'echo_Z':r['echo']['Z'] if r['echo'] else None}
            if ti==len(tolerances)-1:
                for k,limit in cfg['tight_limits'].items():
                    assert item[k]<=limit,(c['id'],k,item[k],limit)
                if item['reverse_relative'] is not None:
                    assert item['reverse_relative']<=cfg['reverse_limit']
            subset.append(item);summary['cases'].append(item)
        summary['settings'].append({'tolerance':tol,**{k:max(r[k] for r in subset) for k in metrics}})
    if len(tolerances)>1:
        changes=[]
        for c in cases:
            r=[next(x for x in summary['cases'] if x['id']==c['id'] and x['tolerance']==t) for t in tolerances]
            changes.append({'id':c['id'],'coarse_to_medium_Z_relative':abs(r[0]['Z']/r[1]['Z']-1),
                            'medium_to_tight_Z_relative':abs(r[1]['Z']/r[2]['Z']-1),
                            'coarse_to_medium_arrival_absolute':abs(r[0]['tr']-r[1]['tr']),
                            'medium_to_tight_arrival_absolute':abs(r[1]['tr']-r[2]['tr'])})
            assert changes[-1]['medium_to_tight_Z_relative']<=cfg['refinement_limit']
        summary['refinement']=changes
    summary['status']='PASS_FINITE_NUMERICAL_DIAGNOSTICS'
    with Path(args.output).open('x') as f:json.dump(summary,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':summary['status'],'rows':len(summary['cases']), 'settings':summary['settings']},indent=2))


if __name__=='__main__':main()
