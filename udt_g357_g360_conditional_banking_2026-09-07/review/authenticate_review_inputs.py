"""Read-only correspondence checks for banking fidelity; no scientific proof."""
import hashlib
import json
import pathlib
import subprocess

repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
scratch = pathlib.Path('/tmp/udt-sc-banking-fidelity-pHLUdApB')
baseline = 'ed2f7432f068aa7a72628382b890596b3efba06a'
campaign = 'udt_shared_readout_metric_constraint_campaign_2026-09-06'
banking = 'udt_g357_g360_conditional_banking_2026-09-07'

def digest(data):
    return hashlib.sha256(data).hexdigest()

manifest_path = repo / campaign / 'ARTIFACT_SHA256SUMS'
manifest = manifest_path.read_text().splitlines()
payloads = []
for line in manifest:
    expected, rel = line.split('  ', 1)
    assert digest((repo / rel).read_bytes()) == expected, rel
    payloads.append(rel)
tracked = subprocess.check_output(['git', 'ls-files', '-z', '--', campaign], cwd=repo).decode().split('\0')[:-1]
assert set(tracked) == set(payloads) | {f'{campaign}/ARTIFACT_SHA256SUMS'}
assert subprocess.run(['git', 'diff', '--quiet', baseline, '--', campaign], cwd=repo).returncode == 0
assert digest(manifest_path.read_bytes()) == '32daf9c0b69ec4107b310f9275a6bc1e2b674f7c40fb456811f0f6d122a26cfe'

sources = [f'{campaign}/step_01/CANDIDATE_ARGUMENT.md']
for step in range(2, 6):
    folder = f'{campaign}/step_{step:02d}'
    sources += [f'{folder}/{name}' for name in ('QUESTION.md', 'CANDIDATE_ARGUMENT.md', 'REVIEW_RECORD.md')]
    report = 'STAGE_B_ADVERSARIAL_REVIEW.md' if step == 4 else 'PHASE_B_ADVERSARIAL_REVIEW.md'
    sources += [f'{folder}/review/{report}']
sources += [
    f'{campaign}/step_05/repair/REPAIR_RECORD.md',
    f'{campaign}/step_05/repair/review/FOCUSED_REVIEW.md',
    f'{campaign}/step_05/repair/check_exact.py',
    f'{campaign}/step_05/check_exact.py',
    f'{campaign}/DECISION_BRIEF.md',
    'udt_g353_g356_conditional_banking_2026-09-06/BANKING_RECORD.md',
    'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/CANDIDATE_ARGUMENT.md',
    'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/CANDIDATE_ARGUMENT.md',
    'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/AUDIT_REPORT.md',
    'udt_g332_weighted_contact_vacuum_constraint_embedding_2026-09-03/AUDIT_REPORT.md',
    'udt_g335_local_pair_response_persistence_2026-09-03/AUDIT_REPORT.md',
]
source_hashes = {}
for rel in sources:
    data = (repo / rel).read_bytes()
    pinned = subprocess.check_output(['git', 'show', f'{baseline}:{rel}'], cwd=repo)
    assert data == pinned, rel
    source_hashes[rel] = digest(data)

correspondence = {}
for actual, frozen in (
    ('sc5_original_false_pass', 'step_05/review/false_pass_overreject.stdout'),
    ('sc5_repaired_baseline', 'step_05/repair/author_exact.stdout'),
    ('sc5_original_corruption_repaired', 'step_05/repair/review/original_false_pass_reapplied.stdout'),
):
    observed = (scratch / f'{actual}.stdout').read_bytes()
    assert observed == (repo / campaign / frozen).read_bytes(), actual
    result = json.loads(observed)
    correspondence[actual] = {
        'byte_identical_to': f'{campaign}/{frozen}',
        'status': result['status'],
        'assertions': result.get('assertions'),
        'first_guard': result.get('guard'),
        'returncode': json.loads((scratch / f'{actual}.json').read_text())['returncode'],
    }

new_documents = {}
for name in ('BANKING_RECORD.md', 'WORK_ORDER.md', 'NEXT_CAMPAIGN_PROPOSAL.md'):
    rel = f'{banking}/{name}'
    data = (repo / rel).read_bytes()
    new_documents[rel] = {'sha256': digest(data), 'text': data.decode()}

print(json.dumps({
    'baseline': baseline,
    'source_manifest_payloads': len(payloads),
    'source_tracked_files': len(tracked),
    'source_campaign_matches_pinned_manifest_and_git': True,
    'reviewed_scientific_source_hashes': source_hashes,
    'sc5_focused_replay_correspondence': correspondence,
    'new_documents_for_fidelity_review': new_documents,
    'evidence_type': 'source authentication and bounded same-code replay correspondence, not proof or adoption',
}, indent=2))
