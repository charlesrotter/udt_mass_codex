"""Independent integration correspondence audit; no scientific theorem claims.

Only this review directory is written, and only for the immutable receipt.
Never traverses protected payloads. All manifest paths are screened first.
"""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import io
import json
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PKG = HERE.parent
BASE = 'f5faabb43a582fec9a71c1d4a3b065efffae25bd'
DENIED = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12',
)

def sha(x):
    return hashlib.sha256(x).hexdigest()

def git(*args):
    # Invocation-only setting avoids Git's lstat thread allocation under 512MiB.
    # The initial failed capture and its explicit stderr diagnostic are retained.
    p = subprocess.run(['git', '-c', 'core.preloadIndex=false', *args], cwd=ROOT,
                       capture_output=True, check=False, timeout=30)
    if p.returncode:
        sys.stdout.buffer.write(p.stdout)
        sys.stderr.buffer.write(p.stderr)
        raise RuntimeError(('git child failed', args, p.returncode))
    assert not p.stderr
    return p.stdout

def permitted(name):
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts and p.parts
    assert not any(p.parts[0] == prefix for prefix in DENIED)
    assert not (ROOT / p).is_symlink()
    return ROOT / p

receipt = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'runtime_model_version': 'UNATTESTED', 'python': sys.version,
           'platform': platform.platform(), 'first_observed_utc': '2026-09-11T00:28:33Z',
           'argv': sys.argv, 'checks': []}
assert git('branch', '--show-current').decode().strip() == 'grok'
assert git('rev-parse', 'HEAD').decode().strip() == BASE
assert git('rev-parse', 'origin/grok').decode().strip() == BASE
receipt['branch_head_origin'] = ['grok', BASE, BASE]
receipt['remote_freshness'] = 'Parent same-session fetch/pull attributed, not repeated by scoped reviewer'

freeze = json.loads((PKG / 'BANKED_CLAIMS.json').read_text())
claims = freeze['claims']
ids = [f'G{i}' for i in range(383, 413)]
assert [x['premise_id'] for x in claims] == ids
idmap = {x['id']: x['premise_id'] for x in claims}
prefixes = tuple((pid + '\t').encode() for pid in ids)
raw = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
lines = raw.splitlines(keepends=True)
baseline = git('show', BASE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
old = b''.join(line for line in lines if not line.startswith(prefixes))
assert old == baseline == (PKG / 'BASELINE_REGISTRY.tsv').read_bytes()
assert sha(old) == freeze['baseline_registry_sha256']
assert len(old.splitlines()) == 366
new = (PKG / 'BANKED_ROWS.tsv').read_bytes()
assert lines[0] + b''.join(lines[1:31]) == new
assert len(lines) == 396
rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter='\t'))
assert len({x['premise_id'] for x in rows}) == 395
by_id = {x['premise_id']: x for x in rows}
receipt['checks'].append('All original365 rows/header/order exactly equal authorized Git baseline; exact30 additions are the prefix.')

counts = collections.Counter()
artifacts = {}
transcriptions = []
accepted = set(by_id) - set(ids)
for c in claims:
    source = json.loads(permitted(c['banking_assessment_path']).read_text())['candidates']
    hits = [s for s in source if s == c['source_assessment']]
    assert len(hits) == 1, c['id']
    s = hits[0]
    assert c['statement'] == s['statement']
    assert c['assumptions'] == s['assumptions']
    assert c['exclusions'] == s.get('exclusions', s.get('excluded_inferences', []))
    assert c['history'] == s.get('history', s.get('review_and_repair_history', []))
    assert c['source_roles'] == s.get('source_roles', s.get('methods_or_controls_not_separate_physical_premises', []))
    deps = s.get('required_candidate_ids', s.get('required_candidate_dependencies', []))
    strict = [d for d in deps if ':' not in d] + s.get('required_control_candidate_ids', [])
    assert c['required_candidate_ids'] == strict
    assert c['method_or_provenance_candidate_links'] == [d for d in deps if ':' in d]
    sources = s.get('required_source_ids', s.get('required_existing_source_ids', []))
    expected = list(dict.fromkeys(sources + [idmap[d] for d in strict]))
    assert c['required_registry_ids'] == expected
    assert set(expected) <= accepted
    accepted.add(c['premise_id'])
    r = by_id[c['premise_id']]
    category = {'CO2': 'BANKED_CONDITIONAL_DESIGN_CONTROL',
                'LC2': 'BANKED_CONDITIONAL_PUBLISHED_SUMMARY_BENCHMARK',
                'FW2': 'BANKED_REVIEWED_FINITE_PROCEDURE_RESULT'}.get(c['id'], 'BANKED_DERIVED_CONDITIONAL')
    grade = category + '__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON'
    assert c['grade'] == r['current_status'] == grade
    counts[category] += 1
    assert r['epistemic_label'] == 'MIXED'
    assert c['statement'] in r['active_use']
    assert all(a in r['active_use'] for a in c['assumptions'])
    assert all(a in r['open_scope'] for a in c['exclusions'])
    for a in c['artifacts']:
        assert sha(permitted(a['path']).read_bytes()) == a['sha256'], a['path']
        artifacts[a['path']] = a['sha256']
    transcriptions.append({'id': c['id'], 'premise_id': c['premise_id'],
                           'source_assessment_exact': True, 'grade': grade,
                           'dependency_ids': expected, 'artifact_count': len(c['artifacts'])})
