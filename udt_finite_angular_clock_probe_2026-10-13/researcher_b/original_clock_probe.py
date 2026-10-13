"""FAC1 B: original-coordinate preparation and two independent null incidences."""
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import root
from numpy.polynomial.legendre import leggauss


class ClockProbe:
    def __init__(self, exponents=(-1/3, 2/3, 2/3), epsilon=0., fine=False):
        self.r = np.array(exponents, dtype=float)
        self.epsilon = float(epsilon)
        self.fine = fine
        self.z, self.w = leggauss(64 if fine else 32)
        self.rtol = 4e-14 if fine else 2e-12
        self.atol = 4e-16 if fine else 2e-14

    def geom(self, t):
        t = np.asarray(t)
        f = self.epsilon*(t-1)**2/2
        fp = self.epsilon*(t-1)
        lapse = np.exp(f)
        a = np.exp(f[..., None])*t[..., None]**self.r
        h = fp[..., None]+self.r/t[..., None]
        return lapse, a, h, fp

    def integrate(self, fun, lo, hi):
        ts = (lo+hi)/2+(hi-lo)*self.z/2
        return (hi-lo)/2*np.einsum('i,ij->j', self.w, fun(ts))

    def prepare(self, length, mu):
        n = np.array([mu, np.sqrt(max(0., 1-mu*mu)), 0.])
        def ode(s, y):
            t, v = y[:2]
            ut, ui = y[5], y[6:9]
            lapse, a, h, b = self.geom(t)
            xp = n/a**2
            vt = -b*v*v-np.sum(a*a*h*xp*xp)/(lapse*lapse)
            put = -b*v*ut-np.sum(a*a*h*xp*ui)/(lapse*lapse)
            pui = -h*(v*ui+xp*ut)
            return np.r_[v, vt, xp, put, pui]
        y0 = np.array([1., 0., 0., 0., 0., 1., 0., 0., 0.])
        sol = solve_ivp(ode, (0., length), y0, method='DOP853',
                        rtol=self.rtol, atol=self.atol)
        if not sol.success:
            raise RuntimeError(sol.message)
        y = sol.y[:, -1]
        t, v, x, ut, ui = y[0], y[1], y[2:5], y[5], y[6:9]
        lapse, a, h, b = self.geom(t)
        momenta = a*a*ui
        errors = {
            'spacelike_norm': abs(-lapse*lapse*v*v+np.sum(n*n/(a*a))-1),
            'clock_norm': abs(-lapse*lapse*ut*ut+np.sum(a*a*ui*ui)+1),
            'orthogonality': abs(-lapse*lapse*v*ut+np.sum(n*ui)),
            'receiver_ut_match': abs(ut-np.sqrt(1+np.sum(momenta*momenta/(a*a)))/lapse),
        }
        return t, x, momenta, errors

    def one(self, length, mu):
        tp, xp, momenta, errors = self.prepare(length, mu)
        def bvel(ts):
            lapse, a, _, _ = self.geom(ts)
            gamma = np.sqrt(1+np.sum(momenta*momenta/(a*a), axis=-1))
            return lapse[:, None]*momenta/(a*a*gamma[:, None])
        def rayvel(ts, q):
            lapse, a, _, _ = self.geom(ts)
            freq = np.sqrt(np.sum(q*q/(a*a), axis=-1))
            return lapse[:, None]*q/(a*a*freq[:, None])
        def q_of_angle(angle):
            return np.array([np.cos(angle), np.sin(angle), 0.])
        def outgoing(vars):
            angle, ta = vars
            q = q_of_angle(angle)
            return (self.integrate(lambda ts: rayvel(ts, q), 1., ta)
                    -xp-self.integrate(bvel, tp, ta))[:2]
        def incoming(vars):
            angle, ta = vars
            q = q_of_angle(angle)
            return (xp+self.integrate(lambda ts: rayvel(ts, q), tp, ta))[:2]
        theta = np.arccos(mu)
        out = root(outgoing, [theta, 1+length], method='hybr', options={'xtol':1e-11})
        rev = root(incoming, [theta+np.pi, tp+length], method='hybr', options={'xtol':1e-11})
        oe, re = np.max(np.abs(outgoing(out.x))), np.max(np.abs(incoming(rev.x)))
        errors.update(outgoing_incidence=float(oe), reverse_incidence=float(re))
        if max(oe, re) >= 2e-12 or out.x[1] <= max(1., tp) or rev.x[1] <= max(1., tp):
            raise RuntimeError({'L':length, 'mu':mu, 'out':out.message, 'rev':rev.message,
                                'out_x':out.x.tolist(), 'rev_x':rev.x.tolist(), 'errors':errors})
        if max(errors.values()) >= 2e-10:
            raise RuntimeError({'L':length, 'mu':mu, 'errors':errors})
        def omega(t, q, p):
            lapse, a, _, _ = self.geom(t)
            w = np.sqrt(np.sum(q*q/(a*a)))
            gamma = np.sqrt(1+np.sum(p*p/(a*a)))
            return w*gamma-np.sum(q*p/(a*a))
        qo, qr = q_of_angle(out.x[0]), q_of_angle(rev.x[0])
        plus = omega(1., qo, np.zeros(3))/omega(out.x[1], qo, momenta)
        minus = omega(tp, qr, momenta)/omega(rev.x[1], qr, np.zeros(3))
        return dict(L=float(length), mu=float(mu), epsilon=self.epsilon,
                    log_plus=float(np.log(plus)), log_minus=float(np.log(minus)),
                    preparation_t=float(tp), preparation_x=xp.tolist(),
                    receiver_momenta=momenta.tolist(), outgoing_q=qo.tolist(), reverse_q=qr.tolist(),
                    outgoing_t=float(out.x[1]), reverse_t=float(rev.x[1]),
                    outgoing_root_success=bool(out.success), reverse_root_success=bool(rev.success),
                    errors={k:float(v) for k,v in errors.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output')
    ap.add_argument('--fine', action='store_true')
    ap.add_argument('--epsilon', type=float, default=0.)
    ap.add_argument('--lengths', default='0.08,0.06,0.04,0.03,0.02')
    ap.add_argument('--flat', action='store_true')
    args = ap.parse_args()
    output = Path(args.output)
    if output.exists():
        raise RuntimeError('REFUSE_DATA_OVERWRITE')
    started = time.monotonic()
    probe = ClockProbe(exponents=(0.,0.,0.) if args.flat else (-1/3,2/3,2/3),
                       epsilon=args.epsilon, fine=args.fine)
    z, weights = leggauss(48 if args.fine else 24)
    mus, weights = (z+1)/2, weights/2
    lengths = [float(x) for x in args.lengths.split(',')]
    results = []
    for length in lengths:
        rows = [probe.one(length, mu) for mu in mus]
        mp = sum(w*x['log_plus'] for w,x in zip(weights, rows))
        mm = sum(w*x['log_minus'] for w,x in zip(weights, rows))
        axes = [probe.one(length, mu) for mu in (0.,1.)]
        errors = {key:max(x['errors'][key] for x in rows+axes) for key in rows[0]['errors']}
        result = dict(L=length, M_plus=mp, M_minus=mm, plus_over_L4=mp/length**4,
                      minus_over_L4=mm/length**4, max_errors=errors, axes=axes,
                      angular_weights=weights.tolist(), angular_records=rows)
        results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k not in
                          ('axes','angular_weights','angular_records')}), flush=True)
    payload = dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                   arguments=vars(args), dtype='float64', angular_order=len(mus),
                   time_quadrature_order=len(probe.z), rtol=probe.rtol, atol=probe.atol,
                   duration_seconds=time.monotonic()-started, results=results)
    output.write_text(json.dumps(payload, indent=2)+'\n')


if __name__ == '__main__':
    main()
