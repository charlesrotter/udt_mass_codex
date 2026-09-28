#!/usr/bin/env python3
"""Frozen empirical positive-distance shapes, with full covariance and exposure labels.

All families are FREE/IMPORTED empirical controls. No native UDT equation is fitted.
"""
import os
for key in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[key] = '2'
os.environ.setdefault('MPLCONFIGDIR', '/tmp/udt_function_data_mpl')
from pathlib import Path
import csv
import datetime as dt
import gzip
import hashlib
import json
import platform
import resource
import time
resource.setrlimit(resource.RLIMIT_AS, (3*1024**3, 3*1024**3))
import numpy as np
import scipy
from scipy import linalg as la
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from scipy.stats import chi2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results'
K = 5/np.log(10.)  # Mathematical magnitude/log conversion, not a physics constant.
KN = np.log1p([.001,.1,.3,.6,1.,2.3])  # FREE empirical representation.
FAMILIES = ['F0','F1','F2','F3','F4','F5']
GQ = {n:np.polynomial.legendre.leggauss(n) for n in [64,128]}


def js(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, np.generic): return x.item()
    raise TypeError(type(x).__name__)


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, default=js, allow_nan=False)+'\n')


def table(path, rows):
    with path.open('w') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
        w.writeheader(); w.writerows(rows)


def load_release():
    with (ROOT/'raw/Pantheon+SH0ES.dat').open() as f:
        fields=f.readline().split()
        rows=[dict(zip(fields,line.split())) for line in f if line.strip()]
    req=['zHD','zHEL','m_b_corr','IS_CALIBRATOR','m_b_corr_err_DIAG']
    data={k:np.array([float(r[k]) for r in rows]) for k in req}
    data['CID']=np.array([r['CID'] for r in rows])
    data['IDSURVEY']=np.array([int(r['IDSURVEY']) for r in rows])
    with gzip.open(ROOT/'raw/Pantheon+SH0ES_STAT+SYS.cov.gz','rt') as f:
        n=int(f.readline()); cov=np.loadtxt(f).reshape(n,n)
    assert len(rows)==n and np.all(np.isfinite(cov))
    assert all(np.all(np.isfinite(data[k])) for k in req)
    return data,cov


def design(family,x,knots=KN,derivative=0):
    if family=='F4':
        return CubicSpline(knots,np.eye(len(knots)),bc_type='natural')(x,nu=derivative)
    degree=int(family[-1]); ans=np.zeros((len(x),degree+1))
    if derivative==0: ans[:,0]=1
    for power in range(1,degree+1):
        if power>=derivative:
            factor=1
            for j in range(derivative): factor*=power-j
            ans[:,power]=K*factor*x**(power-derivative)
    return ans


def lcdm_integral(z,om,n=64):
    nodes,weights=GQ[n]
    t=z[:,None]*(nodes+1)/2
    h=(1+t)**3-1
    e2=1+om*h
    integral=z/2*(e2**(-.5)@weights)
    deriv=-z/4*(h*e2**(-1.5)@weights)
    return integral,deriv


