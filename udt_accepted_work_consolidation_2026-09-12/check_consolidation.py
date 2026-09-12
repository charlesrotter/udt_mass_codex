"""Check documentary correspondence. PASS does not certify scientific claims."""
from pathlib import Path
import copy
import csv
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
EXPECTED_DIRT = '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
DENY = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
    'archive/', '8_25/',
)

def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def require(test, message):
    if not test:
        raise ValueError(message)

def check_rows(coverage, original, families):
    require(len(coverage) == len(original) == 397, 'registry row count')
    by_id = {r['premise_id']: r for r in original}
    ids = [r['premise_id'] for r in coverage]
    require(len(set(ids)) == 397 and set(ids) == set(by_id), 'registry identity')
    pairs = [('term','term'), ('epistemic_label_exact','epistemic_label'),
             ('active_use_exact','active_use'), ('controlling_source_exact','controlling_source')]
    for r in coverage:
        for left, right in pairs:
            require(r[left] == by_id[r['premise_id']][right], f'exact registry field {r["premise_id"]}:{left}')
        require(r['inspection_disposition'] and 'PENDING' not in r['inspection_disposition'], 'missing inspection disposition')
    require(len(families) == 22 and len({r['family_id'] for r in families}) == 22, 'family identities')
    seen = []
    for f in families:
        members = f['premise_ids'].split(';')
        require(int(f['count']) == len(members), 'family count')
        actual = [r['premise_id'] for r in coverage if r['family_id'] == f['family_id']]
        require(set(actual) == set(members) and len(actual) == len(members), 'family membership')
        seen.extend(members)
    require(len(seen) == 397 and set(seen) == set(ids), 'family census')

def check_safe_path(p):
    require(not Path(p).is_absolute() and '..' not in Path(p).parts and not p.startswith(DENY), 'excluded source path')

coverage = rows(PKG / 'REGISTRY_COVERAGE.tsv')
original = rows(ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv')
families = rows(PKG / 'FAMILY_MAP.tsv')
check_rows(coverage, original, families)

# Independent source-registry equality is the positive check; these mutants
# establish that the metadata checks actually reject the named documentary defects.
catches = []
for name in ['dropped_row', 'duplicate_id', 'changed_grade', 'wrong_family_member', 'pending_disposition']:
    c, f = copy.deepcopy(coverage), copy.deepcopy(families)
    if name == 'dropped_row': c.pop()
    if name == 'duplicate_id': c[0]['premise_id'] = c[1]['premise_id']
    if name == 'changed_grade': c[0]['epistemic_label_exact'] = 'UNAUTHORIZED_UPGRADE'
    if name == 'wrong_family_member': f[0]['premise_ids'] += ';G414'
    if name == 'pending_disposition': c[0]['inspection_disposition'] = 'PENDING'
    try:
        check_rows(c, original, f)
    except ValueError:
        catches.append(name)
    else:
        raise ValueError(f'uncaught metadata mutant: {name}')
try:
    check_safe_path(DENY[0] + 'do_not_open')
except ValueError:
    catches.append('protected_path_rejected_before_read')
else:
    raise ValueError('protected path guard failed')

pins = json.loads((PKG / 'SOURCE_PINS.json').read_text())
ledger = rows(PKG / 'SOURCE_READ_LEDGER.tsv')
require({r['path']: r['sha256'] for r in ledger} == pins['files'], 'source ledger/pin mismatch')
for p, sha in pins['files'].items():
    check_safe_path(p)
    require(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == sha, f'source byte mismatch: {p}')
    baseline = subprocess.check_output(['git','show',f'{pins["baseline"]}:{p}'], cwd=ROOT)
    require(hashlib.sha256(baseline).hexdigest() == sha, f'baseline mismatch: {p}')

account = (ROOT / 'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md').read_text()
links = set(re.findall(r'\]\(([^)]+)\)', account))
for p in links:
    check_safe_path(p)
    require((ROOT / p).is_file(), f'account link missing: {p}')
    if not p.startswith(PKG.name + '/') and p != 'UDT_RESEARCH_ROADMAP.md':
        require(p in pins['files'], f'linked original source not pinned: {p}')
gaps = rows(PKG / 'GAP_AND_REUSE_MAP.tsv')
require(len(gaps) == 13 and len({r['job_id'] for r in gaps}) == 13, 'gap identities')
require(all(all(r.values()) for r in gaps), 'empty gap field')

freeze = PKG / 'INITIAL_FREEZE.json'
if freeze.exists():
    for entry in json.loads(freeze.read_text())['files']:
        require(hashlib.sha256((PKG / entry['snapshot']).read_bytes()).hexdigest() == entry['sha256'], 'initial snapshot changed')

status = subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'], cwd=ROOT, text=True)
task_owned = (PKG.name + '/', 'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md')
unrelated = [s for s in status.splitlines() if s.startswith('?? ') and not s[3:].startswith(task_owned)]
fingerprint = hashlib.sha256(('\n'.join(unrelated)+'\n').encode()).hexdigest()
require(len(unrelated) == 46 and fingerprint == EXPECTED_DIRT, 'original untracked names/status changed')
require(subprocess.check_output(['git','branch','--show-current'], cwd=ROOT, text=True).strip() == 'grok', 'branch changed')
print(json.dumps(dict(result='PASS', meaning='documentary correspondence only', registry_rows=397,
    families=22, gap_jobs=13, pinned_sources=len(pins['files']), valid_account_links=len(links),
    rejected_metadata_mutants=catches, preserved_untracked_entries=len(unrelated),
    preserved_untracked_sha256=fingerprint, initial_snapshot_checked=freeze.exists()), indent=2))
