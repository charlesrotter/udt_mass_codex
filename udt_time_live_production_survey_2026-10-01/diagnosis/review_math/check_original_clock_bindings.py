"""Join original mathematical case reviews to actual clock-input histories."""
import argparse
import hashlib
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[3]
B=ROOT/'udt_time_live_production_survey_2026-10-01'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--require-complete',action='store_true');ap.add_argument('--output',required=True);args=ap.parse_args()
    started=time.monotonic();candidate_path=B/'production_analysis/postprocess/MATH_CANDIDATE.json';manifest_path=B/'production_runtime/campaign.json'
    freeze=read(B/'diagnosis/INITIAL_FREEZE.json')
    for p in [candidate_path,manifest_path]:assert sha(p)==freeze['sha256'][str(p.relative_to(ROOT))]
    candidate=read(candidate_path);manifest=read(manifest_path);rows=[];pending=[]
    assert len(manifest['cases'])==candidate['checked_cases']==234
    for case in manifest['cases']:
        name=case['id'];report_path=B/'review/math/cases'/(name+'.json');report_hash=sha(report_path)
        assert report_hash==candidate['result_sha256'][str(report_path)]
        report=read(report_path);assert report['case']==name and report['status']=='PASS' and report['manifest_sha256']==sha(manifest_path)
        assert report['method_sources']==candidate['method_sources']
        window=report['windows'][2];assert window['index']==2
        binding=window['binding'];history=ROOT/binding['path'];assembly=B/'production_analysis'/name/'ASSEMBLY.json'
        assert history==B/'production_analysis'/name/'histories'/(name+'_window2.npz')
        assert sha(history)==binding['sha256']
        assert sha(assembly)==binding['assembly_sha256']
        assert sha(history.with_suffix('.sources.json'))==binding['sources_sha256']
        assembled=read(assembly);assert assembled['input_sha256'][str(manifest_path)]==sha(manifest_path)
        assert assembled['input_sha256'][case['spec']]==case['spec_sha256']
        assert assembled['output_sha256'][str(history)]==binding['sha256']
        clock_path=assembly.parent/'clock.json';clock_hash=None
        if clock_path.exists():
            clock=read(clock_path);assert clock['history_sha256']==binding['sha256'] and clock['status']=='FINITE_CLOCK_CHECK_PASS'
            assert len(clock['readouts'])==4
            clock_hash=sha(clock_path)
        else:pending.append(name)
        rows.append(dict(case=name,case_report_sha256=report_hash,history_sha256=binding['sha256'],assembly_sha256=binding['assembly_sha256'],sources_sha256=binding['sources_sha256'],available_clock_sha256=clock_hash))
    if args.require_complete:assert not pending,'CLOCK_OUTPUTS_NOT_COMPLETE'
    result=dict(status='PASS',reviewer_context='/root/survey_completion_math',source_sha256=sha(__file__),original_manifest_sha256=sha(manifest_path),original_candidate_sha256=sha(candidate_path),joined_field_cases=len(rows),available_clock_outputs=len(rows)-len(pending),pending_clock_outputs=pending,rows=rows,seconds=time.monotonic()-started,scope='Direct hash join of all234 original late histories/assembly/source maps to original aggregate-bound mathematical case reports, plus available producer clock history identities. No geodesics or field equations recomputed; final actual clock-result checks remain separate. Original65PASS/13unqualified dataset labels unchanged.')
    with Path(args.output).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:result[k] for k in ['status','joined_field_cases','available_clock_outputs','seconds']}))
if __name__=='__main__':main()
