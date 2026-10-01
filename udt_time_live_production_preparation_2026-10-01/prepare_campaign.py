"""Deterministic finite campaign generator. Default is preview, not execution."""
import argparse,copy,hashlib,io,json,math,sys
from pathlib import Path
import numpy as np
from initial_family import construct,tt_tensor
B=Path(__file__).resolve().parent;ROOT=B.parent
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
def write(q,x):
    with Path(q).open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
def families():
    amplitudes=[.25,.5,1.,1.5,2.,3.];deltas=[0.,.5,1.,1.5];angles=[0.,math.pi/12,math.pi/6]
    axial=json.loads((B/'families/axial1.json').read_text())['modes'];oblique=json.loads((B/'families/oblique1.json').read_text())['modes'];out={}
    for ai,a in enumerate(amplitudes):
        modes=copy.deepcopy(axial)
        for m in modes:m['amplitude']*=a
        out[f'axial_a{ai}']=modes
        for pi,delta in enumerate(deltas):
            for ri,angle in enumerate(angles):
                modes=copy.deepcopy(oblique)
                for m in modes:
                    k=np.array(m['k'],dtype=float);k/=np.linalg.norm(k)
                    j=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
                    t=tt_tensor(m['k'],m['matrix']);partner=(j@t-t@j)/2
                    m['matrix']=(math.cos(2*angle)*t+math.sin(2*angle)*partner).tolist();m['amplitude']*=a
                modes[3]['phase']+=delta;out[f'oblique_a{ai}_p{pi}_r{ri}']=modes
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--emit',action='store_true');args=ap.parse_args();data=families()
    summary=dict(datasets=len(data),runs=3*len(data),amplitudes=[.25,.5,1.,1.5,2.,3.],fourth_oblique_phase_offsets=[0.,.5,1.,1.5],polarization_angles_degrees=[0,15,30],meshes_and_controls=['24 coarse','24 half ceiling/CFL','32 coarse'],time_slab=[1,2.5],wall_limit_seconds=21600,output_limit_bytes=64*1024**3,scope='Supplied finite initial-data grid, no physical inequivalence/typicality/completeness or native law claim')
    print(json.dumps(summary,indent=2))
    if not args.emit:return 0
    initial=B/'initial/production';specs=B/'specs/production';runs=B/'runs/production';runtime=B/'production_runtime';analysis=B/'production_analysis'
    areas=[initial,specs,runs,runtime,analysis]
    for q in areas:
        if q.exists():raise RuntimeError('REFUSE_EXISTING_PRODUCTION_AREA: '+str(q))
    for q in areas:
        q.mkdir()
    sources=[B/'supervise.py',B/'production_worker.py',B/'initial_family.py',B/'prepare_campaign.py',B/'families/axial1.json',B/'families/oblique1.json',ROOT/'udt_three_spatial_smoke_2026-10-01/evolution.py',ROOT/'udt_three_spatial_smoke_2026-10-01/constraints.py',ROOT/'udt_time_live_smoke_gate_2026-09-30/checkpoint_io.py']
    sources.extend([ROOT/'udt_three_spatial_smoke_2026-10-01/initial_data.py',B/'specs/axial1_n24.json',B/'specs/axial1_n24_half.json',B/'specs/axial1_n32.json'])
    sources.extend([B/'assemble_campaign.py',B/'assemble_windows.py'])
    bindings={str(q):sha(q) for q in sources};cases=[]
    for name,modes in data.items():
        for n in [24,32]:
            q=initial/f'{name}_n{n}.npz';state=construct(n,modes);buf=io.BytesIO();np.savez_compressed(buf,**state)
            with q.open('xb') as f:f.write(buf.getvalue())
            bindings[str(q)]=sha(q)
        for n,fine in [(24,False),(24,True),(32,False)]:
            cid=f'{name}_n{n}'+('_half' if fine else '');template=B/'specs'/('axial1_n24_half.json' if fine else f'axial1_n{n}.json')
            spec=json.loads(template.read_text());spec['initial']=str((initial/f'{name}_n{n}.npz').relative_to(ROOT));q=specs/f'{cid}.json';write(q,spec)
            cases.append(dict(id=cid,spec=str(q),spec_sha256=sha(q),run=str(runs/cid)))
    manifest=dict(wall_seconds=21600,output_bytes=64*1024**3,storage_roots=[str(initial),str(specs),str(runs),str(runtime),str(analysis)],source_sha256=bindings,cases=cases)
    write(runtime/'campaign.json',manifest);write(runtime/'case_grid.json',summary)
    print('READY_FOR_FIRST_BOUNDED_QUEUE_CHECK:',str(runtime/'campaign.json'))
    return 0
if __name__=='__main__':raise SystemExit(main())
