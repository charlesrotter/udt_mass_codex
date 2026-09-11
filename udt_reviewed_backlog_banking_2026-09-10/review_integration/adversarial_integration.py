"""Independent finite defect injections and exact predecessor-code comparison.

Mutations are in-memory read interception only. No repository bytes are edited.
Counts measure tested implementation defects, not mathematical completeness.
"""
import ast
import collections
import copy
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as g

started = datetime.datetime.now(datetime.timezone.utc).isoformat()
BASE = 'f5faabb43a582fec9a71c1d4a3b065efffae25bd'
PKG = ROOT / 'udt_reviewed_backlog_banking_2026-09-10'
target = ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
raw = target.read_bytes()
lines = raw.splitlines(keepends=True)
columns = lines[0].decode().rstrip('\n').split('\t')
read = Path.read_bytes
results = []

def reject(label, data, expected, path=target, sources=False):
    seen = []
    def poisoned(p):
        if p == path:
            seen.append(str(p))
            return data
        return read(p)
    with patch.object(Path, 'read_bytes', poisoned):
        try:
            g.validate_reviewed_backlog_banking(ROOT, authenticate_sources=sources)
        except SystemExit as exc:
            assert expected in str(exc), (label, str(exc))
            assert seen, label
            results.append({'defect': label, 'rejection': str(exc)})
        else:
            raise AssertionError('FALSE PASS: ' + label)

g.validate_reviewed_backlog_banking(ROOT)
for row_index in range(1, 31):
    cells = lines[row_index].decode().rstrip('\n').split('\t')
    pid = cells[0]
    for column, name in enumerate(columns):
        changed = cells.copy()
        changed[column] += ' APPENDED_UNCONDITIONAL_PHYSICAL_ADOPTION'
        mutated = lines.copy()
        mutated[row_index] = ('\t'.join(changed) + '\n').encode()
        reject(pid + ':' + name, b''.join(mutated), 'backlog exact rows/scope/order changed')

for row_index in range(31, len(lines)):
    mutated = lines.copy()
    # Last-column byte mutation, preserving the original ID and row syntax.
    mutated[row_index] = mutated[row_index].rstrip(b'\n') + b' UNAUTHORIZED_OLD_ROW_CHANGE\n'
    pid = lines[row_index].split(b'\t', 1)[0].decode()
    reject('original:' + pid, b''.join(mutated), 'backlog changed an original365 registry byte')

for pid in ('G413', 'G3830', 'G0383'):
    changed = lines[1].split(b'\t')
    changed[0] = pid.encode()
    reject('extra nonauthorized ID:' + pid, raw + b'\t'.join(changed),
           'backlog changed an original365 registry byte')
reject('header change', raw.replace(b'premise_id\t', b'premise_idx\t', 1),
       'backlog registry header changed')

scope = json.loads((PKG / 'SOURCE_MANIFEST_SCOPE.json').read_text())
entries = [line.split(maxsplit=1)[1] for line in (PKG / 'SOURCE_EVIDENCE_SHA256SUMS').read_text().splitlines()]
for package in scope['original_packages']:
    name = next(n for n in entries if n.startswith(package))
    p = ROOT / name
    reject('source package:' + package, p.read_bytes() + b'CORRUPTED',
           'backlog original source evidence changed', p, True)

old_text = subprocess.run(['git', 'show', BASE + ':verify_current_scientific_premises.py'],
                         cwd=ROOT, capture_output=True, check=True, timeout=15).stdout.decode()
new_text = (ROOT / 'verify_current_scientific_premises.py').read_text()
old_tree, new_tree = ast.parse(old_text), ast.parse(new_text)
old_funcs = {n.name: n for n in old_tree.body if isinstance(n, ast.FunctionDef)}
new_funcs = {n.name: n for n in new_tree.body if isinstance(n, ast.FunctionDef)}
assert set(new_funcs) - set(old_funcs) == {'validate_reviewed_backlog_banking'}
assert not set(old_funcs) - set(new_funcs)
def shape(n):
    return ast.dump(n, include_attributes=False)
