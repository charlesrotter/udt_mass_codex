"""Scoped packaging/preservation checks, not a scientific theorem verifier."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = '9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert git('branch','--show-current') == 'grok'
preserved = [
    'CURRENT_SCIENTIFIC_PREMISES.tsv', 'CURRENT_SCIENTIFIC_PREMISES.md',
    'CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv',
    'AGENTS.md', 'CLAUDE.md', 'verify_current_scientific_premises.py',
    'udt_observational_route_selection_campaign_2026-09-07/SOURCE_LEDGER.md',
    'udt_local_clock_metric_benchmark_campaign_2026-09-07/step_02/review/FINAL_REVIEW.md',
    'udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/EXACT_DERIVATION.md',
    'udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/AUDIT_REPORT.md',
    'startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md',
    'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md',
    'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/AUDIT_REPORT.md',
]
hashes = {}
for rel in preserved:
    old = subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT)
    actual = (ROOT/rel).read_bytes()
    assert actual == old, rel
    hashes[rel] = hashlib.sha256(actual).hexdigest()

prefix = PKG.name+'/'
lines = git('status','--short').splitlines()
unrelated = sorted(x for x in lines if x.startswith('?? ') and not x[3:].startswith(prefix))
names_hash = hashlib.sha256('\n'.join(unrelated).encode()).hexdigest()
assert len(unrelated) == 46
assert names_hash == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea'
# Status names only: never open/hash protected payload contents.
allowed_roots = {'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md'}
changed = git('diff','--name-only',BASE).splitlines()
assert all(p in allowed_roots or p.startswith(prefix) for p in changed)
assert not git('diff','--name-only',BASE,'--','udt_local_clock_metric_benchmark_campaign_2026-09-07')
audit = json.loads((PKG/'STARTUP_PREMISE_AUDIT.json').read_text())
assert audit['returncode']==0 and audit['stderr']=='' and not audit['timeout']
assert '349-row' in audit['stdout'] and 'G364/G365/G366' in audit['stdout']
assert sha(PKG/'STARTUP_PREMISE_AUDIT.json') == '31691c686f06aca6b5eafe221b4d760b5b5ff4b81a9f17b78f7e58f438cfb48c'
sys.path.insert(0,str(ROOT))
import verify_current_scientific_premises as verifier
verifier.validate_startup_surface(ROOT)
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)

capture_records = []
for path in sorted(PKG.rglob('*.json')):
    record = json.loads(path.read_text())
    if 'command' not in record or 'returncode' not in record:
        continue
    if path.name == 'STARTUP_PREMISE_AUDIT.json':
        continue
    if path.stem.endswith('_fetch'):
        expected = 22 if path.stem in {'detector_constants_fetch','detector_constants_mirror_fetch'} else 0
    else:
        expected = 0
    assert record['returncode'] == expected and not record['timeout'], str(path)
    assert path.with_suffix('.stdout').is_file() and path.with_suffix('.stderr').is_file()
    if expected==0 and not path.stem.endswith('_fetch'):
        assert path.with_suffix('.stderr').read_bytes() == b'', str(path)
    capture_records.append(dict(path=str(path.relative_to(PKG)),returncode=expected,
                                duration_seconds=record['duration_seconds']))

print(json.dumps(dict(scope='Packaging/preservation and scoped startup only, not full scientific replay',
    baseline=BASE,head=git('rev-parse','HEAD'),branch='grok',
    immutable_source_bytes_match_baseline=hashes,
    unrelated_untracked_name_count=len(unrelated),untracked_names_sha256=names_hash,
    protected_payloads_inspected=False,scoped_tracked_paths_only=True,
    full_startup_audit_record_verified_not_replayed=True,scoped_startup_surface_pass=True,
    capture_records=capture_records,
    backup_completeness='UNVERIFIED',pre_reboot_unsaved_state='UNVERIFIED',
    host_process_inventory='UNVERIFIED',scratchdisk='UNUSED; archive-dependent scope only',
    scientific_promotion=False,empirical_strain_analysis=False
),indent=2,sort_keys=True))
