"""Parent negative-path checks of separately authored extraction adapter.

Uses actual successful supervisor receipts but copies only control text. No GPU,
new fields, altered scientific inputs or producer array calculation is involved.
"""
import hashlib,json,shutil,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parent
sys.path.insert(0,str(B))
from assemble_campaign import extract
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
base=B/'checks/adapter_parent_fixtures';base.mkdir()
cases=[('output_reserve','ANALYSIS_OUTPUT_RESERVE'),('changed_receipt','ASSEMBLY_ATTEMPT_HASH'),('missing_initial','ASSEMBLY_INITIAL_UNBOUND')]
results=[]
for name,expected in cases:
    folder=base/name;folder.mkdir();runtime=folder/'runtime'
    shutil.copytree(B/'supervisor_smoke/runtime_pause',runtime)
    m=json.loads((B/'supervisor_smoke/pause.json').read_text())
    m['storage_roots'].append(str(folder));analysis=folder/'analysis'
    if name=='output_reserve':m['output_bytes']=1
    elif name=='changed_receipt':
        rp=next((runtime/'attempts').glob('*/receipt.json'));r=json.loads(rp.read_text())
        r['stdout_sha256']='0'*64;rp.write_text(json.dumps(r))
    else:
        spec=json.loads(Path(m['cases'][0]['spec']).read_text())
        initial=(ROOT/spec['initial']).resolve()
        m['source_sha256']={p:h for p,h in m['source_sha256'].items() if Path(p).resolve()!=initial}
    mp=folder/'manifest.json';mp.write_text(json.dumps(m,indent=2)+'\n')
    (runtime/'manifest.sha256').write_text(sha(mp)+'\n')
    try:extract(mp,runtime,analysis)
    except ValueError as e:assert str(e)==expected,(name,str(e));reason=str(e)
    else:raise AssertionError('EXPECTED_REJECTION: '+name)
    assert not analysis.exists()
    results.append(dict(case=name,reason=reason,no_output_created=True))
print(json.dumps(dict(status='PASS',cases=results,adapter_sha256=sha(B/'assemble_campaign.py'),
    scope='Separate parent source and negative-path checks, not an independent scientific integrator'),indent=2))
