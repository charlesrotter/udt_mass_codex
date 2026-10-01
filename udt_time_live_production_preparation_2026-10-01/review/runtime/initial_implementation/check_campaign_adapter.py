"""Regression of refactored extraction and actual supervised receipt bridge.

This is author's regression evidence, not independent review of the new adapter.
The parent performs a separate source review. Temporary duplicate Kasner arrays
are written only under/tmp; original arrays are never overwritten.
"""
import hashlib,json,sys,tempfile
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
sys.path.insert(0,str(BASE))
from assemble_windows import assemble
from assemble_campaign import extract
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
temp=Path(tempfile.mkdtemp(prefix='tpp1_assembler_regression_',dir='/tmp'))
rows=assemble('kasner_n16_half',out=temp)
for row in rows:
    new=Path(row['path']);old=BASE/'histories'/new.name
    with np.load(new,allow_pickle=False) as a,np.load(old,allow_pickle=False) as b:
        assert set(a.files)==set(b.files)
        for key in a.files:assert np.array_equal(a[key],b[key]),(new,key)
manifest=BASE/'supervisor_smoke/pause.json';runtime=BASE/'supervisor_smoke/runtime_pause'
analysis=BASE/'supervisor_smoke/analysis'
first=extract(manifest,runtime,analysis);second=extract(manifest,runtime,analysis)
assert len(first['results'])==2 and not any(row['reused'] for row in first['results'])
assert len(second['results'])==2 and all(row['reused'] for row in second['results'])
for row in first['results']:
    record=json.loads(Path(row['record']).read_text());assert len(record['windows'])==1
    path=ROOT/record['windows'][0]['path']
    # Compare every extracted supervised frame against the original uninterrupted
    # engineering trajectory at the same tick, independently of adapter metadata.
    baseline={json.loads(p.read_text())['step']:p.parent for p in (BASE/'runs/engineering_full').glob('checkpoints/*/metadata.json')}
    with np.load(path,allow_pickle=False) as data:
        for i,t in enumerate(data['times']):
            tick=round((t-1)/.0003125)
            with np.load(baseline[tick]/'state.npz',allow_pickle=False) as original:
                assert np.array_equal(data['g'][i],original['state'][0])
                assert np.array_equal(data['v'][i],original['state'][1])
print(json.dumps(dict(status='CAMPAIGN_ADAPTER_REGRESSION_PASS',kasner_windows=len(rows),
    all_kasner_arrays_bitwise_equal=True,supervised_window_frames_equal_to_original=True,
    first_assembly=first,idempotent_reuse=second,temporary_output=str(temp),
    sources={str(p.relative_to(ROOT)):sha(p) for p in [BASE/'assemble_windows.py',BASE/'assemble_campaign.py',BASE/'prepare_campaign.py']},
    scope='Author regression with actual supervisor receipts; separate parent review required. No new production data orGPU launched.'),indent=2))
