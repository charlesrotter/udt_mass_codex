"""Direct fidelity check from saved scale factors; no parent imports or RHS use."""
from pathlib import Path
import hashlib,json,math,platform
import numpy as np
import scipy
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
summary=json.loads((ROOT/'parent_full/summary.json').read_text())
pins={}
for file in ['PARENT_CANDIDATE_FREEZE.json','PARENT_OUTPUT_FREEZE.json']:
    data=json.loads((ROOT/file).read_text())
    for name,want in data['sha256'].items():
        got=hashlib.sha256(Path(name).read_bytes()).hexdigest()
        assert got==want,(name,got,want)
        pins[name]=got

gx,gw=np.polynomial.legendre.leggauss(16)
def integrate(f,lo,hi):
    return float((hi-lo)*np.dot(gw,f((hi-lo)*gx/2+(hi+lo)/2))/2)

class Clock:
    def __init__(self,t,a):
        self.t=t; self.a=CubicSpline(t,a)
        increments=[integrate(lambda x:1/self.a(x),l,r) for l,r in zip(t[:-1],t[1:])]
        self.eta=np.r_[0.,np.cumsum(increments)]
    def conformal(self,t):
        j=min(np.searchsorted(self.t,t,side='right')-1,len(self.t)-2)
        assert 0<=j<len(self.t)-1
        return self.eta[j]+integrate(lambda x:1/self.a(x),self.t[j],t)
    def arrival(self,start,distance):
        target=self.conformal(start)+distance
        if target>self.eta[-1]:return None
        j=max(0,min(np.searchsorted(self.eta,target)-1,len(self.t)-2))
        return float(brentq(lambda x:self.eta[j]+integrate(lambda y:1/self.a(y),
            self.t[j],x)-target,self.t[j],self.t[j+1],xtol=2e-14,rtol=1e-14))
    def readout(self,start,L):
        tb=self.arrival(start,L);tf=self.arrival(start,2*L)
        if tb is None:return {'status':'FIRST_NOT_REACHED_WITHIN_WINDOW'}
        p=float(self.a(tb)/self.a(start))
        if tf is None:return dict(status='ECHO_NOT_REACHED_WITHIN_WINDOW',first_arrival=tb,p=p)
        return dict(status='BOTH_REACHED',first_arrival=tb,echo_arrival=tf,p=p,
            q=float(self.a(tf)/self.a(tb)),total=float(self.a(tf)/self.a(start)))

# Eleven-point exact derivative weights; actual state used is a, not H or R.
weights={d:np.array([float(x) for x in s.finite_diff_weights(d,list(range(-5,6)),0)[d][-1]])
         for d in range(1,5)}
def metric_residual(t,a,Lambda):
    dt=t[1]-t[0];ac=a[5:-5]
    a1,a2,a3,a4=[np.correlate(a,weights[d],mode='valid')/dt**d for d in range(1,5)]
    H=a1/ac
    Hd=a2/ac-H**2
    Hdd=a3/ac-3*H*Hd-H**3
    Hddd=a4/ac-4*H*Hdd-3*Hd**2-6*H**2*Hd-H**4
    R=6*(Hd+2*H**2)
    Rp=6*(Hdd+4*H*Hd)
    Rpp=6*(Hddd+4*Hd**2+4*H*Hdd)
    Q00=-6*R*(Hd+H**2)+R*R/2+6*H*Rp
    Qii=2*R*(Hd+3*H**2)-R*R/2-2*Rpp-4*H*Rp
    E00=3*H**2+Q00-Lambda
    Eii=-2*Hd-3*H**2+Qii+Lambda
    n0=1+3*H**2+np.abs(Q00)+abs(Lambda)
    ni=1+2*np.abs(Hd)+3*H**2+np.abs(Qii)+abs(Lambda)
    return {'normalized':float(max(max(abs(E00/n0)),max(abs(Eii/ni)))),
        'absolute':float(max(max(abs(E00)),max(abs(Eii)))),
        'sample_count':len(ac),'time_interval':[float(t[5]),float(t[-6])]}

