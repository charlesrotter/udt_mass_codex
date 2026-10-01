"""Bound reviewed clock source and independently replay the finite query/field join."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
B=ROOT/'udt_time_live_production_survey_2026-10-01'
D=B/'diagnosis';HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())

fpath=D/'review_runtime/CLOCK_COMPLETION_FREEZE.json';freeze=read(fpath)
assert sha(fpath)=='749bf96e9414961fee22b991fe473a9903f7e4176a79a4abdf46b8597131c74d'
for p,h in freeze['source_sha256'].items():assert sha(ROOT/p)==h,p
m=read(B/'production_runtime/campaign.json');a=read(B/'production_analysis/postprocess/MATH_CANDIDATE.json')
subset=read(B/'review/runtime/CLOCK_SUBSET_FREEZE.json');queries=read(B/'review/runtime/SUBSET_CLOCK_QUERIES.json');dispatch=read(B/'CLOCK_DISPATCH.json')
indices=[j for j,d in enumerate(a['datasets']) if j%12==0 or '_a0' in d['dataset'] or '_a5' in d['dataset']]
assert indices==subset['selected_dataset_indices'] and len(indices)==30
assert [m['cases'][3*j+1]['id'] for j in indices]==[r['name'] for r in queries['cases']]
counts={'PASS':0,'UNQUALIFIED':0}
for j,d in enumerate(a['datasets']):
    assert set(d['original_equations'])=={r['id'] for r in m['cases'][3*j:3*j+3]}
    counts['PASS' if d['status']=='PASS' else 'UNQUALIFIED']+=1
assert counts=={'PASS':65,'UNQUALIFIED':13}
assert dispatch['origin']==[.31,.47,.19] and dispatch['directions']==[[1,0,0],[0,1,0],[0,0,1],[1,1,1]]
assert dispatch['query_times']==[2.484,2.496] and dispatch['null_threshold']==dispatch['matched_logZ_threshold']==2e-7
assert freeze['wall_timeout_seconds'] is None and freeze['cpu_timeout_seconds'] is None
result=dict(status='CLEARED_FOR_FIXED_DIAGNOSTIC_CLOCK_CHARACTERIZATION',reviewer_context='/root/survey_completion_math',freeze_sha256=sha(fpath),adapter_sha256=sha(D/'review_runtime/clock_completion.py'),review_script_sha256=sha(__file__),original_qualification_counts=counts,independent_subset_count=len(indices),source_sha256=freeze['source_sha256'],source_review='Read actual adapter, fixed batch/comparison, Fourier/Hermite metric, Christoffel/DOP853 and covector/RK45 sources. omega=-p0/sqrt(-g00), Z=omega_e/omega_o, initial null normalization and covector evolution sign are consistent. Source-fixed four directions/origin/time interval and both2e-7 limits unchanged; sign never gates success.',classification='Original234 clocks characterized;13original flagged datasets remain diagnostic regardless of clock PASS. New repair histories need separate map and labels.',independence='Fresh same-model context; source/joins checked independently. Did not rerun geodesics here. Reused two readout integrators share saved fields and Fourier/Hermite interpolation; no independent geometry evolution.',omissions='Source clearance only; final actual234readouts/30Hamilton comparisons and qualification tables require result review. Resource/runtime fixtures owned by runtime context; no new runtime attestation here.')
with (HERE/'CLOCK_SOURCE_REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['status','freeze_sha256','original_qualification_counts','independent_subset_count']}))
