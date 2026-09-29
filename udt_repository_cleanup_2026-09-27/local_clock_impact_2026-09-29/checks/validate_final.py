"""LCIA1 packaging regression; neither semantic completeness nor scientific proof."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from verify_current_scientific_premises import validate_startup_surface


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output([
        'git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
        '-c', 'core.packedGitWindowSize=8m', '-c', 'core.packedGitLimit=32m',
        *args], cwd=ROOT)


launch = json.loads((HERE / 'LAUNCH.json').read_text())
assert git('branch', '--show-current').decode().strip() == 'grok'
assert git('rev-parse', 'HEAD').decode().strip() == launch['head']
assert git('rev-parse', 'origin/grok').decode().strip() == launch['origin_grok']
assert not git('diff', '--cached', '--name-only').strip()
notices = list(csv.DictReader((HERE / 'NOTICE_LEDGER.tsv').open(), delimiter='\t'))
assert len(notices) == 10
by_path = {row['path']: row for row in notices}
assert len(by_path) == 10
for name, expected in launch['package_baseline_sha256'].items():
    content = (ROOT / name).read_bytes()
    if name in by_path:
        row = by_path[name]
        prefix, body = content[:int(row['prefix_bytes'])], content[int(row['prefix_bytes']):]
        assert prefix.startswith(b'<!-- LCIA1_CURRENT_USE_BEGIN -->\n')
        assert prefix.endswith(b'<!-- LCIA1_CURRENT_USE_END -->\n\n')
        assert content.count(b'<!-- LCIA1_CURRENT_USE_BEGIN -->') == 1
        assert digest(prefix) == row['notice_sha256']
        assert digest(content) == row['current_sha256']
        assert digest(body) == row['original_body_sha256'] == expected
        assert row['baseline_commit'] == launch['head']
        assert body == git('show', launch['head'] + ':' + name)
    else:
        assert digest(content) == expected, name
assert len(launch['package_baseline_sha256']) == 849
for name, expected in launch['source_pins'].items():
    assert digest((ROOT / name).read_bytes()) == expected, name
changed = set(git('diff', '--name-only').decode().splitlines())
assert changed == set(launch['maintained_pointers']) | set(by_path)
audit_prefix = HERE.relative_to(ROOT).as_posix() + '/'
untracked = git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
prior = {name for name in untracked if name and not name.startswith(audit_prefix)}
assert prior == set(launch['prior_untracked_names'])
assert len(prior) == 52
for filename, base in [('CANDIDATE_FREEZE.json', HERE),
                       ('review/SOURCE_FIRST_SEAL.json', HERE / 'review')]:
    for name, expected in json.loads((HERE / filename).read_text())['sha256'].items():
        assert digest((base / name).read_bytes()) == expected, name
program = (ROOT / 'CURRENT_RESEARCH_PROGRAM.md').read_text()
old_program = git('show', launch['head'] + ':CURRENT_RESEARCH_PROGRAM.md').decode()
for text in [program, old_program]:
    assert text.count('## Purpose and the missing connection\n') == 1
    assert text.count('## Current next gate\n') == 1
assert program.split('## Purpose and the missing connection\n')[1].split('## Current next gate\n')[0] == old_program.split('## Purpose and the missing connection\n')[1].split('## Current next gate\n')[0]
assert program.split('## Architecture\n')[1] == old_program.split('## Architecture\n')[1]
roadmap = (ROOT / 'UDT_RESEARCH_ROADMAP.md').read_text()
old_roadmap = git('show', launch['head'] + ':UDT_RESEARCH_ROADMAP.md').decode()
marker = '## Machian investigative direction — 2026-09-28\n'
assert roadmap.split(marker)[1] == old_roadmap.split(marker)[1]
receipt = json.loads((HERE / 'checks/premise_audit.json').read_text())
assert receipt['returncode'] == 0 and not receipt['timeout']
assert (HERE / 'checks/premise_audit.stderr').stat().st_size == 0
assert 'PASS: 406-row premise registry' in (HERE / 'checks/premise_audit.stdout').read_text()
validate_startup_surface(ROOT)
assert not git('diff', '--check').strip()
print(json.dumps({
    'result': 'PASS', 'startup_surface': 'PASS', 'unchanged_package_files': 839,
    'byte_preserved_original_briefs': 10, 'unchanged_authority_pins': len(launch['source_pins']),
    'prior_untracked_names_preserved': len(prior), 'exact_tracked_change_paths': len(changed),
    'founding_architecture_and_prior_owner_directions': 'unchanged',
    'candidate_and_source_first_seals': 'unchanged', 'full_premise_audit': 'attributed pre-edit PASS',
    'limits': 'Packaging regression. No scientific regrade or semantic completeness claim.'
}, indent=2))
