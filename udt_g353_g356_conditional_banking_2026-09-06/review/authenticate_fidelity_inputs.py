"""Read-only byte authentication for a bounded documentation fidelity review."""
import hashlib
import json
import pathlib
import subprocess

repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
snapshot = 'c92588ad31f3fd79868378e6e3a318af2de1235f'
campaign = 'udt_g351_g352_content_bridge_campaign_2026-09-06'
sources = [f'{campaign}/step_{i:02d}/{name}' for i in range(1, 5)
           for name in ('CANDIDATE_ARGUMENT.md', 'REVIEW_RECORD.md',
                        'review/STAGE_B_ADVERSARIAL_REVIEW.md')]
sources += [f'{campaign}/DECISION_BRIEF.md', f'{campaign}/ARTIFACT_SHA256SUMS']
sources += [
    'udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md',
    'udt_g352_clock_rate_carried_measure_readout_2026-09-05/EXACT_DERIVATION.md',
    'udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md',
    'udt_g349_finite_null_wavefront_patch_area_2026-09-04/AUDIT_REPORT.md',
    'udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/AUDIT_REPORT.md',
    'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/AUDIT_REPORT.md',
    'udt_g322_g321_maximal_globally_hyperbolic_development_2026-09-01/AUDIT_REPORT.md',
    'udt_g335_local_pair_response_persistence_2026-09-03/AUDIT_REPORT.md',
    'udt_g337_double_silent_third_normal_ownership_2026-09-03/AUDIT_REPORT.md',
]
candidates = {
    'udt_g353_g356_conditional_banking_2026-09-06/BANKING_RECORD.md':
        '871a817662842e6dba2094b7d5b8ac215ee2000cc2d05ac7d8d0755444617540',
    'udt_g353_g356_conditional_banking_2026-09-06/NEXT_CAMPAIGN_DECISION_BRIEF.md':
        'fbb9376559ea4b96edc7367b09863d6838f33012e1147b9efb0ffd305909a6e6',
}
records = []
for path in sources:
    frozen = subprocess.run(['git', 'show', snapshot + ':' + path], cwd=repo,
                            check=True, capture_output=True).stdout
    live = (repo / path).read_bytes()
    assert live == frozen, ('source changed', path)
    records.append(dict(path=path, bytes=len(live), sha256=hashlib.sha256(live).hexdigest(),
                        equals_snapshot=True))
drafts = []
for path, expected in candidates.items():
    data = (repo / path).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert actual == expected, ('candidate changed', path, actual)
    drafts.append(dict(path=path, bytes=len(data), sha256=actual, equals_initial_pin=True))
metadata = {}
for name, cmd in [('head', ['git', 'rev-parse', 'HEAD']),
                  ('branch', ['git', 'branch', '--show-current'])]:
    metadata[name] = subprocess.run(cmd, cwd=repo, check=True, capture_output=True,
                                    text=True).stdout.strip()
assert metadata['head'] == snapshot
assert metadata['branch'] == 'grok'
print(json.dumps(dict(verdict='PASS_BYTE_CORRESPONDENCE_ONLY', snapshot=snapshot,
                     metadata=metadata, sources=records, candidates=drafts,
                     science_recomputed=False, full_premise_audit_run=False), indent=2))
