#!/usr/bin/env python3
"""Independent source-first outgoing-chart actual-incidence check; no parent imports."""
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import mpmath as mp

OUT = Path(__file__).resolve().parent
RADII = [int(z) for z in os.environ.get("CPR_REVIEW_RADII", "25,100,1000,10000").split(",")]
OUTPUT_NAME = os.environ.get("CPR_REVIEW_OUTPUT", "initial_results.json")
started = time.time()
result = {
    "python": sys.version, "mpmath": mp.__version__, "platform": platform.platform(),
    "cpu_only": True, "address_space_limit": resource.getrlimit(resource.RLIMIT_AS),
    "thread_env": {k: os.environ.get(k) for k in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"]},
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "radii": RADII, "decimal_precisions": [40, 70], "records": [], "solve_attempts": 0,
    "failures": [],
}

def sstr(z):
    return mp.nstr(z, mp.mp.dps)

def residuals(r, f, vec, is_null=False, circular=False):
    """Christoffel contraction from independent metric derivative construction."""
    zero = mp.mpf(0)
    g = mp.matrix([[-f(r), -1, 0], [-1, 0, 0], [0, 0, r*r]])
    gi = g**-1
    dg = mp.matrix([[-mp.diff(f, r), 0, 0], [0, 0, 0], [0, 0, 2*r]])
    V = mp.matrix(vec(r))
    gamma = [[[sum(gi[i,l]*((dg[k,l] if j == 1 else 0)+(dg[j,l] if k == 1 else 0)-(dg[j,k] if l == 1 else 0))/2 for l in range(3)) for k in range(3)] for j in range(3)] for i in range(3)]
    acc = []
    for i in range(3):
        derivative = zero if circular else V[1]*mp.diff(lambda x: vec(x)[i], r)
        acc.append(derivative + sum(gamma[i][j][k]*V[j]*V[k] for j in range(3) for k in range(3)))
    norm = (V.T*g*V)[0] + (0 if is_null else 1)
    return max([abs(norm)] + [abs(z) for z in acc]), g

try:
    for digits in [40, 70]:
        mp.mp.dps = digits
        m, a, R0, E = map(mp.mpf, [1, 10, 20, 1])  # FREE query/example parameters.
        lam = mp.mpf("0.0001")  # FREE conditional integration datum; not measured.
        H = mp.sqrt(lam/3)
        h = 1-3*m/a
        om = mp.sqrt(m/a**3-lam/3)
        f = lambda r: 1-2*m/r-lam*r*r/3
        v = lambda r: mp.sqrt(E*E-f(r))
        b_end = mp.mpf(2)  # FREE endpoint ray preparation used to fix phi0 ONCE.
        ss = lambda x, b: mp.sqrt(1 + b*b*H*H - b*b*x*x + 2*m*b*b*x**3)
        ww = lambda x: mp.sqrt(H*H+(E*E-1)*x*x+2*m*x**3)
        u_integrand = lambda x: 1/(ww(x)*(E*x+ww(x)))
        j_integrand = lambda x, b: b*b/(ss(x,b)*(1+ss(x,b)))
        p_integrand = lambda x, b: b/ss(x,b)
        u0 = -mp.quad(lambda r: 1/f(r), [a, R0])
        uc = lambda x: u0+mp.quad(u_integrand, [x, 1/R0])
        jc = lambda x, b: mp.quad(lambda y: j_integrand(y,b), [x, 1/a])
        pc = lambda x, b: mp.quad(lambda y: p_integrand(y,b), [x, 1/a])
        te_end = uc(0)-jc(0,b_end)
        phi0 = -om*te_end-pc(0,b_end)
        emitter = lambda r: [1/mp.sqrt(h), mp.mpf(0), om/mp.sqrt(h)]
        emitter_res, _ = residuals(a, f, emitter, circular=True)
        threshold = mp.mpf("1e-30" if digits == 40 else "1e-55")
        assert emitter_res < threshold, "original circular geodesic"
        assert f(a)>0 and h>0 and om>0
        ell2 = a*a*(m/a-lam*a*a/3)/h
        vpp = mp.diff(lambda r: f(r)*(1+ell2/r**2), a, 2)
        assert vpp > 0, "example radial stability"

        def solve_at(rad):
            result["solve_attempts"] += 1
            assert result["solve_attempts"] <= 100
            x = 1/rad
            u = uc(x)
            def endpoint(bb):
                return phi0+om*(u-jc(x,bb))+pc(x,bb)
            b = mp.findroot(endpoint, (b_end-mp.mpf("0.01"), b_end+mp.mpf("0.01")), tol=mp.mpf(10)**(-digits+5), maxsteps=30)
            if isinstance(b, mp.mpc) and abs(mp.im(b))>threshold:
                raise AssertionError("root left real outgoing branch")
            b = mp.re(b)
            assert abs(b) < a/mp.sqrt(f(a)), "emission turning bound"
            te = u-jc(x,b)
            ir = max(abs(te+jc(x,b)-u), abs(phi0+om*te+pc(x,b)))
            assert ir < threshold, "incidence residual"
            return b,te,ir

        for rr in RADII:
            r = mp.mpf(rr)
            b,te,ir = solve_at(r)
            U = lambda q: [1/(E+v(q)),v(q),mp.mpf(0)]
            sr = lambda q: mp.sqrt(1-f(q)*b*b/q**2)
            K = lambda q: [b*b/(q*q*(1+sr(q))),sr(q),b/q**2]
            ur,g = residuals(r,f,U)
            kr,_ = residuals(r,f,K,is_null=True)
            Ao = -(mp.matrix(U(r)).T*g*mp.matrix(K(r)))[0]
            ge = mp.matrix([[-f(a),-1,0],[-1,0,0],[0,0,a*a]])
            omega_e = -(mp.matrix(emitter(a)).T*ge*mp.matrix(K(a)))[0]
            Z = omega_e/Ao
            assert max(ur,kr) < threshold, "original geodesic equations or norms"
            delta = r*mp.mpf("1e-4")
            bp,tp,_ = solve_at(r+delta)
            bm,tm,_ = solve_at(r-delta)
            arrival = mp.quad(lambda q: 1/v(q), [r-delta,r+delta])/(mp.sqrt(h)*(tp-tm))
            arrival_error = abs(arrival/Z-1)
            assert arrival_error < mp.mpf("1e-7"), "actual arrival derivative"
            # Deliberately wrong derivative holding b fixed: must not pass.
            te_r_fixed_b = 1/(v(r)*(E+v(r)))-b*b/(r*r*sr(r)*(1+sr(r)))
            fixed_b_ratio = 1/(mp.sqrt(h)*v(r)*te_r_fixed_b)
            fixed_b_error = abs(fixed_b_ratio/Z-1)
            assert fixed_b_error > mp.mpf("1e-4"), "failed to detect omitted impact-parameter variation"
            record = dict(digits=digits,R=rr,b=sstr(b),te=sstr(te),te_end=sstr(te_end),phi0=sstr(phi0),
                          Z=sstr(Z),incidence_residual=sstr(ir),original_equation_residual=sstr(max(ur,kr,emitter_res)),
                          arrival_relative_error=sstr(arrival_error),fixed_b_mutant_relative_error=sstr(fixed_b_error),
                          horizon_regular_f=sstr(f(r)),proper_gap=sstr(mp.sqrt(h)*(te_end-te)),
                          H_Z_proper_gap=sstr(H*Z*mp.sqrt(h)*(te_end-te)),
                          radial_Vpp=sstr(vpp))
            result["records"].append(record)
            print(json.dumps(record), flush=True)

    mp.mp.dps=70
    precision_errors=[]
    for rr in RADII:
        lo=next(z for z in result["records"] if z["R"]==rr and z["digits"]==40)
        hi=next(z for z in result["records"] if z["R"]==rr and z["digits"]==70)
        err=max(abs(mp.mpf(lo[k])/mp.mpf(hi[k])-1) for k in ["b","te","Z","H_Z_proper_gap"])
        assert err < mp.mpf("1e-30"), "precision comparison"
        precision_errors.append(sstr(err))
    result["precision_errors"]=precision_errors
    result["status"]="PASS"
except Exception as exc:
    result["status"]="FAIL"
    result["failures"].append({"type": type(exc).__name__, "message":str(exc)})
    print("CHECK FAILURE: "+repr(exc), file=sys.stderr, flush=True)
finally:
    result["elapsed_seconds"]=time.time()-started
    result["peak_rss_KiB"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (OUT/OUTPUT_NAME).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"solve_attempts":result["solve_attempts"],"output":OUTPUT_NAME,"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
sys.exit(0 if result["status"]=="PASS" else 1)
