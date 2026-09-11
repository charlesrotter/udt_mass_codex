#!/usr/bin/env python3
"""Apply acceptance-only metadata after the actual frozen full395 PASS."""
import ast
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path

P = Path(__file__).resolve().parent
ROOT = P.parent
capture = json.loads((P / 'checks/full395.json').read_text())
assert capture['returncode'] == 0 and not capture['timeout']
assert not (P / 'checks/full395.stderr').read_bytes()
assert b'PASS: G383--G412 reviewed backlog' in (P / 'checks/full395.stdout').read_bytes()
inputs = json.loads((P / 'checks/full395_INPUTS.json').read_text())
for name, expected in inputs['files'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
review = json.loads((P / 'review_integration/REVIEW_RECEIPT.json').read_text())
assert review['verdict'] == 'VERIFIED_WITH_CAVEATS_EXACT_INTEGRATION_FIDELITY'
assert not review['unresolved_scientific_or_transcription_objections']
with (P / 'checks/full395_COMPLETION_INPUTS.json').open('x') as f:
    json.dump({'observed_utc': datetime.now(timezone.utc).isoformat(),
               'all17_frozen_inputs_unchanged_through_completion': True,
               'inputs': inputs['files'], 'actual_capture': capture}, f, indent=2)
    f.write('\n')

def replace(name, old, new):
    p = ROOT / name
    s = p.read_text()
    assert s.count(old) == 1, (name, old, s.count(old))
    p.write_text(s.replace(old, new))

prefix = P.name + '/'
replace(prefix + 'BANKING_RECORD.md',
    'DRAFT FOR INTEGRATION FIDELITY REVIEW. Source/readiness gates and the new prebank audit passed;\n'
    'expanded-registry checks and fresh integration review remain pending. No acceptance is claimed\n'
    'from this draft alone. Charles authorized promotion on 2026-09-10; see WORK_ORDER.md.',
    'ACCEPTED AT THE EXACT REVIEWED SCOPES: G383--G412. Source/readiness reviews, the new prebank365\n'
    'audit, fresh integration review and actual expanded full395 audit passed. Charles authorized\n'
    'promotion on 2026-09-10; see WORK_ORDER.md. Final status fidelity and publication have separate\n'
    'receipts; acceptance does not adopt physical premises or change canon.')
replace(prefix + 'BANKING_RECORD.md', '## What is proposed for acceptance', '## What is accepted')
replace(prefix + 'BANKING_RECORD.md', 'BANKED_ROWS.tsv is the exact proposed addition',
        'BANKED_ROWS.tsv is the exact accepted addition')
replace(prefix + 'BANKING_RECORD.md',
    'provenance. This is a new execution, not a rehearsal or source-reviewer rerun.',
    'provenance. This is a new execution, not a rehearsal or source-reviewer rerun.\n\n'
    f"Expanded full395: exit0/PASS, empty stderr, {capture['duration_seconds']:.6f}seconds, "
    f"{capture['maxrss_kib']}KiB max RSS,\n"
    f"2GiB/900s; started{capture['started_utc']}. checks/full395.* preserves the actual run;\n"
    'full395_INPUTS.json and full395_COMPLETION_INPUTS.json authenticate unchanged inputs through\n'
    'completion. The initial failed integration run and all packaging repairs remain preserved.\n'
    'After this PASS, only acceptance/check-receipt prose and additional immutable review pins\n'
    'were finalized; scientific rows, claims, source evidence and verifier logic stayed fixed.\n'
    'Final status/pin fidelity and short-guard outcomes are recorded separately in\n'
    'review_integration/FINAL_FIDELITY.md and checks/final_guards.*; no full source reproof is claimed.')

p = P / 'DISPOSITIONS.tsv'
rows = list(csv.DictReader(io.StringIO(p.read_text()), delimiter='\t'))
changed = 0
for row in rows:
    if row['disposition'] == 'PROPOSED_EXACT_SCOPE_ACCEPTANCE':
        row['disposition'] = 'BANKED_AT_EXACT_REVIEWED_SCOPE'
        row['reason_or_remaining_gate'] = 'Source/readiness, fresh integration review and actual full395 passed; exact conditions and evidence category retained.'
        changed += 1
assert changed == 30
out = io.StringIO(); writer = csv.DictWriter(out, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
writer.writeheader(); writer.writerows(rows); p.write_text(out.getvalue())

replacements = {
    'LIVE.md': [
        ('Banking through G382 is COMPLETE; G383--G412 integration is pending final checks/review.',
         'Exact-scope banking through G412 is COMPLETE; all inherited limits remain.'),
        ('`INDEX.md` routes the banking draft.', '`INDEX.md` routes the acceptance record.')],
    'HANDOFF.md': [
        ('G383--G412 backlog integration awaits final checks/review.', 'G383--G412 exact-scope banking is COMPLETE.'),
        ('banking draft/checks: INDEX.', 'acceptance/checks: INDEX.')],
    'CURRENT_RESEARCH_PROGRAM.md': [
        ('G383--G412 banking draft/checks: INDEX; final integration pending.',
         'G383--G412 exact-scope banking COMPLETE; checks/reviews: INDEX.')],
    'CURRENT_SCIENTIFIC_PREMISES.md': [
        ('Banking through G382 is COMPLETE; G383--G412 integration awaits final checks/review.',
         'Exact-scope banking through G412 is COMPLETE; all inherited limits remain.'),
        ('New prebank365 PASS; expanded banking checks/review: INDEX.',
         'New prebank365 and full395 PASS; banking checks/review: INDEX.')],
    'INDEX.md': [
        ('G383--G412 banking draft; final integration pending. Earlier banking through G382 COMPLETE.',
         'G383--G412 exact-scope banking COMPLETE; actual full395 PASS; scopes/reviews below.')],
    'MEMORY.md': [
        ('G383--G412 backlog integration awaits final checks/review;',
         'G383--G412 exact-scope banking COMPLETE;')],
    'UDT_RESEARCH_ROADMAP.md': [
        ('ER1 COMPLETE, reviewed; G405 exact-scope banking integration pending',
         'ER1 COMPLETE, reviewed; G405 conditionally banked at exact scope'),
        ('with source gates passed and final integration pending.',
         'with source/review gates and actual full395 PASS.'),
        ('Relevant reviewed work included in the banking packet:',
         'Relevant conditional results now banked at their reviewed scopes:')],
}
for name, pairs in replacements.items():
    for old, new in pairs:
        replace(name, old, new)
for name in ('LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md'):
    replace(name, 'G383--G412 exact-scope banking awaits final integration;',
            'G383--G412 exact-scope banking is COMPLETE;')

# Pin additional immutable review records; no verifier logic changes.
p = ROOT / 'verify_current_scientific_premises.py'; s = p.read_text()
node = next(n for n in ast.parse(s).body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == 'REVIEWED_BACKLOG_PINS' for t in n.targets))
pins = ast.literal_eval(node.value)
for name in ('REVIEW_REPORT.md', 'CLAIM_FIDELITY.tsv', 'REVIEW_RECEIPT.json', 'SHA256SUMS'):
    pins[prefix + 'review_integration/' + name] = ''
pins = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in pins}
lines = s.splitlines(keepends=True)
lines[node.lineno-1:node.end_lineno] = ['REVIEWED_BACKLOG_PINS = ' + repr(pins) + '\n']
p.write_text(''.join(lines))
print(json.dumps({'accepted_entries': changed, 'pinned_guard_files': len(pins),
                  'full395_returncode': capture['returncode'],
                  'final_status_fidelity_and_short_guards': 'PENDING_BEFORE_PUBLICATION'}))
