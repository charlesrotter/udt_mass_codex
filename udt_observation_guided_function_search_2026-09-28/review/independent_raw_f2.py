"""Independent review implementation from frozen statistical equations.

No campaign construction imports; direct dense solves, spherical alias search,
analytic F2 AP Jacobian. Written before reading campaign fit code/results.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='2'
import gzip, hashlib, json, platform, sys, time
from pathlib import Path
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np
from scipy.linalg import solve, eigvalsh

P=Path(__file__).resolve().parents[1]; R=P/'review'; t0=time.time()
raw=P/'data/raw'
with (raw/'Pantheon+SH0ES.dat').open() as f:
    fields=f.readline().split(); rows=[line.split() for line in f if line.strip()]
d={name:np.array([row[i] for row in rows]) for i,name in enumerate(fields)}
def col(name):return d[name].astype(float)
with gzip.open(raw/'Pantheon+SH0ES_STAT+SYS.cov.gz','rt') as f:
    n=int(f.readline()); C0=np.loadtxt(f).reshape(n,n)
assert n==len(rows)
C=(C0+C0.T)/2
ix=np.flatnonzero((col('IS_CALIBRATOR')==0)&(col('zHD')>.023))
assert np.isfinite(np.column_stack([col(s)[ix] for s in ('zHD','zHEL','m_b_corr')])).all()
x=np.log1p(col('zHD')[ix]); k=5/np.log(10)
X=np.column_stack((np.ones(len(ix)),k*x,k*x*x))
y=col('m_b_corr')[ix]-k*np.log((1+col('zHEL')[ix])*x)
C=C[np.ix_(ix,ix)]
def gls(xx,yy,cc):
    invx=solve(cc,xx,assume_a='pos'); info=xx.T@invx
    vc=solve(info,np.eye(xx.shape[1]),assume_a='pos')
    b=solve(info,xx.T@solve(cc,yy,assume_a='pos'),assume_a='pos')
    rr=yy-xx@b; wr=solve(cc,rr,assume_a='pos')
    return b,vc,rr,float(rr@wr),float(np.max(np.abs(xx.T@wr)))
b,V,res,chi,score=gls(X,y,C)

# Recompute conservative alias relation from raw coordinates and epochs.
ids=d['CID']; parents={s:s for s in ids}
def find(s):
    while parents[s]!=s:s=parents[s]
    return s
def union(a,b):
    a,b=find(a),find(b)
    if a!=b:parents[max(a,b)]=min(a,b)
ra=np.deg2rad(col('RA')); dec=np.deg2rad(col('DEC')); epoch=col('PKMJD'); zz=col('zHD')
aliases={}
for i in range(n):
    jj=np.arange(i+1,n)
    eligible=(ids[jj]!=ids[i])&(np.abs(epoch[jj]-epoch[i])<10)&(np.abs(zz[jj]-zz[i])<.001)
    jj=jj[eligible]
    hav=np.sin((dec[jj]-dec[i])/2)**2+np.cos(dec[i])*np.cos(dec[jj])*np.sin((ra[jj]-ra[i])/2)**2
    arcsec=np.rad2deg(2*np.arcsin(np.minimum(1,np.sqrt(hav))))*3600
    for j,s in zip(jj[arcsec<5],arcsec[arcsec<5]):
        pair=tuple(sorted((ids[i],ids[j]))); aliases[pair]=float(s); union(*pair)
keys=np.array([find(s) for s in ids[ix]])
val=np.array([int(hashlib.sha256(s.encode()).hexdigest(),16)%5==0 for s in keys]); train=~val
bt,Vt,rt,ct,st=gls(X[train],y[train],C[np.ix_(train,train)])
CT=C[np.ix_(train,train)]; CVT=C[np.ix_(val,train)]
W=solve(CT,CVT.T,assume_a='pos').T
e=y[val]-X[val]@bt-W@rt
B=X[val]-W@X[train]
S=C[np.ix_(val,val)]-W@CVT.T
Vp=S+B@Vt@B.T
pv=float(e@solve(Vp,e,assume_a='pos'))
sign,logdet=np.linalg.slogdet(Vp); assert sign==1

mean=np.genfromtxt(P/'observations/bao/desi_gaussian_bao_ALL_GCcomb_mean.txt',dtype=None,encoding='utf8')
BC=np.loadtxt(P/'observations/bao/desi_gaussian_bao_ALL_GCcomb_cov.txt')
zs=[]; ratios=[]; J=[]
for z in sorted(set(float(r[0]) for r in mean)):
    im=[i for i,r in enumerate(mean) if float(r[0])==z and r[2]=='DM_over_rs']
    ih=[i for i,r in enumerate(mean) if float(r[0])==z and r[2]=='DH_over_rs']
    if not im or not ih:continue
    im,ih=im[0],ih[0]; dm,dh=float(mean[im][1]),float(mean[ih][1])
    row=np.zeros(len(mean)); row[im]=1/dh;row[ih]=-dm/dh**2
    zs.append(z);ratios.append(dm/dh);J.append(row)
zs=np.array(zs); ratios=np.array(ratios); J=np.array(J); Cbao=J@BC@J.T
xp=np.log1p(zs); den=1/xp+b[1]+2*b[2]*xp
pred=np.exp(xp)/den
JP=np.column_stack((np.zeros(len(zs)),-pred/den,-2*xp*pred/den))
Cpred=JP@V@JP.T
domain=(zs>=zz[ix].min())&(zs<=zz[ix].max())
diff=pred[domain]-ratios[domain]; total=(Cbao+Cpred)[np.ix_(domain,domain)]
q=float(diff@solve(total,diff,assume_a='pos'))

# Independent deterministic derivative check and a different-seed MC diagnostic.
fd=[]
for i in range(3):
    h=1e-5; bp=b.copy();bm=b.copy();bp[i]+=h;bm[i]-=h
    fp=np.exp(xp)/(1/xp+bp[1]+2*bp[2]*xp)
    fm=np.exp(xp)/(1/xp+bm[1]+2*bm[2]*xp)
    fd.append((fp-fm)/(2*h))
rng=np.random.default_rng(11282026); draws=rng.multivariate_normal(b,V,size=40000)
dd=1/xp[None,:]+draws[:,1,None]+2*draws[:,2,None]*xp[None,:]
pp=np.exp(xp)[None,:]/dd
positive=np.all(dd[:,domain]>0,axis=1)
result={'implementation':'independent raw parser and dense solves; no production imports',
 'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'threads':2},
 'n_raw':n,'n_primary':len(ix),'z_minmax':[float(zz[ix].min()),float(zz[ix].max())],
 'raw_cov_asymmetry':float(np.max(np.abs(C0-C0.T))),'primary_cov_min_eigenvalue':float(eigvalsh(C,subset_by_index=[0,0])[0]),
 'F2':{'beta':b.tolist(),'covariance':V.tolist(),'chi2':chi,'normal_score_max':score},
 'aliases':[{'cids':list(pair),'separation_arcsec':s} for pair,s in sorted(aliases.items())],
 'validation':{'n_train':int(train.sum()),'n_validation':int(val.sum()),'beta':bt.tolist(),'score':pv,'neg2logpredictive':float(pv+logdet+val.sum()*np.log(2*np.pi)),'log_score':float(-.5*(pv+logdet+val.sum()*np.log(2*np.pi)))},
 'AP':{'z':zs.tolist(),'included':domain.tolist(),'data':ratios.tolist(),'prediction':pred.tolist(),'bao_covariance':Cbao.tolist(),'prediction_covariance':Cpred.tolist(),'quadratic':q,'jacobian_fd_max_abs':float(np.max(np.abs(np.array(fd).T-JP))),
       'MC_draws':len(draws),'MC_seed':11282026,'MC_positive_fraction':float(positive.mean()),'MC_var_ratio':(pp.var(axis=0,ddof=1)/np.diag(Cpred)).tolist(),'MC_bias_in_linear_sigma':((pp.mean(axis=0)-pred)/np.sqrt(np.diag(Cpred))).tolist()},
 'elapsed_s':time.time()-t0,
 'source_hashes':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [raw/'Pantheon+SH0ES.dat',raw/'Pantheon+SH0ES_STAT+SYS.cov.gz',P/'observations/bao/desi_gaussian_bao_ALL_GCcomb_mean.txt',P/'observations/bao/desi_gaussian_bao_ALL_GCcomb_cov.txt']}}
(R/'INDEPENDENT_RAW_F2.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