def fit(family,z,zhel,y,cov,knots=KN):
    n=len(z); x=np.log1p(z)
    cf=la.cho_factor(cov,lower=True,check_finite=True)
    L=np.tril(cf[0]); base=K*np.log((1+zhel)*x)
    solve=lambda a:la.cho_solve(cf,a,check_finite=False)
    if family!='F5':
        X=design(family,x,knots)
        Xw=la.solve_triangular(L,X,lower=True,check_finite=False)
        yw=la.solve_triangular(L,y-base,lower=True,check_finite=False)
        beta,_,rank,singular=la.lstsq(Xw,yw,lapack_driver='gelsd')
        if rank!=X.shape[1]: raise RuntimeError('rank deficient design')
        q,r=la.qr(Xw,mode='economic')
        invr=la.solve_triangular(r,np.eye(r.shape[0]))
        vc=invr@invr.T
        pred=base+X@beta
        optimization=None
    else:
        one=np.ones(n); ci1=solve(one); den=one@ci1
        def evaluate(om):
            distance,_=lcdm_integral(z,om)
            base5=K*np.log((1+zhel)*distance)
            A=ci1@(y-base5)/den
            residual=y-base5-A
            return residual@solve(residual),A,base5
        opt=minimize_scalar(lambda om:evaluate(om)[0],bounds=(0,1),method='bounded',options={'xatol':1e-10})
        if not opt.success: raise RuntimeError('F5 optimization failed')
        _,A,base5=evaluate(opt.x); beta=np.array([A,opt.x]); pred=base5+A
        dist,dd= lcdm_integral(z,opt.x)
        X=np.column_stack([one,K*dd/dist])
        Xw=la.solve_triangular(L,X,lower=True,check_finite=False)
        singular=la.svdvals(Xw); rank=np.linalg.matrix_rank(Xw)
        vc=la.inv(Xw.T@Xw)
        dist128,_=lcdm_integral(z,opt.x,n=128)
        optimization={'success':opt.success,'nfev':opt.nfev,'bound_contact':bool(min(opt.x,1-opt.x)<1e-6),
                      'max_quadrature_magnitude_difference':float(np.max(np.abs(K*np.log(dist128/dist)))),
                      'uncertainty':'local Jacobian information approximation'}
    residual=y-pred; cir=solve(residual); original=float(residual@cir)
    white=la.solve_triangular(L,residual,lower=True,check_finite=False)
    p=len(beta); dof=n-p
    sigma=np.sqrt(np.diag(vc)); corr=vc/np.outer(sigma,sigma)
    info=Xw.T@Xw; score=X.T@cir
    normscore=float(np.max(np.abs(score)/np.sqrt(np.diag(info))))
    summary={'family':family,'n':n,'p':p,'dof':dof,'beta':beta,'sigma':sigma,
             'parameter_covariance':vc,'parameter_correlation':corr,'chi2':original,
             'chi2_whitened':float(white@white),'quadratic_agreement_abs':abs(original-white@white),
             'chi2_reduced':original/dof,'p_upper':float(chi2.sf(original,dof)),
             'p_lower':float(chi2.cdf(original,dof)),
             'aicc_without_common_constant':original+2*p+2*p*(p+1)/(n-p-1),
             'bic_without_common_constant':original+p*np.log(n),
             'magnitude_rms':float(np.sqrt(np.mean(residual**2))),
             'rank':rank,'whitened_design_condition':float(singular[0]/singular[-1]),
             'score_over_information_sqrt_max':normscore,'optimization':optimization}
    if family=='F4': summary['knots_z']=np.expm1(knots)
    return {'summary':summary,'beta':beta,'vc':vc,'pred':pred,'residual':residual,
            'X':X,'knots':knots,'cf':cf}


def predict(family,z,zhel,fitres):
    b=fitres['beta'];x=np.log1p(z)
    if family=='F5':
        f,df=lcdm_integral(z,b[1]);pred=b[0]+K*np.log((1+zhel)*f)
        X=np.column_stack([np.ones(len(x)),K*df/f])
    else:
        X=design(family,x,fitres['knots']); pred=K*np.log((1+zhel)*x)+X@b
    return pred,X


def validate(family,z,zhel,y,cov,train):
    val=~train; it=np.flatnonzero(train);iv=np.flatnonzero(val)
    Ctt=cov[np.ix_(it,it)];Cvt=cov[np.ix_(iv,it)];Cvv=cov[np.ix_(iv,iv)]
    res=fit(family,z[train],zhel[train],y[train],Ctt)
    pv,Xv=predict(family,z[val],zhel[val],res)
    W=la.cho_solve(res['cf'],Cvt.T,check_finite=False).T
    conditional=y[val]-pv-W@res['residual']
    S=Cvv-W@Cvt.T;B=Xv-W@res['X']
    V=S+B@res['vc']@B.T
    V=(V+V.T)/2
    vf=la.cho_factor(V,lower=True)
    score=float(conditional@la.cho_solve(vf,conditional))
    logdet=float(2*np.sum(np.log(np.diag(vf[0]))))
    out={'family':family,'n_train':len(it),'n_validation':len(iv),
         'train_fit':res['summary'],'conditional_predictive_chi2':score,
         'conditional_predictive_dof':len(iv),'conditional_predictive_p_upper':float(chi2.sf(score,len(iv))),
         'conditional_predictive_p_lower':float(chi2.cdf(score,len(iv))),
         'conditional_predictive_minus2logpdf':score+logdet+len(iv)*np.log(2*np.pi),
         'cross_covariance_max_abs':float(np.max(np.abs(Cvt))),
         'uncertainty':'exact linear Gaussian' if family!='F5' else 'local Jacobian approximation',
         'exposure':'same-release consistency split; not blind independent confirmation'}
    table(OUT/f'validation_residuals_{family}.tsv',[
        {'primary_index':int(j),'conditional_residual_mag':float(e),'predictive_sigma_marginal_mag':float(s)}
        for j,e,s in zip(iv,conditional,np.sqrt(np.diag(V)))])
    return out


