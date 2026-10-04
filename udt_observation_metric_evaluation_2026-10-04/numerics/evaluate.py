"""OEV1 supplied-metric ray evaluator; no metric evolution or physical selector.

All physical choices are supplied controls (FREE/free-and-explored), from PRT1.
Numerical constants below are numerical controls, not physical parameters.
Use the unchanged repository capture.py for memory/thread/no-timeout controls.
"""
from pathlib import Path
import argparse, hashlib, json, os, signal, sys
import numpy as np
from scipy.integrate import solve_ivp

STOP = False
NFE = 0
SOLVES = 0


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save_new(p, obj):
    with Path(p).open('x') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n')


def request_stop(signum, frame):
    global STOP
    STOP = True


def metric(kind, t):
    # FREE: fixed nondimensional supplied controls; no fitted or native scale.
    if kind == 'flat':
        return np.ones_like(t), np.zeros_like(t)
    power = {'quadratic': 2, 'cubic': 3}[kind]
    return 1 + t**power, power * t**(power - 1)


def rhs(kind, y):
    t, x, kt, kx = y[:4]
    a, ad = metric(kind, t)
    if not a > 0:
        raise ValueError('OUTSIDE_POSITIVE_METRIC_DOMAIN')
    H = ad / a
    P = y[4:].reshape(2, 2)
    connection = np.array([[0., a * ad * kx], [H * kx, H * kt]])
    return np.r_[kt, kx, -a * ad * kx**2, -2 * H * kt * kx,
                 (-connection @ P).ravel()]


def solve_ray(kind, te, distance, tolerance, cfg, save_trajectory=False):
    global NFE, SOLVES
    SOLVES += 1
    if SOLVES > cfg['max_solves_per_command']:
        raise RuntimeError('RAY_SOLVE_RESOURCE_STOP')
    a0, _ = metric(kind, te)
    direction = float(np.sign(distance))
    if direction == 0:
        raise ValueError('ZERO_LENGTH_QUERY')
    initial = np.r_[te, 0., 1., direction / a0, np.eye(2).ravel()]

    def fun(lam, y):
        global NFE
        NFE += 1
        if STOP:
            raise KeyboardInterrupt('MANUAL_STOP')
        if NFE > cfg['max_rhs_per_command']:
            raise RuntimeError('RHS_RESOURCE_STOP')
        return rhs(kind, y)

    def arrived(lam, y):
        return direction * (y[1] - distance)

    def domain_stop(lam, y):
        return cfg['maximum_coordinate_time'] - y[0]

    arrived.terminal = True
    arrived.direction = 1
    domain_stop.terminal = True
    domain_stop.direction = -1
    sol = solve_ivp(fun, [0, cfg['maximum_affine_parameter']], initial,
                    method='DOP853', rtol=tolerance,
                    atol=tolerance * cfg['absolute_tolerance_factor'],
                    events=[arrived, domain_stop], dense_output=True)
    if not sol.success or len(sol.t_events[0]) != 1:
        raise RuntimeError('NO_CERTIFIED_FINITE_ARRIVAL:' + sol.message)
    end = sol.y_events[0][0]
    if end[2] <= 0:
        raise ValueError('NONFUTURE_ENDPOINT')
    result = dict(te=float(te), distance=float(distance),
                  tr=float(end[0]), lambda_end=float(sol.t[-1]),
                  kt_end=float(end[2]), kx_end=float(end[3]),
                  Z=float(1 / end[2]), logZ=float(-np.log(end[2])),
                  endpoint_error=float(abs(end[1] - distance)), nfev=sol.nfev)
    if not save_trajectory:
        return result, None

    lam = np.unique(np.r_[sol.t, np.linspace(0, sol.t[-1], cfg['saved_nodes'])])
    Y = sol.sol(lam).T
    a, ad = metric(kind, Y[:, 0])
    norm = -Y[:, 2]**2 + a**2 * Y[:, 3]**2
    norm_scale = Y[:, 2]**2 + a**2 * Y[:, 3]**2
    momentum = a**2 * Y[:, 3]
    g0 = np.diag([-1., float(a0**2)])
    metricity = []
    transported_k = []
    for y, av in zip(Y, a):
        P = y[4:].reshape(2, 2)
        metricity.append(np.max(np.abs(P.T @ np.diag([-1., av**2]) @ P - g0)))
        transported_k.append(np.max(np.abs(P @ initial[2:4] - y[2:4])))

    # Original affine equations: differentiate the saved dense trajectory,
    # compare to the unpreconditioned RHS. This is a numerical residual,
    # not independent implementation or a rigorous continuum error enclosure.
    raw_residual, scaled_residual, refinement_change = [], [], []
    for left, right in zip(sol.t[:-1], sol.t[1:]):
        middle = (left + right) / 2
        h = min((right - left) / 8, 1e-3 * (1 + abs(middle)))
        def derivative(step):
            return (sol.sol(middle - 2*step) - 8*sol.sol(middle - step)
                    + 8*sol.sol(middle + step) - sol.sol(middle + 2*step)) / (12*step)
        d1, d2 = derivative(h), derivative(h/2)
        expected = rhs(kind, sol.sol(middle))
        raw_residual.append(np.max(np.abs(d2 - expected)))
        scaled_residual.append(np.max(np.abs(d2 - expected)/(1 + np.abs(expected))))
        refinement_change.append(np.max(np.abs(d2 - d1)))
    result.update(null_absolute=float(np.max(np.abs(norm))),
                  null_relative=float(np.max(np.abs(norm)/norm_scale)),
                  momentum_relative=float(np.max(np.abs(momentum/(direction*a0)-1))),
                  metricity_absolute=float(max(metricity)),
                  transported_k_absolute=float(max(transported_k)),
                  original_residual_absolute=float(max(raw_residual)),
                  original_residual_scaled=float(max(scaled_residual)),
                  residual_difference_refinement=float(max(refinement_change)),
                  saved_nodes=len(lam))
    return result, {'lambda': lam, 'state': Y}


