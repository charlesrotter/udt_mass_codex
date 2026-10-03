"""Clock/calibration-only inverse. No forward module, metric, equation or oracle."""
import argparse,json,math,random
from pathlib import Path
from collections import defaultdict

def reconstruct(data,epsilon=0.,seed=1729):
    if data['schema']!='CBR1_CLOCK_ONLY':raise ValueError('SCHEMA')
    v=data['speed'];assert 0<v<1; rng=random.Random(seed); groups=defaultdict(dict)
    for row in data['records']:
        allowed={'case','center','h','site','L','frame','direction','log_p'}
        if set(row)!=allowed:raise ValueError('UNDECLARED_INVERSE_INPUT')
        key=tuple(row[n] for n in ['case','center','h','site','L'])
        entry=(row['frame'],row['direction'])
        if entry in groups[key]:raise ValueError('DUPLICATE_CLOCK')
        groups[key][entry]=row['log_p']+epsilon*rng.uniform(-1,1)
    scalars={}
    for key,obs in groups.items():
        if set(obs)!={(f,d) for f in range(7) for d in range(3)}:raise ValueError('INCOMPLETE_FRAME_SET')
        L=key[-1];c=[-2*sum(obs[f,d] for d in range(3))/L**2 for f in range(7)]
        scalars[key]=(1-v*v)*sum(c[1:])/(2*v*v)-(1+3/v**2)*c[0]
    bysite=defaultdict(dict)
    for (*base,L),r in scalars.items():bysite[tuple(base)][L]=r
    extrap={};errors={};weight=(6/v**2-2)*6
    for key,levels in bysite.items():
        ls=sorted(levels,reverse=True)
        for large,small in zip(ls,ls[1:]):
            if abs(large/small-2)>1e-12:raise ValueError('NONHALVING_L')
            pair=(large,small)
            extrap[key+pair]=2*levels[small]-levels[large]
            errors[key+pair]=weight*epsilon*(2/small**2+1/large**2)
    byevent=defaultdict(dict)
    for (case,center,h,site,large,small),r in extrap.items():
        byevent[(case,center,h,large,small)][site]=r
    events=[]
    expected={'o','t+','t-','x+','x-','y+','y-','z+','z-'}
    for key,s in sorted(byevent.items()):
        if set(s)!=expected:raise ValueError('INCOMPLETE_GEODESIC_STENCIL')
        case,center,h,large,small=key
        q=(-s['t+']-s['t-']+sum(s[k] for k in ['x+','x-','y+','y-','z+','z-'])-4*s['o'])/h**2
        e=errors[(case,center,h,'o',large,small)]
        events.append(dict(case=case,center=center,h=h,L_large=large,L_small=small,R=s['o'],Q=q,
                           R_noise_bound=e,Q_noise_bound=12*e/h**2))
    fitgroups=defaultdict(list)
    for row in events:fitgroups[(row['case'],row['h'],row['L_large'],row['L_small'])].append(row)
    fits=[]
    for key,rows in sorted(fitgroups.items()):
        rows=sorted(rows,key=lambda row:row['center']);left,right=rows[0],rows[-1]
        dr=right['R']-left['R'];dq=right['Q']-left['Q']
        er=max(row['R_noise_bound'] for row in rows);eq=max(row['Q_noise_bound'] for row in rows)
        fit=dict(case=key[0],h=key[1],L_large=key[2],L_small=key[3],fit_centers=[left['center'],right['center']],
                 delta_R=dr,delta_Q=dq,R_noise_bound=er,Q_noise_bound=eq)
        if abs(dr)<=5e-4+2*er:fit.update(status='UNINFORMATIVE_AT_DECLARED_RESOLUTION')
        else:
            m=dq/dr;intercept=left['Q']-m*left['R']
            hold=[dict(center=row['center'],residual=row['Q']-m*row['R']-intercept) for row in rows[1:-1]]
            fit.update(status='AFFINE_RELATION_ESTIMATED',slope=m,intercept=intercept,heldout=hold,
                       max_heldout_residual=max([abs(row['residual']) for row in hold],default=0.),
                       slope_noise_bound=(2*eq+2*abs(m)*er)/max(abs(dr)-2*er,1e-300))
            if abs(dq)>1e-5+2*eq and m!=0:
                fit.update(alpha=1/(6*m),Lambda=-intercept/(4*m))
            else:fit['parameter_status']='SLOPE_UNRESOLVED_AT_DECLARED_RESOLUTION'
        fits.append(fit)
    return dict(schema='CBR1_INVERSE',epsilon=epsilon,seed=seed,events=events,fits=fits,
                limits='Noise bounds cover the supplied bounded log-record perturbation only, not truncation, solver, preparation or ruler error. No metric/equation/oracle input. Finite tests, not physical law evidence.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');ap.add_argument('--epsilon',type=float,default=0.);ap.add_argument('--seed',type=int,default=1729)
    args=ap.parse_args();out=reconstruct(json.loads(Path(args.input).read_text()),args.epsilon,args.seed)
    with Path(args.output).open('x') as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':'COMPLETED','events':len(out['events']),'fits':len(out['fits']),'epsilon':args.epsilon}))
