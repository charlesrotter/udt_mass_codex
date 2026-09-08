"""Prove exact completion-only delta against the reviewed integration freeze."""
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
BANK = ROOT / 'udt_g372_g373_conditional_banking_2026-09-08'
manifest = BANK / 'INTEGRATION_FREEZE_SHA256SUMS'
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == 'dcef1e8d250152dce19cda79248868ea8900aed82e1fda5e385747ec0507e6fe'
old = b'Promotion integration is PENDING full356 and fresh fidelity gates; its EXECUTION_RECORD.md owns completion.'
new = b'Promotion integration is COMPLETE after full356 and fresh fidelity gates; its EXECUTION_RECORD.md owns completion.'
changed = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md'}
records = {}
entries = manifest.read_text().splitlines()
assert len(entries) == 12
for line in entries:
    expected, relative = line.split(maxsplit=1)
    payload = (ROOT / relative).read_bytes()
    if relative in changed:
        assert payload.count(new) == 1 and payload.count(old) == 0
        restored = payload.replace(new, old, 1)
    else:
        restored = payload
    assert hashlib.sha256(restored).hexdigest() == expected, relative
    records[relative] = {
        'current_sha256': hashlib.sha256(payload).hexdigest(),
        'only_completion_sentence_changed': relative in changed,
    }

pins = {
    'full356.stdout': '99ec8ccceb6f850e8dc8188299594eb6413890e0e6492767ef580b4766fd3cb6',
    'full356.stderr': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'full356.time': '3d9d631d870a4bb5a345132e23f09f90b2c52baa4c7493db5cd140979e85a4ed',
}
for relative, expected in pins.items():
    assert hashlib.sha256((BANK / relative).read_bytes()).hexdigest() == expected
out = (BANK / 'full356.stdout').read_text()
assert 'PASS: 356-row premise registry' in out
assert 'PASS: G372/G373 conditional independent-data and LOCAL ANALYTIC' in out
assert re.search(r'^\s*Exit status: 0$', (BANK / 'full356.time').read_text(), re.M)
parent_capture = json.loads((BANK / 'banking_checks_final.json').read_text())
assert parent_capture['returncode'] == 0 and not parent_capture['timeout']
parent_result = json.loads((BANK / 'banking_checks_final.stdout').read_text())
assert parent_result['registry_rows'] == 356
assert len(parent_result['actual_mutants_caught']) == 11
assert all(parent_result['checks'].values())
assert (BANK / 'banking_checks_final.stderr').read_bytes() == b''
print(json.dumps({
    'verdict': 'PASS_EXACT_COMPLETION_DELTA_AND_RECEIPT_CORRESPONDENCE',
    'targets': records,
    'final_full_audit_receipts': pins,
    'parent_final_focused_result': 'PASS_356_ROWS_11_EXPECTED_MUTANTS',
    'publication_checked': False,
}, indent=2, sort_keys=True))
