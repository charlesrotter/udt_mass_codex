"""Independent frozen-candidate inventory using Git baseline, not author helpers."""
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

R = Path(__file__).resolve().parent
P = R.parent
ROOT = P.parent
BASE = 'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19'

def git(*args):
    return subprocess.run(['git', '-c', 'core.preloadIndex=false', '-c',
        'index.threads=1', *args], cwd=ROOT, capture_output=True,
        check=True, timeout=10).stdout

def readrows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode()), delimiter='\t'))

pins = [line.split(maxsplit=1) for line in
        (P / 'INITIAL_IMPLEMENTATION_SHA256SUMS').read_text().splitlines()]
assert len(pins) == len({p for _, p in pins}) == 12
for sha, path in pins:
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
old = git('show', f'{BASE}:CURRENT_SCIENTIFIC_PREMISES.tsv')
now = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
a, b = readrows(old), readrows(now)
assert len(a) == len(b) == 365
assert list(a[0]) == list(b[0])
assert [r['premise_id'] for r in a] == [r['premise_id'] for r in b]
cells = [{'premise_id': x['premise_id'], 'field': k, 'before': x[k], 'after': y[k]}
         for x, y in zip(a, b) for k in x if x[k] != y[k]]
t = json.loads((P / 'REGISTRY_TRANSITION.json').read_text())
assert cells == t['changed_cells'] and len(cells) == 5
assert {c['premise_id'] for c in cells} == {'G312'}
assert {c['field'] for c in cells} == {
    'current_status', 'active_use', 'open_scope', 'forbidden_regression', 'precedence_rule'}
oldline = next(s for s in old.splitlines(keepends=True) if s.startswith(b'G312\t'))
newline = next(s for s in now.splitlines(keepends=True) if s.startswith(b'G312\t'))
assert oldline.decode() == t['before_line']
assert newline.decode() == t['after_line']
assert now.replace(newline, oldline) == old
status_before, status_after = cells[0]['before'], cells[0]['after']
assert status_before.split('__OWNER_ADOPTED_PROVISIONAL_POSTULATES')[0] == \
    status_after.split('__HISTORICAL_TWO_PREMISE_ADOPTION')[0]
assert status_before[status_before.index('__4690_PRODUCTION_CHECKS'):] == \
    status_after[status_after.index('__4690_PRODUCTION_CHECKS'):]
open_cell = next(c for c in cells if c['field'] == 'open_scope')
assert open_cell['after'].endswith(open_cell['before'])
changes = git('diff', '--name-only', BASE).decode().splitlines()
expected = {p for _, p in pins if '/' not in p or p == 'tests/test_startup_surface.py'}
assert set(changes) == expected, changes
assert git('diff', '--binary', BASE, '--', *sorted(expected)) == \
    (P / 'INITIAL_IMPLEMENTATION.patch').read_bytes()
source = (ROOT / 'verify_current_scientific_premises.py').read_text()
tree = ast.parse(source)
functions = {f.name: f for f in tree.body if isinstance(f, ast.FunctionDef)}
for name in ('main', 'validate_startup_surface'):
    node = functions[name].body[1] if isinstance(functions[name].body[0], ast.Expr) \
        and isinstance(functions[name].body[0].value, ast.Constant) else functions[name].body[0]
    assert isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
    assert isinstance(node.value.func, ast.Name)
    assert node.value.func.id == 'validate_gr_filter_authority', name
assert 'G325 dependency-free replay failed' in source
assert source.count('def registry_bytes_for_historical_banking(') == 1
print(json.dumps({'status': 'PASS', 'initial_frozen_pins': 12,
    'changed_g312_cells': [c['field'] for c in cells],
    'unchanged_other_registry_rows': 364, 'preserved_math_evidence_prefix_suffix': True,
    'original_open_scope_preserved': True, 'exact_patch_matches_baseline': True,
    'current_guard_first_in_main_and_startup': True,
    'scope': 'source and code correspondence, not scientific proof'}, indent=2))
