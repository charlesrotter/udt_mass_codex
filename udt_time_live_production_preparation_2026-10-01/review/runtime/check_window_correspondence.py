"""Recompute selected clock-window correspondence directly from saved fields."""
import hashlib,json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
queries=json.loads((HERE/'LATE_CLOCK_QUERIES.json').read_text());rows=[]
for case in queries['cases']:
    path=ROOT/case['history'];manifest=json.loads(path.with_suffix('.sources.json').read_text())
    assert manifest['history_sha256']==sha(path)
    records=[]
    for source,value in manifest['source_sha256'].items():
        file=ROOT/source;assert sha(file)==value
        if file.name=='metadata.json':records.append((json.loads(file.read_text()),file.parent))
    records.sort(key=lambda row:row[0]['step'])
    with np.load(path,allow_pickle=False) as history:
        assert len(records)==len(history['times'])
        for i,(meta,folder) in enumerate(records):
            assert (folder/'COMMITTED').read_text().strip()==sha(folder/'metadata.json')
            assert meta['payload_sha256']==sha(folder/'state.npz') and meta['eligible_for_resume']
            assert history['times'][i]==meta['t']
            with np.load(folder/'state.npz',allow_pickle=False) as checkpoint:
                assert np.array_equal(history['g'][i],checkpoint['state'][0])
                assert np.array_equal(history['v'][i],checkpoint['state'][1])
        delta=np.diff(history['times']);assert np.max(abs(delta-delta[0]))<1e-14
        rows.append(dict(name=case['name'],history_sha256=sha(path),manifest_sha256=sha(path.with_suffix('.sources.json')),
            frames=len(records),first=float(history['times'][0]),last=float(history['times'][-1]),
            all_g_v_bitwise_equal_to_committed_payloads=True))
print(json.dumps(dict(status='SELECTED_WINDOW_CORRESPONDENCE_PASS',rows=rows,
    scope='Independent exact correspondence and marker/payload hashes; numerical equations checked separately.'),indent=2))