def curves(family,z,fr):
    x=np.log1p(z);xr=np.log1p(.1);b=fr['beta'];vc=fr['vc']
    if family!='F5':
        X=design(family,x,fr['knots']);Xr=design(family,np.array([xr]),fr['knots'])[0]
        B=(X-Xr)/K
        logfr=np.log(x/xr)+B@b
        err=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',B,vc,B),0))
        B1=design(family,x,fr['knots'],1)/K;B2=design(family,x,fr['knots'],2)/K
        slope=1/x+B1@b;curve=-1/x**2+B2@b
        slopeerr=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',B1,vc,B1),0))
        curveerr=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',B2,vc,B2),0))
    else:
        f,df=lcdm_integral(z,b[1]);fref,dfref=lcdm_integral(np.array([.1]),b[1]);
        logfr=np.log(f/fref[0]);B=np.column_stack([np.zeros(len(z)),df/f-dfref[0]/fref[0]])
        err=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',B,vc,B),0))
        # Shape derivatives are analytic in z, with x=ln(1+z).
        E=np.sqrt(1+b[1]*((1+z)**3-1));q=(1+z)/(E*f)
        slope=q;curve=q*(1-1.5*b[1]*(1+z)**3/E**2-q)
        # Finite difference in sole nonlinear shape parameter for diagnostic derivative errors.
        eps=1e-5;sl=[];cu=[]
        for om in [b[1]-eps,b[1]+eps]:
            ff,_=lcdm_integral(z,om);ee=np.sqrt(1+om*((1+z)**3-1));qq=(1+z)/(ee*ff)
            sl.append(qq);cu.append(qq*(1-1.5*om*(1+z)**3/ee**2-qq))
        slopeerr=np.abs((sl[1]-sl[0])/(2*eps))*np.sqrt(vc[1,1])
        curveerr=np.abs((cu[1]-cu[0])/(2*eps))*np.sqrt(vc[1,1])
    return {'zHD':z,'x':x,'log_F_over_F_at_z0p1':logfr,'sigma_log_relative_distance':err,
            'DL_HD_over_DL_HD_at_z0p1':np.exp(x-xr+logfr),
            'DA_HD_over_DA_HD_at_z0p1':np.exp(-x+xr+logfr),
            'd_log_F_dx':slope,'sigma_d_log_F_dx':slopeerr,
            'd2_log_F_dx2':curve,'sigma_d2_log_F_dx2':curveerr}


