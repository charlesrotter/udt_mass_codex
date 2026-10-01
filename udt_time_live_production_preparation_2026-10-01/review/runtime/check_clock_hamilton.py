"""TPP1 adapter of the TDS1 separate Hamilton/RK45 clock checker.

No producer imports. Reuses its reviewed equations, metric interpolation and
accepted-node null diagnostic; this is not a new independent mathematical method.
Each history is queried at 20% and 80% of its saved time span, fixed before results.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicHermiteSpline

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PRIOR=ROOT/'udt_three_spatial_smoke_2026-10-01/review/data_recovery/check_clock_hamilton.py'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

class Metric:
    def __init__(self,path):
        with np.load(path,allow_pickle=False) as data:
            self.times=data['times'];self.n=data['g'].shape[1]
            period=float(data['period'])
            coeff=np.fft.fftn(data['g'],axes=(1,2,3))/self.n**3
            velocity=np.fft.fftn(data['v'],axes=(1,2,3))/self.n**3
        assert len(self.times)>=5 and np.all(np.diff(self.times)>0)
        assert np.isfinite(coeff).all() and np.isfinite(velocity).all()
        self.spline=CubicHermiteSpline(self.times,coeff,velocity,axis=0,extrapolate=False)
        self.wave=np.array(np.meshgrid(*([2*np.pi*np.fft.fftfreq(self.n,d=period/self.n)]*3),indexing='ij'))

    def sample(self,t,x):
        coeff=self.spline(t)
        phase=np.exp(1j*np.einsum('aijk,a->ijk',self.wave,x))
        metric=np.einsum('ijk,ijkab->ab',phase,coeff).real
        time_derivative=np.einsum('ijk,ijkab->ab',phase,self.spline(t,1)).real
        space_derivative=np.einsum('dijk,ijk,ijkab->dab',1j*self.wave,phase,coeff).real
        return metric,np.concatenate((time_derivative[None],space_derivative),axis=0)

def ray(metric,direction):
    origin=np.array([.31,.47,.19]);direction=np.asarray(direction,dtype=float)
    direction/=np.linalg.norm(direction)
    start,end=float(metric.times[0]),float(metric.times[-1]);span=end-start
    emission,reception=start+.2*span,start+.8*span
    g,_=metric.sample(emission,origin)
    spatial=direction@g[1:,1:]@direction;mixed=g[0,1:]@direction
    coordinate_speed=(-mixed+np.sqrt(mixed*mixed-spatial*g[0,0]))/spatial
    k=np.r_[1.,coordinate_speed*direction];p=g@k
    p/=(-p[0]/np.sqrt(-g[0,0]))
    norms=[]
    def ode(t,state):
        g,dg=metric.sample(t,state[:3]);p=state[3:];k=np.linalg.solve(g,p)
        assert k[0]>0 and g[0,0]<0
        norms.append(abs(p@k))
        dp=.5*np.einsum('mab,a,b->m',dg,k,k)/k[0]
        return np.r_[k[1:]/k[0],dp]
    solve=solve_ivp(ode,(emission,reception),np.r_[origin,p],method='RK45',
        rtol=1e-11,atol=1e-12,max_step=min(.003,(reception-emission)/20),dense_output=True)
    assert solve.success
    endpoint=solve.y[:,-1];final_g,_=metric.sample(reception,endpoint[:3])
    received=-endpoint[3]/np.sqrt(-final_g[0,0]);assert received>0
    accepted_norms=[]
    for t in np.unique(np.r_[solve.t,np.linspace(emission,reception,25)]):
        state=solve.sol(t);g,_=metric.sample(t,state[:3]);p=state[3:]
        accepted_norms.append(abs(p@np.linalg.solve(g,p)))
    return dict(Z=float(1/received),logZ=float(-np.log(received)),emission=emission,reception=reception,
        receiver_position=endpoint[:3].tolist(),initial_coordinate_direction=direction.tolist(),
        max_sampled_abs_null_norm=float(max(accepted_norms)),
        max_internal_trial_abs_null_norm=float(max(norms)),nfev=solve.nfev)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('queries')
    args=parser.parse_args();spec=json.loads(Path(args.queries).read_text())
    reports={};sources={}
    for case in spec['cases']:
        path=ROOT/case['history'];metric=Metric(path);name=case['name']
        sources[case['history']]=sha(path)
        directions=([1,0,0],[0,1,0]) if case.get('kasner') else ([1,0,0],[0,1,0],[0,0,1],[1,1,1])
        reports[name]=[ray(metric,d) for d in directions]
        for row in reports[name]:assert row['max_sampled_abs_null_norm']<2e-7,(name,row)
        if case.get('kasner'):
            for row,power in zip(reports[name],[-1/3,2/3]):
                row['exact_error']=abs(row['Z']-np.exp(power*(row['reception']-row['emission'])))
                assert row['exact_error']<2e-7,(name,row)
    print(json.dumps(dict(status='HAMILTON_CLOCK_REVIEW_PASS',readouts=reports,
        history_sha256=sources,queries_sha256=sha(args.queries),checker_sha256=sha(__file__),
        reused_prior_checker_sha256=sha(PRIOR),
        scope='Separate covariant-momentum/RK45 implementation from producer; explicitly adapted prior reviewer code. Shared saved fields, Fourier/Hermite mathematics and conditional geometry.'),indent=2,sort_keys=True))

if __name__=='__main__':main()
