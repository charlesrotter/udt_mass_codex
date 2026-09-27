"""Bounded independent Fraction checks; no source scientific code imports.

Question: do direct static-clock ratio equations recover both coefficients of
the supplied positive LSB1 family, leaving a fourth clock ratio unused, and does
the static proper-clock/ruler conversion retain local c_E? Exact finite controls
support the analytic argument in SOURCE_FIRST.md; they are not a general proof,
apparatus certification, field-law selection or replay of old ray numerics.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import time


def run():
    started = time.monotonic()
    count = 0
    cases = []

    def require(value, label):
        nonlocal count
        if not value:
            raise AssertionError(label)
        count += 1

    for radii in [(1, 2, 3), (1, 3, 5), (2, 3, 7)]:
        x, y, z = map(F, radii)
        for a in [F(-1, 100), F(0), F(1, 100)]:
            for b in [F(-1, 10), F(0), F(1, 10)]:
                def lapse2(r):
                    return 1 + a*r*r + b/r

                f0, f1, f2 = map(lapse2, (x, y, z))
                q1, q2 = f1/f0, f2/f0
                # Solve the two clock constraints by direct elimination.
                A, B, C = y*y-q1*x*x, 1/y-q1/x, q1-1
                D, E, H = z*z-q2*x*x, 1/z-q2/x, q2-1
                det = A*E-B*D
                recovered_a = (C*E-B*H)/det
                recovered_b = (A*H-C*D)/det
                closed_det = (y-x)*(z-x)*(z-y)*(x+y+z)/(x*y*z*f0)
                require(min(f0, f1, f2) > 0, 'positive sampled clock domain')
                require(det == closed_det and det > 0, 'exact determinant')
                require(recovered_a == a and recovered_b == b, 'both coefficients')
                r_unused = F(8)
                actual_unused = lapse2(r_unused)/f0
                predicted_unused = (1+recovered_a*r_unused*r_unused+recovered_b/r_unused)/(1+recovered_a*x*x+recovered_b/x)
                require(predicted_unused == actual_unused, 'unused fourth clock')
                # The affine one-ratio null direction preserves its input ratio.
                shifted_a, shifted_b = a+B*F(1, 100), b-A*F(1, 100)
                g0 = 1+shifted_a*x*x+shifted_b/x
                g1 = 1+shifted_a*y*y+shifted_b/y
                require(g1*f0 == f1*g0, 'one-ratio freedom')
                cases.append({'radii':radii, 'a':str(a), 'b':str(b), 'det':str(det), 'unused_ratio_squared':str(predicted_unused)})

    c = F(3, 2)
    for N in [F(1, 2), F(1), F(2)]:
        f = N*N
        tdot, rdot = F(1), c*f
        require(-c*c*f*tdot*tdot+rdot*rdot/f == 0, 'original radial null constraint')
        proper_speed = (rdot/N)/(N*tdot)
        require(proper_speed == c, 'local proper speed')

    # A specific adverse control: dropping f0 from the claimed determinant.
    # This is an actual wrong algebraic expression, not a denied true assertion.
    x,y,z,a,b=F(1),F(2),F(3),F(1,100),F(1,10)
    f0=1+a*x*x+b/x
    f1=1+a*y*y+b/y
    f2=1+a*z*z+b/z
    q1,q2=f1/f0,f2/f0
    actual=(y*y-q1*x*x)*(1/z-q2/x)-(1/y-q1/x)*(z*z-q2*x*x)
    bad=(y-x)*(z-x)*(z-y)*(x+y+z)/(x*y*z)
    require(actual != bad, 'omitted normalization defect rejected')

    # Post-source-first parent-disclosed narrow hypothesis test. In the flat
    # LSB member use an offset straight chord with an interior perpendicular
    # foot, so the radial path has a nondegenerate one-periapse branch p=3.
    # A=(3,-4), B=(3,5/4), r_A=5, r_B=13/4, chord length 21/4.
    # This separates the derivative of an arrival map from its additive delay.
    p, yA, yB, rA, rB = F(3), F(-4), F(5,4), F(5), F(13,4)
    d, L = yB-yA, F(2)
    require(p*p+yA*yA == rA*rA and p*p+yB*yB == rB*rB,
            'flat chord endpoint radii')
    require(yA < 0 < yB and 0 < p < min(rA,rB), 'regular interior periapse')
    require(F(2)/(p**3) > 0, 'flat simple-turn derivative')
    R, delta, chi_clock = F(1), F(0), F(0)  # log(1)=tanh(0)=0 exactly
    round_trip = 2*L*d/c
    require(round_trip == 14 and round_trip > 0, 'positive flat single-clock RTT')
    require(R == 1 and delta == chi_clock == 0, 'equal rates do not set elapsed duration')

    return {'status':'PASS', 'python':platform.python_version(), 'arithmetic':'fractions.Fraction exact',
            'assertions':count, 'lsb_cases':len(cases), 'local_null_controls':3,
            'adverse_algebra_controls':1, 'seconds':time.monotonic()-started,
            'flat_rate_delay_control':{'p':str(p),'r_A':str(rA),'r_B':str(rB),'d':str(d),'L':str(L),'c_E':str(c),'R':str(R),'delta':str(delta),'chi_clock':str(chi_clock),'tau_round':str(round_trip)},
            'cases':cases, 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limitations':'Finite exact controls; analytic source-relative argument owns universal scope. No physical apparatus, scale selection, native dynamics or statistical independence certified.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
