"""Seal an already completed documentary fidelity judgment and exact byte checks."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

repo = Path('/home/udt-admin/udt_mass_codex')
package = repo / 'udt_optical_instrument_eligibility_2026-09-12'
review = package / 'review'
baseline = 'e89bfe9c6c404e1a70aa334e660ae46327f266ab'
roots = ['CURRENT_RESEARCH_PROGRAM.md', 'HANDOFF.md', 'INDEX.md',
         'LIVE.md', 'UDT_RESEARCH_ROADMAP.md']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo).decode()

source_pins = json.loads((package/'SOURCE_PINS.json').read_text())['pins']
initial_pins = json.loads((package/'INITIAL_REVIEW_FREEZE.json').read_text())['pins']
source_first = json.loads((review/'SOURCE_FIRST_SEAL.json').read_text())
source = json.loads((package/'sources/SOURCE_RECORD.json').read_text())
integration = json.loads((package/'checks/final_integration.stdout').read_text())
navigation = json.loads((package/'checks/final_navigation.json').read_text())
integration_receipt = json.loads((package/'checks/final_integration.json').read_text())
groups = {}
for name, root, pins in [
    ('scientific_source_pins', repo, source_pins),
    ('initial_nine_pins', package, initial_pins),
    ('source_first_seal_pins', review, source_first['pins']),
    ('parent_final_root_correspondence', repo, integration['root_sha256']),
]:
    groups[name] = {p: {'expected': h, 'actual': sha(root/p)} for p,h in pins.items()}
groups['source_cache'] = {
    field: {'expected': source[hfield], 'actual': sha(Path(source[field]))}
    for field,hfield in [('local_temporary_pdf','pdf_sha256'),
                         ('text_cache','text_sha256'),
                         ('rendered_page2','render_sha256')]
}
groups['initial_review_and_repair'] = {
    p: {'expected': h, 'actual': sha(review/p)} for p,h in {
        'REVIEW.md': '36f8c0a02a615782bb622627f250a61360b2640689f9809eaf31d89704a375ae',
        'REPAIR_REVIEW.md': '4c174f64c60eead61dcc2500b626a6309deaefd89ef40439087c7bcad09d39ea',
    }.items()
}
status = git('status','--short')
original = [line for line in status.splitlines()
            if line.startswith('?? ') and line != '?? '+package.name+'/']
fingerprint = hashlib.sha256(('\n'.join(original)+'\n').encode()).hexdigest()
changed = git('diff','--name-only',baseline,'--').splitlines()
branch = git('branch','--show-current').strip()
head,origin = git('rev-parse','HEAD','origin/grok').splitlines()
diff_check = subprocess.run(['git','diff','--check'],cwd=repo,capture_output=True)
checks_pass = (
    branch == 'grok' and head == origin == baseline
    and sorted(changed) == roots
    and len(original) == 46
    and fingerprint == '55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
    and all(r['expected'] == r['actual'] for group in groups.values() for r in group.values())
    and navigation['returncode'] == integration_receipt['returncode'] == diff_check.returncode == 0
    and integration['pass'] is True
    and '359 passed, 1 deselected' in (package/'checks/final_navigation.stdout').read_text()
    and not (package/'checks/final_navigation.stderr').read_bytes()
    and not (package/'checks/final_integration.stderr').read_bytes()
)
package_paths = list(initial_pins) + [
    'INITIAL_REVIEW_FREEZE.json', 'SOURCE_PRESERVING_CLARIFICATION.md',
    'REVIEWED_ASSESSMENT.md', 'DECISION_BRIEF.md', 'SESSION_RECORD.md', 'CLOSEOUT.md',
    'review/SOURCE_FIRST_JUDGMENT.md', 'review/SOURCE_FIRST_SEAL.json',
    'review/REVIEW.md', 'review/REPAIR_REVIEW.md',
    'review/check_source_correspondence.py', 'review/seal_final_fidelity.py',
    'checks/check_integration.py',
]
for stem in ['review/source_correspondence','review/source_first_seal_capture',
             'checks/final_navigation','checks/final_integration']:
    package_paths.extend(stem+suffix for suffix in
                         ['.json','.stdout','.stderr','.capture_provenance.json'])
now = datetime.now(timezone.utc).isoformat()
result = {
    'sealed_utc': now,
    'reviewer_context': '/root/ob2_instrument_review',
    'observed_active_interval': {
        'first_actual_clock_utc': '2026-09-12T14:46:32+00:00',
        'last_observed_at_seal_utc': now,
        'meaning': 'Observed interval, not a claimed exact process lifetime or uninterrupted compute interval',
    },
    'source_first_sealed_utc': source_first['sealed_utc'],
    'direct_review_saved_by_observed_utc': '2026-09-12T14:54:02+00:00',
    'repair_document_read_complete_observed_utc': '2026-09-12T14:55:50+00:00',
    'verdict': 'FIDELITY_REVIEWED; source-bounded documentary finding VERIFIED-WITH-CAVEATS; UNPROMOTED',
    'maximum_conclusion': 'Full OB1 eligibility is not established by this exact selected report; no physical impossibility or apparatus-wide rejection',
    'D1': 'CLOSED by source-preserving clarification; exact-spacing/valid-error-treatment exceptions restored and absolute-delay identification separated from alias-invariant prediction',
    'remaining_objections': [],
    'device_evidence_gates': 'Signed three-optical-frequency records, justified transfer/independent response calibration/applicable errors and unused-confirmation provenance remain undocumented here; Use A additionally needs independent geometry-delay support',
    'allocation': {
        'new_reviewer_contexts': 1,
        'parent_overlap': 'Parent performed documentary closeout/navigation while this actual reviewer context was active',
        'subdelegation': False,
        'old_context_reuse': False,
        'model_override': False,
        'general_capacity': 'UNVERIFIED; this successful allocation establishes only this instance',
    },
    'independence': {
        'context': 'Fresh separately allocated; included repair/final followup in same context',
        'runtime_model_version': 'UNATTESTED',
        'parent_configuration_attributed': 'gpt-6-astra/xhigh',
        'different_model': 'UNTESTED',
        'argument': 'Sealed source-first paper/contract assessment before OB2 author verdict; direct adversarial check and elementary independent measurement/error reasoning',
        'scientific_implementation': 'Not computational; no new scientific script or documentary checklist test',
        'metadata_implementation': 'Independently written correspondence/seal scripts; reused existing capture utility',
        'human_specialist': 'UNTESTED',
        'formal_proof': 'UNTESTED',
    },
    'exposure': {
        'source_first': 'Full OB1 conditional candidate/result/clarification/substantive prior review; full selected paper text and both rendered pages/Figs1-4; permitted framing/source records',
        'after_source_first_seal': 'OB2 initial assessment/fact ledger/selection narrative; then parent decision/session/closeout and repair',
        'data': 'Published plots/text exposed as documentary evidence; no digitization, extraction, fit, statistical reanalysis or reserved target data',
        'sources': 'Exactly one selected apparatus report; no other instrument full text or target dataset',
    },
    'final_fidelity_reads': [
        'Complete repaired assessment, clarification, decision brief, final session record and closeout',
        'Complete five-root git diff and exact parent navigation/integration stdout, stderr, JSON and wrapper provenance',
        'Integration metadata-check implementation; same-session full397 receipt/stdout/stderr',
    ],
    'source_and_preservation_check': {
        'correspondence_pass': checks_pass,
        'branch': branch, 'head': head, 'origin_grok': origin,
        'changed_tracked_paths': changed,
        'original_untracked_name_status_count': len(original),
        'original_untracked_name_status_sha256': fingerprint,
        'groups': groups,
        'git_diff_check_exit': diff_check.returncode,
        'protected_payload_read_or_hash': False,
        'backup_completeness': 'UNVERIFIED',
        'hash_limit': 'Byte correspondence only; not truth, chronology, protected-payload integrity or archival completeness',
    },
    'reused_actual_checks': {
        'navigation': navigation,
        'navigation_scope': '359 passed, 1 deselected; parent execution inspected, not reviewer replay or scientific proof',
        'integration': integration_receipt,
        'same_session_full397': {
            'attributed_path': 'udt_optics_bridge_assessment_2026-09-12/checks/closeout_full397.json',
            'started_utc': '2026-09-12T14:04:07.374205+00:00',
            'duration_seconds': 402.80235642998014,
            'returncode': 0,
            'reviewer_rerun': False,
            'attribution_basis': 'Actual receipt/stdout/stderr inspected; source/registry/premise/AGENTS pins unchanged',
        },
        'fetch': 'Parent-attributed actual success before integration; the integration script records that assertion and does not itself execute fetch; reviewer checked local refs only',
    },
    'root_sha256': {p: sha(repo/p) for p in roots},
    'final_package_sha256': {p: sha(package/p) for p in package_paths},
    'additional_source_sha256': {'tests/test_startup_surface.py': sha(repo/'tests/test_startup_surface.py')},
    'publication': 'NOT_CLAIMED; subsequent parent-owned manifest/staging/sync/commit/push metadata is outside this prepublication fidelity seal',
    'omissions': 'No full397 or OB1 scientific replay, Maxwell/guide solve, finite-wave certification, hardware test, statistical analysis, new transfer, target data, survey, contact, protected/archive payload access, runtime change, GPU production, source edits, commit, physical adoption, promotion or successor dispatch',
}
if not checks_pass:
    print(json.dumps(result,indent=2))
    raise SystemExit('Final correspondence failed; no fidelity seal written')
with (review/'FINAL_FIDELITY.json').open('x') as stream:
    json.dump(result,stream,indent=2)
    stream.write('\n')
print(json.dumps({'sealed_utc':now,'verdict':result['verdict'],
                  'correspondence_pass':checks_pass,
                  'fidelity_sha256':sha(review/'FINAL_FIDELITY.json')},indent=2))
