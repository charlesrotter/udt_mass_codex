"""Recovered independent original-constraint review; producer code never imported."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = BASE / 'review/data'
sys.path.insert(0, str(OLD))
from check_constraints import constraints, derivative, selftest
from check_harmonic import contracted


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def density_momentum(gamma, K, periods):
    """D_j K^j_i = gamma^-1/2 d_j(gamma^1/2 K^j_i)-K^jk d_i gamma_jk/2."""
    inverse = np.linalg.inv(gamma)
    volume = np.sqrt(np.linalg.det(gamma))
    mixed = np.einsum('...jk,...ki->...ji', inverse, K)
    raised = np.einsum('...ja,...ab,...bk->...jk', inverse, K, inverse)
    trace = np.trace(mixed, axis1=-2, axis2=-1)
    result = np.zeros(gamma.shape[:-1])
    for i in range(3):
        result[..., i] = -derivative(trace, i, periods)
        result[..., i] -= .5 * np.einsum('...jk,...jk->...', raised, derivative(gamma, i, periods))
        for j in range(3):
            result[..., i] += derivative(volume * mixed[..., j, i], j, periods) / volume
    return result


records = []
for n in (8, 12, 16):
    path = BASE / f'initial_n{n}.npz'
    with np.load(path, allow_pickle=False) as data:
        periods = np.broadcast_to(data['period'], (3,))
        gamma, K, g, v = (data[key] for key in ('gamma', 'K', 'g', 'v'))
        original, arrays = constraints(gamma, K, periods)
        harmonic = contracted(g, v, periods)
        alternate_M = density_momentum(gamma, K, periods)
        seed = data['seed']
        seed_div = sum(derivative(seed[..., j, :], j, periods) for j in range(3))
        seed_trace = np.trace(seed, axis1=-2, axis2=-1)
        lorentz_eigenvalues = np.linalg.eigvalsh(g)
        assert np.all(lorentz_eigenvalues[..., 0] < 0)
        assert np.all(lorentz_eigenvalues[..., 1:] > 0)
        assert np.array_equal(g[..., 1:, 1:], gamma)
        assert np.array_equal(v[..., 1:, 1:], -2 * K)
        modified_v = v.copy()
        modified_v[..., 0, 0] += .02
        invalid = float(np.max(np.abs(contracted(g, modified_v, periods))))
        assert invalid > .009
        original.update(
            n=n, source_sha256=digest(path),
            harmonic_max=float(np.max(np.abs(harmonic))),
            alternate_density_momentum_max=float(np.max(np.abs(alternate_M))),
            momentum_formula_difference=float(np.max(np.abs(alternate_M - arrays['M']))),
            seed_trace_abs_max=float(np.max(np.abs(seed_trace))),
            seed_divergence_abs_max=float(np.max(np.abs(seed_div))),
            conformal_residual_history=data['constraint_history'].tolist(),
            invalid_v00_caught_abs_max=invalid,
        )
        assert max(original['hamiltonian_abs_max'], *original['momentum_abs_max_by_component'],
                   original['harmonic_max']) < 2e-5
        assert original['spatial_derivative_gram_rank'] == 3
        assert original['seed_trace_abs_max'] < 1e-14
        assert original['seed_divergence_abs_max'] < 1e-14
        records.append(original)

for earlier, later in zip(records, records[1:]):
    assert later['hamiltonian_abs_max'] < earlier['hamiltonian_abs_max']
    assert max(later['momentum_abs_max_by_component']) < max(earlier['momentum_abs_max_by_component'])
    assert later['harmonic_max'] < earlier['harmonic_max']

result = dict(
    status='INITIAL_DATA_REVIEW_PASS', numpy_version=np.__version__, records=records,
    checker_selftest=selftest(),
    source_hashes={str(p.relative_to(BASE)): digest(p) for p in [
        HERE/'check_initial.py', OLD/'check_constraints.py', OLD/'check_harmonic.py',
        BASE/'initial_data.py', BASE/'WORK_ORDER.md']},
    attribution='Original metric/connection and harmonic checkers reused unchanged from interrupted /root/tds_data; new context audited formulas and added density-divergence momentum comparison. No producer imports. Same Fourier discretization, not independent discretization.',
    scope='Finite saved initial data only; refinement evidence is not continuum certification. Rank3 excludes constant-coordinate translations, not arbitrary Killing fields. CONDITIONAL Ric=0, G312 GR FILTER ONLY; no native equation selection.',
)
print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
