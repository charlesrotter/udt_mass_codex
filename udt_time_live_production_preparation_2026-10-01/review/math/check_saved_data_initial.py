"""Thin scoped adapter reusing fixed independent TDS1 original ADM methods."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT/'udt_three_spatial_smoke_2026-10-01/review/data'
sys.path.insert(0, str(OLD))
from check_constraints import constraints, derivative
from check_harmonic import contracted


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extrinsic(g, v, period):
    """Independently reconstruct K from Lie_beta gamma, with live lapse/shift."""
    gamma = g[..., 1:, 1:]
    gamma_inv = np.linalg.inv(gamma)
    spacetime_inv = np.linalg.inv(g)
    alpha = 1/np.sqrt(-spacetime_inv[..., 0, 0])
    beta = np.einsum('...ij,...j->...i', gamma_inv, g[..., 0, 1:])
    dgamma = [derivative(gamma, k, period) for k in range(3)]
    dbeta = [derivative(beta, k, period) for k in range(3)]
    lie = np.zeros_like(gamma)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                lie[..., i, j] += beta[..., k]*dgamma[k][..., i, j]
                lie[..., i, j] += gamma[..., k, j]*dbeta[i][..., k] + gamma[..., i, k]*dbeta[j][..., k]
    return gamma, (lie-v[..., 1:, 1:])/(2*alpha[..., None, None]), alpha, beta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output')
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--kind', choices=['initial', 'window'], required=True)
    ap.add_argument('--limit', type=float, default=2e-5)
    args = ap.parse_args()
    if not np.isfinite(args.limit) or args.limit <= 0:
        ap.error('finite positive limit required')
    rows = []
    for filename in args.inputs:
        with np.load(filename, allow_pickle=False) as saved:
            period = np.broadcast_to(saved['period'], (3,))
            indices = [None] if args.kind == 'initial' else sorted(set([0, len(saved['times'])//2, len(saved['times'])-1]))
            for index in indices:
                g = saved['g'] if index is None else saved['g'][index]
                v = saved['v'] if index is None else saved['v'][index]
                gamma, K, alpha, beta = extrinsic(g, v, period)
                if index is None:
                    assert np.max(abs(gamma-saved['gamma'])) == 0
                    assert np.max(abs(K-saved['K'])) < 1e-14
                result, _ = constraints(gamma, K, period)
                covector = contracted(g, v, period)
                vector = np.einsum('...ab,...b->...a', np.linalg.inv(g), covector)
                result.update(input=filename, input_sha256=sha(filename), index=index,
                    time=None if index is None else float(saved['times'][index]),
                    harmonic_covector_abs_max=float(abs(covector).max()),
                    harmonic_vector_abs_max=float(abs(vector).max()),
                    lapse_minmax=[float(alpha.min()),float(alpha.max())],
                    shift_abs_max=float(abs(beta).max()))
                quantities = [result['hamiltonian_abs_max'], *result['momentum_abs_max_by_component'], result['harmonic_vector_abs_max']]
                assert all(np.isfinite(x) and x <= args.limit for x in quantities), result
                if index is None:
                    seed = saved['seed']
                    trace = float(abs(np.trace(seed, axis1=-2, axis2=-1)).max())
                    div = sum(derivative(seed[...,j,:],j,period) for j in range(3))
                    divergence = float(abs(div).max())
                    assert trace < 2e-14 and divergence < 2e-13
                    result.update(seed_trace_abs_max=trace, seed_divergence_abs_max=divergence)
                    bad = v.copy(); bad[...,0,0] += .02
                    bad_residual = float(abs(contracted(g,bad,period)).max())
                    assert bad_residual > .009
                    result['invalid_harmonic_velocity_caught'] = bad_residual
                rows.append(result)
    result = dict(status='PASS', kind=args.kind, limit=args.limit, rows=rows,
        numpy=np.__version__, source_sha256=sha(__file__),
        reused_independent_sources={str(p.relative_to(ROOT)):sha(p) for p in [OLD/'check_constraints.py', OLD/'check_harmonic.py']},
        attribution='Reuses fixed TDS1 independent NumPy original ADM and harmonic implementations; new adapter independently reconstructs K through Lie_beta gamma. No producer code imports. Same Fourier mathematics, no independent time integrator.',
        scope='Finite saved points only, with supplied periodic marking; no continuum or generic-stability claim.')
    with Path(args.output).open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