def main():
    t0=time.monotonic()
    if OUT.exists(): raise RuntimeError('Refusing to overwrite existing result directory')
    OUT.mkdir()
    seal=json.loads((ROOT/'FREEZE_SEAL.json').read_text())
    assert hashlib.sha256((ROOT/'FREEZE.md').read_bytes()).hexdigest()==seal['freeze_sha256']
    data,raw=load_release();sym=(raw+raw.T)/2
    z=data['zHD'];noncal=data['IS_CALIBRATOR']==0
    primary=noncal&(z>.023)
    ix=np.flatnonzero(primary);zz=z[primary];zh=data['zHEL'][primary];y=data['m_b_corr'][primary]
    cov=sym[np.ix_(ix,ix)];eigen=la.eigvalsh(cov)
    assert eigen[0]>0
    cids=data['CID'][primary]
    train=np.array([int(hashlib.sha256(c.encode()).hexdigest(),16)%5!=0 for c in cids])
    assert not set(cids[train])&set(cids[~train])
    diagnostics={'run_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'python':platform.python_version(),
        'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,
        'dtype':'float64','thread_limit':2,'memory_limit_bytes':3*1024**3,'release_rows':len(z),
        'release_unique_CID':len(set(data['CID'])),'primary_rows':len(ix),'primary_unique_CID':len(set(cids)),
        'primary_z_min':float(zz.min()),'primary_z_max':float(zz.max()),
        'train_rows':int(train.sum()),'validation_rows':int((~train).sum()),
        'train_unique_CID':len(set(cids[train])),'validation_unique_CID':len(set(cids[~train])),
        'raw_covariance_asymmetry_max_abs':float(np.max(np.abs(raw-raw.T))),
        'primary_covariance_eigen_min':float(eigen[0]),'primary_covariance_eigen_max':float(eigen[-1]),
        'primary_covariance_condition':float(eigen[-1]/eigen[0]),
        'max_diag_sigma_difference_to_rounded_table':float(np.max(np.abs(np.sqrt(np.diag(sym))-data['m_b_corr_err_DIAG']))),
        'freeze_sha256':seal['freeze_sha256'],'fit_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    table(OUT/'primary_rows.tsv',[{'release_index_zero_based':int(j),'CID':data['CID'][j],
        'IDSURVEY':int(data['IDSURVEY'][j]),'zHD':float(z[j]),'zHEL':float(data['zHEL'][j]),
        'm_b_corr':float(data['m_b_corr'][j]),'partition':'development' if t else 'validation'} for j,t in zip(ix,train)])
    print('METADATA',json.dumps(diagnostics),flush=True)
    validation=[validate(f,zz,zh,y,cov,train) for f in FAMILIES]
    save_json(OUT/'validation.json',validation)
    for v in validation:print('VALIDATION',v['family'],v['conditional_predictive_chi2'],v['n_validation'],flush=True)
    fits={f:fit(f,zz,zh,y,cov) for f in FAMILIES}
    save_json(OUT/'full_fits.json',{f:r['summary'] for f,r in fits.items()})
    for f,r in fits.items():print('PRIMARY',f,json.dumps(r['summary'],default=js),flush=True)
    sensitivity=[]
    for label,mask in [('zgt0p01',noncal&(z>.01)),('zgt0p05',noncal&(z>.05)),('primary_zlt1',primary&(z<1))]:
        ids=np.flatnonzero(mask);cs=sym[np.ix_(ids,ids)]
        for f in FAMILIES:
            r=fit(f,z[mask],data['zHEL'][mask],data['m_b_corr'][mask],cs)
            sensitivity.append({'variant':label,**r['summary']})
            rcurve=curves(f,np.array([.05,.1,.3,.6,1.]),r)
            sensitivity[-1]['common_grid_curves']=rcurve
    for label,cc in [('raw_upper',np.triu(raw)+np.triu(raw,1).T),('raw_lower',np.tril(raw)+np.tril(raw,-1).T)]:
        cs=cc[np.ix_(ix,ix)]
        for f in FAMILIES[:-1]:
            r=fit(f,zz,zh,y,cs)
            sensitivity.append({'variant':label,**r['summary'],
                'chi2_delta_primary':r['summary']['chi2']-fits[f]['summary']['chi2'],
                'parameter_delta_primary':r['beta']-fits[f]['beta']})
    spline_variants={}
    for label,knots in [('spline_coarse',np.log1p([.001,.3,.6,2.3])),
                        ('spline_fine',np.log1p([.001,.05,.1,.2,.3,.45,.6,1.,2.3]))]:
        r=fit('F4',zz,zh,y,cov,knots)
        spline_variants[label]=r
        sensitivity.append({'variant':label,**r['summary'],'common_grid_curves':curves('F4',np.array([.05,.1,.3,.6,1.]),r)})
    save_json(OUT/'sensitivity.json',sensitivity)
    grids=np.geomspace(zz.min(),zz.max(),400)
    curvetab=[];anchortab=[]
    for f,r in fits.items():
        for g,dest in [(grids,curvetab),(np.array([.05,.1,.3,.6,1.,2.]),anchortab)]:
            cc=curves(f,g,r)
            for j in range(len(g)):dest.append({'family':f,**{k:float(v[j]) for k,v in cc.items()}})
    table(OUT/'curves.tsv',curvetab);table(OUT/'anchor_curves.tsv',anchortab)
    table(OUT/'residuals.tsv',[{'release_index_zero_based':int(j),'CID':data['CID'][j],'zHD':float(z[j]),
        **{f'{f}_residual_mag':float(r['residual'][i]) for f,r in fits.items()}} for i,j in enumerate(ix)])
    table(OUT/'model_comparison.tsv',[{k:r['summary'][k] for k in ['family','n','p','chi2','dof','chi2_reduced','p_upper','p_lower','aicc_without_common_constant','bic_without_common_constant']} for r in fits.values()])

    # Relative reduced brightness shape is displayed against the frozen F0 baseline.
    fig,axes=plt.subplots(3,1,figsize=(9,11),sharex=True,gridspec_kw={'height_ratios':[1.5,1,1]})
    colors=dict(zip(FAMILIES,['#777777','#e07a17','#2868ba','#32914c','#9426a3','#111111']))
    base=K*np.log((1+zh)*np.log1p(zz));Aref=fits['F2']['beta'][0]
    axes[0].scatter(zz,y-base-Aref,s=5,alpha=.18,color='#666666',rasterized=True,label='Processed light curves')
    for f,r in fits.items():
        pg,X=predict(f,grids,grids,r);baseline=K*np.log((1+grids)*np.log1p(grids))
        q=pg-baseline-Aref;sd=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',X,r['vc'],X),0))
        axes[0].plot(grids,q,label=f,color=colors[f],lw=1.6)
        if f in ['F2','F4']:axes[0].fill_between(grids,q-1.96*sd,q+1.96*sd,color=colors[f],alpha=.14)
        c=curves(f,grids,r);cc=c['log_F_over_F_at_z0p1']-np.log(np.log1p(grids)/np.log1p(.1))
        axes[1].plot(grids,np.expm1(cc)*100,color=colors[f],lw=1.6)
        if f in ['F2','F4']:
            e=c['sigma_log_relative_distance'];axes[1].fill_between(grids,np.expm1(cc-1.96*e)*100,np.expm1(cc+1.96*e)*100,color=colors[f],alpha=.14)
    axes[2].scatter(zz,fits['F2']['residual'],s=5,alpha=.25,color=colors['F2'],rasterized=True)
    axes[2].axhline(0,color='black',lw=.8)
    axes[0].set_ylabel('Magnitude correction\nrelative to F0 + shared offset')
    axes[1].set_ylabel('Relative distance departure\nfrom F0, anchored z=0.1 (%)')
    axes[2].set_ylabel('F2 residual (mag)');axes[2].set_xlabel('Corrected release redshift zHD')
    axes[0].legend(ncol=4,fontsize=8);axes[0].set_ylim(-.7,.8);axes[2].set_ylim(-.8,.8)
    for a in axes:a.set_xscale('log');a.grid(alpha=.2)
    fig.suptitle('Pantheon+ empirical shape controls — full STAT+SYS covariance\nDRAFT; no native-law or absolute-distance inference; shaded pointwise 95% bands',fontsize=11)
    fig.tight_layout();fig.savefig(OUT/'empirical_curves_residuals.png',dpi=180);fig.savefig(OUT/'empirical_curves_residuals.pdf');plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(9,7),sharex=True)
    for label,r in [('F4 primary',fits['F4']),*spline_variants.items()]:
        c=curves('F4',grids,r)
        for a,key,err in [(axes[0],'d_log_F_dx','sigma_d_log_F_dx'),(axes[1],'d2_log_F_dx2','sigma_d2_log_F_dx2')]:
            # Subtract the analytically known ln(x) derivative to expose shape information.
            reference=1/np.log1p(grids) if key=='d_log_F_dx' else -1/np.log1p(grids)**2
            val=c[key]-reference;a.plot(grids,val,label=label);a.fill_between(grids,val-1.96*c[err],val+1.96*c[err],alpha=.15)
    axes[0].set_ylabel('d ln(F/x) / dx');axes[1].set_ylabel('d² ln(F/x) / dx²');axes[1].set_xlabel('zHD')
    axes[0].legend(fontsize=8)
    for a in axes:a.set_xscale('log');a.grid(alpha=.2)
    fig.suptitle('Spline representation sensitivity — pointwise 95% bands\nBoundary curvature is imposed; finite-range derivative uncertainty is model conditional',fontsize=11)
    fig.tight_layout();fig.savefig(OUT/'spline_derivative_sensitivity.png',dpi=180);fig.savefig(OUT/'spline_derivative_sensitivity.pdf');plt.close(fig)
    diagnostics['elapsed_seconds']=time.monotonic()-t0
    diagnostics['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    save_json(OUT/'diagnostics.json',diagnostics)
    print('COMPLETE',json.dumps(diagnostics),flush=True)


if __name__=='__main__': main()
