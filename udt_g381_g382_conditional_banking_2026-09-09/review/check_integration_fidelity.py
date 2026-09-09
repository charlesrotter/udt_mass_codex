"""Run real banking guards with read-only in-memory byte mutations."""
import csv
import hashlib
import importlib.util
import io
import json
import locale
import pathlib
import sys
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKAGE = 'udt_g381_g382_conditional_banking_2026-09-09'
REGISTRY = 'CURRENT_SCIENTIFIC_PREMISES.tsv'
RECORD = PACKAGE + '/BANKING_RECORD.md'
SOURCE = 'udt_neighboring_tidal_consistency_campaign_2026-09-08/step_01/CANDIDATE_INITIAL.md'
mode = sys.argv[1]
spec = importlib.util.spec_from_file_location('current_premise_guards', ROOT / 'verify_current_scientific_premises.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

registry = (ROOT / REGISTRY).read_bytes()
rows = list(csv.DictReader(io.StringIO(registry.decode()), delimiter='\t'))
assert len(rows) == len({r['premise_id'] for r in rows}) == 365
ids = [row['premise_id'] for row in rows]
assert ids.index('G381') < ids.index('G382'), 'G381 must precede G382 in registry order'
old = b''.join(line for line in registry.splitlines(keepends=True)
               if not line.startswith((b'G381\t', b'G382\t')))
assert hashlib.sha256(old).hexdigest() == 'ae78d872143a62d6f3811d77ca909d1b90a2dee2f259b0ec862c1fd502e23afe'

changes = {
    'forget_dependency': (REGISTRY, b'REQUIRES_BANKED_G381_AND_G310', b'REQUIRES_UNBANKED_NT1_AND_G310'),
    'drop_fullslots': (REGISTRY, b'FULL_FOUR_CURVATURE_SLOT_CONNECTION_CORRECTION_NOT_RAW_SLOPES', b'RAW_COMPONENT_SLOPES_ONLY'),
    'erase_lost': (REGISTRY, b'LOST_AUTHOR_BUFFERED_INTERMEDIATES_NOT_RECOVERED', b'AUTHOR_BUFFERED_INTERMEDIATES_RECOVERED'),
    'widen_scalar': (REGISTRY, b'EVERY_CANONICAL_NULL_JET_ACTUAL_SMOOTH_LOCAL_RICCI_FLAT_REALIZATION_LAMBDA_ZERO_ONLY', b'ALL_LAMBDA_GENERAL_JET_REALIZATION'),
    'change_grade': (REGISTRY, b'G381\tneighboring_ideal_tidal_first_derivative_compatibility_and_obstruction\tBANKED_DERIVED_CONDITIONAL', b'G381\tneighboring_ideal_tidal_first_derivative_compatibility_and_obstruction\tPHYSICAL_ADOPTION'),
    'record_scalar_boundary': (RECORD, b'ALL-Lambda necessity and Lambda=0 realization are distinct scopes.', b'All Lambda realizations follow.'),
    'source_byte': (SOURCE, b'# NT1', b'# MUTATED NT1'),
    'prior_row': (REGISTRY, b'G358\teventwise_joint_timelike_null_algebraic_einstein_curvature_constraints', b'G358\tMUTATED_OLD_RESULT'),
}

original_open = pathlib.Path.open
overlay = {}
if mode != 'baseline':
    relative, original, replacement = changes[mode]
    data = (ROOT / relative).read_bytes()
    assert data.count(original) == 1, (mode, data.count(original))
    changed = data.replace(original, replacement)
    overlay[ROOT / relative] = changed
    print(json.dumps({'mode': mode, 'actual_read_mutation': relative,
                      'old': original.decode(), 'new': replacement.decode(),
                      'before_sha256': hashlib.sha256(data).hexdigest(),
                      'after_sha256': hashlib.sha256(changed).hexdigest(),
                      'writes_to_original_files': False}), flush=True)

def read_overlay(path, mode='r', *args, **kwargs):
    if path in overlay:
        assert 'r' in mode and not any(c in mode for c in 'wax+'), mode
        data = overlay[path]
        encoding = kwargs.get('encoding') or 'utf-8'
        if encoding == 'locale':
            encoding = locale.getpreferredencoding(False)
        return io.BytesIO(data) if 'b' in mode else io.StringIO(data.decode(encoding))
    return original_open(path, mode, *args, **kwargs)

with patch.object(pathlib.Path, 'open', read_overlay):
    module.validate_neighboring_tidal_banking(ROOT, authenticate_sources=True)
print(json.dumps({'status': 'PASS', 'mode': mode, 'banking_guards_executed': True,
                  'rows': len(rows), 'old_rows_byte_identity': True,
                  'evidence_type': 'banking source/integration regression, not scientific proof'}), flush=True)
if mode != 'baseline':
    raise RuntimeError('ACTUAL FALSE PASS: altered banking input was accepted')
