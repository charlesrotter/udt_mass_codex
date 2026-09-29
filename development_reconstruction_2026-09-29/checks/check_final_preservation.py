"""Bounded packaging checks; no protected payload reads or scientific replay."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'development_reconstruction_2026-09-29'
launch = json.loads((WORK / 'LAUNCH.json').read_text())


def git(*args):
    return subprocess.check_output(['git', '-c', 'core.preloadIndex=false',
                                    '-c', 'index.threads=1', *args], cwd=ROOT)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


fixed = ['CANON.md', 'founding.md', 'CURRENT_SCIENTIFIC_PREMISES.tsv',
         'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv',
         'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md']
for name in fixed:
    assert sha(ROOT / name) == launch['source_before_sha256'][name], name

allowed = sorted(['AGENTS.md', 'CLAUDE.md', 'CURRENT_RESEARCH_PROGRAM.md',
                  'CURRENT_SCIENTIFIC_PREMISES.md', 'HANDOFF.md', 'INDEX.md',
                  'LIVE.md', 'MEMORY.md', 'UDT_RESEARCH_ROADMAP.md',
                  'verify_current_scientific_premises.py'])
changed = sorted(git('diff', '--name-only', launch['head']).decode().splitlines())
assert changed == allowed, changed
assert git('diff', '--cached', '--name-only') == b'', 'unexpected staged work'
assert git('branch', '--show-current').decode().strip() == 'grok'
assert git('rev-parse', 'HEAD').decode().strip() == launch['head']

# Inspect names only: never open, hash or reconstruct unrelated/protected payloads.
untracked = set(git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
assert set(launch['prior_untracked_names']) <= untracked

before = ast.parse(git('show', launch['head'] + ':verify_current_scientific_premises.py'))
after = ast.parse((ROOT / 'verify_current_scientific_premises.py').read_text())
functions = lambda tree: {node.name: ast.dump(node) for node in tree.body
                          if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
old_funcs, new_funcs = functions(before), functions(after)
assert old_funcs.keys() == new_funcs.keys()
changed_funcs = sorted(k for k in old_funcs if old_funcs[k] != new_funcs[k])
assert changed_funcs == ['main', 'validate_startup_surface'], changed_funcs

record = json.loads((WORK / 'REVIEW_RECORD.json').read_text())
for name, expected in record['accepted_sha256'].items():
    assert sha(ROOT / name) == expected, name
for reviewer in record['reviewers']:
    assert sha(ROOT / reviewer['attestation']) == reviewer['sha256']
    attestation = json.loads((ROOT / reviewer['attestation']).read_text())
    assert sha(ROOT / attestation['report_path']) == attestation['report_sha256']

links_checked = 0
for name in ['UDT_DEVELOPMENT.md', 'INDEX.md', 'UDT_RESEARCH_ROADMAP.md']:
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', (ROOT / name).read_text()):
        if '://' in target or target.startswith('mailto:'):
            continue
        path, _, anchor = target.partition('#')
        dest = ROOT / (path or name)
        assert dest.exists(), (name, target)
        if anchor and dest.name == 'UDT_DEVELOPMENT.md':
            assert f'id="{anchor}"' in dest.read_text(), (name, target)
        links_checked += 1

surfaces = ['LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
            'CURRENT_SCIENTIFIC_PREMISES.md', 'INDEX.md', 'MEMORY.md']
sizes = {name: {'before_lines': len(git('show', launch['head'] + ':' + name).splitlines()),
                'after_lines': len((ROOT / name).read_text().splitlines())}
         for name in surfaces}
files = [p for p in WORK.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
size = sum(p.stat().st_size for p in files)
assert size < 20 * 1024**2
print(json.dumps({'status': 'PASS', 'fixed_sources_unchanged': fixed,
                  'tracked_changes': changed, 'original_validator_changes': changed_funcs,
                  'prior_untracked_names_preserved': len(launch['prior_untracked_names']),
                  'protected_payloads_read_or_hashed': False,
                  'accepted_files_match': len(record['accepted_sha256']),
                  'actual_reviewers_bound': len(record['reviewers']),
                  'local_links_checked': links_checked, 'startup_surface_lines': sizes,
                  'workspace_files_at_check': len(files), 'workspace_bytes_at_check': size}, indent=2))
