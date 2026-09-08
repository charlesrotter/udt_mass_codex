"""Independent banking correspondence/hostile fixtures; no mathematical re-proof.

Original source files are read only. Generated temporary fixtures are private.
The validator and author checker remain shared-code regression dependencies.
"""
import hashlib
import json
import platform
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
BASE = '7e6d144a9f45fc2cee6d041448e6b6ee9e324cc3'
CAMPAIGN = 'udt_vacuum_common_scale_campaign_2026-09-08'
BANK = 'udt_g374_g375_conditional_banking_2026-09-08'
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as validator

checks, rejections, hashes = {}, {}, {}

def insist(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = True

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, timeout=10)

raw = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
old = git('show', BASE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
lines = raw.splitlines(keepends=True)
retained = b''.join(line for line in lines if not line.startswith((b'G374\t', b'G375\t')))
insist('all356_earlier_rows_literal_byte_identity', retained == old)
insist('exactly_G374_G375_added', len(lines) == len(old.splitlines()) + 2
       and sum(line.startswith(b'G374\t') for line in lines) == 1
       and sum(line.startswith(b'G375\t') for line in lines) == 1)
expected_grade = 'BANKED_DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON'
for name in ('G374', 'G375'):
    row = next(line.decode().rstrip('\n').split('\t') for line in lines if line.startswith((name+'\t').encode()))
    insist(name + '_literal_grade', row[2] == expected_grade and row[3] == 'MIXED')
    insist(name + '_whole_source_pointer', row[7] == BANK + '/BANKING_RECORD.md')
hashes['earlier356_registry_sha256'] = hashlib.sha256(retained).hexdigest()
hashes['current_registry_sha256'] = hashlib.sha256(raw).hexdigest()

paths = git('ls-tree', '-r', '--name-only', BASE, '--', CAMPAIGN).decode().splitlines()
insist('original_campaign_count71', len(paths) == 71)
for path in paths:
    payload = (ROOT / path).read_bytes()
    insist('original_blob:' + path, payload == git('show', BASE + ':' + path))
    hashes[path] = hashlib.sha256(payload).hexdigest()
for path in ('CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv'):
    insist('preserved:' + path, (ROOT / path).read_bytes() == git('show', BASE + ':' + path))

def reject(label, target_root, expected, authenticate=True):
    try:
        validator.validate_vacuum_scale_banking(target_root, authenticate_sources=authenticate)
    except (AssertionError, RuntimeError, SystemExit) as exc:
        insist('matching_rejection:' + label, expected in str(exc))
        rejections[label] = str(exc)
    else:
        raise AssertionError('REVIEW_FALSE_PASS: ' + label)

with tempfile.TemporaryDirectory(prefix='udt-vs-fidelity-fixture-') as temporary:
    fixture = Path(temporary)
    shutil.copytree(ROOT / CAMPAIGN, fixture / CAMPAIGN)
    (fixture / BANK).mkdir()
    reg_path = fixture / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
    reg_path.write_bytes(raw)
    shutil.copyfile(ROOT / BANK / 'BANKING_RECORD.md', fixture / BANK / 'BANKING_RECORD.md')
    validator.validate_vacuum_scale_banking(fixture)
    insist('fully_authenticated_unmodified_fixture', True)

    # Change actual immutable bytes, keeping manifest expectations fixed.
    for label, relative, expected in (
        ('original_candidate_corrupt', 'step_01/CANDIDATE_INITIAL.md', 'original evidence changed'),
        ('review_caveat_corrupt', 'step_02/review/REVIEW_RECORD.md', 'original evidence changed'),
        ('failed_run_corrupt', 'step_02/author_checks_initial.stderr', 'original evidence changed'),
        ('manifest_corrupt', 'EVIDENCE_SHA256SUMS', 'original manifest changed'),
        ('completion_corrupt', 'COMPLETION_RECORD.md', 'original completion changed'),
    ):
        target = fixture / CAMPAIGN / relative
        original = target.read_bytes()
        try:
            target.write_bytes(original + b'\nREVIEW_ONLY_CORRUPTION\n')
            reject(label, fixture, expected)
        finally:
            target.write_bytes(original)

    header = lines[0].decode().rstrip('\n').split('\t')
    def changed_field(identifier, field, transform):
        updated = list(lines)
        for index, line in enumerate(updated):
            if line.startswith((identifier + '\t').encode()):
                columns = line.decode().rstrip('\n').split('\t')
                field_index = header.index(field)
                before = columns[field_index]
                columns[field_index] = transform(before)
                insist('mutation_is_nonidentity:' + identifier + ':' + field, columns[field_index] != before)
                updated[index] = ('\t'.join(columns) + '\n').encode()
                return b''.join(updated)
        raise AssertionError('missing fixture row')

    for label, identifier, field, transform, expected in (
        ('wrong_source_pointer', 'G374', 'controlling_source', lambda s: s.replace('BANKING_RECORD', 'UNREVIEWED_RESULT'), 'G374 banking source changed'),
        ('unconditional_epistemic_label', 'G375', 'epistemic_label', lambda s: 'DERIVED', 'G375 banking grade changed'),
        ('provisional_authority_erased', 'G374', 'active_use', lambda s: s.replace('OWNER_PROVISIONAL_G310_G312', 'DERIVED_PHYSICAL_VACUUM_LAW'), 'scope lacks OWNER_PROVISIONAL'),
        ('contractibility_erased', 'G375', 'active_use', lambda s: s.replace('CONTRACTIBLE', 'ARBITRARY_TOPOLOGY'), 'scope lacks FIXED_CONNECTED_CONTRACTIBLE'),
        ('curved_null_scalar_erased', 'G375', 'active_use', lambda s: s.replace('NONCONSTANT_CURVED_NULL_SECTOR_BOTH_SCALARS_ZERO', 'ARBITRARY_SCALARS'), 'scope lacks NONCONSTANT_CURVED_NULL'),
        ('physical_size_closed', 'G375', 'open_scope', lambda s: s.replace('physical size', 'size selected'), 'open scope lacks physical size'),
    ):
        try:
            reg_path.write_bytes(changed_field(identifier, field, transform))
            reject(label, fixture, expected, authenticate=False)
        finally:
            reg_path.write_bytes(raw)

# An always-passing validator must cause the AUTHOR harness itself to fail.
# This executes its real mutant loop; it does not inspect a marker string.
try:
    with patch.object(validator, 'validate_vacuum_scale_banking', lambda *args, **kwargs: None):
        runpy.run_path(str(ROOT / BANK / 'check_banking.py'), run_name='__main__')
except AssertionError as exc:
    insist('author_false_pass_path_executed', str(exc) == 'false-pass: old_row_changed')
    rejections['author_always_pass_validator'] = str(exc)
else:
    raise AssertionError('author mutation harness accepted an always-pass validator')

print(json.dumps({'kind': 'proportional source correspondence and hostile guard fixtures, NOT proof',
    'python': platform.python_version(), 'baseline': BASE, 'checks': checks,
    'actual_rejections': rejections, 'sha256': hashes,
    'shared_code_limit': 'actual validator and author harness reused; reviewer-selected corruptions and byte comparisons'}, indent=2, sort_keys=True))
