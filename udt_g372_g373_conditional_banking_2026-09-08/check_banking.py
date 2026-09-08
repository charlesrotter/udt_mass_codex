"""Scoped correspondence and actual rejection paths; not scientific proof.

Adapted from the unchanged G370/G371 checker, reusing the existing capture tool.
"""
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

baseline = v.COUPLED_BANKING_SNAPSHOT
check('branch_grok', git('branch', '--show-current').strip() == 'grok')
for guard in (v.validate_conditional_banking, v.validate_shared_constraint_banking,
              v.validate_persistence_banking, v.validate_restrictiveness_banking,
              v.validate_source_metric_banking, v.validate_reconstruction_banking,
              v.validate_coupled_banking, v.validate_startup_surface):
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
      v.COUPLED_BANKING_CAMPAIGN).strip())
check('original_campaign_has81_tracked_files', len(git('ls-files',
      v.COUPLED_BANKING_CAMPAIGN).splitlines()) == 81)
check('canon_and_fixed_manuscript_unchanged', not git('diff', baseline, '--name-only',
      'CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv').strip())
check('no_python_cache_in_banking', not list(pkg.rglob('*.pyc')))

# Temporary fixtures exercise actual guard rejection, not source corrections.
registry = (root / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()
record = (root / v.COUPLED_BANKING_SOURCE).read_text()
mutants = [
    ('old_row_changed', registry.replace('G371\t', 'G371_BAD\t', 1), record,
     'changed an existing scientific registry row'),
    ('missing_new_row', '\n'.join(line for line in registry.split('\n') if not line.startswith('G373\t')), record,
     'must add exactly two distinct rows'),
    ('duplicate_new_row', registry + next(line for line in registry.splitlines() if line.startswith('G372\t')) + '\n', record,
     'must add exactly two distinct rows'),
    ('physical_grade_substitute', registry.replace(v.CONDITIONAL_BANKING_STATUS, 'NATIVE_PHYSICAL_SOURCE_LAW', 1), record,
     'G373 banking grade changed'),
    ('analytic_called_smooth', registry.replace('REAL_ANALYTIC_SEEDS_LOCAL_REGULAR_POSITIVE_TUBE_ONLY', 'ALL_SMOOTH_SEEDS'), record,
     'G373 scope lacks REAL_ANALYTIC_SEEDS_LOCAL_REGULAR_POSITIVE_TUBE_ONLY'),
    ('vacuous_checks_counted', registry.replace('THREE_VACUOUS_AUTHOR_PRODUCT_CHECKS_EXCLUDED', 'ALL_CHECKS_SUPPORT_PROOF'), record,
     'G373 scope lacks THREE_VACUOUS_AUTHOR_PRODUCT_CHECKS_EXCLUDED'),
    ('initial_product_replaced', registry.replace('ORIGINAL_PHASE_LABEL_MEASURE_PRODUCT_MATCH_AND_PROPAGATION', 'CONSERVATION_ALONE'), record,
     'G373 scope lacks ORIGINAL_PHASE_LABEL_MEASURE_PRODUCT_MATCH_AND_PROPAGATION'),
    ('uniqueness_all_categories', registry.replace('ANALYTIC_LOCAL_GEOMETRIC_UNIQUENESS_AT_IDENTIFIED_INITIAL_DATA', 'ALL_SMOOTH_UNIQUENESS'), record,
     'G373 scope lacks ANALYTIC_LOCAL_GEOMETRIC_UNIQUENESS_AT_IDENTIFIED_INITIAL_DATA'),
    ('chart_called_law', registry.replace('B_NONZERO_SUFFICIENT_CHART_NOT_NECESSARY_LAW', 'B_NONZERO_NECESSARY_PHYSICAL_LAW'), record,
     'G372 scope lacks B_NONZERO_SUFFICIENT_CHART_NOT_NECESSARY_LAW'),
    ('other_model_claimed', registry.replace('FRESH_SEPARATE_CONTEXT_MODEL_UNKNOWN_DIFFERENT_MODEL_UNTESTED', 'INDEPENDENT_DIFFERENT_MODEL', 1), record,
     'G373 review independence changed'),
    ('record_exclusion_erased', registry, record.replace('THREE EXCLUDED', 'THREE SUPPORTING'),
     'record lacks THREE EXCLUDED'),
]
caught = {}
for name, reg, rec, expected in mutants:
    with tempfile.TemporaryDirectory(prefix='udt-cd-bank-guard-') as temp:
        fixture = Path(temp)
        (fixture / 'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(reg)
        target = fixture / v.COUPLED_BANKING_SOURCE
        target.parent.mkdir(parents=True)
        target.write_text(rec)
        try:
            v.validate_coupled_banking(fixture, authenticate_sources=False)
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
