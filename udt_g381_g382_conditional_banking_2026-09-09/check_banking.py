"""Exact-source NT banking correspondence and actual rejection fixtures; not proof."""
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

pkg = Path(__file__).resolve().parent
root = pkg.parent
sys.path.insert(0, str(root))
import verify_current_scientific_premises as v

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.preloadIndex=false',
        '-c', 'index.threads=1', '-c', 'core.packedGitWindowSize=16m',
        '-c', 'core.packedGitLimit=64m', *args], cwd=root, text=True)

checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    assert condition, name

base = v.NEIGHBORING_TIDAL_BANKING_SNAPSHOT
allowed = {'AGENTS.md', 'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
    'CURRENT_SCIENTIFIC_PREMISES.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
    'INDEX.md', 'MEMORY.md', 'verify_current_scientific_premises.py'}
check('grok', git('branch', '--show-current').strip() == 'grok')
check('only_authorized_changes', all(p in allowed or p.startswith(pkg.name+'/')
    for p in git('diff', base, '--name-only').splitlines()))
names = sorted(s for s in git('status', '--short').splitlines()
    if s.startswith('?? ') and not s[3:].startswith(pkg.name+'/'))
check('46_unrelated_names', len(names) == 46)
check('unrelated_name_digest', hashlib.sha256('\n'.join(names).encode()).hexdigest()
    == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
check('original_evidence_canon_manuscript_unchanged', not git('diff', base, '--name-only', '--',
    'CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv',
    'udt_neighboring_tidal_consistency_campaign_2026-09-08').strip())
v.validate_neighboring_tidal_banking(root)
checks['338_original_files_inherited_source_pins_and_363_unchanged_rows'] = True
v.validate_startup_surface(root)
checks['all_prior_banking_and_current_tracking_guards'] = True

reg = (root/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text()
record = (root/v.NEIGHBORING_TIDAL_BANKING_SOURCE).read_text()
rows = list(csv.DictReader(io.StringIO(reg), delimiter='\t'))
by_id = {r['premise_id']: r for r in rows}
mutants = []
lines = reg.splitlines(keepends=True)
new_prefixes = tuple(pid+'\t' for pid in v.NEIGHBORING_TIDAL_BANKING_IDS)
misplaced = ''.join(line for line in lines if not line.startswith(new_prefixes))
misplaced += ''.join(line for line in lines if line.startswith(new_prefixes))
mutants.append(('new_rows_misplaced_after_history', misplaced, record,
    'rows must precede historical rows in dependency order'))
def row_mutation(name, pid, field, value, reason):
    old = '\t'.join(by_id[pid].values())
    row = dict(by_id[pid]); row[field] = value
    mutants.append((name, reg.replace(old, '\t'.join(row.values()), 1), record, reason))

mutants.append(('old_row_changed', reg.replace('G380\t', 'G380_BAD\t', 1), record,
    'changed an existing scientific registry row'))
for pid in v.NEIGHBORING_TIDAL_BANKING_IDS:
    original = '\t'.join(by_id[pid].values())
    mutants.append(('missing_'+pid, reg.replace(original+'\n', '', 1), record,
        'must add exactly two distinct rows'))
    mutants.append(('duplicate_'+pid, reg+original+'\n', record,
        'must add exactly two distinct rows'))
    row_mutation('physical_grade_'+pid, pid, 'current_status', 'PHYSICAL_STABILITY',
        pid+' banking grade changed')
    row_mutation('epistemic_'+pid, pid, 'epistemic_label', 'DERIVED',
        pid+' banking grade changed')
    row_mutation('wrong_source_'+pid, pid, 'controlling_source', 'CANON.md',
        pid+' banking source changed')
    row_mutation('different_model_'+pid, pid, 'precedence_rule', 'DIFFERENT_MODEL_VERIFIED',
        pid+' review independence changed')
    for token in by_id[pid]['active_use'].split('__'):
        row_mutation('scope_'+pid+'_'+token, pid, 'active_use',
            by_id[pid]['active_use'].replace(token, 'REMOVED_SCOPE_TOKEN', 1),
            pid+' scope lacks '+token)
    row_mutation('open_limits_'+pid, pid, 'open_scope', 'PHYSICAL_IDENTIFICATION_COMPLETE',
        pid+' open scope lacks')
    row_mutation('false_pass_history_'+pid, pid, 'forbidden_regression', 'ALL_CHECKS_PASSED',
        pid+' guard lacks')
for token in ['G381 enters the accepted dependency chain before G382',
              'ALL FOUR', 'NONZERO REAL', 'RESTRICTED',
              'ALL-Lambda necessity and Lambda=0 realization',
              'TWO original PASS17 false passes', 'TWO original PASS13 false passes',
              'SIX actual failures', 'NINE actual failures',
              'LOST, not recovered', 'NOT separately',
              'No new campaign is authorized']:
    assert token in record, token
    mutants.append(('record_'+token.replace('\n', ' '), reg,
        record.replace(token, 'REMOVED_RECORD_SCOPE'), 'banking record lacks'))

caught = {}
for name, raw, text, expected in mutants:
    with tempfile.TemporaryDirectory(prefix='udt-nt-bank-guard-', dir='/tmp') as temp:
        fixture = Path(temp)
        (fixture/'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(raw)
        dest = fixture/v.NEIGHBORING_TIDAL_BANKING_SOURCE
        dest.parent.mkdir(parents=True); dest.write_text(text)
        try:
            v.validate_neighboring_tidal_banking(fixture, authenticate_sources=False)
        except (AssertionError, RuntimeError, SystemExit) as exc:
            check('expected_rejection:'+name, expected in str(exc))
            caught[name] = str(exc)
        else:
            raise AssertionError('actual false pass:'+name)

# Genuine manifest/payload corruptions in an owned temporary fixture only.
with tempfile.TemporaryDirectory(prefix='udt-nt-bank-source-', dir='/tmp') as temp:
    fixture = Path(temp)
    for relative in ['CURRENT_SCIENTIFIC_PREMISES.tsv', v.NEIGHBORING_TIDAL_BANKING_SOURCE,
                     pkg.name+'/SOURCE_EVIDENCE_SHA256SUMS']:
        dest = fixture/relative; dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root/relative, dest)
    manifest = fixture/pkg.name/'SOURCE_EVIDENCE_SHA256SUMS'
    original_manifest = manifest.read_bytes()
    manifest.write_bytes(b'bad manifest\n')
    try:
        v.validate_neighboring_tidal_banking(fixture)
    except SystemExit as exc:
        check('actual_manifest_corruption_caught', 'source manifest changed' in str(exc))
    else:
        raise AssertionError('manifest false pass')
    manifest.write_bytes(original_manifest)
    first = original_manifest.decode().splitlines()[0].split(maxsplit=1)[1]
    target = fixture/first; target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((root/first).read_bytes()+b'\nCORRUPTION\n')
    try:
        v.validate_neighboring_tidal_banking(fixture)
    except SystemExit as exc:
        check('actual_original_payload_corruption_caught', 'original evidence changed: '+first in str(exc))
    else:
        raise AssertionError('payload false pass')

print(json.dumps({'kind':'source/registry correspondence and selected actual guard rejections NOT proof',
    'snapshot':base, 'registry_rows':len(rows), 'checks':checks,
    'actual_scope_mutants_caught':caught, 'extra_manifest_payload_catches':2,
    'coverage_limit':'not exhaustive semantic or guard independence certification',
    'backup_completeness':'UNVERIFIED', 'pre_reboot_unsaved_state':'UNVERIFIED',
    'protected_payload_bytes':'NOT_INSPECTED/UNVERIFIED'}, indent=2))
