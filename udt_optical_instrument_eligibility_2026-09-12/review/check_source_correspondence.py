"""Read-only byte/status correspondence audit; not a scientific eligibility test."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path('/home/udt-admin/udt_mass_codex')
package = repo / 'udt_optical_instrument_eligibility_2026-09-12'
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
expected_head = 'e89bfe9c6c404e1a70aa334e660ae46327f266ab'
expected_status = '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo).decode()

status = git('status', '--short')
original = ''.join(line + '\n' for line in status.splitlines()
                   if line != '?? udt_optical_instrument_eligibility_2026-09-12/')
source_pins = json.loads((package / 'SOURCE_PINS.json').read_text())['pins']
freeze_pins = json.loads((package / 'INITIAL_REVIEW_FREEZE.json').read_text())['pins']
source = json.loads((package / 'sources/SOURCE_RECORD.json').read_text())
source_results = {name: {'expected': pin, 'actual': digest(repo / name)}
                  for name, pin in source_pins.items()}
freeze_results = {name: {'expected': pin, 'actual': digest(package / name)}
                  for name, pin in freeze_pins.items()}
cache_results = {field: {'path': source[field], 'expected': source[hash_field],
                         'actual': digest(Path(source[field]))}
                 for field, hash_field in (
                     ('local_temporary_pdf', 'pdf_sha256'),
                     ('text_cache', 'text_sha256'),
                     ('rendered_page2', 'render_sha256'))}
result = {
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': 'Byte/status correspondence only; no protected payload reads or scientific tests',
    'python_version': sys.version,
    'git_version': git('--version').strip(),
    'branch': git('branch', '--show-current').strip(),
    'head': git('rev-parse', 'HEAD').strip(),
    'origin_grok': git('rev-parse', 'origin/grok').strip(),
    'status_command': ['git', 'status', '--short'],
    'original_status_entries': original.splitlines(),
    'original_status_count': len(original.splitlines()),
    'original_status_sha256': hashlib.sha256(original.encode()).hexdigest(),
    'source_pins': source_results,
    'initial_freeze_pins': freeze_results,
    'source_cache_pins': cache_results,
    'reviewer_page1_sha256': digest(Path('/tmp/ob2_reviewer_shen_page1.png')),
    'remote_sync': 'Parent-attributed; this reviewer only checked local tracking ref',
}
result['correspondence_pass'] = (
    result['branch'] == 'grok'
    and result['head'] == result['origin_grok'] == expected_head
    and result['original_status_count'] == 46
    and result['original_status_sha256'] == expected_status
    and all(r['expected'] == r['actual'] for group in
            (source_results, freeze_results, cache_results) for r in group.values())
)
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['correspondence_pass'] else 1)
