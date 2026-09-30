"""Post-freeze implementation of declared diagnostics; no outcome selection."""
from pathlib import Path
import hashlib,json,numpy as np
from analyze import ROOT,load,clocks,shift

names=['pilot_n32','pilot_n64','survey_n64','survey_n128','survey_n128_halfdt','survey_n256',
       'challenge_n128','challenge_n256','period_k050_n128','period_k050_n256',
       'period_k100_n128','period_k100_n256']
pairs=[('survey_n64','survey_n128'),('survey_n128','survey_n128_halfdt'),
       ('survey_n128_halfdt','survey_n256'),('challenge_n128','challenge_n256'),
       ('period_k050_n128','period_k050_n256'),('period_k100_n128','period_k100_n256')]
summary={};allclocks={}
for name in names:
    d,m=load(name);c=clocks(d,m);allclocks[name]=c
    summary[name]={key:m[key] for key in ('elapsed_seconds','peak_gpu_allocated_bytes','max_constraint','max_tail','shape','steps')}
    summary[name]['field_sha256']=hashlib.sha256((ROOT/'runs'/name/'fields.npz').read_bytes()).hexdigest()
    summary[name]['logZ_range']=[min(r['logZ_min'] for r in c),max(r['logZ_max'] for r in c)]
    summary[name]['delta_logZ_vs_zero_velocity_homogeneous_min']=min(r['delta_logZ_vs_homogeneous_min'] for r in c)
    summary[name]['final_lambda_mean_increase']=(d['state'][-1,:,4].mean(-1)-d['state'][0,:,4].mean(-1)).tolist()
comparisons=[]
for a,b in pairs:
    da,ma=load(a);db,mb=load(b);assert np.array_equal(da['times'],db['times'])
    factor=mb['spec']['n']//ma['spec']['n'];err=np.abs(da['state']-db['state'][...,::factor])
    per_case=np.max(err,axis=(0,2,3)).tolist()
    ca,cb=allclocks[a],allclocks[b];assert len(ca)==len(cb)
    # Compare the same full clock fields at shared emitter sites, not extrema
    # sampled on different grids (which have their own sampling difference).
    logerr=0.
    for te in (1.,4.,8.,16.):
        for dist in (1.,2.,4.,8.):
            if te+dist>da['times'][-1]:continue
            ia=np.flatnonzero(np.isclose(da['times'],te,atol=1e-12,rtol=0))[0]
            ib=np.flatnonzero(np.isclose(da['times'],te+dist,atol=1e-12,rtol=0))[0]
            za=(shift(da['state'][ib,:,4],dist,ma['spec']['k'])-da['state'][ia,:,4])/4
            zb=(shift(db['state'][ib,:,4],dist,mb['spec']['k'])-db['state'][ia,:,4])/4
            logerr=max(logerr,float(np.max(np.abs(za-zb[:,::factor]))))
    record={'a':a,'b':b,'max_abs_state':float(err.max()),'case_max_abs_state':per_case,'max_abs_logZ':logerr}
    assert err.max()<2e-5 and logerr<2e-5
    comparisons.append(record)
for r in summary.values():
    assert r['max_constraint']<2e-5 and r['max_tail']<1e-6
    assert r['delta_logZ_vs_zero_velocity_homogeneous_min']>-2e-5
result={'status':'PARENT_DIAGNOSTICS_PASS_IN_DECLARED_SCOPE',
    'runs':summary,'refinement':comparisons,
    'total_evolution_seconds':sum(r['elapsed_seconds'] for r in summary.values()),
    'history_executions_including_repeats':sum(r['shape'][1] for r in summary.values()),
    'saved_grid_bytes':sum((ROOT/'runs'/n/'fields.npz').stat().st_size for n in names),
    'interpretation':'Conditional two-Killing Ric=0; fixed supplied clocks and lifted longitudinal branches. Per-period supplied data differ; no universal curve, native selection or infinite-time conclusion.'}
with (ROOT/'CAMPAIGN_DIAGNOSTICS.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
with (ROOT/'CLOCK_READOUTS.json').open('x') as f:json.dump(allclocks,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('runs','refinement')},indent=2))
print(json.dumps(comparisons,indent=2))

# A standalone explanatory figure. Three amplitudes at the frozen phase0;
# full results remain above. Bands span sampled emission locations.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d,m=load('challenge_n256');times=d['times'];u=d['state'];ids=[c['id'] for c in m['spec']['cases']]
fig,ax=plt.subplots(1,2,figsize=(11,4.4),layout='constrained')
for name,label,col in [('a0_p0','initial amplitude 0.15','#1b6ca8'),('a1_p0','0.45','#ab7216'),('a2_p0','0.90','#b33c4a')]:
    j=ids.index(name)
    ax[0].plot(times,u[:,j,4].mean(-1)-u[0,j,4].mean(),label=label,color=col)
    distances=np.arange(.25,8.001,.25);values=[]
    for dist in distances:
        it=np.flatnonzero(np.isclose(times,1+dist,atol=1e-12,rtol=0))[0]
        values.append((shift(u[it,j,4],dist,.75)-u[0,j,4])/4-.25*np.log(1+dist))
    values=np.array(values)
    ax[1].plot(distances,values.mean(1),color=col,label=label)
    ax[1].fill_between(distances,values.min(1),values.max(1),color=col,alpha=.14)
ax[1].plot(distances,-.25*np.log(1+distances),color='.4',ls='--',label='zero-velocity homogeneous control')
ax[1].axhline(0,color='.5',lw=.6)
ax[0].set(xlabel='Areal coordinate time t',ylabel='Mean λ increase',title='Metric response accumulates')
ax[1].set(xlabel='Chosen longitudinal branch duration d',ylabel='log Z (positive = redshift)',title='Actual supplied-clock comparison, emission t = 1')
ax[0].legend(fontsize=8);ax[1].legend(fontsize=7)
fig.suptitle('Conditional Ricci-flat testbed • not a selected UDT geometry',fontsize=12)
for a in ax:a.grid(alpha=.15)
fig.savefig(ROOT/'CONDITIONAL_CLOCK_COMPARISON.png',dpi=170)
fig.savefig(ROOT/'CONDITIONAL_CLOCK_COMPARISON.pdf')
