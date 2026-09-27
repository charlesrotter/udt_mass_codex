"""One bounded navigation/preservation check; no scientific computation."""
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BASE = '8aac11e13a2311347771e11f507f4f2042ea02a2'
ARCHIVE = 'archive/remaining_working_surfaces_2026-09-27/'
PACKET = 'udt_repository_cleanup_2026-09-27/'
VS = 'udt_vacuum_common_scale_campaign_2026-09-08/step_01/'
FW = 'udt_gw170817_fixed_window_test_campaign_2026-09-07/'
FORBIDDEN = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
)

# Actual exposure order; ranges describe model-visible intake, not proof review.
SOURCES = [
 ('AGENTS.md', 'full'),
 ('LIVE.md', 'STARTUP_CURRENT block only'),
 ('HANDOFF.md', 'STARTUP_CURRENT block only'),
 ('CURRENT_RESEARCH_PROGRAM.md', 'full bounded orientation'),
 ('CURRENT_SCIENTIFIC_PREMISES.md', 'full bounded orientation'),
 ('CLAUDE.md', 'heading search; lines9-83,121-134'),
 ('.claude/skills/completeness-map/SKILL.md', 'full'),
 ('.claude/skills/verifier-before-record/SKILL.md', 'full'),
 ('INDEX.md', 'full compact navigation'),
 ('MEMORY.md', 'full compact navigation'),
 ('README.md', 'full compact navigation'),
 (PACKET+'README.md', 'full navigation; other review links not followed'),
 ('udt_g374_g375_conditional_banking_2026-09-08/BANKING_RECORD.md', 'full'),
 (FW+'DECISION_BRIEF.md', 'full'),
 ('UDT_METRIC_KERNEL_DEVELOPMENT.md', 'review-name search; lines1-24; requested4550-4620 empty'),
 ('founding.md', 'full requested output truncated; lines1-145 reread; no unshown passage relied on'),
 (PACKET+'REPOSITORY_MAP.md', 'full'),
 (ARCHIVE+'README.md', 'full'),
 ('udt_foundation_alignment_audit_2026-09-27/continuation/DECISION_BRIEF.md', 'full'),
 ('udt_foundation_alignment_audit_2026-09-27/README.md', 'full navigation; other review links not followed'),
 ('udt_foundation_alignment_audit_2026-09-27/continuation/attachment/CANDIDATE.md', 'owner/original/Charles/concept/provenance search hits only'),
 ('udt_foundation_alignment_audit_2026-09-27/candidate/SOURCE_CLAIM_MAP.tsv', 'audit_id and source_paths fields only; no lecture content'),
 ('PROVENANCE.md', 'full; latest Git commit queried'),
 (ARCHIVE+'REORGANIZATION_R0_PREREG_2026-07-18.md', 'lines1-145'),
 (FW+'step_02/review/FINAL_REVIEW.md', 'full original scientific review; no numerical replay'),
 ('udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md', 'G412/FW2/G374/VS1 search; lines1-25,80-111'),
 (PACKET+'archive/ARCHIVE_MANIFEST.tsv', 'header and exact observer-pair filename row; two selected rows for byte check'),
 (VS+'REVIEWED_RESULT.md', 'full'),
 (VS+'review/REVIEW_RECORD.md', 'full original scientific review; no reproof'),
 (ARCHIVE+'UDT_METRIC_KERNEL_OBSERVER_PAIR_FIDELITY_REVIEW_2026-09-05.md', 'lines1-50'),
 ('CURRENT_SCIENTIFIC_PREMISES.tsv', 'G374 and G412 only'),
 ('udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md', 'full 92 lines; requested1-130'),
]

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def digest(data):
    return hashlib.sha256(data).hexdigest()

checks = []
def require(name, condition, detail):
    checks.append({'check':name, 'passed':bool(condition), 'detail':detail})
    if not condition:
        raise AssertionError(name)

require('actual_branch', git('branch','--show-current').decode().strip() == 'grok', 'grok')
require('actual_head', git('rev-parse','HEAD').decode().strip() == BASE, BASE)
tracked = set(git('ls-files','-z').decode().split('\0'))
manifest = list(csv.DictReader((ROOT/PACKET/'archive/ARCHIVE_MANIFEST.tsv').open(), delimiter='\t'))
selected_names = ['REORGANIZATION_R0_PREREG_2026-07-18.md', 'UDT_METRIC_KERNEL_OBSERVER_PAIR_FIDELITY_REVIEW_2026-09-05.md']
for name in selected_names:
    rows = [r for r in manifest if r['source'] == name]
    require('unique_archive_mapping:'+name, len(rows) == 1, len(rows))
    row = rows[0]
    original = git('show', BASE+':'+name)
    archived = (ROOT/row['destination']).read_bytes()
    require('archive_byte_identity:'+name, archived == original, row['destination'])
    require('archive_sha256:'+name, digest(archived) == row['sha256'], digest(archived))
    require('archive_blob_oid:'+name, git('rev-parse',BASE+':'+name).decode().strip() == row['source_blob_oid'], row['source_blob_oid'])
    require('archive_source_pin:'+name, row['source_commit'] == BASE, row['source_commit'])
    require('archive_original_absent:'+name, not (ROOT/name).exists(), 'historical direct root path absent')

