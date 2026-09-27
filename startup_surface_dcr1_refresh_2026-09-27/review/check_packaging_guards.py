"""Bounded editorial-repair regression; not renewed scientific verification."""
from pathlib import Path
import ast,csv,datetime,hashlib,json,sys,tempfile,time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from pin_hash import pin_matches,normalize_eol
REVIEW=Path(__file__).resolve().parent
start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
source=(ROOT/'verify_current_scientific_premises.py').read_text(encoding='utf-8-sig')
tree=ast.parse(source)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
def require(condition,message):
    if not condition: raise SystemExit(message)
def sha(payload): return hashlib.sha256(payload).hexdigest()
records=[]
for short,directory,special in [
 ('g236','udt_g236_dual_sne_relational_state_reconstruction_2026-08-23','STATE_RECONSTRUCTION.tsv'),
 ('g237','udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23','JOINT_STATE.tsv')]:
    package=ROOT/directory
    with (package/'FINAL_EVIDENCE_MANIFEST.tsv').open() as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    registered={row['path']:row['sha256'] for row in rows}
    assert len(registered)==len(rows)
    statements=[]
    for node in main.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==short+'_actual' for t in node.targets): statements.append(node)
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and node.value.args and isinstance(node.value.args[-1],ast.Constant) and node.value.args[-1].value==short.upper()+' final evidence manifest mismatch': statements.append(node)
    assert len(statements)==2
    code=compile(ast.Module(body=statements,type_ignores=[]),'extracted '+short+' manifest statements','exec')
    def run(where,pins):
        env={short:where,short+'_registered':pins,'pin_matches':pin_matches,'require':require}
        exec(code,env)
    run(package,registered)
    raw_bad=[];normalized_bad=[]
    for name,pin in registered.items():
        payload=(package/name).read_bytes()
        if sha(payload)!=pin: raw_bad.append(name)
        if sha(payload.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))!=pin: normalized_bad.append(name)
    assert raw_bad==[]
    assert normalized_bad==[special]
    base={'a.tsv':b'alpha\r\nbeta\r\n','b.md':b'fixed\n'}
    pins={name:sha(data) for name,data in base.items()}
    outcomes={}
    cases={'raw':dict(base),'lf':dict(base,**{'a.tsv':b'alpha\nbeta\n'}),'changed_payload':dict(base,**{'a.tsv':b'alpha\r\nBETA\r\n'}),'added_path':dict(base,**{'extra.txt':b'extra\n'}),'missing_path':{'a.tsv':base['a.tsv']}}
    with tempfile.TemporaryDirectory(prefix=short+'-guard-',dir=REVIEW) as scratch:
        for case,contents in cases.items():
            work=Path(scratch)/case;work.mkdir()
            for name,data in contents.items(): (work/name).write_bytes(data)
            try: run(work,pins);accepted=True
            except SystemExit as error:
                assert str(error)==short.upper()+' final evidence manifest mismatch'
                accepted=False
            assert accepted==(case in ('raw','lf'))
            outcomes[case]='ACCEPTED' if accepted else 'REJECTED'
    payload=(package/special).read_bytes()
    records.append({'package':directory,'manifest_rows':len(rows),'raw_mismatches':raw_bad,'normalized_mismatches':normalized_bad,'special_file':special,'special_raw_sha256':sha(payload),'special_normalized_sha256':sha(normalize_eol(payload)),'exact_extracted_guard_hostile_checks':outcomes})
binary=ROOT/'udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/RADIAL_REPRESENTATION.npz'
payload=binary.read_bytes();pin='68deaa48bb68493febb1c9d34de426a215675f917b971b1aca59f833d468600b'
assert sha(payload)==pin and sha(normalize_eol(payload))!=pin
assert sha(payload+b'changed')!=pin
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-tick,'result':'PASS','kind':'Checksum correspondence and regression only; no scientific artifacts interpreted or reconstructed.','manifest_checks':records,'binary':{'path':str(binary.relative_to(ROOT)),'raw_sha256':sha(payload),'normalized_sha256':sha(normalize_eol(payload)),'raw_matches_frozen_pin':True,'changed_payload_rejected':True},'guard_source_sha256':sha((ROOT/'verify_current_scientific_premises.py').read_bytes()),'pin_helper_sha256':sha((ROOT/'pin_hash.py').read_bytes()),'scratch':'Reviewer-owned TemporaryDirectory fixtures under review automatically removed.'}
(REVIEW/'PACKAGING_GUARD_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
