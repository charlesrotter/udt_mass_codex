"""Review actual repair coverage, gate meaning and maxima; no further solve."""
import datetime,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];B=ROOT/'udt_time_live_production_survey_2026-10-01';D=B/'diagnosis';HERE=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

math_path=HERE/'REPAIR_MATH.json';result=read(math_path);capture=read(HERE/'all_refined_math_run.json')
assert capture['returncode']==0 and capture['wall_timeout_seconds'] is None and capture['cpu_timeout_seconds'] is None
assert capture['command'][-2:]==['--output',str(math_path.relative_to(ROOT))]
assert result['status']=='PASS' and result['selected_cases']==26 and result['original_equations_pass']
assert result['adapter_sha256']==sha(HERE/'check_repair.py')
manifest=read(D/'repair_runtime/campaign.json');assert result['repair_specs_review']['manifest_sha256']==sha(D/'repair_runtime/campaign.json')
cases={}
for p,h in result['case_report_sha256'].items():
    assert sha(ROOT/p)==h;r=read(ROOT/p);assert r['status']=='PASS' and [w['index'] for w in r['windows']]==[0,1,2]
    assert r['adapter_sha256']==result['adapter_sha256'] and r['method_sources']==result['repair_specs_review']['method_sources']
    assert r['manifest_sha256']==result['repair_specs_review']['manifest_sha256'];cases[r['case']]=r
assert set(cases)=={r['id'] for r in manifest['cases']}
assert sum(r['n']==24 for r in cases.values())==sum(r['n']==32 for r in cases.values())==13
windows=[w for r in cases.values() for w in r['windows']];adm=[a for w in windows if 'late_adm' in w for a in w['late_adm']]
routes=[]
for row in result['datasets']:
    assert row['original_status']=='DIAGNOSTIC_NOT_QUALIFIED' and row['repaired_status']=='PASS'
    base=read(B/'review/math/cases'/(row['base_case']+'.json'));fine=cases[row['fine32_case']]
    assert sha(B/'review/math/cases'/(row['base_case']+'.json'))==row['base_report_sha256']
    assert row['base_case']==row['dataset']+'_n24_half' and row['quarter_case']==row['dataset']+'_n24_quarter' and row['fine32_case']==row['dataset']+'_n32_half'
    assert max(row['final_time_refinement'].values())<=2e-7
    for record in row['spatial']:
        order=str(record['order']);lo=max(w['centers'][order]['common8_max'] for w in base['windows']);hi=max(w['centers'][order]['common8_max'] for w in fine['windows']);full=max(w['centers'][order]['ricci_max'] for r in [base,fine] for w in r['windows'])
        assert lo==record['coarse_common8_max'] and hi==record['fine_common8_max'] and full==record['all_points_both_meshes_max']
        assert lo>=10*hi or full<1e-8
        routes.append(dict(dataset=row['dataset'],order=int(order),route='tenfold' if lo>=10*hi else 'small_error_only',ratio=lo/hi,all_points_max=full))
