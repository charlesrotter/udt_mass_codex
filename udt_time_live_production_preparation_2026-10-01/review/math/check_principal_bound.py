"""Independent frozen-principal-frequency and TT controls; no producer imports."""
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np


def bound(gamma, alpha, beta, kmax):
    if not all(np.all(np.isfinite(x)) for x in (gamma, alpha, beta, kmax)):
        raise ValueError('nonfinite geometry')
    eig = np.linalg.eigvalsh(gamma)
    if eig.min() <= 0 or alpha <= 0 or kmax <= 0:
        raise ValueError('invalid geometry or Fourier radius')
    return float(kmax * (np.sum(np.abs(beta)) + alpha * np.sqrt(3 / eig.min())))


def main():
    rng = np.random.default_rng(721019)
    modes = np.array(list(itertools.product(range(-4, 5), repeat=3)), dtype=float)
    records = []
    for index in range(24):
        A = rng.normal(size=(3, 3))
        gamma = A.T @ A + (.08 + index / 20) * np.eye(3)
        alpha = float(np.exp(rng.normal()))
        beta = rng.normal(size=3)
        exact = np.abs(modes @ beta) + alpha * np.sqrt(np.einsum('ni,ij,nj->n', modes, np.linalg.inv(gamma), modes))
        predicted = bound(gamma, alpha, beta, 4)
        assert np.max(exact) <= predicted * (1 + 1e-14)
        records.append(dict(index=index, principal_max=float(np.max(exact)), bound=predicted,
                            ratio=float(np.max(exact) / predicted)))
    # Dropping shift can badly underestimate even a flat constant metric.
    beta = np.array([4., 0., 0.])
    shifted_exact = 4 * (4 + 1)
    without_shift = 4 * np.sqrt(3)
    assert shifted_exact > without_shift
    assert shifted_exact <= bound(np.eye(3), 1., beta, 4)
    invalids = [(np.diag([1., 1., -1.]), 1., np.zeros(3), 4),
                (np.eye(3), float('nan'), np.zeros(3), 4),
                (np.eye(3), 1., np.array([float('inf'), 0., 0.]), 4),
                (np.eye(3), 1., np.zeros(3), 0)]
    caught = 0
    for args in invalids:
        try:
            bound(*args)
        except ValueError:
            caught += 1
    assert caught == len(invalids)
    tt_records = []
    for n in [np.array(x, dtype=float) for x in [(1,0,0),(1,1,0),(1,2,3),(-2,1,2),(0,0,-3)]]:
        # Independent QR null basis, not a producer cross-product construction.
        _, _, vh = np.linalg.svd(n.reshape(1, 3), full_matrices=True)
        p, q = vh[1:]
        for label, tensor in [('plus', np.outer(p,p)-np.outer(q,q)),
                              ('cross', np.outer(p,q)+np.outer(q,p))]:
            trace = float(abs(np.trace(tensor)))
            trans = float(np.max(np.abs(n @ tensor)))
            sym = float(np.max(np.abs(tensor-tensor.T)))
            assert max(trace, trans, sym) < 2e-15
            tt_records.append(dict(n=n.tolist(), kind=label, trace=trace, transversality=trans,
                                   symmetry=sym, norm2=float(np.sum(tensor*tensor))))
    print(json.dumps(dict(status='PASS', coordinate_bound_trials=records,
          omitted_shift_caught=dict(exact=shifted_exact, incorrect_bound=without_shift),
          invalid_hypotheses_caught=caught, analytic_tt_checks=tt_records,
          source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          numpy=np.__version__, producer_imports=False,
          scope='Finite controls for analytic TT and frozen-coefficient principal bound; no variable-coefficient or nonlinear stability assertion.'), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
