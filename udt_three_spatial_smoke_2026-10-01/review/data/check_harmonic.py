#!/usr/bin/env python3
"""Independent initial contracted-Christoffel check from saved g and its velocity."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from check_constraints import derivative


def contracted(g, v, periods):
    inverse = np.linalg.inv(g)
    derivatives = [v] + [derivative(g, i, periods) for i in range(3)]
    covector = np.zeros(g.shape[:-1])
    for mu in range(4):
        for a in range(4):
            for b in range(4):
                covector[..., mu] += inverse[..., a, b] * (
                    derivatives[a][..., mu, b] - .5 * derivatives[mu][..., a, b])
    return covector


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    ap.add_argument('--limit', type=float, default=2e-5)
    args = ap.parse_args()
    with np.load(args.input, allow_pickle=False) as data:
        g, v = data['g'], data['v']
        periods = np.broadcast_to(data['period'], (3,))
        H = contracted(g, v, periods)
        bad_v = v.copy()
        bad_v[..., 0, 0] += .02
        bad_H = contracted(g, bad_v, periods)
    largest = float(np.max(np.abs(H)))
    bad_largest = float(np.max(np.abs(bad_H)))
    assert bad_largest > .009
    result = {'input': str(args.input), 'sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'contracted_Christoffel_abs_max_by_covector_component': np.max(np.abs(H), axis=(0, 1, 2)).tolist(),
              'invalid_v00_caught_abs_max': bad_largest, 'limit': args.limit,
              'status': 'PASS' if np.isfinite(largest) and largest <= args.limit else 'FAIL',
              'scope': 'initial harmonic gauge from independent saved-metric contraction, no evolution certification'}
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if result['status'] != 'PASS':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
