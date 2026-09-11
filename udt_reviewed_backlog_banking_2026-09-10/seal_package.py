#!/usr/bin/env python3
"""Seal this completed evidence change once; publication receipt is subsequent."""
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
ROOT_FILES = (
    'AGENTS.md', 'CURRENT_RESEARCH_PROGRAM.md', 'CURRENT_SCIENTIFIC_PREMISES.md',
    'CURRENT_SCIENTIFIC_PREMISES.tsv', 'HANDOFF.md', 'INDEX.md', 'LIVE.md', 'MEMORY.md',
    'UDT_RESEARCH_ROADMAP.md', 'verify_current_scientific_premises.py',
    'tests/test_startup_surface.py', 'tests/test_reviewed_backlog_banking.py',
)
EXCLUDED = {'SHA256SUMS', 'STAGING_FILES.json', 'PUBLICATION_RECEIPT.md',
            'PUBLICATION_RECEIPT.json'}
files = [ROOT / name for name in ROOT_FILES]
files += [p for p in PACKAGE.rglob('*') if p.is_file() and not p.is_symlink()
          and '__pycache__' not in p.parts and p.suffix != '.pyc'
          and not (p.parent == PACKAGE and p.name in EXCLUDED)]
files = sorted(set(files))
names = [str(p.relative_to(ROOT)) for p in files]
with (PACKAGE / 'SHA256SUMS').open('x') as output:
    for p, name in zip(files, names):
        output.write(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + name + '\n')
with (PACKAGE / 'STAGING_FILES.json').open('x') as output:
    json.dump({'scope': 'Only this banking package and the twelve explicit root/test files; '
                       'publication receipts are subsequent, caches excluded. '
                       'Ignored stdout files are intentional evidence.',
               'files': names + [str((PACKAGE / 'SHA256SUMS').relative_to(ROOT)),
                                 str((PACKAGE / 'STAGING_FILES.json').relative_to(ROOT))]},
              output, indent=2)
    output.write('\n')
print(json.dumps({'manifest_files': len(files), 'staging_files': len(files) + 2,
                  'bytes': sum(p.stat().st_size for p in files)}))
