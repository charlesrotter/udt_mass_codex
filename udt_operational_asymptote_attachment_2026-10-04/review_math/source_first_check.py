"""OAA1 independent source-first finite checks. Frozen before first execution.

Only mpmath and Python stdlib; no OAA1 parent candidate/code/results are inputs.
Numerical values below are FREE explored query data, not physical selections.
"""
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time

os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import mpmath as mp

ROOT = Path(__file__).resolve().parent
CONFIGS = [
    {'name': 'radial_limit', 'm': '1', 'a': '10', 'H': '.01', 'E': '1', 'fraction': '0'},
    {'name': 'regular_nonzero', 'm': '1', 'a': '10', 'H': '.01', 'E': '1', 'fraction': '.5'},
    {'name': 'near_photon_negative', 'm': '1', 'a': '3.001', 'H': '.18', 'E': '1', 'fraction': '-.999'},
]
DPS = [60, 100]
RADII = ['10000', '1000000', '100000000']
MAX_CASES = 18


def main():
    started = time.time()
    raw = ROOT / 'source_first_raw.jsonl'
    if raw.exists():
        raise RuntimeError('Preserve existing results; this initial frozen run cannot overwrite them.')
    records = []
    with raw.open('x') as out:
        for dps in DPS:
            mp.mp.dps = dps
            for cfg in CONFIGS:
                m, a, H, E = [mp.mpf(cfg[k]) for k in ['m', 'a', 'H', 'E']]
                h = 1 - 3*m/a
                f = lambda r: 1-2*m/r-H**2*r**2
                Om = mp.sqrt(m/a**3-H**2)
                bmax = a/mp.sqrt(f(a))
                bs = mp.mpf(cfg['fraction'])*bmax
                xa = 1/a
                sq = lambda x, b: mp.sqrt(1+H**2*b**2-b**2*x**2+2*m*b**2*x**3)
                S = lambda b: mp.sqrt(1+H**2*b**2)
                # Fixed integration subdivision resolves the almost tangent source.
                def quad(fun, lo, hi):
                    pts = [lo] + [q*hi for q in map(mp.mpf, ['.25','.5','.75','.9','.99','.999']) if lo < q*hi < hi] + [hi]
                    return mp.quad(fun, pts)
                def P(R, b):
                    return quad(lambda x: b/sq(x,b), 1/R, xa)
                def U(R, b):
                    return quad(lambda x: b*b/(sq(x,b)*(1+sq(x,b))), 1/R, xa)
                pinf = quad(lambda x: bs/sq(x,bs), mp.mpf(0), xa)
                uinf = quad(lambda x: bs*bs/(sq(x,bs)*(1+sq(x,bs))), mp.mpf(0), xa)
                def C(b):
                    sb = S(b)
                    return -a/sb + quad(lambda x: b*b*(1-2*m*x)/(sb*sq(x,b)*(sb+sq(x,b))), mp.mpf(0), xa)
                cs = C(bs)
                ss = S(bs)
                qstar = 1-Om*bs
                zc = H*qstar/(mp.sqrt(h)*ss)
                residue = ss*cs/H-E/(H*H*ss)
                for radius in RADII:
                    if len(records) >= MAX_CASES:
                        raise RuntimeError('finite-case budget exceeded')
                    R = mp.mpf(radius)
                    row = {'case': len(records)+1, 'config': cfg, 'dps': dps, 'R': radius}
                    try:
                        x = 1/R
                        V = mp.sqrt(H*H+(E*E-1)*x*x+2*m*x**3)
                        d = mp.quad(lambda y: 1/(mp.sqrt(H*H+(E*E-1)*y*y+2*m*y**3)*(E*y+mp.sqrt(H*H+(E*E-1)*y*y+2*m*y**3))), [0,x])
                        def residual(b):
                            return P(R,b)-Om*U(R,b)-pinf+Om*uinf-Om*d
                        def deriv(b):
                            return (1-Om*b)*quad(lambda y: 1/sq(y,b)**3,x,xa)
                        b = bs
                        iterations = []
                        # Deterministic bounded Newton, no retry or changed tolerance.
                        for j in range(16):
                            rr = residual(b)
                            iterations.append({'j':j,'b':mp.nstr(b,dps),'residual':mp.nstr(rr,dps)})
                            if abs(rr) < mp.mpf(10)**(-dps+12):
                                break
                            b -= rr/deriv(b)
                            if not abs(b) < bmax:
                                raise ArithmeticError('iterate left strict source bound')
                        else:
                            raise ArithmeticError('fixed Newton iteration limit reached')
                        te = uinf-d-U(R,b)
                        s = sq(x,b)
                        v = V/x
                        A = x*(1/(E*x+V)+V*b*b/(1+s))
                        we = (1-Om*b)/mp.sqrt(h)
                        # Direct logarithmic-coordinate affine integration.
                        zmax = mp.log(R/a)
                        Ldirect = mp.quad(lambda z: a*mp.exp(z)/sq(mp.exp(-z)/a,b), [zmax*i/8 for i in range(9)])
                        cb = C(b)
                        sb = S(b)
                        tail = mp.quad(lambda y: b*b*(1-2*m*y)/(sb*sq(y,b)*(sb+sq(y,b))),[0,x])
                        Ltail = R/sb+cb-tail
                        uu, ur = x/(E*x+V), v
                        ku, kr = b*b*x*x/(1+s), s
                        Adot = f(R)*ku*uu+ku*ur+kr*uu
                        Do, De, Z = A*Ldirect, we*Ldirect, we/A
                        vals = {'b_star':bs,'b':b,'b_bound':bmax,'t_e':te,'A':A,'A_metric_contraction':Adot,'omega_e':we,'Z':Z,'L_direct':Ldirect,'L_tail':Ltail,'D_o':Do,'D_e':De,'S_star':ss,'C_star':cs,'receiver_limit':1/H,'distance_residue':residue,'observed_residue':R*(Do-1/H),'Z_over_R':Z/R,'Z_over_R_limit':zc,'clock_product':Z*(-mp.sqrt(h)*te),'clock_product_limit':1/H,'incidence_time_residual':te+U(R,b)-uinf+d,'incidence_angle_residual':Om*te+P(R,b)-pinf,'normalization_ratio_error':De/Do-Z,'affine_integral_relative_error':(Ldirect-Ltail)/Ldirect,'frequency_relative_error':(A-Adot)/A}
                        row['values'] = {k:mp.nstr(vv,dps) for k,vv in vals.items()}
                        row['iterations'] = iterations
                        tol = mp.mpf(10)**(-dps+15)
                        row['checks'] = {
                            'source_and_ray_regular': bool(a>3*m and f(a)>0 and Om>0 and abs(b)<bmax),
                            'causal_emission_side': bool(te<0),
                            'affine_direct_tail': bool(abs(vals['affine_integral_relative_error'])<tol),
                            'metric_endpoint_frequency': bool(abs(vals['frequency_relative_error'])<tol),
                            'incidence_residuals': bool(abs(vals['incidence_time_residual'])<tol and abs(vals['incidence_angle_residual'])<tol),
                            'ratio_identity': bool(abs(vals['normalization_ratio_error'])/Z<tol),
                        }
                        row['passed'] = all(row['checks'].values())
                    except Exception as exc:
                        row['passed'] = False
                        row['failure'] = repr(exc)
                    records.append(row)
                    out.write(json.dumps(row,sort_keys=True)+'\n')
                    out.flush()
                    print(json.dumps({'case':row['case'],'config':cfg['name'],'dps':dps,'R':radius,'passed':row['passed'],'failure':row.get('failure'),'D_o':row.get('values',{}).get('D_o'),'distance_residue':row.get('values',{}).get('distance_residue')}),flush=True)
    low = {(r['config']['name'],r['R']):r for r in records if r['dps']==DPS[0]}
    precision = []
    for r in records:
        if r['dps'] != DPS[1] or 'values' not in r: continue
        r0 = low[(r['config']['name'],r['R'])]
        if 'values' not in r0: continue
        err = max(abs(mp.mpf(r['values'][key])-mp.mpf(r0['values'][key]))/(1+abs(mp.mpf(r['values'][key]))) for key in ['b','Z','D_o','D_e'])
        precision.append({'config':r['config']['name'],'R':r['R'],'max_scaled_discrepancy':mp.nstr(err,40),'passed':bool(err<mp.mpf('1e-40'))})
    result = {'python':sys.version,'platform':platform.platform(),'mpmath':mp.__version__,'cpu_only':True,'memory_limit_bytes':2*1024**3,'blas_threads':1,'wall_or_cpu_timeout':None,'cases':len(records),'case_budget':MAX_CASES,'elapsed_s':time.time()-started,'cases_passed':sum(r['passed'] for r in records),'precision_checks':precision,'all_passed':all(r['passed'] for r in records) and all(p['passed'] for p in precision),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}
    (ROOT/'SOURCE_FIRST_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
