#!/usr/bin/env python3
"""OAA1 independent endpoint-affine and causal-protocol controls; not a field solve."""
import hashlib
import json
import os
import platform
import resource
import sys
from pathlib import Path

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import mpmath as mp

OUT = Path(__file__).resolve().parent
ROWS = []
CHECKS = []
COUNT = 0


def serial(x):
    if isinstance(x, (mp.mpf, mp.mpc)):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, list):
        return [serial(v) for v in x]
    return x


def check(name, actual, threshold):
    ok = actual < threshold
    CHECKS.append(dict(name=name, actual=str(actual), threshold=str(threshold), passed=bool(ok)))
    if not ok:
        print('FAILED', name, str(actual), str(threshold), flush=True)


def metric(f, r, x, y):
    return -f*x[0]*y[0]-x[0]*y[1]-x[1]*y[0]+r*r*x[2]*y[2]


def family(a0, H0, E0, bstar0, dps):
    global COUNT
    mp.mp.dps = dps
    m, a, H, E, bs = map(mp.mpf, ['1', a0, H0, E0, bstar0])
    h = 1-3*m/a
    Om = mp.sqrt(m/a**3-H**2)
    f = lambda r: 1-2*m/r-H**2*r*r
    v = lambda r: mp.sqrt(E**2-f(r))
    sx = lambda x, b: mp.sqrt(1+b*b*H*H-b*b*x*x+2*m*b*b*x**3)
    V = lambda x: mp.sqrt(H*H+(E*E-1)*x*x+2*m*x**3)
    P = lambda x, b: mp.quad(lambda q: b/sx(q,b), [x, 1/a])
    U = lambda x, b: mp.quad(lambda q: b*b/(sx(q,b)*(1+sx(q,b))), [x, 1/a])
    ui, pi = U(0,bs), P(0,bs)
    bound = a/mp.sqrt(f(a)) * mp.mpf('.999')

    def solve(R):
        global COUNT
        COUNT += 1
        if COUNT > 100:
            raise RuntimeError('Finite-case cap reached')
        x = 1/R
        uo = ui-mp.quad(lambda q: 1/(V(q)*(V(q)+E*q)), [0,x])
        fun = lambda b: Om*(uo-U(x,b))+P(x,b)-pi
        lo, hi, b = -bound, bound, bs
        if not (fun(lo)<0<fun(hi)):
            raise ValueError('Frozen bracket does not enclose root')
        for iteration in range(160):
            value = fun(b)
            if abs(value)<mp.power(10,-dps+8):
                break
            if value > 0:
                hi = b
            else:
                lo = b
            deriv = (1-Om*b)*mp.quad(lambda q: 1/sx(q,b)**3, [x,1/a])
            proposal = b-value/deriv
            b = proposal if lo < proposal < hi else (lo+hi)/2
        else:
            raise RuntimeError('Root iteration budget reached')
        te = uo-U(x,b)
        s = sx(x,b)
        vv = v(R)
        k = [b*b/(R*R*(1+s)),s,b/(R*R)]
        u = [1/(E+vv),vv,mp.mpf(0)]
        ao = -metric(f(R),R,k,u)
        ka = [b*b/(a*a*(1+sx(1/a,b))),sx(1/a,b),b/(a*a)]
        ue = [1/mp.sqrt(h),mp.mpf(0),Om/mp.sqrt(h)]
        ae = -metric(f(a),a,ka,ue)
        S = mp.sqrt(1+H*H*b*b)
        # Independent affine quadrature in r, without the normalized-distance formula.
        breaks = [a]
        while breaks[-1]*10 < R:
            breaks.append(breaks[-1]*10)
        breaks.append(R)
        L = mp.quad(lambda r: 1/mp.sqrt(1-f(r)*b*b/(r*r)), breaks)
        do, de = ao*L, ae*L
        tol = mp.mpf('1e-30')
        check(f'incidence_{dps}_{a}_{R}',abs(Om*te+P(x,b)-pi),tol)
        check(f'receiver_norm_{dps}_{a}_{R}',abs(metric(f(R),R,u,u)+1),tol)
        check(f'ray_norm_{dps}_{a}_{R}',abs(metric(f(R),R,k,k)),tol)
        check(f'emitter_norm_{dps}_{a}_{R}',abs(metric(f(a),a,ue,ue)+1),tol)
        check(f'emitter_frequency_{dps}_{a}_{R}',abs(ae-(1-Om*b)/mp.sqrt(h)),tol)
        regular_ao=1/(E+vv)+vv*b*b/(R*R*(1+s))
        check(f'receiver_frequency_{dps}_{a}_{R}',abs(ao-regular_ao),tol)
        row = dict(kind='incidence',case=COUNT,dps=dps,a=a,H=H,E=E,bstar=bs,R=R,
                   b=b,te=te,affine=L,d_o=do,d_e=de,Z=ae/ao,Hd_o=H*do,
                   incidence_residual=abs(Om*te+P(x,b)-pi),iterations=iteration)
        ROWS.append(serial(row))
        return row

    central=[]
    for R in map(mp.mpf,['60','600','6000','60000']):
        c=solve(R)
        delta=R*mp.mpf('1e-5')
        before,after=solve(R-delta),solve(R+delta)
        # Integrating proper time independently avoids reusing d tau/dR at the center.
        dtau = mp.quad(lambda r: 1/v(r), [R-delta,R+delta])
        diff_z=dtau/(mp.sqrt(h)*(after['te']-before['te']))
        check(f'arrival_derivative_{dps}_{a}_{R}',abs(diff_z/c['Z']-1),mp.mpf('3e-8'))
        central.append(c)
        print('CENTRAL',dps,str(a),str(R),'b',mp.nstr(c['b'],10),
              'Hdo',mp.nstr(c['Hd_o'],13),'Z',mp.nstr(c['Z'],13),flush=True)
    errors=[abs(c['Hd_o']-1) for c in central]
    check(f'limit_final_{dps}_{a}',errors[-1],mp.mpf('.005'))
    check(f'limit_shrinks_1_{dps}_{a}',errors[-1]/errors[-2],mp.mpf(1))
    check(f'limit_shrinks_2_{dps}_{a}',errors[-2]/errors[-3],mp.mpf(1))
    return central


