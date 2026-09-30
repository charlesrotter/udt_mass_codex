"""PCW1 packaging correspondence, not scientific proof or a completeness test."""
from pathlib import Path
import hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'udt_physical_connection_whiteboard_2026-09-30/'
WORK = ROOT / PREFIX
def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git', '-c', 'core.preloadIndex=false',
        '-c', 'index.threads=1', *args], cwd=ROOT, text=True).strip()

launch = json.loads((WORK / 'LAUNCH.json').read_text())
freeze = json.loads((WORK / 'INTEGRATION_FREEZE.json').read_text())
candidate = json.loads((WORK / 'CANDIDATE_FREEZE.json').read_text())
for path, expected in candidate['sha256'].items():
    assert digest(path) == expected, ('initial candidate changed', path)
for path, expected in freeze['accepted_sha256'].items():
    assert digest(path) == expected, ('integration changed', path)
record = json.loads((ROOT / 'development_reconstruction_2026-09-29/REVIEW_RECORD.json').read_text())
assert record['accepted_sha256'] == freeze['accepted_sha256']
assert len(record['reviewers']) == 2
for reviewer in record['reviewers']:
    att = json.loads((ROOT / reviewer['attestation']).read_text())
    assert digest(reviewer['attestation']) == reviewer['sha256']
    assert att['accepted_sha256'] == freeze['accepted_sha256']
    assert att['verdict'] == 'ACCEPT_WITH_LIMITS'
    assert digest(att['report_path']) == att['report_sha256']

# Names only: never open, hash or inspect protected payloads.
unrelated = [x for x in git('ls-files', '--others', '--exclude-standard').splitlines()
             if not x.startswith(PREFIX)]
assert unrelated == launch['unrelated_untracked_names']
assert git('branch', '--show-current') == 'grok'
allowed = set(freeze['changed_previous_bindings']) | {
    'development_reconstruction_2026-09-29/REVIEW_RECORD.json'}
assert set(git('diff', '--name-only').splitlines()) <= allowed
for path in ('CURRENT_SCIENTIFIC_PREMISES.tsv', 'founding.md', 'CANON.md'):
    original = subprocess.check_output(['git', 'show', launch['head'] + ':' + path], cwd=ROOT)
    assert (ROOT/path).read_bytes() == original, ('protected authority changed',path)

link_count = 0
for path in [ROOT/'UDT_DEVELOPMENT.md', ROOT/'LIVE.md', ROOT/'HANDOFF.md',
             ROOT/'UDT_RESEARCH_ROADMAP.md', *sorted(WORK.rglob('*.md'))]:
    for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]*)\)', path.read_text()):
        if target.startswith(('http:', 'https:', '#')):
            continue
        target = target.split('#',1)[0]
        if target:
            assert (path.parent/target).exists(), ('missing local link', str(path), target)
            link_count += 1
size = sum(p.stat().st_size for p in WORK.rglob('*') if p.is_file())
assert size < 20*1024*1024
print(json.dumps({'status':'PASS', 'scope':'Byte/route/preservation correspondence only',
    'candidate_files':len(candidate['sha256']), 'accepted_files':len(freeze['accepted_sha256']),
    'preserved_unrelated_names':len(unrelated), 'local_links':link_count,
    'package_bytes':size},indent=2))
