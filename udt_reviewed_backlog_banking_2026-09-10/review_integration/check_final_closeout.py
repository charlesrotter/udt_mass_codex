"""Focused acceptance status/pin comparison against authenticated full395 inputs.

No original science executes and no repository files are mutated. Exact small
text diff and machine receipt are printed for this same review context.
"""
from pathlib import Path
import ast
import csv
import datetime
import difflib
import hashlib
import io
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PKG = HERE.parent
SNAP = HERE / 'pre_closeout'
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as g

sha = lambda b: hashlib.sha256(b).hexdigest()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
input_record = json.loads((PKG / 'checks/full395_INPUTS.json').read_text())
assert input_record['files'] == json.loads((SNAP / 'SNAPSHOT_RECEIPT.json').read_text())['copied_files']
changed = {}
final_hashes = {}
diffs = []
for name, expected in input_record['files'].items():
    before = (SNAP / name).read_bytes()
    assert sha(before) == expected, name
    after = (ROOT / name).read_bytes()
    final_hashes[name] = sha(after)
    if before != after:
        changed[name] = {'before': expected, 'after': sha(after)}
        diffs.extend(difflib.unified_diff(before.decode().splitlines(), after.decode().splitlines(),
                     fromfile='full395_input/' + name, tofile='final/' + name, lineterm=''))

allowed_changed = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
    'CURRENT_SCIENTIFIC_PREMISES.md', 'INDEX.md', 'MEMORY.md', 'UDT_RESEARCH_ROADMAP.md',
    str((PKG / 'BANKING_RECORD.md').relative_to(ROOT)),
    str((PKG / 'DISPOSITIONS.tsv').relative_to(ROOT)), 'verify_current_scientific_premises.py'}
assert set(changed) <= allowed_changed, set(changed) - allowed_changed

before_tree = ast.parse((SNAP / 'verify_current_scientific_premises.py').read_text())
after_tree = ast.parse((ROOT / 'verify_current_scientific_premises.py').read_text())
pins = []
for tree in (before_tree, after_tree):
    matches = [n for n in tree.body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == 'REVIEWED_BACKLOG_PINS']
    assert len(matches) == 1
    pins.append(ast.literal_eval(matches[0].value))
    matches[0].value = ast.Constant(value='PIN_ONLY_COMPARISON_PLACEHOLDER')
assert ast.dump(before_tree, include_attributes=False) == ast.dump(after_tree, include_attributes=False)
before_pins, after_pins = pins
assert set(before_pins) <= set(after_pins)
changed_old_pins = {name for name in before_pins if before_pins[name] != after_pins[name]}
assert changed_old_pins <= {str((PKG / n).relative_to(ROOT)) for n in ('BANKING_RECORD.md', 'DISPOSITIONS.tsv')}
expected_new = {str((HERE / n).relative_to(ROOT)) for n in
                ('REVIEW_REPORT.md', 'CLAIM_FIDELITY.tsv', 'REVIEW_RECEIPT.json', 'SHA256SUMS')}
assert set(after_pins) - set(before_pins) == expected_new
for name, expected in after_pins.items():
    assert sha((ROOT / name).read_bytes()) == expected, name

before_disp = list(csv.DictReader((SNAP / PKG.name / 'DISPOSITIONS.tsv').open(), delimiter='\t'))
after_disp = list(csv.DictReader((PKG / 'DISPOSITIONS.tsv').open(), delimiter='\t'))
assert len(before_disp) == len(after_disp)
disposition_changes = []
for i, (before, after) in enumerate(zip(before_disp, after_disp)):
    delta = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
    if i < 30:
        assert before['disposition'] == 'PROPOSED_EXACT_SCOPE_ACCEPTANCE'
        assert after['disposition'] == 'BANKED_AT_EXACT_REVIEWED_SCOPE'
        assert set(delta) <= {'disposition', 'reason_or_remaining_gate'}, delta
        disposition_changes.append({'item': after['item'], 'changes': delta})
    else:
        assert not delta, (i, delta)

for line in (HERE / 'SHA256SUMS').read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    assert sha((ROOT / name).read_bytes()) == expected, name

full = json.loads((PKG / 'checks/full395.json').read_text())
completion = json.loads((PKG / 'checks/full395_COMPLETION_INPUTS.json').read_text())
assert completion['inputs'] == input_record['files']
assert completion['all17_frozen_inputs_unchanged_through_completion'] is True
assert completion['actual_capture'] == full
assert full['command'] == ['python3', 'verify_current_scientific_premises.py']
assert full['returncode'] == 0 and full['timeout'] is False
assert full['address_space_bytes'] == 2 * 1024**3 and full['cpu_seconds'] == 900
assert (PKG / 'checks/full395.stderr').read_bytes() == b''
full_out = (PKG / 'checks/full395.stdout').read_bytes()
assert b'PASS: G383--G412 reviewed backlog:27 conditional mathematical results' in full_out

g.validate_reviewed_backlog_banking(ROOT)
g.validate_startup_surface(ROOT)

print(json.dumps({'verdict': 'PASS_EXACT_STATUS_AND_PIN_ONLY_CLOSEOUT',
    'started_utc': started, 'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'runtime_model_version': 'UNATTESTED', 'same_context_followup': True,
    'python': sys.version, 'argv': sys.argv,
    'full395_attributed_parent_capture': full,
    'full395_stdout_sha256': sha(full_out),
    'full395_input_record_sha256': sha((PKG / 'checks/full395_INPUTS.json').read_bytes()),
    'unchanged_registry_claims_rows_sources_tests': True,
    'verifier_entire_AST_unchanged_except_pin_dictionary': True,
    'all_prior_pin_keys_retained': True, 'changed_existing_pins': sorted(changed_old_pins),
    'new_review_pins': sorted(expected_new), 'old_review_seal_unchanged': True,
    'changed_files': changed, 'all_final17_file_hashes': final_hashes,
    'disposition_changes': disposition_changes, 'exact_diff': '\n'.join(diffs) + '\n'}, indent=2))
