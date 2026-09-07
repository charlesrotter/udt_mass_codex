"""Preserve numerical explanation of reviewer direct-summation failure."""
import json
from pathlib import Path
import numpy as np
import independent_operator as new
import INITIAL_independent_operator as old

repo = Path(__file__).resolve().parents[3]
d = json.loads((repo/'udt_complementary_wave_observable_campaign_2026-09-07/step_02/design_run.stdout').read_text())
b = new.nullrow(np.array(d['F_HLV_plus_cross']))
tau = np.array(d['arrival_minus_geocenter_seconds'])
rows = []
for start in (1187010216,1187011516):
    assert start-4 >= 1187008980
    raw = np.array([np.fromfile(f'/tmp/udt-gw170817-fixed-window-xshnIR/offsource/{det}_{start}_98s_f64le.bin',dtype='<f8')*1e21 for det in ('H1','L1','V1')])
    core = new.residual(raw,tau,b)
    bins = np.array([30*90,61*90,137*90,500*90])
    fast = np.fft.fft(core*new.HANN)[bins]
    old_rel = float(np.linalg.norm(old.direct_bins(core,bins)-fast)/np.linalg.norm(fast))
    new_rel = float(np.linalg.norm(new.direct_bins(core,bins)-fast)/np.linalg.norm(fast))
    assert new_rel < 1e-10
    rows.append({'core':start,'unreduced_argument_relative_error':old_rel,
                 'integer_modular_argument_relative_error':new_rel})
assert any(row['unreduced_argument_relative_error'] >= 1e-10 for row in rows)
print(json.dumps({'reviewer_only_failure':True,'same_Fourier_sum_no_tolerance_relaxation':True,
                  'physical_claim':False,'rows':rows},indent=2))
