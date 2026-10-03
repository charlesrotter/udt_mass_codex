"""Frozen finite CPU experiment. Save clock-only inverse before opening truth."""
import json,hashlib,time,platform,sys,math,copy
from pathlib import Path
import numpy as np
import scipy
from forward import Geometry,clock_triplet,expand_frames
from inverse import reconstruct
B=Path(__file__).resolve().parent
CENTERS=[-.6,-.3,0.,.3,.6]; HS=[.16,.08,.04]; LS=[.02,.01,.005]
KINDS={'A':'quadratic','B':'scalar_false_pass','C':'cubic_control'}
SITES=['o','t+','t-','x+','x-','y+','y-','z+','z-']
def save(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n')
def main():
    out=B/'main';out.mkdir(exist_ok=False);start=time.monotonic();calls=0
    freeze=json.loads((B/'RUN_FREEZE.json').read_text())
    for name,digest in freeze['files'].items():
        assert hashlib.sha256((B/name).read_bytes()).hexdigest()==digest,name
    all_inverse={};all_geometries={};counts={}
    for level in ['coarse','fine']:
        folder=out/level;folder.mkdir();records=[];details=[];mapping=[];placements=[]
        geometries={case:Geometry(kind,level=='fine') for case,kind in KINDS.items()}
        for case,g in geometries.items():
            cache={}
            for center in CENTERS:
                for h in HS:
                    spatial=g.spatial_site_time(center,h)
                    times=[center,center+h,center-h]+[spatial]*6
                    for site,t in zip(SITES,times):
                        placements.append(dict(case=case,center=center,h=h,site=site,cosmic_time=t))
                        for L in LS:
                            key=(t,L)
                            if key not in cache:
                                values=clock_triplet(g,t,L,.6)
                                ids=[]
                                for value in values:
                                    ids.append(len(details))
                                    details.append(dict(query_id=ids[-1],case=case,t=t,L=L,**value))
                                cache[key]=(values,ids)
                            values,ids=cache[key]
                            for row in expand_frames(values):
                                frame=row['frame'];direction=row['direction']
                                k=0 if frame==0 else (1 if direction==0 else 2)
                                mapping.append(ids[k])
                                records.append(dict(case=case,center=center,h=h,site=site,L=L,
                                                    frame=frame,direction=direction,log_p=row['log_p']))
            calls+=g.calls
            if calls>100000:raise RuntimeError('TOTAL_QUERY_BUDGET')
        public=dict(schema='CBR1_CLOCK_ONLY',speed=.6,records=records)
        save(folder/'observations.json',public)
        save(folder/'forward_details.json',dict(unique_queries=details,observation_query_ids=mapping,placements=placements,
             convention='Boost triads rotate/reflect with their frames; direction0 is along each boost. Isometry copies are not independent geometry samples.'))
        reread=json.loads((folder/'observations.json').read_text())
        epsilons=[0.] if level=='coarse' else [0.,1e-14,1e-12,1e-10]
        for epsilon in epsilons:
            inv=reconstruct(reread,epsilon,1729)
            tag='clean' if epsilon==0 else f'noise_{epsilon:.0e}'
            save(folder/f'inverse_{tag}.json',inv);all_inverse[level,tag]=inv
        counts[level]=dict(records=len(records),unique_queries=len(details),max_null=max(r['null_residual'] for r in details),max_norm=max(r['norm_error'] for r in details))
        all_geometries[level]=geometries
    # Predetermined worst-case signed log error; no target truth used.
    public=json.loads((out/'fine/observations.json').read_text())
    subset=dict(schema=public['schema'],speed=public['speed'],records=[r for r in public['records'] if r['case']=='A' and r['center']==0 and r['h']==.04])
    clean=reconstruct(subset);perturbed=copy.deepcopy(subset);epsilon=1e-12;v=.6
    for row in perturbed['records']:
        if row['L'] not in [.01,.005]:continue
        ws=-4 if row['site']=='o' else (-1 if row['site'].startswith('t') else 1)
        wf=-(1+3/v**2) if row['frame']==0 else (1-v*v)/(2*v*v)
        wl=2 if row['L']==.005 else -1
        row['log_p']+=math.copysign(epsilon,ws*wf*wl*(-2/row['L']**2))
    adv=reconstruct(perturbed)
    save(out/'adversarial_observations.json',perturbed);save(out/'adversarial_inverse.json',adv)
    select=lambda x:next(r for r in x['events'] if r['L_small']==.005)
    amplification=dict(epsilon=epsilon,observed_Q_change=select(adv)['Q']-select(clean)['Q'],
        bound=12*88*epsilon*(2/.005**2+1/.01**2)/.04**2)
    save(out/'adversarial_result.json',amplification)
    # All inverse artifacts now exist. Only here write the separately excluded truth.
    truth=[];grid=np.arange(-1200,1201,dtype=float)/1000
    metric={'t':grid.tolist(),'a':{},'exclusion':'Oracle/calibration audit only; never an inverse input.'}
    for case,g in all_geometries['fine'].items():
        metric['a'][case]=g.state(grid)[3].tolist()
        for t in CENTERS:
            H,R,P,a=[float(q) for q in g.state(t)]
            if case=='A':Q=R/6
            elif case=='B':Q=0.
            else:
                a1=.09*t*t;a2=.18*t;a3=.18
                A=a2/a;P=6*(a3/a+H*A-2*H**3)
                second=6*(A*A-8*H*H*A+6*H**4)
                Q=-second-3*H*P
            truth.append(dict(case=case,center=t,R=R,Q=Q))
    save(out/'oracle.json',dict(truth=truth,case_kinds=KINDS,positive='Equation-generated comparison; not evidence for its physical law.'))
    save(out/'metric_a_only.json',metric)
    result=dict(status='FORWARD_AND_INVERSE_COMPLETED',counts=counts,total_queries=calls,
        duration_seconds=time.monotonic()-start,python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),
        controls=dict(centers=CENTERS,h=HS,L=LS,v=.6,domain=[-1.5,1.5],dtype='float64',noise_seed=1729))
    save(out/'RUN_RESULT.json',result);print(json.dumps(result))
if __name__=='__main__':main()
