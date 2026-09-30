"""Parent diagnostics: exact NE1 and resolved-history/readout comparisons.

Same-author diagnostics; independent validation is in review/numerics.
"""
from pathlib import Path
import json, numpy as np
from scipy.special import jv,yv

ROOT=Path(__file__).resolve().parent

def load(name):
    p=ROOT/'runs'/name
    return np.load(p/'fields.npz'),json.loads((p/'metadata.json').read_text())

def exact_ne1(t,x,e,k=.75):
    a=-3*np.pi/4*yv(0,k);b=3*np.pi/4*jv(0,k)
    f=a*jv(0,k*t)+b*yv(0,k*t)
    fp=-k*(a*jv(1,k*t)+b*yv(1,k*t))
    ell=.5*t*t*(fp*fp+k*k*f*f)+.5*t*f*fp-9/8
    return np.array([e*f*np.cos(k*x),e*fp*np.cos(k*x),np.zeros_like(x),np.zeros_like(x),
                     4*np.log(.75)+e*e*(ell+.5*t*f*fp*np.cos(2*k*x))])

def pilot():
    a,ma=load('pilot_n32');b,mb=load('pilot_n64')
    exact_errors={}
    for data,name in [(a,'n32'),(b,'n64')]:
        truth=np.stack([exact_ne1(t,data['x'],.3) for t in data['times']])
        exact_errors[name]=float(np.max(np.abs(data['state'][:,1]-truth)))
    assert np.array_equal(a['times'],b['times'])
    difference=float(np.max(np.abs(a['state']-b['state'][...,::2])))
    result={'exact_ne1_max_absolute_error':exact_errors,'n32_n64_max_absolute_difference':difference,
       'max_constraint':[ma['max_constraint'],mb['max_constraint']],
       'scope':'same-author exact analytic and refinement checks, not independent CPU/Ricci gate'}
    assert max(exact_errors.values())<2e-6 and difference<2e-6
    (ROOT/'PILOT_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

def shift(a,d,k):
    n=a.shape[-1]; freq=np.fft.fftfreq(n,1/n)*k
    return np.fft.ifft(np.fft.fft(a,axis=-1)*np.exp(1j*freq*d),axis=-1).real

def clocks(data,metadata):
    t=data['times'];u=data['state'];k=metadata['spec']['k'];output=[]
    for te in (1.,4.,8.,16.):
        for d in (1.,2.,4.,8.):
            if te+d>t[-1]:continue
            ie=np.flatnonzero(np.isclose(t,te,rtol=0,atol=1e-12))
            io=np.flatnonzero(np.isclose(t,te+d,rtol=0,atol=1e-12))
            if len(ie)!=1 or len(io)!=1:continue
            diff=(shift(u[io[0],:,4],d,k)-u[ie[0],:,4])/4
            logz=diff-.25*np.log((te+d)/te)
            for j,c in enumerate(metadata['spec']['cases']):
                output.append({'id':c['id'],'te':te,'d':d,'logZ_min':float(logz[j].min()),
                    'logZ_max':float(logz[j].max()),'logZ_mean':float(logz[j].mean()),
                    'delta_logZ_vs_homogeneous_min':float(diff[j].min()),
                    'delta_logZ_vs_homogeneous_max':float(diff[j].max())})
    return output

if __name__=='__main__':pilot()
