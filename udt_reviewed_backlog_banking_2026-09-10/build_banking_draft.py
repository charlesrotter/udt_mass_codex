"""Freeze reviewed claim transcriptions and exact additive rows, before integration checks.

Not a theorem checker. Original scientific sources and reviews own each statement.
This script writes only this banking package and refuses to overwrite its freeze.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BASE='f5faabb43a582fec9a71c1d4a3b065efffae25bd'
SOURCE=str(HERE.relative_to(ROOT)/'BANKING_RECORD.md')
ORDER=['CP1','HB2','HB3','BI2','BI3','NR1','NR2','LG1','LG2','LE1','SE1','NE1',
       'ND1','ND2','QC1','QC2','GL1','GL2','RF1','NCI1','DCI1','KTI1','ER1',
       'TM1','TM2','CO1','CO2','RD1','LC2','FW2']
IDMAP={name:f'G{383+i}' for i,name in enumerate(ORDER)}
TERMS=['chosen_constant_wave_curvature_phase_current_application',
       'weighted_hopf_ricci_projector_first_drift','weighted_hopf_closed_leaf_persistence_class',
       'berger_homogeneous_hopf_preservation_and_descent','berger_local_matched_first_jet_line_departure',
       'compact_mode_quadratic_realizability_obstruction','compact_mode_exact_local_analytic_realizability',
       'localized_constraint_adjoint_kernel_and_balances','localized_exact_constraint_completion',
       'localized_development_curvature_decay_and_anisotropy','spatial_curvature_anisotropy_evolution',
       'exact_polarized_nonlinear_ripple_geometry','static_spherical_response_discrimination',
       'nonlinear_response_tangent_integrability','controlled_static_angular_readout_bounds',
       'static_uniform_readout_bound_counterexamples','weighted_leading_response_estimate',
       'conditional_regular_metric_einstein_necessity_limit','intrinsic_realizable_normal_jet_response_expansion',
       'null_clock_endpoint_scalar_integrability','directional_clock_timelike_curvature_factorization',
       'stationary_kernel_shift_twist_information','exact_coupled_metric_kernel_finite_realization',
       'conditional_gradiometer_tidal_interface','fixed_linear_scalar_identifiability_and_unused_tests',
       'conditional_wave_geometry_and_network_null_relation','fixed_query_detector_network_design_control',
       'bounded_waveform_prediction_and_response_design','conditional_published_local_clock_benchmark',
       'frozen_offsource_finite_procedure_sensitivity_failure']

def sha(data): return hashlib.sha256(data).hexdigest()
def normal(x):
    key=x.get('id',x.get('candidate'))
    if key in ('original_curvature_recipe','ORIGINAL_CURVATURE_RECIPE','CURVATURE_RECIPE','CPC1'):key='CP1'
    art=x.get('artifacts',x.get('controlling_artifacts',[]))
    if isinstance(art,dict):art=list(art.values())
    art=art+x.get('whole_repair_closeout_and_history_artifacts',[])
    art=list({a['path']:a for a in art}.values())
    for a in art:
        if sha((ROOT/a['path']).read_bytes())!=a['sha256']:
            raise SystemExit('Source artifact changed: '+a['path'])
    deps=x.get('required_candidate_ids',x.get('required_candidate_dependencies',[]))
    strict=[d for d in deps if ':' not in d]
    # The explicitly annotated method/provenance links do not become scientific premises.
    links=[d for d in deps if ':' in d]
    strict+=x.get('required_control_candidate_ids',[])
    sources=x.get('required_source_ids',x.get('required_existing_source_ids',[]))
    result=dict(id=key,statement=x['statement'],assumptions=x['assumptions'],
                exclusions=x.get('exclusions',x.get('excluded_inferences',[])),
                history=x.get('history',x.get('review_and_repair_history',[])),
                required_source_ids=sources,required_candidate_ids=strict,
                method_or_provenance_candidate_links=links,
                source_roles=x.get('source_roles',x.get('methods_or_controls_not_separate_physical_premises',[])),
                artifacts=art,source_assessment=x)
    return result

all_claims=[]
for relative in sys.argv[1:]:
    data=json.loads((HERE/relative).read_text())
    for x in data['candidates']:
        c=normal(x);c['banking_assessment_path']=str(HERE.relative_to(ROOT)/relative)
        all_claims.append(c)
by_key={x['id']:x for x in all_claims}
if len(by_key)!=len(all_claims) or set(by_key)!=set(ORDER):
    raise SystemExit(f'Candidate membership mismatch: missing={set(ORDER)-set(by_key)}, extra={set(by_key)-set(ORDER)}')
baseline=subprocess.run(['git','show',BASE+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT,
                        capture_output=True,check=True).stdout
if (ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()!=baseline:
    raise SystemExit('Freeze requires unchanged baseline registry.')
oldrows=list(csv.DictReader(io.StringIO(baseline.decode()),delimiter='\t'))
fields=list(oldrows[0]);oldids={r['premise_id'] for r in oldrows}
if len(oldrows)!=len(oldids) or len(oldids)!=365:raise SystemExit('Baseline row count/uniqueness')
claims=[];newrows=[];accepted=set(oldids)
common_limit=('Physical identification remains OPEN; G166 native assembly is OPEN; G176 remains WORKING; '
              'G312 GR is FILTER ONLY and response-class membership is unclosed. '
              'No physical metric/equation/observer/population/history/scale selection or canon follows.')
common_guard=('Conditional mathematical or design/benchmark scope called physical adoption, empirical certification or canon; '
              'supplied data or optional equation called derived native UDT; old failures, excluded false passes or LOST evidence erased; '
              'review/check counts or checksums called proof; source credit or reused methods called independent confirmation; '
              'configured model called runtime-attested or different-model independence inferred.')
for key,term in zip(ORDER,TERMS):
    c=by_key[key];pid=IDMAP[key]
    required=list(dict.fromkeys(c['required_source_ids']+[IDMAP[d] for d in c['required_candidate_ids']]))
    if not set(required)<=accepted:raise SystemExit(f'{key} unknown/forward dependency {set(required)-accepted}')
    category={'CO2':'BANKED_CONDITIONAL_DESIGN_CONTROL',
              'LC2':'BANKED_CONDITIONAL_PUBLISHED_SUMMARY_BENCHMARK',
              'FW2':'BANKED_REVIEWED_FINITE_PROCEDURE_RESULT'}.get(key,'BANKED_DERIVED_CONDITIONAL')
    grade=category+'__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON'
    c.update(premise_id=pid,term=term,grade=grade,required_registry_ids=required)
    row=dict(premise_id=pid,term=term,current_status=grade,epistemic_label='MIXED',
             active_use=key+'; ENTIRE frozen statement and controlling reviews/repairs. '+c['statement']+
                        ' HYPOTHESES: '+'; '.join(c['assumptions']),
             open_scope=common_limit+' '+'; '.join(c['exclusions']),
             forbidden_regression=common_guard,
             controlling_source=SOURCE,
             precedence_rule=f'{pid} accepts only {key} at its exact frozen scope; required registry IDs: '+
                 ','.join(required)+'; BANKED_CLAIMS.json distinguishes required premises from methods/controls/source credit. '+
                 'ENTIRE original candidate, review, repairs, exclusions and discovery history remain controlling. '+
                 'Fresh separate-context banking fidelity is not blind reproof; runtime model/version UNATTESTED; '+
                 'different-model/human/formal axes UNTESTED. LIVE then exact registry then banking record and immutable sources; conflict means STOP.')
    for v in row.values():
        if '\n' in v or '\t' in v:raise SystemExit('Unexpected multiline registry field')
    claims.append(c);newrows.append(row);accepted.add(pid)

buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=fields,delimiter='\t',lineterminator='\n')
w.writeheader();w.writerows(newrows)
for name,data in [('BASELINE_REGISTRY.tsv',baseline),('BANKED_ROWS.tsv',buf.getvalue().encode()),
                  ('BANKED_CLAIMS.json',(json.dumps(dict(baseline_head=BASE,baseline_registry_sha256=sha(baseline),
                     original_row_count=365,new_row_count=len(claims),claims=claims),indent=2)+'\n').encode())]:
    with (HERE/name).open('xb') as f:f.write(data)
print('Frozen draft:',len(claims),'claims;',365+len(claims),'prospective registry rows.')
