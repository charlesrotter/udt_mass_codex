#!/usr/bin/env python3
"""Finite LSB1 checks. Original argument, not assertion counts, owns the theorem."""
import argparse
import json
import math
import platform
import sys
import warnings
from fractions import Fraction as F

import numpy as np
import scipy
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq
import sympy as sp

# FREE supplied diagnostic coefficients/layout, frozen in CHECK_CONTRACT.md.
AS = (-.002, 0., .002)
BS = (-.4, 0., .4)
RA, RB, PHI = 6., 8., 2.


def f(r, a, b):
    return 1 + a*r*r + b/r


def calibrate(a, b, mutate=None):
    rr = (2., 4., 8.)
    q = np.array([f(r, a, b)/f(rr[0], a, b) for r in rr[1:]])
    if mutate == 'invert_clock':
        q = 1/q
    matrix = np.column_stack([np.array(rr[1:])**2-q*rr[0]**2,
                              1/np.array(rr[1:])-q/rr[0]])
    ab = np.linalg.solve(matrix, q-1)
    return ab, q, matrix


def leg(p, R, a, b, tight=False):
    tol = 2e-12 if tight else 2e-11
    end = math.sqrt(1-p/R)

    def values(x):
        u = 1-x*x
        J = 2-x*x + b/p*(3-3*x*x+x**4)
        V = u*u + a*p*p + b/p*u**3
        assert J > 0 and V > 0, ('leg_positivity', J, V)
        return 2/math.sqrt(J), 2*p*math.sqrt(f(p, a, b))/(V*math.sqrt(J))

    az, aze = quad(lambda x: values(x)[0], 0., end,
                   epsabs=tol, epsrel=tol, limit=100)
    time, te = quad(lambda x: values(x)[1], 0., end,
                   epsabs=tol, epsrel=tol, limit=100)
    return az, time, aze, te


def solve(a, b, tight=False, mutate=None):
    def target(p):
        return leg(p, RA, a, b, tight)[0]+leg(p, RB, a, b, tight)[0]-PHI
    bracket = [target(p) for p in (1.6, 5.5)]
    assert bracket[0]*bracket[1] < 0, ('root_bracket', bracket)
    p = brentq(target, 1.6, 5.5, xtol=2e-13 if tight else 2e-12, rtol=2e-14)
    la, lb = leg(p, RA, a, b, tight), leg(p, RB, a, b, tight)
    kp = f(p, a, b)/(p*p)
    lapseB = 1. if mutate == 'drop_receiver_lapse' else math.sqrt(f(RB, a, b))
    psi = math.asin(lapseB/(RB*math.sqrt(kp)))
    lapseA = 1. if mutate == 'drop_source_lapse' else math.sqrt(f(RA, a, b))
    rtt = 2*lapseA*(la[1]+lb[1])  # Units L/c_E, not seconds without L.
    R = math.sqrt(f(RB, a, b)/f(RA, a, b))
    delta = -math.log(R)
    chord = math.sqrt(RA*RA+RB*RB-2*RA*RB*math.cos(PHI))
    pflat = RA*RB*math.sin(PHI)/chord
    psiflat = math.asin(pflat/RB)
    return {'a':a, 'b':b, 'p':p, 'K_p':kp, 'impact_B':1/math.sqrt(kp),
            'bracket_values':bracket, 'angular_residual':la[0]+lb[0]-PHI,
            'legs':[la,lb], 'clock_R_A_B':R, 'clock_delta':delta,
            'chi_clock':math.tanh(delta), 'psi_B':psi,
            'roundtrip_cE_over_L':rtt, 'flat_chord':chord, 'flat_p':pflat,
            'flat_psi_B':psiflat, 'angle_contrast':psi-psiflat,
            'time_contrast_cE_over_L':rtt-2*chord}


