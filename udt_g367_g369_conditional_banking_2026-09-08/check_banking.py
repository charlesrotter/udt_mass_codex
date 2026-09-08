"""Scoped banking correspondence and actual negative guard controls, not proof."""
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
pkg = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
import verify_current_scientific_premises as v

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.preloadIndex=false',
        '-c', 'index.threads=1', *args], cwd=root, text=True)

checks = {}
def check(name, value):
    checks[name] = bool(value)
    assert value, name

baseline = v.SOURCE_METRIC_BANKING_SNAPSHOT
check('branch_grok', git('branch', '--show-current').strip() == 'grok')
v.validate_conditional_banking(root)
v.validate_shared_constraint_banking(root)
v.validate_persistence_banking(root)
v.validate_restrictiveness_banking(root)
v.validate_source_metric_banking(root)
v.validate_startup_surface(root)
checks['all_five_banking_guards_and_current_startup'] = True
allowed = {'AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
           'INDEX.md', 'MEMORY.md', 'verify_current_scientific_premises.py'}
owned = (pkg.name + '/', 'udt_metric_source_reconstructibility_campaign_2026-09-08/')
changes = git('diff', baseline, '--name-only').splitlines()
check('only_authorized_tracked_changes', all(p in allowed or p.startswith(owned) for p in changes))
status = git('status', '--short').splitlines()
unrelated = sorted(line for line in status if line.startswith('?? ') and not line[3:].startswith(owned))
check('unrelated_46_names_preserved', len(unrelated) == 46)
check('unrelated_names_hash', hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
      == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('original_campaign_unchanged', not git('diff', baseline, '--name-only',
      v.SOURCE_METRIC_BANKING_CAMPAIGN).strip())
check('canon_and_fixed_manuscript_unchanged', not git('diff', baseline, '--name-only',
      'CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv').strip())

# Real mutations of isolated temporary fixtures exercise the new scope guard.
# No source or worktree payload is modified. These are implementation controls.
registry = (root / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()
record = (root / v.SOURCE_METRIC_BANKING_SOURCE).read_text()
mutants = [
 ('old_row_change', registry.replace('G366\t', 'G366_BAD\t', 1), record,
  'changed an existing scientific registry row'),
 ('missing_new_row', '\n'.join(line for line in registry.split('\n') if not line.startswith('G369\t')), record,
  'must add exactly three distinct rows'),
 ('duplicate_new_row', registry + next(line for line in registry.splitlines() if line.startswith('G367\t')) + '\n', record,
  'must add exactly three distinct rows'),
 ('optional_scope_removed', registry.replace('OPTIONAL_ALGEBRAIC_LORENTZ_NATURAL_CLASS_ONLY', 'NATIVE_UNRESTRICTED_CLASS'), record,
  'G368 scope lacks'),
 ('review_exposure_erased', registry, record.replace('NOT wholly target-outline-blind', 'fully blind'),
  'record lacks NOT wholly target-outline-blind'),
 ('native_grade_mutation', registry.replace(v.CONDITIONAL_BANKING_STATUS, 'NATIVE_PHYSICAL_LAW', 1), record,
  'G369 banking grade changed'),
]
caught = {}
for name, reg, rec, expected in mutants:
    with tempfile.TemporaryDirectory(prefix='udt-sm-bank-guard-') as temp:
        fixture = Path(temp)
        (fixture / 'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(reg)
        target = fixture / v.SOURCE_METRIC_BANKING_SOURCE
        target.parent.mkdir(parents=True)
        target.write_text(rec)
        try:
            v.validate_source_metric_banking(fixture, authenticate_sources=False)
        except (AssertionError, RuntimeError, SystemExit) as exc:
            check('mutant_expected_reason:' + name, expected in str(exc))
            caught[name] = str(exc)
        else:
            raise AssertionError('false-pass mutant: ' + name)
print(json.dumps({'kind': 'banking correspondence/regression, not scientific proof',
    'baseline': baseline, 'head': git('rev-parse', 'HEAD').strip(),
    'checks': checks, 'actual_mutants_caught': caught,
    'registry_rows': len(v.read_tsv(root / 'CURRENT_SCIENTIFIC_PREMISES.tsv')),
    'backup_completeness': 'UNVERIFIED', 'pre_reboot_unsaved_state': 'UNVERIFIED',
    'host_wide_process_state': 'UNVERIFIED', 'protected_payloads': 'NOT_INSPECTED'},
    indent=2, sort_keys=True))
