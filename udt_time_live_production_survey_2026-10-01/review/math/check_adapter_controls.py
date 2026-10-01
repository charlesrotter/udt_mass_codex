"""Finite positive/negative interface controls before TPS1 outcomes."""
import json
from pathlib import Path
import tempfile
import numpy as np
import check_survey as check

results = []
g = np.broadcast_to(np.diag([-1., 1., 1., 1.]), (4, 4, 4, 4, 4)).copy()
v = np.zeros_like(g)
check.check_geometry(g, v)
result = check.adm_row(g, v, 2*np.pi)
assert result['status'] == 'PASS'
results.append(dict(name='flat_positive_control', status='PASS'))

for label, change in [
    ('nonsymmetric_metric', lambda a, b: a.__setitem__((..., 0, 1), .01)),
    ('nonsymmetric_velocity', lambda a, b: b.__setitem__((..., 0, 1), .01)),
    ('nonfinite_metric', lambda a, b: a.__setitem__((0, 0, 0, 0, 0), np.nan)),
    ('nonspacelike_slice', lambda a, b: a.__setitem__((..., 1, 1), -1.)),
    ('positive_time_inverse', lambda a, b: a.__setitem__((..., 0, 0), 1.)),
]:
    a, b = g.copy(), v.copy()
    change(a, b)
    try:
        check.check_geometry(a, b)
    except ValueError as error:
        results.append(dict(name=label, caught=str(error)))
    else:
        raise AssertionError(label)

for name, call in [
    ('outside_scope', lambda: check.checked_path('/tmp/tps1-not-owned')),
    ('wrong_float_dtype', lambda: check.check_geometry(g.astype(np.float32), v)),
    ('wrong_velocity_shape', lambda: check.check_geometry(g, v[:2])),
]:
    try:
        call()
    except ValueError as error:
        results.append(dict(name=name, caught=str(error)))
    else:
        raise AssertionError(name)

with tempfile.TemporaryDirectory(prefix='tps1_math_control_', dir=check.HERE) as folder:
    path = Path(folder)/'artifact.json'
    check.write(path, dict(value=1))
    assert check.checked_path(path, check.sha(path)) == path
    try:
        check.checked_path(path, '0'*64)
    except ValueError as error:
        results.append(dict(name='artifact_hash_catch', caught=str(error)))
    else:
        raise AssertionError('hash')
    try:
        check.write(path, dict(value=2))
    except FileExistsError:
        results.append(dict(name='immutable_output', status='PASS'))
    else:
        raise AssertionError('overwrite')

print(json.dumps(dict(status='PASS', rows=results,
    source_sha256=check.sha(__file__), checked_source_sha256=check.sha(check.__file__),
    scope='Adapter schema/geometry/hash/output controls; not production outcome qualification'), indent=2))
