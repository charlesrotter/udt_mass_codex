#!/usr/bin/env python3
"""Independent source-first original-geodesic scalar variation, not parent code."""
import argparse
import json
import platform
import sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.special import jv, yv

parser=argparse.ArgumentParser()
parser.add_argument('--tight',action='store_true')
args=parser.parse_args()
k=.75  # PINNED source normalization G394
A=-(3*np.pi/4)*yv(0,k)
B=(3*np.pi/4)*jv(0,k)
def ff(t):
    return A*jv(0,k*t)+B*yv(0,k*t), -k*(A*jv(1,k*t)+B*yv(1,k*t))

def solve(e):
    def rhs(t,u):
        f,fp=ff(t)
        rt=-3/(4*t)+e*e*t*fp*fp/4-e*fp/2
        rxx=k*k*e*f*(1-e*t*fp)/2
        return [u[1], -rt*u[1]-rxx*u[0]]
    def event(t,u): return u[0]
    result=solve_ivp(rhs,(1,80),(0,1),method='DOP853',
                     rtol=2e-12 if args.tight else 2e-10,
                     atol=2e-14 if args.tight else 2e-12,
                     max_step=.025 if args.tight else .05,
                     events=event,dense_output=True)
    assert result.success,result.message
    ts=np.linspace(1,80,791)
    us=result.sol(ts)
    roots=[float(t) for t in result.t_events[0] if t>1+1e-7]
    return dict(epsilon=e,roots=roots,nfev=result.nfev,
                crossing_brackets=[dict(t=t,minus=result.sol(t-1e-3).tolist(),
                                        plus=result.sol(t+1e-3).tolist()) for t in roots],
                samples=np.column_stack([ts,us.T]).tolist())

cases=[solve(e) for e in (1/6,-1/6,.5,-.5,1,-1,2,-2)]
print(json.dumps(dict(versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),
                     tight=args.tight,cases=cases),indent=2))