unchanged = [name for name in old_funcs if shape(old_funcs[name]) == shape(new_funcs[name])]
assert {'_gr_filter_validated_snapshot', 'validate_gr_filter_authority',
        'registry_bytes_for_historical_banking'} <= set(unchanged)

history_funcs = ['replay_package_with_current_registry_rows_removed'] + [name for name in old_funcs
                 if name.startswith('validate_') and name.endswith('_banking')]
historical_code_exact = []
for name in history_funcs:
    source = ast.get_source_segment(new_text, new_funcs[name])
    source = source.replace('REVIEWED_BACKLOG_BANKING_IDS + ', '')
    source = source.replace(' + REVIEWED_BACKLOG_BANKING_IDS', '')
    if name == 'validate_neighboring_tidal_banking':
        added = 'rows = [row for row in read_tsv(root / "CURRENT_SCIENTIFIC_PREMISES.tsv")\n            if row["premise_id"] not in REVIEWED_BACKLOG_BANKING_IDS]'
        assert source.count(added) == 1
        source = source.replace(added, 'rows = read_tsv(root / "CURRENT_SCIENTIFIC_PREMISES.tsv")')
    assert shape(ast.parse(source).body[0]) == shape(old_funcs[name]), name
    historical_code_exact.append(name)

main_source = ast.get_source_segment(new_text, new_funcs['main'])
main_source = main_source.replace('REVIEWED_BACKLOG_PREFIXES + ', '')
main_source = main_source.replace('    validate_reviewed_backlog_banking(ROOT)\n', '')
main_source = main_source.replace('CURRENT_REGISTRY_ROW_COUNT', '365')
main_source = main_source.replace('premise registry must contain exactly 395 rows',
                                  'premise registry must contain exactly 365 rows')
main_reduced = ast.parse(main_source).body[0]
old_main = copy.deepcopy(old_funcs['main'])
# The last statement is only the expanded human-readable PASS message.
for node in (main_reduced, old_main):
    last = node.body.pop()
    assert isinstance(last, ast.Expr) and isinstance(last.value, ast.Call)
    assert isinstance(last.value.func, ast.Name) and last.value.func.id == 'print'
assert shape(main_reduced) == shape(old_main), 'Main audit changed beyond added-row compatibility/count/new guard/final print'
old_hashes = collections.Counter(n.value for n in ast.walk(old_tree)
    if isinstance(n, ast.Constant) and isinstance(n.value, str)
    and len(n.value) == 64 and set(n.value) <= set('0123456789abcdef'))
new_hashes = collections.Counter(n.value for n in ast.walk(new_tree)
    if isinstance(n, ast.Constant) and isinstance(n.value, str)
    and len(n.value) == 64 and set(n.value) <= set('0123456789abcdef'))
assert not old_hashes - new_hashes

projection = g.registry_bytes_for_historical_banking(ROOT)
delta = [(a.split(b'\t')[0].decode()) for a, b in zip(lines, projection.splitlines(keepends=True)) if a != b]
assert delta == ['G312']
assert len(lines) == len(projection.splitlines(keepends=True))
transition = g.validate_gr_filter_authority(ROOT)
old_projection = b''.join(line for line in projection.splitlines(keepends=True)
                          if not line.startswith(tuple((f'G{i}\t').encode() for i in range(383, 413))))
assert hashlib.sha256(old_projection).hexdigest() == transition['baseline_registry_sha256']

print(json.dumps({'verdict': 'PASS_FINITE_ADVERSARIAL_AND_EXACT_CODE_COMPARISON',
    'started_utc': started, 'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python': sys.version, 'argv': sys.argv, 'defects_rejected': len(results),
    'added_row_cell_mutations': 30 * len(columns), 'original_row_mutations': 365,
    'extra_id_mutations': 3, 'header_mutations': 1, 'source_package_mutations': len(scope['original_packages']),
    'unchanged_functions_exact_AST': unchanged,
    'historical_functions_exact_AST_after_only_declared30_id_projection': historical_code_exact,
    'main_exact_AST_except_declared30_id_projection_count_new_guard_and_final_print': True,
    'every_original64_hex_literal_and_multiplicity_preserved': True,
    'G312_projection_only_changed_id': delta, 'results': results}, indent=2))
