"""Post-inverse oracle comparison, saved-a tensor check, all frozen gates."""
import json,math
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent;O=B/'main'
def read(name):return json.loads((O/name).read_text())
def key(r):return tuple(r[k] for k in ['case','center','h','L_large','L_small'])
def weights(derivative):
    # Exact rational moment equations on -4..4, independently from the ODE.
    xs=list(range(-4,5));a=[[Fraction(x)**k for x in xs]+[Fraction(math.factorial(k) if k==derivative else 0)] for k in range(9)]
    for i in range(9):
        j=next(j for j in range(i,9) if a[j][i]);a[i],a[j]=a[j],a[i]
        pivot=a[i][i];a[i]=[v/pivot for v in a[i]]
        for j in range(9):
            if j!=i:
                q=a[j][i];a[j]=[v-q*w for v,w in zip(a[j],a[i])]
    return [float(a[i][-1]) for i in range(9)]
def main():
    fine=read('fine/inverse_clean.json');coarse=read('coarse/inverse_clean.json')
    truth={(r['case'],r['center']):r for r in read('oracle.json')['truth']};gates={};errors=[]
    for r in fine['events']:
        target=truth[r['case'],r['center']]
        errors.append(dict(**r,R_error=r['R']-target['R'],Q_error=r['Q']-target['Q']))
    finest=[r for r in errors if r['h']==.04 and r['L_small']==.005]
    gates['scalar_accuracy']=max(abs(r['R_error']) for r in finest)<=5e-4
    gates['box_accuracy']=max(abs(r['Q_error']) for r in finest)<=2e-3
    fits={r['case']:r for r in fine['fits'] if r['h']==.04 and r['L_small']==.005}
    pos=fits['A'];gates['positive_alpha']=abs(pos.get('alpha',math.inf)-1)<=.05
    gates['positive_Lambda']=abs(pos.get('Lambda',math.inf))<=5e-4
    gates['positive_holdout']=pos.get('max_heldout_residual',math.inf)<=1e-3
    gates['false_pass_uninformative']=fits['B']['status']=='UNINFORMATIVE_AT_DECLARED_RESOLUTION'
    gates['offlaw_discriminated']=fits['C'].get('max_heldout_residual',0)>5e-3
    coarsemap={key(r):r for r in coarse['events']}
    sensitivity={s:max(abs(r[s]-coarsemap[key(r)][s]) for r in fine['events']) for s in ['R','Q']}
    fo=read('fine/observations.json')['records'];co=read('coarse/observations.json')['records'];assert len(fo)==len(co)
    for a,b in zip(fo,co):assert {k:v for k,v in a.items() if k!='log_p'}=={k:v for k,v in b.items() if k!='log_p'}
    sensitivity['log_p']=max(abs(a['log_p']-b['log_p']) for a,b in zip(fo,co))
    gates['numeric_refinement']=all(sensitivity[s]<=limit for s,limit in [('log_p',1e-10),('R',5e-5),('Q',1e-3)])
    base={key(r):r for r in fine['events']};noises=[]
    for tag in ['1e-14','1e-12','1e-10']:
        data=read(f'fine/inverse_noise_{tag}.json');changes=[]
        for row in data['events']:
            changes.append(dict(case=row['case'],center=row['center'],h=row['h'],L_small=row['L_small'],
                R_change=abs(row['R']-base[key(row)]['R']),Q_change=abs(row['Q']-base[key(row)]['Q']),
                R_bound=row['R_noise_bound'],Q_bound=row['Q_noise_bound']))
        gates[f'noise_bound_{tag}']=all(r['R_change']<=r['R_bound']+1e-12 and r['Q_change']<=r['Q_bound']+1e-10 for r in changes)
        noises.append(dict(epsilon=float(tag),changes=changes,fits=data['fits']))
    adv=read('adversarial_result.json');gates['adversarial_bound_attained']=abs(adv['observed_Q_change']/adv['bound']-1)<=.001
    metric=read('metric_a_only.json');jets=[];ws={d:weights(d) for d in range(1,5)}
    for case,values in metric['a'].items():
        for t in [-.6,-.3,0.,.3,.6]:
            center=round((t+1.2)*1000)
            for step in [.04,.02]:
                stride=round(step*1000);ys=[values[center+i*stride] for i in range(-4,5)]
                ds=[values[center]]+[math.fsum(w*y for w,y in zip(ws[d],ys))/step**d for d in range(1,5)]
                a,a1,a2,a3,a4=ds;H=a1/a;A=a2/a;R=6*(A+H*H)
                P=6*(a3/a+H*A-2*H**3);second=6*(a4/a+A*A-8*H*H*A+6*H**4);Q=-second-3*H*P
                E00=3*H*H-6*R*A+R*R/2+6*H*P
                Es=-2*A-H*H+2*R*(A+2*H*H)-R*R/2-2*second-4*H*P
                jets.append(dict(case=case,t=t,step=step,a_jet=ds,R=R,Q=Q,E00=E00,Es=Es,trace_check=-E00+3*Es-(6*Q-R)))
    positive=[r for r in jets if r['case']=='A'];false=[r for r in jets if r['case']=='B']
    gates['positive_original_tensor']=max(abs(r[k]) for r in positive for k in ['E00','Es'])<=2e-6
    gates['false_original_tensor']=all(r['E00']>1e-2 and abs(r['R'])<1e-6 and abs(r['Q'])<1e-6 for r in false)
    result=dict(status='PASS' if all(gates.values()) else 'LIMIT_OR_DEFECT_REQUIRES_REVIEW',gates=gates,
        finest_errors=finest,all_errors=errors,finest_fits=fits,numerical_sensitivity=sensitivity,noise=noises,adversarial=adv,saved_a_tensor_checks=jets,
        limits='Finite numerical evidence for supplied symmetric synthetic controls. No experimental feasibility, generic4D, native selection or error certification.')
    with (O/'EVALUATION.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k] for k in ['status','gates','finest_fits','numerical_sensitivity','adversarial']}))
if __name__=='__main__':main()
