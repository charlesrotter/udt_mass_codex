"""Proportional final byte/routing correspondence, no scientific reproof."""
import csv
import hashlib
import io
import json
import pathlib
import subprocess

root=pathlib.Path.cwd()
base='9edec2e528e058cbfab11de7a1eff1f90d0cc970'
work='udt_gr_commitment_audit_2026-09-29/'
git=['git','-c','index.threads=1','-c','core.preloadIndex=false',
     '-c','core.packedGitWindowSize=16m','-c','core.packedGitLimit=64m']
def old(p):return subprocess.check_output(git+['show',base+':'+p])
def digest(data):return hashlib.sha256(data).hexdigest()
def sha(p):return digest((root/p).read_bytes())
def rows(data):return list(csv.DictReader(io.StringIO(data.decode()),delimiter='\t'))

freeze=json.loads((root/work/'INTEGRATION_FREEZE.json').read_text())
accepted=freeze['accepted_sha256']
assert len(accepted)==52
assert {p:sha(p) for p in accepted}==accepted
original_freezes={}
for p in ['DIRECT_FREEZE.json','CANDIDATE_FREEZE.json']:
    pins=json.loads((root/work/p).read_text())['sha256']
    assert {q:sha(q) for q in pins}==pins
    original_freezes[p]=len(pins)
launch_pins=json.loads((root/work/'SOURCE_PINS.json').read_text())['sha256']
for p,h in launch_pins.items():
    value=digest(old(p)) if p=='UDT_DEVELOPMENT.md' else sha(p)
    assert value==h,(p,value,h)

gp='development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
go=json.loads(old(gp));gn=json.loads((root/gp).read_text())
assert len(go['sources_sha256'])==70 and len(gn['sources_sha256'])==74
assert all(gn['sources_sha256'][p]==h==sha(p) for p,h in go['sources_sha256'].items())
added_pins=set(gn['sources_sha256'])-set(go['sources_sha256'])
assert len(added_pins)==4 and all(p.startswith(work) for p in added_pins)
assert all(sha(p)==gn['sources_sha256'][p] for p in added_pins)
assert all(e in gn['edges'] for e in go['edges'])
nodes={n['id']:n for n in gn['nodes']}
for c,n in [('C_HOMOTHETY','R10H'),('C_GCA_COMPARISON','R17C'),('C_LOVELOCK','R17L')]:
    assert nodes[c]['kind']=='conditional_class'
    assert c in nodes[n]['required_conditions']
    assert {'from':c,'to':n,'kind':'hypothesis'} in gn['edges']
    assert {'from':n,'to':'R18','kind':'interpretation'} in gn['edges']

registry='CURRENT_SCIENTIFIC_PREMISES.tsv'
assert (root/registry).read_bytes()==old(registry)
assert len(rows((root/registry).read_bytes()))==406
dis='development_reconstruction_2026-09-29/CLAIM_DISPOSITIONS.tsv'
before=rows(old(dis));after=rows((root/dis).read_bytes())
assert len(before)==len(after)==406
changed=[]
for a,b in zip(before,after):
    if a!=b:changed.append(a[next(iter(a))])
    for k in a:
        if 'sha' in k:assert a[k]==b[k],(k,a,b)
assert set(changed)=={'G11','G301','G310','G312'}
recent='development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv'
ro=rows(old(recent));rn=rows((root/recent).read_bytes())
assert len(ro)==27 and len(rn)==28 and rn[:27]==ro
assert rn[-1][next(iter(rn[-1]))]=='GCA1'

central=(root/'UDT_DEVELOPMENT.md').read_text()
insertion=(root/work/'CENTRAL_INSERTION.md').read_text()
one=insertion.split('## After R10, before R11\n\n',1)[1].split('\n## In R17,',1)[0].strip()
two=insertion.split('## In R17, after conservation completion and before finite clock variation\n\n',1)[1].split('\n## R18 addition',1)[0].strip()
three=insertion.split('## R18 addition\n\n',1)[1].strip()
assert all(x in central for x in [one,two,three])

launch=json.loads((root/work/'LAUNCH.json').read_text())
current=set(subprocess.check_output(git+['ls-files','--others','--exclude-standard','-z']).decode().strip('\0').split('\0'))
unrelated={p for p in current if not p.startswith(work)}
assert unrelated==set(launch['unrelated_untracked_names'])
assert len(unrelated)==52
assert subprocess.check_output(git+['rev-parse','HEAD'],text=True).strip()==base
assert subprocess.check_output(git+['branch','--show-current'],text=True).strip()=='grok'

print(json.dumps({'status':'PASS_CORRESPONDENCE_ONLY',
 'integration_freeze_sha256':sha(work+'INTEGRATION_FREEZE.json'),
 'accepted_files':len(accepted),'original_freezes_verified':original_freezes,
 'launch_pins_verified':len(launch_pins),'old_graph_pins_unchanged':70,
 'new_graph_pins':sorted(added_pins),'old_edges_preserved':len(go['edges']),
 'conditional_nodes_checked':['R10H','R17C','R17L'],
 'actual_registry_rows_unchanged':406,'editorial_dispositions_changed':changed,
 'old_recent_rows_unchanged':27,'new_recent_row':'GCA1',
 'exact_insertions_present':3,'unrelated_names_preserved':len(unrelated),
 'protected_payloads':'Names only; no payload hash/content read',
 'work_record_sha256_at_review':sha(work+'WORK_RECORD.md'),
 'scope':'Byte/routing preservation and actual integration correspondence, not predecessor scientific reproof'},indent=2))
