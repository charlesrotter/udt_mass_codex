"""Seal this review's finite report, claim dispositions and actual capture receipts."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
ROOT = PKG.parent
sha = lambda b: hashlib.sha256(b).hexdigest()
claims = json.loads((PKG / 'BANKED_CLAIMS.json').read_text())['claims']
with (HERE / 'CLAIM_FIDELITY.tsv').open('x', newline='') as f:
    fields = ['premise_id', 'original_result', 'fidelity_disposition', 'category',
              'required_registry_ids', 'statement_sha256', 'assessment_path', 'assessment_sha256',
              'scope_owner', 'qualification']
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    w.writeheader()
    for c in claims:
        w.writerow(dict(premise_id=c['premise_id'], original_result=c['id'],
            fidelity_disposition='VERIFIED_WITH_CAVEATS_EXACT_INTEGRATION_FIDELITY',
            category=c['grade'], required_registry_ids=','.join(c['required_registry_ids']),
            statement_sha256=sha(c['statement'].encode()),
            assessment_path=c['banking_assessment_path'],
            assessment_sha256=sha((ROOT / c['banking_assessment_path']).read_bytes()),
            scope_owner='ENTIRE original pinned candidate/review/repair and BANKED_CLAIMS scope',
            qualification='Parent final full395/status/preservation/publication gates pending; not new scientific proof/adoption/canon'))

captures = {}
for stem in ('integrity_01', 'git_status_failure_diagnostic', 'integrity_02',
             'integrity_03', 'targeted_pytest_01', 'adversarial_01'):
    record = json.loads((HERE / (stem + '.json')).read_text())
    record['stdout_sha256'] = sha((HERE / (stem + '.stdout')).read_bytes())
    record['stderr_sha256'] = sha((HERE / (stem + '.stderr')).read_bytes())
    record['capture_provenance_sha256'] = sha((HERE / (stem + '.capture_provenance.json')).read_bytes())
    captures[stem] = record
receipt = {
    'reviewer': '/root/banking_integration_review',
    'runtime_model_version': 'UNATTESTED',
    'fresh_context': True, 'source_exposed': True,
    'different_model': 'UNTESTED', 'independent_scientific_reproof': False,
    'independent_correspondence_mutation_AST_implementation': True,
    'first_observed_utc': '2026-09-11T00:28:33Z',
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python': sys.version, 'argv': sys.argv,
    'verdict': 'VERIFIED_WITH_CAVEATS_EXACT_INTEGRATION_FIDELITY',
    'unresolved_scientific_or_transcription_objections': [],
    'parent_pending_gates': ['final full395 audit', 'navigation guard repair/short regression',
                             'final acceptance record/pins', 'preservation and publication'],
    'captures': captures,
    'report_sha256': sha((HERE / 'REVIEW_REPORT.md').read_bytes()),
    'per_claim_dispositions_sha256': sha((HERE / 'CLAIM_FIDELITY.tsv').read_bytes()),
    'reviewed_snapshot': json.loads((HERE / 'integrity_03.stdout').read_text())['integration_snapshot_sha256'],
}
with (HERE / 'REVIEW_RECEIPT.json').open('x') as f:
    json.dump(receipt, f, indent=2)
    f.write('\n')
with (HERE / 'SHA256SUMS').open('x') as f:
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.name != 'SHA256SUMS':
            f.write(sha(p.read_bytes()) + '  ' + str(p.relative_to(ROOT)) + '\n')
print(json.dumps({'completed_utc': receipt['completed_utc'], 'verdict': receipt['verdict'],
                  'claim_count': len(claims), 'report_sha256': receipt['report_sha256']}, indent=2))
