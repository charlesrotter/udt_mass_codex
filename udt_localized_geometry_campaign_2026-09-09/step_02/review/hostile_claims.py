"""Intentional red runs: feed preserved invalid conclusions to exact guards.

This reuses reviewer algebra and is catch-proof/regression, not another
independence axis. Each registered command is expected to return nonzero.
"""
import pathlib
import runpy
import sys

root = pathlib.Path(__file__).resolve().parent
mode, = sys.argv[1:]
if mode == 'raised_map':
    data = runpy.run_path(str(root / 'direct_checks.py'))
    assert data['extra'] == data['s'].zeros(3, 1), 'REJECTED: varying metric raising preserves the source linearization'
else:
    data = runpy.run_path(str(root / 'independent_algebra.py'))
    if mode == 'central_parity':
        assert data['weak_parity_average'].rank() == 0, 'REJECTED: central inversion removes the rotational obstruction'
    elif mode == 'raw_blend':
        assert data['blend_H'] == 0, 'REJECTED: lawful endpoints imply their cutoff blend solves all constraints'
    else:
        raise ValueError(mode)