def controls(dps):
    global COUNT
    mp.mp.dps=dps
    for eta in map(mp.mpf,['-1','0','.5','1']):
        COUNT+=1
        omega=mp.cosh(eta)-mp.sinh(eta)
        do=3*omega
        z=1/omega
        check(f'boost_{dps}_{eta}',abs(do-3*mp.exp(-eta)),mp.mpf('1e-30'))
        ROWS.append(serial(dict(kind='boost',case=COUNT,dps=dps,eta=eta,d_o=do,Z=z)))
    a,H,m=mp.mpf(8),mp.mpf('.02'),mp.mpf(1)
    f=lambda r:1-2*m/r-H*H*r*r
    rc=mp.findroot(f,(40,55))
    prev_radar=mp.mpf(0)
    # Independent integrable bound: f=(rc-r)Q(r), Q positive continuous on[a,rc].
    slice_endpoint=mp.quad(lambda y: 2*y/mp.sqrt(f(rc-y*y)),
                           [mp.mpf('1e-15'),mp.sqrt(rc-a)])
    for j in (1,2,3):
        COUNT+=1
        R=rc-(rc-a)*mp.power(10,-j)
        radar=mp.sqrt(f(a))*mp.quad(lambda r:1/f(r),[a,R])
        spatial=mp.quad(lambda r:1/mp.sqrt(f(r)),[a,R])
        check(f'radar_increases_{dps}_{j}',prev_radar-radar,mp.mpf(0))
        check(f'slice_bounded_{dps}_{j}',spatial-slice_endpoint,mp.mpf(0))
        prev_radar=radar
        ROWS.append(serial(dict(kind='radar_control',case=COUNT,dps=dps,R=R,
                               rc=rc,radar=radar,spatial=spatial,
                               truncated_slice_endpoint=slice_endpoint)))
        print('RADAR',dps,j,mp.nstr(radar,12),mp.nstr(spatial,12),flush=True)


def main():
    values={}
    for dps in (45,75):
        for args in [('8','.02','1.2','0'),('10','.01','1','2')]:
            values[(dps,args[0])]=family(*args,dps)
        controls(dps)
    mp.mp.dps=75
    for a in ('8','10'):
        for low,high in zip(values[(45,a)],values[(75,a)]):
            for key in ('b','te','affine','d_o','d_e','Z'):
                rel=abs(low[key]-high[key])/max(1,abs(high[key]))
                check(f'precision_{a}_{high["R"]}_{key}',rel,mp.mpf('1e-25'))


if __name__=='__main__':
    meta=dict(python=sys.version,platform=platform.platform(),mpmath=mp.__version__,
              code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              blas_env={k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']},
              cap_bytes=2*1024**3,wall_cpu_timeout=False)
    failure=None
    try:
        main()
    except Exception as exc:
        failure=repr(exc)
        raise
    finally:
        result=dict(metadata=meta,finite_case_count=COUNT,checks=CHECKS,rows=ROWS,
                    exception=failure,passed=failure is None and all(c['passed'] for c in CHECKS))
        (OUT/'NUMERICAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
        print('RESULT',result['passed'],'cases',COUNT,'checks',len(CHECKS),flush=True)
