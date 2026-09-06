"""Read-only aggregator for already captured review evidence."""
import argparse, json, pathlib
p=argparse.ArgumentParser();p.add_argument('--artifacts',type=pathlib.Path,required=True)
a=p.parse_args(); d=a.artifacts
expected={'drop_Hu_connection':'variable_profile_connection','drop_dual':'full_B_coefficient',
 'force_closed':'cubic_nonclosure_guard','inverse_metric_weight':'conversion_homothety_weight',
 'gauge_linear_force':'full_linear_term_gauge_removal'}
rows=[]
for name,guard in expected.items():
    stem='stage_b_mutant_'+name
    meta=json.loads((d/(stem+'.json')).read_text())
    err=(d/(stem+'.stderr')).read_text()
    guards=[line.split('AssertionError: ',1)[1] for line in err.splitlines() if line.startswith('AssertionError: ')]
    assert meta['returncode']==1 and guards==[guard],(name,meta,guards)
    assert (d/(stem+'.stdout')).read_bytes()==b''
    rows.append({'mutation':name,'observed_first_guard':guards[0],**meta})
for stem in ['stage_b_auth_candidate','stage_b_auth_source','stage_b_author_baseline',
             'stage_b_author_byte_compare','stage_b_author_tensors','stage_b_independent_compare']:
    meta=json.loads((d/(stem+'.json')).read_text());assert meta['returncode']==0
baseline=json.loads((d/'stage_b_author_baseline.stdout').read_text())
assert baseline['group_count']==19
assert json.loads((d/'stage_b_independent_compare.stdout').read_text())['status']=='PASS'
print(json.dumps({'status':'PASS','baseline_guard_groups':19,'all_five_actual_first_guards_matched':True,
                  'mutants':rows,'evidence_type':'Author replays are regression; independent comparison is separately recorded'},indent=2))
