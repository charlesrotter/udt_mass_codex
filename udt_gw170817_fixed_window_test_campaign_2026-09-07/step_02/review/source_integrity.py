"""Hash-only check of original source and author repeated-extract bytes."""
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
cache = Path('/tmp/udt-gw170817-fixed-window-xshnIR')
meta = json.loads((root.parent/'step_01/metadata_filtered_run.stdout').read_text())
diagnostic = json.loads((root/'diagnostic_run.stdout').read_text())
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024**2),b''):
            h.update(chunk)
    return h.hexdigest()
records = []
for det in ('H1','L1','V1'):
    original = cache/f'{det}_complete.hdf5'
    source_hash = sha(original)
    assert source_hash == meta['files'][det]['sha256']
    repeat = cache/'diagnostic'/f'{det}_1187011516_repeat.bin'
    extract = cache/'offsource'/f'{det}_1187011516_98s_f64le.bin'
    repeated_hash,extract_hash = sha(repeat),sha(extract)
    assert repeated_hash == extract_hash
    saved = next(x for x in diagnostic['records'][1]['raw_statistics'] if x['detector']==det)
    assert extract_hash == saved['original_sha256'] == saved['reextract_sha256']
    records.append({'detector':det,'source_sha256':source_hash,'source_bytes':original.stat().st_size,
                    'original_and_repeated_offsource_sha256':extract_hash})
print(json.dumps({'scope':'whole-file byte hashing only; no HDF5 strain arrays opened or re-extracted',
                  'all_original_sources_match_FW1':True,'all_three_author_repeat_bytes_match':True,
                  'event_samples_read':False,'records':records},indent=2))
