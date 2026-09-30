"""Conditional two-Killing Ric=0 numerical histories; no native UDT selection."""
from pathlib import Path
import argparse, hashlib, json, math, time
import numpy as np
import torch

torch.set_num_threads(1)
DTYPE=torch.float64

def coefficients(x, modes):
    result=np.zeros_like(x)
    for m,a,p in modes:
        result += a*np.cos(m*x+p)
    return result

def initial(spec):
    n,k=spec['n'],spec['k']; theta=np.arange(n)*2*np.pi/n
    wave=np.fft.fftfreq(n,1/n)*k
    def dx(a): return np.fft.ifft(1j*wave*np.fft.fft(a)).real
    states=[]; projections=[]
    for c in spec['cases']:
        p,v,q,w=[coefficients(theta,c.get(key,[])) for key in ('P','V','Q','W')]
        px,qx=dx(p),dx(q)
        momentum=v*px+np.exp(2*p)*w*qx
        denom=np.mean(px**2)
        alpha=0.
        if denom>1e-24:
            alpha=np.mean(momentum)/denom
            v=v-alpha*px
        else:
            assert abs(np.mean(momentum))<1e-12, 'invalid periodic initial constraint'
        momentum=v*px+np.exp(2*p)*w*qx
        assert abs(np.mean(momentum))<1e-12
        rhs=2*momentum
        coeff=np.fft.fft(rhs); primitive=np.zeros(n,dtype=complex)
        primitive[1:]=coeff[1:]/(1j*wave[1:])
        lam=np.fft.ifft(primitive).real+4*np.log(.75)
        # Initial Nyquist/aliasing incompatibility is checked, never discarded.
        err=np.max(np.abs(dx(lam)-rhs))
        states.append(np.array([p,v,q,w,lam]))
        projections.append({'id':c['id'],'alpha':float(alpha),'initial_constraint_max':float(err)})
    return np.array(states),projections

def engine(n,k,device):
    wave=torch.fft.fftfreq(n,d=1/n,device=device,dtype=DTYPE)*k
    def dx(a): return torch.fft.ifft(1j*wave*torch.fft.fft(a,dim=-1),dim=-1).real
    def rhs(t,u):
        p,v,q,w,lam=u.unbind(1)
        ft=torch.fft.fft(torch.stack((p,q),dim=1),dim=-1)
        grads=torch.fft.ifft(1j*wave*ft,dim=-1).real
        seconds=torch.fft.ifft(-wave**2*ft,dim=-1).real
        px,qx=grads.unbind(1); pxx,qxx=seconds.unbind(1)
        e=torch.exp(2*p)
        return torch.stack((v,pxx-v/t+e*(w*w-qx*qx),w,
                            qxx-w/t-2*(v*w-px*qx),
                            t*(v*v+px*px+e*(w*w+qx*qx))),dim=1)
    return dx,rhs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('spec');ap.add_argument('output')
    args=ap.parse_args(); spec=json.loads(Path(args.spec).read_text())
    out=Path(args.output); assert not out.exists(), 'refuse grid artifact overwrite'
    out.mkdir(parents=True)
    assert spec['n'] in (32,64,128,256) and len(spec['cases'])<=64
    assert spec['device']=='cuda' and torch.cuda.is_available()
    props=torch.cuda.get_device_properties(0)
    torch.cuda.reset_peak_memory_stats()
    start=time.monotonic(); raw, projections=initial(spec)
    u=torch.as_tensor(raw,dtype=DTYPE,device='cuda'); dx,rhs=engine(spec['n'],spec['k'],'cuda')
    t=1.; dt=spec['dt']; end=spec['end']
    regular=np.arange(1,end+1e-9,spec['snapshot_dt']).tolist()
    targets=set(regular+[end])
    for center in spec['stencil_centers']:
        for h in (.004,.002):
            targets.update(float(center+j*h) for j in range(-4,5))
    targets=sorted(x for x in targets if 1<=x<=end)
    times=[t]; states=[raw]; diagnostics=[]; steps=0
    for target in targets[1:]:
        while t<target-1e-12:
            h=min(dt,target-t)
            a=rhs(t,u); b=rhs(t+h/2,u+h*a/2)
            c=rhs(t+h/2,u+h*b/2); d=rhs(t+h,u+h*c)
            u=u+h*(a+2*b+2*c+d)/6; t+=h; steps+=1
        t=target
        p,v,q,w,lam=u.unbind(1)
        momentum=dx(lam)-2*t*(v*dx(p)+torch.exp(2*p)*w*dx(q))
        ft=torch.fft.fft(u,dim=-1)/spec['n']
        modes=torch.fft.fftfreq(spec['n'],d=1/spec['n'],device='cuda').abs()
        tail=ft[...,modes>=spec['n']/3].abs().amax().item()
        constraint=momentum.abs().amax().item()
        finite=bool(torch.isfinite(u).all())
        elapsed=time.monotonic()-start
        info={'t':t,'constraint_max':constraint,'tail_max':tail,'finite':finite}
        diagnostics.append(info)
        states.append(u.detach().cpu().numpy());times.append(t)
        if not finite or constraint>spec['constraint_stop'] or elapsed>550:
            np.savez_compressed(out/'failure.npz',times=np.array(times),state=np.stack(states),x=np.arange(spec['n'])*2*np.pi/spec['k']/spec['n'])
            (out/'FAILURE.json').write_text(json.dumps({'diagnostic':info,'elapsed':elapsed,'reason':'finite/constraint/time stop'},indent=2))
            raise RuntimeError('run stopped; diagnostic artifacts retained')
        assert torch.cuda.max_memory_allocated()<24*1024**3
    torch.cuda.synchronize()
    x=np.arange(spec['n'])*2*np.pi/spec['k']/spec['n']
    np.savez_compressed(out/'fields.npz',times=np.array(times),state=np.stack(states),x=x)
    metadata={'spec':spec,'spec_sha256':hashlib.sha256(Path(args.spec).read_bytes()).hexdigest(),
       'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'device':props.name,'torch':torch.__version__,'numpy':np.__version__,
       'dtype':'float64','shape':list(np.stack(states).shape),'steps':steps,
       'elapsed_seconds':time.monotonic()-start,'peak_gpu_allocated_bytes':torch.cuda.max_memory_allocated(),
       'initial_projections':projections,'max_constraint':max(x['constraint_max'] for x in diagnostics),
       'max_tail':max(x['tail_max'] for x in diagnostics),'diagnostics':diagnostics}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({k:v for k,v in metadata.items() if k not in ('spec','diagnostics','initial_projections')}))

if __name__=='__main__':main()
