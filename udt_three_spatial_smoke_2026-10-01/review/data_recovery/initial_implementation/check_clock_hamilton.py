"""Independent covariant-momentum ray integration from saved full metric."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicHermiteSpline

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent

class Metric:
    def __init__(self,path):
        with np.load(path,allow_pickle=False) as data:
            self.times=data['times'];self.n=data['g'].shape[1]
            period=float(data['period'])
            coeff=np.fft.fftn(data['g'],axes=(1,2,3))/self.n**3
            velocity=np.fft.fftn(data['v'],axes=(1,2,3))/self.n**3
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
    emission,reception=1.02,1.08
    g,_=metric.sample(emission,origin)
    spatial=direction@g[1:,1:]@direction
    mixed=g[0,1:]@direction
    coordinate_speed=(-mixed+np.sqrt(mixed*mixed-spatial*g[0,0]))/spatial
    k=np.r_[1.,coordinate_speed*direction]
    p=g@k
    p/=(-p[0]/np.sqrt(-g[0,0]))
    norms=[]
    def ode(t,state):
        g,dg=metric.sample(t,state[:3])
        p=state[3:];k=np.linalg.solve(g,p)
        assert k[0]>0 and g[0,0]<0
        norms.append(abs(p@k))
        dp=.5*np.einsum('mab,a,b->m',dg,k,k)/k[0]
        return np.r_[k[1:]/k[0],dp]
    solve=solve_ivp(ode,(emission,reception),np.r_[origin,p],method='RK45',rtol=1e-11,atol=1e-12,max_step=.003)
    assert solve.success
    endpoint=solve.y[:,-1]
    final_g,_=metric.sample(reception,endpoint[:3])
    received=-endpoint[3]/np.sqrt(-final_g[0,0])
    assert received>0
    return dict(Z=float(1/received),logZ=float(-np.log(received)),
                receiver_position=endpoint[:3].tolist(),
                initial_coordinate_direction=direction.tolist(),
                max_sampled_abs_null_norm=float(max(norms)),nfev=solve.nfev)

reports={};source={}
for name in ('kasner_half','n16_half'):
    path=BASE/'histories'/f'{name}.npz';metric=Metric(path)
    source[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    directions=([1,0,0],[0,1,0]) if name=='kasner_half' else ([1,0,0],[0,1,0],[0,0,1],[1,1,1])
    reports[name]=[ray(metric,d) for d in directions]
    for row in reports[name]:assert row['max_sampled_abs_null_norm']<2e-7
for row,power in zip(reports['kasner_half'],[-1/3,2/3]):
    row['exact_error']=abs(row['Z']-np.exp(power*.06))
    assert row['exact_error']<2e-7
comparison=None
producer=BASE/'CLOCK_READOUT.json'
if producer.exists():
    other=json.loads(producer.read_text())
    comparison={name:max(abs(a['logZ']-b['logZ']) for a,b in zip(rows,other['readouts'][name])) for name,rows in reports.items()}
    assert max(comparison.values())<2e-7
print(json.dumps(dict(status='HAMILTON_CLOCK_REVIEW_PASS',readouts=reports,
    producer_logZ_differences=comparison,history_sha256=source,
    checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    scope='Distinct covariant-momentum equations and RK45 integration; independent implementation of metric sampling with SciPy Hermite. Shared saved fields and Fourier/Hermite mathematical methods, not independent data or discretization.'),indent=2,sort_keys=True))
