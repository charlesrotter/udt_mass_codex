import json
import platform
import resource
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))

exact = []
for m, lam, r in [(F(1), F(1, 1000), F(10)),
                  (F(2), F(0), F(30)),
                  (F(1, 2), F(-1, 700), F(13))]:
    f = 1 - 2*m/r - lam*r*r/3
    fp = 2*m/r**2 - 2*lam*r/3
    fpp = -4*m/r**3 - 2*lam/3
    p = -r*fp/(2*f)
    q = -r*r*fpp/(2*f) + r*r*fp*fp/(2*f*f)
    ap = f*(2*p*p+p-q)
    at = 1-f*(1+p)
    assert ap == -3*m/r and at == 3*m/r and ap+at == 0
    exact.append(dict(m=str(m), Lambda=str(lam), r=str(r),
                      A_parallel=str(ap), A_perp=str(at)))

# Proper period squared is 4 pi^2 h / Omega^2. Its dimensionless ratio is exact.
m, a, lam = F(1), F(1000), F(1, 10**9)
h = 1-3*m/a
omega2 = m/a**3-lam/3
period_squared_ratio = (m/a**3)/omega2
x = lam*a**3/(3*m)
assert period_squared_ratio == 1/(1-x) == F(3, 2)
recovery = {'a': str(a), 'Lambda': str(lam), 'metric_correction': str(lam*a*a/3),
            'frequency_squared_fractional_change': str(-x),
            'proper_period_squared_ratio': str(period_squared_ratio)}

# Unadopted higher-jet response E_ab=Hessian_ab(R), on R^(1,1) x S^2.
# At sphere radius s=2, R=2/s^2 is constant, so E=0, while Ric is not Einstein.
s = F(2)
gdiag = [-F(1), F(1), s*s, s*s]  # equatorial regular angular chart
ricdiag = [F(0), F(0), F(1), F(1)]
scalar = sum(ricdiag[i]/gdiag[i] for i in range(4))
tf = [ricdiag[i]-scalar*gdiag[i]/4 for i in range(4)]
assert scalar == F(1, 2) and tf != [F(0)]*4
response = {'metric':'flat Lorentzian 2-plane x round S^2 radius 2',
            'R':str(scalar), 'TF_Ric_diagonal':[str(z) for z in tf],
            'Hessian_R_diagonal':['0']*4,
            'status':'UNADOPTED logical control; violates R10 order/weight/nondegeneracy gates'}

samples = []
for digits in [50,90]:
    mp.mp.dps = digits
    m, a, lam, E = mp.mpf(1), mp.mpf(10), mp.mpf('0.001'), mp.mpf(1)
    H = mp.sqrt(lam/3)
    h = 1-3*m/a
    f_at_a = 1-2*m/a-lam*a*a/3
    Omega = mp.sqrt(m/a**3-lam/3)
    B = a/mp.sqrt(f_at_a)
    bound = 2*E*(1+Omega*B)/mp.sqrt(h)
    for r in map(mp.mpf, ['20','30','100','10000','10000000000']):
        f = 1-2*m/r-lam*r*r/3
        v = mp.sqrt(E*E-f)
        for b in map(mp.mpf, ['-2','0','2']):
            assert 1-f_at_a*b*b/(a*a) > 0
            S = mp.sqrt(1-f*b*b/(r*r))
            direct = (E-v*S)/f
            stable = (1+v*v*b*b/(r*r))/(E+v*S)
            assert abs(direct/stable-1)<mp.mpf('1e-40')
            Z = (1-Omega*b)/(mp.sqrt(h)*stable)
            tail = (1-Omega*b)/(mp.sqrt(h)*mp.sqrt(1+H*H*b*b))
            if f > 0: assert 0 < Z <= bound
            if r == mp.mpf('10000000000'):
                assert abs(Z/(H*r)/tail-1) < mp.mpf('1e-7')
            samples.append({'digits':digits,'r':str(r),'b':str(b),
                            'f':mp.nstr(f,25),'Z':mp.nstr(Z,25),
                            'Z_over_Hr':mp.nstr(Z/(H*r),25),
                            'tail_coefficient':mp.nstr(tail,25)})
    # At f=0, v=E and S=1; use arbitrary regular radius r_h=50.
    r_h, b = mp.mpf(50), mp.mpf(2)
    horizon_A = (1+E*E*b*b/(r_h*r_h))/(2*E)
    assert horizon_A > 0 and mp.isfinite(horizon_A)

result = {'python':platform.python_version(),'mpmath':mp.__version__,
          'precisions':[50,90],'finite_numeric_cases':len(samples)+2,
          'exact_cases':len(exact)+2,'angular_exact':exact,
          'proper_recovery':recovery,'response_control':response,
          'samples':samples,'verdict':'PASS; mathematical controls only'}
out = Path(__file__).with_name('CONTROL_RESULT.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'finite_numeric_cases':len(samples)+2,
                  'exact_cases':len(exact)+2,'output':str(out)},sort_keys=True))
