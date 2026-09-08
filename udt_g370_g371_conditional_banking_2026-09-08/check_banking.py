"""Additive banking/preservation guards and actual mutants, not scientific proof."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

pkg = Path(__file__).resolve().parent
root = pkg.parent
sys.path.insert(0, str(root))
import verify_current_scientific_premises as v

checks = {}
def check(name, value):
    checks[name] = bool(value)
    assert value, name

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.preloadIndex=false',
        '-c', 'index.threads=1', *args], cwd=root, text=True)

baseline = v.RECONSTRUCTION_BANKING_SNAPSHOT
check('branch_grok', git('branch', '--show-current').strip() == 'grok')
for guard in (v.validate_conditional_banking, v.validate_shared_constraint_banking,
              v.validate_persistence_banking, v.validate_restrictiveness_banking,
              v.validate_source_metric_banking, v.validate_reconstruction_banking,
              v.validate_startup_surface):
    guard(root)
    checks[guard.__name__] = True

allowed = {'AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
           'INDEX.md', 'MEMORY.md', 'verify_current_scientific_premises.py'}
owned = pkg.name + '/'
changes = git('diff', baseline, '--name-only').splitlines()
check('only_authorized_tracked_changes', all(p in allowed or p.startswith(owned) for p in changes))
unrelated = sorted(line for line in git('status', '--short').splitlines()
                   if line.startswith('?? ') and not line[3:].startswith(owned))
check('unrelated_46_names_preserved', len(unrelated) == 46)
check('unrelated_names_hash', hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
      == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('original_campaign_unchanged', not git('diff', baseline, '--name-only',
      v.RECONSTRUCTION_BANKING_CAMPAIGN).strip())
check('canon_and_fixed_manuscript_unchanged', not git('diff', baseline, '--name-only',
      'CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv').strip())
check('original_campaign_has71_tracked_files', len(git('ls-files',
      v.RECONSTRUCTION_BANKING_CAMPAIGN).splitlines()) == 71)
campaign = root / v.RECONSTRUCTION_BANKING_CAMPAIGN
failed = campaign / 'step_02/review/independent_product_check_initial_failed.py'
corrected = campaign / 'step_02/review/independent_product_check.py'
check('syntax_only_correction_preserved', failed.read_text().replace(
      '.subs(u:s.Rational(1,4))', '.subs(u,s.Rational(1,4))', 1) == corrected.read_text())
receipt = json.loads((campaign / 'step_02/review/independent_initial.json').read_text())
check('failed_reviewer_run_remains_failed', receipt['returncode'] == 1 and
      'SyntaxError' in (campaign / 'step_02/review/independent_initial.stderr').read_text())
check('no_python_cache_in_banking', not list(pkg.rglob('*.pyc')))

# Isolated temporary fixtures, not modifications of any source/worktree payload.
# These test implementation rejection paths; separate review owns scope fidelity.
registry = (root / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()
record = (root / v.RECONSTRUCTION_BANKING_SOURCE).read_text()
mutants = [
    ('old_row_changed', registry.replace('G369\t', 'G369_BAD\t', 1), record,
     'changed an existing scientific registry row'),
    ('missing_new_row', '\n'.join(line for line in registry.split('\n') if not line.startswith('G371\t')), record,
     'must add exactly two distinct rows'),
    ('duplicate_new_row', registry + next(line for line in registry.splitlines() if line.startswith('G370\t')) + '\n', record,
     'must add exactly two distinct rows'),
    ('physical_grade_substitute', registry.replace(v.CONDITIONAL_BANKING_STATUS, 'NATIVE_PHYSICAL_SOURCE_LAW', 1), record,
     'G371 banking grade changed'),
    ('ambient_replaced_by_cut', registry.replace('FULL_AMBIENT_NEIGHBORHOOD_COVECTOR_CLOSURE', 'NULL_CUT_PULLBACK_ONLY'), record,
     'G371 scope lacks FULL_AMBIENT_NEIGHBORHOOD_COVECTOR_CLOSURE'),
    ('data_variation_called_gauge', registry.replace('FREE_CROSS_PHASE_LABELS_LOCAL_PRODUCT_NOT_PASSIVE_GAUGE', 'ALL_LABEL_CHANGES_PASSIVE_GAUGE'), record,
     'G371 scope lacks FREE_CROSS_PHASE_LABELS_LOCAL_PRODUCT_NOT_PASSIVE_GAUGE'),
    ('minimality_limit_erased', registry.replace('LIST_NOT_MINIMAL_OR_PROVED_INDEPENDENT', 'PROVED_MINIMAL_INDEPENDENT_LIST'), record,
     'G370 scope lacks LIST_NOT_MINIMAL_OR_PROVED_INDEPENDENT'),
    ('post_exposure_called_blind', registry, record.replace('NOT retrospectively blind', 'retrospectively blind'),
     'record lacks NOT retrospectively blind'),
]
caught = {}
for name, reg, rec, expected in mutants:
    with tempfile.TemporaryDirectory(prefix='udt-rt-bank-guard-') as temp:
        fixture = Path(temp)
        (fixture / 'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(reg)
        target = fixture / v.RECONSTRUCTION_BANKING_SOURCE
        target.parent.mkdir(parents=True)
        target.write_text(rec)
        try:
            v.validate_reconstruction_banking(fixture, authenticate_sources=False)
        except (AssertionError, RuntimeError, SystemExit) as exc:
            check('mutant_expected_reason:' + name, expected in str(exc))
            caught[name] = str(exc)
        else:
            raise AssertionError('false-pass mutant: ' + name)

print(json.dumps({'kind': 'banking correspondence/regression, NOT scientific proof',
    'baseline': baseline, 'head': git('rev-parse', 'HEAD').strip(),
    'checks': checks, 'actual_mutants_caught': caught,
    'registry_rows': len(v.read_tsv(root / 'CURRENT_SCIENTIFIC_PREMISES.tsv')),
    'backup_completeness': 'UNVERIFIED', 'pre_reboot_unsaved_state': 'UNVERIFIED',
    'host_wide_process_state': 'UNVERIFIED', 'protected_payloads': 'NOT_INSPECTED'},
    indent=2, sort_keys=True))