records=[]; finite=[]; maxerr=0.; maxres=0.; maxmap=0.; maxfinite=0.
for case in summary['cases']:
    entry={'id':case['id'],'grids':[]}
    refs=case['levels'][2]['clocks']
    for grid in [32,64,128]:
        path=ROOT/'parent_full'/case['id']/'level_2'/f'grid_{grid}.npz'
        with np.load(path) as data:
            t=data['t'].copy();a=data['y'][3].copy()
        clock=Clock(t,a)
        row={'grid':grid,'original_metric_residual':metric_residual(t,a,case['Lambda']),'clocks':[]}
        for ref in refs:
            readout=clock.readout(0.,ref['L'])
            assert readout['status']==ref['status']
            errors={k:abs(readout[k]-ref[k]) for k in ['first_arrival','echo_arrival','p','q','total'] if k in ref}
            row['clocks'].append(dict(L=ref['L'],readout=readout,errors=errors))
            if grid==128:
                for k,e in errors.items():assert e<=1e-7*(1+abs(ref[k])),(case['id'],k,e)
                maxerr=max(maxerr,*errors.values())
        entry['grids'].append(row)
        if grid==128:
            maxres=max(maxres,row['original_metric_residual']['normalized'])
            assert row['original_metric_residual']['normalized']<=1e-7,(case['id'],row['original_metric_residual'])
            # Finite proper interval: direct correspondence vs integrated local slope.
            L=.25;delta=.01;start=.1
            first=lambda ss:clock.arrival(ss,L)
            echo=lambda ss:clock.arrival(ss,2*L)
            interval_first=first(start+delta)-first(start)
            interval_echo=echo(start+delta)-echo(start)
            ip=integrate(lambda ss:np.array([clock.a(first(v))/clock.a(v) for v in ss]),start,start+delta)
            it=integrate(lambda ss:np.array([clock.a(echo(v))/clock.a(v) for v in ss]),start,start+delta)
            ferr=max(abs(interval_first-ip),abs(interval_echo-it))
            maxfinite=max(maxfinite,ferr);assert ferr<1e-10
            ss=.5;dd=1e-5
            dfirst=(first(ss+dd)-first(ss-dd))/(2*dd)
            decho=(echo(ss+dd)-echo(ss-dd))/(2*dd)
            expected_first=float(clock.a(first(ss))/clock.a(ss))
            expected_echo=float(clock.a(echo(ss))/clock.a(ss))
            merr=max(abs(dfirst-expected_first),abs(decho-expected_echo))
            maxmap=max(maxmap,merr);assert merr<1e-7
            finite.append({'id':case['id'],'emission_start':start,'emission_interval':delta,
                'reception_interval':interval_first,'echo_interval':interval_echo,
                'integral_error':ferr,'map_derivative_error':merr,
                'instantaneous_times_interval_difference':interval_first-float(clock.a(first(start))/clock.a(start))*delta})
    records.append(entry)

# Flat-event series from repeated differentiation of independently derived evolution.
H,R,P,al,La,bb=s.symbols('H R P alpha Lambda b', nonzero=True)
velocity=[R/6-2*H**2,P,-3*H*P-(R-4*La)/(6*al),H*bb]
vars=[H,R,P,bb]
derivative=lambda expr:s.expand(sum(s.diff(expr,v)*rhs for v,rhs in zip(vars,velocity)))
vals={H:0,R:0,La:0,bb:1}
current=bb;series={}
for n in range(1,6):
    current=derivative(current)
    series[str(n)]=str(s.simplify(current.subs(vals)/s.factorial(n)))
assert series=={'1':'0','2':'0','3':'P/36','4':'0','5':'-P/(4320*alpha)'},series
cubic=[]
for case in summary['cases']:
    if case['id']=='flat_event':
        for row in case['levels'][2]['cubic']:
            lp=math.log(row['p']);lq=math.log(row['q']);L=row['L']
            cubic.append({'L':L,'logp':lp,'logq':lq,
                'normalized_cubic_p':lp/L**3,'normalized_cubic_q':lq/L**3,
                'p_relative_cubic_error':abs(lp/row['predicted_log_p']-1),
                'q_relative_cubic_error':abs(lq/row['predicted_log_q']-1)})
    if case['id']=='contracting':
        assert all(row['p']<1 and row['q']<1 for row in case['levels'][2]['clocks'])
assert all(cubic[i+1]['p_relative_cubic_error']<cubic[i]['p_relative_cubic_error'] for i in range(2))
assert all(cubic[i+1]['q_relative_cubic_error']<cubic[i]['q_relative_cubic_error'] for i in range(2))
result={'status':'PASS','versions':{'python':platform.python_version(),'numpy':np.__version__,
    'scipy':scipy.__version__,'sympy':s.__version__},'parent_files_hash_verified':len(pins),
    'source':'tight parent saved a(t) only, three sample grids, no eta/H/R/P use in clock or tensor reconstruction',
    'maximum_clock_difference':maxerr,'maximum_metric_original_residual':maxres,
    'maximum_finite_interval_integral_error':maxfinite,'maximum_map_derivative_error':maxmap,
    'records':records,'finite_intervals':finite,'flat_event_scale_series':series,'cubic':cubic,
    'limits':'Float64 interpolation/finite differences, finite supplied geometries; not continuum certification or physical adoption'}
print(json.dumps(result,indent=2))
