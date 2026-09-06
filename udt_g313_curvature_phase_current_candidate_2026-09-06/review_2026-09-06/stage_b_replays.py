"""Exposed author-code replay only; outputs are generated evidence in review scratch."""
import datetime
import json
import pathlib
import subprocess
import time

scratch = pathlib.Path('/tmp/udt-curvature-review-qassiP')
repo = pathlib.Path('/home/udt-admin/udt_mass_codex')
pkg = repo/'udt_g313_curvature_phase_current_candidate_2026-09-06'
expected = {
 'omit_dual':'full_quadratic_tensor',
 'omit_dual_half':'full_quadratic_tensor',
 'euclidean_contraction':'full_quadratic_tensor',
 'wrong_root_degree':'root_full_fourth_power',
 'past_root':'future_sign_positive_A',
 'differentials_zero':'nonclosed_control',
 'homothety_inverse_frozen':'homothety_raised_current',
 'euclidean_cut_area':'cut_area_A_2',
 'phase_gauge_recreates_mu':'fixed_current_phase_gauge_A_2',
}
records=[]
jobs=[('saved_witness_replay', ['python3','-B',str(pkg/'recompute_saved_witnesses.py')],0,None)]
jobs += [(name,['python3','-B',str(pkg/'check_candidate.py'),'--mutation',name],1,guard)
         for name,guard in expected.items()]
for name,command,wanted,guard in jobs:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    before=time.monotonic()
    result=subprocess.run(command,cwd=repo,capture_output=True,text=True,timeout=60)
    elapsed=time.monotonic()-before
    (scratch/f'stage_b_{name}.stdout').write_text(result.stdout)
    (scratch/f'stage_b_{name}.stderr').write_text(result.stderr)
    rec={'name':name,'command':command,'start_utc':start,'elapsed_seconds':elapsed,
         'returncode':result.returncode,'expected_returncode':wanted,
         'expected_guard':guard,'guard_seen':guard is None or f'AssertionError: {guard}' in result.stderr}
    records.append(rec)
    print(json.dumps(rec),flush=True)
    assert result.returncode == wanted and rec['guard_seen'],rec
(scratch/'STAGE_B_REPLAY_RESULTS.json').write_text(json.dumps(records,indent=2)+'\n')
