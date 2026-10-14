"""Read-only FKA1 correspondence check; writes only this review's result JSON."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path('udt_foundation_kernel_audit_2026-10-13')
REVIEW = PACKAGE / 'review/math'
FREEZE = PACKAGE / 'INTEGRATION_FREEZE.json'
PROTECTED = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12',
)


def sha(path):
    h = hashlib.sha256()
    with (ROOT / path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def screened(path):
    p = Path(path)
    if p.is_absolute() or '..' in p.parts:
        return False
    try:
        resolved = (ROOT / p).resolve().relative_to(ROOT)
    except ValueError:
        return False
    for candidate in (p.as_posix(), resolved.as_posix()):
        if any(candidate == q or candidate.startswith(q + '/') for q in PROTECTED):
            return False
    return True


start = time.monotonic()
freeze = json.loads((ROOT / FREEZE).read_text())
accepted = freeze['accepted_sha256']
# Screen every accepted path before reading any accepted payload.
rejected = [p for p in accepted if not screened(p)]
assert not rejected, rejected
symlinks = [p for p in accepted if (ROOT / p).is_symlink()]
assert not symlinks, symlinks
prior_path = freeze['prior_review_record']
assert screened(prior_path)
prior = json.loads((ROOT / prior_path).read_text())
old = prior['accepted_sha256']
baseline = json.loads((ROOT / PACKAGE / 'BASELINE.json').read_text())
actual = {p: sha(p) for p in accepted}
mismatches = [p for p in accepted if actual[p] != accepted[p]]
changed = {p for p in old.keys() & accepted.keys() if old[p] != accepted[p]}
added = set(accepted) - set(old)
removed = set(old) - set(accepted)
binding_checks = {
    p: {'old_matches': record['old'] == old.get(p),
        'new_matches': record['new'] == accepted.get(p)}
    for p, record in freeze['changed_prior_files'].items()
}
status = git('status', '--porcelain=v1', '-z', '--untracked-files=all').decode().split('\0')
tracked = sorted(row[3:] for row in status if row and not row.startswith('?? '))
untracked = sorted(row[3:] for row in status if row.startswith('?? '))
unrelated = sorted(p for p in untracked if not p.startswith(PACKAGE.as_posix() + '/'))
old_unrelated = sorted(baseline['unrelated_untracked_names'])
original_freezes = [
    'SCIENCE_FREEZE.json',
    'explorer_a/INITIAL_FREEZE.json',
    'explorer_b/INITIAL_FREEZE.json',
    'explorer_b/CANDIDATE_FREEZE.json',
    'explorer_a/CLOCK_MAP_CROSS_CHECK_FREEZE.json',
    'STARTING_SOURCE_PINS.json',
    'ADDENDUM_SOURCE_PINS.json',
    'COMPARISON_SOURCE_PINS.json',
]
original_checks = []
for name in original_freezes:
    source = json.loads((ROOT / PACKAGE / name).read_text())
    for raw, expected in source['sha256'].items():
        candidates = [Path(raw), PACKAGE / Path(name).parent / raw, PACKAGE / raw]
        path = next(str(candidate) for candidate in candidates
                    if screened(str(candidate)) and (ROOT / candidate).is_file())
        assert screened(path), path
        source_hash = (hashlib.sha256(git('show', freeze['baseline_head'] + ':' + path)).hexdigest()
                       if name == 'COMPARISON_SOURCE_PINS.json' and path == 'UDT_DEVELOPMENT.md'
                       else sha(path))
        original_checks.append({'manifest': name, 'path': path,
                                'version': (freeze['baseline_head'] if name == 'COMPARISON_SOURCE_PINS.json' and path == 'UDT_DEVELOPMENT.md' else 'working file'),
                                'matches': source_hash == expected})
initial_dir = PACKAGE / 'initial_integration'
initial_freeze_path = initial_dir / 'INTEGRATION_FREEZE.json'
initial_freeze_hash_matches = sha(initial_freeze_path) == 'babd81f470a5aea044e9b34d2c0e0d1d06c1cb242cb57ad700ae6201ccfd31e3'
initial_freeze = json.loads((ROOT / initial_freeze_path).read_text())
initial_snapshots = []
for path in sorted((ROOT / initial_dir).rglob('*')):
    if not path.is_file() or path.name == 'INTEGRATION_FREEZE.json':
        continue
    relative = path.relative_to(ROOT / initial_dir).as_posix()
    source = relative if relative in initial_freeze['accepted_sha256'] else str(PACKAGE / relative)
    assert screened(path.relative_to(ROOT).as_posix())
    initial_snapshots.append({'snapshot': path.relative_to(ROOT).as_posix(),
                             'original_path': source,
                             'matches': sha(path.relative_to(ROOT)) == initial_freeze['accepted_sha256'][source]})
initial_binding_hash_matches = sha(REVIEW / 'INITIAL_FINAL_BINDING_CHECK.json') == 'bc71b28396b1df885e44a4d6ee2bc2e496fd804832c2f6cbdc34adac68e4282c'
head_prior_checks = {p: hashlib.sha256(git('show', 'HEAD:' + p)).hexdigest() == old[p]
                     for p in changed}
head = git('rev-parse', 'HEAD').decode().strip()
branch = git('branch', '--show-current').decode().strip()
result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer': '/root/fka_review_math',
    'freeze_path': str(FREEZE), 'freeze_sha256': sha(FREEZE),
    'prior_record_path': prior_path, 'prior_record_sha256': sha(prior_path),
    'prior_record_hash_matches': sha(prior_path) == freeze['prior_review_record_sha256'],
    'accepted_count': len(accepted), 'all_accepted_hashes_match': not mismatches,
    'mismatches': mismatches,
    'protected_prefixes_screened_before_reads': list(PROTECTED),
    'protected_accepted_paths': rejected, 'symlink_paths': symlinks,
    'total_hashed_bytes': sum((ROOT / p).stat().st_size for p in accepted),
    'prior_accepted_count': len(old), 'changed_prior_count': len(changed),
    'changed_prior_exact': changed == set(freeze['changed_prior_files']),
    'changed_prior_binding_checks': binding_checks,
    'added_count': len(added), 'added_exact_new_files': added == set(freeze['new_files']),
    'removed_prior_paths': sorted(removed),
    'unchanged_prior_count': len(set(old) & set(accepted)) - len(changed),
    'head': head, 'branch': branch,
    'head_matches_baseline': head == baseline['head'] == freeze['baseline_head'],
    'tracked_dirty_paths': tracked, 'tracked_dirty_equals_named': set(tracked) == changed,
    'unrelated_untracked_count': len(unrelated),
    'unrelated_names_match_baseline': unrelated == old_unrelated,
    'unrelated_added': sorted(set(unrelated) - set(old_unrelated)),
    'unrelated_missing': sorted(set(old_unrelated) - set(unrelated)),
    'CANON_matches_HEAD': git('show', 'HEAD:CANON.md') == (ROOT / 'CANON.md').read_bytes(),
    'exact_registry_matches_HEAD': git('show', 'HEAD:CURRENT_SCIENTIFIC_PREMISES.tsv') == (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes(),
    'original_freeze_reference_checks': original_checks,
    'original_freeze_references_all_match': all(x['matches'] for x in original_checks),
    'initial_integration_freeze_preserved': initial_freeze_hash_matches,
    'initial_integration_snapshot_checks': initial_snapshots,
    'initial_binding_check_preserved': initial_binding_hash_matches,
    'changed_prior_hashes_match_HEAD': head_prior_checks,
    'runtime': {'python': sys.version, 'git': git('--version').decode().strip()},
    'command': 'python3 ' + str(REVIEW / 'FINAL_VERIFY_BINDINGS.py'),
    'verification_script_sha256': sha(REVIEW / 'FINAL_VERIFY_BINDINGS.py'),
    'method': 'Python stdlib streaming SHA-256; entire accepted name/resolved-path protected screen before payload reads; compare with preserved prior record and baseline. Byte correspondence is not corpus reproof.',
    'repository_tests': 'normal/maintenance/full406 closure tests remain parent gate; no scientific replay needed absent changed concern',
    'scientific_integration_disposition': 'FM1 corrected summary independently inspected; final report states scope',
    'elapsed_seconds': time.monotonic() - start,
}
checks = [not mismatches, not removed, result['prior_record_hash_matches'],
          result['changed_prior_exact'], result['added_exact_new_files'],
          all(all(v.values()) for v in binding_checks.values()),
          result['head_matches_baseline'], branch == 'grok',
          result['tracked_dirty_equals_named'], result['unrelated_names_match_baseline'],
          result['CANON_matches_HEAD'], result['exact_registry_matches_HEAD'],
          result['original_freeze_references_all_match'], initial_freeze_hash_matches,
          initial_binding_hash_matches, all(x['matches'] for x in initial_snapshots),
          all(head_prior_checks.values())]
result['status'] = 'PASS' if all(checks) else 'FAIL'
(ROOT / REVIEW / 'FINAL_BINDING_CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'freeze_sha256', 'accepted_count',
    'changed_prior_count', 'added_count', 'unchanged_prior_count',
    'unrelated_untracked_count', 'elapsed_seconds']}, indent=2))
if not all(checks):
    raise SystemExit(1)
