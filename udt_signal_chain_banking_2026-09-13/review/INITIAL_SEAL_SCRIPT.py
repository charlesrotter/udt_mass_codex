"""Administrative final review seal; writes only this review directory."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json

R = Path(__file__).resolve().parents[2]
B = R / 'udt_signal_chain_banking_2026-09-13'
V = B / 'review'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
amend = read(B / 'FINAL_INTAKE_AMENDMENT.json')
intake = read(B / 'FINAL_REVIEW_INTAKE.json')
old = B / amend['initial_copy']
new = B / 'CLOSEOUT.md'
assert sha(old) == amend['old_closeout_sha256'] == intake['files'][str(new.relative_to(R))]
assert sha(new) == amend['new_closeout_sha256']
assert sha(B / 'FINAL_REVIEW_INTAKE.json') == amend['initial_intake_sha256']
assert sha(V / 'INITIAL_FINAL_INTAKE.json') == amend['initial_intake_sha256']
assert sha(V / 'INITIAL_FINAL_CLOSEOUT.md') == amend['old_closeout_sha256']
before = 'Reviewer integration:198 hostile cases, including all new-row fields, current'
after = ('Reviewer integration:198 boundary cases (163 rejections,35 valid/historical\n'
         '  acceptances), including all new-row fields, current')
assert old.read_text().count(before) == 1
assert old.read_text().replace(before, after) == new.read_text()
for n, h in intake['files'].items():
    assert sha(R / n) == (amend['new_closeout_sha256'] if n == str(new.relative_to(R)) else h)
meta = read(V / 'FINAL_METADATA_CHECK.json')
assert meta['original_intake_mismatches'] == {str(new.relative_to(R)): {
    'original': amend['old_closeout_sha256'], 'current': amend['new_closeout_sha256']}}
initial = read(V / 'REVIEW_RECEIPT.json')
for n, h in initial['input_sha256'].items():
    assert sha(R / n) == h
assert sha(V / 'REVIEW_RECEIPT.json') == '84b825fefc72ff9cd43ca0998fae12e3e670e6d23e027dcc06f22f8580aa4845'
amend_check = {
    'verdict': 'PASS_EXACT_ONE_FILE_EDITORIAL_AMENDMENT',
    'original_final_intake_unchanged': True,
    'original_closeout_copies_authenticated': 2,
    'changed_files': [str(new.relative_to(R))],
    'other_nine_original_intake_files_unchanged': True,
    'exact_replacement': {'before': before, 'after': after},
    'science_guard_test_change': False,
    'amendment_sha256': sha(B / 'FINAL_INTAKE_AMENDMENT.json'),
    'old_closeout_sha256': sha(old),
    'current_closeout_sha256': sha(new),
}
(V / 'FINAL_AMENDMENT_CHECK.json').write_text(json.dumps(amend_check, indent=2) + '\n')
captures = []
for stem in ['source_authentication', 'saved_readouts', 'integration_initial', 'integration_pinned', 'manifest_membership']:
    data = read(V / (stem + '.json'))
    assert data['returncode'] == 0 and not data['timeout']
    captures.append({'stem': stem, **{k: data[k] for k in ['started_utc', 'duration_seconds', 'maxrss_kib', 'command', 'cpu_seconds', 'address_space_bytes']}})
paths = set(initial['input_sha256'])
paths.update(read(B / 'AUDIT_INPUTS.json')['sha256'])
paths.update(intake['files'])
paths.update(['CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md',
              'udt_signal_continuation_2026-09-13/WORK_ORDER.md'])
for p in B.iterdir():
    if p.is_file() and p.name in ['AUDIT_INPUTS.json', 'POST_AUDIT_NAVIGATION.json', 'FINAL_REVIEW_INTAKE.json',
                                  'FINAL_INTAKE_AMENDMENT.json', 'CLOSEOUT_BEFORE_COUNT_CLARIFICATION.md',
                                  'EXECUTION_INTERVALS.json', 'INTEGRATION_REPAIR_NOTE.md']:
        paths.add(str(p.relative_to(R)))
for directory in [V, B / 'checks']:
    for p in directory.iterdir():
        if p.is_file() and p.name != 'FINAL_RECEIPT.json':
            paths.add(str(p.relative_to(R)))
hashes = {n: sha(R / n) for n in sorted(paths)}
now = datetime.datetime.now(datetime.timezone.utc)
start = datetime.datetime.fromisoformat('2026-09-13T02:36:34+00:00')
deadline = datetime.datetime.fromisoformat('2026-09-13T03:16:34+00:00')
assert now < deadline
receipt = {
    'sealed_utc': now.isoformat(),
    'actual_review_end_utc': now.isoformat(),
    'verdict': 'VERIFIED_WITH_CAVEATS_EXACT_CONDITIONAL_BANKING_FIDELITY_ACCEPTED',
    'unresolved_review_objections': [],
    'closed_initial_pending_gates': ['guard implementation and actual boundary/catch tests', 'original398 preservation/current406 exact claims', 'new parent full406 premise audit', 'final navigation, input, closeout and source fidelity'],
    'remaining_parent_owned': ['exact staging and evidence manifest', 'accepted commit/push and publication receipts'],
    'review_context': '/root/signal_banking_review',
    'actual_separate_context_count': 1,
    'subdelegation_count': 0,
    'parent_startup_attribution': 'Completed earlier in the same continuing top-level session; reviewer independently checked assigned scope and local branch/hash/status.',
    'baseline_head': meta['baseline_head'],
    'local_origin_ref': meta['local_origin_ref'],
    'branch': meta['branch'],
    'remote_fetch_pull': 'Parent-attributed successful synchronization; reviewer independently read local refs, did not mutate Git.',
    'conservative_allocation_start_utc': start.isoformat(),
    'first_observed_clock_utc': '2026-09-13T02:37:02Z',
    'first_action': initial['first_action'],
    'hard_deadline_utc': deadline.isoformat(),
    'elapsed_upper_bound_seconds': (now - start).total_seconds(),
    'configured_parent_attribution': 'gpt-6-astra/xhigh; not runtime attestation',
    'runtime_model': 'UNATTESTED',
    'different_model': 'UNTESTED',
    'general_capacity': 'UNVERIFIED',
    'exposure': initial['source_exposure'],
    'independence': 'Fresh separate context; independent saved-readout arithmetic and Path.open attack harness; actual shared production guards. Original scientific arguments and verdicts exposed and attributed; not blind scientific reproof.',
    'source_manifest_members': 662,
    'source_membership_and_working_baseline_hashes_exact': True,
    'original398_byte_identity': True,
    'current406_exact_claims': True,
    'acceptance_ids': ['G416=OB1', 'G417=ZDR1', 'G418=NCR1', 'G419=NTB1', 'G420=LSB1', 'G421=CSS3', 'G422=CSS4', 'G423=CSS5'],
    'boundary_cases_per_integration_run': {'total': 198, 'expected_rejections': 163, 'valid_historical_acceptances': 35},
    'additional_catches': {'same_shared_gate_disabled_red_assertions': 4, 'forged_membership_rejection': 1},
    'repairs': [
        {'id': 'D1', 'scope': 'freeze versus output/exposure chronology', 'status': 'RESOLVED_EXPLICIT_ACCEPTANCE_AMENDMENT', 'science_changed': False},
        {'id': 'PARENT_WORD_LIMIT', 'scope': 'MEMORY451 to450 words', 'status': 'RESOLVED_ORIGINAL_FAILURE_PRESERVED_THRESHOLD_UNCHANGED', 'science_changed': False},
        {'id': 'FINAL_COUNT_PRECISION', 'scope': '198 boundary cases:163 rejection and35 acceptance', 'status': 'RESOLVED_EXACT_ONE_FILE_FINAL_INTAKE_AMENDMENT', 'science_changed': False},
    ],
    'parent_checks': {
        'initial_integration': '775 passed,1 failed,1 deselected; original failure preserved',
        'repaired_integration': '778 passed,1 deselected; captured exit0',
        'new_full406': {'capture': 'checks/premise406.json', 'started_utc': '2026-09-13T02:53:59.265734+00:00', 'duration_seconds': 403.5664156450657, 'returncode': 0, 'timeout': False, 'maxrss_kib': 120192, 'attribution': 'Actual parent capture inspected, not reviewer rerun or historical CSS398 substitute'},
        'final_focused': '489 passed,1 deselected; captured exit0',
    },
    'audit_input_correspondence': {'named_inputs': 15, 'explicit_later_navigation_changes': 7, 'science_guard_test_inputs_unchanged': True, 'whole_program_atomic_snapshot': 'NOT_ATTESTED', 'launch_to_later_input_record_no_change': 'PARENT_ATTRIBUTED'},
    'reviewer_captures': captures,
    'reviewer_captured_wall_seconds_total': sum(c['duration_seconds'] for c in captures),
    'reviewer_maxrss_kib': max(c['maxrss_kib'] for c in captures),
    'reviewer_capture_controls': 'Serialized CPU/one library thread; <=180seconds and2048MiB each.',
    'nine_capture_intervals_independently_recomputed': True,
    'same_context_overlap': False,
    'cross_context_capture_overlaps': meta['observed_cross_context_overlaps'],
    'process_census_limit': 'Captured checks only; administrative/source reads are not a complete process census.',
    'original_scientific_campaign_reruns': 0,
    'full_premise_verifier_reruns_by_reviewer': 0,
    'preservation': {'original_untracked_status_names': 51, 'status_name_sha256': meta['original_untracked_name_status_sha256'], 'protected_payload_bytes_read_or_hashed': False, 'fixed_document_sha256': meta['fixed_document_sha256'], 'index_empty_at_final_metadata_check': True},
    'omissions': ['new scientific reproof or original trajectory campaign', 'interval certification', 'empirical validation or physical-model selection', 'different-model/human/runtime attestation', 'genericity or exhaustive software proof', 'protected payload and backup completeness', 'Stage B/C scientific results', 'subsequent Git staging/commit/push/publication'],
    'input_sha256': hashes,
    'receipt_self_hash': 'Excluded to avoid circularity; caller may hash sealed file.',
}
(V / 'FINAL_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'verdict': receipt['verdict'], 'end_utc': now.isoformat(), 'elapsed_upper_bound_seconds': receipt['elapsed_upper_bound_seconds'], 'final_fidelity_sha256': sha(V / 'FINAL_FIDELITY.md'), 'final_receipt_sha256': sha(V / 'FINAL_RECEIPT.json'), 'reviewed_hash_count': len(hashes), 'amendment': amend_check['verdict']}, indent=2))