summary=dict(status='REPAIR_RESULT_VERIFIED_WITH_CAVEATS',reviewer_context='/root/survey_completion_math',repair_math_sha256=sha(math_path),capture_sha256=sha(HERE/'all_refined_math_run.json'),review_code_sha256=sha(__file__),cases=len(cases),windows=len(windows),original_interior_time_slices=sum(w['original']['tested_time_slices'] for w in windows),late_ADM_states=len(adm),original_Ricci_max=max(w['original']['ricci_max'] for w in windows),late_H_max=max(a['hamiltonian_abs_max'] for a in adm),late_M_max=max(max(a['momentum_abs_max_by_component']) for a in adm),late_harmonic_max=max(a['harmonic_vector_abs_max'] for a in adm),sixth_eighth_tensor_difference=max(w['sixth_eighth_tensor_max_difference'] for w in windows),temporal_g_max=max(r['final_time_refinement']['g'] for r in result['datasets']),temporal_v_max=max(r['final_time_refinement']['v'] for r in result['datasets']),new32_half_center_max=max(w['centers'][order]['ricci_max'] for r in cases.values() if r['n']==32 for w in r['windows'] for order in ['6','8']),spatial_routes=routes,remaining_refined_flags=[],original_flags_preserved=13,scope='Actual finite same-premise numerical gates, not continuum certification or physical selection.')
with (HERE/'REPAIR_RESULT_SUMMARY.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
text=f'''# Actual 26-case repair result review

**VERIFIED-WITH-CAVEATS:** all13 repaired triples pass the unchanged finite
numerical gates. This qualifies the explicitly different triple old24half /
new24quarter / new32half for each flagged dataset. It does not turn the original
24coarse /24half /32coarse result into a pass. The original65PASS/13unqualified
aggregate and all failed comparisons remain fixed; no further refinement ran.

Canonical result SHA-256: `{sha(math_path)}`.
All-case capture SHA-256: `{sha(HERE/'all_refined_math_run.json')}`.
`REPAIR_RESULT_SUMMARY.json` provides the exact quantities, per-order gate routes
and bindings. This is an actual result review, not the final common-freeze
attestation or scientific promotion.

## Actual coverage and result

The26new histories comprise13 meshes at24³ with quarter ceilings and13 at32³
with half ceilings. All78saved windows were checked:390eligible original
five-point Ricci time slices,156sixth/eighth-order center tensors and78late
ADM/harmonic states. All spatial points are used for the original residuals,
constraints and small-error alternative; the ratio uses the same marked8³
events at three window centers. Two slices at each window endpoint remain
outside the original centered Ricci diagnostic. Saved-time gaps are not tested.

Original-Ricci maximum is {summary['original_Ricci_max']:.12e}; late Hamiltonian,
momentum and harmonic-vector maxima are {summary['late_H_max']:.12e},
{summary['late_M_max']:.12e} and {summary['late_harmonic_max']:.12e}, all below2e-5.
Matched24half→24quarter final g/v maxima are {summary['temporal_g_max']:.12e} /
{summary['temporal_v_max']:.12e}, below2e-7.

All12oblique datasets pass10fold spatial improvement at both stencil orders;
the smallest ratio is110.03245058282957. The axial dataset does **not** show
10fold improvement: ratios5.17609003583873 and3.8593471612548313. It passes only
the unchanged small-error alternative, all-point maxima1.218974032823894e-9
and1.2968525142653675e-9, both below1e-8. There are no remaining repaired-triple
flags. New32half center all-point residuals are at most
{summary['new32_half_center_max']:.12e}; largest sixth/eighth tensor disagreement
over all26new histories is {summary['sixth_eighth_tensor_difference']:.12e}.

The finer-step results support the proposed diagnosis of evolution-time
contamination limiting the original32coarse spatial comparison. The retained
24-level oblique residuals and new32half residuals now separate clearly under
the original rule. Ratios of residual maxima are finite accuracy diagnostics,
not convergence orders, uniform continuum bounds or nonlinear stability proofs.
The axial small-error result must not be described as10fold convergence.

## Independence, resources and chronology

This is actual fresh context `/root/survey_completion_math`, same inherited
model. The first-pair reports were computed in this context and authenticated/
reused by the full call; the other24case reports were newly computed. The13
old24half baselines reuse authenticated original reports. The unchanged TPS1
checker reuses independently authored TDS/TPP original Ricci/ADM and stencil
methods, with no producer evolution imports. The earlier exposed diagnosis
also independently reconstructed42late tensors using separately arranged code
and analytical controls. Shared raw fields, Fourier mathematics and the lack
of an independent general-data time integrator remain explicit limitations.
This result review inspected exact case membership, source bindings, slice
counts, all criterion routes and maxima; it did not repeat every Ricci solve
after the successful captured full check.

The full capture began at {capture['started_utc']}, ran
{capture['duration_seconds']:.6f}s, and returned0. Maximum resident set was
{capture['maxrss_kib']}KiB under2GiB address space. No wall/CPU timeout, signal
or extra scientific run occurred. Assembly had completed at14:42:52.684UTC;
the full check began about300.4s later following an agent dispatch/turn
interruption. That delay is separate from numerical execution and is not a
solver failure or additional research. Parent/runtime reviews independently
own the completed GPU schedule and832checkpoint authentication.

All claims stay within supplied periodic conformal-CMC initial data and
harmonic conditional Ric(g)=0, Lambda=0, G312 GR FILTER ONLY. There is no new
boundary, scale, source, carrier, physical observer population, native response
E, genericity or long-time stability claim. Refined-clock characterization is
cleared as the fixed supplied-field diagnostic on these exact bound inputs;
its actual results and descriptive atlas still require their separate review.
'''
with (HERE/'REPAIR_RESULT_REVIEW.md').open('x') as f:f.write(text)
print(json.dumps({k:v for k,v in summary.items() if k!='spatial_routes'}))
