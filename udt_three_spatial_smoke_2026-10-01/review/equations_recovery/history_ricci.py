#!/usr/bin/env python3
"""Independent original Ricci from g-only histories; no producer imports.

Coordinate components are comparison diagnostics, not invariant error bounds.
Five-point centered time differences omit two saved slices at either endpoint.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def spatial_derivative(a, axis, period, second_axis=None):
    n = a.shape[axis]
    frequency = 2*np.pi*np.fft.fftfreq(n, d=period/n)
    shape = [1]*a.ndim
    shape[axis] = n
    factor = 1j*frequency.reshape(shape)
    if second_axis is not None:
        m = a.shape[second_axis]
        shape = [1]*a.ndim
        shape[second_axis] = m
        factor = factor*(1j*2*np.pi*np.fft.fftfreq(m, d=period/m).reshape(shape))
    return np.fft.ifftn(factor*np.fft.fftn(a, axes=(0,1,2)), axes=(0,1,2)).real


def metric_jets(history, times, index, period):
    dt = float(times[1]-times[0])
    g = history[index]
    d = np.zeros(g.shape[:-2]+(4,4,4))
    dd = np.zeros(g.shape[:-2]+(4,4,4,4))
    d[...,0,:,:] = (history[index-2]-8*history[index-1]+8*history[index+1]-history[index+2])/(12*dt)
    dd[...,0,0,:,:] = (-history[index-2]+16*history[index-1]-30*g+16*history[index+1]-history[index+2])/(12*dt*dt)
    for i in range(3):
        d[...,i+1,:,:] = spatial_derivative(g,i,period)
        mixed = spatial_derivative(d[...,0,:,:],i,period)
        dd[...,0,i+1,:,:] = mixed
        dd[...,i+1,0,:,:] = mixed
        for j in range(3):
            dd[...,i+1,j+1,:,:] = spatial_derivative(g,i,period,j)
    return g,d,dd


def original_ricci(g,d,dd):
    """Construct Gamma, partial Gamma, then original Ricci, independently of RHS."""
    inverse = np.linalg.inv(g)
    if not np.all(np.isfinite(inverse)) or np.any(inverse[...,0,0]>=0):
        raise ValueError('NONSPACELIKE_SLICE_OR_INVALID_INVERSE')
    dinverse = -np.einsum('...ac,...kcd,...db->...kab',inverse,d,inverse)
    lower = np.empty(g.shape[:-2]+(4,4,4))
    dlower = np.empty(g.shape[:-2]+(4,4,4,4))
    for b in range(4):
        for m in range(4):
            for n in range(4):
                lower[...,b,m,n] = (d[...,m,b,n]+d[...,n,b,m]-d[...,b,m,n])/2
                for k in range(4):
                    dlower[...,k,b,m,n] = (dd[...,k,m,b,n]+dd[...,k,n,b,m]-dd[...,k,b,m,n])/2
    connection = np.einsum('...ab,...bmn->...amn',inverse,lower)
    dconnection = (np.einsum('...kab,...bmn->...kamn',dinverse,lower)
                   + np.einsum('...ab,...kbmn->...kamn',inverse,dlower))
    ricci = np.zeros_like(g)
    for m in range(4):
        for n in range(4):
            for a in range(4):
                ricci[...,m,n] += dconnection[...,a,a,m,n]-dconnection[...,n,a,m,a]
                for b in range(4):
                    ricci[...,m,n] += (connection[...,a,m,n]*connection[...,b,a,b]
                                      - connection[...,a,m,b]*connection[...,b,n,a])
    harmonic = np.einsum('...mn,...amn->...a',inverse,connection)
    # ADM normal n^mu=(-g^00)^(-1/2)(-g^mu0) evaluated from the saved metric.
    normal = -inverse[..., :, 0]/np.sqrt(-inverse[...,0,0])[...,None]
    scalar = np.einsum('...mn,...mn->...',inverse,ricci)
    einstein = ricci-g*scalar[...,None,None]/2
    normal_projection = np.einsum('...mn,...n->...m',einstein,normal)
    return ricci,harmonic,normal_projection


def analyze(history,times,period):
    if history.dtype != np.float64 or history.ndim!=6 or history.shape[-2:]!=(4,4):
        raise ValueError('INVALID_HISTORY_SCHEMA')
    if len(times)!=len(history) or len(times)<5 or not np.all(np.isfinite(history)):
        raise ValueError('INVALID_HISTORY_VALUES')
    if not np.isfinite(period) or period<=0 or not np.all(np.isfinite(times)):
        raise ValueError('INVALID_COORDINATES')
    if times[1]<=times[0] or np.max(abs(np.diff(times)-(times[1]-times[0])))>1e-12:
        raise ValueError('NONUNIFORM_TIME_HISTORY')
    rows=[]
    for index in range(2,len(times)-2):
        ricci,harmonic,constraint=original_ricci(*metric_jets(history,times,index,period))
        if not all(np.all(np.isfinite(a)) for a in (ricci,harmonic,constraint)):
            raise ValueError('NONFINITE_ORIGINAL_GEOMETRY')
        rows.append({'index':index,'time':float(times[index]),
                     'ricci_max':float(abs(ricci).max()),
                     'ricci_rms':float(np.sqrt(np.mean(ricci**2))),
                     'harmonic_max':float(abs(harmonic).max()),
                     'einstein_normal_projection_max':float(abs(constraint).max())})
    return {'shape':list(history.shape),'period':float(period),'dt':float(times[1]-times[0]),
            'tested_time_slices':len(rows),'points_per_slice':int(np.prod(history.shape[1:4])),
            'endpoint_omissions':2,'rows':rows,
            **{name:max(row[name] for row in rows) for name in ['ricci_max','ricci_rms','harmonic_max','einstein_normal_projection_max']}}


def own_kasner(times,n=4,p=(-1/3,2/3,2/3)):
    metric=np.zeros((len(times),n,n,n,4,4),dtype=np.float64)
    rates=(1.,*p)
    for i,r in enumerate(rates):metric[...,i,i]=((-1 if i==0 else 1)*np.exp(2*r*(times-1)))[:,None,None,None]
    return metric


def selftest():
    results=[]
    for dt in [.005,.0025]:
        times=1+np.arange(round(.1/dt)+1)*dt
        good=analyze(own_kasner(times),times,2*np.pi)
        bad=analyze(own_kasner(times,p=(.2,.3,.5)),times,2*np.pi)
        assert good['ricci_max']<1e-7 and good['harmonic_max']<1e-8
        assert bad['ricci_max']>.5
        results.append({'dt':dt,'good_max':good['ricci_max'],'bad_max':bad['ricci_max']})
    # Exact independent curvature anchor: flat FLRW with a(t)=exp(h*t), h=.2.
    h=.2;t=.17;g=np.diag([-1.,*([np.exp(2*h*t)]*3)])
    d=np.zeros((4,4,4));dd=np.zeros((4,4,4,4))
    for i in range(1,4):d[0,i,i]=2*h*g[i,i];dd[0,0,i,i]=4*h*h*g[i,i]
    ric,_,_=original_ricci(g,d,dd)
    expected=np.diag([-3*h*h,*([3*h*h*np.exp(2*h*t)]*3)])
    error=float(abs(ric-expected).max());assert error<1e-14
    return {'status':'SELFTEST_PASS','analytic_flrw_ricci_error':error,'kasner_fd_checks':results}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('output')
    parser.add_argument('histories',nargs='*')
    parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args();started=time.monotonic()
    if args.selftest:result=selftest()
    else:
        result={'status':'MEASURED_ORIGINAL_RICCI','histories':[]}
        for path in args.histories:
            with np.load(path,allow_pickle=False) as data:
                detail=analyze(data['g'],data['times'],float(data['period']))
                if 'kasner' in Path(path).as_posix().lower():
                    detail['own_analytic_kasner_metric_error']=float(abs(data['g']-own_kasner(data['times'],data['g'].shape[1])).max())
            detail.update(path=str(Path(path).resolve()),sha256=sha(path))
            result['histories'].append(detail)
    result.update(source_sha256=sha(__file__),numpy=np.__version__,seconds=time.monotonic()-started,
                  producer_imports=False,producer_velocities_or_accelerations_used=False,
                  scope='Original coordinate Ricci and normal Einstein projections from all interior metric-only saved slices; finite-difference/Fourier floating-point diagnostics, not continuum certification.')
    with Path(args.output).open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