def exact_checks():
    r0,r1,r2,a,b=sp.symbols('r0 r1 r2 a b', nonzero=True)
    ff = lambda r: 1+a*r*r+b/r
    q1,q2=ff(r1)/ff(r0),ff(r2)/ff(r0)
    mat=sp.Matrix([[r1*r1-q1*r0*r0,1/r1-q1/r0],
                   [r2*r2-q2*r0*r0,1/r2-q2/r0]])
    want=(r1-r0)*(r2-r0)*(r2-r1)*(r0+r1+r2)/(r0*r1*r2*ff(r0))
    assert sp.factor(mat.det()-want)==0, 'exact_calibration_determinant'
    rec=[]
    for aa in (F(-1,500),F(0),F(1,500)):
        for bb in (F(-2,5),F(0),F(2,5)):
            q=[f(F(r),aa,bb)/f(F(2),aa,bb) for r in (4,8)]
            A=[F(r*r)-qi*4 for r,qi in zip((4,8),q)]
            B=[F(1,r)-qi/2 for r,qi in zip((4,8),q)]
            y=[qi-1 for qi in q]; D=A[0]*B[1]-A[1]*B[0]
            ar=(y[0]*B[1]-y[1]*B[0])/D
            br=(A[0]*y[1]-A[1]*y[0])/D
            assert (ar,br)==(aa,bb), 'rational_coefficient_recovery'
            rec.append({'a':str(aa),'b':str(bb),'determinant':str(D)})
    x,p=sp.symbols('x p', positive=True)
    u=1-x*x; r=p/u
    H=1/p**2+b/p**3-1/r**2-b/r**3
    J=2-x*x+b/p*(3-3*x*x+x**4)
    V=u*u+a*p*p+b/p*u**3
    assert sp.factor(H-x*x*J/p**2)==0,'turning_H_transform'
    assert sp.factor(u*u*ff(r)-V)==0,'turning_lapse_transform'
    vr,vp=sp.symbols('vr vp')
    assert sp.factor(sp.diff((a+vr)/(a+vp),a)-(vp-vr)/(a+vp)**2)==0,'angle_derivative'
    q=sp.symbols('q',positive=True)
    chi=(1-q)/(1+q)
    assert sp.factor(chi+chi.subs(q,1/q))==0,'odd_clock_kernel'
    return {'symbolic_determinant':'PASS','rational_recovery':rec,
            'turning_transform':'PASS','angle_derivative':'PASS','clock_reversal':'PASS'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutate',choices=['invert_clock','drop_receiver_lapse','drop_source_lapse'])
    args=parser.parse_args()
    result={'status':'FAIL','mutation':args.mutate,'versions':{'python':platform.python_version(),
            'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
            'dtype':'float64 plus exact symbolic/rational checks','records':[],
            'scope':'Finite checks, not interval certification or observational data.'}
    try:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('error', IntegrationWarning)
            if not args.mutate:
                result['exact']=exact_checks()
            for a in AS:
                for b in BS:
                    ab,q,matrix=calibrate(a,b,args.mutate)
                    cerr=float(np.max(np.abs(ab-[a,b])))
                    assert cerr<=2e-12,('calibration_recovery',a,b,cerr)
                    row=solve(float(ab[0]),float(ab[1]),mutate=args.mutate)
                    row['supplied_coefficients']=[a,b]
                    row['calibration_q']=q.tolist()
                    row['calibration_matrix_condition_2']=float(np.linalg.cond(matrix))
                    row['calibration_recovery_error']=cerr
                    assert abs(row['angular_residual'])<=2e-10,('endpoint_angle',row)
                    # Original local tetrad contraction of an affine k with E=1.
                    j=row['impact_B']; kr=math.sqrt(1-j*j*f(RB,a,b)/RB**2)
                    k_phi_hat=j/RB; k_radial_hat=kr/math.sqrt(f(RB,a,b))
                    tetrad_angle=math.atan2(k_phi_hat,k_radial_hat)
                    assert abs(row['psi_B']-tetrad_angle)<=2e-11,('receiver_tetrad_angle',row['psi_B'],tetrad_angle)
                    proper=2*math.sqrt(f(RA,a,b))*sum(z[1] for z in row['legs'])
                    assert abs(row['roundtrip_cE_over_L']-proper)/(1+abs(proper))<=2e-12,('source_proper_clock',row['roundtrip_cE_over_L'],proper)
                    expected_chi=(f(RA,a,b)-f(RB,a,b))/(f(RA,a,b)+f(RB,a,b))
                    assert abs(row['chi_clock']-expected_chi)<=2e-14,('clock_kernel',row)
                    tight=solve(float(ab[0]),float(ab[1]),tight=True)
                    keys=('p','psi_B','roundtrip_cE_over_L','clock_R_A_B','chi_clock')
                    diffs={k:abs(row[k]-tight[k])/(1+abs(tight[k])) for k in keys}
                    assert max(diffs.values())<=2e-9,('tighter_repeat',diffs)
                    row['tighter_scaled_differences']=diffs
                    row['tighter_readouts']={k:tight[k] for k in keys}
                    result['records'].append(row)
            for b in BS:
                subset=[r for r in result['records'] if r['supplied_coefficients'][1]==b]
                pvals=[r['p'] for r in subset]
                assert max(pvals)-min(pvals)<=2e-11,('coordinate_a_cancellation',b,pvals)
                angles=[r['psi_B'] for r in subset]
                assert all(y>x for x,y in zip(angles,angles[1:])),('strict_angle_a_response',b,angles)
            flat=next(r for r in result['records'] if r['supplied_coefficients']==[0.,0.])
            errors=[abs(flat['p']-flat['flat_p']),abs(flat['angle_contrast']),abs(flat['time_contrast_cE_over_L'])/(1+2*flat['flat_chord'])]
            assert max(errors)<=2e-10,('flat_chord',errors)
            result['flat_errors']=errors
            result['warnings']=[str(w.message) for w in ws]
            result['status']='PASS'
    except Exception as exc:
        result['failure']=repr(exc)
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    sys.exit(main())
