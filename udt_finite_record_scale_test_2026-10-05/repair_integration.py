"""Preserve and repair display rounding and review-method wording only."""
from pathlib import Path
import json,hashlib
B=Path('udt_finite_record_scale_test_2026-10-05');W=Path('development_reconstruction_2026-09-29');R=B/'integration_repair'
R.mkdir(exist_ok=False)
files={'UDT_DEVELOPMENT.md':Path('UDT_DEVELOPMENT.md'),'CENTRAL_INSERT.md':B/'CENTRAL_INSERT.md','WORK_RECORD.md':B/'WORK_RECORD.md','DEVELOPMENT_GRAPH.json':W/'DEVELOPMENT_GRAPH.json','INTEGRATION_FREEZE.json':B/'INTEGRATION_FREEZE.json'}
for name,p in files.items():
    with (R/name).open('xb') as f:f.write(p.read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
original={str(p):sha(p) for p in files.values()}
with (R/'ORIGINAL_BINDINGS.json').open('x') as f:json.dump(original,f,indent=2);f.write('\n')
for p in [Path('UDT_DEVELOPMENT.md'),B/'CENTRAL_INSERT.md']:
    s=p.read_text()
    for a,b in [('[.0049725836,.0050676842]','[.0049725835,.0050676842]'),('[.0049722999,.0050673991]','[.0049722998,.0050673991]')]:
        assert s.count(a)==1,a;s=s.replace(a,b)
    p.write_text(s)
p=B/'WORK_RECORD.md';s=p.read_text();assert 'Exposed replay solved\nall25 saved states' in s
s=s.replace('Exposed replay solved\nall25 saved states','Exposed replay recomputed\nall25 saved states')
s=s.replace('Window certificates, both long intervals, short interval and angular margin\nwere independently recomputed.', 'These25 exposed cases used saved states with independently evaluated original\nincidence and proper-time residuals/readouts; they were not new root solves.\nThe36 source-first cases supplied the independent root solving. Window\ncertificates, both long intervals, short interval and angular margin were\nindependently recomputed.')
p.write_text(s)
record='''# Final integration display/provenance repair

Both actual final reviewers identified reporting defects after the first
integration freeze. The initial freeze and changed files are preserved here.
Its SHA was de498e1e31889f453e4e048499778aa002e4b4d053e97947ca6a9ff586a11321.

1. Displayed central lower endpoints rounded inward. They now round outward
to .0049725835 and .0049722998; upper endpoints were already outward. The exact
saved outputs and enclosing formula are unchanged. No actual numerical
certification precision is strengthened by this presentation correction.
2. WORK_RECORD said the math review solved25 saved cases; it recomputed their
readouts and independently integrated original-equation residuals using saved
states. Its36 source-first cases performed independent root solves. The two
corruption controls demonstrate nonvacuity. Fidelity separately re-solved25
centers. The exact same checks remain evidence, with accurate independence.

No candidate, equations, source grade, confirmation outcome, tolerance or
physical premise changed. Graph review_support is refreshed only for this
actually reviewed wording repair and adds this explicit history. Maintenance
is repeated on repaired bytes. Both actual contexts must review the repair and
verify the new exact map before attestations; no automatic hash acceptance.
'''
(R/'REPAIR_RECORD.md').write_text(record)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());targets=None
for q in g['review_support']:
    if q['path']==str(B/'WORK_RECORD.md'):q['sha256']=sha(B/'WORK_RECORD.md');targets=q['targets']
assert targets
g['review_support'].append({'path':str(R/'REPAIR_RECORD.md'),'sha256':sha(R/'REPAIR_RECORD.md'),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
# The old current freeze and old maintenance receipts are retained by rename;
# no destructive removal and no overwritten historical receipt.
(B/'INTEGRATION_FREEZE.json').rename(R/'ORIGINAL_FREEZE_FILE.json')
for ext in ['json','stdout','stderr']:(B/('checks/final_maintenance.'+ext)).rename(R/('final_maintenance.'+ext))
print(json.dumps({'status':'DISPLAY_AND_PROVENANCE_REPAIR','preserved_files':list(files),'candidate_and_science_unchanged':True}))
