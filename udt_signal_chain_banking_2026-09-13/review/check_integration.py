"""Independent input attacks on actual banking functions; no source writes.
Usage: python check_integration.py MODULE_NAME
This reuses the established in-memory Path.open fault-injection method, but
constructs its own current eight-row cases and saved baseline correspondence.
"""
from pathlib import Path
import ast,csv,datetime,hashlib,importlib,io,json,subprocess,sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
new=importlib.import_module(sys.argv[1]);old=importlib.import_module('verify_current_scientific_premises')
B=ROOT/'udt_signal_chain_banking_2026-09-13';REG=ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv'
ids=tuple('G'+str(i) for i in range(416,424));idbytes={x.encode() for x in ids}
validate=getattr(new,next(n for n in vars(new) if n.startswith('validate_') and n.endswith('_banking')))
project_name=next(n for n in vars(new) if n.startswith('without_'))
project=getattr(new,project_name)
raw=REG.read_bytes();lines=raw.splitlines(keepends=True)
rowmap={l.split(b'\t',1)[0].decode():l for l in lines[1:] if l.split(b'\t',1)[0] in idbytes}
assert set(rowmap)==set(ids)
baseline=subprocess.check_output(['git','show','bf1a58140ef3eaf438f18e3cc2dcd57df52d2549:CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT)
assert b''.join(l for l in lines if l.split(b'\t',1)[0] not in idbytes)==baseline
assert len(list(csv.DictReader(raw.decode().splitlines(),delimiter='\t')))==406
claims=json.loads((B/'BANKED_CLAIMS.json').read_text())
expected={c['id']:c['claim'] for c in claims['claims']}
actual={r['premise_id']:r for r in csv.DictReader(raw.decode().splitlines(),delimiter='\t')}
assert all(actual[i]==expected[i] for i in ids)
opened_original=Path.open;events=[]
def exercise(label,fn,payloads,*,target=REG,expect_reject=False,expected_reads=1):
 observed=[]
 def opened(path,mode='r',*args,**kwargs):
  if path==target:
   data=payloads[min(len(observed),len(payloads)-1)];observed.append(str(path))
   return io.BytesIO(data) if 'b' in mode else io.StringIO(data.decode(kwargs.get('encoding') or 'utf-8'))
  return opened_original(path,mode,*args,**kwargs)
 error=None
 with patch.object(Path,'open',opened):
  try:fn()
  except SystemExit as exc:error=str(exc)
 assert len(observed)==expected_reads,(label,'reads',len(observed),expected_reads)
 assert (error is not None)==expect_reject,(label,error)
 events.append({'case':label,'reads':len(observed),'rejection':error})
 return error
newfn=lambda:validate(ROOT,authenticate_sources=False)
for ident in ids:
 row=rowmap[ident]
 for field in range(9):
  fields=row.rstrip(b'\n').split(b'\t');fields[field]+=b' CORRUPTED'
  exercise(ident+':field'+str(field),newfn,[raw.replace(row,b'\t'.join(fields)+b'\n')],expect_reject=True)
 exercise(ident+':missing',newfn,[raw.replace(row,b'')],expect_reject=True)
 exercise(ident+':duplicate',newfn,[raw.replace(row,row+row)],expect_reject=True)
exercise('all new rows absent',newfn,[baseline],expect_reject=True)
exercise('old row changed',newfn,[raw.replace(b'G394\t',b'G394_CORRUPTED\t',1)],expect_reject=True)
exercise('header changed',newfn,[raw.replace(b'premise_id\t',b'altered_id\t',1)],expect_reject=True)
assert b'G394_CORRUPTED\t' in project(raw.replace(b'G394\t',b'G394_CORRUPTED\t',1))
poison=raw.replace(rowmap['G421'],rowmap['G421'].replace(b'NOT_PHYSICAL_ADOPTION',b'PHYSICAL_ADOPTION'))
partial=raw.replace(rowmap['G418'],b'');duplicate=raw.replace(rowmap['G422'],rowmap['G422']*2)
names=['validate_conditional_banking','validate_shared_constraint_banking','validate_persistence_banking','validate_restrictiveness_banking','validate_source_metric_banking','validate_reconstruction_banking','validate_coupled_banking','validate_vacuum_scale_banking','validate_berger_banking','validate_closed_fibre_banking','validate_neighboring_tidal_banking','validate_reviewed_backlog_banking','validate_ti1_banking','validate_ti2_banking','validate_ncb1_banking']
calls={n:(lambda n=n:getattr(old,n)(ROOT,authenticate_sources=False)) for n in names}
calls['new_current']=newfn
calls['historical_banking_snapshot']=lambda:old.historical_banking_snapshot(ROOT)
calls['registry_bytes_for_historical_banking']=lambda:old.registry_bytes_for_historical_banking(ROOT)
for name,fn in calls.items():
 exercise(name+':valid then poisoned second read',fn,[raw,poison])
 exercise(name+':poisoned first then valid',fn,[poison,raw],expect_reject=True)
 exercise(name+':partial then valid',fn,[partial,raw],expect_reject=True)
 exercise(name+':duplicate then valid',fn,[duplicate,raw],expect_reject=True)
 exercise(name+':historical absence',fn,[baseline],expect_reject=(name=='new_current'))
validate(ROOT)
source_names=[line.split(maxsplit=1)[1] for line in (B/'SOURCE_EVIDENCE_SHA256SUMS').read_text().splitlines()]
# Each package's initial candidate and final review represent actual byte-poison
# checks. All662 files were independently authenticated separately; no claim of
# one separate poisoned replay for every source file is made here.
selected=[]
for pkg in claims['source_packages']:
 members=[n for n in source_names if n.startswith(pkg+'/')]
 for ending in ['INITIAL_CANDIDATE.md','FINAL_FIDELITY.md']:
  match=[n for n in members if n.endswith(ending)]
  if not match:match=[n for n in members if n.endswith('FINAL_FIDELITY_REVIEW.md')]
  assert match,(pkg,ending);selected.append(match[0])
for name in sorted(set(selected)):
 path=ROOT/name;exercise('source poison:'+name,lambda:validate(ROOT),[path.read_bytes()+b'\nSOURCE_CORRUPTION\n'],target=path,expect_reject=True)
for name in ['BANKED_CLAIMS.json','BANKED_ROWS.tsv','BANKING_RECORD.md','SOURCE_EVIDENCE_SHA256SUMS','SOURCE_MEMBERSHIP.json']:
 path=B/name;exercise('acceptance poison:'+name,lambda:validate(ROOT,authenticate_sources=False),[path.read_bytes()+b'\nFORGED\n'],target=path,expect_reject=True)
# Catch proof: retain row deletion but remove only the authenticating gate in
# memory. The same hostile-input rejection assertion must now fail.
def unsafe(data,*,required=False):
 return b''.join(l for l in data.splitlines(keepends=True) if l.split(b'\t',1)[0] not in idbytes)
red=[]
# The inspected adapter centralizes the new gate in ncb1_banking_guard;
# all four historical callers traverse that same gate, not four new copies.
for module_name,fnname in [('verify_current_scientific_premises','validate_conditional_banking'),('ti1_banking_guard','validate_ti1_banking'),('ti2_banking_guard','validate_ti2_banking'),('ncb1_banking_guard','validate_ncb1_banking')]:
 module=importlib.import_module('ncb1_banking_guard')
 assert hasattr(module,project_name)
 with patch.object(module,project_name,unsafe):
  try:exercise('removed authentication:'+module_name,calls[fnname],[poison],expect_reject=True)
  except AssertionError as exc:
   assert 'reads' not in str(exc),str(exc)
   red.append({'module':module_name,'unchanged_hostile_assertion_failed':str(exc)})
  else:raise AssertionError('Hostile check did not turn red when auth was removed: '+module_name)
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_DIRECT_BYTE_AUTHENTICATION_AND_HOSTILE_BOUNDARIES','module':sys.argv[1],'projector':project_name,'original398_byte_identity':True,'current406_exact_rows':True,'events':events,'removed_authentication_catchproofs':red,'source_poison_count':len(set(selected)),'input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REG,B/'BANKED_CLAIMS.json',ROOT/(sys.argv[1]+'.py'),ROOT/'verify_current_scientific_premises.py']},'scope':'Independent fault-injection harness executing shared guarded implementations; correspondence/regression, not new scientific proof.'},indent=2))
