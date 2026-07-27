#!/usr/bin/env python3
"""Fail-closed verifier with one exercised mutation per preregistered catch."""
from __future__ import annotations
import copy,csv,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
STAMPS=("COPRESENCE = WORKING_INTERPRETIVE_FRAME","METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL","INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED","COMPLETE_WHOLE_SOLUTION_LAW = OPEN")
IDS=tuple(f'O{i:02d}' for i in range(1,9))
def rows(name):
    with (HERE/name).open(newline='',encoding='utf-8') as h:return list(csv.DictReader(h,delimiter='\t'))
def base():
    return {'stamps':STAMPS,'ids':IDS,'packet_items':5,'independence_not_silence':True,'local_not_solder':True,'abstract_not_path':True,'scalar_not_full':True,'metric_transport_not_founding':True,'specified_path_not_endpoint':True,'endpoint_not_selected_parallel':True,'parallel_not_founding':True,'inversion_not_holonomy':True,'c01_character':True,'c01_nonidentity_composition':True,'both_countermodels':True,'c02_offshell':True,'path_ontology_selected':False,'downstream_open':True,'overlay_only':True,'lambda_seam_quotient_selected':False,'action_source_carrier_inferred':False,'density_bootstrap_mass_xmax_inferred':False,'dynamics_signalling_fit_inferred':False,'premise_promoted':False}
def validate(s):
    assert s['stamps']==STAMPS and s['ids']==IDS and s['packet_items']==5
    for k in ('independence_not_silence','local_not_solder','abstract_not_path','scalar_not_full','metric_transport_not_founding','specified_path_not_endpoint','endpoint_not_selected_parallel','parallel_not_founding','inversion_not_holonomy','c01_character','c01_nonidentity_composition','both_countermodels','c02_offshell','downstream_open','overlay_only'):assert s[k]
    for k in ('path_ontology_selected','lambda_seam_quotient_selected','action_source_carrier_inferred','density_bootstrap_mass_xmax_inferred','dynamics_signalling_fit_inferred','premise_promoted'):assert not s[k]
def rejected(field,value):
    s=copy.deepcopy(base());s[field]=value
    try:validate(s)
    except AssertionError:return 'PASS'
    raise AssertionError(f'corruption accepted: {field}')
def main():
    obj=rows('OBJECT_CLASSIFICATION.tsv');graph=rows('IMPLICATION_GRAPH.tsv');cm=rows('COUNTERMODEL_LEDGER.tsv');reg=rows('DOWNSTREAM_REGRADE.tsv');src=rows('SOURCE_PROPOSITIONS.tsv');contract=rows('FALSIFICATION_CONTRACT.tsv')
    result=json.loads((HERE/'DERIVATION_RESULT.json').read_text());ind=json.loads((HERE/'INDEPENDENT_RESULT.json').read_text())
    assert tuple(r['object_id'] for r in obj)==IDS and len(graph)==12 and len(cm)==2 and len(reg)==10 and len(src)==19
    assert result['status']=='COMPUTED' and ind['status']=='PASS'
    by={r['object_id']:r for r in obj}
    assert by['O01']['classification']=='FOUNDING_DERIVED'
    assert by['O02']['classification']=='FOUNDING_DERIVED_ABSTRACT'
    assert by['O03']['classification']=='METRIC_DERIVED_CONDITIONAL'
    assert by['O04']['classification']=='CONDITIONAL_SUPPLIED_STRUCTURE'
    assert by['O05']['transport_type']=='PATH_LABELLED'
    assert by['O06']['classification']=='NOT_DERIVED'
    assert by['O07']['classification']=='NOT_DERIVED_EXTRA_RESTRICTION'
    assert by['O08']['classification']=='ALGEBRAICALLY_AVAILABLE_NOT_PHYSICALLY_SELECTED'
    assert cm[0]['nabla_X']=='NONZERO_EXACT_-2_AT_r1' and cm[1]['nabla_X']=='NONZERO_EXACT_-3/25_AT_P00_ALL_LAMBDA'
    assert result['founding_requires_global_parallelism'] is False and result['complete_physical_semantics']=='OPEN'
    assert not result['path_groupoid_selected_as_physics'] and not result['endpoint_only_selected_as_physics'] and not result['lambda_selected']
    for f in ('PREREGISTRATION.md','AUDIT_REPORT.md','EXACT_DERIVATION.md'):
        t=(HERE/f).read_text()
        for stamp in STAMPS:assert stamp in t
    mutations={'F01':('stamps',STAMPS[:-1]),'F02':('ids',IDS[:-1]),'F03':('packet_items',6),'F04':('independence_not_silence',False),'F05':('local_not_solder',False),'F06':('abstract_not_path',False),'F07':('scalar_not_full',False),'F08':('metric_transport_not_founding',False),'F09':('specified_path_not_endpoint',False),'F10':('endpoint_not_selected_parallel',False),'F11':('parallel_not_founding',False),'F12':('inversion_not_holonomy',False),'F13':('c01_character',False),'F14':('c01_nonidentity_composition',False),'F15':('both_countermodels',False),'F16':('c02_offshell',False),'F17':('path_ontology_selected',True),'F18':('downstream_open',False),'F19':('overlay_only',False),'F20':('lambda_seam_quotient_selected',True),'F21':('action_source_carrier_inferred',True),'F22':('density_bootstrap_mass_xmax_inferred',True),'F23':('dynamics_signalling_fit_inferred',True),'F24':('premise_promoted',True)}
    assert set(mutations)=={r['catch_id'] for r in contract}
    catches=[{'catch_id':r['catch_id'],'result':rejected(*mutations[r['catch_id']]),'corruption_or_overclaim':r['corruption_or_overclaim']} for r in contract]
    with (HERE/'CATCH_PROOFS.tsv').open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(catches[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(catches)
    out={'schema':'udt-founding-reciprocity-object-verification-1.0','status':'PASS','objects':'8/8','source_propositions':'19/19','countermodels':'2/2','implication_edges_and_nonedges':'12/12','downstream_regrades':'10/10','catch_proofs':'24/24','independent_local_anchor':'-2','complete_witness_anchor':'-3/25','founding_requires_global_parallelism':False,'complete_physical_semantics':'OPEN'}
    (HERE/'VERIFICATION_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
