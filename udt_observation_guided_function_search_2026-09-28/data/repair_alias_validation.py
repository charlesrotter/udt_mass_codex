#!/usr/bin/env python3
"""Only the documented source-grouping repair; preserve all initial artifacts."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime as dt
import hashlib,json
import numpy as np
from scipy.linalg import solve
import fit_empirical as fe

P=Path(__file__).resolve().parent


def main():
    out=P/'alias_validation'
    if out.exists():raise RuntimeError('Refuse overwrite')
    out.mkdir()
    freeze=P/'ALIAS_REPAIR_FREEZE.md'
    fe.save_json(out/'FREEZE_SEAL.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'freeze_sha256':hashlib.sha256(freeze.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exposure':'initial fits and alias schema diagnostics already exposed; repaired scores not yet computed'})
    d,raw=fe.load_release();N=len(d['CID']);parent=list(range(N))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        a,b=root(i),root(j);parent[b]=a
    byid={}
    for i,cid in enumerate(d['CID']):
        if cid in byid:union(i,byid[cid])
        byid[cid]=i
    alias=json.loads((P/'results/schema_diagnostic.json').read_text())['possible_cross_CID_aliases_same_sky_time_redshift']
    for pair in alias:
        i,j=pair['i'],pair['j'];assert d['CID'][i]==pair['CID_i'] and d['CID'][j]==pair['CID_j'];union(i,j)
    components={}
    for i in range(N):components.setdefault(root(i),[]).append(i)
    keys={r:min(d['CID'][i] for i in group) for r,group in components.items()}
    mask=(d['IS_CALIBRATOR']==0)&(d['zHD']>.023);ids=np.flatnonzero(mask)
    key=np.array([keys[root(i)] for i in ids]);train=np.array([int(hashlib.sha256(c.encode()).hexdigest(),16)%5!=0 for c in key])
    original=np.array([int(hashlib.sha256(c.encode()).hexdigest(),16)%5!=0 for c in d['CID'][mask]])
    C=((raw+raw.T)/2)[np.ix_(ids,ids)];z=d['zHD'][mask];zh=d['zHEL'][mask];y=d['m_b_corr'][mask]
    fe.table(out/'assignments.tsv',[{'release_index_zero_based':int(i),'CID':d['CID'][i],'group_key':g,
        'partition':'development' if t else 'validation','changed_from_original':bool(t!=old)} for i,g,t,old in zip(ids,key,train,original)])
    fe.OUT=out
    res=[fe.validate(f,z,zh,y,C,train) for f in fe.FAMILIES]
    fe.save_json(out/'validation.json',res)
    # Independent direct-solve anchor of repaired F2 score, no fitted beta imported.
    x=np.log1p(z);X=np.column_stack([np.ones(len(z)),fe.K*x,fe.K*x*x]);yy=y-5*np.log10((1+zh)*x)
    T=np.flatnonzero(train);V=np.flatnonzero(~train);Ctt=C[np.ix_(T,T)];Cvt=C[np.ix_(V,T)]
    gt=solve(Ctt,np.column_stack([yy[T],X[T]]),assume_a='sym');info=X[T].T@gt[:,1:]
    beta=solve(info,X[T].T@gt[:,0],assume_a='sym');vc=solve(info,np.eye(3),assume_a='sym')
    W=solve(Ctt,Cvt.T,assume_a='sym').T;e=yy[V]-X[V]@beta-W@(yy[T]-X[T]@beta)
    B=X[V]-W@X[T];Q=C[np.ix_(V,V)]-W@Cvt.T+B@vc@B.T
    score=float(e@solve(Q,e,assume_a='sym'));given=[r for r in res if r['family']=='F2'][0]
    diff=abs(score-given['conditional_predictive_chi2']);assert diff<2e-8
    old=json.loads((P/'results/validation.json').read_text())
    summary={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'DRAFT_ALIAS_REPAIR_CHECKED',
        'primary_rows':len(ids),'primary_conservative_groups':len(set(key)),
        'development_rows':len(T),'validation_rows':len(V),'changed_primary_rows':int(np.sum(train!=original)),
        'F2_direct_anchor_chi2':score,'F2_direct_anchor_abs_difference':diff,
        'all_data_fits':'unchanged; no refit','identity_limit':'finite conservative alias check, not exhaustive physical identity verification',
        'validation_comparison':[{'family':a['family'],'old_chi2':a['conditional_predictive_chi2'],
            'old_n':a['n_validation'],'repaired_chi2':b['conditional_predictive_chi2'],'repaired_n':b['n_validation'],
            'repaired_minus2logpdf':b['conditional_predictive_minus2logpdf']} for a,b in zip(old,res)]}
    fe.save_json(out/'summary.json',summary);print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
