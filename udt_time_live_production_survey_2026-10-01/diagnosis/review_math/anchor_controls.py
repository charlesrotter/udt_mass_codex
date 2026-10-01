"""Spatially varying geometry controls and scoped reused independent ADM anchors."""
import json
import sys
from pathlib import Path
import numpy as np
from diagnose import ROOT,BASE,HERE,sha,jets,ricci,loaded
sys.path.insert(0,str(BASE/'review/math'))
from check_survey import adm_row
from check_constraints import selftest

def main():
    n=16;L=2*np.pi;t=2.49+np.arange(-4,5)*.0025
    x,y,z=np.meshgrid(*([L*np.arange(n)/n]*3),indexing='ij')
    h=np.zeros((9,n,n,n,4,4));h[...,0,0]=-1
    J=np.broadcast_to(np.eye(3),(n,n,n,3,3)).copy()
    J[...,0,:]+=(.05*np.cos(x+y+z))[...,None]
    h[...,1:,1:]=np.einsum('...ki,...kj->...ij',J,J)
    flat_error=float(abs(ricci(*jets(h,t,L,8))).max());assert flat_error<2e-12
    h[:]=0;h[...,0,0]=-1;h[...,1,1]=1;h[...,3,3]=1
    f=1+.1*np.cos(x);h[...,2,2]=f*f
    expected=np.zeros((n,n,n,4,4));expected[...,1,1]=.1*np.cos(x)/f;expected[...,2,2]=.1*f*np.cos(x)
    curved=ricci(*jets(h,t,L,8));curved_error=float(abs(curved-expected).max());assert curved_error<2e-12 and abs(curved).max()>.1
    rows=[]
    for name in ['axial_a5','oblique_a5_p0_r2','oblique_a5_p3_r0']:
        for suffix in ['_n24_half','_n32']:
            case=name+suffix;data,binding=loaded(case)
            r=adm_row(data['g'][-1],data['v'][-1],float(data['period']))
            expected=json.loads((BASE/'review/math/cases'/f'{case}.json').read_text())['windows'][2]['late_adm'][-1]
            for key in ['hamiltonian_abs_max','momentum_abs_max_by_component','harmonic_vector_abs_max']:assert r[key]==expected[key]
            assert r['status']=='PASS'
            rows.append(dict(case=case,time=float(data['times'][-1]),binding=binding,adm=r))
    result=dict(status='PASS',source_sha256=sha(__file__),own_ricci_code_sha256=sha(HERE/'diagnose.py'),spatial_analytic_controls=dict(n=n,offdiagonal_periodic_flat_pullback_error=flat_error,curved_warped_metric_error=curved_error,curved_ricci_max=float(abs(curved).max())),reused_ADM_controls=selftest(),saved_ADM_rows=rows,attribution='Fresh execution of TDS/TPP independently authored ADM methods via unchanged TPS1 adapter; same implementation as original reports, therefore replay/regression, not a new independent ADM implementation.',method_sources={str(p.relative_to(ROOT)):sha(p) for p in [BASE/'review/math/check_survey.py',ROOT/'udt_time_live_production_preparation_2026-10-01/review/math/check_saved_data.py',ROOT/'udt_three_spatial_smoke_2026-10-01/review/data/check_constraints.py',ROOT/'udt_three_spatial_smoke_2026-10-01/review/data/check_harmonic.py']})
    with (HERE/'ANCHOR_CONTROLS.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status='PASS',flat_error=flat_error,curved_error=curved_error,saved_ADM_cases=len(rows))),flush=True)

if __name__=='__main__':main()
