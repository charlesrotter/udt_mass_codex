"""Generalize only TDS1 query times; retain its reviewed geometry interpolator."""
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
B=Path(__file__).resolve().parent;ROOT=B.parent
sys.path.insert(0,str(ROOT/'udt_three_spatial_smoke_2026-10-01'))
from clock_readout import History

def query(history,direction):
    te=history.times[0]+.2*(history.times[-1]-history.times[0]);to=history.times[0]+.8*(history.times[-1]-history.times[0])
    origin=np.array([.31,.47,.19]);direction=np.array(direction,dtype=float);direction/=np.linalg.norm(direction)
    g,_=history.sample(te,origin)
    if g[0,0]>=0:raise ValueError('CLOCK_OR_TIME_ORIENTATION')
    a=direction@g[1:,1:]@direction;b=g[0,1:]@direction;speed=(-b+np.sqrt(b*b-a*g[0,0]))/a;k=np.r_[1.,speed*direction]
    omega=-(g[0]@k)/np.sqrt(-g[0,0]);k/=omega;nulls=[]
    def rhs(t,y):
        x=y[:3];k=y[3:];g,conn=history.sample(t,x)
        if g[0,0]>=0 or k[0]<=0:raise ValueError('CLOCK_OR_TIME_ORIENTATION')
        nulls.append(float(abs(k@g@k)))
        return np.r_[k[1:]/k[0],-np.einsum('abc,b,c->a',conn,k,k)/k[0]]
    result=solve_ivp(rhs,(te,to),np.r_[origin,k],method='DOP853',rtol=2e-11,atol=2e-12,max_step=min(.005,(to-te)/8),dense_output=True)
    if not result.success:raise RuntimeError(result.message)
    end=result.y[:,-1];g,_=history.sample(to,end[:3])
    if g[0,0]>=0:raise ValueError('CLOCK_OR_TIME_ORIENTATION')
    omega=-(g[0]@end[3:])/np.sqrt(-g[0,0]);z=1/omega;sampled=[]
    for t in np.unique(np.r_[result.t,np.linspace(te,to,25)]):
        y=result.sol(t);metric,_=history.sample(t,y[:3]);sampled.append(float(abs(y[3:]@metric@y[3:])))
    if not np.isfinite(z) or z<=0 or max(sampled)>=2e-7:raise ValueError('NULL_OR_FREQUENCY_FAILURE')
    return dict(te=float(te),to=float(to),emitter_position=origin.tolist(),receiver_position=end[:3].tolist(),initial_coordinate_direction=direction.tolist(),emitted_frequency=1.,received_frequency=float(omega),Z=float(z),logZ=float(np.log(z)),max_sampled_abs_null_norm=max(sampled),max_internal_trial_abs_null_norm=max(nulls),sampled_null_points=len(sampled),function_evaluations=result.nfev)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('history');ap.add_argument('output');ap.add_argument('--kasner',action='store_true');args=ap.parse_args();start=time.monotonic()
    history=History(args.history);directions=[[1,0,0],[0,1,0]] if args.kasner else [[1,0,0],[0,1,0],[0,0,1],[1,1,1]]
    results=[query(history,d) for d in directions]
    if args.kasner:
        for row,power in zip(results,[-1/3,2/3]):
            row['exact_Z']=float(np.exp(power*(row['to']-row['te'])));row['exact_error']=abs(row['Z']-row['exact_Z'])
            if row['exact_error']>2e-7:raise ValueError('EXACT_CONTROL_FAILURE')
    report=dict(status='FINITE_CLOCK_CHECK_PASS',history=args.history,history_sha256=hashlib.sha256(Path(args.history).read_bytes()).hexdigest(),readouts=results,seconds=time.monotonic()-start,scope='Supplied fixed-coordinate clocks and regular null queries within one late window; no selected observers or gap-spanning ray')
    with Path(args.output).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report,indent=2))
