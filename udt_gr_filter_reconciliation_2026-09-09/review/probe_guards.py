"""Reviewer-designed probes; production guards and author fixture are exposed.

The imported startup fixture is shared scaffolding, not an independent test
implementation. Mutation selection, verdict checks and race injection are
reviewer-written. All mutations live in TemporaryDirectory; root is unchanged.
"""
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[1]
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as guard

spec = importlib.util.spec_from_file_location('review_shared_startup_fixture',
                                            ROOT / 'tests/test_startup_surface.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
records = []

def positive(name, call):
    call()
    records.append({'name': name, 'result': 'PASS'})

def rejection(name, call, required):
    try:
        call()
    except SystemExit as e:
        message = str(e)
        result = 'REJECTED_AS_REQUIRED' if required in message else 'WRONG_REJECTION'
        records.append({'name': name, 'result': result, 'message': message,
                        'required_exception': required})
    else:
        records.append({'name': name, 'result': 'FALSE_PASS',
                        'required_exception': required})

def edit_field(raw, premise_id, field, value):
    lines = raw.decode().splitlines(keepends=True)
    col = lines[0].rstrip('\n').split('\t').index(field)
    for i, line in enumerate(lines):
        if line.startswith(premise_id + '\t'):
            cells = line.rstrip('\n').split('\t')
            cells[col] = value
            lines[i] = '\t'.join(cells) + '\n'
            break
    else:
        raise AssertionError(premise_id)
    return ''.join(lines).encode()

positive('actual_current_startup', lambda: guard.validate_startup_surface(ROOT))
baseline = subprocess.run(['git', '-c', 'core.preloadIndex=false', '-c',
    'index.threads=1', '-c', 'core.packedGitWindowSize=16m', '-c',
    'core.packedGitLimit=64m', 'show',
    'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19:CURRENT_SCIENTIFIC_PREMISES.tsv'],
    cwd=ROOT, capture_output=True, check=True, timeout=10).stdout
with tempfile.TemporaryDirectory(prefix='udt-gr-reconciliation-review-') as temporary:
    root = fixture._startup_copy(Path(temporary))
    positive('shared_fixture_current_startup', lambda: guard.validate_startup_surface(root))
    reg = root / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
    clean = reg.read_bytes()
    transition = guard.validate_gr_filter_authority(root)
    assert guard.registry_bytes_for_historical_banking(root) == baseline
    records.append({'name': 'exact_projection_to_independent_git_baseline', 'result': 'PASS'})
    for cell in transition['changed_cells']:
        reg.write_bytes(edit_field(clean, 'G312', cell['field'], cell['before']))
        rejection('old_g312_cell_' + cell['field'],
                  lambda: guard.registry_bytes_for_historical_banking(root),
                  'GR-filter current G312 row')
        reg.write_bytes(clean)
    reg.write_bytes(clean.replace(transition['after_line'].encode(),
                                 transition['before_line'].encode()))
    rejection('old_whole_g312_current', lambda: guard.validate_gr_filter_authority(root),
              'GR-filter current G312 row')
    rejection('old_whole_g312_historical', lambda: guard.registry_bytes_for_historical_banking(root),
              'GR-filter current G312 row')
    reg.write_bytes(clean + transition['after_line'].encode())
    rejection('duplicate_g312', lambda: guard.validate_gr_filter_authority(root),
              'GR-filter current G312 row')
    reg.write_bytes(clean)
    for field in ('current_status', 'epistemic_label', 'controlling_source'):
        reg.write_bytes(edit_field(clean, 'G312', field, 'CORRUPTED_SCIENCE'))
        rejection('g312_science_' + field, lambda: guard.validate_gr_filter_authority(root),
                  'GR-filter current G312 row')
        reg.write_bytes(clean)
    reg.write_bytes(edit_field(clean, 'G310', 'active_use', 'DDR_UNADOPTED'))
    rejection('ddr_authority_demotion', lambda: guard.validate_gr_filter_authority(root),
              'GR-filter retained DDR authority changed')
    reg.write_bytes(clean)
    for relative in guard.GR_FILTER_PINS:
        target = root / relative
        original = target.read_bytes()
        target.write_bytes(original + b'\nCurrent stronger GR authority restored.\n')
        rejection('pin_drift_' + relative, lambda: guard.validate_gr_filter_authority(root),
                  'GR-filter authority/source pin changed')
        target.write_bytes(original)
    validators = (
        ('validate_conditional_banking', 'G353'),
        ('validate_shared_constraint_banking', 'G357'),
        ('validate_persistence_banking', 'G361'),
        ('validate_restrictiveness_banking', 'G364'),
        ('validate_source_metric_banking', 'G367'),
        ('validate_reconstruction_banking', 'G370'),
        ('validate_coupled_banking', 'G372'),
        ('validate_vacuum_scale_banking', 'G374'),
        ('validate_berger_banking', 'G376'),
        ('validate_closed_fibre_banking', 'G379'),
        ('validate_neighboring_tidal_banking', 'G381'),
    )
    for name, added_id in validators:
        function = getattr(guard, name)
        positive('positive_' + name, lambda f=function: f(root, authenticate_sources=False))
        reg.write_bytes(edit_field(clean, 'G301', 'epistemic_label', 'UNAUTHORIZED_OLD_ROW'))
        rejection('unrelated_row_' + name, lambda f=function: f(root, authenticate_sources=False),
                  'changed an existing scientific registry row')
        reg.write_bytes(clean)
        reg.write_bytes(edit_field(clean, added_id, 'current_status', 'UNAUTHORIZED_CURRENT_GRADE'))
        rejection('live_added_row_' + name, lambda f=function: f(root, authenticate_sources=False),
                  'grade changed')
        reg.write_bytes(clean)
    surfaces = ('LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
                'CURRENT_SCIENTIFIC_PREMISES.md', 'MEMORY.md', 'INDEX.md')
    literal = "In the quiet terrestrial/solar regime, UDT must reproduce GR's local principal response and dynamics, not merely contain completed vacuum solutions that also solve GR."
    statements = (
        ('explicit_gr_authority', 'GR dynamics remains a current response-law input.'),
        ('literal_superseded_owner_premise', literal),
        ('original_adoption_shorthand', 'G312 premises are owner-adopted provisionally.'),
    )
    for surface in surfaces:
        path = root / surface
        original = path.read_bytes()
        for label, statement in statements:
            if surface in ('LIVE.md', 'HANDOFF.md'):
                changed = original.replace(b'<!-- STARTUP_CURRENT_END -->',
                    statement.encode() + b'\n<!-- STARTUP_CURRENT_END -->')
            else:
                changed = original + b'\n' + statement.encode() + b'\n'
            path.write_bytes(changed)
            rejection(surface + '_' + label, lambda: guard.validate_startup_surface(root),
                      'GR-filter current surface contradicts authority')
            path.write_bytes(original)
    original_read = Path.read_bytes
    reg_reads = [0]
    poisoned = edit_field(clean, 'G312', 'current_status', 'UNAUTHORIZED_REPLACEMENT_AFTER_CHECK')
    def alternate_read(path):
        if path == reg:
            reg_reads[0] += 1
            return clean if reg_reads[0] == 1 else poisoned
        return original_read(path)
    with patch.object(Path, 'read_bytes', alternate_read):
        try:
            projected = guard.registry_bytes_for_historical_banking(root)
        except SystemExit as e:
            records.append({'name': 'registry_read_swap_between_validation_and_projection',
                'result': 'REJECTED_AS_REQUIRED', 'message': str(e), 'reads': reg_reads[0]})
        else:
            records.append({'name': 'registry_read_swap_between_validation_and_projection',
                'result': 'FALSE_PASS' if reg_reads[0] > 1 and projected == baseline else 'PASS',
                'reads': reg_reads[0], 'poisoned_row_disappeared_into_old_valid_snapshot': projected == baseline,
                'injection': 'deterministic replacement on second read models concurrent registry write'})
    assert reg.read_bytes() == clean
failures = [r for r in records if r['result'] in ('FALSE_PASS', 'WRONG_REJECTION')]
print(json.dumps({'reviewer_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'guard_source_sha256': hashlib.sha256((ROOT / 'verify_current_scientific_premises.py').read_bytes()).hexdigest(),
    'fixture_source_sha256': hashlib.sha256((ROOT / 'tests/test_startup_surface.py').read_bytes()).hexdigest(),
    'scaffolding': 'author fixture shared; cases independently designed; production code is under test',
    'cases': len(records), 'failures': len(failures), 'results': records}, indent=2))
raise SystemExit(1 if failures else 0)
