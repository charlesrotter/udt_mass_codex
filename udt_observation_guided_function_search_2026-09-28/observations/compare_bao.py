"""Frozen conditional BAO check of SNe-only fits; no parameter optimization."""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_key] = '2'
os.environ.setdefault('MPLCONFIGDIR', '/tmp/udt_function_bao_mpl')
from pathlib import Path
import datetime
import hashlib
import json
import platform
import resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.interpolate import make_interp_spline
from scipy.linalg import cho_factor, cho_solve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'data' / 'results'
K = 5 / np.log(10.)

def encode(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, np.generic): return o.item()
    raise TypeError(type(o).__name__)

def predict(family, z, beta, knots=None):
    """Return ratio, coefficient Jacobian and log-distance slope."""
    x = np.log1p(z)
    j = np.zeros((len(z), len(beta)))
    if family == 'F5':
        om = beta[1]
        h = (1 + z)**3 - 1
        E = np.sqrt(1 + om*h)
        f = np.array([quad(lambda t: (1+om*((1+t)**3-1))**-.5,
                           0, zz, epsabs=1e-12, epsrel=1e-12)[0] for zz in z])
        df = np.array([quad(lambda t: -.5*((1+t)**3-1)*(1+om*((1+t)**3-1))**-1.5,
                            0, zz, epsabs=1e-12, epsrel=1e-12)[0] for zz in z])
        ratio = E*f
        j[:, 1] = h*f/(2*E)+E*df
        return ratio, j, (1+z)/ratio
    if family == 'F4':
        basis = make_interp_spline(np.log1p(knots), np.eye(len(beta)), bc_type='natural')
        b1 = basis(x, nu=1)/K
    else:
        b1 = np.zeros_like(j)
        for power in range(1, len(beta)):
            b1[:, power] = power*x**(power-1)
    slope = 1/x + b1@beta
    ratio = (1+z)/slope
    j = -(1+z)[:, None]*b1/slope[:, None]**2
    return ratio, j, slope

def draw_predictions(family, z, draws, knots=None):
    x=np.log1p(z)
    if family == 'F5':
        om=draws[:, 1]
        nodes,weights=np.polynomial.legendre.leggauss(64)
        t=z[:,None]*(nodes+1)/2
        h=(1+t)**3-1
        e2=1+om[:,None,None]*h[None,:,:]
        if not np.all(e2>0): raise ValueError('F5 coefficient draws left positive E2 domain')
        f=z[None,:]/2*np.einsum('ijk,k->ij',e2**-.5,weights)
        ratio=f*np.sqrt(1+om[:,None]*((1+z)**3-1))
        return ratio,np.ones_like(ratio,dtype=bool)
    if family=='F4':
        b1=make_interp_spline(np.log1p(knots),np.eye(draws.shape[1]),bc_type='natural')(x,nu=1)/K
    else:
        b1=np.zeros((len(z),draws.shape[1]))
        for power in range(1,draws.shape[1]): b1[:,power]=power*x**(power-1)
    slope=1/x[None,:]+draws@b1.T
    return (1+z)[None,:]/slope,slope>0

