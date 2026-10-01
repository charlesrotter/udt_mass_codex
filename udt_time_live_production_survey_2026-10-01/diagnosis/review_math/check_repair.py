"""Narrow manifest adapter to fixed independent TPS1 case checks; no solver edits."""
import argparse
import copy
import json
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ROOT=BASE.parent
D=BASE/'diagnosis'
sys.path.insert(0,str(BASE/'review/math'))
import check_survey as fixed

def require(ok,message):
    if not ok:raise ValueError(message)

def exact_delta(old,new,n):
    require(set(old)==set(new),'SPEC_KEYS_CHANGED')
    require(new['n']==old['n']==n,'MESH_CHANGED')
    require({k for k in old if old[k]!=new[k]}=={'cfl','max_step_ticks'},'ONLY_TWO_CONTROL_CHANGES')
    require(new['cfl']*2==old['cfl'] and new['max_step_ticks']*2==old['max_step_ticks'],'NOT_EXACT_HALVING')
    require(new['wall_seconds'] is None and new['constraint_limit']==2e-5,'STOP_OR_THRESHOLD_CHANGED')

def review_specs():
    map_path=D/'REPAIR_CASES.json';manifest_path=D/'repair_runtime/campaign.json'
    mapping=fixed.read(map_path);m=fixed.read(manifest_path)
    original_path=BASE/'production_runtime/campaign.json';candidate_path=BASE/'production_analysis/postprocess/MATH_CANDIDATE.json'
    freeze=fixed.read(D/'INITIAL_FREEZE.json')
    for p in [original_path,candidate_path]:require(fixed.sha(p)==freeze['sha256'][str(p.relative_to(ROOT))],'ORIGINAL_FREEZE_CHANGED')
    require(mapping['original_manifest_sha256']==fixed.sha(original_path),'ORIGINAL_MANIFEST_BINDING')
    require(mapping['original_failed_aggregate_sha256']==fixed.sha(candidate_path),'ORIGINAL_CANDIDATE_BINDING')
    require(mapping['repair_manifest_sha256']==fixed.sha(manifest_path),'REPAIR_MANIFEST_BINDING')
    original=fixed.read(original_path);candidate=fixed.read(candidate_path)
    old={r['id']:r for r in original['cases']}
    flagged={r['dataset'] for r in candidate['datasets'] if r['status']=='DIAGNOSTIC_NOT_QUALIFIED'}
    expected={'axial_a5'}|{f'oblique_a5_p{p}_r{r}' for p in range(4) for r in range(3)}
    names=[r['dataset'] for r in mapping['datasets']]
    require(flagged==expected==set(names) and len(names)==13,'EXACT_FLAGGED_DATASETS')
    require(names[0]=='oblique_a5_p0_r0','FIRST_PAIR_CHANGED')
    require(len(m['cases'])==mapping['case_count']==26,'EXACT_26_CASES')
    ids=[r['id'] for r in m['cases']];require(len(set(ids))==26,'DUPLICATE_CASE')
    expected_ids=[];spec_rows=[]
    for mp in mapping['datasets']:
        name=mp['dataset']
        require(mp==dict(dataset=name,original_status='DIAGNOSTIC_NOT_QUALIFIED',base_case=name+'_n24_half',quarter_case=name+'_n24_quarter',fine32_case=name+'_n32_half'),'CASE_MAP_CHANGED')
        for suffix,old_suffix,n in [('n24_quarter','n24_half',24),('n32_half','n32',32)]:
            cid=name+'_'+suffix;expected_ids.append(cid)
            r=next(r for r in m['cases'] if r['id']==cid)
            spec_path=fixed.checked_path(r['spec'],r['spec_sha256'])
            require(spec_path.parent==D/'repair_specs','SPEC_LOCATION')
            require(Path(r['run'])==BASE/'runs/refinement'/cid,'RUN_LOCATION')
            o=old[name+'_'+old_suffix];old_spec=fixed.read(fixed.checked_path(o['spec'],o['spec_sha256']))
            spec=fixed.read(spec_path);exact_delta(old_spec,spec,n)
            initial=fixed.checked_path(spec['initial']);require(str(initial) in m['source_sha256'],'UNBOUND_INITIAL')
            require(m['source_sha256'][str(initial)]==original['source_sha256'][str(initial)]==fixed.sha(initial),'INITIAL_CHANGED')
            spec_rows.append(dict(case=cid,n=n,cfl=spec['cfl'],max_step_ticks=spec['max_step_ticks'],output_bytes=spec['output_bytes'],initial_sha256=fixed.sha(initial)))
    require(ids==expected_ids,'CASE_ORDER')
    require(m['wall_seconds'] is None and m['output_bytes']==original['output_bytes']==64*1024**3,'GLOBAL_LIMITS_CHANGED')
    for p,h in m['source_sha256'].items():
        source=Path(p).resolve()
        require(source.is_relative_to(ROOT),'SOURCE_OUTSIDE_REPOSITORY')
        require(fixed.sha(source)==h,'SOURCE_HASH_CHANGED: '+str(source))
    require(fixed.method_sources()==candidate['method_sources'],'FROZEN_CHECKER_CHANGED')
    # Targeted guard defects are in-memory only; no production/spec mutation.
    fixture=fixed.read(m['cases'][0]['spec']);old_fixture=fixed.read(old[names[0]+'_n24_half']['spec']);caught=[]
    for label,mutator in [('changed_initial',lambda s:s.update(initial='other.npz')),('loosened_threshold',lambda s:s.update(constraint_limit=2e-4)),('wrong_mesh',lambda s:s.update(n=32)),('unchanged_cfl',lambda s:s.update(cfl=old_fixture['cfl'])),('wrong_step_ratio',lambda s:s.update(max_step_ticks=1))]:
        bad=copy.deepcopy(fixture);mutator(bad)
        try:exact_delta(old_fixture,bad,24)
        except ValueError:caught.append(label)
        else:raise ValueError('UNCAUGHT_SPEC_DEFECT: '+label)
    m['_manifest_sha256']=fixed.sha(manifest_path);m['_manifest_path']=str(manifest_path)
    return m,mapping,candidate,dict(status='PASS',cases=spec_rows,defect_controls_caught=caught,dispatch_sha256=fixed.sha(D/'REPAIR_DISPATCH.md'),manifest_sha256=fixed.sha(manifest_path),map_sha256=fixed.sha(map_path),method_sources=fixed.method_sources())

