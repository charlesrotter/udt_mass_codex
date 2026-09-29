"""Exact integration correspondence, source preservation and bounded routing audit."""
import csv
import datetime
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

root=Path.cwd()
here=Path(__file__).resolve().parent
package=root/'udt_gr_commitment_audit_2026-09-29'
baseline='9edec2e528e058cbfab11de7a1eff1f90d0cc970'
def git(*a):
    return subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1',*a])
def old(p):return git('show',baseline+':'+p)
def sha(data):return hashlib.sha256(data).hexdigest()
def load_tsv(b):return list(csv.DictReader(io.StringIO(b.decode()),delimiter='\t'))

freeze_path=package/'INTEGRATION_FREEZE.json'
accepted=json.loads(freeze_path.read_text())['accepted_sha256']
assert len(accepted)==52
for p,h in accepted.items():assert sha((root/p).read_bytes())==h,p

versioned_freezes={}
for p,key in [(package/'CANDIDATE_FREEZE.json','sha256'),
              (package/'DIRECT_FREEZE.json','sha256'),
              (here/'SOURCE_FIRST_SEAL.json','files')]:
    pins=json.loads(p.read_text())[key]
    assert all(sha((root/n).read_bytes())==h for n,h in pins.items()),str(p)
    versioned_freezes[str(p.relative_to(root))]={'sha256':sha(p.read_bytes()),'entry_count':len(pins)}
source_launch=json.loads((package/'SOURCE_PINS.json').read_text())['sha256']
for p,h in source_launch.items():
    data=old(p) if p=='UDT_DEVELOPMENT.md' else (root/p).read_bytes()
    assert sha(data)==h,p

graph_path='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
before=json.loads(old(graph_path));after=json.loads((root/graph_path).read_text())
assert len(before['sources_sha256'])==70
assert all(after['sources_sha256'].get(p)==h for p,h in before['sources_sha256'].items())
assert len(after['sources_sha256'])==74
assert all(sha((root/p).read_bytes())==h for p,h in after['sources_sha256'].items())
assert all(e in after['edges'] for e in before['edges'])
assert all(r in after['review_support'] for r in before['review_support'])
new_nodes={n['id']:n for n in after['nodes'] if n['id'] not in {m['id'] for m in before['nodes']}}
assert set(new_nodes)=={'C_HOMOTHETY','C_GCA_COMPARISON','C_LOVELOCK','R10H','R17C','R17L'}
for condition,result in [('C_HOMOTHETY','R10H'),('C_GCA_COMPARISON','R17C'),('C_LOVELOCK','R17L')]:
    assert condition in new_nodes[result]['required_conditions']
    assert {'from':condition,'to':result,'kind':'hypothesis'} in after['edges']
sys.path.insert(0,str(root))
import verify_udt_development as verifier
affected=verifier.affected_nodes(after,['udt_gr_commitment_audit_2026-09-29/INITIAL_CANDIDATE.md'])
assert {'R10','R10H','R11','R12','R17','R17C','R17L','R18'}<=set(affected)

registry_path='CURRENT_SCIENTIFIC_PREMISES.tsv'
assert (root/registry_path).read_bytes()==old(registry_path)
assert len(load_tsv((root/registry_path).read_bytes()))==406
disp_path='development_reconstruction_2026-09-29/CLAIM_DISPOSITIONS.tsv'
disp_old=load_tsv(old(disp_path));disp_new=load_tsv((root/disp_path).read_bytes())
assert len(disp_old)==len(disp_new)==406
changed=[(a,b) for a,b in zip(disp_old,disp_new) if a!=b]
ids=[next(iter(a.values())) for a,b in changed]
assert set(ids)=={'G11','G301','G310','G312'}
rowhash_field=[k for k in disp_old[0] if 'sha256' in k][0]
assert all(a[rowhash_field]==b[rowhash_field] for a,b in zip(disp_old,disp_new))
recent_path='development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'
recent_before=old(recent_path);recent_after=(root/recent_path).read_bytes()
assert recent_after.startswith(recent_before)
assert len(load_tsv(recent_before))==27 and len(load_tsv(recent_after))==28

central=(root/'UDT_DEVELOPMENT.md').read_text()
insertion=(package/'CENTRAL_INSERTION.md').read_text()
headings=['## After R10, before R11','## In R17, after conservation completion and before finite clock variation','## R18 addition']
blocks=[]
for i,h in enumerate(headings):
    block=insertion.split(h+'\n\n',1)[1]
    if i+1<len(headings):block=block.split(headings[i+1],1)[0]
    block=block.strip()
    assert central.count(block)==1,h
    blocks.append({'heading':h,'sha256':sha(block.encode())})
assert (root/'CURRENT_RESEARCH_PROGRAM.md').read_text()==verifier.program_text(central)

launch=json.loads((package/'LAUNCH.json').read_text())
untracked=set(git('ls-files','--others','--exclude-standard','-z').decode().split('\0'))-{''}
assert len(launch['unrelated_untracked_names'])==52
assert set(launch['unrelated_untracked_names'])<=untracked
assert (package/'PREVIOUS_REVIEW_RECORD.json').read_bytes()==old('development_reconstruction_2026-09-29/REVIEW_RECORD.json')
unchanged_accepted=[]
for p in accepted:
    if p.startswith('udt_gr_commitment_audit_2026-09-29/'):continue
    if (root/p).read_bytes()==old(p):unchanged_accepted.append(p)

result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'baseline':baseline,'head':git('rev-parse','HEAD').decode().strip(),
        'branch':git('branch','--show-current').decode().strip(),
        'freeze_sha256':sha(freeze_path.read_bytes()),'accepted_files':52,
        'frozen_inputs':versioned_freezes,'launch_pins':len(source_launch),
        'graph_original_pins_preserved':70,'graph_added_pins':4,
        'graph_no_old_edges_or_review_support_removed':True,
        'new_node_ids':sorted(new_nodes),'affected_nodes':affected,
        'registry_byte_identical_rows':406,'editorial_dispositions_changed':ids,
        'all_disposition_registry_row_hashes_retained':True,
        'old_recent_rows_unchanged':27,'new_recent_rows':28,
        'exact_central_insertion_blocks':blocks,'generated_orientation_matches':True,
        'unrelated_untracked_names_preserved':52,'protected_payload_read_or_hash':False,
        'previous_review_record_byte_identical_to_baseline':True,
        'accepted_files_identical_to_baseline':unchanged_accepted,
        'work_record_inspected_sha256':sha((package/'WORK_RECORD.md').read_bytes()),
        'scope':'Correspondence and bounded routing, not scientific acceptance, semantic completeness or a full406 rerun'}
assert result['head']==baseline and result['branch']=='grok'
with (here/'FINAL_CORRESPONDENCE_RESULTS.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,sort_keys=True,indent=2))
