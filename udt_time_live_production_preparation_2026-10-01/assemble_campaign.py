"""Manifest/attempt-aware extraction of authenticated completed queue windows.

Bridges adapt receipt schemas; they are not fabricated execution receipts.
An assembly record certifies correspondence only, not original-equation residuals.
"""
import argparse,hashlib,json,re
from pathlib import Path
from assemble_windows import assemble

B=Path(__file__).resolve().parent;ROOT=B.parent
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def owned(path):
    path=Path(path).resolve()
    if not path.is_relative_to(B):raise ValueError('ASSEMBLY_PATH_SCOPE')
    return path
def write(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n')
def used(roots):
    files={q.resolve() for root in roots if root.exists() for q in root.rglob('*') if q.is_file()}
    return sum(q.stat().st_size for q in files)

def extract(manifest,runtime,analysis,limit=0):
    manifest=owned(manifest);runtime=owned(runtime);analysis=owned(analysis)
    m=json.loads(manifest.read_text());mh=sha(manifest)
    if (runtime/'manifest.sha256').read_text().strip()!=mh:raise ValueError('ASSEMBLY_MANIFEST_BINDING')
    roots=[owned(p) for p in m['storage_roots']]
    if not any(analysis.is_relative_to(p) for p in roots):raise ValueError('ANALYSIS_NOT_BUDGETED')
    if type(m['output_bytes'])!=int or not 0<m['output_bytes']<=64*1024**3:raise ValueError('ASSEMBLY_OUTPUT_LIMIT')
    bindings={Path(p).resolve():h for p,h in m['source_sha256'].items()}
    external={ROOT/'udt_three_spatial_smoke_2026-10-01'/name for name in ['initial_data.py','evolution.py','constraints.py']}
    external.add(ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py')
    for path,value in bindings.items():
        if not (path.is_relative_to(B) or path in external):raise ValueError('ASSEMBLY_SOURCE_SCOPE')
        if sha(path)!=value:raise ValueError('ASSEMBLY_SOURCE_CHANGED')
    worker=B/'production_worker.py'
    if worker not in bindings:raise ValueError('ASSEMBLY_WORKER_UNBOUND')
    completed={};attempts=[]
    for folder in sorted((runtime/'attempts').iterdir()):
        if not folder.is_dir():continue
        rp=folder/'receipt.json'
        if not rp.exists():raise ValueError('INCOMPLETE_ATTEMPT_REQUIRES_REVIEW')
        receipt=json.loads(rp.read_text());attempts.append(dict(case=receipt['case'],returncode=receipt['returncode']))
        launch=json.loads((folder/'launch.json').read_text())
        if launch['manifest_sha256']!=mh or launch['case']!=receipt['case'] or launch['command']!=receipt['command']:
            raise ValueError('ASSEMBLY_LAUNCH_BINDING')
        for key in ['stdout','stderr']:
            if sha(folder/key)!=receipt[key+'_sha256']:raise ValueError('ASSEMBLY_ATTEMPT_HASH')
        if receipt['returncode']!=0:continue
        if receipt.get('worker_status')!='TPP1_RUN_COMPLETE':raise ValueError('ASSEMBLY_COMPLETION_STATUS')
        if receipt['case'] in completed:raise ValueError('DUPLICATE_COMPLETION_REQUIRES_REVIEW')
        completed[receipt['case']]=(rp,receipt)
    known={row['id'] for row in m['cases']}
    if not set(completed)<=known:raise ValueError('ASSEMBLY_UNKNOWN_CASE')
    results=[]
    for row in m['cases']:
        if row['id'] not in completed:continue
        if limit and len(results)>=limit:break
        if not re.fullmatch('[a-z0-9_-]+',row['id']):raise ValueError('ASSEMBLY_CASE_ID')
        specpath=owned(row['spec']);run=owned(row['run']);spec=json.loads(specpath.read_text())
        if sha(specpath)!=row['spec_sha256']:raise ValueError('ASSEMBLY_SPEC_CHANGED')
        rp,receipt=completed[row['id']]
        command=receipt['command']
        if len(command) not in [4,5] or Path(command[1]).resolve()!=worker or Path(command[2]).resolve()!=specpath or Path(command[3]).resolve()!=run or (len(command)==5 and command[4]!='--resume'):
            raise ValueError('ASSEMBLY_COMMAND_BINDING')
        initial=owned(ROOT/spec['initial'])
        if initial not in bindings:raise ValueError('ASSEMBLY_INITIAL_UNBOUND')
        for marker in run.glob('checkpoints/ckpt_*/COMMITTED'):
            metadata=marker.parent/'metadata.json'
            if marker.read_text().strip()!=sha(metadata):raise ValueError('ASSEMBLY_METADATA_HASH')
            signature=json.loads(metadata.read_text())['signature']
            if signature['initial']!=bindings[initial]:raise ValueError('ASSEMBLY_CHECKPOINT_INITIAL')
            for source,value in signature['code'].items():
                if bindings.get((ROOT/source).resolve())!=value:raise ValueError('ASSEMBLY_CHECKPOINT_CODE')
        final=json.loads((rp.parent/'stdout').read_text().splitlines()[-1])
        if final.get('status')!='TPP1_RUN_COMPLETE' or final.get('tick')!=spec['end_tick']:raise ValueError('ASSEMBLY_INCOMPLETE_ENDPOINT')
        directory=analysis/row['id'];record_path=directory/'ASSEMBLY.json'
        inputs={str(manifest):mh,str(rp):sha(rp),str(rp.parent/'launch.json'):sha(rp.parent/'launch.json'),str(specpath):sha(specpath),str(initial):bindings[initial]}
        if record_path.exists():
            record=json.loads(record_path.read_text())
            if record['input_sha256']!=inputs:raise ValueError('ASSEMBLY_REUSE_INPUT_CHANGED')
            for path,value in record['output_sha256'].items():
                if sha(owned(path))!=value:raise ValueError('ASSEMBLY_REUSE_OUTPUT_CHANGED')
            results.append(dict(case=row['id'],reused=True,record=str(record_path)));continue
        if directory.exists():raise ValueError('INCOMPLETE_ASSEMBLY_REQUIRES_REVIEW')
        n=spec['n'];windows=spec['windows']
        if type(n)!=int or not 8<=n<=64 or not windows:raise ValueError('ASSEMBLY_SPEC_DOMAIN')
        # Uncompressed g/v payload plus1MiB per window covers compression/header
        # overhead and manifests conservatively for these bounded arrays.
        reserve=sum(w['count']*2*n**3*16*8+1024**2 for w in windows)+1024**2
        if used(roots)+reserve>m['output_bytes']:raise ValueError('ANALYSIS_OUTPUT_RESERVE')
        directory.mkdir(parents=True)
        bridge=directory/'receipt_bridge.json'
        write(bridge,dict(returncode=0,spec_sha256=row['spec_sha256'],worker_sha256=bindings[worker],
            bridge_provenance=dict(manifest=str(manifest),manifest_sha256=mh,actual_attempt_receipt=str(rp),
                actual_attempt_receipt_sha256=sha(rp),meaning='Schema adapter deriving declared hashes from authenticated manifest; not another execution receipt')))
        outputs=assemble(row['id'],receipt=bridge,run=run,source_spec=specpath,out=directory/'histories')
        hashes={str(bridge):sha(bridge)}
        for output in outputs:
            path=Path(output['path']);path=path if path.is_absolute() else ROOT/path
            hashes[str(path)]=sha(path);hashes[str(path.with_suffix('.sources.json'))]=sha(path.with_suffix('.sources.json'))
        record=dict(case=row['id'],input_sha256=inputs,output_sha256=hashes,windows=outputs,
            adapter_sha256=sha(__file__),assembler_sha256=sha(B/'assemble_windows.py'),
            scope='Authenticated byte/array correspondence only; original equations, convergence and readouts remain separate checks')
        write(record_path,record)
        if used(roots)>m['output_bytes']:raise ValueError('ANALYSIS_OUTPUT_LIMIT')
        results.append(dict(case=row['id'],reused=False,record=str(record_path)))
    return dict(status='CAMPAIGN_WINDOW_ASSEMBLY_COMPLETE',results=results,attempts=attempts,
        manifest_sha256=mh,used_bytes=used(roots),scope='Completed cases only; failures retained, assembly is not numerical qualification')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('manifest');ap.add_argument('runtime');ap.add_argument('--analysis',default=str(B/'production_analysis'));ap.add_argument('--limit',type=int,default=0);args=ap.parse_args()
    if args.limit<0:raise ValueError('INVALID_ASSEMBLY_LIMIT')
    print(json.dumps(extract(args.manifest,args.runtime,args.analysis,args.limit),indent=2))
