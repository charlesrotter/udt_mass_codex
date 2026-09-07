"""Independent small text/context correspondence check, not scientific proof."""
import hashlib
import json
from pathlib import Path
import subprocess

root=Path.cwd();pkg=root/'udt_recipe_restrictiveness_campaign_2026-09-07'
base='5e022dff9346707563bed18b4ed7dd4150ab2b94'
context={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','CURRENT_SCIENTIFIC_PREMISES.md','INDEX.md','MEMORY.md'}
sha=lambda data:hashlib.sha256(data).hexdigest()
manifest=pkg/'INTEGRATION_TEXT_SHA256SUMS'
assert sha(manifest.read_bytes())=='29ff76893f13070b8a516f2212bd80a3751d892c96ef1c78ea3b9ee2800d3827'
lines=manifest.read_text().splitlines();assert len(lines)==11
for line in lines:
    want,path=line.split(None,1);assert sha((root/path).read_bytes())==want,path
records=[]
for relative in ('step_01/review/STAGE_A_SHA256SUMS','step_02/review/STAGE_A_SHA256SUMS.stdout','step_03/review/source_hashes.stdout'):
    seen=set()
    for line in (pkg/relative).read_text().splitlines():
        want,path=line.split(None,1)
        if path not in context:continue
        seen.add(path)
        out=subprocess.run(['git','-c','core.preloadIndex=false','-c','index.threads=1','show',base+':'+path],capture_output=True,check=True,timeout=15)
        assert sha(out.stdout)==want,(relative,path)
        assert sha((root/path).read_bytes())!=want,('expected refreshed context',path)
    assert seen==context,(relative,seen)
    records.append({'manifest':relative,'baseline_context_hashes_verified':len(seen)})
sizes={p:{'lines':len((root/p).read_text().splitlines()),'words':len((root/p).read_text().split())} for p in sorted(context)}
# The immutable test supplies these exact bounds; this check measures current bytes.
limits={'LIVE.md':(135,900),'HANDOFF.md':(100,600),'CURRENT_RESEARCH_PROGRAM.md':(155,1100),
 'CURRENT_SCIENTIFIC_PREMISES.md':(140,1320),'INDEX.md':(118,570),'MEMORY.md':(70,450)}
for p,(lines_max,words_max) in limits.items():assert sizes[p]['lines']<=lines_max and sizes[p]['words']<=words_max,(p,sizes[p])
test_runs=[]
for name,code,marker in [('startup_integration_tests',1,'947 words'),('startup_integration_tests_bounded',1,'913 words'),('startup_integration_tests_final',0,'193 passed, 1 deselected')]:
    meta=json.loads((pkg/(name+'.json')).read_text());text=(pkg/(name+'.stdout')).read_text()
    assert meta['returncode']==code and not meta['timeout'] and marker in text
    assert (pkg/(name+'.stderr')).read_bytes()==b''
    test_runs.append({'run':name,'exit':code,'duration_seconds':meta['duration_seconds'],'maxrss_kib':meta['maxrss_kib'],'observed_marker':marker})
print(json.dumps({'status':'PASS','current_integration_members':11,'historical_context_correspondence':records,
 'current_surface_sizes':sizes,'retained_regression_runs':test_runs,
 'science_exception':'NONE; all scientific entries are separately checked against actual current bytes by the fully inspected unchanged helper.',
 'full_premise_audit':'MAIN_ONLY_NOT_RERUN','scope':'CORRESPONDENCE_AND_REGRESSION_EVIDENCE_NOT_SCIENCE'},indent=2))
