"""OEV1 independent metric quadrature/affine checker; no parent code imports."""
from pathlib import Path
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import argparse, copy, datetime, hashlib, json, platform, sys
import mpmath as mp
import numpy as np

mp.mp.dps = 60
COUNT = {'scalar_roots': 0, 'scalar_integrals': 0, 'trajectory_samples': 0}
CACHE = {}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def count(kind):
    COUNT[kind] += 1
    if COUNT['scalar_roots'] + COUNT['scalar_integrals'] > 1000:
        raise RuntimeError('FROZEN_ANCHOR_BUDGET_EXCEEDED')

def m(value):
    return mp.mpf(str(value))

def scale(kind, t):
    if kind == 'flat':
        return mp.mpf(1)
    return 1 + t**{'quadratic': 2, 'cubic': 3}[kind]

def eta(kind, t):
    if kind == 'flat':
        return t
    if kind == 'quadratic':
        return mp.atan(t)
    r = mp.sqrt(3)
    return mp.log(1+t)/3-mp.log(t*t-t+1)/6+mp.atan((2*t-1)/r)/r+mp.pi/(6*r)

def primitive(kind, t):
    return t if kind == 'flat' else t + t**({'quadratic': 3, 'cubic': 4}[kind]) / {'quadratic': 3, 'cubic': 4}[kind]

def horizon(kind):
    return mp.inf if kind == 'flat' else (mp.pi/2 if kind == 'quadratic' else 2*mp.pi/(3*mp.sqrt(3)))

def arrival(kind, te, distance):
    te, distance = m(te), abs(m(distance))
    key = (kind, str(te), str(distance), mp.mp.dps)
    if key in CACHE:
        return CACHE[key]
    if kind == 'cubic' and te <= -1:
        raise ValueError('OUTSIDE_SUPPLIED_DOMAIN')
    target = eta(kind, te) + distance
    if target >= horizon(kind):
        raise ValueError('NO_FINITE_RECEPTION_ANALYTIC')
    count('scalar_roots')
    if kind == 'flat':
        result = te + distance
    elif kind == 'quadratic':
        result = mp.tan(target)
    else:
        lo, hi = te, max(mp.mpf(1), te+distance)
        while eta(kind, hi) < target:
            hi = 2*hi+1
        for _ in range(230):
            middle = (lo+hi)/2
            if eta(kind, middle) < target:
                lo = middle
            else:
                hi = middle
            if hi-lo < mp.mpf('1e-49') * (1+abs(middle)):
                break
        result = (lo+hi)/2
    count('scalar_integrals')
    integral = mp.quad(lambda t: 1/scale(kind,t), [te, (te+result)/2, result])
    if abs(integral-distance) >= mp.mpf('1e-45'):
        raise AssertionError(('DIRECT_QUADRATURE_DISAGREEMENT', kind, str(abs(integral-distance))))
    CACHE[key] = result
    return result

def endpoint_errors(kind, endpoint, expected_te, expected_distance):
    assert endpoint['te'] == expected_te and endpoint['distance'] == expected_distance
    te, distance = m(endpoint['te']), m(endpoint['distance'])
    tr = arrival(kind, te, distance)
    ae, ar = scale(kind, te), scale(kind, tr)
    expected = {'tr': tr, 'lambda_end': (primitive(kind,tr)-primitive(kind,te))/ae,
                'kt_end': ae/ar, 'kx_end': mp.sign(distance)*ae/ar**2,
                'Z': ar/ae, 'logZ': mp.log(ar/ae)}
    errors = {}
    for key, value in expected.items():
        denom = abs(value) if key in ('kt_end','kx_end','Z') else 1+abs(value)
        errors[key] = float(abs(m(endpoint[key])-value)/denom)
    return errors, expected