def main():
    if not (DATA/'diagnostics.json').exists():
        raise RuntimeError('Data-lane completion marker not yet present; do not read partial outputs')
    out=ROOT/'comparison_checked'
    if out.exists(): raise RuntimeError('Refuse output-directory overwrite')
    out.mkdir()
    freeze=ROOT/'BAO_COMPARISON_FREEZE.md'
    fits=json.loads((DATA/'full_fits.json').read_text())
    diagnostics=json.loads((DATA/'diagnostics.json').read_text())
    means=np.genfromtxt(ROOT/'bao/desi_gaussian_bao_ALL_GCcomb_mean.txt',
                        names=['z','value','quantity'],dtype=None,encoding='utf8')
    C=np.loadtxt(ROOT/'bao/desi_gaussian_bao_ALL_GCcomb_cov.txt')
    assert C.shape==(len(means),len(means)) and np.allclose(C,C.T,atol=0,rtol=0)
    cho_factor(C)
    pairs=[]
    for z in np.unique(means['z']):
        m=np.flatnonzero((means['z']==z)&(means['quantity']=='DM_over_rs'))
        h=np.flatnonzero((means['z']==z)&(means['quantity']=='DH_over_rs'))
        if len(m)==1 and len(h)==1: pairs.append((z,int(m[0]),int(h[0])))
    zz=np.array([p[0] for p in pairs]); values=means['value']
    J=np.zeros((len(pairs),len(means))); ratios=[]
    for row,(_,im,ih) in enumerate(pairs):
        ratios.append(values[im]/values[ih]); J[row,im]=1/values[ih]
        J[row,ih]=-values[im]/values[ih]**2
    ratios=np.array(ratios); R=J@C@J.T
    inside=(zz>=diagnostics['primary_z_min'])&(zz<=diagnostics['primary_z_max'])
    rng=np.random.default_rng(9282026)
    mc=rng.multivariate_normal(values,C,size=100000,check_valid='raise')
    mc_ratios=np.column_stack([mc[:,im]/mc[:,ih] for _,im,ih in pairs])
    denominator_positive=bool(all(np.all(mc[:,ih]>0) for _,_,ih in pairs))
    ratio_mc_cov=np.cov(mc_ratios,rowvar=False)
    bao_diag={'draws':100000,'seed':9282026,'all_denominators_positive':denominator_positive,
              'mean_bias_over_linear_sigma':(mc_ratios.mean(axis=0)-ratios)/np.sqrt(np.diag(R)),
              'variance_ratio_to_linear':np.diag(ratio_mc_cov)/np.diag(R)}
    bao_ok=(denominator_positive and
            np.max(np.abs(bao_diag['mean_bias_over_linear_sigma'][inside]))<.2 and
            np.max(np.abs(bao_diag['variance_ratio_to_linear'][inside]-1))<.2)
    records={}; curve_rows=[]
    grid=np.geomspace(diagnostics['primary_z_min'],max(zz),450)
    fig,ax=plt.subplots(figsize=(9,6))
    ax.errorbar(zz[inside],ratios[inside],yerr=np.sqrt(np.diag(R))[inside],fmt='o',color='black',
                capsize=3,label='DESI compressed ratios, within SNe domain')
    ax.errorbar(zz[~inside],ratios[~inside],yerr=np.sqrt(np.diag(R))[~inside],fmt='s',mfc='none',
                color='black',capsize=3,label='Outside SNe domain: extrapolation only')
    for family,record in fits.items():
        beta=np.array(record['beta']);V=np.array(record['parameter_covariance']);knots=record.get('knots_z')
        pred,G,slope=predict(family,zz,beta,knots)
        P=G@V@G.T
        rng=np.random.default_rng(9282027)
        draws=rng.multivariate_normal(beta,V,size=20000,check_valid='raise')
        pd,positive=draw_predictions(family,zz,draws,knots)
        positive_fraction=float(np.mean(np.all(positive[:,inside],axis=1)))
        # Preserve every draw; do not condition statistics on validity or clip ratios.
        diagvar=np.diag(P);nonzero=diagvar>1e-24
        varratio=np.ones(len(zz));bias=np.zeros(len(zz))
        varratio[nonzero]=np.var(pd[:,nonzero],axis=0,ddof=1)/diagvar[nonzero]
        bias[nonzero]=(np.mean(pd[:,nonzero],axis=0)-pred[nonzero])/np.sqrt(diagvar[nonzero])
        applicable=inside&nonzero
        pred_ok=(positive_fraction>=.999 and np.all(slope[inside]>0) and
                 (not np.any(applicable) or (np.max(abs(varratio[applicable]-1))<.2 and np.max(abs(bias[applicable]))<.2)))
        residual=pred-ratios;total=(R+P)[np.ix_(inside,inside)]
        statistic=None
        if bao_ok and pred_ok:
            res=residual[inside];statistic=float(res@cho_solve(cho_factor(total),res))
        fd=[]
        for j,b in enumerate(beta):
            step=1e-7*max(1.,abs(b));bp=beta.copy();bm=beta.copy();bp[j]+=step;bm[j]-=step
            fd.append((predict(family,zz,bp,knots)[0]-predict(family,zz,bm,knots)[0])/(2*step))
        fd=np.column_stack(fd)
        jacobian_error=float(np.max(abs(fd-G)/(1+abs(G))))
        if jacobian_error>2e-7: raise AssertionError(f'{family} parameter Jacobian disagreement {jacobian_error}')
        records[family]={'prediction':pred,'prediction_covariance':P,'residual':residual,
                         'log_F_slope':slope,'positive_draw_fraction_all_included':positive_fraction,
                         'prediction_mc_variance_ratio':varratio,'prediction_mc_mean_bias_sigma':bias,
                         'local_gaussian_prediction_diagnostic_pass':bool(pred_ok),
                         'quadratic_consistency_statistic':statistic,'included_points':int(inside.sum()),
                         'statistic_interpretation':'approximate conditional tension diagnostic; no calibrated chi-square significance',
                         'cross_probe_covariance':'assumed zero; not empirically certified',
                         'parameter_jacobian_finite_difference_relative_error':jacobian_error}
        gp,gj,gs=predict(family,grid,beta,knots)
        line=ax.plot(grid,np.where(gs>0,gp,np.nan),lw=1.6,label=family)[0]
        if family in ['F2','F4']:
            sigma=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',gj,V,gj),0))
            ax.fill_between(grid,gp-sigma,gp+sigma,color=line.get_color(),alpha=.12)
        for z,p,s in zip(grid,gp,gs): curve_rows.append({'family':family,'z':float(z),'F_AP':float(p),'Fprime_over_F':float(s)})
    ax.axvline(diagnostics['primary_z_max'],ls=':',color='#777777',lw=1)
    ax.set(xlabel='Redshift z',ylabel='D_M / D_H',ylim=(0,6.5),xlim=(0,2.45))
    ax.grid(alpha=.2);ax.legend(fontsize=8,ncol=2)
    ax.set_title('Conditional cross-probe check: SNe-only shapes against BAO\nFlat homogeneous geometry + conventional ruler/optics; no BAO retuning',fontsize=10)
    fig.tight_layout();fig.savefig(out/'bao_shape_comparison.png',dpi=180);fig.savefig(out/'bao_shape_comparison.pdf');plt.close(fig)
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
            'dtype':'float64','status':'DRAFT conditional empirical/kinematic comparison, not native UDT confirmation',
            'z':zz,'ratios':ratios,'ratio_covariance':R,'within_sne_domain':inside,
            'bao_gaussian_ratio_diagnostics':bao_diag,'bao_delta_diagnostic_pass':bool(bao_ok),
            'models':records,'curves':curve_rows,
            'input_sha256':{str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in [freeze,Path(__file__),DATA/'full_fits.json',DATA/'diagnostics.json',
                                      ROOT/'bao/desi_gaussian_bao_ALL_GCcomb_mean.txt',ROOT/'bao/desi_gaussian_bao_ALL_GCcomb_cov.txt']}}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,default=encode,allow_nan=False)+'\n')
    print(json.dumps({'bao_delta_ok':bool(bao_ok),'included':int(inside.sum()),
                      'models':{f:{k:r[k] for k in ['quadratic_consistency_statistic','local_gaussian_prediction_diagnostic_pass','positive_draw_fraction_all_included']} for f,r in records.items()}},indent=2))

if __name__=='__main__': main()
