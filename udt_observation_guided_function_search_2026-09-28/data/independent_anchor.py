#!/usr/bin/env python3
"""Same-context, different-implementation numerical anchors; not independent review.

Does not import fit_empirical. Re-parses source and uses dense symmetric solves,
explicit interval polynomial spline construction, and adaptive quadrature.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[key]='2'
from pathlib import Path
import datetime as dt
import gzip
import hashlib
import json
import resource
resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
import numpy as np
from scipy.linalg import solve
from scipy.integrate import quad
from scipy.stats import chi2

P=Path(__file__).resolve().parent
O=P/'results'
K=5/np.log(10.)


def cardinal(knots, points):
    """Solve coefficients for four local polynomial coefficients on each interval."""
    intervals=len(knots)-1; n=4*intervals
    eq=[];rhs=[]
    for i in range(intervals):
        h=knots[i+1]-knots[i]
        for t,j in [(0.,i),(h,i+1)]:
            row=np.zeros(n);row[4*i:4*i+4]=[1,t,t*t,t*t*t]
            target=np.zeros(len(knots));target[j]=1
            eq.append(row);rhs.append(target)
    for i in range(intervals-1):
        h=knots[i+1]-knots[i]
        row=np.zeros(n);row[4*i:4*i+4]=[0,1,2*h,3*h*h];row[4*(i+1)+1]=-1
        eq.append(row);rhs.append(np.zeros(len(knots)))
        row=np.zeros(n);row[4*i:4*i+4]=[0,0,2,6*h];row[4*(i+1)+2]=-2
        eq.append(row);rhs.append(np.zeros(len(knots)))
    row=np.zeros(n);row[2]=2;eq.append(row);rhs.append(np.zeros(len(knots)))
    h=knots[-1]-knots[-2];row=np.zeros(n);row[-4:]=[0,0,2,6*h]
    eq.append(row);rhs.append(np.zeros(len(knots)))
    coef=solve(np.array(eq),np.array(rhs))
    out=[]
    for x in points:
        i=int(np.clip(np.searchsorted(knots,x,side='right')-1,0,intervals-1))
        t=x-knots[i];out.append(np.array([1,t,t*t,t*t*t])@coef[4*i:4*i+4])
    return np.array(out)


def main():
    target=O/'independent_anchor.json'
    if target.exists(): raise RuntimeError('Refuse overwrite')
    d=np.genfromtxt(P/'raw/Pantheon+SH0ES.dat',names=True,dtype=None,encoding='utf8')
    rawbytes=gzip.decompress((P/'raw/Pantheon+SH0ES_STAT+SYS.cov.gz').read_bytes())
    vals=np.fromstring(rawbytes.decode(),sep=' ');n=int(vals[0]);raw=vals[1:].reshape(n,n)
    mask=(d['IS_CALIBRATOR']==0)&(d['zHD']>.023);ids=np.flatnonzero(mask)
    C=((raw+raw.T)/2)[np.ix_(ids,ids)]
    z=d['zHD'][mask];zh=d['zHEL'][mask];m=d['m_b_corr'][mask];x=np.log1p(z)
    y=m-5*np.log10((1+zh)*x)
    published=json.loads((O/'full_fits.json').read_text())
    checks={}
    for degree in range(5):
        f=f'F{degree}'
        if degree<4:
            X=np.column_stack([np.ones(len(x))]+[K*x**j for j in range(1,degree+1)])
        else:X=cardinal(np.log1p(published[f]['knots_z']),x)
        ci=solve(C,np.column_stack([y,X]),assume_a='sym')
        info=X.T@ci[:,1:];beta=solve(info,X.T@ci[:,0],assume_a='sym')
        vc=solve(info,np.eye(len(beta)),assume_a='sym')
        r=y-X@beta;cr=solve(C,r,assume_a='sym');score=float(r@cr)
        bdiff=float(np.max(np.abs(beta-published[f]['beta'])))
        cdiff=float(np.max(np.abs(vc-published[f]['parameter_covariance'])))
        qdiff=abs(score-published[f]['chi2'])
        backward=float(np.linalg.norm(C@cr-r)/(np.linalg.norm(C,ord=np.inf)*np.linalg.norm(cr)+np.linalg.norm(r)))
        assert bdiff<2e-9 and cdiff<2e-10 and qdiff<2e-8 and backward<2e-14
        checks[f]={'beta_max_abs_difference':bdiff,'covariance_max_abs_difference':cdiff,
                   'chi2':score,'chi2_abs_difference':qdiff,'original_solve_scaled_backward_error':backward}
        if f=='F2':
            train=np.array([int(hashlib.sha256(s.encode()).hexdigest(),16)%5!=0 for s in d['CID'][mask]])
            T=np.flatnonzero(train);V=np.flatnonzero(~train);Ctt=C[np.ix_(T,T)];Cvt=C[np.ix_(V,T)]
            gt=solve(Ctt,np.column_stack([y[T],X[T]]),assume_a='sym')
            inf=X[T].T@gt[:,1:];bt=solve(inf,X[T].T@gt[:,0],assume_a='sym')
            covbt=solve(inf,np.eye(3),assume_a='sym')
            W=solve(Ctt,Cvt.T,assume_a='sym').T
            e=y[V]-X[V]@bt-W@(y[T]-X[T]@bt)
            B=X[V]-W@X[T];predcov=C[np.ix_(V,V)]-W@Cvt.T+B@covbt@B.T
            q=float(e@solve(predcov,e,assume_a='sym'))
            given=[v for v in json.loads((O/'validation.json').read_text()) if v['family']=='F2'][0]
            err=abs(q-given['conditional_predictive_chi2']);assert err<2e-8
            checks['F2_validation']={'conditional_predictive_chi2':q,'difference':err,'n_validation':len(V)}
    om=published['F5']['beta'][1];A=published['F5']['beta'][0]
    values=np.array([quad(lambda t:1/np.sqrt(om*(1+t)**3+1-om),0,zz,epsabs=2e-13,epsrel=2e-13)[0] for zz in z])
    r=m-A-5*np.log10((1+zh)*values);q=float(r@solve(C,r,assume_a='sym'))
    assert abs(q-published['F5']['chi2'])<2e-8
    checks['F5_adaptive_quadrature']={'chi2':q,'difference':abs(q-published['F5']['chi2']),
        'anchors':{str(zz):quad(lambda t:1/np.sqrt(om*(1+t)**3+1-om),0,zz,epsabs=2e-13,epsrel=2e-13)[0] for zz in [.1,.5,1,2]}}
    # Explicit likelihood contrast, conditional on the frozen processed-data Gaussian model.
    contrasts={}
    for lo,hi in [('F0','F1'),('F1','F2'),('F2','F3')]:
        delta=published[lo]['chi2']-published[hi]['chi2'];df=published[hi]['p']-published[lo]['p']
        contrasts[f'{lo}_to_{hi}']={'delta_chi2':delta,'extra_parameters':df,'nominal_nested_p':float(chi2.sf(delta,df))}
    diag=np.sqrt(np.diag((raw+raw.T)/2));dif=diag-d['m_b_corr_err_DIAG']
    checks['release_schema_diagnostic']={'n_release':n,'distinct_CID_keys':len(set(d['CID'])),
        'all_rows_sigma_vs_table_max_abs':float(np.max(abs(dif))),
        'primary_sigma_vs_table_max_abs':float(np.max(abs(dif[mask]))),
        'primary_sigma_vs_table_median_difference':float(np.median(dif[mask])),
        'interpretation':'Published plotting-error column is not numerically the covariance diagonal; it was never used for fitting. Issue6/13 retained, unresolved explanation.'}
    result={'status':'PASS_WITH_RELEASE_CAVEATS','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'independence':'same author context, separate implementation; no import/reuse of fitter functions; not separate-context review',
        'raw_covariance_sha256':hashlib.sha256(rawbytes).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checks':checks,'nested_contrasts':contrasts,
        'not_checked':'Raw-photometry likelihood, physical optical transfer, unknown covariance errors, native-law derivation, parameter identifiability beyond this empirical model.'}
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
