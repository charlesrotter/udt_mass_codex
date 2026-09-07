"""Scoped packaging/preservation checks, not a scientific theorem verifier."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = '9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd'
GIT = ['git', '-c', 'core.preloadIndex=false']  # per-child only, no repository config change
def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT, text=True).strip()
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
    old = subprocess.check_output(GIT+['show',BASE+':'+rel],cwd=ROOT)
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
pins = {
    'step_01/CANDIDATE.md':'c5dd7945858f287845ebfbf6f38e0bdf9bc929e66463abd8b08105959a3d7ad0',
    'step_01/review/FINAL_REVIEW.md':'31c578ab9a26beb1e762c4c994c8c92291ed6300c4ae11149a737cdb63cbb11f',
    'step_02/CANDIDATE.md':'bd06415b173dc2a0b32f05f5beb6cdb0cd3ab3a0e08ad0a055bf7653f4f4c087',
    'step_02/design_checks.py':'cf836e712dc133a86560cd7d234203b2ec55c40fc5730b51a1697a1b788c0682',
    'step_02/design_inputs.json':'2d17901bfe84069ff4ac2c43eb500f0b3bd844b3136a8ba6d5582a7d710eb38c',
    'step_02/design_run.stdout':'b89c8e432788842cdbddc1270c3135043e60f12c557cb24725d2162560fdfac2',
    'step_02/review/FINAL_REVIEW.md':'1a3cb941541f8f9aea5a1edae936798e59a0b94d68d8569bb32bb9549a5052b8',
    'NEXT_WORK_ORDER.md':'f9cc992b3c99aec495a56706f379020746cc650a65e9277ed96ca7c517044e70',
}
for rel, expected in pins.items():
    assert sha(PKG/rel) == expected, rel
brief = (PKG/'DECISION_BRIEF.md').read_text()
final_header = ('Review state: CO1 and CO2 VERIFIED-WITH-CAVEATS in fresh separate contexts;\n'
                'CO1 used one preserved same-premise repair. The CO2 final review also controls\n'
                "this return packet and the proposed work order's implementation limitations.\n")
initial_header = ('Review state: CO1 reviewed with caveats after one preserved same-premise\n'
                  'repair; CO2 and this return packet pending fresh separate-context review.\n')
assert brief.count(final_header) == 1
restored = brief.replace(final_header,initial_header)
assert hashlib.sha256(restored.encode()).hexdigest() == '116d6a2158a1fb61cd93cfba8029ff78c3cf88102d20233054cae6b2082a1292'
sys.path.insert(0,str(ROOT))
import verify_current_scientific_premises as verifier
verifier.validate_startup_surface(ROOT)
subprocess.run(GIT+['diff','--check'],cwd=ROOT,check=True)

capture_records = []
for path in sorted(PKG.rglob('*.json')):
    record = json.loads(path.read_text())
    if 'command' not in record or 'returncode' not in record:
        continue
    if path.name == 'STARTUP_PREMISE_AUDIT.json':
        continue
    if path.stem == 'preservation_precheck':
        expected = 1
        assert b'unable to create threaded lstat' in path.with_suffix('.stderr').read_bytes()
    elif path.stem.endswith('_fetch'):
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
    pinned_reviewed_artifacts_unchanged=pins,decision_brief_change_status_only=True,
    full_startup_audit_record_verified_not_replayed=True,scoped_startup_surface_pass=True,
    capture_records=capture_records,
    backup_completeness='UNVERIFIED',pre_reboot_unsaved_state='UNVERIFIED',
    host_process_inventory='UNVERIFIED',scratchdisk='UNUSED; archive-dependent scope only',
    scientific_promotion=False,empirical_strain_analysis=False
),indent=2,sort_keys=True))