receipt['claim_transcriptions'] = transcriptions
receipt['category_counts'] = dict(counts)
receipt['checks'].append('All30 exact source-assessment statement, assumption, exclusion, history, role and dependency transcriptions authenticated; source artifacts authenticated.')

entries = {}
manifest = PKG / 'SOURCE_EVIDENCE_SHA256SUMS'
for line in manifest.read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    assert len(expected) == 64 and set(expected) <= set('0123456789abcdef')
    permitted(name)
    assert name not in entries
    entries[name] = expected
assert len(entries) == 2612
for name, expected in entries.items():
    assert sha(permitted(name).read_bytes()) == expected, name
assert all(entries.get(name) == expected for name, expected in artifacts.items())
scope = json.loads((PKG / 'SOURCE_MANIFEST_SCOPE.json').read_text())
originals = []
for package in scope['original_packages']:
    permitted(package)
    originals.extend(git('ls-files', '-z', '--', package).decode().split('\0')[:-1])
assert len(originals) == len(set(originals)) == 2152
assert set(originals) <= set(entries)
assert git('diff', BASE, '--', *scope['original_packages']) == b''
receipt['authenticated_source_file_count'] = len(entries)
receipt['original_tracked_files_unchanged'] = len(originals)
receipt['checks'].append('All2612 explicitly permitted manifest files authenticated; all2152 complete scoped original tracked files covered and unchanged against baseline Git.')

prebank = json.loads((PKG / 'checks/prebank_365.json').read_text())
assert prebank['returncode'] == 0 and prebank['timeout'] is False
assert prebank['command'] == ['python3', 'verify_current_scientific_premises.py']
assert (PKG / 'checks/prebank_365.stderr').read_bytes() == b''
assert b'PASS:' in (PKG / 'checks/prebank_365.stdout').read_bytes()
receipt['parent_prebank_audit_authenticated_not_rerun'] = prebank
status = git('status', '--porcelain=v1', '-unormal').decode()
original_untracked = [line for line in status.splitlines() if line.startswith('?? ')
    and not line[3:].startswith('udt_reviewed_backlog_banking_2026-09-10/')
    and line[3:] != 'tests/test_reviewed_backlog_banking.py']
fingerprint = sha(('\n'.join(original_untracked) + '\n').encode())
receipt['original_untracked_name_status_count'] = len(original_untracked)
receipt['original_untracked_name_status_sha256'] = fingerprint
assert len(original_untracked) == 46
assert fingerprint == '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
receipt['checks'].append('Original46 name/status fingerprint matches; this does not inspect or certify protected payloads/backups.')

targets = list(git('diff', '--name-only').decode().splitlines())
targets += [str((PKG / n).relative_to(ROOT)) for n in
            ('BANKING_RECORD.md', 'BANKED_CLAIMS.json', 'BANKED_ROWS.tsv', 'DISPOSITIONS.tsv',
             'SOURCE_EVIDENCE_SHA256SUMS', 'SOURCE_MANIFEST_SCOPE.json', 'WORK_ORDER.md')]
targets += ['tests/test_reviewed_backlog_banking.py']
receipt['integration_snapshot_sha256'] = {name: sha(permitted(name).read_bytes()) for name in targets}
receipt['completed_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt['verdict'] = 'PASS_INTEGRITY_CORRESPONDENCE_ONLY'
print(json.dumps(receipt, indent=2))
