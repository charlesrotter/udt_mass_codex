"""Documentary checks only; not a mathematical or full-registry verifier."""
import csv
import hashlib
import json
import pathlib
import platform
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
REVIEW = pathlib.Path(__file__).resolve().parent
BASE = '4a699eec12b656a9487fa41f5ebad5993ef7adc5'
GIT = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1']
CURRENT = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'INDEX.md', 'MEMORY.md'}

def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT)

def digest(data):
    return hashlib.sha256(data).hexdigest()

pins = list(csv.DictReader((REVIEW / 'SOURCE_FIRST_SOURCE_PINS.tsv').open(),
                           delimiter='\t'))
pin_results = []
for row in pins:
    path = row['path']
    actual = digest((ROOT / path).read_bytes())
    same = actual == row['sha256']
    pin_results.append(dict(path=path, sha256=actual, unchanged=same,
                            current_surface=path in CURRENT))
    assert same or path in CURRENT, ('source_changed', path)

registry = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
baseline_registry = git('show', BASE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
assert registry == baseline_registry, 'registry_bytes_changed'
rows = list(csv.DictReader(registry.decode().splitlines(), delimiter='\t'))
by_id = {row['premise_id']: row for row in rows}
assert len(rows) == len(by_id) == 365, 'row_count_or_duplicate'

protected_authorities = ['CANON.md', 'AGENTS.md', 'CLAUDE.md', 'founding.md',
                        'verify_current_scientific_premises.py',
                        'UDT_METRIC_KERNEL_DEVELOPMENT.md',
                        'UDT_METRIC_KERNEL_COVERAGE.tsv']
for path in protected_authorities:
    assert (ROOT / path).read_bytes() == git('show', BASE + ':' + path), path

selected = ['G257', 'G260', 'G301', 'G310', 'G311', 'G312', 'G313',
            'G338', 'G348', 'G350', 'G351', 'G352', 'G368', 'G369',
            'G372', 'G373', 'G375', 'G382']
selected_sources = []
for key in selected:
    row = by_id[key]
    path = row['controlling_source']
    assert (ROOT / path).is_file(), ('missing_selected_source', key, path)
    selected_sources.append(dict(id=key, term=row['term'],
                                 controlling_source=path))

startup = json.loads((ROOT / 'udt_gr_filter_authority_audit_2026-09-09' /
                      'STARTUP_PREMISE_AUDIT.json').read_text())
assert startup['returncode'] == 1 and 'G325' in startup['stderr']
assert 'replay_exact:DERIVATION_RESULT.json' in startup['stderr']

print(json.dumps(dict(
    evidence_kind='DOCUMENTARY_SOURCE_CORRESPONDENCE_NOT_SCIENCE_CERTIFICATION',
    python=platform.python_version(), baseline=BASE,
    actual_head=git('rev-parse', 'HEAD').decode().strip(),
    branch=git('branch', '--show-current').decode().strip(),
    registry_rows=len(rows), registry_sha256=digest(registry),
    registry_byte_identical_to_baseline=True,
    unchanged_authorities=protected_authorities,
    tracked_changed_paths=git('diff', '--name-only', BASE).decode().splitlines(),
    source_pins=pin_results, selected_controlling_routes=selected_sources,
    reused_parent_full365='NOT_PASSED_G325; no independent rerun',
), indent=2))
