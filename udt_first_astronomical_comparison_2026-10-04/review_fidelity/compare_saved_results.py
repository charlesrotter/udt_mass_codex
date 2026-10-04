import decimal,json,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
decimal.getcontext().prec=80
D=decimal.Decimal
p=Path(__file__).resolve().parent
ours=json.loads((p/'INDEPENDENT_RESULTS.json').read_text())
parent=json.loads((p.parent/'CONSTRUCTION_RESULT.json').read_text())['CGCG_summary']
rows=ours['summary_CMB']; cases=[]
for label,own,actual in [('Z', [r['Z'] for r in rows], [parent['Z_marginal'][0],parent['Z_median'],parent['Z_marginal'][1]]),('Phi_summary',[r['phi_clock'] for r in rows],[parent['Phi_summary_marginal'][1],parent['Phi_summary_median'],parent['Phi_summary_marginal'][0]]),('chi_summary',[r['chi_clock'] for r in rows],[parent['chi_summary_marginal'][1],parent['chi_summary_median'],parent['chi_summary_marginal'][0]]),('D',[r['D_Mpc'] for r in ours['areas']],parent['D_Mpc']),('area',[r['abs_det_B_Mpc2_at_omega_o_1'] for r in ours['areas']],parent['area_Mpc2'])]:
  for k,(a,b) in enumerate(zip(own,actual)):
    err=abs(D(a)-D(b));assert err < D('1e-57')
    cases.append({'quantity':label,'index':k,'absolute_error':str(err),'pass':True})
for k,v in [('distance_Mpc','1.5'),('systemic_optical_velocity_km_s','1.7')]:
  assert D(parent['XI_separate_model_choice_systematic'][k])==D(v)
  cases.append({'quantity':k,'expected':v,'pass':True})
result={'all_pass':True,'cases':cases,'count':len(cases),'maximum_absolute_error':str(max(D(q.get('absolute_error','0')) for q in cases)),'interpretation':'Pre-repair independent output keys phi_clock/chi_clock are arithmetic names only; repaired interpretation is transformed systemic summary until reference-clock/branch bridge exists. No implicit physical identification.','parent_code_read':False,'scope':'Saved numerical values only; parent analytic/numerical methodology not replayed here.'}
(p/'SAVED_RESULT_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':True,'cases':len(cases),'maximum_absolute_error':result['maximum_absolute_error']}))
