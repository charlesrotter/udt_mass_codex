"""Record an actual completed review judgment; this does not perform review."""
import datetime
import hashlib
import json
from pathlib import Path

package = Path('udt_clock_optical_physical_connection_2026-10-13')
directory = package/'review_math'
freeze_path = package/'INTEGRATION_FREEZE.json'
freeze_bytes = freeze_path.read_bytes()
assert hashlib.sha256(freeze_bytes).hexdigest() == '2268d07448fdd18ca616396109380698838b6e00257a394b7c9fa29a8c2a2fb9'
freeze = json.loads(freeze_bytes)
correspondence = json.loads((directory/'final_correspondence_01.stdout').read_text())
assert correspondence['status'] == 'PASS'
assert correspondence['accepted_files_checked'] == len(freeze['accepted_sha256'])
assert not correspondence['accepted_map_mismatches']
report = directory/'FINAL_REVIEW.md'
attestation = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'context': '/root/coc_review_math',
    'verdict': 'ACCEPT_WITH_LIMITS',
    'report_path': str(report),
    'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
    'freeze_path': str(freeze_path),
    'freeze_sha256': correspondence['freeze_sha256'],
    'review_scope': 'Actual source-first/direct/repair/final exposed mathematical integration review; unchanged prior corpus inherits its prior review, not a fresh reproof.',
    'independence': {
        'context': 'fresh separate context at source-first stage; subsequently exposed',
        'model': 'same inherited model; exact model identifier not separately exposed',
        'argument': 'independent source-first normal-coordinate/Jacobi derivation and boost analysis; direct adversarial source review afterward',
        'implementation': 'independent original-geodesic/incidence/induced-area dS2 x R2 control and exact accelerated-flat control; shared Python/SymPy library',
        'not_claimed': ['different-model review', 'human review', 'formal proof', 'empirical validation', 'whole-corpus reproof'],
    },
    'pending_external_gates': ['normal development guard after binding', '57 maintenance tests after binding', 'full406 premise audit after binding', 'staged and committed correspondence', 'publication and remote correspondence'],
    'accepted_sha256': freeze['accepted_sha256'],
}
destination = directory/'FINAL_ATTESTATION.json'
with destination.open('x') as handle:
    json.dump(attestation, handle, indent=2)
    handle.write('\n')
print(json.dumps({'attestation': str(destination),
                  'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
                  'report_sha256': attestation['report_sha256'],
                  'accepted_files': len(attestation['accepted_sha256']),
                  'verdict': attestation['verdict']}))
