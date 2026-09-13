#!/usr/bin/env python3
"""CSS4 finite conditional guide diagnostics; equations remain in the candidate."""
import argparse,json,math,platform,sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp

# FREE supplied examples and dimensional conversion; see CHECK_CONTRACT.md.
CASES=[(-.3,0.),(.3,0.),(0.,0.),(0.,-.02),(0.,.02)]
R,TREF,SCALE=1.,1.,1.7

def delta(te,b0,kappa,sign,mutate=None):
    b=b0+kappa*(te-TREF)
    C=R*R*kappa/2
    if mutate=='reverse_sign':sign=-sign
    if mutate=='freeze_shift':C=0.
    F=2*math.pi if C==0 else -math.expm1(-sign*C*2*math.pi)/(sign*C)
    return (R-sign*R*R*b/2)*F

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutate',choices=['reverse_sign','freeze_shift','drop_clock_scale']);arg=parser.parse_args()
    out={'status':'FAIL','mutation':arg.mutate,'records':[],'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'scope':'Ten chosen histories/emissions, explicit guide; no free-geodesic or physical energy claim.'}
    try:
        for b0,kappa in CASES:
            for te in (1.,3.):
                rows=[]
                for sign in (1,-1):
                    d=delta(te,b0,kappa,sign,arg.mutate)
                    sol=solve_ivp(lambda ell,t:[R-sign*R*R*(b0+kappa*(t[0]-TREF))/2],(0.,2*math.pi),[te],method='DOP853',rtol=2e-11,atol=2e-13,max_step=.05)
                    assert sol.success,sol.message
                    measured=(1. if arg.mutate=='drop_clock_scale' else SCALE)*d
                    original=SCALE*(float(sol.y[0,-1])-te)
                    err=abs(measured-original)
                    assert err<=2e-9,('original_null_guide_and_proper_clock',b0,kappa,te,sign,err)
                    assert 0<=te<sol.y[0,-1]<=15,('time_window',te,sol.y[0,-1])
                    bvals=b0+kappa*(sol.y[0]-TREF)
                    assert np.max(abs(bvals))*.55<1,('positive_slice',float(np.max(abs(bvals))))
                    slope=math.exp(-sign*math.pi*R*R*kappa)
                    hh=1e-4
                    fd=((te+hh+delta(te+hh,b0,kappa,sign))-(te-hh+delta(te-hh,b0,kappa,sign)))/(2*hh)
                    assert abs(fd-slope)<=2e-7,('time_tag_slope',fd,slope)
                    finite=(te+.6+delta(te+.6,b0,kappa,sign))-(te+delta(te,b0,kappa,sign))
                    assert abs(finite-.6*slope)<=2e-12,('whole_event_affine_map',finite,slope)
                    rows.append({'sign':sign,'coordinate_duration':d,'proper_duration':measured,'ode_proper_duration':original,'ode_error':err,'slope':slope,'slope_fd':fd,'finite_event_stretch':finite/.6,'last_time':float(sol.y[0,-1]),'nfev':sol.nfev})
                be=b0+kappa*(te-TREF);contrast=rows[0]['proper_duration']-rows[1]['proper_duration']
                frozen=-2*math.pi*SCALE*R*R*be
                assert abs(rows[0]['slope']*rows[1]['slope']-1)<=2e-14,'opposite_slopes'
                kr=math.log(rows[1]['slope']/rows[0]['slope'])/(2*math.pi*R*R)
                assert abs(kr-kappa)<=2e-14,'rate_calibration'
                if kappa==0:assert abs(contrast-frozen)<=2e-12,'stationary_limit'
                if be==0 and kappa!=0:
                    C=R*R*kappa/2;exact=2*SCALE*R/C*(1-math.cosh(C*2*math.pi))
                    assert abs(contrast-exact)<=2e-12,'zero_initial_circulation'
                    assert contrast*kappa<0,'signed_dynamic_contrast'
                out['records'].append({'b_star':b0,'kappa':kappa,'emission_t':te,'directions':rows,'proper_direction_contrast':contrast,'frozen_direction_contrast':frozen,'recovered_kappa':kr})
        out['status']='PASS'
    except Exception as exc:out['failure']=repr(exc)
    print(json.dumps(out,indent=2,allow_nan=False));return 0 if out['status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
