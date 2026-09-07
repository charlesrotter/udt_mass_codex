"""Bounded PC1--PC3 source correspondence check; no scientific calculation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path('/home/udt-admin/udt_mass_codex')
BASE = 'c663c3ebee1755c348388170df4906eb00d1a8e8'
PKG = 'udt_phase_current_product_persistence_campaign_2026-09-07'
FORBIDDEN = ('udt_kernel_plane_global_curvature_holonomy_atlas_',
             'udt_native_onshell_timelive_reset_owner_audit_',
             'udt_pair_regime_flow_reciprocal_orchestra_amplification_',
             'udt_sne_xmax_G88_am_radial_compatibility_atlas_')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def digest(data):
    return hashlib.sha256(data).hexdigest()

manifests = [f'{PKG}/CAMPAIGN_SHA256SUMS']
for step in ('01', '02', '03'):
    manifests += [f'{PKG}/step_{step}/{name}' for name in
                  ('FREEZE_SHA256SUMS', 'SOURCE_SHA256SUMS', 'review/REVIEW_SHA256SUMS')]
records = []
for name in manifests:
    pairs = [line.split(None, 1) for line in (ROOT / name).read_text().splitlines()]
    paths = [path for expected, path in pairs]
    assert len(paths) == len(set(paths)), name
    for expected, path in pairs:
        assert not Path(path).is_absolute() and '..' not in Path(path).parts
        assert not path.startswith(FORBIDDEN), path
        if path == 'CURRENT_SCIENTIFIC_PREMISES.tsv':
            data = git('show', f'{BASE}:{path}')
            source = 'PINNED_BASELINE_GIT_BLOB_NOT_CURRENT_REGISTRY'
        else:
            data = (ROOT / path).read_bytes()
            source = 'WORKTREE_SOURCE'
        assert digest(data) == expected, (name, path)
    records.append(dict(manifest=name, sha256=digest((ROOT / name).read_bytes()),
                        entries=len(pairs), result='PASS'))
    if name.endswith('review/REVIEW_SHA256SUMS'):
        directory = (ROOT / name).parent
        actual = {str(p.relative_to(ROOT)) for p in directory.rglob('*')
                  if p.is_file() and p.name != 'REVIEW_SHA256SUMS'}
        assert actual == set(paths), (name, sorted(actual - set(paths)), sorted(set(paths) - actual))
    if name.endswith('/CAMPAIGN_SHA256SUMS'):
        actual = {str(p.relative_to(ROOT)) for p in (ROOT / PKG).rglob('*') if p.is_file()}
        assert actual == set(paths) | {name, f'{PKG}/CLOSURE_RECEIPT.json'}

commits = ['2112f80867d38e4707c5f69898bd84914754c407',
           'e4071d092b8c1b84d8732534f54d0278b226f6ba',
           '167519b259069fefb17463f2e68e030064b851da']
pins = []
for i, commit in enumerate(commits, 1):
    path = f'{PKG}/step_{i:02}/CANDIDATE_ARGUMENT.md'
    data = (ROOT / path).read_bytes()
    assert git('show', f'{commit}:{path}') == data
    assert subprocess.run(['git', 'merge-base', '--is-ancestor', commit, BASE], cwd=ROOT).returncode == 0
    pins.append(dict(commit=commit, path=path, sha256=digest(data), result='PASS'))

tracked = git('ls-files', '--', PKG).decode().splitlines()
assert tracked
changed = git('diff', '--name-only', BASE, '--', PKG).decode().splitlines()
assert not changed, changed
print(json.dumps(dict(status='PASS', python=sys.version,
    git_version=git('--version').decode().strip(), baseline=BASE,
    observed_head=git('rev-parse', 'HEAD').decode().strip(),
    branch=git('branch', '--show-current').decode().strip(),
    manifests=records, candidate_commit_pins=pins,
    tracked_campaign_files=len(tracked), campaign_diff_against_baseline=changed,
    review_membership='EXACT', campaign_membership='EXACT_241_PLUS_MANIFEST_AND_RECEIPT',
    registry_authentication='HISTORICAL_MANIFEST_HASH_CHECKED_AGAINST_PINNED_BASELINE_BLOB',
    scientific_computations='NONE', remote_freshness='NOT_CHECKED_BY_THIS_REVIEW'), indent=2))
