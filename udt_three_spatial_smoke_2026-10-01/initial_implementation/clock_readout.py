"""Supplied-clock readouts on saved conditional geometries; no observer selection."""
import hashlib,json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
B=Path(__file__).resolve().parent

class History:
    def __init__(self,path):
        with np.load(path,allow_pickle=False) as d:
            self.times=d['times'];self.n=d['g'].shape[1];self.period=float(d['period'])
            self.g=np.fft.fftn(d['g'],axes=(1,2,3))/self.n**3
            self.v=np.fft.fftn(d['v'],axes=(1,2,3))/self.n**3
        self.freq=np.meshgrid(*([2*np.pi*np.fft.fftfreq(self.n,d=self.period/self.n)]*3),indexing='ij')
    def sample(self,t,x):
        if not self.times[0]-1e-12<=t<=self.times[-1]+1e-12:raise ValueError('OUTSIDE_SAVED_TIME_SLAB')
        i=np.clip(np.searchsorted(self.times,t,side='right')-1,0,len(self.times)-2)
        h=self.times[i+1]-self.times[i];u=(t-self.times[i])/h
        f=(2*u**3-3*u*u+1)*self.g[i]+h*(u**3-2*u*u+u)*self.v[i]+(-2*u**3+3*u*u)*self.g[i+1]+h*(u**3-u*u)*self.v[i+1]
        ft=((6*u*u-6*u)/h)*self.g[i]+(3*u*u-4*u+1)*self.v[i]+((-6*u*u+6*u)/h)*self.g[i+1]+(3*u*u-2*u)*self.v[i+1]
        phase=np.exp(1j*sum(k*xj for k,xj in zip(self.freq,x)))
        def value(a):return np.einsum('ijk,ijkab->ab',phase,a,optimize=False).real
        g=value(f);dg=np.stack([value(ft),*[value(1j*k[...,None,None]*f) for k in self.freq]])
        inv=np.linalg.inv(g);conn=np.empty((4,4,4))
        for a in range(4):
            for b in range(4):
                for c in range(4):conn[a,b,c]=sum(inv[a,d]*(dg[b,d,c]+dg[c,d,b]-dg[d,b,c])/2 for d in range(4))
        return g,conn

def query(history,direction):
    te,to=1.02,1.08;origin=np.array([.31,.47,.19]);direction=np.array(direction,dtype=float);direction/=np.linalg.norm(direction)
    g,_=history.sample(te,origin);a=direction@g[1:,1:]@direction;b=g[0,1:]@direction
    speed=(-b+np.sqrt(b*b-a*g[0,0]))/a;k=np.r_[1.,speed*direction]
    omega=-(g[0]@k)/np.sqrt(-g[0,0]);k/=omega
    nulls=[]
    def rhs(t,y):
        x=y[:3];k=y[3:];g,conn=history.sample(t,x)
        if g[0,0]>=0 or k[0]<=0:raise ValueError('CLOCK_OR_TIME_ORIENTATION')
        nulls.append(float(abs(k@g@k)))
        return np.r_[k[1:]/k[0],-np.einsum('abc,b,c->a',conn,k,k)/k[0]]
    result=solve_ivp(rhs,(te,to),np.r_[origin,k],method='DOP853',rtol=2e-11,atol=2e-12,max_step=.005)
    if not result.success:raise RuntimeError(result.message)
    end=result.y[:,-1];g,_=history.sample(to,end[:3]);omega=-(g[0]@end[3:])/np.sqrt(-g[0,0])
    z=1/omega
    assert np.isfinite(z) and z>0 and max(nulls)<2e-7,(z,max(nulls))
    return {'te':te,'to':to,'emitter_position':origin.tolist(),'receiver_position':end[:3].tolist(),
            'initial_coordinate_direction':direction.tolist(),'emitted_frequency':1.,'received_frequency':float(omega),
            'Z':float(z),'logZ':float(np.log(z)),'max_sampled_abs_null_norm':max(nulls),'function_evaluations':result.nfev,
            'receiver':'fixed-coordinate timelike clock at computed arrival position; not a selected cosmological observer'}

def main():
    start=time.monotonic();results={};hashes={}
    for name in ['kasner','kasner_half','n8_repaired','n12','n16','n16_half']:
        p=B/'histories'/f'{name}.npz';history=History(p);hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        directions=[[1,0,0],[0,1,0]] if name.startswith('kasner') else [[1,0,0],[0,1,0],[0,0,1],[1,1,1]]
        results[name]=[query(history,d) for d in directions]
        if name.startswith('kasner'):
            for row,power in zip(results[name],[-1/3,2/3]):
                row['exact_Z']=float(np.exp(power*(row['to']-row['te'])))
                row['exact_error']=abs(row['Z']-row['exact_Z']);assert row['exact_error']<2e-7
    differences={name:max(abs(a['logZ']-b['logZ']) for a,b in zip(results[name],results['n16_half'])) for name in ['n8_repaired','n12','n16']}
    assert differences['n16']<2e-7
    if differences['n8_repaired']>1e-9:assert differences['n12']<differences['n8_repaired']/10
    report={'status':'MARKED_CLOCK_CHECK_PASS','scope':'finite queries on conditional saved metric; supplied fixed-coordinate clocks and rays',
            'interpolation':'spatial Fourier, cubic Hermite time using saved g and v; DOP853 null geodesics',
            'query_convention':'Z=emitted frequency/received frequency=received tick interval/emitted tick interval',
            'histories_sha256':hashes,'readouts':results,'max_logZ_changes_against_n16_half':differences,'seconds':time.monotonic()-start}
    with (B/'CLOCK_READOUT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k!='readouts'},indent=2))

if __name__=='__main__':main()
