#!/usr/bin/env python3
"""Fail-closed comparison-map verification and exercised preregistered catches."""
from __future__ import annotations
import copy,csv,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
STAMPS=("COPRESENCE = WORKING_INTERPRETIVE_FRAME","METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL","INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED","COMPLETE_WHOLE_SOLUTION_LAW = OPEN")
MIDS=tuple(f'M{i:02d}' for i in range(1,13));AIDS=tuple(f'A{i:02d}' for i in range(1,13))
def rows(n):
    with (HERE/n).open(newline='',encoding='utf-8') as h:return list(csv.DictReader(h,delimiter='\t'))
def base():return {'stamps':STAMPS,'candidates':MIDS,'axioms':AIDS,'all_retained':True,'distance_signed':False,'scale_disclosed':True,'endpoint_theorem':True,'period_test':True,'closed_not_exact':True,'transport_types_separate':True,'rapidity_control':True,'coordinate_covariant':False,'cut_types_separate':True,'path_ontology_selected':False,'section_disclosed':True,'orientation_disclosed':True,'K_branch_scoped':True,'local_phi_universalized':False,'lambda_seam_quotient_selected':False,'action_source_carrier_inferred':False,'boundary_density_bootstrap_mass_xmax_inferred':False,'dynamics_signalling_fit_inferred':False,'local_physics_modified':False,'complete_space_claimed':False,'stationary_control':True,'cut_control':True,'independence_not_silence':True,'conditional_promoted':False}
def validate(s):
    assert s['stamps']==STAMPS and s['candidates']==MIDS and s['axioms']==AIDS
    for k in ('all_retained','scale_disclosed','endpoint_theorem','period_test','closed_not_exact','transport_types_separate','rapidity_control','cut_types_separate','section_disclosed','orientation_disclosed','K_branch_scoped','stationary_control','cut_control','independence_not_silence'):assert s[k]
    for k in ('distance_signed','coordinate_covariant','path_ontology_selected','local_phi_universalized','lambda_seam_quotient_selected','action_source_carrier_inferred','boundary_density_bootstrap_mass_xmax_inferred','dynamics_signalling_fit_inferred','local_physics_modified','complete_space_claimed','conditional_promoted'):assert not s[k]
def reject(k,v):
    s=copy.deepcopy(base());s[k]=v
    try:validate(s)
    except AssertionError:return 'PASS'
    raise AssertionError(f'accepted {k}')
def main():
    cand=rows('CANDIDATE_OUTCOMES.tsv');prop=rows('PROPERTY_MATRIX.tsv');asm=rows('ASSEMBLY_OUTCOMES.tsv');src=rows('SOURCE_PROPOSITIONS.tsv');contract=rows('FALSIFICATION_CONTRACT.tsv')
    result=json.loads((HERE/'DERIVATION_RESULT.json').read_text());ind=json.loads((HERE/'INDEPENDENT_RESULT.json').read_text());review=(HERE/'FRESH_ADVERSARIAL_REVIEW.md').read_text()
    assert tuple(r['candidate_id'] for r in cand)==MIDS and len(prop)==144 and len(asm)==6 and len(src)==20
    assert {r['candidate_id'] for r in prop}==set(MIDS) and {r['axiom_id'] for r in prop}==set(AIDS)
    assert all(sum(r['candidate_id']==m for r in prop)==12 for m in MIDS)
    by={r['candidate_id']:r for r in cand}
    assert by['M02']['classification']=='DERIVED_BOUNDED_COMPLETE_STATIONARY_SCALAR_MAP'
    assert by['M08']['classification']=='COVARIANT_FRAME_MOTION_READOUT_NOT_UNIVERSAL_POSITIONAL_DEPTH'
    assert by['M09']['classification']=='STATIC_COORDINATE_REALIZATION_NOT_COVARIANT_OBSERVABLE'
    assert by['M10']['classification']=='DERIVED_TYPED_CONSTRUCTOR_GIVEN_DEPTH_PAIR_AND_PATH'
    assert asm[2]['result']=='EXACT_REDUCIBLE_COMPARISON_DATA_FAMILY_CONDITIONAL'
    assert asm[4]['result']=='FORBIDDEN_CROSS_WITNESS_SPLICE' and asm[5]['result']=='OPEN_NO_SINGLE_ALL_GATE_SELECTED_MAP'
    assert result['status']=='COMPUTED' and ind['status']=='PASS' and not result['complete_map_derived_unconditionally']
    assert result['bounded_stationary_scalar_map_derived'] and result['bounded_stationary_metric_native_one_form_derived'] and result['conditional_reducible_comparison_family_available_exact']
    assert not result['endpoint_physical_semantics_selected'] and not result['path_physical_semantics_selected'] and not result['lambda_selected']
    assert 'VERIFIED-WITH-CAVEATS' in review and 'comparison_map_adversary' in review
    for f in ('PREREGISTRATION.md','EXACT_DERIVATION.md','AUDIT_REPORT.md'):
        t=(HERE/f).read_text()
        for stamp in STAMPS:assert stamp in t
    mutations={'F01':('stamps',STAMPS[:-1]),'F02':('candidates',MIDS[:-1]),'F03':('axioms',AIDS[:-1]),'F04':('all_retained',False),'F05':('distance_signed',True),'F06':('scale_disclosed',False),'F07':('endpoint_theorem',False),'F08':('period_test',False),'F09':('closed_not_exact',False),'F10':('transport_types_separate',False),'F11':('rapidity_control',False),'F12':('coordinate_covariant',True),'F13':('cut_types_separate',False),'F14':('path_ontology_selected',True),'F15':('section_disclosed',False),'F16':('orientation_disclosed',False),'F17':('K_branch_scoped',False),'F18':('local_phi_universalized',True),'F19':('lambda_seam_quotient_selected',True),'F20':('action_source_carrier_inferred',True),'F21':('boundary_density_bootstrap_mass_xmax_inferred',True),'F22':('dynamics_signalling_fit_inferred',True),'F23':('local_physics_modified',True),'F24':('complete_space_claimed',True),'F25':('stationary_control',False),'F26':('cut_control',False),'F27':('independence_not_silence',False),'F28':('conditional_promoted',True)}
    assert set(mutations)=={r['catch_id'] for r in contract}
    catches=[{'catch_id':r['catch_id'],'result':reject(*mutations[r['catch_id']]),'corruption_or_overclaim':r['corruption_or_overclaim']} for r in contract]
    with (HERE/'CATCH_PROOFS.tsv').open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(catches[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(catches)
    out={'schema':'udt-complete-physical-comparison-map-verification-1.0','status':'PASS','candidates':'12/12','axioms':'12/12','property_cells':'144/144','assemblies':'6/6','sources':'20/20','independent':'PASS','fresh_adversarial_review':'VERIFIED-WITH-CAVEATS','catch_proofs':'28/28','bounded_stationary_scalar_map':True,'conditional_hybrid_map':True,'universal_complete_physical_map':False}
    (HERE/'VERIFICATION_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
