import csv,hashlib,io,json,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parents[1]
def check_pins(path,base):
 obj=json.loads(path.read_text())
 for p,digest in obj['sha256'].items(): assert hashlib.sha256((base/p).read_bytes()).hexdigest()==digest,(path.name,p)
 return len(obj['sha256'])
frozen=check_pins(root/'CANDIDATE_FREEZE.json',root)
sources=check_pins(root/'SOURCE_PINS.json',repo)
saved=json.loads((root/'SOURCE_REGISTRY_ROWS.json').read_text())
raw=(repo/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
assert hashlib.sha256(raw).hexdigest()==saved['registry_sha256']
rows={row['premise_id']:row for row in csv.DictReader(io.StringIO(raw.decode()),delimiter='\t')}
for row in saved['rows']:assert rows[row['premise_id']]==row,row['premise_id']
captures=[]
for name,expected in [('initial_rate',0),('mutant_omit_spatial_ricci_rate',1),('mutant_freeze_third_time',1),('parent_analysis',0),('parent_analysis_order_extension',0)]:
 receipt=json.loads((root/f'checks/{name}.json').read_text())
 assert receipt['returncode']==expected and not receipt['timeout'],name
 out=json.loads((root/f'checks/{name}.stdout').read_text())
 if expected:
  failed=[x for x in out['checks'] if x['nonzero']]
  assert len(failed)==1 and failed[0]['name']=='time_derivative_original_Ricci_including_inverse_metric',name
 else: assert all(not x['nonzero'] for x in out['checks']),name
 if not expected:assert (root/f'checks/{name}.stderr').read_bytes()==b'',name
 captures.append({'name':name,'expected_exit':expected,'receipt':receipt})
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=repo).decode()
unrelated=''.join(x+'\n' for x in status.splitlines() if x.startswith('?? ') and not x.endswith('udt_two_shape_evolution_2026-09-11/'))
assert hashlib.sha256(unrelated.encode()).hexdigest()=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
print(json.dumps({'status':'PASS','candidate_pins':frozen,'source_pins':sources,'exact_registry_rows':len(saved['rows']),
 'author_captures_inspected_not_replayed':captures,'original46_name_status_preserved':True},indent=2))
