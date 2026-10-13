"""Proportional correspondence check; no inherited scientific reproof."""
import hashlib
import json
import platform
import subprocess
from pathlib import Path

pkg = Path('research_goal_orientation_2026-10-13')
freeze_path = pkg / 'INTEGRATION_FREEZE.json'
freeze = json.loads(freeze_path.read_text())
prior_path = Path(freeze['prior_review_record'])
prior = json.loads(prior_path.read_text())
baseline = json.loads((pkg / 'BASELINE.json').read_text())
initial_path = pkg / 'INITIAL_INTEGRATION_FREEZE.json'
initial = json.loads(initial_path.read_text())
initial_texts = json.loads((pkg / 'INITIAL_INTEGRATION_TEXTS.json').read_text())
blocked_prefixes = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
)
blocked_names = set(baseline['existing_untracked_names_only'])
current = freeze['accepted_sha256']
previous = prior['accepted_sha256']
names = set(current) | set(previous) | set(initial['accepted_sha256'])
unsafe = [p for p in names if p in blocked_names or p.startswith(blocked_prefixes)
          or Path(p).is_absolute() or '..' in Path(p).parts]
assert not unsafe, unsafe
# All accepted-map names are screened before any corresponding content is hashed.
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
freeze_hash = sha(freeze_path)
assert freeze_hash == 'ce8bfaf36af32d7fc088a0bf25a42a70df1563cd8ef9f5f8a2283d8ff773546a'
assert sha(initial_path) == '38e538b89d4ad82b6cc2c9d60392c0e1e419ae454fa87e37f323a0a61ff4e0da'
assert sha(prior_path) == freeze['prior_review_record_sha256']
changed = sorted(p for p in current.keys() & previous.keys() if current[p] != previous[p])
added = sorted(current.keys() - previous.keys())
removed = sorted(previous.keys() - current.keys())
unchanged = [p for p in current.keys() & previous.keys() if current[p] == previous[p]]
assert changed == sorted(freeze['inherited_changed']) == sorted(freeze['explicit_changed_documents'])
assert added == sorted(freeze['added']) and removed == freeze['removed'] == []
assert len(unchanged) == freeze['inherited_unchanged_count'] == 14624
assert len(current) == 14640 and len(changed) == 6 and len(added) == 10
content_checked = {p: sha(p) for p in changed + added}
assert all(content_checked[p] == current[p] for p in content_checked)
assert set(initial_texts) == set(changed)
for p, archived in initial_texts.items():
    assert hashlib.sha256(archived['text'].encode()).hexdigest() == archived['sha256']
    assert archived['sha256'] == initial['accepted_sha256'][p]
repaired = sorted(p for p in initial['accepted_sha256'] if initial['accepted_sha256'][p] != current[p])
assert repaired == ['AGENTS.md', 'CLAUDE.md', 'UDT_RESEARCH_ROADMAP.md']
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
tracked_changes = subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], text=True).splitlines()
assert head == baseline['head'] and branch == baseline['branch'] == 'grok'
assert sorted(tracked_changes) == changed
untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()
unrelated = sorted(p for p in untracked if not p.startswith(str(pkg) + '/'))
assert unrelated == sorted(blocked_names)
committed_prior = subprocess.check_output(['git', 'show', head + ':development_reconstruction_2026-09-29/REVIEW_RECORD.json'])
assert hashlib.sha256(committed_prior).hexdigest() == freeze['prior_review_record_sha256']
diff_check = subprocess.run(['git', 'diff', '--check'], text=True, capture_output=True)
assert diff_check.returncode == 0, diff_check.stdout + diff_check.stderr
print(json.dumps({
    'verdict': 'PASS', 'python_version': platform.python_version(),
    'head': head, 'branch': branch, 'freeze_sha256': freeze_hash,
    'accepted_count': len(current), 'inherited_unchanged_map_count': len(unchanged),
    'changed': changed, 'added': added, 'removed': removed,
    'repaired_since_initial_freeze': repaired,
    'initial_freeze_and_six_archived_text_hashes_match': True,
    'protected_or_unrelated_accepted_paths': unsafe,
    'unrelated_untracked_names_preserved_count': len(unrelated),
    'changed_and_added_content_checked': content_checked,
    'prior_record_matches_committed_baseline': True,
    'git_diff_check_exit': diff_check.returncode,
    'git_diff_check_stdout': diff_check.stdout,
    'git_diff_check_stderr': diff_check.stderr,
    'inherited_content_note': 'Map inheritance and unchanged tracked status verified; inherited source bodies were not independently rehashed or re-proved in this proportional method review.'
}, indent=2))
