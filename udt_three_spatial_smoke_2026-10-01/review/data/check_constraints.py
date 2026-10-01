#!/usr/bin/env python3
"""Independent CPU original 3+1 constraints; no producer modules imported.

Input NPZ gamma,K: (Nx,Ny,Nz,3,3), period scalar or three-vector (optional 2pi).
This is finite collocation evidence, not continuum certification.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np


def derivative(value, axis, periods):
    n = value.shape[axis]
    wave = 2 * np.pi * np.fft.fftfreq(n, d=float(periods[axis]) / n)
    # A real collocation first derivative sets the even-grid Nyquist mode to zero.
    if n % 2 == 0:
        wave[n // 2] = 0
    shape = [1] * value.ndim
    shape[axis] = n
    return np.fft.ifft(1j * wave.reshape(shape) * np.fft.fft(value, axis=axis), axis=axis).real


def constraints(gamma, K, periods):
    if gamma.shape != K.shape or gamma.shape[-2:] != (3, 3) or gamma.ndim != 5:
        raise ValueError('gamma,K require identical (Nx,Ny,Nz,3,3) shape')
    if any(n < 4 or n > 32 for n in gamma.shape[:3]):
        raise ValueError('bounded checker mesh must be between4 and32 per direction')
    if gamma.dtype != np.float64 or K.dtype != np.float64:
        raise ValueError('float64 required')
    if not np.all(np.isfinite(gamma)) or not np.all(np.isfinite(K)):
        raise ValueError('nonfinite data')
    if np.max(np.abs(gamma - gamma.swapaxes(-1, -2))) > 1e-12 or np.max(np.abs(K - K.swapaxes(-1, -2))) > 1e-12:
        raise ValueError('nonsymmetric data')
    eig = np.linalg.eigvalsh(gamma)
    if np.min(eig) <= 0:
        raise ValueError('nonpositive spatial metric')
    inv = np.linalg.inv(gamma)
    dg = [derivative(gamma, i, periods) for i in range(3)]
    connection = np.zeros(gamma.shape[:3] + (3, 3, 3))
    for k in range(3):
        for i in range(3):
            for j in range(3):
                for ell in range(3):
                    connection[..., k, i, j] += .5 * inv[..., k, ell] * (
                        dg[i][..., ell, j] + dg[j][..., ell, i] - dg[ell][..., i, j])
    dconnection = [derivative(connection, i, periods) for i in range(3)]
    Ricci = np.zeros_like(gamma)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                Ricci[..., i, j] += dconnection[k][..., k, i, j] - dconnection[j][..., k, i, k]
                for ell in range(3):
                    Ricci[..., i, j] += (
                        connection[..., k, i, j] * connection[..., ell, k, ell]
                        - connection[..., ell, i, k] * connection[..., k, j, ell])
    R = np.einsum('...ij,...ij->...', inv, Ricci)
    mixed = np.einsum('...ik,...kj->...ij', inv, K)
    trace = np.trace(mixed, axis1=-2, axis2=-1)
    norm2 = np.einsum('...ij,...ji->...', mixed, mixed)
    H = R + trace * trace - norm2
    dmixed = [derivative(mixed, i, periods) for i in range(3)]
    M = np.zeros(gamma.shape[:3] + (3,))
    for i in range(3):
        M[..., i] -= derivative(trace, i, periods)
        for j in range(3):
            M[..., i] += dmixed[j][..., j, i]
            for k in range(3):
                M[..., i] += (connection[..., j, j, k] * mixed[..., k, i]
                              - connection[..., k, j, i] * mixed[..., j, k])
    derivatives = [np.concatenate((dg[i].reshape(-1), derivative(K, i, periods).reshape(-1)))
                   for i in range(3)]
    gram = np.array([[np.dot(x, y) / x.size for y in derivatives] for x in derivatives])
    gram_eig = np.linalg.eigvalsh(gram)
    rank_tol = max(1e-24, float(np.max(gram_eig)) * 1e-10)
    result = {
        'shape': list(gamma.shape), 'dtype': str(gamma.dtype),
        'hamiltonian_abs_max': float(np.max(np.abs(H))),
        'momentum_abs_max_by_component': np.max(np.abs(M), axis=(0, 1, 2)).tolist(),
        'scalar_curvature_abs_max': float(np.max(np.abs(R))),
        'trace_K_minmax': [float(trace.min()), float(trace.max())],
        'spatial_metric_eigenvalue_minmax': [float(eig.min()), float(eig.max())],
        'spatial_derivative_gram_eigenvalues': gram_eig.tolist(),
        'spatial_derivative_gram_rank': int(np.count_nonzero(gram_eig > rank_tol)),
        'gram_rank_scope': 'excludes constant-coordinate translation symmetry only; not arbitrary Killing fields',
    }
    return result, {'H': H, 'M': M, 'R': R, 'Ricci': Ricci}


def selftest():
    n = 16
    periods = np.full(3, 2 * np.pi)
    x, y, z = np.meshgrid(*[np.arange(n) * 2 * np.pi / n] * 3, indexing='ij')
    gamma = np.broadcast_to(np.eye(3), (n, n, n, 3, 3)).copy()
    K = np.broadcast_to(np.diag([1 / 3, -2 / 3, -2 / 3]), gamma.shape).copy()
    seed, arrays = constraints(gamma, K, periods)
    assert seed['hamiltonian_abs_max'] < 1e-14 and np.max(np.abs(arrays['M'])) < 1e-14
    f = .01 * np.cos(x) + .015 * np.sin(y) + .012 * np.cos(z)
    conformal = gamma * np.exp(2 * f)[..., None, None]
    a = .1 + .02 * np.sin(x) - .013 * np.cos(y) + .017 * np.sin(z)
    varying_K = a[..., None, None] * conformal
    check, fields = constraints(conformal, varying_K, periods)
    grad_f2 = (.01 * np.sin(x)) ** 2 + (.015 * np.cos(y)) ** 2 + (.012 * np.sin(z)) ** 2
    analytic_R = np.exp(-2 * f) * (4 * f - 2 * grad_f2)
    analytic_M = np.stack([-.04 * np.cos(x), -.026 * np.sin(y), -.034 * np.cos(z)], axis=-1)
    R_error = float(np.max(np.abs(fields['R'] - analytic_R)))
    M_error = float(np.max(np.abs(fields['M'] - analytic_M)))
    assert R_error < 2e-12 and M_error < 2e-12
    bad_K = K.copy()
    bad_K[..., 0, 0] += .01 * np.cos(y)
    bad, _ = constraints(gamma, bad_K, periods)
    assert bad['hamiltonian_abs_max'] > .01
    assert max(bad['momentum_abs_max_by_component']) > .009
    assert check['spatial_derivative_gram_rank'] == 3
    return {'status': 'PASS', 'constant_seed': seed, 'analytic_conformal_R_error': R_error,
            'analytic_isotropic_K_momentum_error': M_error, 'deliberate_invalid_K_caught': bad,
            'numpy_version': np.__version__, 'scope': 'checker self-controls, not producer validation'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path, nargs='?')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--limit', type=float, default=2e-5)
    args = ap.parse_args()
    if args.selftest:
        result = selftest()
    else:
        if args.input is None or not math.isfinite(args.limit) or args.limit <= 0:
            ap.error('input and a finite positive limit required')
        with np.load(args.input, allow_pickle=False) as saved:
            period = np.asarray(saved['period'] if 'period' in saved.files else 2 * np.pi)
            periods = np.broadcast_to(period, (3,))
            if not np.all(np.isfinite(periods)) or np.min(periods) <= 0:
                raise ValueError('invalid coordinate periods')
            result, _ = constraints(saved['gamma'], saved['K'], periods)
        result.update(input=str(args.input), sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),
                      limit=args.limit, implementation='independent NumPy original metric/connection constraints')
        result['status'] = 'PASS' if max(result['hamiltonian_abs_max'], *result['momentum_abs_max_by_component']) <= args.limit else 'FAIL'
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if result['status'] != 'PASS':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
