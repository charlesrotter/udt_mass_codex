"""Version/routing correspondence, not scientific certification."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as v
P=Path('udt_physical_connection_whiteboard_2026-09-30')
H=lambda b:hashlib.sha256(b).hexdigest()
freeze=json.loads((P/'INTEGRATION_FREEZE.json').read_text())
for p,h in freeze['accepted_sha256'].items():
    assert H(Path(p).read_bytes())==h,p
candidate=json.loads((P/'CANDIDATE_FREEZE.json').read_text())
for p,h in candidate['sha256'].items():
    assert H(Path(p).read_bytes())==h,p
master=Path('UDT_DEVELOPMENT.md').read_text()
assert Path('CURRENT_RESEARCH_PROGRAM.md').read_text()==v.program_text(master)
graph=json.loads(Path('development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
node=next(n for n in graph['nodes'] if n['id']=='O_PCW_PROPOSALS')
assert node['kind']=='open_join' and not node['registry_ids']
out=[e for e in graph['edges'] if e['from']=='O_PCW_PROPOSALS']
assert out==[{'from':'O_PCW_PROPOSALS','to':'R18','kind':'open_boundary'}]
assert v.affected_nodes(graph,[str(P/'REPAIR.md')])==['O_PCW_PROPOSALS','R18']
# Reconstruct the intermediate central version in memory from the actual
# launch commit and the one-hunk saved patch, checking every context line.
base=subprocess.check_output(['git','show','ef00adf90d0389711289e4baed38bf00a047fd6d:UDT_DEVELOPMENT.md'])
pins=json.loads((P/'START_SOURCE_PINS.json').read_text())
assert H(base)==pins['UDT_DEVELOPMENT.md']
lines=base.decode().splitlines(keepends=True)
patch=(P/'CENTRAL_DISCUSSION_PATCH.diff').read_text().splitlines(keepends=True)
match=re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@',patch[2])
assert match
start,oldn,_,newn=map(int,match.groups())
old=[];new=[]
for line in patch[3:]:
    assert line[0] in ' +-',line
    if line[0] in ' -':old.append(line[1:])
    if line[0] in ' +':new.append(line[1:])
assert len(old)==oldn and len(new)==newn
assert lines[start-1:start-1+oldn]==old
intermediate=''.join(lines[:start-1]+new+lines[start-1+oldn:]).encode()
assert H(intermediate)=='45556024bf38e9c2c21d1001fd71c9b831af22eddddf1600d88a79a0b1da96a2'
print(json.dumps({'status':'PASS','accepted_file_count':len(freeze['accepted_sha256']),
 'candidate_file_count':len(candidate['sha256']),
 'freeze_sha256':H((P/'INTEGRATION_FREEZE.json').read_bytes()),
 'intermediate_central_sha256':H(intermediate),
 'checks':['all accepted bytes','unchanged original candidate','generated program equality',
 'open-join-only edge','repair routes to proposal and R18 only','launch/intermediate reconstruction'],
 'scope':'correspondence and shared-verifier regression, not full scientific reproof'},indent=2))
