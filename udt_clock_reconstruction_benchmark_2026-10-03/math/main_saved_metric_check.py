"""Original tensor from saved a only and independent clock spots. No parent imports."""
import json,math,hashlib,platform
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
import source_first_check as own

B=Path(__file__).resolve().parents[1]
P=B/'main/metric_a_only.json';saved=json.loads(P.read_text());t=np.array(saved['t'])
assert len(t)==2401 and np.max(np.abs(np.diff(t)-.001))<5e-15
mp.mp.dps=70
nodes=list(range(-5,6))
mat=mp.matrix([[mp.mpf(j)**k for j in nodes] for k in range(11)])
weights={d:mp.lu_solve(mat,mp.matrix([mp.factorial(d) if k==d else 0 for k in range(11)])) for d in range(1,5)}
rows=[]
for case,av in saved['a'].items():
  assert len(av)==len(t) and min(av)>0
  for step in [.03,.04]:
    stride=round(step/.001)
    for center in np.linspace(-.9,.9,37):
      index=int(np.argmin(abs(t-center)));assert abs(t[index]-center)<1e-12
      points=[mp.mpf(str(av[index+j*stride])) for j in nodes]
      a=points[5]
      d={q:sum(weights[q][j]*points[j] for j in range(11))/mp.mpf(str(step))**q for q in range(1,5)}
      H=d[1]/a;A=d[2]/a;Hd=A-H*H
      R=6*(A+H*H)
      Rp=6*(d[3]/a+d[1]*d[2]/a**2-2*d[1]**3/a**3)
      Rpp=6*(d[4]/a+d[2]**2/a**2-8*d[1]**2*d[2]/a**3+6*d[1]**4/a**4)
      Box=-Rpp-3*H*Rp
      E00=3*H**2-6*R*A+R**2/2+6*H*Rp
      Es=-(2*Hd+3*H**2)+2*R*(A+2*H**2)-R**2/2-2*Rpp-4*H*Rp
      assert abs((-E00+3*Es)-(6*Box-R))<mp.mpf('1e-60')
      rows.append(dict(case=case,step=step,t=float(center),R=float(R),Box=float(Box),E00=float(E00),Es=float(Es)))
summary=[]
for case in saved['a']:
 for step in [.03,.04]:
  part=[r for r in rows if r['case']==case and r['step']==step]
  summary.append(dict(case=case,step=step,max_tensor=max(max(abs(r['E00']),abs(r['Es'])) for r in part),
                      min_abs_E00=min(abs(r['E00']) for r in part),max_abs_R=max(abs(r['R']) for r in part),
                      max_abs_Box=max(abs(r['Box']) for r in part)))
assert max(r['max_tensor'] for r in summary if r['case']=='A')<2e-6
assert min(r['min_abs_E00'] for r in summary if r['case']=='B')>1e-2
assert max(r['max_abs_R'] for r in summary if r['case']=='B')<1e-6
assert max(r['max_abs_Box'] for r in summary if r['case']=='B')<1e-6

# Forward spot checks use only a-samples to make an independent interpolant.
# This is a distinct smooth interpolant, not an interval-certified parent metric.
raw=json.loads((B/'main/fine/forward_details.json').read_text())['unique_queries']
spots=[]
for case in ['A','B','C']:
 spline=CubicSpline(t,np.array(saved['a'][case]))
 own.metric=lambda tt,k:(float(spline(tt)),float(spline(tt,1)/spline(tt)))
 own.eta=lambda tt,k:quad(lambda q:1/float(spline(q)),0,tt,epsabs=1e-13,epsrel=1e-13,limit=100)[0]
 for center in [-.6,.3]:
  selected=[r for r in raw if r['case']==case and abs(r['t']-center)<1e-14 and r['L']==.02]
  assert len(selected)==3
  for r in selected:
   kind=r['unique_forward_kind'];v=0 if kind=='rest' else .6
   U,triad=own.frame(center,[v,0,0],0)
   val=own.clock(center,U,triad[1 if kind=='boost_trans' else 0],.02,0,case=='A')
   spots.append(dict(case=case,t=center,kind=kind,parent_log=r['log_p'],own_log=val['logp'],
                     error=abs(r['log_p']-val['logp']),
                     arrival_derivative_error=val.get('derivative_frequency_error')))
assert max(r['error'] for r in spots)<2e-10
assert max(r['arrival_derivative_error'] for r in spots if r['case']=='A')<2e-8
result=dict(status='PASS independent saved-a tensor and forward spots',summary=summary,tensor_rows=rows,
            clock_spots=spots,metric_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),
            limits='Original tensor alpha1 Lambda0; no H/R/P/RHS or parent evaluator imports. 11point finite derivatives at two spacings are finite floating diagnostics, not interval bounds. Clock spots use independently interpolated saved a and shared SciPy numerical libraries. Parent EVALUATION not opened before this check.',
            versions=dict(python=platform.python_version(),mpmath=mp.__version__))
with (B/'math/MAIN_SAVED_METRIC_CHECK.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(status=result['status'],summary=summary,max_clock_error=max(r['error'] for r in spots),
                     max_arrival_error=max(r['arrival_derivative_error'] for r in spots if r['case']=='A'))))
