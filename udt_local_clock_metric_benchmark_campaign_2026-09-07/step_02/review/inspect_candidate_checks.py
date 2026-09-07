"""Post-seal candidate replay, independent-output comparison and hostile checks."""
import copy
import hashlib
import importlib.util
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
STEP = HERE.parent
CODE = STEP / 'evaluate_benchmark.py'
assert hashlib.sha256(CODE.read_bytes()).hexdigest() == '27c87e02c3cc2591b6735ef80e9fb40161cbf234733263600105271db2d65240'
assert hashlib.sha256((STEP/'benchmark_run.stdout').read_bytes()).hexdigest() == '94f823ad0475c487f412d0ef0d3871d505a78e914da47f40825904465e77d1b8'
spec = importlib.util.spec_from_file_location('lc2_candidate_review', CODE)
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
data = candidate.load_inputs()
recomputed = candidate.evaluate(data)
candidate.validate(data,recomputed)
saved = json.loads((STEP/'benchmark_run.stdout').read_text())
assert recomputed == saved['result'], 'candidate replay differs from saved output'
assert candidate.catch_proofs(data,recomputed) == saved['catch_proofs'], 'catch proof replay differs'
independent = json.loads((HERE/'source_first_run.stdout').read_text())
comparisons = []

def match(label, actual, expected):
    # Local float equivalence, not experimental tolerance. No order-one absolute
    # tolerance for m^-1 values: require relative agreement down to their scale.
    af, ef = float(actual), float(expected)
    assert math.isclose(af,ef,rel_tol=5e-15,abs_tol=0), (label,af,ef)
    comparisons.append({'quantity':label,'candidate':af,'independent':ef})

for dest, src in [('reference','mu_U'),('residual','D_U'),('zero_mismatch_displacement','zero_mismatch_b0_U')]:
    match(dest,recomputed[dest],independent[src]['float'])
for name in ('Q','C'):
    key = name+'_upper_SD_U'
    expected = independent[key] if name == 'Q' else independent[key]['float']
    match(name+'_width',recomputed['bands'][name]['width'],expected)
    endpoints = independent['nominal_'+name+'_band_U']
    match(name+'_lower',recomputed['bands'][name]['lower'],endpoints[0])
    match(name+'_upper',recomputed['bands'][name]['upper'],endpoints[1])
    tk = 'all_shift_threshold_'+name+'_U'
    threshold = independent[tk] if name=='Q' else independent[tk]['float']
    match(name+'_threshold',recomputed['bands'][name]['all_displacements_threshold'],threshold)
    assert recomputed['bands'][name]['zero_in_band'] is True
co = recomputed['clock_only']
for dest,src in [('effective_linear_kappa_up_per_m','kappa_up_per_m'),('standard_uncertainty_per_m','kappa_SD_per_m'),('equivalent_support_acceleration_m_s2','a_clock_m_s2'),('standard_uncertainty_acceleration_m_s2','a_clock_SD_m_s2')]:
    match(dest,co[dest],independent[src]['float'])
match('clock_band_lower',co['band_lower_per_m'],independent['kappa_band_per_m'][0])
match('clock_band_upper',co['band_upper_per_m'],independent['kappa_band_per_m'][1])
for row,other in zip(recomputed['diagnostic_displacements'],independent['scenarios']):
    match('shift_center_'+row['multiplier'],row['center'],other['D_plus_b']['float'])
    assert row['Q_zero_in_shifted_band'] == other['Q_zero_inclusion_exact_squared_comparison']
    assert row['C_zero_in_shifted_band'] == other['C_zero_inclusion_exact_comparison']

hostile = []
def probe(label, mutant, expected_guard=None):
    try:
        candidate.validate(data,mutant)
    except AssertionError as err:
        hostile.append({'case':label,'rejected':True,'guard':str(err)})
        if expected_guard is not None:
            assert str(err)==expected_guard
    else:
        hostile.append({'case':label,'rejected':False,'guard':None})

# Recreate the seven defects independently rather than trusting returned labels.
r=copy.deepcopy(recomputed);r['reference']=str(-candidate.D(r['reference']));probe('sign',r,'reference sign')
r=copy.deepcopy(recomputed);r['reference']=str(candidate.D(r['reference'])*100);probe('cm_omitted',r,'inverse dimension/sign mapping')
r=copy.deepcopy(recomputed);r['measurement_standard_uncertainty']='0.7';probe('statistical_only',r,'stat-only/double-counted uncertainty')
r=copy.deepcopy(recomputed);r['experiment_count']=2;probe('duplicate',r,'duplicate experiment')
r=copy.deepcopy(recomputed);r['reference_origin']='clock_target';r['reference']=r['y'];probe('target_reference',r,'target-derived reference')
r=copy.deepcopy(recomputed)
for row in r['diagnostic_displacements']:
    for name in ('Q','C'):
        oldlo=candidate.D(r['bands'][name]['lower']);oldhi=candidate.D(r['bands'][name]['upper'])
        row[name+'_zero_in_shifted_band'] = oldlo <= candidate.D(row['center']) <= oldhi
probe('literal_old_center_rule',r,'R1 moving-band criterion')
r=copy.deepcopy(recomputed);r['error_hard_bound_or_confidence_coverage_claimed']=True;probe('hard_coverage',r,'unsupported coverage')
# Additional claim-relevant false-pass search, with surviving correct result kept.
r=copy.deepcopy(recomputed);r['clock_only']['standard_uncertainty_acceleration_m_s2']='0.000001';probe('wrong_acceleration_uncertainty',r)
r=copy.deepcopy(recomputed);r['clock_only']['band_lower_per_m']='1.23e-16';r['clock_only']['band_upper_per_m']='1.25e-16';probe('wrong_clock_only_band',r)
r=copy.deepcopy(recomputed);r['zero_mismatch_displacement']='0';probe('wrong_zero_mismatch_displacement',r)
r=copy.deepcopy(recomputed)
negative=-candidate.D(r['bands']['Q']['width']);residual=candidate.D(r['residual'])
r['bands']['Q'].update(width=str(negative),lower=str(residual-negative),upper=str(residual+negative),zero_in_band=False,all_displacements_threshold=None)
for row in r['diagnostic_displacements']:
    row['Q_zero_in_shifted_band']=False
probe('coherent_negative_standard_uncertainty_width',r)
print(json.dumps({'python':sys.version,'source_first_comparisons':comparisons,'candidate_replay_matches_saved':True,'declared_seven_catch_proofs_replayed':True,'hostile_checks':hostile,'interpretation':'Actual result independently agrees; extra false passes identify finite guard coverage gaps, not a wrong benchmark result.'},indent=2))
