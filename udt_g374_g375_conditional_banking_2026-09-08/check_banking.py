"""Proportional banking correspondence and actual rejection paths, not proof."""
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

base = v.VACUUM_SCALE_BANKING_SNAPSHOT
owned = (pkg.name + '/', 'udt_hopfion_bridge_stability_reassessment_2026-09-08/')
allowed = {'AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
           'INDEX.md', 'MEMORY.md', 'verify_current_scientific_premises.py'}
check('grok', git('branch', '--show-current').strip() == 'grok')
check('authorized_tracked_changes', all(p in allowed or p.startswith(owned)
      for p in git('diff', base, '--name-only').splitlines()))
unrelated = sorted(line for line in git('status', '--short').splitlines()
                   if line.startswith('?? ') and not line[3:].startswith(owned))
check('46_unrelated_status_names_preserved', len(unrelated) == 46)
check('unrelated_names_hash', hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
      == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('original71_files', len(git('ls-files', v.VACUUM_SCALE_BANKING_CAMPAIGN).splitlines()) == 71)
check('original_campaign_unchanged', not git('diff', base, '--name-only',
      v.VACUUM_SCALE_BANKING_CAMPAIGN).strip())
check('canon_manuscript_unchanged', not git('diff', base, '--name-only',
      'CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv').strip())
v.validate_vacuum_scale_banking(root)
checks['authenticated_vacuum_scale_guard'] = True
v.validate_startup_surface(root)
checks['startup_surface_and_all_prior_banking_scope_guards'] = True

registry = (root / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()
record = (root / v.VACUUM_SCALE_BANKING_SOURCE).read_text()
mutants = [
    ('old_row_changed', registry.replace('G373\t', 'G373_BAD\t', 1), record,
     'changed an existing scientific registry row'),
    ('missing_new_row', '\n'.join(x for x in registry.split('\n') if not x.startswith('G375\t')), record,
     'must add exactly two distinct rows'),
    ('duplicate_new_row', registry + next(x for x in registry.splitlines() if x.startswith('G374\t')) + '\n', record,
     'must add exactly two distinct rows'),
    ('physical_grade', registry.replace(v.CONDITIONAL_BANKING_STATUS, 'PHYSICAL_SCALE_SELECTION', 1), record,
     'G375 banking grade changed'),
    ('fixed_base_omitted', registry.replace('FIXED_SUPPLIED_SMOOTH_LOCAL_4D_LORENTZ_EINSTEIN_BASE', 'UNKNOWN_BASE'), record,
     'G374 scope lacks FIXED_SUPPLIED'),
    ('pointwise_only', registry.replace('RANK_SIX_SMOOTH_CONNECTION_ALL_NEIGHBORHOOD_LOOPS', 'POINTWISE_WEYL_ONLY'), record,
     'G374 scope lacks RANK_SIX'),
    ('fixed_target_retuned', registry.replace('FIXED_TARGET_SCALAR_EXTRA_QUADRATIC_RESTRICTION', 'TARGET_ALWAYS_FREE'), record,
     'scope lacks FIXED_TARGET'),
    ('positivity_omitted', registry.replace('POSITIVE_U_MAY_REQUIRE_SHRINKING', 'ALL_GLOBAL_U'), record,
     'scope lacks POSITIVE_U'),
    ('germ_scope_erased', registry.replace('FIXED_B_VERSUS_OPEN_FLAT_PATCH_GERM_DISTINCTION', 'EVERY_GERM_SAME_DIMENSION'), record,
     'G375 scope lacks FIXED_B'),
    ('repair_erased', registry.replace('ORIGINAL_FAILURE_NORMALIZER_ONLY_REPAIR_RETAINED', 'ALL_ORIGINAL_CHECKS_PASSED'), record,
     'G375 scope lacks ORIGINAL_FAILURE'),
    ('model_upgraded', registry.replace('FRESH_SEPARATE_CONTEXT_MODEL_UNKNOWN_DIFFERENT_MODEL_UNTESTED', 'DIFFERENT_MODEL_PROVED', 1), record,
     'G375 review independence changed'),
    ('record_failure_relabelled', registry, record.replace('NOT PASS', 'PASSED'),
     'record lacks NOT PASS'),
]
caught = {}
for name, reg, rec, expected in mutants:
    with tempfile.TemporaryDirectory(prefix='udt-vs-bank-guard-') as temp:
        fixture = Path(temp)
        (fixture / 'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(reg)
        target = fixture / v.VACUUM_SCALE_BANKING_SOURCE
        target.parent.mkdir(parents=True)
        target.write_text(rec)
        try:
            v.validate_vacuum_scale_banking(fixture, authenticate_sources=False)
        except (AssertionError, RuntimeError, SystemExit) as exc:
            check('actual_expected_rejection:' + name, expected in str(exc))
            caught[name] = str(exc)
        else:
            raise AssertionError('false-pass: ' + name)
print(json.dumps(dict(kind='banking correspondence/regression NOT proof', baseline=base,
    checks=checks, actual_mutants_caught=caught, registry_rows=358,
    backup_completeness='UNVERIFIED', pre_reboot_unsaved_state='UNVERIFIED',
    host_wide_process_state='UNVERIFIED', protected_payloads='NOT_INSPECTED'), indent=2))
