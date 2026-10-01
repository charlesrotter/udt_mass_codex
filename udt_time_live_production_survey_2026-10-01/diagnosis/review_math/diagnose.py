"""Bounded independent arithmetic/metric-jet diagnostic; no producer imports."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'udt_time_live_production_survey_2026-10-01'
HERE = Path(__file__).resolve().parent

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def read(path):return json.loads(Path(path).read_text())

def weights(order,derivative):
    x=list(range(-order//2,order//2+1));n=len(x)
    a=[[Fraction(z)**p for z in x]+[Fraction((1 if derivative==1 else 2) if p==derivative else 0)] for p in range(n)]
    for c in range(n):
        pivot=next(r for r in range(c,n) if a[r][c])
        a[c],a[pivot]=a[pivot],a[c]
        scale=a[c][c];a[c]=[v/scale for v in a[c]]
        for r in range(n):
            if r!=c:
                scale=a[r][c];a[r]=[v-scale*u for v,u in zip(a[r],a[c])]
    w=[row[-1] for row in a]
    for p in range(n):assert sum(v*z**p for v,z in zip(w,x))==((1 if derivative==1 else 2) if p==derivative else 0)
    return np.asarray([np.longdouble(v.numerator)/v.denominator for v in w])

def time_derivative(h,t,order,k):
    delta=np.longdouble(t[1])-np.longdouble(t[0]);mid=len(t)//2
    out=np.zeros(h.shape[1:],dtype=np.longdouble)
    for j,c in enumerate(weights(order,k)):
        out+=c*(h[mid-order//2+j].astype(np.longdouble)-h[mid].astype(np.longdouble))
    return np.asarray(out/delta**k,dtype=np.float64)

def jets(h,t,L,order):
    g=h[len(t)//2];n=g.shape[0]
    d=np.empty(g.shape[:-2]+(4,4,4));dd=np.empty(g.shape[:-2]+(4,4,4,4))
    d[...,0,:,:]=time_derivative(h,t,order,1)
    dd[...,0,0,:,:]=time_derivative(h,t,order,2)
    k=2*np.pi*np.fft.fftfreq(n,d=L/n)
    f=np.fft.fftn(g,axes=(0,1,2));ft=np.fft.fftn(d[...,0,:,:],axes=(0,1,2))
    factors=[]
    for a in range(3):
        shape=[1]*g.ndim;shape[a]=n;factors.append(1j*k.reshape(shape))
    for a in range(3):
        d[...,a+1,:,:]=np.fft.ifftn(f*factors[a],axes=(0,1,2)).real
        dd[...,0,a+1,:,:]=dd[...,a+1,0,:,:]=np.fft.ifftn(ft*factors[a],axes=(0,1,2)).real
        for b in range(3):dd[...,a+1,b+1,:,:]=np.fft.ifftn(f*factors[a]*factors[b],axes=(0,1,2)).real
    return g,d,dd

def ricci(g,d,dd):
    """Separate contraction arrangement of original Christoffel-definition Ricci."""
    gi=np.linalg.inv(g)
    lo=np.empty_like(d);dlo=np.empty_like(dd)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                lo[...,a,b,c]=(d[...,b,a,c]+d[...,c,a,b]-d[...,a,b,c])/2
                for k in range(4):dlo[...,k,a,b,c]=(dd[...,k,b,a,c]+dd[...,k,c,a,b]-dd[...,k,a,b,c])/2
    ga=np.einsum('...ij,...jkl->...ikl',gi,lo,optimize=True)
    dga=np.einsum('...ij,...ajkl->...aikl',gi,dlo,optimize=True)
    dga-=np.einsum('...ij,...ajk,...klm->...ailm',gi,d,ga,optimize=True)
    r=np.einsum('...aamn->...mn',dga)-np.einsum('...nama->...mn',dga)
    r+=np.einsum('...amn,...bab->...mn',ga,ga,optimize=True)
    r-=np.einsum('...amb,...bna->...mn',ga,ga,optimize=True)
    assert np.isfinite(r).all()
    return r

def controls():
    times=2.49+np.arange(-4,5)*.0025;rows=[]
    for p in [(-1/3,2/3,2/3),(.2,.3,.5)]:
        h=np.zeros((9,4,4,4,4,4))
        for i,r in enumerate((1,*p)):h[...,i,i]=((-1 if i==0 else 1)*np.exp(2*r*(times-1)))[:,None,None,None]
        target=np.diag([sum(p)-sum(z*z for z in p),0,0,0])
        for order in [6,8]:
            r=ricci(*jets(h,times,2*np.pi,order));error=float(abs(r-target).max())
            assert error<2e-8
            rows.append(dict(control='harmonic_kasner',p=p,order=order,error=error,ricci_max=float(abs(r).max())))
    rate=.2;g=np.diag([-1,1.7,1.7,1.7]);d=np.zeros((4,4,4));dd=np.zeros((4,4,4,4))
    for i in range(1,4):d[0,i,i]=2*rate*g[i,i];dd[0,0,i,i]=4*rate**2*g[i,i]
    expected=np.diag([-3*rate**2,*([3*rate**2*1.7]*3)])
    error=float(abs(ricci(g,d,dd)-expected).max());assert error<1e-14
    rows.append(dict(control='analytic_exponential_FLRW_jets',error=error))
    return rows

def loaded(case):
    directory=BASE/'production_analysis'/case
    p=directory/'histories'/f'{case}_window2.npz';s=p.with_suffix('.sources.json');assembly=read(directory/'ASSEMBLY.json');source=read(s)
    digest=sha(p);assert digest==source['history_sha256']==assembly['output_sha256'][str(p)]
    assert sha(s)==assembly['output_sha256'][str(s)]
    with np.load(p,allow_pickle=False) as z:data={k:z[k] for k in z.files}
    assert data['g'].dtype==np.float64 and data['v'].dtype==np.float64
    assert np.array_equal(np.rint((data['times']-1)*3200).astype(int),source['ticks'])
    checkpoints={}
    for path,digest in source['source_sha256'].items():
        pth=Path(path);pth=ROOT/pth if not pth.is_absolute() else pth
        assert sha(pth)==digest
        if pth.name=='metadata.json':
            m=read(pth);assert m['eligible_for_resume'] and m['diagnostic'] is None
            assert pth.with_name('COMMITTED').read_text().strip()==sha(pth)
            payload=pth.with_name('state.npz');assert sha(payload)==m['payload_sha256']
            checkpoints[m['step']]=(payload,m['t'])
    assert sorted(checkpoints)==source['ticks']
    for j,tick in enumerate(source['ticks']):
        payload,t=checkpoints[tick]
        with np.load(payload,allow_pickle=False) as z:
            state=z['state'];assert np.array_equal(state[0],data['g'][j]) and np.array_equal(state[1],data['v'][j])
        assert t==data['times'][j]
    return data,dict(history=str(p.relative_to(ROOT)),sha256=sha(p),source_sha256=sha(s),all9_checkpoint_arrays_replayed=True)

def main():
    start=time.monotonic();frozen=read(BASE/'diagnosis/INITIAL_FREEZE.json')
    for p,h in frozen['sha256'].items():assert sha(ROOT/p)==h
    candidate=read(BASE/'production_analysis/postprocess/MATH_CANDIDATE.json')
    reports={}
    for p,h in candidate['result_sha256'].items():assert sha(p)==h;reports[read(p)['case']]=read(p)
    gate_rows=[]
    for dataset in candidate['datasets']:
        name=dataset['dataset'];a=reports[name+'_n24'];b=reports[name+'_n32']
        status=[]
        for order in ['6','8']:
            low=max(w['centers'][order]['common8_max'] for w in a['windows'])
            high=max(w['centers'][order]['common8_max'] for w in b['windows'])
            full=max(w['centers'][order]['ricci_max'] for r in [a,b] for w in r['windows'])
            expected=next(s for s in dataset['spatial'] if s['order']==int(order))
            passed=(low>=10*high or full<1e-8)
            assert passed==(expected['status']=='PASS') and low==expected['coarse_common8_max'] and high==expected['fine_common8_max'] and full==expected['all_points_both_meshes_max']
            status.append(passed)
        gate_rows.append(dict(dataset=name,spatial_pass=all(status),temporal_pass=dataset['temporal_status']=='PASS',status=dataset['status']))
    chosen=[d for d in candidate['datasets'] if d['status']!='PASS']
    chosen.append(next(d for d in candidate['datasets'] if d['dataset']=='oblique_a4_p0_r0'))
    rows=[];control=controls()
    print(json.dumps(dict(event='CONTROLS_PASS',gate_rows=len(gate_rows))),flush=True)
    for dataset in chosen:
        name=dataset['dataset'];fields={};tensors={};records={}
        for suffix in ['_n24','_n24_half','_n32']:
            case=name+suffix;data,binding=loaded(case);n=data['g'].shape[1];fields[suffix]={k:data[k][-1].copy() for k in ['g','v']}
            record=dict(binding=binding,shape=list(data['g'].shape),time=float(data['times'][4]),orders={})
            for order in [6,8]:
                r=ricci(*jets(data['g'],data['times'],float(data['period']),order));tensors[(suffix,order)]=r
                common=r[::n//8,::n//8,::n//8]
                fullmax=float(abs(r).max());commonmax=float(abs(common).max())
                expected=reports[case]['windows'][2]['centers'][str(order)]
                record['orders'][str(order)]=dict(all_points_max=fullmax,common8_max=commonmax,report_all_max_absolute_difference=abs(fullmax-expected['ricci_max']),report_common_max_absolute_difference=abs(commonmax-expected['common8_max']),argmax=list(map(int,np.unravel_index(abs(r).argmax(),r.shape))))
                assert abs(fullmax-expected['ricci_max'])<2e-10 and abs(commonmax-expected['common8_max'])<2e-10
            record['sixth_eighth_tensor_difference']=float(abs(tensors[(suffix,6)]-tensors[(suffix,8)]).max())
            record['saved_v_vs_eighth_metric_time_derivative']=float(abs(data['v'][4]-time_derivative(data['g'],data['times'],8,1)).max())
            records[suffix]=record
            del data
        temporal={k:float(abs(fields['_n24'][k]-fields['_n24_half'][k]).max()) for k in ['g','v']}
        assert temporal==dataset['final_time_refinement']
        tensor_difference={str(o):float(abs(tensors[('_n24',o)]-tensors[('_n24_half',o)]).max()) for o in [6,8]}
        rows.append(dict(dataset=name,original_status=dataset['status'],temporal=temporal,coarse_half_curvature_tensor_difference=tensor_difference,centers=records))
        print(json.dumps(dict(event='DATASET_DONE',dataset=name,temporal=temporal,tensor_difference=tensor_difference)),flush=True)
    all_windows=[w for r in reports.values() for w in r['windows']]
    result=dict(status='DIAGNOSTIC_CHECKS_COMPLETE',reviewer_context='/root/survey_completion_math',startup='Parent startup/synchronization attributed; own branch/hash/status and scoped instructions checked.',model='same inherited model; not cross-model',prior_exposure='13 known flags and original reports; diagnosis frozen in PLAN.md before direct-array computations.',independence='Own rational stencil generation, extended-precision time accumulation and separately arranged Ricci contraction. Shared saved fields, NumPy FFT mathematics and defining Christoffel Ricci. No independent general-data time integrator.',numpy=np.__version__,controls=control,gate_rows=gate_rows,direct_array_rows=rows,report_coverage=dict(cases=len(reports),windows=len(all_windows),original_ricci_max=max(w['original']['ricci_max'] for w in all_windows),late_H_max=max(a['hamiltonian_abs_max'] for w in all_windows if 'late_adm' in w for a in w['late_adm']),late_M_max=max(max(a['momentum_abs_max_by_component']) for w in all_windows if 'late_adm' in w for a in w['late_adm']),late_harmonic_max=max(a['harmonic_vector_abs_max'] for w in all_windows if 'late_adm' in w for a in w['late_adm'])),omissions='Original 5-point15-slice and late ADM coverage is authenticated report coverage, not a full234 replay. Direct Ricci only late centers; no unsaved-gap or continuum bounds.',source_sha256=sha(__file__),initial_freeze_sha256=sha(BASE/'diagnosis/INITIAL_FREEZE.json'),seconds=time.monotonic()-start)
    with (HERE/'DIAGNOSTIC.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],datasets=len(rows),seconds=result['seconds'])),flush=True)

if __name__=='__main__':main()
