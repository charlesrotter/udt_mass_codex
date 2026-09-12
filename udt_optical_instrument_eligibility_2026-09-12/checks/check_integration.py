"""OB2 byte, scope and navigation correspondence; no scientific eligibility test."""
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parents[2]
package = repo / 'udt_optical_instrument_eligibility_2026-09-12'
baseline = 'e89bfe9c6c404e1a70aa334e660ae46327f266ab'
allowed = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'INDEX.md', 'UDT_RESEARCH_ROADMAP.md'}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo).decode()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

groups = {}
for name, root in [('SOURCE_PINS.json', repo), ('INITIAL_REVIEW_FREEZE.json', package)]:
    pins = json.loads((package / name).read_text())['pins']
    groups[name] = {p: {'expected': h, 'actual': sha(root / p)} for p, h in pins.items()}
source = json.loads((package / 'sources/SOURCE_RECORD.json').read_text())
groups['temporary_source'] = {field: {'expected': source[hash_field],
                                    'actual': sha(Path(source[field]))}
    for field, hash_field in [('local_temporary_pdf', 'pdf_sha256'),
                             ('text_cache', 'text_sha256'),
                             ('rendered_page2', 'render_sha256')]}
status_command = ['status', '--porcelain=v1', '--untracked-files=normal']
original = [line for line in git(*status_command).splitlines()
            if line.startswith('?? ') and line != '?? '+package.name+'/']
fingerprint = hashlib.sha256(('\n'.join(original)+'\n').encode()).hexdigest()
changed = set(git('diff', '--name-only', baseline, '--').splitlines())
nav = json.loads((package / 'checks/final_navigation.json').read_text())
nav_stdout = (package / 'checks/final_navigation.stdout').read_text()
with (repo / 'CURRENT_SCIENTIFIC_PREMISES.tsv').open(newline='') as stream:
    registry_rows = sum(1 for _ in csv.DictReader(stream, delimiter='\t'))
result = {'checked_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': __doc__, 'python_version': sys.version, 'git_version': git('--version').strip(),
    'branch': git('branch', '--show-current').strip(),
    'head': git('rev-parse', 'HEAD').strip(), 'origin_grok': git('rev-parse', 'origin/grok').strip(),
    'parent_observed_fetch': {'command': ['git', 'fetch', 'origin'], 'exit_code': 0,
                            'fresh_fetch_before_this_check': True},
    'original_status_command': ['git', *status_command],
    'original_name_status_count': len(original), 'original_name_status_sha256': fingerprint,
    'protected_payload_inspection': False, 'backup_completeness': 'UNVERIFIED',
    'changed_tracked_paths': sorted(changed), 'allowed_tracked_paths': sorted(allowed),
    'registry_rows': registry_rows, 'correspondence': groups,
    'actual_navigation': nav, 'navigation_stdout_sha256': sha(package / 'checks/final_navigation.stdout'),
    'same_session_full397_attribution': 'STARTUP_RECORD.json; unchanged exact source pins; no new OB2 full397 run',
    'root_sha256': {p: sha(repo / p) for p in sorted(allowed)},
    'root_sizes': {p: {'lines': len((repo/p).read_text().splitlines()),
                       'words': len((repo/p).read_text().split())} for p in sorted(allowed)}}
result['pass'] = (result['branch'] == 'grok' and result['head'] == result['origin_grok'] == baseline
    and changed == allowed and registry_rows == 397 and len(original) == 46
    and fingerprint == '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
    and all(r['expected'] == r['actual'] for group in groups.values() for r in group.values())
    and nav['returncode'] == 0 and '359 passed, 1 deselected' in nav_stdout
    and not (package / 'checks/final_navigation.stderr').read_bytes())
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['pass'] else 1)