def check_cases(m,mapping,candidate,limit):
    selected=m['cases'][:limit] if limit else m['cases'];case_results={};hashes={};outdir=HERE/'repair_cases';outdir.mkdir(exist_ok=True)
    methods=fixed.method_sources();adapter=fixed.sha(__file__)
    for row in selected:
        p=outdir/(row['id']+'.json')
        if p.exists():
            r=fixed.read(p)
            require(r['case']==row['id'] and r['method_sources']==methods and r['adapter_sha256']==adapter and r['manifest_sha256']==m['_manifest_sha256'],'EXISTING_CASE_REPORT_BINDING')
            # Re-authenticate source artifacts without rerunning expensive Ricci.
            for w in r['windows']:
                require(fixed.sha(ROOT/w['binding']['path'])==w['binding']['sha256'],'REUSED_WINDOW_CHANGED')
        else:
            r=fixed.check_case(m,row['id'],D/'repair_analysis')
            r.update(method_sources=methods,adapter_sha256=adapter,manifest_sha256=m['_manifest_sha256'],reviewer_context='/root/survey_completion_math',attribution='Fresh execution of unchanged independently authored TDS/TPP/TPS1 original-equation methods; shared fields/Fourier, no independent general-data integrator.')
            fixed.write(p,r)
        case_results[row['id']]=r;hashes[str(p.relative_to(ROOT))]=fixed.sha(p)
        print(json.dumps(dict(event='REPAIR_CASE_CHECKED',case=row['id'],status=r['status'])),flush=True)
    dataset_rows=[]
    for mp in mapping['datasets'][:len(selected)//2]:
        base_path=BASE/'review/math/cases'/(mp['base_case']+'.json')
        require(str(base_path) in candidate['result_sha256'] and fixed.sha(base_path)==candidate['result_sha256'][str(base_path)],'OLD_BASE_REPORT_CHANGED')
        a=fixed.read(base_path);b=case_results[mp['quarter_case']];c=case_results[mp['fine32_case']]
        require(a['case']==mp['base_case'] and a['method_sources']==methods and a['manifest_sha256']==mapping['original_manifest_sha256'],'OLD_BASE_METHOD_CHANGED')
        coarse=fixed.authenticated_window(mp['base_case'],2,BASE/'production_analysis')[0]
        fine=fixed.authenticated_window(mp['quarter_case'],2,D/'repair_analysis')[0]
        require(coarse['g'].shape==fine['g'].shape==(9,24,24,24,4,4) and np.array_equal(coarse['times'],fine['times']) and coarse['period']==fine['period'],'MATCHED_COMPARISON_EVENTS')
        temporal={k:float(abs(coarse[k][-1]-fine[k][-1]).max()) for k in ['g','v']}
        spatial=[]
        for order in ['6','8']:
            low=max(w['centers'][order]['common8_max'] for w in a['windows']);high=max(w['centers'][order]['common8_max'] for w in c['windows'])
            whole=max(w['centers'][order]['ricci_max'] for r in [a,c] for w in r['windows'])
            spatial.append(dict(order=int(order),coarse_common8_max=low,fine_common8_max=high,ratio=None if high==0 else low/high,all_points_both_meshes_max=whole,status='PASS' if low>=10*high or whole<1e-8 else 'INCONCLUSIVE_REFINEMENT'))
        eq=all(r['status']=='PASS' for r in [a,b,c]);tp=max(temporal.values())<=2e-7
        passed=eq and tp and all(r['status']=='PASS' for r in spatial)
        dataset_rows.append(dict(**mp,repaired_status='PASS' if passed else 'DIAGNOSTIC_NOT_QUALIFIED',original_equations_pass=eq,final_time_refinement=temporal,temporal_status='PASS' if tp else 'FAIL',spatial=spatial,base_report_sha256=fixed.sha(base_path)))
    return dict(status='PASS' if all(r['repaired_status']=='PASS' for r in dataset_rows) else 'DIAGNOSTIC_NOT_QUALIFIED',selected_cases=len(selected),original_equations_pass=all(r['status']=='PASS' for r in case_results.values()),datasets=dataset_rows,case_report_sha256=hashes)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--specs-only',action='store_true');ap.add_argument('--limit',type=int,default=0);ap.add_argument('--output',required=True);args=ap.parse_args()
    require(args.limit in [0,2,26],'LIMIT_MUST_BE_FIRST_PAIR_OR_ALL')
    start=time.monotonic();m,mapping,candidate,specs=review_specs()
    result=specs if args.specs_only else check_cases(m,mapping,candidate,args.limit)
    result.update(adapter_sha256=fixed.sha(__file__),numpy=np.__version__,seconds=time.monotonic()-start,reviewer_context='/root/survey_completion_math',repair_specs_review=specs if not args.specs_only else None,scope='Finite same-premise resolution repair; original65/13status table immutable, repaired triple is old24half/new24quarter/new32half. No new criterion or continuum claim.')
    fixed.write(args.output,result);print(json.dumps(dict(status=result['status'],output=args.output)),flush=True)
    return 0 if result['status']=='PASS' else 2

if __name__=='__main__':raise SystemExit(main())
