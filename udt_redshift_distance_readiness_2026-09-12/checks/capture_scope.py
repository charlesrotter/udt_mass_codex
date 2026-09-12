"""ZDR1 source/freeze and workspace correspondence; no scientific proof or payload audit."""
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

package = Path(__file__).resolve().parents[1]
repo = package.parent
startup = json.loads((package / 'STARTUP_RECORD.json').read_text())
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
source = json.loads((package / 'sources/DES_SOURCE.json').read_text())
groups['temporary_DES_source'] = {source['temporary_cache']:
    {'expected': source['sha256'], 'actual': sha(Path(source['temporary_cache']))}}
status_args = ['status', '--porcelain=v1', '--untracked-files=normal']
original = [line for line in git(*status_args).splitlines()
            if line.startswith('?? ') and line != '?? '+package.name+'/']
fingerprint = hashlib.sha256(('\n'.join(original)+'\n').encode()).hexdigest()
changed = set(git('diff', '--name-only', startup['head'], '--').splitlines())
with (repo / 'CURRENT_SCIENTIFIC_PREMISES.tsv').open(newline='') as stream:
    rows = sum(1 for _ in csv.DictReader(stream, delimiter='\t'))
executions = {}
for name in ['current_full397', 'conditional_joins', 'postclarification_navigation']:
    stem = package / 'checks' / name
    executions[name] = {'receipt': json.loads(stem.with_suffix('.json').read_text()),
        'stdout_sha256': sha(stem.with_suffix('.stdout')),
        'stderr_bytes': stem.with_suffix('.stderr').stat().st_size}
result = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'scope': __doc__,
    'python_version': sys.version, 'git_version': git('--version').strip(),
    'branch': git('branch', '--show-current').strip(),
    'head': git('rev-parse', 'HEAD').strip(), 'origin_grok': git('rev-parse', 'origin/grok').strip(),
    'fetch_evidence': 'Parent just observed git fetch origin exit0; not rerun by this command',
    'original_status_command': ['git', *status_args],
    'original_name_status_count': len(original), 'original_name_status_sha256': fingerprint,
    'changed_tracked_paths': sorted(changed), 'allowed_tracked_paths': sorted(allowed),
    'registry_rows': rows, 'correspondence': groups, 'actual_executions': executions,
    'root_pins': {p: sha(repo / p) for p in sorted(allowed)},
    'protected_payload_inspection': False, 'backup_completeness': 'UNVERIFIED',
    'pre_reboot_unsaved_state': 'UNVERIFIED', 'general_agent_capacity': 'UNVERIFIED'}
result['pass'] = (result['branch'] == 'grok'
    and result['head'] == result['origin_grok'] == startup['head']
    and changed == allowed and rows == 397
    and len(original) == startup['original_untracked_count']
    and fingerprint == startup['original_name_status_sha256']
    and all(x['expected'] == x['actual'] for group in groups.values() for x in group.values())
    and all(x['receipt']['returncode'] == 0 and x['stderr_bytes'] == 0
            for x in executions.values())
    and '359 passed, 1 deselected' in
        (package / 'checks/postclarification_navigation.stdout').read_text())
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['pass'] else 1)