def evaluate_case(case, tolerance, cfg):
    kind, L = case['metric'], case['L']
    center, trajectory = solve_ray(kind, 0., L, tolerance, cfg, True)
    perturbations = []
    derivatives = []
    for h in cfg['emission_steps']:
        minus, _ = solve_ray(kind, -h, L, tolerance, cfg)
        plus, _ = solve_ray(kind, h, L, tolerance, cfg)
        derivative = (plus['tr']-minus['tr'])/(2*h)
        derivatives.append(derivative)
        perturbations.append(dict(h=h, minus=minus, plus=plus,
                                  arrival_derivative=derivative))
    assert len(derivatives) == 2
    assert cfg['emission_steps'][0] == 2 * cfg['emission_steps'][1]
    richardson = (4*derivatives[1]-derivatives[0])/3
    center.update(arrival_derivative_richardson=richardson,
                  arrival_frequency_relative=abs(richardson/center['Z']-1),
                  arrival_step_difference=abs(derivatives[1]-derivatives[0])/3)
    reverse = echo = None
    if case.get('reverse'):
        reverse, _ = solve_ray(kind, 0., -L, tolerance, cfg)
    if case.get('echo'):
        echo, _ = solve_ray(kind, center['tr'], -L, tolerance, cfg)
    return dict(case=case, tolerance=tolerance, center=center,
                perturbations=perturbations, reverse=reverse, echo=echo), trajectory


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config'); ap.add_argument('output')
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--signal-after', type=int, default=0)
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    out = Path(args.output); out.mkdir(exist_ok=True, parents=True)
    meta = dict(config_sha256=sha(args.config), code_sha256=sha(__file__),
                smoke=args.smoke, equation='original affine null geodesic and parallel transport',
                numpy=np.__version__, scipy=__import__('scipy').__version__)
    mp = out/'metadata.json'
    if mp.exists():
        if json.loads(mp.read_text()) != meta:
            raise RuntimeError('CHECKPOINT_CONFIG_OR_CODE_MISMATCH')
    else:
        save_new(mp, meta)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    cases = [c for c in cfg['cases'] if c.get('smoke')] if args.smoke else cfg['cases']
    tols = [cfg['tolerances'][-1]] if args.smoke else cfg['tolerances']
    completed = skipped = 0
    for case in cases:
        for ti, tol in enumerate(tols):
            key = case['id']+'_t'+str(ti)
            rp, tp = out/(key+'.json'), out/(key+'.npz')
            if rp.exists():
                previous = json.loads(rp.read_text())
                if previous['binding'] != meta or sha(tp) != previous['trajectory_sha256']:
                    raise RuntimeError('CHECKPOINT_CONTENT_MISMATCH')
                skipped += 1
                continue
            if STOP:
                print(json.dumps(dict(status='INTERRUPTED_AFTER_CHECKPOINT',
                                      completed=completed, skipped=skipped, rhs=NFE, solves=SOLVES)))
                return 130
            if tp.exists():
                raise RuntimeError('INCOMPLETE_CHECKPOINT_PRESERVED_REQUIRES_REVIEW')
            result, trajectory = evaluate_case(case, tol, cfg)
            # The NPZ is written once, then its hash is committed in the row.
            with tp.open('xb') as f:
                np.savez_compressed(f, **trajectory)
            result.update(binding=meta, trajectory_sha256=sha(tp))
            save_new(rp, result)
            completed += 1
            if args.signal_after and completed == args.signal_after:
                os.kill(os.getpid(), signal.SIGINT)
    print(json.dumps(dict(status='FINITE_EVALUATION_COMPLETE', completed=completed,
                          skipped=skipped, rhs=NFE, solves=SOLVES)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