def trajectory_errors(kind, states, lambdas):
    maxima = dict(affine=0., conformal=0., kt=0., kx=0., transport=0., null=0.)
    for row, lam in zip(states,lambdas):
        COUNT['trajectory_samples'] += 1
        t,x,kt,kx = map(m,row[:4])
        a = scale(kind,t)
        errors = {'affine': abs(m(lam)-primitive(kind,t))/(1+abs(m(lam))),
                  'conformal': abs(x-eta(kind,t))/(1+abs(x)),
                  'kt': abs(kt*a-1), 'kx': abs(kx*a*a-1),
                  'null': abs(-kt*kt+a*a*kx*kx)/(kt*kt+a*a*kx*kx)}
        r = mp.log(a)
        matrix = [mp.cosh(r), -mp.sinh(r), -mp.sinh(r)/a, mp.cosh(r)/a]
        errors['transport'] = max(abs(m(x)-v)/(1+abs(v)) for x,v in zip(row[4:],matrix))
        for key,value in errors.items():
            maxima[key] = max(maxima[key],float(value))
    return maxima

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('package'); ap.add_argument('run'); ap.add_argument('output')
    args = ap.parse_args()
    package,run,out = Path(args.package),Path(args.run),Path(args.output)
    freeze = json.loads((package/'numerics/FREEZE.json').read_text())
    for path,digest in freeze['sha256'].items():
        assert sha(path)==digest, ('PARENT_FROZEN_SOURCE_DRIFT',path)
    ownfreeze=json.loads((Path(__file__).parent/'INDEPENDENT_FREEZE.json').read_text())
    for path,digest in ownfreeze['sha256'].items():
        assert sha(path)==digest,('REVIEWER_FREEZE_DRIFT',path)
    cfg=json.loads((package/'numerics/config.json').read_text())
    meta=json.loads((run/'metadata.json').read_text())
    assert not meta['smoke']
    assert meta['config_sha256']==sha(package/'numerics/config.json')
    assert meta['code_sha256']==sha(package/'numerics/evaluate.py')
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'method':'independent metric primitive/root/direct quadrature and affine/invariant/transport checks; no parent imports',
            'versions':{'python':sys.version,'platform':platform.platform(),'mpmath':mp.__version__,'numpy':np.__version__},
            'precision_dps':60,'input_sha256':{},'rows':[],'availability':[],
            'failures':[],'limits':'finite floating agreement; not interval certification, native admission, empirical confirmation, or global numerical proof'}
    mutation_source=None
    for case in cfg['cases']:
        kind,L=case['metric'],case['L']
        first= m(L) < horizon(kind)
        echo = 2*m(L) < horizon(kind)
        assert first and (not case.get('echo') or echo)
        assert all(eta(kind,m(h))+m(L)<horizon(kind) and eta(kind,-m(h))+m(L)<horizon(kind) for h in cfg['emission_steps'])
        report['availability'].append({'id':case['id'],'first':first,'immediate_echo':echo,
                                       'echo_evaluated':case.get('echo',False),'method':'analytic positive conformal integral; not failed numerical solve'})
        for ti,tol in enumerate(cfg['tolerances']):
            rp=run/(case['id']+'_t'+str(ti)+'.json');tp=rp.with_suffix('.npz')
            r=json.loads(rp.read_text()); data=np.load(tp)
            assert r['case']==case and r['tolerance']==tol and r['binding']==meta
            assert sha(tp)==r['trajectory_sha256']
            report['input_sha256'][str(rp)]=sha(rp);report['input_sha256'][str(tp)]=sha(tp)
            states,lambdas=data['state'],data['lambda']
            assert states.shape==(r['center']['saved_nodes'],8) and lambdas.shape==(len(states),)
            assert np.isfinite(states).all() and np.isfinite(lambdas).all()
            assert np.all(np.diff(lambdas)>0) and lambdas[0]==0
            assert np.allclose(states[0], [0,0,1,1,1,0,0,1],rtol=0,atol=0)
            threshold=max(1e-9,500*tol)
            ce,expected=endpoint_errors(kind,r['center'],0.,L)
            trajectories=trajectory_errors(kind,states,lambdas)
            endpoints=[{'role':'center','errors':ce}]
            exact_derivatives=[]
            saved_derivatives=[]
            for i,h in enumerate(cfg['emission_steps']):
                perturb=r['perturbations'][i]
                assert perturb['h']==h
                errors_minus,exminus=endpoint_errors(kind,perturb['minus'],-h,L)
                errors_plus,explus=endpoint_errors(kind,perturb['plus'],h,L)
                endpoints += [{'role':'minus_'+str(h),'errors':errors_minus},{'role':'plus_'+str(h),'errors':errors_plus}]
                exact_derivatives.append((explus['tr']-exminus['tr'])/(2*m(h)))
                saved_derivatives.append((perturb['plus']['tr']-perturb['minus']['tr'])/(2*h))
                assert saved_derivatives[-1]==perturb['arrival_derivative']
            rich=(4*exact_derivatives[1]-exact_derivatives[0])/3
            savedrich=(4*saved_derivatives[1]-saved_derivatives[0])/3
            assert savedrich==r['center']['arrival_derivative_richardson']
            derivative_error=float(abs(m(savedrich)/expected['Z']-1))
            derivative_truncation=float(abs(rich/expected['Z']-1))
            if r['reverse']:
                reverse,_=endpoint_errors(kind,r['reverse'],0.,-L)
                endpoints.append({'role':'reverse','errors':reverse})
            else:
                assert not case.get('reverse')
            echo_exact=None
            if r['echo']:
                ee,execho=endpoint_errors(kind,r['echo'],r['center']['tr'],-L)
                endpoints.append({'role':'echo_given_saved_first_reception','errors':ee})
                t2=arrival(kind,0,2*m(L))
                echo_exact=scale(kind,t2)/scale(kind,expected['tr'])
                ee['full_echo_ratio']=float(abs(m(r['echo']['Z'])/echo_exact-1))
            else:
                assert not case.get('echo')
            maximum=max([*trajectories.values(),*(value for e in endpoints for value in e['errors'].values())])
            success=maximum<=threshold and derivative_error<=2e-5
            if not success:
                report['failures'].append({'id':case['id'],'ti':ti,'maximum':maximum,'threshold':threshold,'derivative_error':derivative_error})
            log_error=m(r['center']['logZ'])-expected['logZ']
            item={'id':case['id'],'metric':kind,'L':L,'tolerance':tol,'threshold':threshold,'pass':success,
                  'endpoint_errors':endpoints,'trajectory_errors':trajectories,
                  'arrival_derivative_relative_error':derivative_error,
                  'exact_ladder_richardson_relative_truncation':derivative_truncation,
                  'frequency_Z_expected':mp.nstr(expected['Z'],45),'arrival_t_expected':mp.nstr(expected['tr'],45),
                  'logZ_absolute_error':float(abs(log_error)),
                  'quadratic_extraction_error':float(abs(2*log_error/m(L)**2)),
                  'cubic_extraction_error':float(abs(log_error/m(L)**3)) if kind=='cubic' else None,
                  'echo_Z_expected':mp.nstr(echo_exact,45) if echo_exact is not None else None}
            report['rows'].append(item)
            if case['id']=='quadratic_1' and ti==2:
                mutation_source=(kind,copy.deepcopy(r['center']),L,threshold)
    report['precision_repeats']=[]
    for kind,L in [('flat',1.0),('quadratic',cfg['cases'][6]['L']),('cubic',cfg['cases'][-1]['L'])]:
        original=arrival(kind,0,L)
        with mp.workdps(90):
            repeated=arrival(kind,0,L)
            error=abs(original-repeated)/(1+abs(repeated))
        assert error<mp.mpf('1e-45')
        report['precision_repeats'].append({'metric':kind,'L':L,'relative_change':float(error)})
    kind,original,L,threshold=mutation_source
    clean,_=endpoint_errors(kind,original,0.,L)
    assert max(clean.values())<=threshold
    catches=[]
    wrong=copy.deepcopy(original);wrong['kt_end']=1/wrong['kt_end'];wrong['Z']=1/wrong['Z'];wrong['logZ']=-wrong['logZ']
    errors,_=endpoint_errors(kind,wrong,0.,L)
    catches.append({'mutation':'invert_nonflat_receive_frequency','guard':'kt_end/Z/logZ against original metric','rejected':max(errors.values())>threshold,'maximum_error':max(errors.values())})
    wrong=copy.deepcopy(original);wrong['kx_end']=-wrong['kx_end']
    errors,_=endpoint_errors(kind,wrong,0.,L)
    catches.append({'mutation':'reverse_spatial_tangent_on_fixed_branch','guard':'signed metric momentum','rejected':errors['kx_end']>threshold,'maximum_error':errors['kx_end']})
    wrong=copy.deepcopy(original);wrong['tr']+=0.01
    errors,_=endpoint_errors(kind,wrong,0.,L)
    catches.append({'mutation':'move_reception_off_incidence','guard':'independent null-incidence root','rejected':errors['tr']>threshold,'maximum_error':errors['tr']})
    assert all(c['rejected'] for c in catches)
    report['catch_proofs']=catches
    report['counts']=COUNT
    report['status']='PASS_INDEPENDENT_FINITE_METRIC_CHECKS' if not report['failures'] else 'FAIL_INDEPENDENT_FINITE_METRIC_CHECKS'
    with out.open('x') as f:
        json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':report['status'],'rows':len(report['rows']),'counts':COUNT,'failures':report['failures'],'catch_proofs':catches},indent=2))
    return 0 if not report['failures'] else 1

if __name__=='__main__':
    sys.exit(main())
