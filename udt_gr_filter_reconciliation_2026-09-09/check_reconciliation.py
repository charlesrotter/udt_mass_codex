"""Bounded authority/preservation checks, not scientific proof or full365 waiver."""
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as guard

BASE = 'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19'
GIT = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1']
ALLOWED = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'MEMORY.md', 'INDEX.md',
           'CURRENT_SCIENTIFIC_PREMISES.tsv', 'verify_current_scientific_premises.py',
           'tests/test_startup_surface.py'}
checks = []

def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

transition = guard.validate_gr_filter_authority(ROOT)
before = git('show', BASE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
current = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
check('baseline_registry_pin', sha(before) == transition['baseline_registry_sha256'])
check('projection_exact_baseline_not_current',
      guard.registry_bytes_for_historical_banking(ROOT) == before != current)
old_rows = list(csv.DictReader(io.StringIO(before.decode()), delimiter='\t'))
new_rows = guard.read_tsv(ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv')
check('schema_order_and_365_rows', before.splitlines()[0] == current.splitlines()[0]
      and len(old_rows) == len(new_rows) == 365
      and [row['premise_id'] for row in old_rows] == [row['premise_id'] for row in new_rows])
cells = [dict(premise_id=a['premise_id'], field=field, before=a[field], after=b[field])
         for a, b in zip(old_rows, new_rows) for field in a if a[field] != b[field]]
check('exact_five_cell_transition', cells == transition['changed_cells'] and len(cells) == 5)
check('epistemic_labels_and_scientific_source_pointers_preserved',
      all(a['epistemic_label'] == b['epistemic_label']
          and a['controlling_source'] == b['controlling_source']
          for a, b in zip(old_rows, new_rows)))
old_g312 = next(row for row in old_rows if row['premise_id'] == 'G312')['current_status']
new_g312 = next(row for row in new_rows if row['premise_id'] == 'G312')['current_status']
check('g312_mathematical_stamp_prefix_preserved',
      old_g312.split('__OWNER_ADOPTED_PROVISIONAL_POSTULATES_AUTHORIZED')[0]
      == new_g312.split('__HISTORICAL_TWO_PREMISE_ADOPTION')[0])
check('g312_review_counts_exclusions_suffix_preserved',
      old_g312.split('__4690_PRODUCTION_CHECKS')[1]
      == new_g312.split('__4690_PRODUCTION_CHECKS')[1])

for name in ('conditional', 'shared_constraint', 'persistence', 'restrictiveness',
             'source_metric', 'reconstruction', 'coupled', 'vacuum_scale', 'berger',
             'closed_fibre', 'neighboring_tidal'):
    getattr(guard, 'validate_' + name + '_banking')(ROOT)
    check('actual_current_scopes_and_historical_sources:' + name, True)
guard.validate_startup_surface(ROOT)
check('actual_current_startup_surface', True)

# This is the exact G351 replay block from the ACTUAL current main(), executed
# separately because G325 stops full main earlier. No edited or skipped main.
# All loaded AST nodes retain their current source lines and globals.
tree = ast.parse((ROOT / 'verify_current_scientific_premises.py').read_text())
main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
blocks = [node for node in main.body if isinstance(node, ast.With)
          and 'g351_current_replay_' in ast.get_source_segment(
              (ROOT / 'verify_current_scientific_premises.py').read_text(), node)]
check('exactly_one_actual_g351_replay_block', len(blocks) == 1)
namespace = dict(vars(guard))
namespace['g351'] = ROOT / 'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05'
exec(compile(ast.Module(body=blocks, type_ignores=[]), str(ROOT / 'verify_current_scientific_premises.py'),
             'exec'), namespace)
check('actual_g351_historical_no_write_replay_47_checks', True)

# The prior audit is fixed history. Its six old current-page pins are checked
# at the named baseline; every other manifest file is checked live AND baseline.
audit = ROOT / 'udt_gr_filter_authority_audit_2026-09-09'
entries = (audit / 'EVIDENCE_SHA256SUMS').read_text().splitlines()
check('entire_prior_audit_83_pin_inventory', len(entries) == 83)
for line in entries:
    expected, relative = line.split(maxsplit=1)
    check('prior_audit_baseline_pin:' + relative, sha(git('show', BASE + ':' + relative)) == expected)
    if relative not in ALLOWED:
        check('prior_audit_live_preserved:' + relative, sha((ROOT / relative).read_bytes()) == expected)

for relative in ('CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md',
                 'UDT_METRIC_KERNEL_COVERAGE.tsv', 'AGENTS.md', 'CLAUDE.md'):
    check('preserved_control_or_fixed_science:' + relative,
          (ROOT / relative).read_bytes() == git('show', BASE + ':' + relative))
changed = git('diff', '--name-only', BASE, '--').decode().splitlines()
check('tracked_write_scope_before_or_after_publication',
      all(name in ALLOWED or name.startswith(HERE.name + '/') for name in changed))
status = git('status', '--short', '--untracked-files=normal').decode().splitlines()
unrelated = sorted(line for line in status if line.startswith('?? ')
                   and not line[3:].startswith(HERE.name + '/'))
check('unrelated_46_status_names_only_preserved', len(unrelated) == 46 and
      sha('\n'.join(unrelated).encode()) == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
print(json.dumps(dict(status='PASS_BOUNDED_CORRESPONDENCE_NOT_FULL365', checks=checks,
                     count=len(checks), python=sys.version, baseline=BASE,
                     g351_replay=dict(command=namespace['g351_replay'].args,
                                      returncode=namespace['g351_replay'].returncode,
                                      stdout=namespace['g351_replay'].stdout,
                                      stderr=namespace['g351_replay'].stderr,
                                      evidence_before=namespace['g351_before'],
                                      evidence_after=namespace['g351_after']),
                     omitted='No new science proof, full dependency closure, protected payload, '
                     'backup, archive, GPU or observational audit; G325 NOT_PASSED remains.'), indent=2))
