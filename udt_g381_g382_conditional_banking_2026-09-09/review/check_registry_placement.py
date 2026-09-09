"""Independent byte placement/reconstruction check and actual misplaced-row probe."""
import csv
import hashlib
import importlib.util
import io
import pathlib
import sys
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
registry = ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
lines = registry.read_bytes().splitlines(keepends=True)
new = [line for line in lines if line.startswith((b'G381\t', b'G382\t'))]
old = [line for line in lines if not line.startswith((b'G381\t', b'G382\t'))]
assert len(new) == 2 and lines[1:3] == new
assert new[0].startswith(b'G381\t') and new[1].startswith(b'G382\t')
assert hashlib.sha256(b''.join(old)).hexdigest() == 'ae78d872143a62d6f3811d77ca909d1b90a2dee2f259b0ec862c1fd502e23afe'
initial = ROOT / 'udt_g381_g382_conditional_banking_2026-09-09/INITIAL_REGISTRY_DIFF.patch'
initial_new = [line[1:] for line in initial.read_bytes().splitlines(keepends=True)
               if line.startswith((b'+G381\t', b'+G382\t'))]
assert initial_new == new, 'new row bytes changed rather than moved'

with (ROOT / 'udt_g244_metric_native_observer_sky_response_query_2026-08-24/SOURCE_MANIFEST.tsv').open() as handle:
    pins = list(csv.DictReader(handle, delimiter='\t'))
expected = next(r['sha256'] for r in pins if r['path'] == 'CURRENT_SCIENTIFIC_PREMISES.tsv')
g244_index = next(i for i, line in enumerate(lines) if line.startswith(b'G244\t'))
historical = lines[0] + b''.join(lines[g244_index+1:])
assert hashlib.sha256(historical).hexdigest() == expected
print('PASS: relocated new rows preserve old bytes and exact G244 historical registry', flush=True)

if sys.argv[1] == 'misplaced':
    spec = importlib.util.spec_from_file_location('guards', ROOT / 'verify_current_scientific_premises.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    misplaced = b''.join(old + new)
    original_open = pathlib.Path.open
    def overlay(path, mode='r', *args, **kwargs):
        if path == registry:
            return io.BytesIO(misplaced) if 'b' in mode else io.StringIO(misplaced.decode())
        return original_open(path, mode, *args, **kwargs)
    print('Actual read overlay: move unchanged G381/G382 to registry bottom; no source writes', flush=True)
    with patch.object(pathlib.Path, 'open', overlay):
        module.validate_neighboring_tidal_banking(ROOT, authenticate_sources=True)
    raise RuntimeError('ACTUAL FALSE PASS: misplaced rows accepted')
