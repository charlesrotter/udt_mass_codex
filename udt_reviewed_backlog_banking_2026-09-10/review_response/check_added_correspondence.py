"""Adjudicate the observed CO2 runtime-only stdout difference explicitly."""
import hashlib
import json
from pathlib import Path

out=Path(__file__).resolve().parent
repo=out.parent.parent
results=json.loads((out/'METROLOGY_REPLAY_RESULTS.json').read_text())
assert len(results['results'])==8
for row in results['results']:
    assert row['launch_returncode']==0 and row['receipt']['returncode']==0
    assert row['comparison']['.stderr']['byte_identical']
    if row['name']!='CO2':assert row['comparison']['.stdout']['byte_identical']
old_path=repo/'udt_complementary_wave_observable_campaign_2026-09-07/step_02/review/independent_run.stdout'
new_path=out/'replay_added_CO2.stdout'
old=json.loads(old_path.read_text());new=json.loads(new_path.read_text())
assert old.keys()==new.keys()
diff=[k for k in old if old[k]!=new[k]]
assert diff==['python'],diff
assert old['python']=='3.10.12 (main, Jun 22 2026, 18:55:27) [GCC 11.4.0]'
assert new['python']=='3.10.12 (main, Aug 31 2026, 10:18:17) [GCC 11.4.0]'
old_python=old.pop('python');new_python=new.pop('python')
assert old==new
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
print(json.dumps({'status':'PASS_SCIENTIFIC_FIELDS_EXACT_RUNTIME_BUILD_DIFF_DISCLOSED',
    'unchanged_source_execution_passes':8,'whole_stdout_byte_identical':7,
    'CO2_only_different_field':'python','CO2_old_python':old_python,'CO2_current_python':new_python,
    'CO2_remaining_fields_exactly_equal':True,'old_stdout_sha256':sha(old_path),
    'new_stdout_sha256':sha(new_path),'source_outputs_modified':False,
    'exposure':'Comparison rule specified after the one-field difference was observed; no blind prediction claim.'},indent=2,sort_keys=True))