for name, expected in [
    (VS+'CANDIDATE_INITIAL.md','13d516978df4cc0de99ef94428efaf1253d9cc4fe8aa07a7e7bf55032b928c9b'),
    (VS+'review/REVIEW_RECORD.md','c287a30178ccb55deea4fab760ee61e76faf1abee73d975231ac3a357369e3c1'),
]:
    require('original_review_pin:'+name, digest((ROOT/name).read_bytes()) == expected, expected)
for name in ['UDT_METRIC_KERNEL_DEVELOPMENT.md','UDT_METRIC_KERNEL_COVERAGE.tsv','PROVENANCE.md','CURRENT_SCIENTIFIC_PREMISES.tsv']:
    require('unchanged_baseline:'+name, (ROOT/name).read_bytes() == git('show',BASE+':'+name), 'exact bytes')

for name in ['PROVENANCE.md','origin_prompts_screenshot_2025-08-12.png','provenance_origin_prompts_2025-08-12.png']:
    require('tracked_provenance:'+name, name in tracked, 'Git metadata only for screenshots; images not opened')

route_tokens = [
 ('INDEX.md',PACKET+'README.md'),
 (PACKET+'README.md','../'+ARCHIVE+'README.md'),
 (PACKET+'README.md','archive/ARCHIVE_MANIFEST.tsv'),
 (ARCHIVE+'README.md','UDT_METRIC_KERNEL_OBSERVER_PAIR_FIDELITY_REVIEW_2026-09-05.md'),
 ('INDEX.md','udt_g374_g375_conditional_banking_2026-09-08/BANKING_RECORD.md'),
 ('INDEX.md',FW+'DECISION_BRIEF.md'),
 ('INDEX.md','udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md'),
 ('INDEX.md','udt_foundation_alignment_audit_2026-09-27/continuation/DECISION_BRIEF.md'),
]
for source, token in route_tokens:
    require('navigation_token:'+source+':'+token, token in (ROOT/source).read_text(), token)

registry = list(csv.DictReader((ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').open(), delimiter='\t'))
selected = {r['premise_id']:r for r in registry if r['premise_id'] in {'G374','G412'}}
require('selected_registry_ids', set(selected) == {'G374','G412'}, sorted(selected))
require('G374_conditional_category', selected['G374']['current_status'] == 'BANKED_DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON', selected['G374']['current_status'])
require('G412_finite_procedure_category', selected['G412']['current_status'] == 'BANKED_REVIEWED_FINITE_PROCEDURE_RESULT__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON', selected['G412']['current_status'])

with (OUT/'SOURCE_EXPOSURE.tsv').open('w') as f:
    writer=csv.writer(f, delimiter='\t', lineterminator='\n')
    writer.writerow(['exposure_sequence','path','read_depth','sha256','bytes','baseline_tracked'])
    for i,(name,depth) in enumerate(SOURCES,1):
        require('outside_protected_prefixes:'+name, not name.startswith(FORBIDDEN), name)
        allowed = name in tracked or name.startswith(PACKET) or name.startswith(ARCHIVE)
        require('authorized_source_path:'+name, allowed, 'tracked text or authorized maintenance artifact')
        data=(ROOT/name).read_bytes()
        writer.writerow([i,name,depth,digest(data),len(data),name in tracked])

# Reproducible exact bounded source excerpts used by the report, not raw arrays/logs.
excerpts = [
 ('INDEX.md',66,81),('INDEX.md',87,117),
 ('udt_g374_g375_conditional_banking_2026-09-08/BANKING_RECORD.md',1,57),
 (VS+'REVIEWED_RESULT.md',1,26),(VS+'review/REVIEW_RECORD.md',1,49),
 (FW+'DECISION_BRIEF.md',1,35),(FW+'step_02/review/FINAL_REVIEW.md',67,119),
 ('udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md',80,104),
 ('PROVENANCE.md',1,41),('PROVENANCE.md',43,84),
 (ARCHIVE+'REORGANIZATION_R0_PREREG_2026-07-18.md',1,18),
 (ARCHIVE+'README.md',1,32),('UDT_METRIC_KERNEL_DEVELOPMENT.md',1,23),
 ('udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md',23,64),
]
with (OUT/'CITED_EXCERPTS.txt').open('w') as f:
    for name,start,end in excerpts:
        lines=(ROOT/name).read_text().splitlines()
        for i in range(start-1,min(end,len(lines))):
            f.write(f'{name}:{i+1}: {lines[i]}\n')
        f.write('\n')

report = {
 'timestamp_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer_context':'/root/cleanup_retrieval_review',
 'source_first_sha256':digest((OUT/'SOURCE_FIRST.md').read_bytes()),
 'head':BASE,
 'scientific_computations_executed':False,
 'source_exposure_count':len(SOURCES),
 'checks_passed':len(checks),
 'checks':checks,
 'known_limit':'Fixed manuscript historical direct hyperlink is dangling; current-pointer exact-filename archive recovery succeeds.',
}
(OUT/'CHECK_RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
