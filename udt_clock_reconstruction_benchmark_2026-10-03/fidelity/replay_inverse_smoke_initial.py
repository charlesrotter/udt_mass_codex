"""Independent raw-linear-weight CBR1 replay; imports no parent scientific code."""
import argparse, json, random, hashlib, platform
from pathlib import Path
from decimal import Decimal as D, getcontext
from collections import defaultdict

getcontext().prec=50
SITES={'o':-4,'t+':-1,'t-':-1,'x+':1,'x-':1,'y+':1,'y-':1,'z+':1,'z-':1}
def dec(x):return D(str(x))
def raw_coeff(v,frame,L):
    v2=dec(v)**2
    return (2*(1+3/v2) if frame==0 else -(1-v2)/v2)/dec(L)**2

def replay(data, epsilon=0., seed=1729):
    assert set(data)=={'schema','speed','records'}
    assert data['schema']=='CBR1_CLOCK_ONLY'
    values={}; noise={}; rng=random.Random(seed)
    for row in data['records']:
        assert set(row)=={'case','center','h','site','L','frame','direction','log_p'}
        key=tuple(row[k] for k in ['case','center','h','site','L','frame','direction'])
        assert key not in values
        dy=epsilon*rng.uniform(-1,1)
        values[key]=D.from_float(row['log_p']+dy)
        noise[key]=D.from_float(dy)
    bases=defaultdict(set)
    for case,center,h,site,L,frame,direction in values:
        bases[(case,center,h)].add(L)
    events=[]
    for (case,center,h),lengths in sorted(bases.items()):
        levels=sorted(lengths,reverse=True)
        for big,small in zip(levels,levels[1:]):
            assert dec(big)==2*dec(small)
            answer={'R':D(0),'Q':D(0),'R_noise_bound':D(0),'Q_noise_bound':D(0)}
            for site,sw in SITES.items():
                for L,ew in [(big,-1),(small,2)]:
                    for frame in range(7):
                        for direction in range(3):
                            key=(case,center,h,site,L,frame,direction)
                            weight=raw_coeff(data['speed'],frame,L)*ew
                            qw=weight*sw/dec(h)**2
                            answer['Q']+=qw*values[key]
                            answer['Q_noise_bound']+=abs(qw)*dec(epsilon)
                            if site=='o':
                                answer['R']+=weight*values[key]
                                answer['R_noise_bound']+=abs(weight)*dec(epsilon)
            events.append(dict(case=case,center=center,h=h,L_large=big,L_small=small,**answer))
    groups=defaultdict(list)
    for e in events:groups[(e['case'],e['h'],e['L_large'],e['L_small'])].append(e)
    fits=[]
    for key,rows in sorted(groups.items()):
        rows=sorted(rows,key=lambda e:e['center']); left,right=rows[0],rows[-1]
        dr=right['R']-left['R'];dq=right['Q']-left['Q']
        er=max(e['R_noise_bound'] for e in rows);eq=max(e['Q_noise_bound'] for e in rows)
        fit=dict(case=key[0],h=key[1],L_large=key[2],L_small=key[3],delta_R=dr,delta_Q=dq)
        if abs(dr)<=D('0.0005')+2*er:
            fit['status']='UNINFORMATIVE_AT_DECLARED_RESOLUTION'
        else:
            m=dq/dr;b=left['Q']-m*left['R']
            hold=[dict(center=e['center'],residual=e['Q']-m*e['R']-b) for e in rows[1:-1]]
            fit.update(status='AFFINE_RELATION_ESTIMATED',slope=m,intercept=b,heldout=hold,max_heldout_residual=max([abs(e['residual']) for e in hold],default=D(0)))
            if abs(dq)>D('0.00001')+2*eq and m:
                fit.update(alpha=1/(6*m),Lambda=-b/(4*m))
            else:fit['parameter_status']='SLOPE_UNRESOLVED_AT_DECLARED_RESOLUTION'
        fits.append(fit)
    return dict(events=events,fits=fits,epsilon=epsilon,seed=seed)

def eventkey(e):return tuple(e[k] for k in ['case','center','h','L_large','L_small'])
def fitkey(e):return tuple(e[k] for k in ['case','h','L_large','L_small'])
def compare(got, reference):
    events={eventkey(e):e for e in reference['events']}
    assert set(events)=={eventkey(e) for e in got['events']}
    maxdiff={'R':D(0),'Q':D(0),'R_noise_bound':D(0),'Q_noise_bound':D(0)}
    for row in got['events']:
        other=events[eventkey(row)]
        for field in maxdiff:maxdiff[field]=max(maxdiff[field],abs(row[field]-dec(other[field])))
    assert maxdiff['R']<D('1e-10') and maxdiff['Q']<D('1e-7'),maxdiff
    ff={fitkey(e):e for e in reference['fits']}; maxparam=D(0)
    for row in got['fits']:
        other=ff[fitkey(row)]
        assert row['status']==other['status'],(row,other)
        for field in ['alpha','Lambda','slope','intercept','max_heldout_residual']:
            assert (field in row)==(field in other),(field,row,other)
            if field in row:
                delta=abs(row[field]-dec(other[field]))/(1+abs(row[field]))
                maxparam=max(maxparam,delta)
                assert delta<D('1e-7'),(field,delta)
    return dict(max_event_difference=maxdiff,max_parameter_scaled_difference=maxparam)

def jsonable(x):
    if isinstance(x,D):return str(x)
    if isinstance(x,dict):return {k:jsonable(v) for k,v in x.items()}
    if isinstance(x,list):return [jsonable(v) for v in x]
    return x

def main():
    ap=argparse.ArgumentParser();ap.add_argument('observations');ap.add_argument('output');ap.add_argument('--reference');ap.add_argument('--epsilon',type=float,default=0.)
    args=ap.parse_args();path=Path(args.observations);data=json.loads(path.read_text())
    result=replay(data,args.epsilon)
    result.update(scope='Independent exposed Decimal raw-linear-weight inverse, no oracle',python=platform.python_version(),decimal_precision=getcontext().prec,
        input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),record_count=len(data['records']))
    if args.reference:
        ref=Path(args.reference);result['comparison']=compare(result,json.loads(ref.read_text()));result['reference_sha256']=hashlib.sha256(ref.read_bytes()).hexdigest()
    with Path(args.output).open('x') as f:json.dump(jsonable(result),f,indent=2);f.write('\n')
    print(json.dumps(jsonable({k:v for k,v in result.items() if k not in ['events','fits']}),indent=2))

if __name__=='__main__':main()
